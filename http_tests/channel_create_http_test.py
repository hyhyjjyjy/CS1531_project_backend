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

def test_create_channel_invalid_input():
    clear_v1()
    user1 = auth_register_v2("bunnydongao@gmail.com","abcdefg1234", "bunny", "dong").json()

    assert channels_create_v2(user1['token'], "dadfewfwefewfewfewfewfewfewfew", True).status_code == INPUT_ERROR
    assert channels_create_v2(user1['token'], "fwefwewfewfwefefweefwefewfefwe", False).status_code == INPUT_ERROR
    assert channels_create_v2(user1['token'], "A very very very very very long channel", True).status_code == INPUT_ERROR

    assert channels_create_v2(2.5, "fwegertgre", True).status_code == ACCESS_ERROR
    assert channels_create_v2(3.5, "oiefnweifpof", False).status_code == ACCESS_ERROR    

def test_create_channel_successfully():
    clear_v1()
    u1 = auth_register_v2("bunnydongao@gmail.com","abcdefg1234", "bunny", "dong").json()
    u2 = auth_register_v2("jamesdongao@gmail.com","abcdefg1234", "bunny", "dong").json()
    u3 = auth_register_v2("Mikedongao@gmail.com","abcdefg1234", "abcdef", "fwef").json()

    channel_1 = channels_create_v2(u1['token'], "The party channel 1", True).json()['channel_id']
    assert(channels_listall_v2(u1['token']).json() == {'channels' : [{'channel_id': channel_1, 'name': "The party channel 1",},]})
    
    channel_2 = channels_create_v2(u2['token'], "The party channel 2", True).json()['channel_id']

    assert(channels_listall_v2(u1['token']).json() == {'channels' : [{'channel_id': channel_1, 'name': "The party channel 1",},
                                      {'channel_id': channel_2, 'name': "The party channel 2",},]})

    channel_3 = channels_create_v2(u3['token'], "The party channel 3", True).json()['channel_id']

    assert(channels_listall_v2(u1['token']).json() == {'channels' : [{'channel_id': channel_1, 'name': "The party channel 1",},
                                      {'channel_id': channel_2, 'name': "The party channel 2",},
                                      {'channel_id': channel_3, 'name': "The party channel 3",},]})