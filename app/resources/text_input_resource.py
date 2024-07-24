# app/resources/text_input_resource.py

from flask_restful import Resource
from flask import request
from utils.hatespeech_predict import textpreprocess, stemmer  # type: ignore
from utils.modification import save_to_db, get_all_processed_texts

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

    def get(self):
        try:
            texts = get_all_processed_texts()
            return {"texts": texts}, 200
        except Exception as e:
            return {"error": str(e)}, 500
