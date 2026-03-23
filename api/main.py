from fastapi import FastAPI, File, UploadFile
import uvicorn
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Load the model
MODEL_PATH = "../Models/1"
model = tf.keras.models.load_model(MODEL_PATH)

# Class names (assuming alphabetical order from dataset)
CLASS_NAMES = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

@app.get("/ping")
async def ping():
    return {"message": "Hello, I am alive"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read the image file
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # Resize to 256x256
    image = image.resize((256, 256))
    
    # Convert to array
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    
    # Add batch dimension
    img_array = tf.expand_dims(img_array, 0)
    
    # Predict
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_class_index]
    confidence = round(100 * np.max(predictions[0]), 2)
    
    return {
        "predicted_class": predicted_class,
        "confidence": confidence
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)