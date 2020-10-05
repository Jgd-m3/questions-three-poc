#!/usr/bin/env python3
from questions_three.scaffolds.xunit import TestSuite
from dotenv import load_dotenv
from payloads.User import UserPayloads
from steps.Users import Users
import os



class GoRest_Tests(TestSuite):
    
    def setup_suite(self):
        # BEFORE SUITE
        load_dotenv()
        self.uri = os.getenv('gorest_uri')
        self.token = os.getenv('token')

    def teardown_suite(self):
        # AFTER SUITE
        pass

    def setup(self):
        # BEFORE TEST
        self.user = Users(self.uri, self.token)


    def teardown(self):
        # AFTER TEST
        pass

    def test_check_users(self):
        body = UserPayloads.new_user('juano1', 'Male')
        resp = self.user.create_user(body)
        self.user.delete_user(resp['id'])

