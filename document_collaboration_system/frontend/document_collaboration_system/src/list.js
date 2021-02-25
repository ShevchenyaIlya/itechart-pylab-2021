import React, {useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import DraftsIcon from '@material-ui/icons/Drafts';
import {send_request} from "./send_request";
import {useHistory} from "react-router-dom";

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
  let [documents, setDocuments] = useState([]);

  useEffect(() => {
    if (sessionStorage.getItem("token") === null) {
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
                            <DraftsIcon/>
                        </ListItemIcon>
                        <ListItemText primary={single_document.document_name + " " + single_document._id}/>
                    </ListItem>
                )
            }
        </List>
        <Divider />
      </div>
    </div>
  );
}
