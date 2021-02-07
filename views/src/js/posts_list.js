function ListItemHeader(props) {
    return <h2>{props.post_url}</h2>;
}


function ListItemBody(props) {
    const post = Object.entries(props.post);

    return (
        <ul>
        {
            post.map(post_field => <li><b>{post_field[0] + ": "}</b>{post_field[1]}</li>)
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
            <ListItemHeader key={post.unique_id} post_url={post.post_url}/>
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
        let new_page_number = operation(page_number);

        if (new_page_number !== -1) {
            fetchPosts("filter_field=votes_number&page=" + new_page_number + "&order=ASC")
            .then(data => {
                if (data.length === 0) {
                    new_page_number -= 1;
                }

                return data;
            }).then(data => {
                if (new_page_number !== page_number) {
                    renderList(data, postsContainer);
                }

                page.innerHTML = new_page_number;
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


const postsContainer = document.getElementById("posts_list");
fetchPosts("order_field=votes_number&page=0&order=ASC").then(data => renderList(data, postsContainer));
