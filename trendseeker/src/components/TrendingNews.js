// src/components/TrendingNews.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TrendingNews = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrendingNews = async () => {
      try {
        const response = await axios.post('http://localhost:3000/run-script', {
          startDate: '2024-07-01',
          endDate: '2024-07-20',
        });
        setNews(response.data); // Directly using response.data if it's the output
      } catch (err) {
        setError('Failed to fetch trending news.');
      } finally {
        setLoading(false);
      }
    };

    fetchTrendingNews();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  if (!news || news.length === 0) return <p>No trending news found.</p>;

  return (
    <div>
      <h1>Trending News</h1>
      <ul>
        {news.map((item, index) => (
          <li key={index}>
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
    </div>
  );
};

export default TrendingNews;
