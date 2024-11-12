Here's a README.md for GitHub, structured to explain each functionality (OCR, Writer Identification, and Keyword Search) in detail.

---

# Kannada Writer Identification and Keyword Search

This project is a Flask web application designed to perform three main tasks:
1. **Writer Identification**: Predict the writer based on uploaded handwriting samples.
2. **OCR (Optical Character Recognition)**: Extract Kannada and English text from images.
3. **Keyword Search**: Search for keywords in the extracted text, including keyword mappings between English and Kannada.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
  - [OCR](#ocr)
  - [Writer Identification](#writer-identification)
  - [Keyword Search](#keyword-search)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Writer Identification**: Predicts the writer's name from handwriting samples using a trained deep learning model.
- **OCR with EasyOCR**: Extracts Kannada and English text from images using EasyOCR.
- **Keyword Search**: Allows users to search and highlight specific keywords in the extracted text, including automatic keyword mapping between English and Kannada.

---

## Setup

### Prerequisites

- Python 3.7 or higher
- Flask
- TensorFlow
- EasyOCR
- numpy
- PIL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sai-darshan-k/kannada_kranti.git
   cd kannada_kranti
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the trained Keras model `final_writer_identification_model.keras` and place it in the project directory.

---

## Usage

Start the Flask application:

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000` to access the application.

---

### OCR

1. Go to the **OCR** page.
2. Upload an image containing Kannada and/or English text.
3. The app will use EasyOCR to extract text from the image and display it on the screen.

### Writer Identification

1. Go to the **Writer Identification** page.
2. Upload an image of handwriting.
3. The application will preprocess the image, pass it through a trained deep learning model, and return the predicted writer along with a confidence score.

### Keyword Search

1. Go to the **Keyword Search** page.
2. Upload an image containing text and enter a keyword to search.
3. The app will highlight the keyword if it appears in the text.
   - If the English keyword has a mapped Kannada word, the Kannada version will also be searched for and highlighted.

---

## Endpoints

### Web Pages
- `/` - Home page
- `/identify_writer` - Writer Identification page
- `/findme` - Keyword Search page
- `/ocr` - OCR page

### API Endpoints

- `POST /predict`
   - **Description**: Predicts the writer from an uploaded image of handwriting.
   - **Params**: `file` (image file)
   - **Returns**: JSON with `predicted_writer` and `confidence`.

- `POST /extract_text`
   - **Description**: Extracts Kannada and English text from an uploaded image.
   - **Params**: `file` (image file)
   - **Returns**: JSON with `extracted_text`.

- `POST /find_keyword`
   - **Description**: Searches for a specified keyword in the extracted text.
   - **Params**: `file` (image file), `keyword` (string)
   - **Returns**: JSON with `keyword_found` (boolean) and `highlighted_text` (string with keywords highlighted if found).

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions.

---

## License

This project is licensed under the MIT License.

--- 

Let me know if you'd like to add any additional sections or details!
