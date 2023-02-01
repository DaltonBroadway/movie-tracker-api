import dataclasses
import typing
import uuid
from collections import namedtuple
from functools import lru_cache

from fastapi import (APIRouter, Body, Depends, Header, HTTPException, Path,
                     Query)
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt, JWTError
from starlette.responses import JSONResponse, Response

from api.dto.detail import DetailResponse
from api.dto.movie import (CreateMovieBody, MovieCreatedResponse,
                           MovieResponse, MovieUpdateBody)
from api.entities.movie import Movie
from api.repository.movie.abstractions import (MovieRepository,
                                               RepositoryException)
from api.repository.movie.mongo import MongoMovieRepository
from api.settings import Settings, settings_instance

http_basic = HTTPBasic()


def basic_authentication(credentials: HTTPBasicCredentials = Depends(http_basic)):
    if credentials.username == "Bruce" and credentials.password == "basic":
        return
    raise HTTPException(status_code=401, detail="invalid_credentials")


@dataclasses.dataclass
class Token:
    name: str
    admin: bool


def authenticate_jwt(authorization: typing.Union[str, None] = Header(default=None)):
    token_secret = 'TEST_SECRET'
    if authorization is None:
        raise HTTPException(status_code=401, detail="invalid_token")
    token = authorization.split(" ")[1]
    try:
        token_payload = jwt.decode(token, token_secret, algorithms=['HS256'])
    except JWTError as e:
        raise HTTPException(status_code=401, detail="invalid_token") from e
    return Token(name=token_payload.get("name"), admin=token_payload.get("admin", False))


router = APIRouter(
    prefix="/api/v1/movies",
    tags=["movies"],
    dependencies=[Depends(basic_authentication)],
)


@lru_cache()
def movie_repository(settings: Settings = Depends(settings_instance)):
    """
    Movie repository to be used as a FastAPI dependency
    """
    return MongoMovieRepository(
        conn_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


def pagination_params(
    skip: int = Query(0, title="skip", description="Number of items to skip", ge=0),
    limit: int = Query(
        0, title="limit", description="Limit of items to to return", le=1000
    ),
):
    Pagination = namedtuple("Pagination", ["skip", "limit"])
    return Pagination(skip, limit)


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def create_movie(
    movie: CreateMovieBody = Body(..., title="Movie", description="Movie Details"),
    repo: MovieRepository = Depends(movie_repository),
):
    """
    Creates a movie
    """
    movie_id = str(uuid.uuid4())
    await repo.create(
        movie=Movie(
            movie_id=movie_id,
            title=movie.title,
            description=movie.description,
            release_year=movie.release_year,
            watched=movie.watched,
        )
    )
    return MovieCreatedResponse(id=movie_id)


@router.get(
    "/{movie_id}",
    responses={200: {"model": MovieResponse}, 404: {"model": DetailResponse}},
)
async def get_movie_by_id(
    movie_id: str, repo: MovieRepository = Depends(movie_repository)
):
    """
    Returns a movie if found. None otherwise
    """
    movie = await repo.get_by_id(movie_id=movie_id)
    if movie is None:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                DetailResponse(message=f"Movie: {movie_id} not found")
            ),
        )
    return MovieResponse(
        id=movie_id,
        title=movie.title,
        description=movie.description,
        release_year=movie.release_year,
        watched=movie.watched,
    )


@router.get("/", response_model=typing.List[MovieResponse])
async def get_movies_by_title(
    title: str = Query(
        ..., title="Movie Title", description="Title of the movie.", min_length=3
    ),
    pagination=Depends(pagination_params),
    repo: MovieRepository = Depends(movie_repository),
):
    """
    Returns a list of movies with matching title if found. Empty list otherwise
    """
    movies = await repo.get_by_title(
        title=title, skip=pagination.skip, limit=pagination.limit
    )
    return_value = []
    for movie in movies:
        return_value.append(
            MovieResponse(
                id=movie.id,
                title=movie.title,
                description=movie.description,
                release_year=movie.release_year,
                watched=movie.watched,
            )
        )
    return return_value


@router.patch(
    "/{movie_id}",
    responses={200: {"model": DetailResponse}, 400: {"model": DetailResponse}},
)
async def patch_update_movie(
    movie_id: str = Path(..., title="Movie ID", description="The ID of the Movie"),
    update_parameters: MovieUpdateBody = Body(
        ..., title="Update Body", description="Parameters of the movie to be updated"
    ),
    repo: MovieRepository = Depends(movie_repository),
):
    """
    Updates a movie
    """
    try:
        await repo.update(
            movie_id=movie_id,
            params=update_parameters.dict(exclude_unset=True, exclude_none=True),
        )
        return DetailResponse(message=f"Movie: {movie_id} updated successfully")
    except RepositoryException as e:
        return JSONResponse(
            status_code=400, content=jsonable_encoder(DetailResponse(message=str(e)))
        )


@router.delete("/{movie_id}", status_code=204)
async def delete_movie(
    movie_id: str = Path(..., title="Movie ID", description="The ID of the Movie"),
    repo: MovieRepository = Depends(movie_repository),
):
    await repo.delete(movie_id=movie_id)
    return Response(status_code=204)
