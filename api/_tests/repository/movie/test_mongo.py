import pytest

# noinspection PyUnresolvedReferences
from api._tests.fixture import mongo_movie_repo_fixture
from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException


@pytest.mark.asyncio
async def test_create(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            movie_id="test",
            title="My Movie",
            description="My Description",
            release_year=1990,
            watched=True,
        )
    )
    movie: Movie = await mongo_movie_repo_fixture.get_by_id("test")
    assert movie == Movie(
        movie_id="test",
        title="My Movie",
        description="My Description",
        release_year=1990,
        watched=True,
    )
    await mongo_movie_repo_fixture.delete("test")


@pytest.mark.parametrize(
    "initial_movies,movie_id,expected_result",
    [
        pytest.param([], "test-id", None, id="empty"),
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
            id="found",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(
    mongo_movie_repo_fixture, initial_movies, movie_id, expected_result
):
    for movie in initial_movies:
        await mongo_movie_repo_fixture.create(movie)
    movie: Movie = await mongo_movie_repo_fixture.get_by_id(movie_id)
    assert movie == expected_result


@pytest.mark.parametrize(
    "initial_movies,title,expected_result",
    [
        pytest.param([], "test-id", [], id="empty"),
        pytest.param(
            [
                Movie(
                    movie_id="test-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="test-id-0",
                    title="Other Movie",
                    description="My Description",
                    release_year=1990,
                ),
            ],
            "My Movie",
            [
                Movie(
                    movie_id="test-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                )
            ],
            id="found-one",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="test-id-1",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="test-id-2",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="test-id-3",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="test-id-0",
                    title="Other Movie",
                    description="My Description",
                    release_year=1990,
                ),
            ],
            "My Movie",
            [
                Movie(
                    movie_id="test-id-1",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="test-id-2",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="test-id-3",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
            ],
            id="found-many",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(
    mongo_movie_repo_fixture, initial_movies, title, expected_result
):
    for movie in initial_movies:
        await mongo_movie_repo_fixture.create(movie)
    movie: Movie = await mongo_movie_repo_fixture.get_by_title(title)
    assert movie == expected_result


@pytest.mark.parametrize(
    "title,skip,limit,expected_result",
    [
        pytest.param(
            "My Movie",
            2,
            1000,
            [
                Movie(
                    movie_id="my-id-3",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="my-id-4",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="my-id-5",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
            ],
            id="skip",
        ),
        pytest.param(
            "My Movie",
            0,
            3,
            [
                Movie(
                    movie_id="my-id-1",
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
                Movie(
                    movie_id="my-id-3",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
            ],
            id="limit",
        ),
        pytest.param(
            "My Movie",
            2,
            2,
            [
                Movie(
                    movie_id="my-id-3",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
                Movie(
                    movie_id="my-id-4",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                ),
            ],
            id="skip-and-limit",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title_pagination(
    mongo_movie_repo_fixture, title, skip, limit, expected_result
):
    initial_movies = [
        Movie(
            movie_id="my-id-1",
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
        Movie(
            movie_id="my-id-3",
            title="My Movie",
            description="My Description",
            release_year=1990,
        ),
        Movie(
            movie_id="my-id-4",
            title="My Movie",
            description="My Description",
            release_year=1990,
        ),
        Movie(
            movie_id="my-id-5",
            title="My Movie",
            description="My Description",
            release_year=1990,
        ),
    ]
    for movie in initial_movies:
        await mongo_movie_repo_fixture.create(movie)
    movie: Movie = await mongo_movie_repo_fixture.get_by_title(
        title=title, skip=skip, limit=limit
    )
    assert movie == expected_result


@pytest.mark.asyncio
async def test_delete(mongo_movie_repo_fixture):
    initial_movie = Movie(
        movie_id="test",
        title="My Movie",
        description="My Description",
        release_year=1990,
    )
    await mongo_movie_repo_fixture.create(initial_movie)
    await mongo_movie_repo_fixture.delete(movie_id="test")
    assert await mongo_movie_repo_fixture.get_by_id(movie_id="test") is None


@pytest.mark.asyncio
async def test_update(mongo_movie_repo_fixture):
    initial_movie = Movie(
        movie_id="test",
        title="My Movie",
        description="My Description",
        release_year=1990,
    )
    await mongo_movie_repo_fixture.create(initial_movie)
    await mongo_movie_repo_fixture.update(
        movie_id="test",
        params={
            "title": "Test Title",
            "description": "Test Description",
            "release_year": 2000,
            "watched": True,
        },
    )
    movie: Movie = await mongo_movie_repo_fixture.get_by_id("test")
    assert movie == Movie(
        movie_id="test",
        title="Test Title",
        description="Test Description",
        release_year=2000,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_fail(mongo_movie_repo_fixture):
    initial_movie = Movie(
        movie_id="test",
        title="My Movie",
        description="My Description",
        release_year=1990,
    )
    await mongo_movie_repo_fixture.create(initial_movie)
    with pytest.raises(RepositoryException):
        await mongo_movie_repo_fixture.update(movie_id="my-id", params={"id": "fail"})
