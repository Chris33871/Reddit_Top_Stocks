import React, { useEffect, useState } from 'react';
import './RedditData.css'

function App() {
  const [tickersData, setTickersData] = useState([]);

  useEffect(() => {
    fetch('/api')  // Replace '/api' with the appropriate URL of your Flask API endpoint
      .then(response => response.json())
      .then(data => setTickersData(data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className='redditData'>
      <h1 className='redditData--h1'>Top Tickers</h1>
      {Object.keys(tickersData).length > 0 ? (
        <ul className='redditData--ul'>
          {Object.entries(tickersData).map(([ticker, data]) => (
            <li className='redditData--li' key={ticker}>
              {ticker}: {data.price + '$'}
            </li>
          ))}
        </ul>
      ) : (
        <p className='redditData--p'>Loading...</p>
      )}
    </div>
  );
}

export default App;