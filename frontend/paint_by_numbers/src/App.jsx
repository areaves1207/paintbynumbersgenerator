import { useEffect, useRef, useState} from "react";
import PaintByNumbers from "./components/PaintByNumbers"
import Header from "./components/Header"
import './App.css';
import Title from "./components/Title";
import './components/fonts.css';
import Gallery from "./components/Gallery";
import Generator from "./components/Generator";
import Footer from "./components/Footer";
import Popup from "./components/Popup";


function App() {
  const generatorRef = useRef(null);
  const [isPopupOpen, setPopupOpen] = useState(false);

  const scrollToGenerator = () => {
    generatorRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(()=>{ //if we have visited the site before, and then closed the about page, dont open it on refresh.
    const visitedBefore = localStorage.getItem("popupClosed");
    if(visitedBefore === "true"){
      setPopupOpen(false);
    }else{
      setPopupOpen(true);
    }
  }, [])

  const closePopup = () =>{
    setPopupOpen(false)
    localStorage.setItem("popupClosed", "true")
  }


  return (
    <div className="App">
      <Header openPopup={()=> setPopupOpen(true)}/>

      {isPopupOpen && <Popup isOpen={isPopupOpen} onClose={() => closePopup()}>
        <h1>Welcome to my Paint By Numbers Generator!</h1>

        <h3>
          This project was made after I kept seeing instagram ads for paint by number kits available for purchase.
          After recently taking a computer vision class last year, I decided it would be fun to work on something similar
          in my free time. Over the last few weeks, I've spent a couple hours a day working from the ground up,
          using what I learned in my classes for the back end, and learning a ton of brand new stuff with React, HTML, CSS,
          and other things for my front end.
        </h3>

        <h4>
          When I first got this project running, it wasn't that optimized; there were many matrix operations that were very slow. Over the
          course of a few weeks, I've cut image generation time from ~15 minutes down to ~3! The fun part about this project is that I have implemented just about *everything* myself, such as a custom Canny edge
          detector, K-Means clustering, palette generation, etc.
        </h4>

        <h4>
          This site is hosted by Vercel and the back end is hosted by Render. FastAPI is used to connect everything.
          Since both are free hosting sites, the input and output is limited, and so the wait times for generating an
          image are unfortunately longer than I'd like and the outputs have to be pretty small (640x480).
        </h4>

        <h4>
          Thank you for checking it out! It's been a fun project to work on, and my first ever full stack development!
        </h4>

        <h6>
          To see this message again, click the "About" button in the top right corner, or clear your cookies.
        </h6>

      </Popup>}

      <div className={StyleSheet.body}>
        <Title onClickScroll={scrollToGenerator}/>
        <Gallery/>
        <Generator ref={generatorRef}/>
      </div>
      <Footer/>
    </div>
  )
}

export default App
