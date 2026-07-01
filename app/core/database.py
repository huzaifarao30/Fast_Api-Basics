fake_db = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"},
]


def get_db():
        """Yield the data store. Swap this body for a real DB session later —
    every route that depends on get_db() will not need to change."""
        try:
            yield fake_db
        finally:
            pass
