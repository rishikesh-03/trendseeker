import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './TrendingNews.css';

const NewsWebsiteHeadlines = () => {
  const { source } = useParams();
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(new Date().toISOString().split('T')[0]);

  const fetchTrendingNews = async () => {
    try {
      const response = await axios.post('http://localhost:3000/api/run-script', {
        startDate,
        endDate,
      });
      setNews(response.data.filter((item) => item.source === source));
    } catch (err) {
      setError('Failed to fetch trending news.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrendingNews();
  }, [source, startDate, endDate]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="trending-news-page">
      <h1>{source} Headlines</h1>
      <div className="date-inputs">
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </div>
      {news.length === 0 ? (
        <p>No headlines found for {source}.</p>
      ) : (
        <ul className="news-list">
          {news.map((item, index) => (
            <li key={index} className="news-item">
              <h2>{item.headline}</h2>
              <a href={item.link} target="_blank" rel="noopener noreferrer">
                Read more
              </a>
              <p>Source: {item.source}</p>
              <p>Published at: {new Date(item.timestamp).toLocaleString()}</p>
              <p>Score: {item.score}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default NewsWebsiteHeadlines;
