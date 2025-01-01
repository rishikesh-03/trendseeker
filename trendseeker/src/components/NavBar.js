import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';

const NavBar = () => {
  return (
    <nav className="navbar">
      <h1>Trending News</h1>
      <div>
        <Link to="/">Home</Link>
        <Link to="/news-websites">News Websites</Link>
      </div>
    </nav>
  );
};

export default NavBar;
