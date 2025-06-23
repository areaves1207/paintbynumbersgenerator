import styles from './footer.module.css';

import github_img from './images/github-mark.png';

const github_page = () => {
    window.open('https://github.com/areaves1207', '_blank');
}

export default function Footer(){
    return (
        <footer className={styles.footer}>

            <div className={styles.claims}>All rights reserved &copy;</div>
            <div onClick={github_page} className={styles.logos}>GitHub <img className={styles.img} src={github_img}></img></div>
        </footer>
    );
}