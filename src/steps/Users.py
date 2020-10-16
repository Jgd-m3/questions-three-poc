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
    
    def create_user(self, usr_body_dic):
        uri = '{}{}'.format(self.url, EP.USERS)
        headrs = {'authorization': 'Bearer {}'.format(self.token), "Content-Type": "application/json"}
        return HttpClient().post(uri, data=json.dumps(usr_body_dic), headers=headrs)
    
    def create_user_without_auth(self, usr_body_dic):
        uri = '{}{}'.format(self.url, EP.USERS)
        headrs = {"Content-Type": "application/json"}
        return HttpClient().post(uri, data=json.dumps(usr_body_dic), headers=headrs)

    def update_user(self, usr_body_dic, usr_id):
        uri = '{}{}'.format(self.url, EP.USER_BY_ID.params(usr_id))
        headrs = {'authorization': 'Bearer {}'.format(self.token), "Content-Type": "application/json"}
        return HttpClient().put(uri, data=json.dumps(usr_body_dic), headers=headrs)

    def update_user_without_auth(self, usr_body_dic, usr_id):
        uri = '{}{}'.format(self.url, EP.USER_BY_ID.params(usr_id))
        headrs = {"Content-Type": "application/json"}
        return HttpClient().put(uri, data=json.dumps(usr_body_dic), headers=headrs)


    def get_user_by_id(self, usr_id):
        uri = '{}{}'.format(self.url, EP.USER_BY_ID.params(usr_id))
        return HttpClient().get(uri)


    def get_users_with_filters(self, filters):
        uri = '{}{}'.format(self.url, EP.USERS)
        return HttpClient().get(uri, params=filters)


    def delete_user(self, usr_id):
        uri = '{}{}'.format(self.url, EP.USER_BY_ID.params(usr_id))
        return HttpClient().delete(uri, headers = {'authorization': 'Bearer {}'.format(self.token)})


    def delete_user_without_auth(self, usr_id):
        uri = '{}{}'.format(self.url, EP.USER_BY_ID.params(usr_id))
        return HttpClient().delete(uri)
