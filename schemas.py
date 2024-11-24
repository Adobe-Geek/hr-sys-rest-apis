from marshmallow import Schema, fields
from models.user import UserModel


class PlainDepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    abbreviation = fields.Str(required=True)
    # manager_id = fields.Int()


class PlainEmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    last_name = fields.Str(required=True)
    first_name = fields.Str(required=True)
    passport = fields.Str()
    birth_date = fields.Date()
    birth_place = fields.Str()
    address = fields.Str()
    hire_date = fields.Date()
    department_id = fields.Int()


class PlainVacationSchema(Schema):
    id = fields.Int(dump_only=True)
    # employee_id = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)


class VacationUpdateSchema(Schema):
    vacation_id = fields.Int(required=True)  # Int
    employee_id = fields.Int()
    start_date = fields.Date()  # Date
    end_date = fields.Date()  # Date


class DepartmentSchema(PlainDepartmentSchema):
    manager_id = fields.Int(load_only=True)
    # employees = fields.List(fields.Nested(PlainEmployeeSchema()), dump_only=True)
    employee = fields.Nested(PlainEmployeeSchema, dump_only=True)


class EmployeeSchema(PlainEmployeeSchema):
    department_id = fields.Int(load_only=True)
    vacations = fields.List(fields.Nested(PlainVacationSchema), dump_only=True)
    department = fields.Nested(PlainDepartmentSchema, dump_only=True)
    # departments = fields.List(fields.Nested(PlainDepartmentSchema()), dump_only=True)


class VacationSchema(PlainVacationSchema):
    employee_id = fields.Int(required=True, load_only=True)
    employee = fields.Nested(PlainEmployeeSchema, dump_only=True)


class UserSchema(Schema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)

    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
