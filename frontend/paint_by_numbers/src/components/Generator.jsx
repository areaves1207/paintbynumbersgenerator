import Checkbox from "./Checkbox";
import styles from "./generator.module.css"
import { useState } from "react";

export default function Generator(){
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [selectedImgSize, setSelectedImgSize] = useState("480p");
    const [numColors, setNumColors ] = useState(16);


    const [checkboxes, setChecked] = useState({
        reduceImg: false,
        option2: false
    });

    const handleSlider = (event) =>{
        setNumColors(event.target.value);
    };

    const handleImgSizeChange = (changeEvent) => {
        setSelectedImgSize(changeEvent.target.value);
    };

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
                {selectedFile != null && (<img className={styles.img} src={previewUrl}></img>)}

                {selectedFile != null && (<div className={styles.checkboxes}>
                    <Checkbox
                        checked={checkboxes.reduceImg}
                        onChange={() => handleCheckboxChange("reduceImg")}
                        label="Reduce image size?"
                    />

                    {checkboxes.reduceImg && (
                        <div>
                            <label className={styles.radioLabel}> <input type="radio" value="480p" checked={selectedImgSize === "480p"} onChange={handleImgSizeChange}/>480p</label>
                            <label className={styles.radioLabel}> <input type="radio" value="720p" checked={selectedImgSize === "720p"} onChange={handleImgSizeChange}/>720p</label>
                            <label className={styles.radioLabel}> <input type="radio" value="1080p" checked={selectedImgSize === "1080p"} onChange={handleImgSizeChange}/>1080p</label>
                        </div>
                    )}

                    {/* <Checkbox
                        checked={checkboxes.option2}
                        onChange={() => handleCheckboxChange("option2")}
                        label="option 2"
                    /> */}
                </div>)}

                <div>
                    <input type="range" min="4" max="128" value={numColors} onChange={handleSlider}></input><p>{numColors}</p>
                </div>
            </div>
            
        </div>
    );
}