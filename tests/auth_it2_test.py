#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 10:56:18 2021

@author: z5257847
"""

import pytest
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.user import user_profile_v2
from src.admin import admin_user_remove_v1

#Fixture to register 3 users to prevent repeating code
@pytest.fixture
def register_three_users():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    auth_register_v2('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student')

#Testing multiple invalid emails to determine if auth_register_v2 is correctly identifying this error
def test_invalid_email_register():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('invalidemailgmail.com', '123abc!@#', 'Comp', 'Student')
        auth_register_v2('invalid#email@gmail.com', '123abc!@#', 'Comp', 'Student')              
    clear_v1()

#Testing passwords less than 6 characters long to determine if auth_register_v2 is correctly identifying this error
def test_short_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('pwdshortemail1@gmail.com', 'hi', 'Comp', 'Student')
    with pytest.raises(InputError):
        auth_register_v2('pwdshortemail2@gmail.com', '', 'Comp', 'Student')
    with pytest.raises(InputError):
        auth_register_v2('pwdshortemail3@gmail.com', 'COMP', 'Comp', 'Student')
    clear_v1()

#Testing first names less than 1 character and more than 50 characters long to determine if auth_register_v2 is correctly identifying this error
def test_invalid_first_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('fnameshortemail1@gmail.com', 'hello123', '', 'Student')
    with pytest.raises(InputError):
        auth_register_v2('fnamelongemail1@gmail.com', 'hello123', 
                         'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 
                         'Student')
    clear_v1()

#Testing last names less than 1 character and more than 50 characters long to determine if auth_register_v2 is correctly identifying this error
def test_invalid_last_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('lnameshortemail1@gmail.com', 'hello123', 'Comp',
                         'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz') 
    clear_v1()

def test_simple_register():
    clear_v1()
    result = auth_register_v2('firstemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    assert type(result) == dict
    assert len(result) == 2
    assert type(result['token']) == str
    assert type(result['auth_user_id']) == int
    clear_v1()

def test_multiple_register():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student')
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
    clear_v1()

def test_removed_users():
    result1 = auth_register_v2('firstemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    admin_user_remove_v1(result1['token'], result3['auth_user_id'])
    result4 = auth_register_v2('fourthemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    assert result4['auth_user_id'] != result3['auth_user_id']
    assert result4['auth_user_id'] != result2['auth_user_id']
    assert result4['auth_user_id'] != result1['auth_user_id']

#Testing for multiple users, whilst an error is raised, to ensure the code continues to function as expected
def test_multiple_register_with_error(register_three_users):
    result1 = auth_register_v2('fourthemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    with pytest.raises(InputError):   
        auth_register_v2('invalidemailgmail.com', '123abc!@#', 'Comp', 'Student')                      
    result2 = auth_register_v2('fifthemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    assert result1 != result2
    assert result1['auth_user_id'] != result2['auth_user_id']
    assert result1['token'] != result2['token']
    clear_v1()

#Testing auth_register_v1 to check that an error is raised when an already registered email is used again
def test_email_in_use_register(register_three_users):
    with pytest.raises(InputError):                         
        auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')               
    with pytest.raises(InputError):
        auth_register_v2('secondemail@gmail.com', 'random', 'Comp', 'Student')               
    with pytest.raises(InputError):
        auth_register_v2('thirdemail@gmail.com', 'random', 'Comp', 'Student') 
    clear_v1()

def test_invalid_email_login():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')    
    with pytest.raises(InputError):
        auth_login_v2('invalidemailgmail.com', '123abc!@#')
    with pytest.raises(InputError):
        auth_login_v2('invalid#email@gmail.com', '123abc!@#')
    clear_v1()

def test_email_doesnt_belong(register_three_users):
    with pytest.raises(InputError):
        auth_login_v2('comp@gmail.com','random')
    with pytest.raises(InputError):
        auth_login_v2('unsw@gmail.com','random')
    with pytest.raises(InputError):
        auth_login_v2('sydney@gmail.com','random')
    clear_v1()

def test_password_doesnt_match(register_three_users):
    with pytest.raises(InputError):
        auth_login_v2('validemail@gmail.com','incorrect')
    with pytest.raises(InputError):
        auth_login_v2('secondemail@gmail.com','wrongpass')
    with pytest.raises(InputError):
        auth_login_v2('thirdemail@gmail.com','errorexpect')
    clear_v1()

def test_empty_login():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v2('validemail@gmail.com','incorrect')  
    clear_v1()

def test_login_basic():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')    
    result2 = auth_login_v2('validemail@gmail.com', '123abc!@#')
    assert result1 != result2
    assert type(result1) == dict
    assert type(result1['auth_user_id']) == int
    assert type(result2) == dict
    assert type(result2['auth_user_id']) == int
    assert result1['auth_user_id'] == result2['auth_user_id']
    assert result1['token'] != result2['token']
    clear_v1()

def test_login_multiple():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student') 
    result1a = auth_login_v2('validemail@gmail.com', '123abc!@#')
    result2a = auth_login_v2('secondemail@gmail.com', '123abc!@#')
    result3a = auth_login_v2('thirdemail@gmail.com', '123abc!@#')
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
    clear_v1()

def test_logout_basic():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result2 = auth_logout_v1(result1['token'])
    assert result2 == {'is_success' : True,}
    clear_v1()

def test_logout_empty():
    clear_v1()
    with pytest.raises(AccessError):
        auth_logout_v1('')
    clear_v1()

def test_invalid_logout_token():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result2 = auth_logout_v1(result1['token'])
    with pytest.raises(AccessError):    
        auth_logout_v1(result1['token'])
    assert result2 == {'is_success' : True,}
    clear_v1()


def test_multiple_logout():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student') 
    result1a = auth_logout_v1(result1['token'])
    result2a = auth_logout_v1(result2['token'])
    result3a = auth_logout_v1(result3['token'])
    assert result1a == {'is_success' : True,}
    assert result2a == {'is_success' : True,}
    assert result3a == {'is_success' : True,}
    clear_v1()
    
def test_multiple_logout_with_error():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student') 
    result1a = auth_logout_v1(result1['token'])
    with pytest.raises(AccessError):
        auth_logout_v1(result1['token'])
    result2a = auth_logout_v1(result2['token'])
    result3a = auth_logout_v1(result3['token'])
    assert result1a == {'is_success' : True,}
    assert result2a == {'is_success' : True,}
    assert result3a == {'is_success' : True,}
    clear_v1()

def test_logout_with_login():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    result3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student') 
    result1a = auth_login_v2('validemail@gmail.com', '123abc!@#')
    result1a = auth_login_v2('validemail@gmail.com', '123abc!@#')
    result2a = auth_login_v2('secondemail@gmail.com', '123abc!@#')
    result3a = auth_login_v2('thirdemail@gmail.com', '123abc!@#')
    result1b = auth_logout_v1(result1['token'])
    result2b = auth_logout_v1(result2['token'])
    result3b = auth_logout_v1(result3['token'])
    result1c = auth_logout_v1(result1a['token'])
    result2c = auth_logout_v1(result2a['token'])
    result3c = auth_logout_v1(result3a['token'])
    assert result1b == {'is_success' : True,}
    assert result2b == {'is_success' : True,}
    assert result3b == {'is_success' : True,}
    assert result1c == {'is_success' : True,}
    assert result2c == {'is_success' : True,}
    assert result3c == {'is_success' : True,}
    clear_v1()

def test_basic_handle():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    output = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output['user']['handle_str'] == 'compstudent'
    clear_v1()
     
def test_trailing_int_handle():
    clear_v1()
    auth_register_v2('jordanmilch@gmail.com', 'random', 'Jordan', 'Milch')
    user_2 = auth_register_v2('jmilch@gmail.com', 'random', 'Jordan', 'Milch')
    output = user_profile_v2(user_2['token'], user_2['auth_user_id'])
    assert output['user']['handle_str'] == 'jordanmilch0'
    clear_v1()
     
#Testing that the handle is limited to 20 characters
def test_handle_with_name_over_20_characters():
    clear_v1()
    user_1 = auth_register_v2('jordanmilch@gmail.com', 'random', 'Jordan', 'Milchabcdefghijk')
    output = user_profile_v2(user_1['token'], user_1['auth_user_id'])
    assert output['user']['handle_str'] == 'jordanmilchabcdefghi'
    clear_v1()
     
#Testing that the handle does not exceed 20 characters even with a trailing integer added
def test_handle_with_name_over_20_characters_and_trailing_int():
    clear_v1()
    auth_register_v2('jordanmilch@gmail.com', 'random', 'Jordan', 'Milchabcdefghijk')
    user_2 = auth_register_v2('jmilch@gmail.com', 'random', 'Jordan', 'Milchabcdefghijk')
    output = user_profile_v2(user_2['token'], user_2['auth_user_id'])
    assert output['user']['handle_str'] == 'jordanmilchabcdefgh0'
    clear_v1()
     
#Testing multiple advanced handles - such as double digit trailing integers with handles already 20 characters long
def test_advanced_handle_creation():
    clear_v1()
    user_1 = auth_register_v2('jordanmilch@gmail.com', 'random', 'Jordan', 'Milch')
    user_2 = auth_register_v2('jordanmilch1@gmail.com', 'random', 'Jordan', 'Milch')
    user_3 = auth_register_v2('jordanmilch2@gmail.com', 'random', 'Jordan', 'Milch')
    user_4 = auth_register_v2('jordanmilch3@gmail.com', 'random', 'Jordan', 'Milch')
    user_5 = auth_register_v2('random@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_6 = auth_register_v2('random1@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_7 = auth_register_v2('random2@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_8 = auth_register_v2('random3@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_9 = auth_register_v2('random4@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_10 = auth_register_v2('random5@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_11 = auth_register_v2('random6@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_12 = auth_register_v2('random7@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_13 = auth_register_v2('random8@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_14 = auth_register_v2('random9@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_15 = auth_register_v2('random10@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    user_16 = auth_register_v2('random11@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
 
    output1 = user_profile_v2(user_1['token'], user_1['auth_user_id'])
    output2 = user_profile_v2(user_2['token'], user_2['auth_user_id'])
    output3 = user_profile_v2(user_3['token'], user_3['auth_user_id'])
    output4 = user_profile_v2(user_4['token'], user_4['auth_user_id'])
    output5 = user_profile_v2(user_5['token'], user_5['auth_user_id'])
    output6 = user_profile_v2(user_6['token'], user_6['auth_user_id'])
    output7 = user_profile_v2(user_7['token'], user_7['auth_user_id'])
    output8 = user_profile_v2(user_8['token'], user_8['auth_user_id'])
    output9 = user_profile_v2(user_9['token'], user_9['auth_user_id'])
    output10 = user_profile_v2(user_10['token'], user_10['auth_user_id'])
    output11 = user_profile_v2(user_11['token'], user_11['auth_user_id'])
    output12 = user_profile_v2(user_12['token'], user_12['auth_user_id'])
    output13 = user_profile_v2(user_13['token'], user_13['auth_user_id'])
    output14 = user_profile_v2(user_14['token'], user_14['auth_user_id'])
    output15 = user_profile_v2(user_15['token'], user_15['auth_user_id'])
    output16 = user_profile_v2(user_16['token'], user_16['auth_user_id'])
 
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
    clear_v1()
 
def test_handle_whitespace():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp  ', 'Student')
    output = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output['user']['handle_str'] == 'compstudent'
    clear_v1()
   
def test_handle_atsign():
    clear_v1()
    result1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp@@', 'Student')
    output = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output['user']['handle_str'] == 'compstudent'
    clear_v1()