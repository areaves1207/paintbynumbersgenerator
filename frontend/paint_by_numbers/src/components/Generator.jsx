import Checkbox from "./Checkbox";
import styles from "./generator.module.css"
import { useState } from "react";

export default function Generator(){
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [checkboxes, setChecked] = useState({
        reduceImg: false,
        option2: false
    });

    const handleCheckboxChange = (key) => {
        //take in the prev state and set our checkbox via its key to the opposite
        setChecked(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };
    
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

            <div className={styles.preview} >
                <img className={styles.img} src={previewUrl}></img>

                <Checkbox
                    checked={checkboxes.reduceImg}
                    onChange={() => handleCheckboxChange("reduceImg")}
                    label="Reduce image size?"
                />

                <Checkbox
                    checked={checkboxes.option2}
                    onChange={() => handleCheckboxChange("option2")}
                    label="option 2"
                />
            </div>
            
        </div>
    );
}