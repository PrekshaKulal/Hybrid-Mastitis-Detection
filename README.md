# AI-Based Mastitis Disease Detection System

This project is developed as part of my academic work.
The objective of this project is to detect Mastitis disease using Artificial Intelligence and Deep Learning techniques.

The system uses a hybrid approach that combines image-based analysis and symptom-based prediction to support early and accurate detection.

## Project Description
Mastitis is a common disease affecting dairy animals and can cause serious health and economic loss if not detected early.
This project implements a hybrid AI model that integrates:
- A Convolutional Neural Network (CNN) for image-based Mastitis detection
- An Artificial Neural Network (ANN) for symptom-based prediction

The final prediction is obtained by combining the outputs of both models using an average-based hybrid logic.

## Data Processing and Preprocessing
The following data processing steps are applied before model training and prediction:

### Image Data Processing
- Image resizing and normalization
- Noise reduction and enhancement
- Conversion of images into numerical arrays
- Dataset splitting into training and testing sets

### Symptom Data Processing
- Handling missing values
- Encoding symptom data
- Feature normalization and scaling
- Preparation of input features for ANN model

These preprocessing steps help improve model accuracy and reliability.

## Hybrid Prediction Logic
Predictions from the CNN image model and ANN symptom model are generated independently.
The final result is calculated by averaging both predictions to produce a combined output.
This hybrid method enhances decision accuracy by using both visual and symptom-based information.

## Technologies Used
- Python
- Jupyter Notebook / Google Colab
- Machine Learning & Deep Learning
- TensorFlow, Keras
- NumPy, Pandas
- OpenCV
- Streamlit (for web-based user interface)

## Project Structure
- `MainProject.ipynb` : Data preprocessing, model training, and evaluation
- `app.py` : Streamlit application file
- `home.py`, `about.py`, `contact.py` : Streamlit UI pages
- `hybrid.py` : Hybrid prediction logic
- `image.py` : Image processing and prediction
- `symptoms.py` : Symptom-based prediction
- Trained model files (`.h5`)
- Supporting datasets and assets

## Dataset
Image and symptom-based datasets are used for Mastitis detection.


## How to Run the Project
1. Install required Python libraries
2. Run the Streamlit application:
3. Upload an image and enter symptom details to obtain prediction results

## Applications
- Early detection of Mastitis in dairy animals
- AI-assisted veterinary diagnosis
- Academic and research applications

## Note
This project is developed for academic learning and demonstration purposes only.
