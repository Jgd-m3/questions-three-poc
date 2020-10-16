#!/usr/bin/env python3

class Poc_Asserts:

    @classmethod
    def check_response_contains_values_from_dict(cls, dict_body, response):
        for k in dict_body:
            assert response[k] == dict_body[k], 'error in the response {} != {}'.format(k, dict_body[k])
        
    @classmethod
    def check_list_contains_dict(cls, obj, resp_list):
        assert obj in resp_list, '{} list doesnt not contains {}'.format(resp_list, obj)

    @classmethod
    def check_status_code(cls, expected_status, actual_status):
        assert expected_status == actual_status, 'error in status code: (expected) {} != {} (actual)'.format(expected_status, actual_status)

    
    @classmethod
    def check_objects_are_equals(cls, expected_object, actual_object):
        assert expected_object == actual_object, 'error in objects equals: (expected) {} != {} (actual)'.format(expected_object, actual_object)

    @classmethod
    def check_objects_not_equals(cls, expected_object, actual_object):
        assert expected_object != actual_object, 'error in objects not equals: (expected) {} == {} (actual)'.format(expected_object, actual_object)