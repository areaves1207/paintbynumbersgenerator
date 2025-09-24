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
    const [imgTight, setImgTight] = useState(null);
    const [imgSmooth, setImgSmooth] = useState(null);
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
        setImgTight(null); setImgSmooth(null);
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

            const smoothImg = await zip.file("final_image_smooth.png").async("blob");
            // const tightImg = await zip.file("final_image_tight.png").async("blob");

            // const img1Url = URL.createObjectURL(tightImg);
            const img2Url = URL.createObjectURL(smoothImg);
            
            // setImgTight(img1Url);
            setImgSmooth(img2Url);
            
        }
        catch(err){
            console.error("Upload failed:", err);
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
                        {/* <Info 
                            questionText={"Why so long?"}
                            explanationText={"There are 2 primary reasons. First is that this is hosted for free on Render, which means they only allocate 0.1 CPU power to each request. It takes about 4-7 minutes just to get the server to aknowledge a request. Secondly, as it stands there is a lot of matrix manipulation that is done without NumPy which is much slower, but it is next on the optimization list. Hopefully we can get the time down soon. It works, it's just unfortunately very slow..."}>
                        </Info> */}
                    </div>)
                }

                {failure && 
                    <div className={styles.fail}>
                        <img className={styles.fail_img} src={X_img}></img>
                        <p>Error. Failed to generate.</p>
                    </div>
                }

            </div>)}
            
            {imgSmooth && <div className={styles.resultImages}>
                {/* <figure>
                    {<img src={imgTight} className={styles.result_img} alt="tight result" />}
                    <figcaption>Tight image</figcaption>
                    <a href={imgTight} download="tight_result.png">
                        <button>Download Tight Image</button>
                    </a>
                </figure> */}
                <figure>
                    {<img src={imgSmooth} className={styles.result_img} alt="Result" />}
                    <figcaption>Canvas</figcaption>
                    <a href={imgSmooth} download="canvas.png">
                        <button>Download Canvas</button>
                    </a>
                </figure>
            </div>}

        </div>
    );
});

export default Generator;
