import pytest
from src.auth import auth_register_v2
from src.user import user_profile_setemail_v2, user_profile_sethandle_v1, users_all_v1, user_profile_setname_v2, user_profile_v2
from src.other import clear_v1
from src.error import InputError, AccessError
from src.admin import admin_user_remove_v1

def test_user_invalid_u_id():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    invalid_id = result1['auth_user_id'] + 1
    with pytest.raises(InputError):
        user_profile_v2(result1['token'], invalid_id)
    clear_v1()

def test_invalid_token():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    with pytest.raises(AccessError):
        user_profile_setemail_v2('', 'secondemail@gmail.com')
    with pytest.raises(AccessError):
        user_profile_sethandle_v1('', 'compstudent01')
    with pytest.raises(AccessError):
        user_profile_setname_v2('', 'jordan', 'milch')
    with pytest.raises(AccessError):
        user_profile_v2('', result1['auth_user_id'])
    with pytest.raises(AccessError):
        users_all_v1('')
    clear_v1()

def test_basic_user():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    output = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert len(output) == 1
    assert len(output['user']) == 6
    assert output['user']['email'] == 'firstemail@gmail.com'
    assert output['user']['name_first'] == 'comp'
    assert output['user']['name_last'] == 'student'
    assert output['user']['handle_str'] == 'compstudent'
    clear_v1()

def test_multiple_user():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'two', 'bee')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'three', 'cee')
    output1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    output2 = user_profile_v2(result1['token'], result2['auth_user_id'])
    output3 = user_profile_v2(result1['token'], result3['auth_user_id'])
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
    clear_v1()

#Testing if a removed user can still be accessed through user_profile
def test_removed_user():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'two', 'bee')
    admin_user_remove_v1(result1['token'], result2['auth_user_id'])
    output1 = user_profile_v2(result1['token'], result2['auth_user_id'])
    assert len(output1) == 1
    assert len(output1['user']) == 6
    assert output1['user']['email'] == 'secondemail@gmail.com'
    assert output1['user']['name_first'] + output1['user']['name_last'] == 'Removed user'
    assert output1['user']['handle_str'] == 'twobee'    
    clear_v1()
    
      
def test_invalid_first_setname():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    with pytest.raises(InputError):
        user_profile_setname_v2(result1['token'], 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'hello')
    clear_v1()

#Testing last names less than 1 character and more than 60 characters long to determine if auth_register_v1 is correctly identifying this error
def test_invalid_last_name():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    with pytest.raises(InputError):
        user_profile_setname_v2(result1['token'], 'hello', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
    clear_v1()

def test_basic_setname():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    output1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output1['user']['name_first'] == 'one'
    assert output1['user']['name_last'] == 'aye'
    user_profile_setname_v2(result1['token'], 'hello', 'world')
    output2 = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output2['user']['name_first'] == 'hello'
    assert output2['user']['name_last'] == 'world'
    clear_v1()

def test_multiple_setname():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'two', 'bee')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'three', 'cee')
    output1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    output2 = user_profile_v2(result1['token'], result2['auth_user_id'])
    output3 = user_profile_v2(result1['token'], result3['auth_user_id'])
    assert output1['user']['name_first'] == 'one'
    assert output1['user']['name_last'] == 'aye'
    assert output2['user']['name_first'] == 'two'
    assert output2['user']['name_last'] == 'bee'
    assert output3['user']['name_first'] == 'three'
    assert output3['user']['name_last'] == 'cee'
    user_profile_setname_v2(result1['token'], 'hello', 'world')
    user_profile_setname_v2(result2['token'], 'jump', 'start')
    user_profile_setname_v2(result3['token'], 'take', 'onme')
    output1a = user_profile_v2(result1['token'], result1['auth_user_id'])
    output2a = user_profile_v2(result2['token'], result2['auth_user_id'])
    output3a = user_profile_v2(result3['token'], result3['auth_user_id'])

    assert output1a['user']['name_first'] == 'hello'
    assert output1a['user']['name_last'] == 'world'
    assert output2a['user']['name_first'] == 'jump'
    assert output2a['user']['name_last'] == 'start'
    assert output3a['user']['name_first'] == 'take'
    assert output3a['user']['name_last'] == 'onme'
    clear_v1()

def test_invalid_email():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    with pytest.raises(InputError):
        user_profile_setemail_v2(result1['token'], 'jordanmilchgmail.com')
    with pytest.raises(InputError):
        user_profile_setemail_v2(result1['token'], 'a@hgmail.com')

def test_email_in_use():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'two', 'bee')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'three', 'cee')
    with pytest.raises(InputError):
        user_profile_setemail_v2(result1['token'], 'secondemail@gmail.com')
    with pytest.raises(InputError):
        user_profile_setemail_v2(result2['token'], 'firstemail@gmail.com')
    with pytest.raises(InputError):
        user_profile_setemail_v2(result3['token'], 'firstemail@gmail.com')
    clear_v1()

def test_basic_setemail():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    output1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output1['user']['email'] == 'firstemail@gmail.com'
    user_profile_setemail_v2(result1['token'], 'secondemail@gmail.com')
    output2 = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output2['user']['email'] == 'secondemail@gmail.com'
    clear_v1()

def test_multiple_setemail():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'two', 'bee')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'three', 'cee')
    output1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    output2 = user_profile_v2(result1['token'], result2['auth_user_id'])
    output3 = user_profile_v2(result1['token'], result3['auth_user_id'])
    assert output1['user']['email'] == 'firstemail@gmail.com'
    assert output2['user']['email'] == 'secondemail@gmail.com'
    assert output3['user']['email'] == 'thirdemail@gmail.com'
    user_profile_setemail_v2(result1['token'], 'random@random.com')
    user_profile_setemail_v2(result2['token'], 'one@one.com')
    user_profile_setemail_v2(result3['token'], 'two@two.com')
    output1a = user_profile_v2(result1['token'], result1['auth_user_id'])
    output2a = user_profile_v2(result2['token'], result2['auth_user_id'])
    output3a = user_profile_v2(result3['token'], result3['auth_user_id'])

    assert output1a['user']['email'] == 'random@random.com'
    assert output2a['user']['email'] == 'one@one.com'
    assert output3a['user']['email'] == 'two@two.com'
    clear_v1()

def test_handle_in_use():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'two', 'bee')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'three', 'cee')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(result1['token'], 'threecee')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(result2['token'], 'oneaye')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(result3['token'], 'twobee')
    clear_v1()

def test_invalid_handle():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(result1['token'], 'a')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(result1['token'], '')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(result1['token'], 'abcdefghijklmnopqrstuvwxyz')
    clear_v1()

def test_assumptions_handle():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(result1['token'], 'Jordan Milch')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(result1['token'], 'Jordan@Milch')
    clear_v1()

def test_basic_sethandle():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    output1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output1['user']['handle_str'] == 'oneaye'
    user_profile_sethandle_v1(result1['token'], 'newhandle')
    output2 = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert output2['user']['handle_str'] == 'newhandle'
    clear_v1()

def test_multiple_sethandle():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'two', 'bee')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'three', 'cee')
    output1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    output2 = user_profile_v2(result1['token'], result2['auth_user_id'])
    output3 = user_profile_v2(result1['token'], result3['auth_user_id'])
    assert output1['user']['handle_str'] == 'oneaye'
    assert output2['user']['handle_str'] == 'twobee'
    assert output3['user']['handle_str'] == 'threecee'
    user_profile_sethandle_v1(result1['token'], 'newhandle')
    user_profile_sethandle_v1(result2['token'], 'random')
    user_profile_sethandle_v1(result3['token'], 'compstudent')
    output1a = user_profile_v2(result1['token'], result1['auth_user_id'])
    output2a = user_profile_v2(result2['token'], result2['auth_user_id'])
    output3a = user_profile_v2(result3['token'], result3['auth_user_id'])

    assert output1a['user']['handle_str'] == 'newhandle'
    assert output2a['user']['handle_str'] == 'random'
    assert output3a['user']['handle_str'] == 'compstudent'
    clear_v1()

def test_users_all_basic():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    profile = user_profile_v2(result1['token'], result1['auth_user_id'])
    output = users_all_v1(result1['token'])
    assert type(output) == dict
    assert len(output) == 1
    assert len(output['users']) == 1
    assert output['users'][0] == profile['user']
    clear_v1()

def test_users_all_multiple():
    clear_v1()
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'one', 'aye')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'two', 'bee')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'three', 'cee')
    profile1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    profile2 = user_profile_v2(result1['token'], result2['auth_user_id'])
    profile3 = user_profile_v2(result1['token'], result3['auth_user_id'])

    output = users_all_v1(result1['token'])

    assert type(output) == dict
    assert len(output) == 1
    assert len(output['users']) == 3
    assert output['users'][0] == profile1['user']
    assert output['users'][1] == profile2['user']
    assert output['users'][2] == profile3['user']
    clear_v1()
