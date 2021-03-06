import argparse
import asyncio
import json
import logging
import os
import subprocess
import time
import uuid
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import aiohttp
import dateparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from assignment2.converters import string_to_logging_level


def find_chrome_driver() -> str:
    p = subprocess.run("which -a chromedriver", shell=True, stdout=subprocess.PIPE)
    return p.stdout.decode().rstrip(os.linesep)


def load_xpath_templates_from_json():
    with open("xpath_config.json") as json_file:
        xpath_templates = json.load(json_file)

    return xpath_templates


def generate_uuid():
    return str(uuid.uuid1().hex)


def serialize_output_string(parsed_data: Dict[str, str]) -> str:
    sequence = [
        "post_url",
        "username",
        "user_karma",
        "user_cake_day",
        "post_karma",
        "comment_karma",
        "post_date",
        "comments_number",
        "votes_number",
        "post_category",
    ]

    output_string = generate_uuid()
    for field in sequence:
        output_string = ";".join([output_string, parsed_data[field]])

    return output_string


def config_browser(chrome_drive_path: str) -> webdriver.Chrome:
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"  # possible: "normal", "eagle", "none"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--no-proxy-server")

    return webdriver.Chrome(
        chrome_drive_path, options=options, desired_capabilities=caps
    )


def get_posts_list(html, xpath_templates):
    soup = BeautifulSoup(html, "lxml")
    all_posts_html = soup.select_one(xpath_templates["all_posts_block"])

    return all_posts_html.find_all("div", class_="Post")


def config_logger(log_level: int) -> logging.Logger:
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("reddit_parser")
    logger.setLevel(log_level)
    return logger


def parse_publication_date(tag_with_date):
    publish_date = tag_with_date.get_text()
    days_ago = int(publish_date.split(" ")[0])
    post_date = datetime.today() - timedelta(days=days_ago)
    return str(post_date.date())


def parse_comment_number(post, xpath_templates):
    comments_number = post.select_one(
        xpath_templates["comments_number_inside_post"]
    ).find_all(recursive=False)[-1]
    comments_number = comments_number.select("a > span")

    # Representation may have distinct html formats
    if len(comments_number) == 1:
        return comments_number[0].get_text().split(" ")[0]
    else:
        return (
            comments_number[0]
            .select_one("div")
            .find_all(recursive=False)[-1]
            .get_text()
        )


def hover_current_post_element(browser, element):
    hover = webdriver.ActionChains(browser).move_to_element(element)
    hover.perform()


def parse_main_page(current_post_info, post, post_id, logger, xpath_templates):
    current_post_info["votes_number"] = post.select_one(
        xpath_templates["votes_number_inside_post"]
    ).get_text()

    top_post_html_source = post.select_one(
        xpath_templates["top_post_line_block"]
    ).findChildren(recursive=False)[0]
    if top_post_html_source.name == "article":
        top_post_html_source = top_post_html_source.select_one(
            xpath_templates["article_shell"]
        )
    else:
        top_post_html_source = top_post_html_source.select_one(
            xpath_templates["div_shell"]
        )

    all_a_tags_inside_block = top_post_html_source.find_all("a")
    current_post_info["post_url"] = all_a_tags_inside_block[-1]["href"]
    current_post_info["post_category"] = (
        top_post_html_source.select_one(xpath_templates["post_category"])
        .get_text()
        .lstrip("r/")
    )

    # User deleted
    if len(all_a_tags_inside_block) == 2:
        logger.debug(
            f"The post (post_id: {post_id}, url: {current_post_info['post_url']}) "
            f"exists, but the user has been deleted!"
        )
        return None

    name_parse_string = all_a_tags_inside_block[1]
    current_post_info["username"] = name_parse_string.get_text().lstrip("u/")
    current_post_info["post_date"] = parse_publication_date(all_a_tags_inside_block[-1])
    current_post_info["comments_number"] = parse_comment_number(post, xpath_templates)
    user_page_url = "".join(["https://www.reddit.com", name_parse_string["href"]])

    return user_page_url


def navigate_popup_menu(browser, post_id, current_post_info, logger):
    popup_menu = browser.find_element_by_id(f"UserInfoTooltip--{post_id}")
    popup_menu = popup_menu.find_element_by_xpath("..")
    hover_current_post_element(browser, popup_menu)

    try:
        popup_element = WebDriverWait(browser, 2).until(
            expected_conditions.presence_of_element_located(
                (By.ID, f"UserInfoTooltip--{post_id}-hover-id")
            )
        )
        parse_popup_menu(current_post_info, popup_element)
    except (TimeoutException, StaleElementReferenceException):
        logger.debug(
            f"Popup menu does not appear for this post(url: {current_post_info['post_url']})."
        )
        return None

    return popup_element


def parse_popup_menu(current_post_info, popup_element):
    popup_menu_info = (
        BeautifulSoup(popup_element.get_attribute("innerHTML"), "html.parser")
        .findChildren(recursive=False)[-2]
        .findChildren(recursive=False)[-3]
    )

    tags_with_numbers = list(popup_menu_info.children)
    current_post_info["post_karma"] = tags_with_numbers[1].select_one("div").get_text()
    current_post_info["comment_karma"] = (
        tags_with_numbers[2].select_one("div").get_text()
    )


async def get_user_html_from_new_browser_tab(browser, user_page_url, xpath_templates):
    browser.execute_script(f"window.open('{user_page_url}');")
    await asyncio.sleep(1)
    browser.switch_to.window(browser.window_handles[1])
    user_page_html = browser.page_source
    soup = BeautifulSoup(user_page_html, "lxml")
    user_profile_info = soup.select_one(xpath_templates["user_profile_block"])

    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    return user_profile_info


async def parse_user_page(
    browser, user_page_url, current_post, logger, xpath_templates
):
    user_profile_info = await get_user_html_from_new_browser_tab(
        browser, user_page_url, xpath_templates
    )
    try:
        current_post["user_karma"] = user_profile_info.select_one(
            xpath_templates["user_karma"]
        ).get_text()
        user_cake_day = dateparser.parse(
            user_profile_info.select_one(xpath_templates["user_cake_day"]).get_text()
        )

        current_post["user_cake_day"] = str(user_cake_day.date())
    except AttributeError:
        logger.debug(
            f"Failed to access user(link: {user_page_url}) page due to age limit!"
        )

        return False, current_post

    return True, current_post


async def start_user_parsing(browser, source, logger, xpath_templates):
    return await asyncio.gather(
        *[
            parse_user_page(browser, url, value, logger, xpath_templates)
            for url, value in source
        ]
    )


def parse_reddit_page(
    chrome_drive_path: str,
    post_count: int,
    logger: logging.Logger,
    xpath_templates: Dict[str, str],
    condition,
    parsing_queue,
) -> None:
    logger.info(f"Start chrome driver!")
    browser = config_browser(chrome_drive_path)

    try:
        browser.get("https://www.reddit.com/top/?t=month")
        total_posts_count = 0

        while condition["Parsed count"] < post_count:
            current_post_info = {}
            single_posts = get_posts_list(browser.page_source, xpath_templates)
            post = single_posts[total_posts_count]
            post_id = post["id"]

            current_post = browser.find_element_by_id(post_id)
            hover_current_post_element(browser, current_post)

            user_page_url = parse_main_page(
                current_post_info, post, post_id, logger, xpath_templates
            )
            if user_page_url is None:
                total_posts_count += 1
                continue

            popup_element = navigate_popup_menu(
                browser, post_id, current_post_info, logger
            )
            if popup_element is None:
                total_posts_count += 1
                continue

            total_posts_count += 1
            parsing_queue.append([user_page_url, current_post_info])
        else:
            logger.info(f"{post_count} records were successfully placed in the file!")

    except Exception as exception:
        logger.error(exception, exc_info=True)
    finally:
        browser.quit()
        condition["Processing"] = False


async def send_data(url, session, post):
    async with session.post(url, data=json.dumps(post).encode("utf-8")) as response:
        return await response.read()


async def start_sending(parsed_information):
    url = "http://localhost:8087/posts/"
    tasks = []

    async with aiohttp.ClientSession() as session:
        for post in parsed_information:
            task = asyncio.ensure_future(send_data(url, session, post))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def parse_users_tabs(
    chrome_driver_path, post_count, logger, xpath_templates, condition, parsing_queue
):
    browser = config_browser(chrome_driver_path)
    parsed_information = []
    try:
        while condition["Processing"] and condition["Parsed count"] <= post_count:
            time.sleep(1)

            if parsing_queue:
                parsing_ready_posts = parsing_queue[:]
                result = asyncio.run(
                    start_user_parsing(
                        browser, parsing_ready_posts, logger, xpath_templates
                    )
                )

                for return_status, saved_dictionary in result:
                    if return_status:
                        saved_dictionary["unique_id"] = generate_uuid()
                        parsed_information.append(saved_dictionary)
                        condition["Parsed count"] += 1

                        logger.debug(
                            f"All information has been received on this post(url: {saved_dictionary['post_url']})"
                        )

                asyncio.run(start_sending(parsed_information))
                parsed_information.clear()

                for post in parsing_ready_posts:
                    parsing_queue.remove(post)
    except Exception as exception:
        logger.error(exception, exc_info=True)
    finally:
        browser.quit()


def scrape(
    executors, driver_path, post_count, logger, xpath_information, *, running_loop
):
    condition = {"Processing": True, "Parsed count": 0}
    need_parsing = []
    running_loop.run_in_executor(
        executors,
        parse_users_tabs,
        driver_path,
        post_count,
        logger,
        xpath_information,
        condition,
        need_parsing,
    )
    running_loop.run_in_executor(
        executors,
        parse_reddit_page,
        driver_path,
        post_count,
        logger,
        xpath_information,
        condition,
        need_parsing,
    )


def parse_command_line_arguments() -> Tuple[str, str, int]:
    argument_parser = argparse.ArgumentParser(description="Reddit parser")
    argument_parser.add_argument(
        "--path",
        metavar="path",
        type=str,
        help="Chromedriver path",
        default=find_chrome_driver(),
    )
    argument_parser.add_argument(
        "--log_level",
        metavar="log_level",
        type=str,
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Minimal logging level('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')",
    )
    argument_parser.add_argument(
        "--post_count",
        metavar="post_count",
        type=int,
        default=10,
        choices=range(0, 101),
        help="Parsed post count",
    )
    args = argument_parser.parse_args()

    return args.path, args.log_level, args.post_count


if __name__ == "__main__":
    chrome_driver, min_log_level, max_post_count = parse_command_line_arguments()
    configured_logger = config_logger(string_to_logging_level(min_log_level))
    xpath = load_xpath_templates_from_json()
    executor = ThreadPoolExecutor(max_workers=20)

    if not os.path.isfile(chrome_driver):
        configured_logger.error(
            f"Chrome drive does not exists at this link: {chrome_driver}!"
        )
    else:
        start = time.time()
        loop = asyncio.get_event_loop()
        scrape(
            executor,
            chrome_driver,
            max_post_count,
            configured_logger,
            xpath,
            running_loop=loop,
        )
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))
        executor.shutdown(True)
        configured_logger.debug(f"Processing time: {time.time() - start} seconds")
