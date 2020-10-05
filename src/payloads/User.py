#!/usr/bin/env python3
import json
from errors.PocErrors import StepError

class UserPayloads:
    
    @classmethod
    def new_user(cls, usrName, gender):
        return json.dumps({
            "name": usrName,
            "email": "{}@test-poc.com".format(usrName),
            "gender": gender,
            "status": "Active"
        })




    @classmethod
    def patch_user(cls, attr, attr_value):
        valids = ['name', 'email', 'gender', 'status']
        if attr not in valids:
            raise StepError('user attribute "{}" doesnt exist'.format(attr))
        return json.dumps({
            attr: attr_value
        })