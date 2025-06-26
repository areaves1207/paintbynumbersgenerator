import styles from './title.module.css';

export default function Title({onClickScroll}){
    return (
        <div className={styles.title}>
            <div className={styles.sirtitle}>
                PAINT BY NUMBERS GENERATOR
            </div>

            <div className={styles.subtitle}>
                CREATE ART FROM REALITY
            </div>

            <button onClick={onClickScroll} className={styles.button}>MAKE A CANVAS</button>
        </div>
    );
}