from fastapi import FastAPI, File, UploadFile
import uvicorn
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Load the model
MODEL_PATH = "../Models/1"
loaded_model = None
infer = None
use_keras_model = False

try:
    # Keras path first (supports .h5, .keras, and TF Keras SavedModel in some envs)
    loaded_model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    use_keras_model = True
except Exception:
    # Fallback: load as tf.saved_model and use a signature for inference
    loaded_model = tf.saved_model.load(MODEL_PATH)
    infer = loaded_model.signatures.get("serving_default")
    if infer is None:
        raise RuntimeError("SavedModel has no serving_default signature")

# Class names (assuming alphabetical order from dataset)
CLASS_NAMES = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

@app.get("/ping")
async def ping():
    return {"message": "Hello, I am alive"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        print("---- REQUEST START ----")

        if not file:
            return {"error": "No file received"}

        print("Filename:", file.filename)

        image_data = await file.read()
        print("File size:", len(image_data))

        if len(image_data) == 0:
            return {"error": "Empty file"}

        image = Image.open(io.BytesIO(image_data))
        print("Image opened successfully")

        image = image.resize((256, 256))
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = img_array / 255.0
        img_array = tf.expand_dims(img_array, 0)

        print("Running prediction...")

        if use_keras_model:
            predictions = loaded_model.predict(img_array)
        else:
            out = infer(tf.constant(img_array))
            predictions = next(iter(out.values())).numpy()

        predicted_class_index = np.argmax(predictions[0])
        predicted_class = CLASS_NAMES[predicted_class_index]
        confidence = round(100 * np.max(predictions[0]), 2)

        print("Prediction done")

        return {
            "predicted_class": predicted_class,
            "confidence": confidence
        }

    except Exception as e:
        print("ERROR OCCURRED:", str(e))
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)