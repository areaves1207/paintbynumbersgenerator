import styles from "./generator.module.css"

export default function Generator(){
    return (
        <div className={styles.div}>
            <div className={styles.infoText}>Upload an image to generate it's canvas</div>

            <button className={styles.button}>Upload image</button>
        </div>
    );
}