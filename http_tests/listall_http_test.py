import pytest
import requests
from src import config

#####
#Helper Functions
#####

SUCCESS = 200
INPUT_ERROR = 400
ACCESS_ERROR = 403

def clear_v1():
    url = config.url
    return requests.delete(f"{url}clear/v1")

def auth_register_v2(email, password, name_first, name_last):
    url = config.url
    return requests.post(f"{url}auth/register/v2", json={'email': email, 'password': password, 'name_first': name_first, 'name_last': name_last})

def channels_listall_v2(token):
    url = config.url
    return requests.get(f"{url}channels/listall/v2", params={'token': token})    

def channels_create_v2(token, name, is_public):
    url = config.url
    return requests.post(f"{url}channels/create/v2", json={'token': token, 'name': name, 'is_public': is_public})

def channel_invite_v2(token, channel_id, u_id):
    url = config.url
    return requests.post(f"{url}channel/invite/v2", json={'token': token, 'channel_id': channel_id, 'u_id': u_id})

# Tests an empty list - where there are no channels
def test_empty():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa1', 'a', 'a').json()
    assert channels_listall_v2(user_1['token']).json() == {'channels' : []}
    
# Tests one channel with the user part of that channel
def test_single_channel_including_user():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa1', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    assert channels_listall_v2(user_1['token']).json() == {'channels' : [{'channel_id': channel_1['channel_id'],
                                             'name': 'Channel 1'}]}
    
# Tests one channel with the user not part of that channel
def test_single_channel_excluding_user():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa1', 'a', 'a').json()
    user_2 = auth_register_v2('bb@b.com', 'bbbbbb1', 'b', 'b').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    assert channels_listall_v2(user_2['token']).json() == {'channels' : [{'channel_id': channel_1['channel_id'],
                                             'name': 'Channel 1'}]}

# Tests a range of channels with different permissions and checks that everyone gets the same list containing all channels
def test_multiple_channels_different_permissions():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa1', 'a', 'a').json()
    user_2 = auth_register_v2('bb@b.com', 'bbbbbb1', 'b', 'b').json()
    user_3 = auth_register_v2('cb@c.com', 'aaaaaa1', 'a', 'a').json()
    user_4 = auth_register_v2('db@d.com', 'bbbbbb1', 'b', 'b').json()
    user_5 = auth_register_v2('eb@e.com', 'aaaaaa1', 'a', 'a').json()
    user_6 = auth_register_v2('fb@f.com', 'bbbbbb1', 'b', 'b').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_2 = channels_create_v2(user_2['token'], 'Channel 2', True).json()
    channel_3 = channels_create_v2(user_3['token'], 'Channel 3', False).json()
    channel_4 = channels_create_v2(user_4['token'], 'Channel 4', False).json()
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_5['auth_user_id'])
    assert channels_listall_v2(user_1['token']).json() == {'channels' : [{'channel_id': channel_1['channel_id'],
                                            'name': 'Channel 1'},
                                           {'channel_id': channel_2['channel_id'],
                                            'name': 'Channel 2'},
                                           {'channel_id': channel_3['channel_id'],
                                            'name': 'Channel 3'},
                                           {'channel_id': channel_4['channel_id'],
                                            'name': 'Channel 4'}]}
    assert channels_listall_v2(user_1['token']).json() == channels_listall_v2(user_2['token']).json()
    assert channels_listall_v2(user_1['token']).json() == channels_listall_v2(user_3['token']).json()
    assert channels_listall_v2(user_1['token']).json() == channels_listall_v2(user_4['token']).json()
    assert channels_listall_v2(user_1['token']).json() == channels_listall_v2(user_5['token']).json() 
    assert channels_listall_v2(user_1['token']).json() == channels_listall_v2(user_6['token']).json()