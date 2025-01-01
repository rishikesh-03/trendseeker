import React from 'react';
import { Link } from 'react-router-dom';
import './NewsWebsites.css';

const newsWebsites = ['TOI', 'The Hindu', 'Indian Express', 'NDTV', 'India Today'];

const NewsWebsites = () => {
  return (
    <div className="news-website-page">
      <h1>News Websites</h1>
      <ul className="news-website-list">
        {newsWebsites.map((website, index) => (
          <li key={index}>
            <Link to={`/news-websites/${website}`}>{website}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NewsWebsites;
