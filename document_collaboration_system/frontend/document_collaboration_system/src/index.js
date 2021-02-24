import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './App';
import Home from './home';
import DocumentList from './documentList';
import Login from './login';
import reportWebVitals from './reportWebVitals';
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

class Index extends React.Component{
  constructor(props) {
    super(props);
    this.state = {nickname: "", session_token: "", document: ""};

    this.updateState = (field) => (value) => {
        this.setState({[field]: value});
    };
  }

  componentDidMount() {
    this.updateState("session_token")(sessionStorage.getItem("token"));
    this.updateState("username")(sessionStorage.getItem("username"));
  }

  render() {
    return (
        <>
          <Router>
            <Switch>
              <Route exact path="/login">
                <Login/>
              </Route>
              <Route path="/document">
                <App document={this.state.document} setDocument={this.updateState("document")}/>
              </Route>
              <Route exact path="/documents">
                <DocumentList />
              </Route>
              <Route exact path="/">
                <Home setDocument={this.updateState("document")}/>
              </Route>
            </Switch>
          </Router>
        </>
    );
  }
}

ReactDOM.render(
  <Index/>,
  document.getElementById('root')
);

reportWebVitals();
