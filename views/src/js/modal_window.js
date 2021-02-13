const showModalWindow = () => {
    const modalWindow = document.getElementById("modal-window");
    clear_filters();

    if (modalWindow.style.display === "none") {
        modalWindow.style.display = "block";
    }
    else {
        modalWindow.style.display = "none";
    }
}

const get_filters_blocks = () => {
    const category = document.getElementById("category");
    const date = document.getElementById("post_date");
    const votes_from = document.getElementById("votes_number_from");
    const votes_to = document.getElementById("votes_number_to");

    return [category, date, votes_from, votes_to]
}

const clear_filters = () => {
    configurations.votes_number = null;
    configurations.post_date = null;
    configurations.post_category = null;
}

function CategoryFilter() {
    return (
        <div>
            <label htmlFor="category"><b>Category:</b></label>
            <input name="category" id="category" type={"text"}/>
        </div>
    )
}


function VotesNumberFilter() {
    return (
        <div>
            <label><b>Votes number:</b><br/></label>
            <div>
                <label htmlFor="from"><b>From:</b></label>
                <input name="from" type={"text"} id="votes_number_from" style={{width: "45%"}}/>
            </div>
            <div>
                <label htmlFor="to"><b>To:</b></label>
                <input name="to" type={"text"} id="votes_number_to" style={{width: "45%"}}/>
            </div>
        </div>
    )
}

function PostDateFilter() {
    return (
        <div>
            <label htmlFor="post_date"><b>Post date: </b></label>
            <input name="post_date" id="post_date" type="date"/>
        </div>
    )
}

function Filters() {
    return (
        <div id="modal-window" style={{display: 'none'}}>
            <h3>Filters</h3>
            <PostDateFilter/>
            <CategoryFilter/>
            <VotesNumberFilter/>
            <SubmitFilters/>
        </div>
    );
}

function SubmitFilters() {
    const handler = () => {
        const [category, post_date, votes_from, votes_to] = get_filters_blocks()

        configurations.post_category = category.value;
        configurations.votes_number = [votes_from.value, votes_to.value].join("-");
        configurations.post_date = post_date.value;
        configurations.page = 0;
        updatePostsList();
    }

    return (
        <button onClick={handler} style={{margin: "10px"}}>Filter</button>
    )
}

ReactDOM.render(
    <Filters filters={filters}/>,
    document.getElementById("filters_container")
);