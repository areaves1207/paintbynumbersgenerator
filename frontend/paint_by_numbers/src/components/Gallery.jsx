import styles from './gallery.module.css';

import seaside from './images/pbn_seaside.png';
import food from './images/pbn_food.png';
import cat from './images/pbn_awesomecat.png';
import street from './images/pbn_street.png';

export default function Gallery(){
    return (
        <div className={styles.container}>
            <div className={styles.img}><img src={seaside}></img></div>
            <div className={styles.img}><img src={food}></img></div>
            <div className={styles.img}><img src={cat}></img></div>
            <div className={styles.img}><img src={street}></img></div>
        </div>
    );
}