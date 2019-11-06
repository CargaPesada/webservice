import firebase_admin
from flask import Flask
from flask_restful import Api
from controllers import users_controller, trucks_controller, offices_controller, schedules_controller, \
    services_controller, pieces_controller
from firebase_admin import credentials
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing enabled for all URI
api = Api(app)
cred = credentials.Certificate("database/credentials.json")
firebase_admin.initialize_app(cred)

# User endpoints
api.add_resource(users_controller.UsersController,
                 '/user/register', '/user/all', '/user/status')
api.add_resource(users_controller.UsersControllerById,
                 '/user/<user_mail>', '/user/delete/<user_mail>', '/user/update/<user_mail>')
api.add_resource(users_controller.UsersControllerByRegion,
                 '/user/all/<region>')
api.add_resource(users_controller.UsersControllerByJob,
                 '/user/job/<job>')

# Office endpoints
api.add_resource(offices_controller.OfficesController,
                 '/office/register', '/office/all')
api.add_resource(offices_controller.OfficeControllerById,
                 '/office/<office_id>', '/office/delete/<office_id>', '/office/update/<office_id>')
api.add_resource(offices_controller.OfficeControllerByRegion,
                 '/office/all/<region>')
api.add_resource(offices_controller.OfficeControllerByUser,
                 '/office/user/<cpf>')

# Trucks endpoints
api.add_resource(trucks_controller.TrucksController,
                 '/truck/register', '/truck/all')
api.add_resource(trucks_controller.TrucksControllerById,
                 '/truck/<truck_id>', '/truck/delete/<truck_id>', '/truck/update/<truck_id>')
api.add_resource(trucks_controller.TrucksControllerByRegion,
                 '/truck/all/<region>')

# Schedules endpoints
api.add_resource(schedules_controller.SchedulesController,
                 '/schedule/register', '/schedule/delete/<office_id>/<event_id>', '/schedule/list/<office_id>', '/schedule/update')

# Services endpoints
api.add_resource(services_controller.ServicesController,
                 '/service/list', '/service/register', '/service/delete/<service>', '/service/update')
# Pieces endpoints
api.add_resource(pieces_controller.PiecesController,
                 '/piece/list', '/piece/register', '/piece/delete/<piece>', '/piece/update')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
