import React from 'react';
import './Button.css'


const StyledButton = ({onClick}) => {
    

    return (
        <form>
            {/* 
                The button needs to first get data (so type='button') but 
                should also submit data bc it needs to re-render the page 
                showing the graphs etc
             */}
            <input
                type='button'
                className='form--btn'
                value={'Request Data'}
                onClick={onClick} >
            </input>
        </form>
    );
};

export default StyledButton


