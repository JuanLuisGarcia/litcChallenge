class RelatedObjectNotFound(Exception):
    def __init__(self, exc, object_value):
        self.description = f'Related Object {object_value} not found'
        self.code = exc.code
        super().__init__()


class UnknowError(Exception):
    def __init__(self, exc):
        self.description = 'Unknown Error'
        self.code = 500
        super().__init__()


class TypeError(Exception):
    def __init__(self, exc):
        self.description = exc
        self.code = exc
        super().__init__()

