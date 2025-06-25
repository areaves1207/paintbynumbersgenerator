import { useRef } from "react";
import PaintByNumbers from "./components/PaintByNumbers"
import Header from "./components/Header"
import './App.css';
import Title from "./components/Title";
import './components/fonts.css';
import Gallery from "./components/Gallery";
import Generator from "./components/Generator";
import Footer from "./components/Footer";


function App() {
  const generatorRef = useRef(null);

  const scrollToGenerator = () => {
    generatorRef.current?.scrollIntoView({ behavior: "smooth" });
  };


  return (
    <div className="App">
      <Header/>
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
