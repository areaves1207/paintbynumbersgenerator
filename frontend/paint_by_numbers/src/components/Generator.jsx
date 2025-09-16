import SpinnerLoader from "./SpinnerLoader";
import styles from "./generator.module.css"
import JSZip from "jszip";
import { forwardRef, useState } from "react";


const Generator = forwardRef((_, ref) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
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
                }, file.type, 0.8);

            }
            img.src = e.target.result;
        }
        reader.readAsDataURL(file);
    };


    // when the GENERATE button is clicked
    const handleSubmit = async() =>{
        setImgTight(null); setImgSmooth(null);
        setGenerating(true);
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("numColors", numColors);
        const upload_url = "https://paintbynumbersgenerator-h1lp.onrender.com/upload_img/"
        try{
            console.log(`Sending image to url: ${upload_url}`);

            const response = await fetch(upload_url, {

                method: "POST",
                body: formData,
            });


            const blob = await response.blob();
            const zip = await JSZip.loadAsync(blob);

            const smoothImg = await zip.file("final_image_smooth.png").async("blob");
            // const tightImg = await zip.file("final_image_tight.png").async("blob");

            const img1Url = URL.createObjectURL(tightImg);
            // const img2Url = URL.createObjectURL(smoothImg);
            
            setImgTight(img1Url);
            // setImgSmooth(img2Url);
            
        }
        catch(err){
            console.error("Upload failed:", err);
        }
        setGenerating(false);
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
