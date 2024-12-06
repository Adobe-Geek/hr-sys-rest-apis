
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import DepartmentModel
from schemas import DepartmentSchema

blp = Blueprint("departments", __name__, description="Operations on departments")


@blp.route("/department")
class DepartmentList(MethodView):
    @blp.response(200, DepartmentSchema(many=True))
    def get(self):
        return DepartmentModel.query.all()

    @blp.arguments(DepartmentSchema)
    @blp.response(200, DepartmentSchema)
    def post(self, department_data):
        department = DepartmentModel(**department_data)
        try:
            db.session.add(department)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while inserting department")

        return department
