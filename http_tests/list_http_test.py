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

def channels_list_v2(token):
    url = config.url
    return requests.get(f"{url}channels/list/v2", params={'token': token})    

def channels_create_v2(token, name, is_public):
    url = config.url
    return requests.post(f"{url}channels/create/v2", json={'token': token, 'name': name, 'is_public': is_public})

def channel_invite_v2(token, channel_id, u_id):
    url = config.url
    return requests.post(f"{url}channel/invite/v2", json={'token': token, 'channel_id': channel_id, 'u_id': u_id})

# Tests the empty case where a user is not part of any channel
def test_empty_list():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    assert channels_list_v2(user_1['token']).json() == {'channels' : []}
    clear_v1()

# Tests a single case where the user is part of only one channel and only 
# one channel exists
def test_single_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    assert channels_list_v2(user_1['token']).json() == {'channels' : [{'channel_id': channel_1['channel_id'],
                                        'name': 'Channel 1'}]}
    clear_v1()

# Tests a single case again but the user is not part of the channel
def test_non_member_single_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('bb@b.com', 'bbbbbb', 'b', 'b').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    assert channels_list_v2(user_2['token']).json() == {'channels' : []}
    assert channels_list_v2(user_1['token']).json() == {'channels' : [{'channel_id': channel_1['channel_id'],
                                        'name': 'Channel 1'}]}
    clear_v1()

# Adds a user to multiple channels with varying permissions and ensures 
# all the channels are displayed 
def test_multiple_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', False).json()
    channel_3 = channels_create_v2(user_1['token'], 'Channel 3', True).json()
    assert channels_list_v2(user_1['token']).json() == {'channels' : [{'channel_id': channel_1['channel_id'],
                                         'name': 'Channel 1'},
                                        {'channel_id': channel_2['channel_id'],
                                         'name': 'Channel 2'},
                                        {'channel_id': channel_3['channel_id'],
                                         'name': 'Channel 3'}]}
    clear_v1()

# Creates multiple channels with differing permissions and adds a user to 
# only a few of them
def test_mix_channels():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('bb@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', True).json()
    channel_3 = channels_create_v2(user_1['token'], 'Channel 3', False).json()
    channel_4 = channels_create_v2(user_1['token'], 'Channel 4', False).json()
    channel_5 = channels_create_v2(user_1['token'], 'Channel 5', True).json()
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_3['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_5['channel_id'], user_2['auth_user_id'])
    assert channels_list_v2(user_1['token']).json() == {'channels' : [{'channel_id': channel_1['channel_id'],
                                         'name': 'Channel 1'},
                                        {'channel_id': channel_2['channel_id'],
                                         'name': 'Channel 2'},
                                        {'channel_id': channel_3['channel_id'],
                                         'name': 'Channel 3'},
                                        {'channel_id': channel_4['channel_id'],
                                         'name': 'Channel 4'},
                                        {'channel_id': channel_5['channel_id'],
                                         'name': 'Channel 5'}]}  
    assert channels_list_v2(user_2['token']).json() == {'channels' : [{'channel_id': channel_1['channel_id'],
                                         'name': 'Channel 1'},
                                        {'channel_id': channel_3['channel_id'],
                                         'name': 'Channel 3'},
                                        {'channel_id': channel_5['channel_id'],
                                         'name': 'Channel 5'}]}    
    clear_v1()