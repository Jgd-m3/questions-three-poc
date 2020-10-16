#!/usr/bin/env python3

from errors.PocErrors import StepError

class UserPayloads:
    """class to allocate the different body builders in order to send them as a payload"""

    @classmethod
    def attrs(cls): 
        return ['name', 'email', 'gender', 'status']


    @classmethod
    def new_user(cls, usrName, gender):
        """method to return a new user payload"""

        return {
            "name": usrName,
            "email": "{}@test-poc.com".format(usrName),
            "gender": gender,
            "status": "Active"
        }
