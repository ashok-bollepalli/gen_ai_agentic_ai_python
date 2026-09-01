import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ============================================================
# 1. LOAD MODEL
# ============================================================

model = tf.keras.models.load_model("cat_dog_cnn_model.keras")

# ============================================================
# 2. STREAMLIT UI
# ============================================================

st.title("🐱🐶 Cat vs Dog Image Classifier")

st.write("Upload an image and the model will predict whether it is a Cat or Dog.")

# ============================================================
# 3. UPLOAD IMAGE
# ============================================================

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

# ============================================================
# 4. IMAGE CLASSIFICATION
# ============================================================

if uploaded_file is not None:

    # Read image
    image = Image.open(uploaded_file)

    # Display image
    st.image(
        image,
        caption="Uploaded Image",
        width=300
    )

    # Predict button
    if st.button("Classify Image"):

        # Resize image
        image = image.resize((128, 128))

        # Convert image to NumPy array
        image_array = np.array(image)

        # If image has RGBA channel, convert to RGB
        if image_array.shape[-1] == 4:
            image_array = image_array[:, :, :3]

        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)

        # Prediction
        prediction = model.predict(image_array)

        probability = prediction[0][0]

        # ====================================================
        # RESULT
        # ====================================================

        if probability >= 0.5:
            result = "Dog"
            confidence = probability
        else:
            result = "Cat"
            confidence = 1 - probability

        st.success(f"Prediction: {result}")

        st.write(
            f"Confidence: {confidence * 100:.2f}%"
        )
