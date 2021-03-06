function Dropdown({filters}) {
    return (
        <div>
            <button className="button">Order</button>
            <div className="dropdown-content">
                <Swapper />
                {
                    filters.map((filter) => <DropdownItem key={filter} filter_name={filter}/>)
                }
            </div>
        </div>
    );
}

function DropdownItem({filter_name}) {
    function handler(event) {
        event.preventDefault();
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
        this.orderIcon = React.createRef();

        this.handleClick = () => {
            this.setState(state => ({
                isASC: !state.isASC
            }));

            if (this.state.isASC) {
                this.orderIcon.current.className = "fa fa-angle-double-up";
                configurations.order = "DESC";
            } else {
                configurations.order = "ASC";
                this.orderIcon.current.className = "fa fa-angle-double-down";
            }
            updatePostsList()
        }
    }
    render()
    {
        return (
            <h4 onClick={this.handleClick}>
                Sorting by <i ref={this.orderIcon} id="order-icon" className="fa fa-angle-double-down" aria-hidden="true"></i>
            </h4>
        );
    }
}

ReactDOM.render(
    <Dropdown filters={filters}/>,
    document.getElementById("dropdown")
);
