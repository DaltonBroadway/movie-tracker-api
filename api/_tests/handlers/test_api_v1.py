import functools

import pytest

# noinspection PyUnresolvedReferences
from api._tests.fixture import test_client
from api.entities.movie import Movie
from api.handlers.movie_v1 import movie_repository
from api.repository.movie.memory import MemoryMovieRepository


def memory_repository_dependency(dependency):
    return dependency


@pytest.mark.asyncio
async def test_create_movie(test_client):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    result = test_client.post(
        "/api/v1/movies",
        json={
            "title": "My Movie",
            "description": "Test",
            "release_year": 2000,
            "watched": False,
        },
    )
    movie_id = result.json().get("id")
    assert result.status_code == 201
    movie = await repo.get_by_id(movie_id=movie_id)
    assert movie is not None


@pytest.mark.parametrize(
    "movie_json",
    [
        pytest.param(
            {
                "description": "Test",
                "release_year": 2000,
                "watched": False,
            }
        ),
        pytest.param(
            {
                "title": "My Movie",
                "release_year": 2000,
                "watched": False,
            }
        ),
        pytest.param(
            {
                "title": "My",
                "description": "Test",
                "release_year": 2000,
                "watched": False,
            }
        ),
        pytest.param(
            {
                "title": "My Movie",
                "description": "Test",
                "release_year": 0,
                "watched": False,
            }
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_movie_validation_error(test_client, movie_json):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    result = test_client.post(
        "/api/v1/movies",
        json=movie_json,
    )
    assert result.status_code == 422


@pytest.mark.parametrize(
    "movie_seed,movie_id,expected_status_code,expected_result",
    [
        pytest.param(
            [], "test-id", 404, {"message": "Movie: test-id not found"}, id="none-found"
        ),
        pytest.param(
            [
                Movie(
                    movie_id="test-id",
                    title="My Movie",
                    description="My Description",
                    release_year=1990,
                )
            ],
            "test-id",
            200,
            {
                "id": "test-id",
                "title": "My Movie",
                "description": "My Description",
                "release_year": 1990,
                "watched": False,
            },
            id="found",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_movie_by_id(
    test_client, movie_seed, movie_id, expected_status_code, expected_result
):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    for movie in movie_seed:
        await repo.create(movie)
    result = test_client.get(f"/api/v1/movies/{movie_id}")
    assert result.status_code == expected_status_code
    assert result.json() == expected_result


@pytest.mark.parametrize(
    "movie_seed,title,skip,limit,expected_status_code,expected_result",
    [
        pytest.param([], "Test Title", 0, 1000, 200, [], id="empty"),
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
            0,
            1000,
            200,
            [
                {
                    "id": "test-id",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                }
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
            0,
            1000,
            200,
            [
                {
                    "id": "test-id-1",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
                {
                    "id": "test-id-2",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
                {
                    "id": "test-id-3",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
            ],
            id="found-many",
        ),
        pytest.param(
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
            "My Movie",
            2,
            1000,
            200,
            [
                {
                    "id": "my-id-3",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
                {
                    "id": "my-id-4",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
                {
                    "id": "my-id-5",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
            ],
            id="skip",
        ),
        pytest.param(
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
            "My Movie",
            0,
            3,
            200,
            [
                {
                    "id": "my-id-1",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
                {
                    "id": "my-id-2",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
                {
                    "id": "my-id-3",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
            ],
            id="limit",
        ),
        pytest.param(
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
            "My Movie",
            1,
            3,
            200,
            [
                {
                    "id": "my-id-2",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
                {
                    "id": "my-id-3",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
                {
                    "id": "my-id-4",
                    "title": "My Movie",
                    "description": "My Description",
                    "release_year": 1990,
                    "watched": False,
                },
            ],
            id="skip-and-limit",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_movies_by_title(
    test_client, movie_seed, title, skip, limit, expected_status_code, expected_result
):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    for movie in movie_seed:
        await repo.create(movie)
    result = test_client.get(f"/api/v1/movies/?title={title}&skip={skip}&limit={limit}")
    assert result.status_code == expected_status_code
    assert result.json() == expected_result


@pytest.mark.parametrize(
    "update_params,updated_movie",
    [
        pytest.param(
            {"title": "Test Movie"},
            Movie(
                movie_id="test-id",
                title="Test Movie",
                description="My Description",
                release_year=1990,
            ),
            id="update-title",
        ),
        pytest.param(
            {"description": "Test Description"},
            Movie(
                movie_id="test-id",
                title="My Movie",
                description="Test Description",
                release_year=1990,
            ),
            id="update-description",
        ),
        pytest.param(
            {"release_year": 2000},
            Movie(
                movie_id="test-id",
                title="My Movie",
                description="My Description",
                release_year=2000,
            ),
            id="update-release_year",
        ),
        pytest.param(
            {"watched": True},
            Movie(
                movie_id="test-id",
                title="My Movie",
                description="My Description",
                release_year=1990,
                watched=True,
            ),
            id="update-watched",
        ),
        pytest.param(
            {
                "title": "Test Movie",
                "description": "Test Description",
                "release_year": 2000,
                "watched": True,
            },
            Movie(
                movie_id="test-id",
                title="Test Movie",
                description="Test Description",
                release_year=2000,
                watched=True,
            ),
            id="update-multiple",
        ),
    ],
)
@pytest.mark.asyncio
async def test_patch_update_movie(test_client, update_params, updated_movie):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    movie_id = "test-id"
    await repo.create(
        Movie(
            movie_id=movie_id,
            title="My Movie",
            description="My Description",
            release_year=1990,
        )
    )
    result = test_client.patch(f"/api/v1/movies/{movie_id}", json=update_params)
    assert result.status_code == 200
    assert result.json() == {"message": f"Movie: {movie_id} updated successfully"}
    if updated_movie is not None:
        assert await repo.get_by_id(movie_id=movie_id) == updated_movie


@pytest.mark.asyncio
async def test_patch_update_movie(test_client):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    movie_id = "test-id"
    result = test_client.patch(
        f"/api/v1/movies/{movie_id}", json={"title": "test title"}
    )
    assert result.status_code == 400
    assert result.json() == {"message": f"Movie: {movie_id} not found"}


@pytest.mark.asyncio
async def test_delete_movie(test_client):
    repo = MemoryMovieRepository()
    patched_dependency = functools.partial(memory_repository_dependency, repo)
    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    movie_id = "test-id"
    await repo.create(
        Movie(
            movie_id=movie_id,
            title="My Movie",
            description="My Description",
            release_year=1990,
        )
    )
    result = test_client.delete(f"/api/v1/movies/{movie_id}")
    assert result.status_code == 204
    assert await repo.get_by_id(movie_id=movie_id) is None
