# app/resources/file_input_resource.py

from flask_restful import Resource
from flask import request
import pandas as pd
from utils.hatespeech_predict import textpreprocess, stemmer  # type: ignore
from utils.modification import save_to_db

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
