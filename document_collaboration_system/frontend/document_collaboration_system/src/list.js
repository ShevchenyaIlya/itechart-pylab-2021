import React, {useContext, useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import DescriptionIcon from '@material-ui/icons/Description';
import {send_request} from "./send_request";
import {useHistory} from "react-router-dom";
import {AppContext} from "./index";

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    maxWidth: "1000px",
    margin: "auto",
    backgroundColor: theme.palette.background.paper,
  },
  container: {
    minHeight: "600px",
  }
}));

export default function SimpleList() {
  const classes = useStyles();
  const history = useHistory();
  const {alertContent} = useContext(AppContext);
  let [documents, setDocuments] = useState([]);

  useEffect(() => {
    if (sessionStorage.getItem("token") === null) {
      alertContent.handler({alertOpen: true, alertMessage: "Please login!", type: "warning"});
      history.push("/login");
    }
    else {
      send_request("GET", "documents").then(data => {
        if (data !== null) {
          setDocuments(data);
        }
        else {
          history.push("/login");
        }
      });
    }
  }, []);

  const handler = (identifier) => (event) => {
      history.push("document/" + identifier);
  };

  return (
    <div className={classes.container}>
      <div className={classes.root}>
        <List component="nav" aria-label="main mailbox folders">
            {
                documents.map((single_document) =>
                    <ListItem button key={single_document._id} onClick={handler(single_document._id)}>
                        <ListItemIcon>
                            <DescriptionIcon/>
                        </ListItemIcon>
                        <ListItemText primary={single_document.document_name} secondary={single_document.creation_date}/>
                        <ListItemText primary={"Creator"} secondary={single_document.creator}/>
                        <ListItemText secondary={single_document.status}/>
                        <ListItemText secondary={single_document._id}/>
                    </ListItem>
                )
            }
        </List>
        <Divider />
      </div>
    </div>
  );
}
