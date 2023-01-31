import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.memory import MemoryMovieRepository


@pytest.mark.asyncio
async def test_create():
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test",
        title="My Movie",
        description="My Description",
        release_year=1990,
    )
    await repo.create(movie)
    assert await repo.get_by_id("test") is movie


@pytest.mark.parametrize(
    "movies_seed,movie_id,expected_result",
    [
        pytest.param([], "my-id", None, id="empty"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                )
            ],
            "my-id",
            Movie(
                movie_id="my-id",
                title="My Movie",
                description="My Description",
                release_year=1990,
            ),
            id="actual-movie",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(movies_seed, movie_id, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    movie = await repo.get_by_id(movie_id=movie_id)
    assert movie == expected_result


@pytest.mark.parametrize(
    "movies_seed,movie_title,expected_result",
    [
        pytest.param([], "some-title", [], id="empty-results"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                )
            ],
            "some-title",
            [],
            id="empty-results-2",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                )
            ],
            "My Movie",
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                )
            ],
            id="single-result",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="my-id-2",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
            ],
            "My Movie",
            [
                Movie(
                    movie_id="my-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="my-id-2",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
            ],
            id="multiple-results",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(movies_seed, movie_title, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    result = await repo.get_by_title(title=movie_title)
    assert result == expected_result


@pytest.mark.asyncio
async def test_delete():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my-id",
            title="My Movie",
            description="My Description",
            release_year=1990,
        )
    )
    await repo.delete("my-id")
    assert await repo.get_by_id("my-id") is None


@pytest.mark.asyncio
async def test_update():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my-id",
            title="My Movie",
            description="My Description",
            release_year=1990,
        )
    )
    await repo.update(
        movie_id="my-id",
        params={
            "title": "Test Title",
            "description": "Test Description",
            "release_year": 2000,
            "watched": True,
        },
    )
    movie = await repo.get_by_id("my-id")
    assert movie == Movie(
        movie_id="my-id",
        title="Test Title",
        description="Test Description",
        release_year=2000,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_fail():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my-id",
            title="My Movie",
            description="My Description",
            release_year=1990,
        )
    )
    with pytest.raises(RepositoryException):
        await repo.update(movie_id="my-id", params={"id": "fail"})
