import Header from "./header";
import Navbar from "./navbar";
import Footer from "./footer";
import List from "./list";
import React from "react";

function DocumentList() {
  return (
      <div className="documentList">
          <Header/>
          <Navbar />
          <List/>
          <Footer/>
      </div>
  );
}

export default DocumentList;