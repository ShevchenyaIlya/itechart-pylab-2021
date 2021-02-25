function config_request_header(token="",) {
    if (token !== "") {
        return {headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': "Bearer " + token
            }
        };
    }

    return {};
}

function config_body(content=null) {
    if (content !== null) {
        return {body: content};
    }

    return {};
}

function config_request_url(endpoint) {
    return 'http://localhost:5000/' + endpoint;
}

async function send_request(method, endpoint, body=null) {
    const token = sessionStorage.getItem("token");
    const url = config_request_url(endpoint);

    try {
        const response_data  = await fetch(url, {
            ...config_request_header(token),
            ...config_body(body),
            method: method,
            mode: 'cors',
            async: true,
        });

        if ([200, 403].includes(response_data.status)) {
            return response_data.json();
        }
        else {
            return null;
        }
    }
    catch (e) {
        alert("Can't reach connection with server! Try again.");
        throw Error("Can't reach connection with server");
    }
}

export {send_request};
