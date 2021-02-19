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

function ListItem({post}) {

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

function ActionLink({value, page, setPage, operation}) {
    function handleClick() {
        configurations.page = operation(page);

        if (configurations.page !== -1) {
            fetchPosts(createFiltersLine(configurations))
            .then(data => {
                if (data.length === 0) {
                    configurations.page -= 1;
                }
                return data;
            }).then(data => {
                if (configurations.page !== page) {
                    renderList(data, postsContainer);
                }
                setPage(configurations.page);
            });
        }
    }

    return (
        <a href="#" onClick={handleClick}>
            {value}
        </a>
    );
}

function PostsList({posts}) {
    return (
    <div>
        {
            posts.map((post) => <ListItem key={post.unique_id} post={post}/>)
        }
        <Pagination/>
    </div>
    );
}

class Pagination extends React.Component {
    constructor(props) {
        super(props);
        this.state = {page: 0};

        this.setPage = (page) => {
            this.setState({page: page});
        }
    }

    render() {
        return (
            <div className="pagination">
                <ActionLink value={">"} page={this.state.page} setPage={this.setPage} operation={(number) => number + 1}/>
                <a className="active" id="current_page" href="#">{this.state.page}</a>
                <ActionLink value={"<"} page={this.state.page} setPage={this.setPage} operation={(number) => number - 1}/>
            </div>
        )
    }
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
