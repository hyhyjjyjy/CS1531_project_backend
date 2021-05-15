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

def message_senddm_v1(token, dm_id, message):
    url = config.url
    rt = requests.post(f"{url}message/senddm/v1", json={'token': token,
                                                    'dm_id': dm_id,
                                                    'message': message,})
    return rt

def dm_messages_v1(token, dm_id, start):
    url = config.url
    rt = requests.get(f"{url}dm/messages/v1", params={'token': token,
                                                    'dm_id': dm_id,
                                                    'start': start,})
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
    dm_1 = dm_1.json()

    user_list = []
    user_list.append(users[0]['auth_user_id'])
    dm_2 = dm_create_v1(users[1]['token'], user_list)#create dm 2 
    dm_2 = dm_2.json()

    user_list = []
    user_list.append(users[0]['auth_user_id'])
    user_list.append(users[1]['auth_user_id'])
    user_list.append(users[2]['auth_user_id'])
    dm_3 = dm_create_v1(users[3]['token'], user_list)#create dm 3
    dm_3 = dm_3.json()

    message_ids_1 = []
    #correct_msg_1 = []
    for i in range(0, 50):
        msg = str(i)
        message_id = message_senddm_v1(users[0]['token'], dm_1['dm_id'], msg)
        message_id = message_id.json()
        message_ids_1.append(message_id)
        #correct_msg_1.append(msg)


    message_ids_2 = []
    for i in range(200, 400):
        msg = str(i)
        message_id = message_senddm_v1(users[0]['token'], dm_2['dm_id'], msg)
        message_id = message_id.json()
        message_ids_2.append(message_id)


    # message_ids_3 = []
    # for i in range(0, 800):
    #     msg = str(i)
    #     message_id = message_senddm_v1(users[0]['token'], dm_3['dm_id'], msg)
    #     message_ids_3.append(message_id)


    return {'users': users,
            'dms': [dm_1, dm_2, dm_3],
            'msg_ids':[message_ids_1, message_ids_2]}



def test_dm_message_errors(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    
    #invalid dm_id
    rt = dm_messages_v1(users[0]['token'], 1000, 0)
    assert rt.status_code == InputError 

    rt = dm_messages_v1(users[0]['token'], 32423, 0)
    assert rt.status_code == InputError 

    #too large start number
    rt = dm_messages_v1(users[0]['token'], dm_1['dm_id'], 500)
    assert rt.status_code == InputError 

    rt = dm_messages_v1(users[0]['token'], dm_2['dm_id'], 800)
    assert rt.status_code == InputError 

    #invalid token
    rt = dm_messages_v1("dwaedwqa", dm_1['dm_id'], 0)
    assert rt.status_code == AccessError 

    rt = dm_messages_v1("I need your time", dm_1['dm_id'], 0)
    assert rt.status_code == AccessError 

    #authorised member not in the dm
    rt = dm_messages_v1(users[3]['token'], dm_1['dm_id'], 0)
    assert rt.status_code == AccessError 

    rt = dm_messages_v1(users[3]['token'], dm_2['dm_id'], 0)
    assert rt.status_code == AccessError 

    clear_v1()



def test_dm_message_pass(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    message_ids_1 = create_dms['msg_ids'][0]
    message_ids_2 = create_dms['msg_ids'][1]


    messages_1 = dm_messages_v1(users[0]['token'], dm_1['dm_id'], 0)
    messages_1 = messages_1.json()

    end = messages_1['end']
    start = messages_1['start']
    msgs = messages_1['messages']
    assert end == -1
    assert start == 0
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_1[49 - i]['message_id']


    messages_2 = dm_messages_v1(users[0]['token'], dm_2['dm_id'], 0)
    messages_2 = messages_2.json()
    end = messages_2['end']
    start = messages_2['start']
    msgs = messages_2['messages']
    assert end == 50
    assert start == 0
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_2[199 - i]['message_id']
    
    messages_2 = dm_messages_v1(users[0]['token'], dm_2['dm_id'], end)
    messages_2 = messages_2.json()
    end = messages_2['end']
    start = messages_2['start']
    msgs = messages_2['messages']
    assert end == 100
    assert start == 50
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_2[149 - i]['message_id']

    messages_2 = dm_messages_v1(users[0]['token'], dm_2['dm_id'], end)
    messages_2 = messages_2.json()
    end = messages_2['end']
    start = messages_2['start']
    msgs = messages_2['messages']
    assert end == 150
    assert start == 100
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_2[99 - i]['message_id']
    
    messages_2 = dm_messages_v1(users[0]['token'], dm_2['dm_id'], end)
    messages_2 = messages_2.json()
    end = messages_2['end']
    start = messages_2['start']
    msgs = messages_2['messages']
    assert end == -1
    assert start == 150
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_2[49 - i]['message_id']

    clear_v1()