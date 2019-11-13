"""Exceptions that occur when interacting with URA api"""


class ApiError(Exception):
    def __init__(self, message, errors):
        super(ApiError, self).__init__(message)

        self.errors = errors
