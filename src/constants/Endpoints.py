#!/usr/bin/env python3
from enum import Enum


class Endpoints(Enum):

    """class to allocate all the enpoints used in the suites"""

    # Users endpoints
    USERS = "public-api/users"
    USER_BY_ID = "public-api/users/{}"

    def __str__(self):
        return str(self.value)

    def params(self, *params):
        return str(self.value).format(*params)
