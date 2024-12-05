import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db
from blocklist import is_token_revoked
from flask_migrate import Migrate
from dotenv import load_dotenv

# import flask_oauthlib
import models

from resources.department import blp as DepartmentBlueprint
from resources.employee import blp as EmployeeBlueprint
from resources.vacation import blp as VacationBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "HR System API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):

        print(49)
        return is_token_revoked(jwt_payload)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "Token revoked", "error": "token revoked"},
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "Token is not fresh", "error": "fresh token required"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Token has expired", "error": "token expired"}),
            401,
        )

    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     print("test test")
    #     return (
    #         jsonify(
    #             {"message": "Signature verification failed", "error": "invalid token"}
    #         ),
    #         401,
    #     )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request has no access token",
                    "error": "authorization required",
                }
            ),
            401,
        )

    api.register_blueprint(DepartmentBlueprint)
    api.register_blueprint(EmployeeBlueprint)
    api.register_blueprint(VacationBlueprint)
    app.register_blueprint(UserBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
