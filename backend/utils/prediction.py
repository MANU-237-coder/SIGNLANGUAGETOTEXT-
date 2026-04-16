import cv2
import numpy as np
import tensorflow as tf
import json

# =========================
# LOAD MODEL
# =========================
model = tf.keras.models.load_model("backend/model/sign_model.h5")

# =========================
# LOAD LABELS
# =========================
with open("backend/model/labels.json", "r") as f:
    labels_dict = json.load(f)

# Convert index → label
labels = {v: k for k, v in labels_dict.items()}

# =========================
# START CAMERA
# =========================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not working ❌")
    exit()

print("Press 'q' or ESC to quit")

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip for mirror view (optional but good)
    frame = cv2.flip(frame, 1)

    # =========================
    # CROP CENTER BOX
    # =========================
    h, w, _ = frame.shape

    x1, y1 = int(w * 0.3), int(h * 0.3)
    x2, y2 = int(w * 0.7), int(h * 0.7)

    roi = frame[y1:y2, x1:x2]

    # Draw box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # =========================
    # PREPROCESS ROI
    # =========================
    img = cv2.resize(roi, (64, 64))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img / 255.0
    img = np.reshape(img, (1, 64, 64, 1))

    # =========================
    # PREDICTION
    # =========================
    prediction = model.predict(img, verbose=0)
    class_index = np.argmax(prediction)
    label = labels[class_index]

    confidence = np.max(prediction)

    # =========================
    # DISPLAY TEXT
    # =========================
    text = f"{label} ({confidence:.2f})"

    cv2.putText(frame, text, (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    # =========================
    # SHOW WINDOW
    # =========================
    cv2.imshow("Sign Language Detection", frame)

    # =========================
    # EXIT KEY
    # =========================
    key = cv2.waitKey(1)

    if key == ord('q') or key == 27:
        print("Closing camera...")
        break

# =========================
# RELEASE
# =========================
cap.release()
cv2.destroyAllWindows()