class DuplicateTitleError(Exception):
    def __init__(self, title: str):
        self.title = title
