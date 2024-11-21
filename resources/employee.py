import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import EmployeeModel
from schemas import EmployeeSchema

blp = Blueprint("employees", __name__, description="Operations on employees")


@blp.route("/employee/<string:employee_id>")
class Employee(MethodView):
    @blp.response(200, EmployeeSchema)
    def get(self, employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)
        print(employee.department_id)
        print(employee.department)
        print(employee.department.name)
        print(employee.department.__dict__)
        return employee

    def delete(self, employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return {"message": "Employee deleted"}


@blp.route("/employee")
class EmployeeList(MethodView):
    @blp.response(200, EmployeeSchema(many=True))
    def get(self):
        return EmployeeModel.query.all()

    @blp.arguments(EmployeeSchema)
    @blp.response(200, EmployeeSchema)
    def post(self, employee_data):
        employee = EmployeeModel(**employee_data)
        try:
            db.session.add(employee)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while inserting employee")

        return employee
