import pytest
import requests
import json
from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1
from src.dms import dm_create_v1, dm_details_v1, dm_messages_v1
from src.error import InputError, AccessError
from src.message import message_senddm_v1


@pytest.fixture
def create_dms():
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'a', 'b')
    user2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'c', 'd')
    user3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'e', 'f')
    user4 = auth_register_v2('fourthemail@gmail.com', '123abc!@#', 'g', 'h')
    users = [user1, user2, user3, user4]
    
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

    message_ids_1 = []
    #correct_msg_1 = []
    for i in range(0, 50):
        msg = str(i)
        message_id = message_senddm_v1(users[0]['token'], dm_1['dm_id'], msg)
        message_ids_1.append(message_id)
        #correct_msg_1.append(msg)


    message_ids_2 = []
    for i in range(200, 400):
        msg = str(i)
        message_id = message_senddm_v1(users[0]['token'], dm_2['dm_id'], msg)
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
    with pytest.raises(InputError):
        dm_messages_v1(users[0]['token'], 1000, 0)

    with pytest.raises(InputError):
        dm_messages_v1(users[0]['token'], 32423, 0)

    #too large start number
    with pytest.raises(InputError):
        dm_messages_v1(users[0]['token'], dm_1['dm_id'], 500)

    with pytest.raises(InputError):
        dm_messages_v1(users[0]['token'], dm_2['dm_id'], 800)

    #invalid token
    with pytest.raises(AccessError):
        dm_messages_v1("dwaedwqa", dm_1['dm_id'], 0)

    with pytest.raises(AccessError):
        dm_messages_v1("I need your time", dm_1['dm_id'], 0)

    #authorised member not in the dm
    with pytest.raises(AccessError):
        dm_messages_v1(users[3]['token'], dm_1['dm_id'], 0)

    with pytest.raises(AccessError):
        dm_messages_v1(users[3]['token'], dm_2['dm_id'], 0)



def test_dm_message_pass(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    message_ids_1 = create_dms['msg_ids'][0]
    message_ids_2 = create_dms['msg_ids'][1]


    messages_1 = dm_messages_v1(users[0]['token'], dm_1['dm_id'], 0)
    end = messages_1['end']
    start = messages_1['start']
    msgs = messages_1['messages']
    assert end == -1
    assert start == 0
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_1[49 - i]['message_id']


    messages_2 = dm_messages_v1(users[0]['token'], dm_2['dm_id'], 0)
    end = messages_2['end']
    start = messages_2['start']
    msgs = messages_2['messages']
    assert end == 50
    assert start == 0
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_2[199 - i]['message_id']
    
    messages_2 = dm_messages_v1(users[0]['token'], dm_2['dm_id'], end)
    end = messages_2['end']
    start = messages_2['start']
    msgs = messages_2['messages']
    assert end == 100
    assert start == 50
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_2[149 - i]['message_id']

    messages_2 = dm_messages_v1(users[0]['token'], dm_2['dm_id'], end)
    end = messages_2['end']
    start = messages_2['start']
    msgs = messages_2['messages']
    assert end == 150
    assert start == 100
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_2[99 - i]['message_id']
    
    messages_2 = dm_messages_v1(users[0]['token'], dm_2['dm_id'], end)
    end = messages_2['end']
    start = messages_2['start']
    msgs = messages_2['messages']
    assert end == -1
    assert start == 150
    for i in range(0, 50):
        assert msgs[i]['message_id'] == message_ids_2[49 - i]['message_id']

