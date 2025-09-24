import styles from './info.module.css'
import Popup from "./Popup.jsx"
import { useState } from "react";

export default function Info({questionText, explanationText}){
    const [isPopupOpen, setPopupOpen] = useState(false);
    return (
        <>
            <div className={styles.entireQ}>
                    <div className={styles.question}>{questionText}</div>
                    <div className={styles.button} onClick={() => setPopupOpen(true)}>
                        &#9432;
                    </div>
            </div>
            <Popup isOpen={isPopupOpen} onClose={() => setPopupOpen(false)} title={questionText}>
                <div>{explanationText}</div>
            </Popup>
        </>
    );
}