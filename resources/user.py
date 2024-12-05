from flask.views import MethodView
import traceback
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
)
from models.user import UserModel
from schemas import UserSchema, UserLoginSchema
from db import db
from models.tokenblocklist import TokenBlocklist


blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        if UserModel.find_by_username(user_data["username"]):
            abort(400, message="A user with that username already exists.")
        if UserModel.find_by_email(user_data["email"]):
            abort(400, message="A user with that email already exists.")

        hashed_password = UserModel.hash_password(user_data["password"])
        user = UserModel(
            username=user_data["username"],
            password=hashed_password,
            email=user_data["email"],
        )
        try:
            user.save_to_db()
            user.send_confirmation_email()
            return user, 201
        except:
            traceback.print_exc()
            return {"message": "Failed to create user"}, 500


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


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        user = UserModel.find_by_email(email=login_data["email"])

        if user and UserModel.verify_password(user.password, login_data["password"]):
            if user.activated:
                access_token = create_access_token(identity=str(user.id), fresh=True)
                refresh_token = create_refresh_token(identity=str(user.id))
                return {"access_token": access_token, "refresh_token": refresh_token}
            abort(400, message="You have not confirmed registration, check your email")

        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        if TokenBlocklist.query.filter_by(jti=jti).first():
            return {"message": "Token already invalidated."}, 400
        blocked_token = TokenBlocklist(jti=jti)
        db.session.add(blocked_token)
        db.session.commit()
        return {"message": "Successfully logged out"}


@blp.route("/user/confirm/<int:user_id>")
class UserConfirm(MethodView):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")

        if user.activated:
            return {"message": "User is already activated."}, 200

        user.activated = True
        user.save_to_db()
        return {"message": "User has been activated successfully."}, 200
