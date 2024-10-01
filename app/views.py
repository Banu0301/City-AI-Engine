from flask import render_template, request
from app import app
import pandas as pd
from app.models.profiling_model import profile_city
from app.models.footpath_assessment import assess_footpath

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def profile():
    # Ensure the 'data/city_data.csv' file exists
    try:
        data = pd.read_csv('data/city_data.csv')
    except FileNotFoundError:
        return "Data file not found.", 404

    profile_result = profile_city(data)
    return render_template('profile.html', result=profile_result)

@app.route('/footpath-assessment', methods=['POST'])
def footpath_assessment():
    if 'footpath_image' not in request.files:
        return "No file part", 400

    image = request.files['footpath_image']
    assessment_result = assess_footpath(image)
    return render_template('assessment.html', result=assessment_result)
