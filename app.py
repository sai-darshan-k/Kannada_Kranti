from flask import Flask, request, render_template, jsonify
import numpy as np
import os
import easyocr  # Import EasyOCR
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

app = Flask(__name__)

# Load the trained Keras model
model = load_model('final_writer_identification_model.keras')

# Class label mapping
class_labels = {0: 'Guhan', 1: 'Rohith', 2: 'Sai_Darshan', 3: 'Suhas'}

# Initialize EasyOCR reader for Kannada and English
reader = easyocr.Reader(['en', 'kn'])

# Mapping of English keywords to Kannada words
keyword_mapping = {
    'tayi': 'ತಾಯಿ',
    # Add more mappings as needed
}

# Image preprocessing function for writer identification
def preprocess_image(img_path):
    """Preprocess the image to match the input shape of the model."""
    img = image.load_img(img_path, target_size=(224, 224))  # Resize image to 224x224
    img = image.img_to_array(img)  # Convert image to array
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = img / 255.0  # Normalize the image
    return img

@app.route('/')
def index():
    """Render the main page."""
    return render_template('kannada.html')

@app.route('/identify_writer', methods=['GET'])
def identify_writer():
    """Render the writer identification page."""
    return render_template('identify_writer.html')

@app.route('/findme', methods=['GET'])
def findme():
    """Render the Find Keyword page."""
    return render_template('findme.html')

@app.route('/ocr', methods=['GET'])
def ocr():
    """Render the OCR page."""
    return render_template('ocr.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict the writer from the uploaded image."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded image temporarily
    file_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)  # Create temp directory if it doesn't exist
    file.save(file_path)

    # Preprocess the image
    img = preprocess_image(file_path)

    # Make a prediction
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)  # Get the confidence score for the predicted class

    # Clean up the temporary file
    os.remove(file_path)

    # Map the predicted class to the writer name
    predicted_writer_name = class_labels[predicted_class]

    # Return the predicted writer and confidence
    return jsonify({'predicted_writer': predicted_writer_name, 'confidence': confidence * 100}), 200

@app.route('/extract_text', methods=['POST'])
def extract_text():
    """Extract text from the uploaded image using EasyOCR and find keywords."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded image temporarily
    file_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)  # Create temp directory if it doesn't exist
    file.save(file_path)

    # Perform OCR on the image using EasyOCR
    try:
        results = reader.readtext(file_path)
        extracted_text = ""
        for (bbox, text, prob) in results:
            extracted_text += text + "\n"  # Concatenate extracted text
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Clean up the temporary file
    os.remove(file_path)

    # Return the extracted text
    return jsonify({'extracted_text': extracted_text}), 200

@app.route('/find_keyword', methods=['POST'])
def find_keyword():
    """Find and highlight the keyword in the extracted text."""
    if 'file' not in request.files or 'keyword' not in request.form:
        return jsonify({'error': 'No file part or keyword not provided'}), 400

    file = request.files['file']
    keyword = request.form['keyword'].strip()  # Get the keyword

    # Save the uploaded image temporarily
    file_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)  # Create temp directory if it doesn't exist
    file.save(file_path)

    # Perform OCR on the image using EasyOCR
    try:
        results = reader.readtext(file_path)
        extracted_text = ""
        for (bbox, text, prob) in results:
            extracted_text += text + "\n"  # Concatenate extracted text
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Clean up the temporary file
    os.remove(file_path)

    # Highlight the keyword if it exists in the extracted text
    keyword_found = False
    highlighted_text = extracted_text

    # Check if the keyword is in the mapping
    if keyword in keyword_mapping:
        # If the English keyword is found, find the corresponding Kannada word
        kannada_keyword = keyword_mapping[keyword]
        if kannada_keyword in extracted_text:
            keyword_found = True
            highlighted_text = highlighted_text.replace(kannada_keyword, f"<mark>{kannada_keyword}</mark>")  # Highlight the Kannada word

    # Check if the keyword exists directly in the extracted text
    elif keyword in extracted_text:
        keyword_found = True
        highlighted_text = highlighted_text.replace(keyword, f"<mark>{keyword}</mark>")  # Highlight the keyword

    return jsonify({
        'keyword_found': keyword_found,
        'highlighted_text': highlighted_text
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
