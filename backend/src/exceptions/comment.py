class CommentNotFoundError(Exception):
    def __init__(self) -> None:
        self.detail = "comment not found"


class CommentForbiddenError(Exception):
    def __init__(self) -> None:
        self.detail = "you are not the author of this comment"
