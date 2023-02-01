class Movie:
    def __init__(
        self,
        *,
        movie_id: str,
        title: str,
        description: str,
        release_year: int,
        watched: bool = False,
    ):
        if movie_id is None:
            raise ValueError("Movie ID is required")
        self._id = movie_id
        self._title = title
        self._description = description
        self._release_year = release_year
        self._watched = watched

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def release_year(self) -> int:
        return self._release_year

    @property
    def watched(self) -> bool:
        return self._watched

    def __str__(self):
        return f"{self.id}: {self.title} ({self.release_year}). {self.description}. Watched:{self.watched}"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Movie):
            return False
        return (
            self.id == o.id
            and self.title == o.title
            and self.description == o.description
            and self.release_year == o.release_year
            and self.watched == o.watched
        )
