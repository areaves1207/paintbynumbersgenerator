import styles from './header.module.css';

export default function Header(){
    return (
            <div className={styles.header}>
                <p>Logo</p>
                <nav className={styles.nav}>
                    <ul>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Portfolio</a></li>
                    <li><a href="#contact">Contact</a></li>
                    </ul>
                </nav>
            </div>
    );
}