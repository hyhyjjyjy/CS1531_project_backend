import pytest
import requests
import json
from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1
from src.dms import dm_create_v1, dm_details_v1
from src.error import InputError, AccessError
from src.user import user_profile_v2


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


def test_dm_details_errors(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    #dm_3 = create_dms['dms'][2]

    with pytest.raises(InputError):
        dm_details_v1(users[0]['token'], 100)

    with pytest.raises(InputError):
        dm_details_v1(users[0]['token'], 500)

    with pytest.raises(AccessError):
        dm_details_v1(users[3]['token'], dm_1['dm_id'])

    with pytest.raises(AccessError):
        dm_details_v1(users[3]['token'], dm_2['dm_id'])
    
    with pytest.raises(AccessError):
        dm_details_v1(users[2]['token'], dm_2['dm_id'])
    
    with pytest.raises(AccessError):
        dm_details_v1("fewfwfe", dm_1['dm_id'])
    
    clear_v1()


def test_dm_details(create_dms):
    users = create_dms['users']
    dm_1 = create_dms['dms'][0]
    dm_2 = create_dms['dms'][1]
    dm_3 = create_dms['dms'][2]

    profile_0 = user_profile_v2(users[0]['token'], users[0]['auth_user_id'])['user']
    profile_1 = user_profile_v2(users[0]['token'], users[1]['auth_user_id'])['user']
    profile_2 = user_profile_v2(users[0]['token'], users[2]['auth_user_id'])['user']
    profile_3 = user_profile_v2(users[0]['token'], users[3]['auth_user_id'])['user']


    rt_val_1 = dm_details_v1(users[0]['token'], dm_1['dm_id'])
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