import React, { useRef, useEffect, useState } from "react";

function Camera() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const [prediction, setPrediction] = useState("");
  const [history, setHistory] = useState([]);

  const [sentence, setSentence] = useState("");
  const [currentWord, setCurrentWord] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [lastDetectedTime, setLastDetectedTime] = useState(Date.now());

  const dictionary = [
  // A
  "APPLE", "ANT", "AIR", "ARM", "ASK",
  
  // B
  "BALL", "BAT", "BAG", "BOOK", "BOY",
  
  // C
  "CAT", "CAR", "CUP", "CITY", "CALL",
  
  // D
  "DOG", "DAY", "DOOR", "DRINK", "DRESS",
  
  // E
  "EAT", "EAR", "EYE", "EGG", "ENTER",
  
  // F
  "FAN", "FISH", "FOOD", "FIRE", "FRIEND",
  
  // G
  "GO", "GIRL", "GAME", "GOOD", "GREAT",
  
  // H
  "HELLO", "HI", "HEY", "HOUSE", "HELP",
  
  // I
  "ICE", "INK", "IDEA", "ITEM", "IMPORTANT",
  
  // J
  "JOB", "JUMP", "JOIN", "JUICE", "JOKE",
  
  // K
  "KEY", "KIND", "KEEP", "KITCHEN", "KNOW",
  
  // L
  "LOVE", "LOOK", "LIST", "LIGHT", "LIFE",
  
  // M
  "MAN", "MAP", "MONEY", "MILK", "MOTHER",
  
  // N
  "NO", "NAME", "NICE", "NEED", "NUMBER",
  
  // O
  "OPEN", "ORDER", "ONLY", "OTHER", "OFF",
  
  // P
  "PEN", "PHONE", "PLAY", "PEOPLE", "PLEASE",
  
  // Q
  "QUIET", "QUICK", "QUESTION", "QUEUE", "QUIT",
  
  // R
  "RUN", "READ", "ROOM", "RIGHT", "ROAD",
  
  // S
  "SUN", "SEE", "SIT", "SCHOOL", "SMILE",
  
  // T
  "TIME", "TAKE", "TRY", "TABLE", "THANK",
  
  // U
  "USE", "UP", "UNDER", "UNIT", "USER",
  
  // V
  "VERY", "VIEW", "VOICE", "VISIT", "VALUE",
  
  // W
  "WATER", "WORK", "WALK", "WAIT", "WORD",
  
  // X
  "X-RAY", "XENON", "XMAS",
  
  // Y
  "YES", "YOU", "YOUR", "YOUNG", "YEAR",
  
  // Z
  "ZOO", "ZERO", "ZONE"
];

  useEffect(() => {
    startCamera();
    const interval = setInterval(captureAndPredict, 1500); // ⚡ faster
    return () => clearInterval(interval);
  }, []);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
  };

  const captureAndPredict = async () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    if (!video || !canvas) return;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, 224, 224);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      const formData = new FormData();
      formData.append("image", blob);

      try {
  const res = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    body: formData,
  });

        if (!res.ok) return;

        const data = await res.json();
        console.log("API Response:", data);

        // 🔥 HANDLE NO SIGN
        if (data.prediction === "No Sign") {
          setPrediction("No Sign");
          return;
        }

        // ✅ SHOW LETTER INSTANTLY
        setPrediction(data.prediction);
        setLastDetectedTime(Date.now());

        // 🔥 INSTANT SUGGESTIONS (FAST)
        generateSuggestions(currentWord + data.prediction);

        // 🔥 STABLE LOGIC FOR SENTENCE
        setHistory((prev) => {
          const updated = [...prev, data.prediction].slice(-5);

          const count = {};
          updated.forEach((p) => {
            count[p] = (count[p] || 0) + 1;
          });

          let best = "";
          let max = 0;

          for (let key in count) {
            if (count[key] > max) {
              best = key;
              max = count[key];
            }
          }

          // ✅ Faster stability
          if (max >= 5) {
            setCurrentWord((prevWord) => {
              if (prevWord.endsWith(best)) return prevWord;
              return prevWord + best;
            });
          }

          return updated;
        });

      } catch (err) {
        console.error("Error:", err);
      }
    }, "image/jpeg");
  };

  // 🔥 AUTO SPACE DETECTION
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();

      if (now - lastDetectedTime > 2000 && currentWord !== "") {
        setSentence((prev) => prev + currentWord + " ");
        setCurrentWord("");
        setSuggestions([]);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [lastDetectedTime, currentWord]);

  // 🔥 SUGGESTIONS (FAST + FLEXIBLE)
  const generateSuggestions = (text) => {
    if (!text) {
      setSuggestions([]);
      return;
    }

    const filtered = dictionary.filter((word) =>
      word.startsWith(text.toUpperCase())
    );

    setSuggestions(filtered.slice(0, 4));
  };

  // 🔥 CLEAR
  const clearText = () => {
    setSentence("");
    setCurrentWord("");
    setPrediction("");
    setSuggestions([]);
    setHistory([]);
  };

  // 🔥 SPEAK
  const speakText = () => {
    const fullText = sentence + currentWord;
    if (!fullText) return;

    const speech = new SpeechSynthesisUtterance(fullText);
    window.speechSynthesis.speak(speech);
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>Sign Language Detection</h2>

      <video ref={videoRef} autoPlay width="300" height="300" />

      <canvas
        ref={canvasRef}
        width="224"
        height="224"
        style={{ display: "none" }}
      />

      {/* 🔥 CHARACTER */}
      <h2>Character : {prediction || "None"}</h2>

      {/* 🔥 SENTENCE */}
      <h2>Sentence : {sentence + currentWord}</h2>

      {/* 🔥 SUGGESTIONS */}
      <div>
        <h3 style={{ color: "red" }}>Suggestions:</h3>
        {suggestions.map((word, index) => (
          <button
            key={index}
            onClick={() => {
              setSentence((prev) => prev + word + " ");
              setCurrentWord("");
              setSuggestions([]);
            }}
            style={{ margin: "5px", padding: "10px" }}











            
          >
            {word}
          </button>
        ))}
      </div>

      {/* 🔥 BUTTONS */}
      <div style={{ marginTop: "20px" }}>
        <button onClick={clearText}>Clear</button>
        <button onClick={speakText} style={{ marginLeft: "10px" }}>
          Speak
        </button>
      </div>
    </div>
  );
}

export default Camera;