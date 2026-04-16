from flask_cors import CORS
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2

app = Flask(__name__)
CORS(app)

# ✅ Load model (important fix)
model = tf.keras.models.load_model("model/sign_model.h5", compile=False)

# ✅ Load labels
with open("model/labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

@app.route("/")
def home():
    return "Backend running ✅"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image received"})

        file = request.files["image"]

        # ✅ Read image
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image"})

        print("Original shape:", img.shape)

        
        # Check if image has enough variation (hand present)
        if np.std(img) < 0.06:
         return  jsonify({
        "prediction": "No Sign",
        "confidence": 0
         })

        # ✅ Resize
        img = cv2.resize(img, (64, 64))

        # ✅ Convert to GRAYSCALE (VERY IMPORTANT)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ✅ Normalize
        img = img / 255.0

        # ✅ Reshape (match model input)
        img = img.reshape(1, 64, 64, 1)

        print("Final shape:", img.shape)

        # ✅ Prediction (safe method)
        prediction = model(img, training=False).numpy()

        confidence = float(np.max(prediction))
        class_index = int(np.argmax(prediction))

        # ✅ Confidence filter
        if confidence < 0.8:
            label = "No Sign"
        else:
            label = labels[class_index]

        print("Prediction:", label, "| Confidence:", confidence)

        return jsonify({
            "prediction": label,
            "confidence": confidence
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)