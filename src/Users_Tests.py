#!/usr/bin/env python3
from questions_three.scaffolds.xunit import TestSuite
from dotenv import load_dotenv
from payloads.User import UserPayloads
from steps.Users import Users
from assertions.Asserts import Poc_Asserts
import os


class Users_Tests(TestSuite):

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
        self.usr_id = None

    def teardown(self):    
        # AFTER TEST
        if self.usr_id is not None:
            resp = self.user.delete_user(self.usr_id)
            if resp.json()['code'] == 204:
                print('✓ deleted user -> {}'.format(self.usr_id))
            else:
                print('✗ impossible to delete user -> {}'.format(self.usr_id))


    # creation -----------------------------------------------------------------
    def test_create_user_successfully(self):
        body = UserPayloads.new_user('MyBestUser', 'Male')
        resp = self.user.create_user(body)
        Poc_Asserts.check_status_code(200, resp.status_code)
        resp_body = resp.json()
        Poc_Asserts.check_response_contains_values_from_dict(body, resp_body['data'])
        self.usr_id = resp_body['data']['id']
        print('✓ user created -> {}'.format(self.usr_id))
        resp = self.user.get_user_by_id(self.usr_id)
        Poc_Asserts.check_status_code(200, resp.status_code)
        resp_body = resp.json()
        Poc_Asserts.check_response_contains_values_from_dict(body, resp_body['data'])
        print('✓ got user -> {}'.format(self.usr_id))


    def test_create_user_without_authorization(self):
        body = UserPayloads.new_user('MyWorstUser', 'Male')
        resp = self.user.create_user_without_auth(body)
        Poc_Asserts.check_status_code(200, resp.status_code) #bad design of the api
        resp_body = resp.json()
        Poc_Asserts.check_status_code(401, resp_body['code']) #checking the supposed real code
        Poc_Asserts.check_response_contains_values_from_dict({'message': 'Authentication failed'}, resp_body['data'])
        print('✓ user not created properly [Unauthorized]')


    def test_create_user_without_required_params(self):
        params = UserPayloads.attrs()
        # one by one
        for elem in params:
            self.checking_new_user_removing_X_param(elem)
        # all in one shoot
        empty_payload = {}
        body = self.user.create_user(empty_payload).json()
        Poc_Asserts.check_status_code(422, body['code']) #checking the supposed real code
        for elem in params:
            Poc_Asserts.check_list_contains_dict({'field': elem, 'message': "can't be blank"}, body['data'])
        print('✓ all params checked [Unprocessable Entity]')


    def test_create_user_without_required_enum(self):
        dic = {
            'status': 'can be Active or Inactive',
            'gender': 'can be Male or Female'
            }
        for field, err_msg in dic.items():
            payload = UserPayloads.new_user('Invalid', 'Male')
            payload[field] = 'invalidValue'
            body = self.user.create_user(payload).json()
            Poc_Asserts.check_status_code(422, body['code']) #checking the supposed real code
            Poc_Asserts.check_list_contains_dict({'field': field, 'message': err_msg}, body['data'])
            print('✓ user not created with invalid {} [Unprocessable Entity]'.format(field))
            

    def test_create_user_with_existing_email(self):
        body = UserPayloads.new_user('MyRepeatedUser', 'Male')
        resp = self.user.create_user(body).json()
        Poc_Asserts.check_status_code(201, resp['code'])
        self.usr_id = resp['data']['id']
        print('✓ user created once -> {}'.format(self.usr_id))
        # repeating the request
        resp = self.user.create_user(body).json()
        Poc_Asserts.check_status_code(422, resp['code']) #checking the supposed real code
        Poc_Asserts.check_list_contains_dict({'field': 'email', 'message': "has already been taken"}, resp['data'])
        print('✓ user not created with same email `{}` [Unprocessable Entity]'.format(body['email']))


    # update -----------------------------------------------------------------
    def test_update_user_successfully(self):
        body = UserPayloads.new_user('futureUpdated', 'Female')
        resp = self.user.create_user(body)
        Poc_Asserts.check_status_code(200, resp.status_code)
        self.usr_id = resp.json()['data']['id']
        print('✓ user created -> {}'.format(self.usr_id))
        new_body = UserPayloads.new_user('Updated', 'Male')
        resp = self.user.update_user(new_body, self.usr_id)
        Poc_Asserts.check_status_code(200, resp.status_code)
        resp_body = resp.json()
        Poc_Asserts.check_response_contains_values_from_dict(new_body, resp_body['data'])
        print('✓ user updated -> {}'.format(self.usr_id))
        resp = self.user.get_user_by_id(self.usr_id)
        Poc_Asserts.check_status_code(200, resp.status_code)
        resp_body = resp.json()
        Poc_Asserts.check_response_contains_values_from_dict(new_body, resp_body['data'])
        print('✓ got updated user -> {}'.format(self.usr_id))


    def test_update_user_without_authorization(self):
        body = UserPayloads.new_user('futureNotUpdated', 'Male')
        resp = self.user.create_user(body)
        Poc_Asserts.check_status_code(200, resp.status_code)
        self.usr_id = resp.json()['data']['id']
        print('✓ user created -> {}'.format(self.usr_id))
        new_body = UserPayloads.new_user('Updated', 'Female')
        resp = self.user.update_user_without_auth(new_body, self.usr_id)
        Poc_Asserts.check_status_code(200, resp.status_code) #bad design of the fake api
        resp_body = resp.json()
        Poc_Asserts.check_status_code(401, resp_body['code']) #checking the supposed real code
        Poc_Asserts.check_response_contains_values_from_dict({'message': 'Authentication failed'}, resp_body['data'])
        print('✓ user {} not updated properly [Unauthorized]'.format(self.usr_id))

    def test_update_user_not_found_error(self):
        no_existing_id = 9999999999999999999
        useless_payload = {}
        resp_body = self.user.update_user(useless_payload, no_existing_id).json()
        Poc_Asserts.check_status_code(404, resp_body['code']) #checking the supposed real code
        Poc_Asserts.check_response_contains_values_from_dict({'message': 'Resource not found'}, resp_body['data'])
        print('✓ user `{}` not updated [Not Found]'.format(no_existing_id))

    # TO INCLUDE: data validation in updates as well
    #       test_update_user_with_existing_email():
    #       test_update_user_without_required_enum():
    #       test_update_user_without_required_params():
    #
    #       (not included to avoid repetitions in a PoC for a fake api)


    # deletion -----------------------------------------------------------------
    def test_delete_user_without_authorization(self):
        body = UserPayloads.new_user('delNotAuth', 'Male')
        resp_body = self.user.create_user(body).json()
        Poc_Asserts.check_status_code(201, resp_body['code'])
        self.usr_id = resp_body['data']['id']
        print('✓ user created -> {}'.format(self.usr_id))
        resp_body = self.user.delete_user_without_auth(self.usr_id).json()
        Poc_Asserts.check_status_code(401, resp_body['code']) #checking the supposed real code
        Poc_Asserts.check_response_contains_values_from_dict({'message': 'Authentication failed'}, resp_body['data'])
        print('✓ user {} not deleted [Unauthorized]'.format(self.usr_id))


    def test_delete_user_not_found_error(self):
        no_existing_id = 9999999999999999999
        resp_body = self.user.delete_user(no_existing_id).json()
        Poc_Asserts.check_status_code(404, resp_body['code']) #checking the supposed real code
        Poc_Asserts.check_response_contains_values_from_dict({'message': 'Resource not found'}, resp_body['data'])
        print('✓ user `{}` not deleted [Not Found]'.format(no_existing_id))


    # get user by id -----------------------------------------------------------------
    def test_get_user_by_id_not_found_error(self): 
        no_existing_id = 9999999999999999999
        resp_body = self.user.get_user_by_id(no_existing_id).json()
        Poc_Asserts.check_status_code(404, resp_body['code']) #checking the supposed real code
        Poc_Asserts.check_response_contains_values_from_dict({'message': 'Resource not found'}, resp_body['data'])
        print('✓ impossible get user `{}` [Not Found]'.format(no_existing_id))
    
    

    # get users -----------------------------------------------------------------
    def test_pagination_get_users(self):
        filters = {'page': 1}
        resp_body_pag1 = self.user.get_users_with_filters(filters).json()
        filters = {'page': 2}
        resp_body_pag2 = self.user.get_users_with_filters(filters).json()
        # checking meta
        Poc_Asserts.check_objects_are_equals(1, resp_body_pag1['meta']['pagination']['page'])
        Poc_Asserts.check_objects_are_equals(2, resp_body_pag2['meta']['pagination']['page'])
        # checking first item not iqual
        first_item_1 = resp_body_pag1['data'][0]
        first_item_2 = resp_body_pag2['data'][0]
        Poc_Asserts.check_objects_not_equals(first_item_1, first_item_2)
        print('✓ pagination checked -> userID `{}` != userID `{}`'.format(first_item_1['id'], first_item_2['id']))


    def test_search_user_with_filters(self):
        body = UserPayloads.new_user('MyFilteredUser', 'Male')
        resp = self.user.create_user(body).json()
        Poc_Asserts.check_status_code(201, resp['code'])
        self.usr_id = resp['data']['id']
        body = resp['data']
        print('✓ user created -> {}'.format(self.usr_id))
        for filter_field in ['name', 'email']:
            filters = {filter_field: body[filter_field]}
            resp_body = self.user.get_users_with_filters(filters).json()
            Poc_Asserts.check_list_contains_dict(body, resp_body['data'])
            print('✓ got user {} filtering by {} -> {}'.format(self.usr_id, filter_field, body[filter_field]))


    # other methods -----------------------------------------------------------------
    def checking_new_user_removing_X_param(self, param_name):
        originalBody = UserPayloads.new_user('withoutParam', 'Female')
        originalBody.pop(param_name)
        body = self.user.create_user(originalBody).json()
        Poc_Asserts.check_status_code(422, body['code']) #checking the supposed real code
        Poc_Asserts.check_list_contains_dict({'field': param_name, 'message': "can't be blank"}, body['data'])
        print('✓ user not created without {} [Unprocessable Entity]'.format(param_name))

