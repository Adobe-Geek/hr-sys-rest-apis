import os
from flask import Flask
from flask_smorest import Api
from db import db
from flask_migrate import Migrate
import models

from resources.department import blp as DepartmentBlueprint
from resources.employee import blp as EmployeeBlueprint
from resources.vacation import blp as VacationBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "HR System API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    print(os.getenv("DATABASE_URL"))
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY__TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    api.register_blueprint(DepartmentBlueprint)
    api.register_blueprint(EmployeeBlueprint)
    api.register_blueprint(VacationBlueprint)

    return app


# import uuid
# from flask import Flask, request
# from flask_smorest import abort
# from db import departments, employees, vacations

# app = Flask(__name__)


# @app.get("/department")
# def get_departments():
#     return {"departments": list(departments.values())}


# @app.post("/department")
# def create_department():
#     department_data = request.get_json()
#     department_id = uuid.uuid4().hex
#     department = {**department_data, "id": department_id}
#     departments[department_id] = department
#     return department, 201


# @app.get("/employee")
# def get_employees():
#     return {"employees": list(employees.values())}


# @app.get("/employee/<string:employee_id>")
# def get_employee(employee_id):
#     try:
#         return employees[employee_id]
#     except KeyError:
#         abort(404, message="Employee not found")


# @app.post("/employee")
# def create_employee():
#     employee_data = request.get_json()
#     employee_id = uuid.uuid4().hex
#     employee = {**employee_data, "id": employee_id}
#     employees[employee_id] = employee
#     return employee, 201


# @app.delete("/employee/<string:employee_id>")
# def delete_employee(employee_id):
#     try:
#         del employees[employee_id]
#         return {"message": "Employee deleted"}
#     except KeyError:
#         abort(404, message="Employee not found")


# @app.get("/vacation")
# def get_all_vacations():
#     return {"vacations": list(vacations.values())}


# @app.get("/vacation/<string:vacation_id>")
# def get_vacation(vacation_id):
#     try:
#         return vacations[vacation_id]
#     except KeyError:
#         abort(404, message="Vacation not found")


# @app.post("/vacation")
# def create_vacation():
#     vacation_data = request.get_json()
#     if vacation_data["employee_id"] not in employees:
#         abort(404, message="Employee not found")
#     vacation_id = uuid.uuid4().hex
#     vacation = {**vacation_data, "id": vacation_id}
#     vacations[vacation_id] = vacation
#     return vacation, 201


# @app.delete("/vacation/<string:vacation_id>")
# def delete_vacation(vacation_id):
#     try:
#         del vacations[vacation_id]
#         return {"message": "Vacation deleted"}
#     except KeyError:
#         abort(404, message="Vacation not found")


# @app.put("/vacation/<string:vacation_id>")
# def update_vacation(vacation_id):
#     vacation_data = request.get_json()
#     if "employee_id" not in vacation_data or "start_date" not in vacation_data:
#         abort(404, message="Bad request. Ensure 'employee_id' is in JSON payload")
#     try:
#         vacation = vacations[vacation_id]
#         vacation |= vacation_data
#         return vacation
#     except KeyError:
#         abort(404, message="Vacation not found")
