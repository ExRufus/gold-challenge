# app/main.py

# Import Flask and Flask extensions
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Import data analysis and visualization libraries
import pandas as pd

# Import preprocessing functions
from utils.hatespeech_predict import textpreprocess, stemmer  # type: ignore
import os
import sqlite3

# Get the absolute path
base_dir = os.path.dirname(os.path.abspath(__file__))
stop_words_path = os.path.join(base_dir, '../archive/stopwordbahasa.csv')
alaymap_path = os.path.join(base_dir, '../archive/alay_dictionary.csv')

# Read the stopwords file
try:
    stopwords_df = pd.read_csv(stop_words_path, header=None)
    stop_words = set(stopwords_df[0].tolist())
except Exception as e:
    print(f"Error reading stop words: {e}")
    stop_words = set()
    
# Read the alay dictionary file
try:
    alaymap_df = pd.read_csv(alaymap_path, delimiter=',', header=None)
    alaymap = dict(zip(alaymap_df[0], alaymap_df[1]))
except Exception as e:
    print(f"Error reading alay dictionary: {e}")
    alaymap = {}

# Function to get all processed texts from the database
def get_all_processed_texts():
    conn = sqlite3.connect('cleansed_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT original_text, cleaned_text FROM cleaned_texts')
    rows = cursor.fetchall()
    conn.close()

    texts = [{"original": row[0], "processed": row[1]} for row in rows]
    return texts

# Initialize Flask app
app = Flask(__name__)
SWAGGER_URL = '/api/docs' 
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={ 'app_name': "Data Cleansing API" }
)
app.register_blueprint(swaggerui_blueprint)

# Route to serve swagger.json
@app.route('/swagger.json')
def swagger_json():
    return send_from_directory(directory='static', path='swagger.json')

# Default route
@app.route('/')
def home():
    return jsonify({"message": "api/docs -> swagger"})

# Initialize Flask-RESTful
api = Api(app)
CORS(app)

from app.resources.text_input_resource import TextInputResource
from app.resources.file_input_resource import FileInputResource

# Setup resources
api.add_resource(TextInputResource, "/api/text", methods=["GET", "POST"])
api.add_resource(FileInputResource, "/api/file", methods=["POST"])

if __name__ == '__main__':
    app.run(debug=True, port=8000)
