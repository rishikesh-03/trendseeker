import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import NewsWebsites from './components/NewsWebsites';
import NewsWebsiteHeadlines from './components/NewsWebsiteHeadlines';
import NavBar from './components/NavBar';
import './App.css';

function App() {
  return (
    <Router>
      <NavBar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/news-websites" element={<NewsWebsites />} />
          <Route path="/news-websites/:source" element={<NewsWebsiteHeadlines />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
