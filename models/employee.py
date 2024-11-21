from db import db


class EmployeeModel(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    passport = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(100))
    address = db.Column(db.String(100))
    hire_date = db.Column(db.Date)
    department_id = db.Column(
        db.Integer, db.ForeignKey("departments.id"), nullable=False
    )
    vacations = db.relationship(
        "VacationModel", back_populates="employee", lazy="dynamic"
    )
    # department = db.relationship("DepartmentModel", back_populates="employees")
    department = db.relationship(
        "DepartmentModel",
        # back_populates="department",
        foreign_keys="EmployeeModel.department_id",
    )
