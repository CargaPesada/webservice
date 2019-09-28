import firebase_admin
from flask import Flask
from flask_restful import Api
from controllers import users_controller, trucks_controller, offices_controller
from firebase_admin import credentials
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing enabled for all URI
api = Api(app)
cred = credentials.Certificate("database/credentials.json")
firebase_admin.initialize_app(cred)

# User endpoints
api.add_resource(users_controller.UsersController,
                 '/user/register', '/user/all')
api.add_resource(users_controller.UsersControllerById,
                 '/user/<user_mail>', '/user/delete/<user_mail>', '/user/update/<user_mail>')
api.add_resource(users_controller.UsersControllerByRegion,
                 '/user/all/<region>')

# Office endpoints
api.add_resource(offices_controller.OfficesController,
                 '/office/register', '/office/all')
api.add_resource(offices_controller.OfficeControllerById,
                 '/office/<office_id>', '/office/delete/<office_id>', '/office/update/<office_id>')
api.add_resource(offices_controller.OfficeControllerByRegion,
                 '/office/all/<region>')

# Trucks endpoints
api.add_resource(trucks_controller.TrucksController,
                 '/truck/register', '/truck/all')
api.add_resource(trucks_controller.TrucksControllerById,
                 '/truck/<truck_id>', '/truck/delete/<truck_id>', '/truck/update/<truck_id>')
api.add_resource(trucks_controller.TrucksControllerByRegion,
                 '/truck/all/<region>')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
