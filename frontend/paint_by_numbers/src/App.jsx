import PaintByNumbers from "./components/PaintByNumbers"
import Header from "./components/Header"
import './App.css';
import Title from "./components/Title";
import './components/fonts.css';
import Gallery from "./components/Gallery";
import Generator from "./components/Generator";

function App() {
  return (
    <div className="App">
      <Header></Header>
      <div className={StyleSheet.body}>
        <Title></Title>
        <Gallery></Gallery>
        <Generator></Generator>
      </div>
    </div>
  )
}

export default App
