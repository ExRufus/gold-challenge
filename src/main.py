# Import Flask and Flask extensions
from flask import Flask, request, jsonify
from flask_restful import Resource, Api  # type: ignore
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS  # type: ignore

# Import data analysis and visualization libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.text_preprocessing import clean_text, alaymap, stop_words  # type: ignore
import os

# Inisiasi object flask
app = Flask(__name__)
SWAGGER_URL = '/api/docs' 
API_URL = '/static/swagger.json' 

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    }
)
app.register_blueprint(swaggerui_blueprint)

# inisiasi object flask_restful
api = Api(app)

# inisiasi object flask_cors
CORS(app)

# inisiasi variabel kosong bertipe dictionary
identitas = {}  # variable global , dictionary = json

# Membuat class Resource untuk menerima input teks
class TextInputResource(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            if not json_data or 'text' not in json_data:
                return {"error": "No text provided"}, 400
            
            text = json_data['text']
            processed_text = clean_text(text, alaymap, stop_words)
            
            return {"original": text, "processed": processed_text}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

# Membuat class Resource untuk menerima input file
class FileInputResource(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"error": "No file provided"}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {"error": "No file selected"}, 400

        try:
            df = pd.read_csv(file, encoding='latin1')  # Sesuaikan encoding jika diperlukan
            results = []
            for index, row in df.iterrows():
                text = row.get('Tweet', '')  # Sesuaikan nama kolom sesuai dengan file CSV
                processed_text = clean_text(text, alaymap, stop_words)
                results.append({
                    "original": text,
                    "processed": processed_text
                })
            
            return {"results": results}, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

# Setup resourcenya
api.add_resource(TextInputResource, "/api/text", methods=["POST"])
api.add_resource(FileInputResource, "/api/file", methods=["POST"])

if __name__ == '__main__':
    app.run(debug=True, port=8000)
