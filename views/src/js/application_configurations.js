let configurations = {
    sorting_field: "post_category",
    post_category: null,
    post_date: null,
    votes_number: null,
    order: "ASC",
    page: 0,
}
const filters = ["post_category", "post_date", "votes_number"]
const postsContainer = document.getElementById("posts_list");


function createFiltersLine(configuration) {
    let filtersLine = [];

    for (const [key, value] of Object.entries(configuration)) {
        if (value != null && value !== "") {
            filtersLine.push(`${key}=${value}`);
        }
    }

    return filtersLine.join("&");
}
