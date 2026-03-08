from jose import JWTError, jwt


class TokenService:
    def __init__(self, secret: str, algorithm: str) -> None:
        self._secret = secret
        self._algorithm = algorithm

    def decode(self, token: str) -> int | None:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return int(user_id)
        except (JWTError, ValueError):
            return None
