import styles from "./generator.module.css"
import { useState } from "react";

export default function Generator(){
    const [selectedFile, setSelectedFile] = useState(null);
    
    const fileUploadHandler = event => {
        const file = event.target.files[0];
        console.log(file);
        setSelectedFile(file);
    };

    return (
        <div className={styles.div}>
            <div className={styles.infoText}>Upload an image to generate it's canvas</div>

            <input type='file' accept="image/*" onChange={fileUploadHandler}></input>
            {/* <input type='file' className={styles.button}>Upload image</input> */}
            <img src={selectedFile}></img>
        </div>
    );
}