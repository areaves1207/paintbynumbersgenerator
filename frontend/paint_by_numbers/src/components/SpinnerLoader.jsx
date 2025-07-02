import styles from './spinner.module.css'
import spinner from './gifs/spinner.gif';
import { useState } from "react";

export default function SpinnerLoader(){
    const [showImage, setShowImage] = useState(true);

    return (
        <>
            <div className={styles.spinner}>
                {
                    showImage ? (
                        <img src={spinner}></img>
                    ) : (
                        <h3>"Generating, i promise...</h3>
                    )
                }
            </div>
            <p>Generating...</p>
        </>
    );
}