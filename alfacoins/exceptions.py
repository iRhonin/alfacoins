class ALFACoinsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ServerException(ALFACoinsException):
    pass


class APIException(ALFACoinsException):
    pass
