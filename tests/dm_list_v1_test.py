import pytest
import requests
import json
from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1
from src.dms import dm_create_v1, dm_details_v1, dm_list_v1
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

def test_dm_list_errors(create_dms):

    #invalid token
    with pytest.raises(AccessError):
        dm_list_v1("fdewffe")

    with pytest.raises(AccessError):
        dm_list_v1("afsedf")
    
    clear_v1()




def test_dm_list(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    dm_3 = create_dms['dms'][2]

    rt_val_1 = dm_list_v1(users[0]['token'])
    rt_val_2 = dm_list_v1(users[1]['token'])
    rt_val_3 = dm_list_v1(users[2]['token'])
    rt_val_4 = dm_list_v1(users[3]['token'])


    assert sorted(rt_val_1['dms'], key=lambda x:x['dm_id']) == sorted([
                            {  'dm_id': dm_1['dm_id'],
                               'name': dm_1['dm_name'],
                            },
                            {  'dm_id': dm_2['dm_id'],
                               'name': dm_2['dm_name'],
                            },
                            {  'dm_id': dm_3['dm_id'],
                               'name': dm_3['dm_name'],
                            },
                            ], key=lambda x:x['dm_id'])



    assert sorted(rt_val_2['dms'], key=lambda x:x['dm_id']) == sorted([
                            {  'dm_id': dm_1['dm_id'],
                               'name': dm_1['dm_name'],
                            },
                            {  'dm_id': dm_2['dm_id'],
                               'name': dm_2['dm_name'],
                            },
                            {  'dm_id': dm_3['dm_id'],
                               'name': dm_3['dm_name'],
                            },
                            ], key=lambda x:x['dm_id'])


    assert sorted(rt_val_3['dms'], key=lambda x:x['dm_id']) == sorted([
                            {  'dm_id': dm_1['dm_id'],
                               'name': dm_1['dm_name'],
                            },
                            {  'dm_id': dm_3['dm_id'],
                               'name': dm_3['dm_name'],
                            },
                            ], key=lambda x:x['dm_id'])

    assert sorted(rt_val_4['dms'], key=lambda x:x['dm_id']) == sorted([
                            {  'dm_id': dm_3['dm_id'],
                               'name': dm_3['dm_name'],
                            },
                            ], key=lambda x:x['dm_id'])
   
    clear_v1()