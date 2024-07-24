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

# Function to save cleansed data to the database
def save_to_db(original_text, cleaned_text):
    conn = sqlite3.connect('cleansed_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO cleaned_texts (original_text, cleaned_text)
    VALUES (?, ?)
    ''', (original_text, cleaned_text))
    
    conn.commit()
    conn.close()

# Initialize Flask app
app = Flask(__name__)
SWAGGER_URL = '/api/docs' 
API_URL = '/static/swagger.json' 

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={ 'app_name': "Data Cleansing API" }
)
app.register_blueprint(swaggerui_blueprint)

# Route to serve swagger.json
@app.route('/static/swagger.json')
def swagger_json():
    return send_from_directory(directory='static', path='swagger.json')

# Initialize Flask-RESTful
api = Api(app)
CORS(app)



# Resource to handle text input
class TextInputResource(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            if not json_data or 'text' not in json_data:
                return {"error": "No text provided"}, 400
            
            text = json_data['text']
            processed_text = textpreprocess(text, stop_words, alaymap, stemmer)
            
            # Save to database
            save_to_db(text, processed_text)
            
            return {"original": text, "processed": processed_text}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

# Resource to handle file input
class FileInputResource(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"error": "No file provided"}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {"error": "No file selected"}, 400

        try:
            df = pd.read_csv(file, encoding='latin1')
            results = []
            for index, row in df.iterrows():
                text = row.get('Tweet', '')  # Adjust column name according to CSV
                processed_text = textpreprocess(text, stop_words, alaymap, stemmer)
                results.append({
                    "original": text,
                    "processed": processed_text
                })
                
                # Save to database
                save_to_db(text, processed_text)
            
            return {"results": results}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

# Setup resources
api.add_resource(TextInputResource, "/api/text", methods=["POST"])
api.add_resource(FileInputResource, "/api/file", methods=["POST"])

if __name__ == '__main__':
    app.run(debug=True, port=8000)
