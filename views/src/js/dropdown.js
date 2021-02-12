function Dropdown(props) {
    const filters = props.filters;

    return (
        <fragment>
            <button className="button">Order</button>
            <div className="dropdown-content">
                <Swapper />
                {
                    filters.map((filter) => <DropdownItem key={filter} filter_name={filter}/>)
                }
            </div>
        </fragment>
    );
}

function DropdownItem(props) {
    const filter_name = props.filter_name

    function handler() {
        configurations.sorting_field = filter_name;
        updatePostsList();
    }

    return (
        <a href="#" onClick={handler}>{filter_name}</a>
    )
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
                Sorting by <i id="order-icon" className="fa fa-angle-double-down" aria-hidden="true"></i>
            </h4>
        );
    }
}

ReactDOM.render(
    <Dropdown filters={filters}/>,
    document.getElementById("dropdown")
);
