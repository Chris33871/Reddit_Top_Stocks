import React from 'react'
import './Intro.css';

export default function Intro() {
    return (
        <div>
            <h1 className="body--h1">
                Wallstreetbets Hot Stocks
            </h1>
            <div>
                <p className='div--text'>
                    This is a work in progress projects that collects API data from Reddit 
                    (Titles and Text from the HOT section of the Wallstreetbets subreddit).
                    From those fields are selected and counted, the 2 to 4 capital letters
                    combination without spaces. The most common combinations are then checked against
                    API data from twelve data so that we can easily check the price of the most talked
                    about stocks on reddit's Wallstreetbets.
                    Give it a try!
                    
                </p>
            </div>
        </div>

    )
}