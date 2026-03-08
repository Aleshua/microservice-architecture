from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt


class TokenService:
    def __init__(self, secret: str, algorithm: str, expire_minutes: int) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes)
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode(self, token: str) -> int | None:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return int(user_id)
        except (JWTError, ValueError):
            return None
