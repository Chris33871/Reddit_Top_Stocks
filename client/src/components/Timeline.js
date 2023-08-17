import React from "react";
import './Timeline.css'

export default function Timeline() {
    return (
        <div className="bar">
            <p className="bar--p">Functionality Coming soon</p>
            <div className="bar--dot" data-date="May 11, 2023"></div>
            <div className="bar--dot" data-date="May 12, 2023"></div>
            <div className="bar--dot" data-date="May 13, 2023"></div>
        </div>
    )
}