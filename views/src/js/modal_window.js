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

const clear_filters = () => {
    configurations.votes_number = null;
    configurations.post_date = null;
    configurations.post_category = null;
}

function SelectCategory({categories, setCategory, category_name}) {
    return (
        <div>
            <label htmlFor="category"><b>Category:</b></label>
            <select id="category" value={category_name} onChange={setCategory}>
                <option key={"empty"} value={""}>{""}</option>
                {
                    categories.map((category) => <option key={category} value={category}>{category}</option>)
                }
            </select>
        </div>
    )
}

function VotesNumberFilter({setVotesNumberFrom, setVotesNumberTo, votes_from, votes_to}) {
    return (
        <div>
            <label><b>Votes number:</b><br/></label>
            <div>
                <label htmlFor="from"><b>From:</b></label>
                <input value={votes_from} onChange={setVotesNumberFrom} name="from" type="text" id="votes_number_from"/>
            </div>
            <div>
                <label htmlFor="to"><b>To:</b></label>
                <input value={votes_to} onChange={setVotesNumberTo} name="to" type="text" id="votes_number_to"/>
            </div>
        </div>
    )
}

function PostDateFilter({setPostDate, post_date}) {
    return (
        <div>
            <label htmlFor="post_date"><b>Post date: </b></label>
            <input name="post_date" id="post_date" type="date" value={post_date} onChange={setPostDate}/>
        </div>
    )
}

class Filters extends React.Component {
    constructor(props) {
        super(props);
        this.categories = props.categories;
        this.state = {category: "", post_date: "", votes_from: 0, votes_to: 0};

        this.setFilter = (filter) => (event) => {
            this.setState({[filter]: event.target.value})
        };

        this.handleSubmit = (event) => {
            event.preventDefault();
            configurations.post_category = this.state.category;
            configurations.votes_number = [this.state.votes_from, this.state.votes_to].join("-");
            configurations.post_date = this.state.post_date;
            configurations.page = 0;
            updatePostsList();
        };
    }

    render () {
        return (
            <form onSubmit={this.handleSubmit}>
                <div id="modal-window" style={{display: 'none'}}>
                    <h3>Filters</h3>
                    <PostDateFilter setPostDate={this.setFilter("post_date")} post_date={this.state.post_date}/>
                    <SelectCategory categories={this.categories} setCategory={this.setFilter("category")} category_name={this.state.category}/>
                    <VotesNumberFilter setVotesNumberFrom={this.setFilter("votes_from")}
                                       setVotesNumberTo={this.setFilter("votes_to")}
                                       votes_from={this.state.votes_from} votes_to={this.state.votes_to}/>
                    <input type={"submit"} value={"Submit"}/>
                </div>
            </form>
        );
    }
}

function renderFilters(categories) {
    ReactDOM.render(
        <Filters categories={categories}/>,
        document.getElementById("filters_container")
    );
}

fetchCategories().then(data => {
    let categories = [];
    for (let i = 0; i < data.length; i++) {
        categories.push(data[i][0]);
    }
    renderFilters(categories)
});