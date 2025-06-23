import styles from './gallery.module.css';

import image from './images/1920x1080.jpg';

export default function Gallery(){
    return (
        <div className={styles.container}>
            <div className={styles.img}><img src={image}></img></div>
            <div className={styles.img}><img src={image}></img></div>
            <div className={styles.img}><img src={image}></img></div>
            <div className={styles.img}><img src={image}></img></div>
        </div>
    );
}