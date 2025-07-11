import styles from './header.module.css';

export default function Header({openPopup}){
    return (
            <div className={styles.header}>
                <div className={styles.logo} onClick={() => window.location.reload()}>Logo</div>
                <nav className={styles.nav}>
                    <ul>
                    <li onClick={() => openPopup()}><a>About</a></li>
                    <li><a href="https://github.com/areaves1207" target="_blank">Github</a></li>
                    <li><a href="https://github.com/areaves1207/paintbynumbersgenerator" target="_blank">Repo</a></li>
                    </ul>
                </nav>
            </div>
    );
}