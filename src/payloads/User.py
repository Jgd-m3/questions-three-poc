#!/usr/bin/env python3

from errors.PocErrors import StepError

class UserPayloads:

    @classmethod
    def attrs(cls): 
        return ['name', 'email', 'gender', 'status']


    @classmethod
    def new_user(cls, usrName, gender):
        return {
            "name": usrName,
            "email": "{}@test-poc.com".format(usrName),
            "gender": gender,
            "status": "Active"
        }




    @classmethod
    def patch_user(cls, attr, attr_value):
        valids = cls.attrs()
        if attr not in valids:
            raise StepError('user attribute "{}" doesnt exist'.format(attr))
        return json.dumps({
            attr: attr_value
        })