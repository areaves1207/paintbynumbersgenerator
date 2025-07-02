import SpinnerLoader from "./SpinnerLoader";
import styles from "./generator.module.css"
import JSZip from "jszip";
import { forwardRef, useState } from "react";


const Generator = forwardRef((_, ref) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [selectedImgSize, setSelectedImgSize] = useState("480p");
    const [numColors, setNumColors] = useState(16);
    //where the result imgs are stored
    const [imgTight, setImgTight] = useState(null);
    const [imgSmooth, setImgSmooth] = useState(null);
    const [generating, setGenerating] = useState(false);


    const [checkboxes, setChecked] = useState({
        reduceImg: false,
        option2: false
    });

    const handleSlider = (event) => {
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
        setGenerating(false);
        const file = event.target.files[0];
        console.log(file);
        if (file) {
            setSelectedFile(file);
            setPreviewUrl(URL.createObjectURL(file));
        }

    };


    // when the GENERATE button is clicked
    const handleSubmit = async() =>{
        setImgTight(null); setImgSmooth(null);
        setGenerating(true);
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("numColors", numColors);

        try{
            const response = await fetch("http://localhost:8000/upload_img/", {
                method: "POST",
                body: formData,
            });


            const blob = await response.blob();
            const zip = await JSZip.loadAsync(blob);

            const smoothImg = await zip.file("final_image_smooth.png").async("blob");
            const tightImg = await zip.file("final_image_tight.png").async("blob");

            const img1Url = URL.createObjectURL(tightImg);
            const img2Url = URL.createObjectURL(smoothImg);
            
            setImgTight(img1Url);
            setImgSmooth(img2Url);
            setGenerating(false);
        }
        catch(err){
            console.error("UPload failed:", err);
        }
    };

    return (
        <div className={styles.div} ref={ref}>
            <div className={styles.infoText}>Upload an image to generate it's canvas</div>

            <input type='file' accept="image/*" className={styles.button} onChange={fileUploadHandler}></input>

            {selectedFile != null && 
            (<div className={styles.imageOptions}>
                
                <div className={styles.preview}>
                    <img className={styles.img} src={previewUrl}></img>
                </div>

                {/* slider bar */}
                {selectedFile != null &&
                    (<label className={styles.numColors}>
                        Number of Colors: 
                        <input type="range" min="4" max="64" value={numColors} onChange={handleSlider} />
                        {numColors}
                    </label>)
                }

                {!generating 
                    ? 
                    (<button className={styles.generateButton} onClick={handleSubmit}>GENERATE</button> )
                    :
                    (<div className={styles.spinner}><SpinnerLoader/></div>)
                }

            </div>)}
            
            {imgSmooth && imgTight && <div className={styles.resultImages}>
                <figure>
                    {<img src={imgTight} className={styles.result_img} alt="tight result" />}
                    <figcaption>Tight image</figcaption>
                    <a href={imgTight} download="tight_result.png">
                        <button>Download Tight Image</button>
                    </a>
                </figure>
                <figure>
                    {<img src={imgSmooth} className={styles.result_img} alt="smooth result" />}
                    <figcaption>Smooth image</figcaption>
                    <a href={imgTight} download="tight_result.png">
                        <button>Download Smooth Image</button>
                    </a>
                </figure>
            </div>}

        </div>
    );
});

export default Generator;
