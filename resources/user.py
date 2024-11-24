from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import jwt_required, create_access_token
from models.user import UserModel
from schemas import UserSchema

blp = Blueprint("users", __name__, description="operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        if UserModel.find_by_username(user_data["username"]):
            abort(400, message="A user with that username already exists.")

        hashed_password = pbkdf2_sha256.hash(user_data["password"])
        user = UserModel(username=user_data["username"], password=hashed_password)
        user.save_to_db()
        return user


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        user.delete_from_db()
        return {"message": "User deleted."}, 200
