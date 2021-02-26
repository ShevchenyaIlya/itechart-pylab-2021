import React, {useContext} from 'react';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import { makeStyles } from '@material-ui/core/styles';
import {AppContext} from "./index";

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    height: '0px',
    '& > * + *': {
      marginTop: theme.spacing(2),
    },
  },
}));


export default function CustomizedSnackbars() {
  const classes = useStyles();
  const {alertContent} = useContext(AppContext);
  let {configurations, handler} = alertContent;
  let {alertOpen, alertMessage, type} = configurations;

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    handler({alertOpen: false, alertMessage: "", type: type});
  };

  return (
    <div className={classes.root}>
      <Snackbar open={alertOpen} autoHideDuration={2000} onClose={handleClose} >
        <Alert onClose={handleClose} severity={type}>
            "{alertMessage}"
        </Alert>
      </Snackbar>
    </div>
  );
}