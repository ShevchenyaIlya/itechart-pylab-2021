import React from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import './css/base.css';
import {send_request} from "./send_request";


export default function CustomMenu({document}) {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const documentOperation = (operation) => () => {
      send_request("POST", operation + "/" + document).then((response) => {
          if (response === null) {
              alert("You need have specific role to execute that command");
          }
          else if (typeof response.message !== 'undefined') {
              alert(response.message);
          }
      });
      handleClose();
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
      </Menu>
    </div>
  );
}