# Import Flask and Flask extensions
from flask import Flask, request
from flask_restful import Resource, Api  # type: ignore
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS  # type: ignore

# Import data analysis and visualization libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.text_preprocessing import clean_text as prc

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

# membuat class Resource
class ContohResource(Resource):
    def get(self):
        inp = "- disaat semua cowok berusaha melacak perhatia.."
        return {
            "original": inp,
            "processed": prc(inp)}
    
    def post(self):
        data = request.get_json()  # assuming the data is sent in JSON format
        nama = data.get("nama")
        umur = data.get("umur")
        identitas["nama"] = nama
        identitas["umur"] = umur
        response = {"msg": "Data berhasil dimasukkan"}
        return response

# setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

if __name__ == '__main__':
    app.run(debug=True, port=8000)
