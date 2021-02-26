import React, {useState} from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemIcon from "@material-ui/core/ListItemIcon";
import CommentIcon from '@material-ui/icons/Comment';
import {send_request} from "./send_request";
import "./css/base.css";


export function CommentButton({document}) {
    const [open, setOpen] = useState(false);
    const [comments, setComments] = useState([]);

    const handleClickOpen = () => {
      send_request("GET", "comments/" + document).then((response_data) => {
        setComments(response_data);
      });

      setOpen(true);
    };

    return (
        <div className="commentsButtonContainer">
            <Button aria-controls="simple-menu" aria-haspopup="true" onClick={handleClickOpen}  id="menuButton">
              Comments
            </Button>
            <AlertDialog open={open} setOpen={setOpen} comments={comments}/>
        </div>
    );
}

export function AlertDialog({open, setOpen, comments}) {
  const handleClose = () => {
    setOpen(false);
  };

  return (
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
         <DialogTitle id="alert-dialog-title">{"Check comments for this document!"}</DialogTitle>
         <DialogContent>
           <List component="nav" aria-label="main mailbox folders">
             {
                 comments.map((single_comment) =>
                     <ListItem button key={single_comment._id}>
                         <ListItemIcon>
                             <CommentIcon/>
                         </ListItemIcon>
                         <ListItemText primary={single_comment.author} secondary={(new Date(single_comment.creation_date)).toDateString()}/>
                         <ListItemText primary="Selected:" secondary={single_comment.commented_text}/>
                         <ListItemText primary="Comment:" secondary={single_comment.comment}/>
                     </ListItem>
                 )
             }
           </List>
         </DialogContent>
         <DialogActions>
           <Button onClick={handleClose} color="primary">
             Close
           </Button>
         </DialogActions>
       </Dialog>
   );
 }
