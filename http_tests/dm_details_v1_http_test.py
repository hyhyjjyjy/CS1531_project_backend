import pytest
import requests
import json
import jwt
from src import config
from http_tests.helper_function_for_http_test import user_profile_v2

AccessError = 403
InputError = 400

################################ helper function ##############################################
def clear_v1():
    url = config.url
    rt = requests.delete(f"{url}clear/v1")
    return rt

def auth_register_v2(email, password, name_first, name_last):
    url = config.url
    user = requests.post(f"{url}auth/register/v2", json={'email': email, 
                                                  'password': password, 
                                                  'name_first': name_first, 
                                                  'name_last': name_last})
    return user

def dm_create_v1(token, user_list):
    url = config.url
    dm = requests.post(f"{url}dm/create/v1", json={  'token': token,
                                                    'u_ids': user_list})
    return dm

def dm_details_v1(token, dm_id):
    url = config.url
    rt = requests.get(f"{url}dm/details/v1", params={'token': token,
                                                    'dm_id': dm_id,})
    return rt
################################ helper function ##############################################



@pytest.fixture
def create_dms():
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'a', 'b')
    user2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'c', 'd')
    user3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'e', 'f')
    user4 = auth_register_v2('fourthemail@gmail.com', '123abc!@#', 'g', 'h')
    users = [user1.json(), user2.json(), user3.json(), user4.json()]


    user_list = []
    user_list.append(users[1]['auth_user_id'])
    user_list.append(users[2]['auth_user_id'])
    dm_1 = dm_create_v1(users[0]['token'], user_list)#create dm 1

    user_list = []
    user_list.append(users[0]['auth_user_id'])
    dm_2 = dm_create_v1(users[1]['token'], user_list)#create dm 2 

    user_list = []
    user_list.append(users[0]['auth_user_id'])
    user_list.append(users[1]['auth_user_id'])
    user_list.append(users[2]['auth_user_id'])
    dm_3 = dm_create_v1(users[3]['token'], user_list)#create dm 3



    return {'users': users,
            'dms': [dm_1.json(), dm_2.json(), dm_3.json()]}

#test if the errors occurs when we pass in wrong value into the dm-detail function
def test_dm_details_errors(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    #dm_3 = create_dms['dms'][2]

    rt = dm_details_v1(users[0]['token'], 100)
    assert rt.status_code == InputError

    rt = dm_details_v1(users[0]['token'], 500)
    assert rt.status_code == InputError

    rt = dm_details_v1(users[3]['token'], dm_1['dm_id'])
    assert rt.status_code == AccessError

    rt = dm_details_v1(users[3]['token'], dm_2['dm_id'])
    assert rt.status_code == AccessError

    rt = dm_details_v1(users[2]['token'], dm_2['dm_id'])
    assert rt.status_code == AccessError

    rt = dm_details_v1("fewfwfe", dm_1['dm_id'])
    assert rt.status_code == AccessError

    clear_v1()

#test if the detail function works when we are doing right
def test_dm_details(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    dm_3 = create_dms['dms'][2]

    profile_0 = user_profile_v2(users[0]['token'], users[0]['auth_user_id']).json()['user']
    profile_1 = user_profile_v2(users[0]['token'], users[1]['auth_user_id']).json()['user']
    profile_2 = user_profile_v2(users[0]['token'], users[2]['auth_user_id']).json()['user']
    profile_3 = user_profile_v2(users[0]['token'], users[3]['auth_user_id']).json()['user']


    rt_val_1 = dm_details_v1(users[0]['token'], dm_1['dm_id'])
    rt_val_1 = rt_val_1.json()
    assert rt_val_1['name'] == "ab, cd, ef"
    assert sorted(rt_val_1['members'], key=lambda x:x['u_id']) == sorted([
                                {  'u_id': users[1]['auth_user_id'],
                                    'name_first': 'c',
                                    'name_last': 'd',
                                    'email': 'secondemail@gmail.com',
                                    'handle_str': 'cd',
                                    'profile_img_url' : profile_1['profile_img_url'],

                                },
                                {  'u_id': users[2]['auth_user_id'],
                                    'name_first': 'e',
                                    'name_last': 'f',
                                    'email': 'thirdemail@gmail.com',
                                    'handle_str': 'ef',
                                    'profile_img_url' : profile_2['profile_img_url'],

                                },
                                {  'u_id': users[0]['auth_user_id'],
                                    'name_first': 'a',
                                    'name_last': 'b',
                                    'email': 'validemail@gmail.com',
                                    'handle_str': 'ab',
                                    'profile_img_url' : profile_0['profile_img_url'],

                                },
                                ], key=lambda x:x['u_id'])


    rt_val_2 = dm_details_v1(users[1]['token'], dm_2['dm_id'])
    rt_val_2 = rt_val_2.json()

    assert rt_val_2['name'] == "ab, cd"
    assert sorted(rt_val_2['members'], key=lambda x:x['u_id']) == sorted([
                                {  'u_id': users[0]['auth_user_id'],
                                    'name_first': 'a',
                                    'name_last': 'b',
                                    'email': 'validemail@gmail.com',
                                    'handle_str': 'ab',
                                    'profile_img_url' : profile_0['profile_img_url'],

                                },
                                {  'u_id': users[1]['auth_user_id'],
                                    'name_first': 'c',
                                    'name_last': 'd',
                                    'email': 'secondemail@gmail.com',
                                    'handle_str': 'cd',
                                    'profile_img_url' : profile_1['profile_img_url'],

                                },
                                ], key=lambda x:x['u_id'])


    

    rt_val_3 = dm_details_v1(users[3]['token'], dm_3['dm_id'])
    rt_val_3 = rt_val_3.json()

    assert rt_val_3['name'] == "ab, cd, ef, gh"
    assert rt_val_3['members'] == [
                                {  'u_id': users[0]['auth_user_id'],
                                    'name_first': 'a',
                                    'name_last': 'b',
                                    'email': 'validemail@gmail.com',
                                    'handle_str': 'ab',
                                    'profile_img_url' : profile_0['profile_img_url'],

                                },
                                {  'u_id': users[1]['auth_user_id'],
                                    'name_first': 'c',
                                    'name_last': 'd',
                                    'email': 'secondemail@gmail.com',
                                    'handle_str': 'cd',
                                    'profile_img_url' : profile_1['profile_img_url'],

                                },
                                {  'u_id': users[2]['auth_user_id'],
                                    'name_first': 'e',
                                    'name_last': 'f',
                                    'email': 'thirdemail@gmail.com',
                                    'handle_str': 'ef',
                                    'profile_img_url' : profile_2['profile_img_url'],

                                },
                                {  'u_id': users[3]['auth_user_id'],
                                    'name_first': 'g',
                                    'name_last': 'h',
                                    'email': 'fourthemail@gmail.com',
                                    'handle_str': 'gh',
                                    'profile_img_url' : profile_3['profile_img_url'],

                                },
                                ]
    
    clear_v1()
