import abc
import typing

from api.entities.movie import Movie


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    async def create(self, movie: Movie):
        """
        Inserts a Movie into database

        Raises RepositoryException on failure
        """
        raise NotImplementedError

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """
        Retrieves a Movie by ID. Returns None if not found
        """
        raise NotImplementedError

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
        """
        Returns a list of Movies with the given title
        """
        raise NotImplementedError

    async def delete(self, movie_id: str) -> bool:
        """
        Deletes a movie by ID

        Raises RepositoryException on failure
        """
        raise NotImplementedError

    async def update(self, movie_id: str, params: dict):
        """
        Update a movie by its ID
        """
        raise NotImplementedError
