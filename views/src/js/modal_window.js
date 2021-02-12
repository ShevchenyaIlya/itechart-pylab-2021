function showModalWindow() {
    const modalWindow = document.getElementById("modal-window");

    if (modalWindow.style.display === "none") {
        modalWindow.style.display = "block";
    }
    else {
        modalWindow.style.display = "none";
    }
}

function FilterItem(props) {
    const filter = props.filter_name

    function handler() {
        configurations.sorting_field = filter;
        updatePostsList();
    }

    return <p onClick={handler}>{filter}</p>;
}

function Filters(props) {
    const filters = props.filters;

    return (
        <div id="modal-window" style={{display: 'none'}}>
            <h4>Filters</h4>
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