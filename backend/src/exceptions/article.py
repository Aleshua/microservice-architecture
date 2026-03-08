class ArticleNotFoundError(Exception):
    def __init__(self) -> None:
        self.detail = "article not found"


class ArticleForbiddenError(Exception):
    def __init__(self) -> None:
        self.detail = "you are not the author of this article"


class SlugAlreadyExistsError(Exception):
    def __init__(self) -> None:
        self.detail = "article with this slug already exists"
