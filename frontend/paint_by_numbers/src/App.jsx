import PaintByNumbers from "./components/PaintByNumbers"
import Header from "./components/Header"
import './App.css';
import Title from "./components/Title";
import './components/fonts.css';
import Gallery from "./components/Gallery";

function App() {
  return (
    <div className="App">
      <Header></Header>
      <Title></Title>
      <Gallery></Gallery>
      <PaintByNumbers></PaintByNumbers>
    </div>
  )
}

export default App
