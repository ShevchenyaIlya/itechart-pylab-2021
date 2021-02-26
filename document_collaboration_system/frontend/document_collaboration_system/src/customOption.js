import React, {Component} from "react";
import PropTypes from "prop-types";
import {EditorState, Modifier} from "draft-js";
import ChatBubbleIcon from "@material-ui/icons/ChatBubble";

export default class CustomOption extends Component {
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
    onChange(EditorState.push(editorState, contentState, "change-inline-style"));

    const selectionState = editorState.getSelection();
    const anchorKey = selectionState.getAnchorKey();
    const currentContent = editorState.getCurrentContent();
    const currentContentBlock = currentContent.getBlockForKey(anchorKey);
    const start = selectionState.getStartOffset();
    const end = selectionState.getEndOffset();
    const selectedText = currentContentBlock.getText().slice(start, end);
    this.props.setSelectedText(selectedText);
  };

  render() {
    return (
        <div title="Comment" id="customEditorButton" onClick={this.addComment}><ChatBubbleIcon/></div>
    );
  }
}