function ListItemHeader(props) {
    return <h3>{props.post_header}</h3>;
}

function ListItemBody(props) {
    const post = Object.entries(props.post);

    return (
        <ul>
            {
                post.map(post_field => <li key={post_field[0]}><b>{post_field[0] + ": "}</b>{post_field[1]}</li>)
            }
        </ul>
    );
}

function ListItem(props) {
    const post = props.post;

    return (
    <div>
        <div id="list-item-header">
            {
                <ListItemHeader key={post.unique_id} post_header={post.post_category}/>
            }
        </div>
        <div id="list-item-body">
            {
                <ListItemBody key={post.unique_id} post={post}/>
            }
        </div>
    </div>
    );
}

function ActionLink(props) {
    const value = props.value;
    const operation = props.operation;

    function handleClick() {
        const page = document.getElementById("current_page");
        let page_number = parseInt(page.innerHTML);
        configurations.page = operation(page_number);

        if (configurations.page !== -1) {
            fetchPosts(createFiltersLine(configurations))
            .then(data => {
                if (data.length === 0) {
                    configurations.page -= 1;
                }
                return data;
            }).then(data => {
                if (configurations.page !== page_number) {
                    renderList(data, postsContainer);
                }
                page.innerHTML = configurations.page;
            });
        }
    }

    return (
        <a href="#" onClick={handleClick}>
            {value}
        </a>
    );
}

function PostsList(props) {
    const posts = props.posts;

    return (
    <div>
        {
            posts.map((post) => <ListItem key={post.unique_id} post={post}/>)
        }
        {
            <div className="pagination">
                <ActionLink value={">"} operation={(number) => number + 1}/>
                <a className="active" id="current_page" href="#">0</a>
                <ActionLink value={"<"} operation={(number) => number - 1}/>
            </div>
        }
    </div>
    );
}

function renderList(data, container) {
    ReactDOM.render(
        <PostsList posts={data}/>,
        container
    );
}

const updatePostsList = () => {
    fetchPosts(createFiltersLine(configurations)).then(data => {
        renderList(data, postsContainer);
    });
}

updatePostsList();
