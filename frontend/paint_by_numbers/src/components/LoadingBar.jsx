import React, { useState, useEffect } from 'react';
import styles from './loadingbar.module.css'

function LoadingBar() {
  const [progressValue, setProgressValue] = useState(0);
  const [isUploading, setUploading] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgressValue(prevProgress => {
        if(isUploading){
            if (prevProgress >= 100) {
                clearInterval(interval);
                prevProgress = 0;
                setUploading(false);
                return 0;
            }
            return prevProgress + 1;
        }else{
            if (prevProgress >= 95) {
                    clearInterval(interval);
                    prevProgress = 95;
                    return prevProgress;
                }
            
            return prevProgress + 1;  
        }

      });
    }, 3500);

    return () => clearInterval(interval);
  }, []);

  return (
    <>
    <div>Sending to backend...</div>
    <div className={styles.progressBarContainer}>
      <div
        className={isUploading ? styles.progressBarFiller : styles.progressBarFiller.processing}
        style={{ width: `${progressValue}%` }}
      ></div>
    </div>
    </>
  );
}

export default LoadingBar;