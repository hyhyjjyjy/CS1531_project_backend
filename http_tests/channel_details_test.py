import pytest
import requests
from src import config
from http_tests.helper_function_for_http_test import user_profile_v2

SUCCESS = 200
INPUT_ERROR = 400
ACCESS_ERROR = 403

@pytest.fixture
def set_up_server():
    url = config.url
    requests.delete(f"{url}clear/v1")
    return url

def create_valid_user_data(url):
    """ Creates and returns a set of valid users.
    """
    user_data = [
        requests.post(f"{url}auth/register/v2",
         json={'email': 'ericzheng@mail.com', 'password': 'peterpiper', 
               'name_first': 'Eric', 'name_last': 'Zheng'}).json(),
        requests.post(f"{url}auth/register/v2",
         json={'email': 'joshhatton@mail.com', 'password': 'maryreider', 
               'name_first': 'Josh', 'name_last': 'Hatton'}).json(), 
        requests.post(f"{url}auth/register/v2",
         json={'email': 'bunnydong@mail.com', 'password': 'globalempire4', 
               'name_first': 'Bunny', 'name_last': 'Dong'}).json(), 
        requests.post(f"{url}auth/register/v2",
         json={'email': 'deanzworestine@mail.com', 'password': 'runescape4lyfe', 
               'name_first': 'Dean', 'name_last': 'Zworestine'}).json(), 
        requests.post(f"{url}auth/register/v2",
         json={'email': 'jordanmilch@mail.com', 'password': 'iheartnewyork', 
               'name_first': 'Jordan', 'name_last': 'Milch'}).json()
    ]
        
    return user_data
    
def test_invalid_channel_id_exception(set_up_server):
    """ Tests for InputError when Channel ID is passed in as an invalid channel.
    """
    url = set_up_server
    user_1, user_2, user_3, user_4, user_5 = create_valid_user_data(url)

    channel_1 = requests.post(f"{url}channels/create/v2",
                              json={'token': user_1['token'], 'name': 'Silent Fox', 'is_public': True}).json()
    requests.post(f"{url}channel/join/v2", 
                json={'token': user_2['token'], 'channel_id': channel_1['channel_id']})
    requests.post(f"{url}channel/join/v2", 
                json={'token': user_3['token'], 'channel_id': channel_1['channel_id']})
    requests.post(f"{url}channel/join/v2", 
                json={'token': user_4['token'], 'channel_id': channel_1['channel_id']})
    requests.post(f"{url}channel/join/v2", 
                json={'token': user_5['token'], 'channel_id': channel_1['channel_id']})
    
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'], 
             'channel_id': channel_1['channel_id'] + 1}).status_code == INPUT_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_2['token'], 
             'channel_id': channel_1['channel_id'] + 5}).status_code == INPUT_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_3['token'], 
             'channel_id': channel_1['channel_id'] + 5000}).status_code == INPUT_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_4['token'], 
             'channel_id': channel_1['channel_id'] - 500}).status_code == INPUT_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_5['token'], 
             'channel_id': channel_1['channel_id'] + 2}).status_code == INPUT_ERROR
    
    requests.delete(f"{url}clear/v1")

def test_invalid_auth_id_exception(set_up_server):
    """ Tests when the authorised user is an invalid id
    """
    url = set_up_server
    user_1 = requests.post(f"{url}auth/register/v2",
                           json={'email': 'ericzheng@mail.com', 'password': 'peterpiper',
                                 'name_first': 'Eric', 'name_last': 'Zheng'}).json()
    channel_1 = requests.post(f"{url}channels/create/v2",
                              json={'token': user_1['token'], 'name': 'Silent Fox',
                                    'is_public': True}).json()
    
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'] + 'bug',
             'channel_id': channel_1['channel_id']}).status_code == ACCESS_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'] + 'ttopk',
             'channel_id': channel_1['channel_id']}).status_code == ACCESS_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'] + '12312',
             'channel_id': channel_1['channel_id']}).status_code == ACCESS_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'] + '1',
             'channel_id': channel_1['channel_id']}).status_code == ACCESS_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'] + 't324',
             'channel_id': channel_1['channel_id']}).status_code == ACCESS_ERROR

    requests.delete(f"{url}clear/v1")

def test_unauthorised_user_exception(set_up_server):
    """ Tests for AccessError when Authorised user is not a member of channel
        with channel_id.
    """
    url = set_up_server
    user_1, user_2, user_3, user_4, user_5 = create_valid_user_data(url)

    channel_1 = requests.post(f"{url}channels/create/v2",
     json={'token': user_1['token'], 'name': 'Silent Fox', 'is_public': True}).json()
    channel_2 = requests.post(f"{url}channels/create/v2",
     json={'token': user_2['token'], 'name': 'Channel2', 'is_public': True}).json()
    
    requests.post(f"{url}channel/join/v2",
                  json={'token': user_3['token'], 'channel_id': channel_1['channel_id']})
    
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_3['token'], 
             'channel_id': channel_2['channel_id']}).status_code == ACCESS_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'], 
             'channel_id': channel_2['channel_id']}).status_code == ACCESS_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_4['token'], 
             'channel_id': channel_1['channel_id']}).status_code == ACCESS_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_5['token'], 
             'channel_id': channel_2['channel_id']}).status_code == ACCESS_ERROR
    assert requests.get(f"{url}channel/details/v2",
     params={'token': user_2['token'], 
             'channel_id': channel_1['channel_id']}).status_code == ACCESS_ERROR
    
    requests.delete(f"{url}clear/v1")
    
def test_order_of_exceptions(set_up_server):
    """ Tests that the function raises exceptions in the order as assumed. The order
        should be:
        1. AccessError from invalid token
        2. InputError from invalid channel id
        3. AccessError when any of the authorised user is not already part of
           the channel with channel_id
    """
    url = set_up_server
    
    user_1 = requests.post(f"{url}auth/register/v2", json={'email': 'ericzheng@mail.com', 
                                                           'password': 'peterpiper', 
                                                           'name_first': 'Eric', 
                                                           'name_last': 'Zheng'}).json()
    user_2 = requests.post(f"{url}auth/register/v2", json={'email': 'dsasf@mail.com',
                                                           'password': 'asdfaswes',
                                                           'name_first': 'Eric',
                                                           'name_last': 'Madnes'}).json()
    
    channel_1 = requests.post(f"{url}channels/create/v2",
                              json={'token': user_1['token'],
                                    'name': 'Silent Fox', 
                                    'is_public': True}).json()
    
    # Pass in invalid channel id, invalid auth id, auth_user who is not part 
    # of the channel. This should raise an access error.
    assert requests.get(f"{url}channel/details/v2",
                        params={'token': user_2['token'] + 'bug',
                                'channel_id': channel_1['channel_id'] + 5}).status_code == ACCESS_ERROR
    
    # Pass in invalid channel id, valid auth id, auth_user who is not part 
    # of the channel. This should raise an input error.
    assert requests.get(f"{url}channel/details/v2",
                        params={'token': user_2['token'],
                                'channel_id': channel_1['channel_id'] + 5}).status_code == INPUT_ERROR
    
    # Pass in valid channel id, valid auth id, auth_user who is not part 
    # of the channel. This should raise an access error.
    assert requests.get(f"{url}channel/details/v2",
                        params={'token': user_2['token'],
                                'channel_id': channel_1['channel_id']}).status_code == ACCESS_ERROR
    
    requests.delete(f"{url}clear/v1")
    
def test_correct_details(set_up_server):
    """ Tests for successful list of channel details.
    """
    url = set_up_server
    user_1, user_2, user_3, user_4, user_5 = create_valid_user_data(url)
    # Create 3 channels with owners user1, user2 & user3 respectively
    channel_1 = requests.post(f"{url}channels/create/v2", json={'token': user_1['token'],
                                                                 'name': 'General',
                                                                 'is_public': True}).json()
    channel_2 = requests.post(f"{url}channels/create/v2", json={'token': user_2['token'],
                                                                 'name': 'Music',
                                                                 'is_public': True}).json()
    channel_3 = requests.post(f"{url}channels/create/v2", json={'token': user_3['token'],
                                                                 'name': 'Study',
                                                                 'is_public': True}).json()
    
    # User2, user3, user4 & user5 all join channel1
    requests.post(f"{url}channel/join/v2", json={'token': user_2['token'],
     'channel_id': channel_1['channel_id']})
    requests.post(f"{url}channel/join/v2", json={'token': user_3['token'],
     'channel_id': channel_1['channel_id']})
    requests.post(f"{url}channel/join/v2", json={'token': user_4['token'],
     'channel_id': channel_1['channel_id']})
    requests.post(f"{url}channel/join/v2", json={'token': user_5['token'],
     'channel_id': channel_1['channel_id']})
    # User4 & user5 join channel2
    requests.post(f"{url}channel/join/v2", json={'token': user_4['token'],
                                                 'channel_id': channel_2['channel_id']})
    requests.post(f"{url}channel/join/v2", json={'token': user_5['token'],
                                                 'channel_id': channel_2['channel_id']})
    # User1 & User5 join channel3
    requests.post(f"{url}channel/join/v2", json={'token': user_1['token'],
                                                 'channel_id': channel_3['channel_id']})
    requests.post(f"{url}channel/join/v2", json={'token': user_5['token'],
                                                 'channel_id': channel_3['channel_id']})
    
    profile_1 = user_profile_v2(user_1['token'], user_1['auth_user_id']).json()['user']
    profile_2 = user_profile_v2(user_1['token'], user_2['auth_user_id']).json()['user']
    profile_3 = user_profile_v2(user_1['token'], user_3['auth_user_id']).json()['user']
    profile_4 = user_profile_v2(user_1['token'], user_4['auth_user_id']).json()['user']
    profile_5 = user_profile_v2(user_1['token'], user_5['auth_user_id']).json()['user']
    
    
    assert requests.get(f"{url}channel/details/v2",
                        params={'token': user_1['token'], 'channel_id': channel_1['channel_id']}).json() == {
        'name': 'General',
        'owner_members': [
            {
                'u_id': user_1['auth_user_id'],     
                'name_first': 'Eric',
                'name_last': 'Zheng',
                'email': 'ericzheng@mail.com',
                'handle_str': 'ericzheng',
                'profile_img_url' : profile_1['profile_img_url'],
            }
        ],
        'all_members': [
            {
                'u_id': user_1['auth_user_id'],
                'name_first': 'Eric',
                'name_last': 'Zheng',
                'email': 'ericzheng@mail.com',
                'handle_str': 'ericzheng',
                'profile_img_url' : profile_1['profile_img_url'],

            },
            {
                'u_id': user_2['auth_user_id'],
                'name_first': 'Josh',
                'name_last': 'Hatton',
                'email': 'joshhatton@mail.com',
                'handle_str': 'joshhatton',
                'profile_img_url' : profile_2['profile_img_url'],

            },
            {
                'u_id': user_3['auth_user_id'],
                'name_first': 'Bunny',
                'name_last': 'Dong',
                'email': 'bunnydong@mail.com',
                'handle_str': 'bunnydong',
                'profile_img_url' : profile_3['profile_img_url'],

            },
            {
                'u_id': user_4['auth_user_id'],
                'name_first': 'Dean',
                'name_last': 'Zworestine',
                'email': 'deanzworestine@mail.com',
                'handle_str': 'deanzworestine',
                'profile_img_url' : profile_4['profile_img_url'],

            },
            {
                'u_id': user_5['auth_user_id'],
                'name_first': 'Jordan',
                'name_last': 'Milch',
                'email': 'jordanmilch@mail.com',
                'handle_str': 'jordanmilch',
                'profile_img_url' : profile_5['profile_img_url'],

            }
        ],
    }

    assert requests.get(f"{url}channel/details/v2",
                        params={'token': user_2['token'], 'channel_id': channel_2['channel_id']}).json() == {
        'name': 'Music',
        'owner_members': [
            {
                'u_id': user_2['auth_user_id'],
                'name_first': 'Josh',
                'name_last': 'Hatton',
                'email': 'joshhatton@mail.com',
                'handle_str': 'joshhatton',
                'profile_img_url' : profile_2['profile_img_url'],

            }
        ],
        'all_members': [
            {
                'u_id': user_2['auth_user_id'],
                'name_first': 'Josh',
                'name_last': 'Hatton',
                'email': 'joshhatton@mail.com',
                'handle_str': 'joshhatton',
                'profile_img_url' : profile_2['profile_img_url'],
            },
            {
                'u_id': user_4['auth_user_id'],
                'name_first': 'Dean',
                'name_last': 'Zworestine',
                'email': 'deanzworestine@mail.com',
                'handle_str': 'deanzworestine',
                'profile_img_url' : profile_4['profile_img_url'],

            },
            {
                'u_id': user_5['auth_user_id'],
                'name_first': 'Jordan',
                'name_last': 'Milch',
                'email': 'jordanmilch@mail.com',
                'handle_str': 'jordanmilch',
                'profile_img_url' : profile_5['profile_img_url'],

            },
        ],
    }
    
    assert requests.get(f"{url}channel/details/v2",
                        params={'token': user_3['token'], 'channel_id': channel_3['channel_id']}).json() == {
        'name': 'Study',
        'owner_members': [
            {
                'u_id': user_3['auth_user_id'],
                'name_first': 'Bunny',
                'name_last': 'Dong',
                'email': 'bunnydong@mail.com',
                'handle_str': 'bunnydong',
                'profile_img_url' : profile_3['profile_img_url'],
            }
        ],
        'all_members': [
            {
                'u_id': user_3['auth_user_id'],
                'name_first': 'Bunny',
                'name_last': 'Dong',
                'email': 'bunnydong@mail.com',
                'handle_str': 'bunnydong',
                'profile_img_url' : profile_3['profile_img_url'],
            },
            {
                'u_id': user_1['auth_user_id'],
                'name_first': 'Eric',
                'name_last': 'Zheng',
                'email': 'ericzheng@mail.com',
                'handle_str': 'ericzheng',
                'profile_img_url' : profile_1['profile_img_url'],
            },
            {
                'u_id': user_5['auth_user_id'],
                'name_first': 'Jordan',
                'name_last': 'Milch',
                'email': 'jordanmilch@mail.com',
                'handle_str': 'jordanmilch',
                'profile_img_url' : profile_5['profile_img_url'],

           },
        ],
     }
    
    # Test that channel_details returns the same details for different users in 
    # the same channel.
    resp_1 = requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'], 'channel_id': channel_1['channel_id']}).json()
    resp_2 = requests.get(f"{url}channel/details/v2",
     params={'token': user_2['token'], 'channel_id': channel_1['channel_id']}).json()
    assert resp_1 == resp_2
    
    # Test that channel_details returns different details for users from 
    # different channels
    resp_1 = requests.get(f"{url}channel/details/v2",
     params={'token': user_1['token'], 'channel_id': channel_1['channel_id']}).json()
    resp_2 = requests.get(f"{url}channel/details/v2",
     params={'token': user_5['token'], 'channel_id': channel_2['channel_id']}).json()
    assert resp_1 != resp_2
    
    requests.delete(f"{url}clear/v1")

def test_private_channel_details(set_up_server):
    """ Assume channel_details is able to reveal details of private channels 
        as well 
    """
    url = set_up_server
    user_1, user_2, user_3, user_4, user_5 = create_valid_user_data(url)
    
    channel_1 = requests.post(f"{url}channels/create/v2", json={'token': user_1['token'],
                                                                'name': 'NSFW',
                                                                'is_public': False}).json()
    requests.post(f"{url}channel/invite/v2", json={'token': user_1['token'],
                                                     'channel_id': channel_1['channel_id'],
                                                     'u_id': user_2['auth_user_id']})
    requests.post(f"{url}channel/invite/v2", json={'token': user_1['token'],
                                                     'channel_id': channel_1['channel_id'],
                                                     'u_id': user_3['auth_user_id']})
    requests.post(f"{url}channel/invite/v2", json={'token': user_1['token'],
                                                     'channel_id': channel_1['channel_id'], 
                                                     'u_id': user_4['auth_user_id']})
    requests.post(f"{url}channel/invite/v2", json={'token': user_1['token'],
                                                     'channel_id': channel_1['channel_id'],
                                                     'u_id': user_5['auth_user_id']})
    
    profile_1 = user_profile_v2(user_1['token'], user_1['auth_user_id']).json()['user']
    profile_2 = user_profile_v2(user_1['token'], user_2['auth_user_id']).json()['user']
    profile_3 = user_profile_v2(user_1['token'], user_3['auth_user_id']).json()['user']
    profile_4 = user_profile_v2(user_1['token'], user_4['auth_user_id']).json()['user']
    profile_5 = user_profile_v2(user_1['token'], user_5['auth_user_id']).json()['user']    
    
    assert requests.get(f"{url}channel/details/v2", params={'token': user_1['token'],
                                                            'channel_id': channel_1['channel_id']}).json() == {
        'name': 'NSFW',
        'owner_members': [
            {
                'u_id': user_1['auth_user_id'],
                'name_first': 'Eric',
                'name_last': 'Zheng',
                'email': 'ericzheng@mail.com',
                'handle_str': 'ericzheng',
                'profile_img_url' : profile_1['profile_img_url'],

            }
        ],
        'all_members': [
            {
                'u_id': user_1['auth_user_id'],
                'name_first': 'Eric',
                'name_last': 'Zheng',
                'email': 'ericzheng@mail.com',
                'handle_str': 'ericzheng',
                'profile_img_url' : profile_1['profile_img_url'],

            },
            {
                'u_id': user_2['auth_user_id'],
                'name_first': 'Josh',
                'name_last': 'Hatton',
                'email': 'joshhatton@mail.com',
                'handle_str': 'joshhatton',
                'profile_img_url' : profile_2['profile_img_url'],

            },
            {
                'u_id': user_3['auth_user_id'],
                'name_first': 'Bunny',
                'name_last': 'Dong',
                'email': 'bunnydong@mail.com',
                'handle_str': 'bunnydong',
                'profile_img_url' : profile_3['profile_img_url'],

            },
            {
                'u_id': user_4['auth_user_id'],
                'name_first': 'Dean',
                'name_last': 'Zworestine',
                'email': 'deanzworestine@mail.com',
                'handle_str': 'deanzworestine',
                'profile_img_url' : profile_4['profile_img_url'],

            },
            {
                'u_id': user_5['auth_user_id'],
                'name_first': 'Jordan',
                'name_last': 'Milch',
                'email': 'jordanmilch@mail.com',
                'handle_str': 'jordanmilch',
                'profile_img_url' : profile_5['profile_img_url'],

            }
        ],
    }
    
    requests.delete(f"{url}clear/v1")
