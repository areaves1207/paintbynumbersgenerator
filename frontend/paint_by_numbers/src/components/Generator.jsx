import styles from "./generator.module.css"
import { useState } from "react";

export default function Generator(){
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    
    const fileUploadHandler = event => {
        const file = event.target.files[0];
        console.log(file);
        if(file){
            setSelectedFile(file);
            setPreviewUrl(URL.createObjectURL(file));
        }
        
    };

    return (
        <div className={styles.div}>
            <div className={styles.infoText}>Upload an image to generate it's canvas</div>

            <input type='file' accept="image/*" className={styles.button} onChange={fileUploadHandler}></input>
            {/* <input type='file' >Upload image</input> */}

            <img className={styles.imagePreview} src={previewUrl}></img>
        </div>
    );
}