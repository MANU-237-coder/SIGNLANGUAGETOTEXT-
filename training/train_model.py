from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# ✅ Dataset paths
train_dir = "dataset/train"
test_dir = "dataset/test"

# ✅ Settings
img_size = (64, 64)
batch_size = 32

# ✅ Data Augmentation (important for accuracy)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2
)

test_datagen = ImageDataGenerator(rescale=1./255)

# ✅ Load data
train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    color_mode='grayscale',   # 🔥 IMPORTANT
    class_mode='categorical'
)

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=batch_size,
    color_mode='grayscale',   # 🔥 IMPORTANT
    class_mode='categorical'
)

# ✅ Build Model
model = Sequential()

model.add(Conv2D(32, (3,3), activation='relu', input_shape=(64,64,1)))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(128, (3,3), activation='relu'))
model.add(MaxPooling2D(2,2))

model.add(Flatten())

model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))

# ✅ OUTPUT LAYER (26 classes A–Z)
model.add(Dense(29, activation='softmax'))

# ✅ Compile
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# ✅ Train
model.fit(
    train_data,
    validation_data=test_data,
    epochs=10
)

# ✅ Save model
model.save("model.h5")

print("✅ Training Completed & Model Saved!")