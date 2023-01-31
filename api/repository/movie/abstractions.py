import abc
import typing

from api.entities.movie import Movie


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    def create(self, movie: Movie):
        """
        Creates a movie and returns true on success

        Raises RepositoryException on failure
        """
        raise NotImplementedError

    def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """
        Retrieves a Movie by ID. Returns None if not found
        """
        raise NotImplementedError

    def get_by_title(self, title: str) -> typing.List[Movie]:
        """
        Returns a list of Movies with the given title
        """
        raise NotImplementedError

    def delete(self, movie_id: str) -> bool:
        """
        Deletes a movie by ID

        Raises RepositoryException on failure
        """
        raise NotImplementedError

    def update(self, movie_id: str, params: dict):
        """
        Update a movie by its ID
        """
        raise NotImplementedError
