from flask import Flask, render_template, request
import pandas as pd
import cv2
import numpy as np
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Dummy profiling function
def profile_city(data):
    # Perform profiling operations on the city data
    # Placeholder logic
    return data.describe().to_dict()

# Footpath assessment function
def assess_footpath(image):
    # Convert image from file stream to an OpenCV format
    file = image.read()
    nparr = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        logging.error("Image could not be read")
        raise ValueError("Image could not be read")

    # Dummy assessment logic
    assessment_result = "Assessment complete."
    return assessment_result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def profile():
    try:
        data = pd.read_csv('data/city_data.csv')
        profile_result = profile_city(data)
        return render_template('profile.html', result=profile_result)
    except FileNotFoundError:
        logging.error("Data file not found.")
        return "Data file not found.", 404
    except Exception as e:
        logging.error(f"An error occurred in profile: {str(e)}")
        return f"An error occurred: {str(e)}", 500

@app.route('/footpath-assessment', methods=['POST'])
def footpath_assessment():
    if 'footpath_image' not in request.files:
        logging.error("No file part")
        return "No file part", 400

    image = request.files['footpath_image']

    if image.filename == '':
        logging.error("No selected file")
        return "No selected file", 400

    try:
        # Call the function to assess the footpath
        assessment_result = assess_footpath(image)
        return render_template('assessment.html', result=assessment_result)
    except Exception as e:
        logging.error(f"Error during footpath assessment: {str(e)}")
        return f"An error occurred during assessment: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
