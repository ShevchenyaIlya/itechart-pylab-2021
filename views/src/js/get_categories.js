async function fetchCategories() {
    let url = 'http://localhost:8087/categories/'

    try {
        const response = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            async: true,
        });

        if (response.status === 200) {
            return response.json();
        }
    }
    catch (e) {
        console.error("No connection with server!")
    }

    return [];
}