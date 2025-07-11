import React from 'react';
import styles from './popup.module.css';

const Popup = ({ isOpen, onClose }) => {
    if(!isOpen){
        return(null);
    }
    return (
        <div className={styles.popupOverlay}>
            <div className={styles.popupElements}>
                <h1>Welcome to my Paint By Numbers Generator!</h1>
                <h3>
                    This project was made after I kept seeing instagram ads for paint by number kits available for purchase.
                    After recently taking a computer vision class last year, I decided it would be fun to work on something similar
                    in my free time. Over the last few weeks, I've spent a couple hours a day working from the ground up,
                    using what I learned in my classes for the back end, and learning a ton of brand new stuff with React, HTML, css, and 
                    other things for my front end. 
                </h3>
                <h4>
                    This site is hosted by Vercel and the back end is hosted by Render. FastAPI is used to connect everything.
                    Since both are free hosting sites, the input and output is limited, and so the wait times for generating an
                    image is very long and the outputs are pretty small (640x480). 
                </h4>
                <h4>
                    In all honesty too, it is not extremely optimized, which is a partial reason for the wait time. The next major fix
                    is to make the backend more efficient. I have implemented just about everything myself, such as the
                    custom Canny edge detector, K-Means clustering, and a tight edge detector. The good news is I have my implementations
                    working! They just aren't optimized at the moment, unfortunately. 
                </h4>
                <h4>
                    Thank you for checking it out though! It's been a fun project to work on, and my first ever full stack development!
                </h4>
                <button onClick={() => onClose()}>Close</button>
            </div>
        </div>
    );
};

export default Popup;