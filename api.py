import cv2
import numpy as np
import io
import base64
from flask import Flask, request, render_template
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_v2_preprocess_input
import json

app = Flask(__name__)

model = tf.keras.models.load_model("dhaanviapi.hdf5")

map_dict = {0: 'Bacterial Leaf Blight',
            1: 'Brown Spot',
            2: 'Healthy',
            3: 'Leaf Blast',
            4: 'Leaf Scald',
            5: 'Narrow Brown Spot'}

# Load disease information from JSON file
with open("disease_info.json", "r") as f:
    disease_info = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_bytes = file.read()
            opencv_image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), 1)
            opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
            resized = cv2.resize(opencv_image, (224, 224))
            resized = mobilenet_v2_preprocess_input(resized)
            img_reshape = resized[np.newaxis, ...]

            prediction = model.predict(img_reshape).argmax()
            predicted_label = map_dict[prediction]

            # Convert OpenCV image to base64 for rendering in HTML
            _, buffer = cv2.imencode('.jpg', opencv_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            # Get disease information from the JSON file
            disease_name = map_dict[prediction]
            symptoms = disease_info[disease_name]["symptoms"]
            treatments = disease_info[disease_name]["treatments"]

            return render_template("result.html", predicted_label=predicted_label,
                                   symptoms=symptoms, treatments=treatments)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
