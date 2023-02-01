import typing

import motor.motor_asyncio

from api.entities.movie import Movie
from api.repository.movie.abstractions import (MovieRepository,
                                               RepositoryException)


class MongoMovieRepository(MovieRepository):
    """
    Implements the repository pattern using a Mongo database
    """

    def __init__(
        self,
        conn_string: str = "mongodb://localhost:27017",
        database: str = "movie_track_db",
    ):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(conn_string)
        self._database = self._client[database]
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):

        await self._movies.update_one(
            {"id": movie.id},
            {
                "$set": {
                    "id": movie.id,
                    "title": movie.title,
                    "description": movie.description,
                    "release_year": movie.release_year,
                    "watched": movie.watched,
                }
            },
            upsert=True,
        )

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        document = await self._movies.find_one({"id": movie_id})
        if document:
            return Movie(
                movie_id=document.get("id"),
                title=document.get("title"),
                description=document.get("description"),
                release_year=document.get("release_year"),
                watched=document.get("watched"),
            )
        return None

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
        return_value: typing.List[Movie] = []
        # Get cursor from DB
        documents = self._movies.find({"title": title}).skip(skip).limit(limit)
        # Iterate through documents
        async for document in documents:
            return_value.append(
                Movie(
                    movie_id=document.get("id"),
                    title=document.get("title"),
                    description=document.get("description"),
                    release_year=document.get("release_year"),
                    watched=document.get("watched"),
                )
            )
        return return_value

    async def delete(self, movie_id: str) -> bool:
        await self._movies.delete_one({"id": movie_id})

    async def update(self, movie_id: str, params: dict):
        if "id" in params:
            raise RepositoryException("Can't update Movie ID")
        result = await self._movies.update_one({"id": movie_id}, {"$set": params})
        if result.modified_count == 0:
            raise RepositoryException(f"Movie: {movie_id} not updated")
