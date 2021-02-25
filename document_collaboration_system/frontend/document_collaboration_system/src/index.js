import React, {createContext} from 'react';
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
import CustomizedSnackbars from "./customAlert";

export const AppContext = createContext();

class Index extends React.Component{
  constructor(props) {
    super(props);
    this.state = {nickname: "", session_token: "", document: "", customAlert: {alertOpen: false, alertMessage: "", type: ""}};

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
        <AppContext.Provider value={{name: [this.state.nickname, this.updateState("nickname")], alertContent: {configurations: this.state.customAlert, handler: this.updateState("customAlert")}}}>
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
          <CustomizedSnackbars/>
        </AppContext.Provider>
    );
  }
}

ReactDOM.render(
  <Index/>,
  document.getElementById('root')
);

reportWebVitals();
