from db import db


class DepartmentModel(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    manager_id = db.Column(db.Integer)  # , db.ForeignKey("employees.id"))
    # employees = db.relationship("EmployeeModel", back_populates="department")
    employee = db.relationship("EmployeeModel", back_populates="departments")
