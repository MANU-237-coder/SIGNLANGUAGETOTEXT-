import React, { useState } from "react";
import Camera from "./Camera";
import "./styles.css";

function App() {
  const [text, setText] = useState("");

  const updateText = (letter) => {
    console.log("RECEIVED:", letter);

    if (!letter || letter === "nothing") return;

    if (letter === "space") {
      setText((prev) => prev + " ");
    } else if (letter === "del") {
      setText((prev) => prev.slice(0, -1));
    } else {
      setText((prev) => prev + letter);
    }
  };

  return (
    <div className="app">
      <h1>Sign Language to Text</h1>
      <Camera setResult={updateText} />
      <h2>{text}</h2>
    </div>
  );
}

export default App;
