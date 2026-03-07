from src.exceptions.article import ArticleNotFoundError
from src.exceptions.comment import CommentForbiddenError, CommentNotFoundError
from src.models.comment import Comment
from src.models.user import User
from src.repositories.article import ArticleRepository
from src.repositories.comment import CommentRepository


class CommentUseCases:
    def __init__(
        self,
        repository: CommentRepository,
        article_repository: ArticleRepository,
    ) -> None:
        self._repo = repository
        self._article_repo = article_repository

    async def add_comment(self, slug: str, body: str, author: User) -> Comment:
        article = await self._article_repo.get_by_slug(slug)
        if article is None:
            raise ArticleNotFoundError()

        comment = Comment(
            body=body,
            author_id=author.id,
            article_id=article.id,
        )
        comment = await self._repo.create(comment)
        return comment

    async def get_comments(self, slug: str) -> list[Comment]:
        article = await self._article_repo.get_by_slug(slug)
        if article is None:
            raise ArticleNotFoundError()

        return await self._repo.list_by_article_id(article.id)

    async def delete_comment(self, slug: str, comment_id: int, user: User) -> None:
        article = await self._article_repo.get_by_slug(slug)
        if article is None:
            raise ArticleNotFoundError()

        comment = await self._repo.get_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundError()

        if comment.author_id != user.id:
            raise CommentForbiddenError()

        await self._repo.delete(comment)
