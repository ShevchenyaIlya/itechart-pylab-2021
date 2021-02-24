import React from 'react';
import Header from './header';
import Footer from './footer';
import Navbar from './navbar';
import ControlledAccordions from './accordion';


function Home({setDocument}) {
  return (
      <div className="Home">
          <Header/>
          <Navbar />
          <ControlledAccordions setDocument={setDocument}/>
          <Footer/>
      </div>
  );
}

export default Home;
