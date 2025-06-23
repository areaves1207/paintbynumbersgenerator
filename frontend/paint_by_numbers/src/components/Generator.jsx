import styles from "./generator.module.css"

export default function Generator(){
    return (
        <div className={styles.div}>
            <div>Upload an image to generate it's canvas</div>

            <button>Upload image</button>
        </div>
    );
}