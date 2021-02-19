async function fetchPosts(filters = "") {
    let url = 'http://localhost:8087/posts/'
    if (filters !== "") {
        url += "?" + filters;
    }
    try {
        const response_data  = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            async: true,
        });

        if (response_data.status === 200) {
            return response_data.json();
        }
    }
    catch (e) {
        alert("Can't reach connection with server! Try again.");
        throw Error("Can't reach connection with server");
    }

    return [];
}

function homePage() {
    configurations.page = 0;
    document.getElementById("current_page").innerHTML = "0";
    updatePostsList()
}