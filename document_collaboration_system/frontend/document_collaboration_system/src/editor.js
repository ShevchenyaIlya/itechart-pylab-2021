import React, {Component, useState} from "react";
import {convertToRaw, convertFromRaw, EditorState, Modifier} from "draft-js";
import PropTypes from 'prop-types';
import {Editor} from "react-draft-wysiwyg";
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";
import {Paper} from "@material-ui/core";
import ChatBubbleIcon from '@material-ui/icons/ChatBubble';
import {send_request} from "./send_request";
import {useHistory} from "react-router-dom";
import CustomMenu from "./menu";
import FormDialog from "./placeCommentDialog";

const styleMap = {
  'COMMENT': {
    backgroundColor: 'rgba(255, 255, 0, 0.5)',
  },
};

class CustomOption extends Component {
  static propTypes = {
    onChange: PropTypes.func,
    editorState: PropTypes.object,
  };

  addComment = () => {
    this.props.setOpen(true);
    const { editorState, onChange } = this.props;
    const contentState = Modifier.applyInlineStyle(
      editorState.getCurrentContent(),
      editorState.getSelection(),
      'COMMENT',
    );
    onChange(EditorState.push(editorState, contentState, 'change-inline-style'));
  };

  render() {
    return (
      <div id="customEditorButton" onClick={this.addComment}><ChatBubbleIcon/></div>
    );
  }
}

class ControlledEditor extends Component {
  constructor(props) {
    super(props);
    this.document_id = props.document;

    this.state = {
      editorState: EditorState.createEmpty(),
    };

    this.loadInitialContent = () => {
      send_request("GET", "document/" + this.document_id).then((content) => {
        if (content === null) {
          this.props.history.push("/");
        }
        else if (Object.keys(content.content).length !== 0) {
          if (content.status === "Archive") {
            this.props.setMode(true);
          }

          const DBEditorState = convertFromRaw(content.content);
          const local_state = EditorState.createWithContent(DBEditorState);
          this.setState({
            editorState: local_state
          });
        }
      });
    };

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
          readOnly={this.props.readOnly}
          toolbarCustomButtons={[<CustomOption setOpen={this.props.setOpen}/>]}
          customStyleMap={styleMap}
        />
    );
  }
}

function DocumentEditor({document}) {
  let [readOnlyDocument, setMode] = useState(false);
  const [openModalWindow, setOpen] = React.useState(false);
  const history = useHistory();

  return (
      <>
        <FormDialog openModalWindow={openModalWindow} setOpen={setOpen}/>
        <CustomMenu document={document} readOnly={readOnlyDocument} setMode={setMode}/>
        <Paper elevation={3} className="editorContainer">
          <ControlledEditor document={document} history={history} readOnly={readOnlyDocument} setMode={setMode} setOpen={setOpen}/>
        </Paper>
      </>
  );
}

export default DocumentEditor;