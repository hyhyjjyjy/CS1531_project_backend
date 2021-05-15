import pytest
import requests
import json
import jwt
from src import config

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

def dm_leave_v1(token, dm_id):
    url = config.url
    rt = requests.post(f"{url}dm/leave/v1", json={'token': token,
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




#test if the errors occur when wrong values are passed into dm_leave function
def test_dm_leave_errors(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    #dm_3 = create_dms['dms'][2]

    #invalid token
    rt = dm_leave_v1("ded", dm_1['dm_id'])
    assert rt.status_code == AccessError

    #wrong dm id
    rt = dm_leave_v1(users[0]['token'], 34543)
    assert rt.status_code == InputError
    rt = dm_leave_v1(users[1]['token'], 100)   
    assert rt.status_code == InputError
    

    #not in the dm
    rt = dm_leave_v1(users[3]['token'], dm_1['dm_id'])
    assert rt.status_code == AccessError
    rt = dm_leave_v1(users[3]['token'], dm_2['dm_id'])
    assert rt.status_code == AccessError
    rt = dm_leave_v1(users[2]['token'], dm_2['dm_id'])
    assert rt.status_code == AccessError

    

    clear_v1()


    

#test if a proper user can leave a proper dm 
def test_dm_leave(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    dm_3 = create_dms['dms'][2]

    dm_details_v1(users[0]['token'], dm_1['dm_id'])
    dm_leave_v1(users[2]['token'], dm_1['dm_id'])
    dm_leave_v1(users[0]['token'], dm_1['dm_id'])
    dm_leave_v1(users[1]['token'], dm_1['dm_id'])#leave dm 1
    

    dm_details_v1(users[1]['token'], dm_2['dm_id'])
    dm_leave_v1(users[1]['token'], dm_2['dm_id'])#leave dm 2


    dm_details_v1(users[3]['token'], dm_3['dm_id'])
    dm_leave_v1(users[3]['token'], dm_3['dm_id'])
    dm_leave_v1(users[0]['token'], dm_3['dm_id'])
    dm_leave_v1(users[2]['token'], dm_3['dm_id'])
    dm_leave_v1(users[1]['token'], dm_3['dm_id'])#leave dm 3

    rt = dm_details_v1(users[0]['token'], dm_1['dm_id'])
    assert rt.status_code == InputError
    
    rt = dm_details_v1(users[3]['token'], dm_3['dm_id'])
    assert rt.status_code == InputError

    rt = dm_details_v1(users[1]['token'], dm_2['dm_id'])
    assert rt.status_code == InputError

    clear_v1()