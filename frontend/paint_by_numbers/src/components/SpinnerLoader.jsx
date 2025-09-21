import styles from './spinner.module.css'
import spinner from './gifs/spinner.gif';
import { useState } from "react";

export default function SpinnerLoader({action}){
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
            {/* <div class={styles.eta}>Estimated time: 11 minutes</div>
            <p class={styles.action}>{action}</p> */}
        </>
    );
}