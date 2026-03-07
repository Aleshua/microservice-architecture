class EmailOrUsernameTakenError(Exception):
    def __init__(self, detail: str = "email or username already taken") -> None:
        self.detail = detail


class EmailTakenError(EmailOrUsernameTakenError):
    def __init__(self) -> None:
        super().__init__("email already taken")


class UsernameTakenError(EmailOrUsernameTakenError):
    def __init__(self) -> None:
        super().__init__("username already taken")


class InvalidCredentialsError(Exception):
    def __init__(self) -> None:
        self.detail = "invalid email or password"
