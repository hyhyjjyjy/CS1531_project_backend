import pytest
import requests
import json
from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1
from src.dms import dm_create_v1, dm_details_v1, dm_remove_v1
from src.error import InputError, AccessError



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



    return {'users': users,
            'dms': [dm_1, dm_2, dm_3]}


def test_dm_remove_errors(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    dm_3 = create_dms['dms'][2]

    with pytest.raises(InputError):
        dm_remove_v1(users[0]['token'], 100)
        
    with pytest.raises(InputError):
        dm_remove_v1(users[1]['token'], 100)   

    with pytest.raises(AccessError):
        dm_remove_v1(users[1]['token'], dm_1['dm_id'])

    with pytest.raises(AccessError):
        dm_remove_v1(users[3]['token'], dm_2['dm_id'])

    with pytest.raises(AccessError):
        dm_remove_v1(users[1]['token'], dm_3['dm_id'])

    #invalid token
    with pytest.raises(AccessError):
        dm_remove_v1("fwsef", dm_3['dm_id'])
    with pytest.raises(AccessError):
        dm_remove_v1("afgde", dm_3['dm_id'])
    with pytest.raises(AccessError):
        dm_remove_v1("435vsrf", dm_3['dm_id'])
    
    clear_v1()
    


def test_dm_remove(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    dm_3 = create_dms['dms'][2]

    dm_details_v1(users[0]['token'], dm_1['dm_id'])
    dm_remove_v1(users[0]['token'], dm_1['dm_id'])
    with pytest.raises(InputError):
        dm_details_v1(users[0]['token'], dm_1['dm_id'])

    dm_details_v1(users[1]['token'], dm_2['dm_id'])
    dm_remove_v1(users[1]['token'], dm_2['dm_id'])
    with pytest.raises(InputError):
        dm_details_v1(users[1]['token'], dm_2['dm_id'])
    
    dm_details_v1(users[3]['token'], dm_3['dm_id'])
    dm_remove_v1(users[3]['token'], dm_3['dm_id'])
    with pytest.raises(InputError):
        dm_details_v1(users[3]['token'], dm_3['dm_id'])
    
    clear_v1()