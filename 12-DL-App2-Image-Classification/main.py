import kagglehub
import tensorflow as tf

from tensorflow.keras import layers, models


# ============================================================
# 1. DOWNLOAD DATASET
# ============================================================

path = kagglehub.dataset_download(
    "aleemaparakatta/cats-and-dogs-mini-dataset"
)

print("Dataset downloaded to:")
print(path)


# ============================================================
# 2. DATASET PATH
# ============================================================

# Check the printed path and update this if necessary.
dataset_path = path

print("Dataset path:")
print(dataset_path)


# ============================================================
# 3. LOAD IMAGES
# ============================================================

img_height = 128
img_width = 128
batch_size = 32

train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)


# ============================================================
# 4. CHECK CLASSES
# ============================================================

print("Classes:")
print(train_dataset.class_names)


# ============================================================
# 5. CREATE CNN MODEL
# ============================================================

model = models.Sequential([

    # Input image
    layers.Input(
        shape=(128, 128, 3)
    ),

    # Convert pixels from 0-255 to 0-1
    layers.Rescaling(
        1.0 / 255
    ),

    # CNN Layer 1
    layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    # CNN Layer 2
    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    # Convert feature maps into one-dimensional data
    layers.Flatten(),

    # Fully connected layer
    layers.Dense(
        64,
        activation="relu"
    ),

    # Output: Cat or Dog
    layers.Dense(
        1,
        activation="sigmoid"
    )
])


# ============================================================
# 6. DISPLAY MODEL
# ============================================================

model.summary()


# ============================================================
# 7. COMPILE MODEL
# ============================================================

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


# ============================================================
# 8. TRAIN MODEL
# ============================================================

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=5
)


# ============================================================
# 9. EVALUATE MODEL
# ============================================================

loss, accuracy = model.evaluate(
    validation_dataset
)

print()
print("Validation Accuracy:", accuracy)


# ============================================================
# 10. SAVE MODEL
# ============================================================

model.save(
    "cat_dog_cnn.keras"
)

print()
print("===================================")
print("Model saved successfully!")
print("File: cat_dog_cnn.keras")
print("===================================")