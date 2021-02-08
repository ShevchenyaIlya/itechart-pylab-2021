let configurations = {
    filter_field: "post_category",
    order: "ASC",
    page: 0,
}
const filters = ["post_category", "post date", "votes_number"]
const postsContainer = document.getElementById("posts_list");


function createFiltersLine(configuration) {
    let filtersLine = [];

    for (const [key, value] of Object.entries(configuration)) {
        filtersLine.push(`${key}=${value}`);
    }

    return filtersLine.join("&");
}
