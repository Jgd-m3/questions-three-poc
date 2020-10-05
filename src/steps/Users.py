#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone
from constants.Endpoints import Endpoints as EP
from questions_three.http_client import HttpClient
from errors.PocErrors import StepError

import json


class Users:

    def __init__(self, uri, auth_token):
        super().__init__()
        self.url = uri
        self.token = auth_token
    
    def create_user(self, usr_body):
        uri = '{}{}'.format(self.url, EP.USERS)
        r = HttpClient().post(uri, data=usr_body, headers={'authorization': 'Bearer {}'.format(self.token), "Content-Type": "application/json"})
        if r.status_code != 200:
            #add logs here
            raise StepError('user couldnt be created')
        resp_body = r.json()['data']
        print('usr created -> {}'.format(resp_body['id']))
        return resp_body

    def delete_user(self, usr_id):
        uri = '{}{}'.format(self.url, EP.USER_BY_ID.params(usr_id))
        r = HttpClient().delete(uri, headers = {'authorization': 'Bearer {}'.format(self.token)})
        if r.status_code == 200:
            print('user deleted -> {}'.format(usr_id))
        else:
            #add logs here
            raise StepError('user couldnt be deleted', r)