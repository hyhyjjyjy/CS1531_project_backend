#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 18:32:66 2021

@author: z6267847
"""
import pytest
import requests
from src import config

#Creating global variables for Input and Access errirs
INPUT_ERROR = 400
ACCESS_ERROR = 403

#Testing user_profile_v2 error raising by passing in an invalid u_id
def test_user_invalid_u_id():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    result1 = user1.json()
    invalid_id = result1['auth_user_id'] + 1
    output = requests.get(f"{url}user/profile/v2", params = {'token' : result1['token'], 'u_id' : invalid_id})

    assert output.status_code == INPUT_ERROR

    requests.delete(f"{url}clear/v1")

#Testing all user and users functions to ensure an access error is raised when an invalid token is passed
def test_invalid_token():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    error1 = requests.get(config.url + 'users/all/v1', params={'token': ''})
    error2 = requests.get(f"{url}user/profile/v2", params = {'token' : 'a', 'u_id' : user1['auth_user_id'] })
    error3 = requests.put(f"{url}user/profile/setname/v2", json = {'token' : 'abc', 'name_first' : 'hello', 'name_last' : 'world'})
    error4 = requests.put(f"{url}user/profile/setemail/v2", json = {'token' : 'abcdef', 'email' : 'valid@gmail.com'})
    error6 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : 'ab12', 'handle_str' : 'abcdefgh'})

    assert error1.status_code == ACCESS_ERROR
    assert error2.status_code == ACCESS_ERROR
    assert error3.status_code == ACCESS_ERROR
    assert error4.status_code == ACCESS_ERROR
    assert error6.status_code == ACCESS_ERROR

    requests.delete(f"{url}clear/v1")

#Registering a user and ensuring user_profile_v2 is returning the correct information
def test_basic_user():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    user1 = user1.json()

    output = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output = output.json()

    assert len(output) == 1
    assert len(output['user']) == 6
    assert output['user']['email'] == 'jordan.milch@gmail.com'
    assert output['user']['name_first'] == 'jordan'
    assert output['user']['name_last'] == 'milch'
    assert output['user']['handle_str'] == 'jordanmilch'    

    requests.delete(f"{url}clear/v1")

#Registering multiple users and ensuring user_profile_v2 is returning the correct information
def test_multiple_user():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'two', 'name_last' : 'bee', 'email' : 'secondemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'three', 'name_last' : 'cee', 'email' : 'thirdemail@gmail.com', 'password' : 'random',})
    user3 = user3.json()

    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output2 = output2.json()
    output3 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user3['auth_user_id']})
    output3 = output3.json()

    assert len(output1) == 1
    assert len(output1['user']) == 6
    assert output1['user']['email'] == 'firstemail@gmail.com'
    assert output1['user']['name_first'] == 'one'
    assert output1['user']['name_last'] == 'aye'
    assert output1['user']['handle_str'] == 'oneaye'
    assert len(output2) == 1
    assert len(output2['user']) == 6
    assert output2['user']['email'] == 'secondemail@gmail.com'
    assert output2['user']['name_first'] == 'two'
    assert output2['user']['name_last'] == 'bee'
    assert output2['user']['handle_str'] == 'twobee'
    assert len(output3) == 1
    assert len(output3['user']) == 6
    assert output3['user']['email'] == 'thirdemail@gmail.com'
    assert output3['user']['name_first'] == 'three'
    assert output3['user']['name_last'] == 'cee'
    assert output3['user']['handle_str'] == 'threecee'

    requests.delete(f"{url}clear/v1")

#Testing user_profile_setname function to ensure an error is raised when invalid first name lengths are entered
def test_invalid_first_setname():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.put(f"{url}user/profile/setname/v2", json = {'token' : user1['token'], 'name_first' : 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'name_last' : 'hello'})

    assert output1.status_code == INPUT_ERROR

    requests.delete(f"{url}clear/v1")

#Testing user_profile_setname function to ensure an error is raised when invalid last name lengths are entered
def test_invalid_last_setname():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.put(f"{url}user/profile/setname/v2", json = {'token' : user1['token'], 'name_last' : 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'name_first' : 'hello'})

    assert output1.status_code == INPUT_ERROR

    requests.delete(f"{url}clear/v1")

#Registering a user and changing their name to ensure user_profile_setname is functioning correctly
def test_basic_setname():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()

    assert output1['user']['name_first'] == 'one'
    assert output1['user']['name_last'] == 'aye'

    requests.put(f"{url}user/profile/setname/v2", json = {'token' : user1['token'], 'name_first' : 'hello', 'name_last' : 'world'})

    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output2 = output2.json()

    assert output2['user']['name_first'] == 'hello'
    assert output2['user']['name_last'] == 'world'  

    requests.delete(f"{url}clear/v1")

#Registering multiple users and changing their name to ensure user_profile_setname is functioning correctly
def test_multiple_setname():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()
    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output2 = output2.json()
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'femail@gmail.com', 'password' : 'random',})
    user3 = user3.json()
    output3 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user3['auth_user_id']})
    output3 = output3.json()

    assert output1['user']['name_first'] == 'one'
    assert output1['user']['name_last'] == 'aye'
    assert output2['user']['name_first'] == 'one'
    assert output2['user']['name_last'] == 'aye'
    assert output3['user']['name_first'] == 'one'
    assert output3['user']['name_last'] == 'aye'

    requests.put(f"{url}user/profile/setname/v2", json = {'token' : user1['token'], 'name_first' : 'hello', 'name_last' : 'world'})
    requests.put(f"{url}user/profile/setname/v2", json = {'token' : user2['token'], 'name_first' : 'first', 'name_last' : 'person'})
    requests.put(f"{url}user/profile/setname/v2", json = {'token' : user3['token'], 'name_first' : 'second', 'name_last' : 'person'})

    output1a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1a = output1a.json()
    output2a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output2a = output2a.json()
    output3a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user3['auth_user_id']})
    output3a = output3a.json()

    assert output1a['user']['name_first'] == 'hello'
    assert output1a['user']['name_last'] == 'world'  
    assert output2a['user']['name_first'] == 'first'
    assert output2a['user']['name_last'] == 'person'      
    assert output3a['user']['name_first'] == 'second'
    assert output3a['user']['name_last'] == 'person'  

    requests.delete(f"{url}clear/v1")

#Testing user_profile_setemail to ensure an error is raised when an invalid email is passed in
def test_invalid_email():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user1['token'], 'email' : 'jordanmilchgmail.com'})
    output2 = requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user1['token'], 'email' : 'jordanmilch@gmailcom'})

    assert output1.status_code == INPUT_ERROR
    assert output2.status_code == INPUT_ERROR

    requests.delete(f"{url}clear/v1")

#Testing user_profile_setemail to ensure an error is raised when an email already in use by another user is passed in
def test_email_in_use():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()
    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output2 = output2.json()
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'femail@gmail.com', 'password' : 'random',})
    user3 = user3.json()

    output1 = requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user1['token'], 'email' : 'firstemail@gmail.com'})
    output2 = requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user2['token'], 'email' : 'firemail@gmail.com'})
    output3 = requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user3['token'], 'email' : 'femail@gmail.com'})
    
    assert output1.status_code == INPUT_ERROR
    assert output2.status_code == INPUT_ERROR
    assert output3.status_code == INPUT_ERROR

    requests.delete(f"{url}clear/v1")

#Registering a user and changing their email to ensure user_profile_setemail is functioning correctly
def test_basic_setemail():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()   
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()

    assert output1['user']['email'] == 'firstemail@gmail.com'

    requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user1['token'], 'email' : 'secondemail@gmail.com'})

    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output2 = output2.json()

    assert output2['user']['email'] == 'secondemail@gmail.com'

    requests.delete(f"{url}clear/v1")

#Registering multiple users and changing their email to ensure user_profile_setemail is functioning correctly
def test_multiple_setemail():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()
    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output2 = output2.json()
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'femail@gmail.com', 'password' : 'random',})
    user3 = user3.json()
    output3 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user3['auth_user_id']})
    output3 = output3.json()

    assert output1['user']['email'] == 'firstemail@gmail.com'
    assert output2['user']['email'] == 'firemail@gmail.com'
    assert output3['user']['email'] == 'femail@gmail.com'

    requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user1['token'], 'email' : 'secondemail@gmail.com'})
    requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user2['token'], 'email' : 'secoemail@gmail.com'})
    requests.put(f"{url}user/profile/setemail/v2", json = {'token' : user3['token'], 'email' : 'sedemail@gmail.com'})

    output1a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1a = output1a.json()
    output2a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output2a = output2a.json()
    output3a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user3['auth_user_id']})
    output3a = output3a.json()

    assert output1a['user']['email'] == 'secondemail@gmail.com'
    assert output2a['user']['email'] == 'secoemail@gmail.com'
    assert output3a['user']['email'] == 'sedemail@gmail.com'

    requests.delete(f"{url}clear/v1")

#Testing user_profile_sethandle to ensure that an error is raised if the handle passed in is already in use
def test_handle_in_use():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'two', 'name_last' : 'bee', 'email' : 'firemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'three', 'name_last' : 'cee', 'email' : 'femail@gmail.com', 'password' : 'random',})
    user3 = user3.json()

    error1 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user1['token'], 'handle_str' : 'threecee'})
    error2 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user2['token'], 'handle_str' : 'oneaye'})
    error3 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user3['token'], 'handle_str' : 'twobee'})
    
    assert error1.status_code == INPUT_ERROR
    assert error2.status_code == INPUT_ERROR
    assert error3.status_code == INPUT_ERROR
    
    requests.delete(f"{url}clear/v1")

#Testing user_profile_sethandle to ensure that an error is raised if an invalid handle is passed in
def test_invalid_handle():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'two', 'name_last' : 'bee', 'email' : 'firemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'three', 'name_last' : 'cee', 'email' : 'femail@gmail.com', 'password' : 'random',})
    user3 = user3.json()

    
    error1 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user1['token'], 'handle_str' : ''})
    error2 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user2['token'], 'handle_str' : 'a'})
    error3 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user3['token'], 'handle_str' : 'abcdefghijklmnopqrstu'})

    assert error1.status_code == INPUT_ERROR
    assert error2.status_code == INPUT_ERROR
    assert error3.status_code == INPUT_ERROR

    
    requests.delete(f"{url}clear/v1")

def test_handle_assumptions():
    url = config.url
    requests.delete(f"{url}clear/v1")    
    user4 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'three', 'name_last' : 'cee', 'email' : 'email@gmail.com', 'password' : 'random',})
    user4 = user4.json()
    user6 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'three', 'name_last' : 'cee', 'email' : 'mail@gmail.com', 'password' : 'random',})
    user6 = user6.json()

    error4 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user4['token'], 'handle_str' : 'Jordan Milch'})
    error6 = requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user6['token'], 'handle_str' : 'jordan@milch'})
    
    assert error4.status_code == INPUT_ERROR
    assert error6.status_code == INPUT_ERROR

#Registering a user and changing their handle to ensure user_profile_sethandle is functioning correctly
def test_basic_sethandle():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()   
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()

    assert output1['user']['handle_str'] == 'oneaye'

    requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user1['token'], 'handle_str' : 'compassign'})

    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output2 = output2.json()

    assert output2['user']['handle_str'] == 'compassign'

    requests.delete(f"{url}clear/v1")

#Registering multiple users and changing their handle to ensure user_profile_sethandle is functioning correctly
def test_multiple_sethandle():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'two', 'name_last' : 'bee', 'email' : 'firemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()
    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output2 = output2.json()
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'three', 'name_last' : 'cee', 'email' : 'femail@gmail.com', 'password' : 'random',})
    user3 = user3.json()
    output3 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user3['auth_user_id']})
    output3 = output3.json()

    assert output1['user']['handle_str'] == 'oneaye'
    assert output2['user']['handle_str'] == 'twobee'
    assert output3['user']['handle_str'] == 'threecee'

    requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user1['token'], 'handle_str' : 'hello'})
    requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user2['token'], 'handle_str' : 'world'})
    requests.put(f"{url}user/profile/sethandle/v1", json = {'token' : user3['token'], 'handle_str' : 'program'})

    output1a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1a = output1a.json()
    output2a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output2a = output2a.json()
    output3a = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user3['auth_user_id']})
    output3a = output3a.json()

    assert output1a['user']['handle_str'] == 'hello'
    assert output2a['user']['handle_str'] == 'world'
    assert output3a['user']['handle_str'] == 'program'

    requests.delete(f"{url}clear/v1")

#Testing if users_all is functioning correctly when a single user is registered            
def test_users_all_basic():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()    
    profile = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    profile = profile.json()    
    output = requests.get(f"{url}users/all/v1", params = {'token' : user1['token']})
    output = output.json()

    assert type(output) == dict
    assert len(output) == 1
    assert len(output['users']) == 1
    assert output['users'][0] == profile['user']
    requests.delete(f"{url}clear/v1")

#Testing if users_all is functioning correctly when multiple users are registered            
def test_users_all_multiple():
    url = config.url
    requests.delete(f"{url}clear/v1")

    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'one', 'name_last' : 'aye', 'email' : 'firstemail@gmail.com', 'password' : 'random',})
    user1 = user1.json()    
    profile1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    profile1 = profile1.json() 
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'two', 'name_last' : 'bee', 'email' : 'firemail@gmail.com', 'password' : 'random',})
    user2 = user2.json()    
    profile2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    profile2 = profile2.json() 
    user3 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'three', 'name_last' : 'cee', 'email' : 'femail@gmail.com', 'password' : 'random',})
    user3 = user3.json()    
    profile3 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user3['auth_user_id']})
    profile3 = profile3.json() 

    output = requests.get(f"{url}users/all/v1", params = {'token' : user1['token']})
    output = output.json()
    
    assert type(output) == dict
    assert len(output) == 1
    assert len(output['users']) == 3
    assert output['users'][0] == profile1['user']
    assert output['users'][1] == profile2['user']
    assert output['users'][2] == profile3['user']

    requests.delete(f"{url}clear/v1")
