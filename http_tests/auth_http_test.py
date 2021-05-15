#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 15:16:16 2021

@author: z5257847
"""
import pytest
import requests
from src import config

#Creating global variables for Input and Access errirs
INPUT_ERROR = 400
ACCESS_ERROR = 403

#Fixture to register 3 users to prevent repeating code
@pytest.fixture
def register_three_users():
    url = config.url
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'milch@gmail.com', 'password' : 'random',})
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan@gmail.com', 'password' : 'random',})

#Testing multiple invalid emails to determine if auth_register_v1 is correctly identifying this error
def test_invalid_email_register():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milchgmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail', 'password' : 'random',})
    assert user1.status_code == INPUT_ERROR 
    assert user2.status_code == INPUT_ERROR 
    requests.delete(f"{url}clear/v1")

#Testing passwords less than 6 characters long to determine if auth_register_v1 is correctly identifying this error
def test_short_password():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'hi',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan@gmail.com', 'password' : 'a',})
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'milch@gmail.com', 'password' : '',})

    assert user1.status_code == INPUT_ERROR 
    assert user2.status_code == INPUT_ERROR 
    assert user3.status_code == INPUT_ERROR 
    requests.delete(f"{url}clear/v1")


#Testing first names less than 1 character and more than 50 characters long to determine if auth_register_v2 is correctly identifying this error
def test_invalid_first_name():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : '', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    assert user1.status_code == INPUT_ERROR 
    assert user2.status_code == INPUT_ERROR 
    requests.delete(f"{url}clear/v1")
    
#Testing last names less than 1 character and more than 50 characters long to determine if auth_register_v2 is correctly identifying this error
def test_invalid_last_name():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_last' : '', 'name_first' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_last' : 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'name_first' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    assert user1.status_code == INPUT_ERROR 
    assert user2.status_code == INPUT_ERROR 
    requests.delete(f"{url}clear/v1")

#Registering one user and determing if the output is as expected
def test_simple_register():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    result = user1.json()
    assert type(result) == dict
    assert len(result) == 2
    assert type(result['token']) == str
    assert type(result['auth_user_id']) == int
    requests.delete(f"{url}clear/v1")

#Registering multiple users and checking that the output from each is correct and the u_id/token returned is unique to each user
def test_multiple_register():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'secondemail@gmail.com', 'password' : 'random',})
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'thirdemail@gmail.com', 'password' : 'random',})


    result1 = user1.json()
    result2 = user2.json()
    result3 = user3.json()

    assert type(result1) == dict
    assert len(result1) == 2
    assert type(result1['token']) == str
    assert type(result1['auth_user_id']) == int
    assert type(result2) == dict
    assert len(result2) == 2
    assert type(result2['token']) == str
    assert type(result2['auth_user_id']) == int
    assert type(result3) == dict
    assert len(result3) == 2
    assert type(result3['token']) == str
    assert type(result3['auth_user_id']) == int    
    assert result1['token'] != result2['token']
    assert result1['token'] != result3['token']
    assert result3['token'] != result2['token']
    assert result1['auth_user_id'] != result2['auth_user_id']
    assert result1['auth_user_id'] != result3['auth_user_id']
    assert result3['auth_user_id'] != result2['auth_user_id']
    requests.delete(f"{url}clear/v1")

#Testing for multiple users, whilst an error is raised, to ensure the code continues to function as expected
def test_multiple_register_with_error(register_three_users):
    url = config.url
    
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'fourthemail@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'fourthemailgmail.com', 'password' : 'random',})
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'fifthemail@gmail.com', 'password' : 'random',})
    
    user1 = user1.json()
    user3 = user3.json()

    assert user2.status_code == INPUT_ERROR 
    assert user1 != user3
    assert user1['auth_user_id'] != user3['auth_user_id']
    assert user1['token'] != user3['token']
    requests.delete(f"{url}clear/v1")

#Testing auth_register to check that an error is raised when an already registered email is used again
def test_email_in_use_register(register_three_users):
    url = config.url
    
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'milch@gmail.com', 'password' : 'random',})
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan@gmail.com', 'password' : 'random',})

    assert user1.status_code == INPUT_ERROR 
    assert user2.status_code == INPUT_ERROR 
    assert user3.status_code == INPUT_ERROR 
    requests.delete(f"{url}clear/v1")

#Registering a valid user and then checking that auth_login_v2 correctly identifies an invalid email and raises an InputError
def test_invalid_email_login():
    url = config.url
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    login1 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'jordanmilch.com', 'password' : 'random',})
    login2 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'jordan.milch@gmail', 'password' : 'random',})

    assert login1.status_code == INPUT_ERROR
    assert login2.status_code == INPUT_ERROR
    requests.delete(f"{url}clear/v1")

#Using the aforementioned fixture and checking that auth_login raises an error when an un-registered email is used to try log in
def test_email_doesnt_belong(register_three_users):
    url = config.url
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    login1 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'jordan@milch.com', 'password' : 'random',})
    login2 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'jordan@gmail.com', 'password' : 'random',})

    assert login1.status_code == INPUT_ERROR
    assert login2.status_code == INPUT_ERROR
    requests.delete(f"{url}clear/v1")

#Testing that auth_login_v1 raises an error when a registered email but incorrect password is used
def test_password_doesnt_match(register_three_users):
    url = config.url
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    login1 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'jordan.milch@gmail.com', 'password' : 'hello123',})
    login2 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'jordan.milch@gmail.com', 'password' : 'randompassword',})

    assert login1.status_code == INPUT_ERROR
    assert login2.status_code == INPUT_ERROR
    requests.delete(f"{url}clear/v1")

#Trying to log in without there being any registered users
def test_empty_login():
    url = config.url
    requests.delete(f"{url}clear/v1")
    login1 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'jordan.milch@gmail.com', 'password' : 'hello123',})
    assert login1.status_code == INPUT_ERROR

#Testing basic login functionality to ensure that the output is identical to that of auth_register_v2
def test_login_basic():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    login1 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    result1 = user1.json()
    result2 = login1.json()

    assert result1 != result2
    assert type(result1) == dict
    assert type(result1['auth_user_id']) == int
    assert type(result2) == dict
    assert type(result2['auth_user_id']) == int
    assert result1['auth_user_id'] == result2['auth_user_id']
    assert result1['token'] != result2['token']
    requests.delete(f"{url}clear/v1")

#Testing multiple log-in to ensure functionality remains as expected and no errors are raised
def test_login_multiple():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'secondemail@gmail.com', 'password' : 'random',})
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'thirdemail@gmail.com', 'password' : 'random',})

    login1 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'validemail@gmail.com', 'password' : 'random',})
    login2 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'secondemail@gmail.com', 'password' : 'random',})
    login3 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'thirdemail@gmail.com', 'password' : 'random',})

    result1 = user1.json()
    result2 = user2.json()
    result3 = user3.json()

    result1a = login1.json()
    result2a = login2.json()
    result3a = login3.json()

    assert result1 != result1a
    assert result2 != result2a
    assert result3 != result3a
    assert result1 != result2
    assert result2 != result3
    assert result1a != result2a
    assert result3a != result2a
    assert result1['auth_user_id'] == result1a['auth_user_id']
    assert result2['auth_user_id'] == result2a['auth_user_id']
    assert result2['auth_user_id'] == result2a['auth_user_id']
    assert result1['token'] != result1a['token']
    assert result2['token'] != result2a['token']
    assert result2['token'] != result2a['token']
    requests.delete(f"{url}clear/v1")

#Testing auth_logout functions correctly when a single user is registered
def test_logout_basic():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()    
    result2 = requests.post(f"{url}auth/logout/v1", json = { 'token' : user1['token']})
    assert result2.json() == {'is_success' : True,}
    requests.delete(f"{url}clear/v1")

#Testing auth_logout returns an error when no users are registered
def test_logout_empty():
    url = config.url
    requests.delete(f"{url}clear/v1")
    result2 = requests.post(f"{url}auth/logout/v1", json = { 'token' : ''})
    assert result2.status_code == ACCESS_ERROR
    requests.delete(f"{url}clear/v1")

#Testing a logged out user can then be logged in
def test_logout_login():
    url = config.url
    requests.delete(f"{url}clear/v1")    
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    requests.post(f"{url}auth/logout/v1", json = { 'token' : user1['token']})
    login1 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'validemail@gmail.com', 'password' : 'random',})
    login1 = login1.json()

    assert login1 != user1
    assert type(login1) == dict
    assert type(login1['auth_user_id']) == int
    assert type(login1['token']) == str
    assert type(user1) == dict
    assert type(user1['auth_user_id']) == int
    assert type(user1['token']) == str
    assert user1['auth_user_id'] == login1['auth_user_id']
    assert user1['token'] != login1['token']
    requests.delete(f"{url}clear/v1")    
#Test logout raises an error when an invalid token is passed in
def test_invalid_logout_token():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()    
    result1 = requests.post(f"{url}auth/logout/v1", json = { 'token' : user1['token']})
    result2 = requests.post(f"{url}auth/logout/v1", json = { 'token' : user1['token']})
    assert result2.status_code == ACCESS_ERROR
    assert result1.json() == {'is_success' : True,}
    requests.delete(f"{url}clear/v1")

#Testing logout functions correctly when multiple users are registered
def test_multiple_logout():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'secondemail@gmail.com', 'password' : 'random',})
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'thirddemail@gmail.com', 'password' : 'random',})
  
    user1 = user1.json()
    user2 = user2.json()
    user3 = user3.json()

    result1a = requests.post(f"{url}auth/logout/v1", json = { 'token' : user1['token']})
    result2a = requests.post(f"{url}auth/logout/v1", json = { 'token' : user2['token']})
    result3a = requests.post(f"{url}auth/logout/v1", json = { 'token' : user3['token']})

    assert result1a.json() == {'is_success' : True,}
    assert result2a.json() == {'is_success' : True,}
    assert result3a.json() == {'is_success' : True,}
    requests.delete(f"{url}clear/v1")

#Testing that auth_logout functions correctly with errors in between functionality
def test_multiple_logout_with_error():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'secondemail@gmail.com', 'password' : 'random',})
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'thirddemail@gmail.com', 'password' : 'random',})
  
    user1 = user1.json()
    user2 = user2.json()
    user3 = user3.json()
    
    result1a = requests.post(f"{url}auth/logout/v1", json = { 'token' : user1['token']})
    result1b = requests.post(f"{url}auth/logout/v1", json = { 'token' : user1['token']})
    result2a = requests.post(f"{url}auth/logout/v1", json = { 'token' : user2['token']})
    result3a = requests.post(f"{url}auth/logout/v1", json = { 'token' : user3['token']})

    assert result1a.json() == {'is_success' : True,}
    assert result1b.status_code == ACCESS_ERROR
    assert result2a.json() == {'is_success' : True,}
    assert result3a.json() == {'is_success' : True,}
    requests.delete(f"{url}clear/v1")

#Testing that auth_logout functions correctly with login
def test_logout_with_login():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'secondemail@gmail.com', 'password' : 'random',})
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'thirdemail@gmail.com', 'password' : 'random',})
  
    user1 = user1.json()
    user2 = user2.json()
    user3 = user3.json()

    login1 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'validemail@gmail.com', 'password' : 'random',})
    login2 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'secondemail@gmail.com', 'password' : 'random',})
    login3 = requests.post(f"{url}auth/login/v2", json = { 'email' : 'thirdemail@gmail.com', 'password' : 'random',})
    login1a = requests.post(f"{url}auth/login/v2", json = { 'email' : 'validemail@gmail.com', 'password' : 'random',})

    login1 = login1.json()
    login2 = login2.json()
    login3 = login3.json()
    login1a = login1a.json()

    result1b = requests.post(f"{url}auth/logout/v1", json = { 'token' : user1['token']})
    result2b = requests.post(f"{url}auth/logout/v1", json = { 'token' : user2['token']})
    result3b = requests.post(f"{url}auth/logout/v1", json = { 'token' : user3['token']})
    result1c = requests.post(f"{url}auth/logout/v1", json = { 'token' : login1['token']})
    result2c = requests.post(f"{url}auth/logout/v1", json = { 'token' : login2['token']})
    result3c = requests.post(f"{url}auth/logout/v1", json = { 'token' : login3['token']})

    assert result1b.json() == {'is_success' : True,}
    assert result2b.json() == {'is_success' : True,}
    assert result3b.json() == {'is_success' : True,}
    assert result1c.json() == {'is_success' : True,}
    assert result2c.json() == {'is_success' : True,}
    assert result3c.json() == {'is_success' : True,}
    requests.delete(f"{url}clear/v1")

#Testing the basic generation of a user handle
def test_basic_handle():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output = output.json()
    assert output['user']['handle_str'] == 'compstudent'
    requests.delete(f"{url}clear/v1")

#Testing that the handle correctly adds a trailing integer when a name is repeated    
def test_trailing_int_handle():
    url = config.url
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp', 'name_last' : 'Student', 'email' : 'valemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()

    output = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user2['auth_user_id']})
    output = output.json()

    assert output['user']['handle_str'] == 'compstudent0'
    requests.delete(f"{url}clear/v1")
     
#Testing that the handle is limited to 20 characters
def test_handle_with_name_over_20_characters():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Jordan', 'name_last' : 'Milchabcdefghijk', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output = output.json()
    assert output['user']['handle_str'] == 'jordanmilchabcdefghi'
     
#Testing that the handle does not exceed 20 characters even with a trailing integer added
def test_handle_with_name_over_20_characters_and_trailing_int():
    url = config.url
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Jordan', 'name_last' : 'Milchabcdefghijk', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Jordan', 'name_last' : 'Milchabcdefghijk', 'email' : 'valemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()
    
    output = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user2['auth_user_id']})
    output = output.json()

    assert output['user']['handle_str'] == 'jordanmilchabcdefgh0'
    requests.delete(f"{url}clear/v1")
     
#Testing multiple advanced handles - such as double digit trailing integers with handles already 20 characters long
def test_advanced_handle_creation():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Jordan', 'name_last' : 'Milch', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Jordan', 'name_last' : 'Milch', 'email' : 'valiemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()    
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Jordan', 'name_last' : 'Milch', 'email' : 'valemail@gmail.com', 'password' : 'random',})
    user3 = user3.json()
    user4 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Jordan', 'name_last' : 'Milch', 'email' : 'vaemail@gmail.com', 'password' : 'random',})
    user4 = user4.json()
    user5 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'vemail@gmail.com', 'password' : 'random',})
    user5 = user5.json()
    user6 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'email@gmail.com', 'password' : 'random',})
    user6 = user6.json()
    user7 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'mail@gmail.com', 'password' : 'random',})
    user7 = user7.json()
    user8 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'aa@gmail.com', 'password' : 'random',})
    user8 = user8.json()
    user9 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'bb@gmail.com', 'password' : 'random',})
    user9 = user9.json()
    user10 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'cc@gmail.com', 'password' : 'random',})
    user10 = user10.json()
    user11 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'dd@gmail.com', 'password' : 'random',})
    user11 = user11.json()
    user12 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'ee@gmail.com', 'password' : 'random',})
    user12 = user12.json()
    user13 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'ff@gmail.com', 'password' : 'random',})
    user13 = user13.json()
    user14 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'gg@gmail.com', 'password' : 'random',})
    user14 = user14.json()
    user15 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'hh@gmail.com', 'password' : 'random',})
    user15 = user15.json()
    user16 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'UNSWCOMPSTUDENT', 'name_last' : 'Studyingtwentytwenty', 'email' : 'ii@gmail.com', 'password' : 'random',})
    user16 = user16.json()

    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user2['auth_user_id']})
    output2 = output2.json()
    output3 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user3['auth_user_id']})
    output3 = output3.json()
    output4 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user4['auth_user_id']})
    output4 = output4.json()
    output5 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user5['auth_user_id']})
    output5 = output5.json()
    output6 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user6['auth_user_id']})
    output6 = output6.json()
    output7 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user7['auth_user_id']})
    output7 = output7.json()
    output8 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user8['auth_user_id']})
    output8 = output8.json()
    output9 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user9['auth_user_id']})
    output9 = output9.json()
    output10 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user10['auth_user_id']})
    output10 = output10.json()
    output11 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user11['auth_user_id']})
    output11 = output11.json()
    output12 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user12['auth_user_id']})
    output12 = output12.json()
    output13 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user13['auth_user_id']})
    output13 = output13.json()
    output14 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user14['auth_user_id']})
    output14 = output14.json()
    output15 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user15['auth_user_id']})
    output15 = output15.json()
    output16 = requests.get(f"{url}user/profile/v2", params = {'token' : user2['token'], 'u_id' : user16['auth_user_id']})
    output16 = output16.json()
     
    assert output1['user']['handle_str'] == 'jordanmilch'
    assert output2['user']['handle_str'] == 'jordanmilch0'
    assert output3['user']['handle_str'] == 'jordanmilch1'
    assert output4['user']['handle_str'] == 'jordanmilch2'
    assert output5['user']['handle_str'] == 'unswcompstudentstudy'
    assert output6['user']['handle_str'] == 'unswcompstudentstud0'
    assert output7['user']['handle_str'] == 'unswcompstudentstud1'
    assert output8['user']['handle_str'] == 'unswcompstudentstud2'
    assert output9['user']['handle_str'] == 'unswcompstudentstud3'
    assert output10['user']['handle_str'] == 'unswcompstudentstud4'
    assert output11['user']['handle_str'] == 'unswcompstudentstud5'
    assert output12['user']['handle_str'] == 'unswcompstudentstud6'
    assert output13['user']['handle_str'] == 'unswcompstudentstud7'
    assert output14['user']['handle_str'] == 'unswcompstudentstud8'
    assert output15['user']['handle_str'] == 'unswcompstudentstud9'
    assert output16['user']['handle_str'] == 'unswcompstudentstu10'
    requests.delete(f"{url}clear/v1")

#Testing that whitespace is eliminated from a handle when a user is registered
def test_handle_whitespace():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp  ', 'name_last' : 'Student  ', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    assert output1['user']['handle_str'] == 'compstudent'
    requests.delete(f"{url}clear/v1")

#Testing that the '@' symbol is eliminated from a handle when a user is registered
def test_handle_atsign():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'Comp@@', 'name_last' : 'Student  ', 'email' : 'validemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    assert output1['user']['handle_str'] == 'compstudent'
    requests.delete(f"{url}clear/v1")