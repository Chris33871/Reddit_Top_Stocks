import React, { useState, useEffect } from 'react';
import './App.css'
import Intro from './components/Intro'
import Timeline from './components/Timeline';
import StyledButton from './components/Button';
import RedditData from './components/RedditData';

function App() {

  const [showRedditData, setShowRedditData] = useState(false);

  const handleButtonClick = () => {
    console.log('clicked')
    setShowRedditData(true);
  };

  return (
    <body className="body--app">
      
        <Intro />
        <Timeline />
        <StyledButton onClick={handleButtonClick}/>
        {showRedditData && <RedditData />}
      
    </body>
  );
}

export default App;



