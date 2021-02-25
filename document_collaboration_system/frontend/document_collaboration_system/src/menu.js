import React, {useContext} from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import './css/base.css';
import {send_request} from "./send_request";
import {useHistory} from "react-router-dom";
import {AppContext} from "./index";

export default function CustomMenu({document, readOnly, setMode}) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const history = useHistory();
  const {alertContent} = useContext(AppContext);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const documentOperation = (operation) => () => {
      send_request("POST", operation + "/" + document).then((response) => {
          if (response === null) {
              alertContent.handler({alertOpen: true, alertMessage: "You need have specific role to execute that command", type: "error"});
          }
          else if (typeof response.message !== 'undefined') {
              alertContent.handler({alertOpen: true, alertMessage: response.message, type: "error"});
          }
          else {
              alertContent.handler({alertOpen: true, alertMessage: "Operation executed!", type: "info"});
              if (operation === "archive") {
                  setMode(true);
              }
          }
      });
      handleClose();
  };

  const deleteDocument = () => {
    send_request("DELETE", 'document/' + document).then((response) => {
        if (typeof response.message !== 'undefined') {
            alertContent.handler({alertOpen: true, alertMessage: response.message, type: "error"});
        }
        else {
            alertContent.handler({alertOpen: true, alertMessage: "Document deleted!", type: "info"});
            history.push("/");
        }
    });
    handleClose();
  };

  const getDocumentLink = () => {
      navigator.clipboard.writeText("localhost:3000" + history.location.pathname);
  };

  return (
    <div>
      <Button aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}  id="menuButton">
        File
      </Button>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem onClick={documentOperation("approve")} className="menuListItem">Agreed</MenuItem>
        <MenuItem onClick={documentOperation("sign")}>Signing</MenuItem>
        <MenuItem onClick={documentOperation("archive")}>Archive</MenuItem>
        <MenuItem onClick={deleteDocument}>Delete</MenuItem>
        <MenuItem onClick={getDocumentLink}>Link</MenuItem>
      </Menu>
    </div>
  );
}