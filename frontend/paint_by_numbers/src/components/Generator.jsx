import SpinnerLoader from "./SpinnerLoader";
import X_img from './images/x_error.jpg';
import styles from "./generator.module.css"
import JSZip from "jszip";
import { forwardRef, useState } from "react";


const Generator = forwardRef((_, ref) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [numColors, setNumColors] = useState(8);
    //where the result imgs are stored
    const [combinedImg, setCombinedImg] = useState(null);
    const [canvas, setCanvas] = useState(null);
    const [palette, setPalette] = useState(null);
    const [generating, setGenerating] = useState(false);
    const [failure, setFailure] = useState(false);


    const [checkboxes, setChecked] = useState({
        reduceImg: false,
        option2: false
    });

    const handleSlider = (event) => {
        setNumColors(event.target.value);
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
        if (!file) {
            console.log("File failed");
            return;
        }


        var reader = new FileReader();
        reader.onload = function(e){
            var img = document.createElement("img");
            img.onload = function(event){
                var canvas = document.createElement("canvas");
                var ctx = canvas.getContext("2d");

                const scaled_dim1 = 640;
                const scaled_dim2 = 480;

                let width = img.width;
                let height = img.height;

                //keep the img either landscale or portrait
                if(width > height){ 
                    width = scaled_dim1
                    height = scaled_dim2
                }else{
                    width = scaled_dim2
                    height = scaled_dim1
                }
                canvas.width = width;
                canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);

                canvas.toBlob(function(blob) {
                    setSelectedFile(blob);
                    setPreviewUrl(URL.createObjectURL(blob));
                    console.log("Compressed photo has been blob-ed. Size: " + blob.size);
                }, 'image/jpeg', 0.75);

            }
            img.src = e.target.result;
        }
        reader.readAsDataURL(file);
    };

    // when the GENERATE button is clicked
    const handleSubmit = async() =>{
        setImgTight(null); combinedImg(null);
        setGenerating(true);
        setFailure(false);
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("numColors", numColors);
        const upload_url = "https://pbn-gen.onrender.com/upload_img/" 
        try{
            console.log(`Sending image to url: ${upload_url}`);

            const response = await fetch(upload_url, {

                method: "POST",
                body: formData,
            });


            const blob = await response.blob();
            if(response.status === 204){
                setFailure(true);
            }
            const zip = await JSZip.loadAsync(blob);

            const combinedImgZip = await zip.file("combined_img.png").async("blob");
            const canvasZip = await zip.file("canvas.png").async("blob");
            const paletteZip = await zip.file("palette.png").async("blob");

            const combinedImgURL = URL.createObjectURL(combinedImgZip);
            const canvasURL = URL.createObjectURL(canvasZip);
            const paletteURL = URL.createObjectURL(paletteZip);
            
            setCombinedImg(combinedImgURL);
            setCanvas(canvasURL);
            setPalette(paletteURL);
            
        }
        catch(err){
            console.error("Upload failed; ", err);
        }
        setGenerating(false);
    };

    return (
        <div className={styles.div} ref={ref}>
            <div className={styles.infoText}>Upload an image to generate its canvas</div>

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
                        <input type="range" min="4" max="16" value={numColors} onChange={handleSlider} />
                        {numColors}
                    </label>)
                }

                {!generating 
                    ? 
                    (<button className={styles.generateButton} onClick={handleSubmit}>GENERATE</button> )
                    :
                    (<div className={styles.spinner}>
                        <SpinnerLoader action={"Generating..."}/>
                    </div>)
                }

                {failure && 
                    <div className={styles.fail}>
                        <img className={styles.fail_img} src={X_img}></img>
                        <p>Error. Failed to generate.</p>
                    </div>
                }

            </div>)}
            
            {combinedImg && canvas && palette && <div className={styles.resultImages}>
                <figure>
                    {<img src={combinedImg} className={styles.result_img} alt="Combined Image" />}
                    <figcaption>Combined Image</figcaption>
                    <a href={combinedImg} download="combined_image.png">
                        <button>Download Entire Image</button>
                    </a>

                    <figcaption>Canvas</figcaption>
                    <a href={canvas} download="canvas.png">
                        <button>Download Canvas</button>
                    </a>

                    <figcaption>Palette</figcaption>
                    <a href={palette} download="palette.png">
                        <button>Download Color Palette</button>
                    </a>
                </figure>

            </div>}

        </div>
    );
});

export default Generator;
