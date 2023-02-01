import typing

from api.entities.movie import Movie
from api.repository.movie.abstractions import (MovieRepository,
                                               RepositoryException)


class MemoryMovieRepository(MovieRepository):
    """
    Implements the repository pattern using a simple in memory database
    """

    def __init__(self):
        self._storage = {}

    async def create(self, movie: Movie):
        self._storage[movie.id] = movie

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        return self._storage.get(movie_id)

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
        return_value = []
        for _, value in self._storage.items():
            if title == value.title:
                return_value.append(value)
        if limit == 0:
            return return_value[skip:]
        return return_value[skip : skip + limit]

    async def delete(self, movie_id: str) -> bool:
        self._storage.pop(movie_id, None)

    async def update(self, movie_id: str, params: dict):
        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"Movie: {movie_id} not found")
        for key, value in params.items():
            if key == "id":
                raise RepositoryException("Can't update Movie ID.")
            if hasattr(movie, key):
                setattr(movie, f"_{key}", value)
