function showModalWindow() {
    const modalWindow = document.getElementById("modal-window");

    if (modalWindow.style.display === "none") {
        modalWindow.style.display = "block";
    }
    else {
        modalWindow.style.display = "none";
    }
}

class Swapper extends React.Component {
    constructor(props) {
        super(props);
        this.state = {isASC: true};

        this.handleClick = this.handleClick.bind(this);
    }

    handleClick()
    {
        this.setState(state => ({
            isASC: !state.isASC
        }));

        let order_icon = document.getElementById("order-icon");
        if (this.state.isASC) {
            order_icon.className = "fa fa-angle-double-up";
            configurations.order = "DESC";
        }
        else {
            configurations.order = "ASC";
            order_icon.className = "fa fa-angle-double-down";
        }
        updatePostsList()
    }

    render()
    {
        return (
            <h4 onClick={this.handleClick}>
                Available Filters <i id="order-icon" className="fa fa-angle-double-down" aria-hidden="true"></i>
            </h4>
        );
    }
}


function FilterItem(props) {
    const filter = props.filter_name
    function handler() {
        console.log(filter)
        configurations.filter_field = filter;
        updatePostsList();
    }

    return <p onClick={handler}>{props.filter_name}</p>;
}


function Filters(props) {
    const filters = props.filters;

    return (
        <div id="modal-window" style={{display: 'none'}}>
            <Swapper />
            {
                filters.map((filter) => <FilterItem key={filter} filter_name={filter}/>)
            }
        </div>
    );
}


ReactDOM.render(
    <Filters filters={filters}/>,
    document.getElementById("filters_container")
);