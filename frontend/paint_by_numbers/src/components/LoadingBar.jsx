import React, { useState, useEffect } from 'react';
import styles from './loadingbar.module.css'

function LoadingBar() {
  const [progressValue, setProgressValue] = useState(0);
  const [isUploading, setUploading] = useState(true);
  const [isMaxTime, setIsMaxTime] = useState(false);

  useEffect(() => {
    const maxProgress = 95;
    const delay = isUploading ? 450 : 1995

    const startTime = Date.now();
    const duration = 10000;
    setProgressValue(Math.min(((Date.now() - startTime) / duration) * maxProgress, maxProgress));


    const interval = setInterval(() => {
      setProgressValue(prev => {
        if (prev >= maxProgress) {
          if (isUploading){
            setUploading(false);
            prev = 0;
          }else{
            setIsMaxTime(true);
          }
          return prev;
        }
        return prev + 1;
      });
    }, delay);

    return () => clearInterval(interval);
  }, [isUploading]);

  return (
    <>
      {!isMaxTime && (isUploading ? <div>Sending to backend...</div> : <div>Processing</div>)}
      {isMaxTime && <div>Finalizing image. This may take a minute...</div>}
      <div className={styles.progressBarContainer}>
        <div
          className={isUploading ? styles.progressBarFiller : `${styles.progressBarFiller} ${styles.processing}`}
          style={{ width: `${progressValue}%` }}
        ></div>
      </div>
    </>
  );
}

export default LoadingBar;
