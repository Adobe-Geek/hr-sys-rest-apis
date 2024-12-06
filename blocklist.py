from models.tokenblocklist import TokenBlocklist


def is_token_revoked(jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None
