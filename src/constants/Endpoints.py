#!/usr/bin/env python3
from enum import Enum

class Endpoints(Enum):

    # events
    USERS = "public-api/users"
    USER_BY_ID = "public-api/users/{}"
    POSTS = "public-api/posts"
    POST_BY_ID = "public-api/posts/{}"

    def __str__(self):
        return str(self.value)

    def params(self, *params):
        return str(self.value).format(*params)