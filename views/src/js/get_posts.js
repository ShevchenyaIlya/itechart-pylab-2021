async function fetchPosts(filters = "") {
    let url = 'http://localhost:8087/posts/'
    if (filters !== "") {
        url += "?" + filters;
    }
    const response = await fetch(url, {
        method: 'GET',
        mode: 'cors',
        async: true,
    });

    let response_data = await response;
    if (response_data.status === 200) {
        return response_data.json();
    }

    return [];
}

function homePage() {
    configurations.page = 0;
    document.getElementById("current_page").innerHTML = "0";
    updatePostsList()
}