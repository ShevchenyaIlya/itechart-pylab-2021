import React, {useEffect, useState} from 'react';
import './css/base.css';
import {
  Link,
} from "react-router-dom";
import {useHistory} from "react-router-dom";

function Navbar(){
    let [username, setUsername] = useState(sessionStorage.getItem("username"));
    const history = useHistory();

    const logoutUser = (event) => {
        event.preventDefault();
        sessionStorage.removeItem("username");
        sessionStorage.removeItem("token");
        setUsername("");
        history.push("/");
    };

    useEffect(() => {
        setUsername(sessionStorage.getItem("username"));
    }, []);

    return (
        <div className="navbar">
            <div>
                <Link className="active" to="/"><i className="fa fa-fw fa-home"></i> Home</Link>
                <Link className="" to="/documents"><i className="fa fa-fw fa-book"></i> Documents</Link>
                <Link className="right" to="/login"><i className="fa fa-fw fa-user"></i> Sign In</Link>
                <Link className="right" to="#" onClick={logoutUser}>{username}</Link>
            </div>
        </div>
    );
}

export default Navbar;