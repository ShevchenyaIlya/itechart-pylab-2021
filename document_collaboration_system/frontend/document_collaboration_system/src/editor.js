import React, {Component} from "react";
import {convertToRaw, convertFromRaw, EditorState} from "draft-js";
import {Editor} from "react-draft-wysiwyg";
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";
import {Paper} from "@material-ui/core";
import {send_request} from "./send_request";
import {useHistory} from "react-router-dom";


class ControlledEditor extends Component {
  constructor(props) {
    super(props);
    this.document_id = props.document;

    this.state = {
      editorState: EditorState.createEmpty(),
    };

    this.loadInitialContent = () => {
      send_request("GET", "document/" + this.document_id).then((content) => {
        if (Object.keys(content.content).length !== 0) {
          const DBEditorState = convertFromRaw(content.content);
          const local_state = EditorState.createWithContent(DBEditorState);
          this.setState({
            editorState: local_state
          });
        }
      });
    }

    this.onEditorStateChange = (editorState) => {
      if (sessionStorage.getItem("token") === null) {
        this.props.history.push("/login");
      }
      else {
        const contentState = editorState.getCurrentContent();
        this.setState({
          editorState,
        });
        send_request("PUT", "document/" + this.document_id, JSON.stringify(convertToRaw(contentState))).then();
      }
    };
  }

  componentDidMount() {
    this.loadInitialContent();
    this.timer = setInterval(() => this.loadInitialContent(), 5000);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
    this.timer = null;
  }
  render() {
    const { editorState } = this.state;
    return (
        <Editor
          editorState={editorState}
          wrapperClassName="demo-wrapper"
          editorClassName="demo-editor"
          onEditorStateChange={this.onEditorStateChange}
        />
    )
  }
}

function DocumentEditor({document}) {
  const history = useHistory()
  return (
    <Paper elevation={3} className="editorContainer">
      <ControlledEditor document={document} history={history}/>
    </Paper>
  );
}

export default DocumentEditor