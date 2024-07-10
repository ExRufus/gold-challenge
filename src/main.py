# Import Flask and Flask extensions
from flask import Flask, request
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Import data analysis and visualization libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Inisiasi object flask
app = Flask(__name__)
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)


# inisiasi object flask_restful
api = Api(app)

# inisiasi object flask_cors
CORS(app)

# inisiasi variabel kosong bertipe dictionary
identitas = {} # variable global , dictionary = json

# membuat class Resource
class ContohResource(Resource):
    # metode get dan post
    def get(self):
        # response = {"msg": "Hallo dunia, ini app restfull pertamaku"}
        return identitas
    
    def post(self):
        # data: request.json
        nama = request.form["nama"]
        umur = request.form["umur"]
        identitas["nama"] = nama
        identitas["umur"] = umur
        response = {"msg": "Data berhasil dimasukkan"}
        return response

# setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
