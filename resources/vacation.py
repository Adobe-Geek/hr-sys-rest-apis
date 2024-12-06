
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import VacationModel
from schemas import VacationSchema, VacationUpdateSchema

blp = Blueprint("vacations", __name__, description="Operations on vacations")


@blp.route("/vacation/<string:vacation_id>")
class Vacation(MethodView):
    @blp.response(200, VacationSchema)
    def get(self, vacation_id):
        vacation = VacationModel.query.get_or_404(vacation_id)
        return vacation

    def delete(self, vacation_id):
        vacation = VacationModel.query.get_or_404(vacation_id)
        db.session.delete(vacation)
        db.session.commit()
        return {"message": "Vacation deleted"}

    @blp.arguments(VacationUpdateSchema)
    @blp.response(200, VacationSchema)
    def put(self, vacation_data, vacation_id):
        vacation = VacationModel.query.get(vacation_id)
        if vacation:
            vacation.start_date = vacation_data["start_date"]
            vacation.end_date = vacation_data["end_date"]
        else:
            vacation = VacationModel(id=vacation_id, **vacation_data)

        db.session.add(vacation)
        db.session.commit()
        return vacation


@blp.route("/vacation")
class VacationList(MethodView):
    @blp.response(200, VacationSchema(many=True))
    def get(self):
        return VacationModel.query.all()

    @blp.arguments(VacationSchema)
    @blp.response(201, VacationSchema)
    def post(self, vacation_data):
        vacation = VacationModel(**vacation_data)
        try:
            db.session.add(vacation)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while inserting vacation record")
        return vacation
