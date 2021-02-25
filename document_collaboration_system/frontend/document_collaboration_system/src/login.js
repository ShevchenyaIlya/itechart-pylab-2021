import {Avatar, Button, Paper, TextField} from "@material-ui/core";
import React, {useState} from "react";
import {send_request} from './send_request';
import "./css/login.css";
import {
  Link,
  useHistory
} from "react-router-dom";


function Login() {
    const [textField, setText] = useState("");
    const history = useHistory();

    const handler = (event) => {
      event.preventDefault();

      send_request("POST", "login", textField).then((response_data) => {
          if (response_data === null) {
              alert("Such user does not exists!");
          }
          else {
              const {username, token, id} = response_data;
              sessionStorage.setItem("token", token);
              sessionStorage.setItem("id", id);
              sessionStorage.setItem("username", username);
              history.push("");
          }
      });
    };
    return (
      <Paper elevation={3} className="loginPaperStyle">
        <form noValidate autoComplete="off" onSubmit={handler}>
          <h1>Sign In</h1>
          <Avatar id="avatar"/>
          <TextField id="filled-basic" label="Login" value={textField} onChange={(event) => setText(event.target.value)} variant="filled" className="loginInput"/>
          <Button type="submit" variant="outlined">Login</Button>
          <Link to="/">Home</Link>
        </form>
      </Paper>
    );
}

export default Login;
