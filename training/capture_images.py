import cv2
import os

sign = input("Enter Sign Name (A-J): ").upper()
mode = input("train or val: ").lower()

save_dir = f"../dataset/{mode}/{sign}"
os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Press 'c' to capture image")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture Images", frame)
    key = cv2.waitKey(1)

    if key == ord('c'):
        path = f"{save_dir}/{count}.jpg"
        cv2.imwrite(path, frame)
        print("Saved:", path)
        count += 1

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("DONE")
