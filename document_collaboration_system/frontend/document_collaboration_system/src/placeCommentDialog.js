import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

export default function FormDialog({openModalWindow, setOpen}) {
  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Dialog open={openModalWindow} onClose={handleClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title">Comment</DialogTitle>
        <DialogContent>
          <DialogContentText>
            To leave a comment, please write text in field under.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Comment message"
            type="email"
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleClose} color="primary">
            Leave
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}