class ServerException(Exception):
    pass


class APIException(Exception):

    def __init__(self, message):
        super().__init__(message)
