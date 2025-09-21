import React from 'react';
import styles from './popup.module.css';

const Popup = ({ isOpen, onClose, title, children }) => {
    if(!isOpen){
        return(null);
    }
    return (
        <div className={styles.popupOverlay}>
            <div className={styles.popupElements}>
                <div>{title}</div>
                <div>{children}</div>
                <button onClick={() => onClose()}>Close</button>
            </div>
        </div>
    );
};

export default Popup;