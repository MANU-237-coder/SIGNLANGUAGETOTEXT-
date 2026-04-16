import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load model
model = load_model('../backend/model/sign_model.h5')

# Load class labels
labels_path = '../backend/model/labels.txt'
with open(labels_path, 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

print("Classes:", class_names)

# Test folder path
test_folder = '../dataset/test'

correct = 0
total = 0

for file in os.listdir(test_folder):
    if file.endswith(".jpg") or file.endswith(".png"):
        
        # True label from filename (A_test.jpg -> A)
        true_label = file.split("_")[0]

        img_path = os.path.join(test_folder, file)
        img = cv2.imread(img_path)

        if img is None:
            print("Skipping:", file)
            continue

        # Preprocess same as training
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (64, 64))
        img = img / 255.0
        img = img.reshape(1, 64, 64, 1)

        # Predict
        prediction = model.predict(img, verbose=0)
        predicted_class = class_names[np.argmax(prediction)]

        print(f"{file} → Predicted: {predicted_class} | Actual: {true_label}")

        if predicted_class == true_label:
            correct += 1
        
        total += 1

# Accuracy
accuracy = (correct / total) * 100
print("\n==============================")
print("Total Images:", total)
print("Correct Predictions:", correct)
print("Accuracy: {:.2f}%".format(accuracy))
print("==============================")
