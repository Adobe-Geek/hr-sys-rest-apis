from db import db


class DepartmentModel(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    manager_id = db.Column(
        db.Integer, db.ForeignKey("employees.id", use_alter=True, name="fk_manager_id")
    )
    # employees = db.relationship("EmployeeModel", back_populates="department")
    # employee = db.relationship("EmployeeModel", back_populates="departments")
    manager = db.relationship(
        "EmployeeModel", foreign_keys=[manager_id], backref="managed_department"
    )
    employees = db.relationship(
        "EmployeeModel",
        back_populates="department",
        foreign_keys="EmployeeModel.department_id",
    )
