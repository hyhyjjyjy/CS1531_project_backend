from src.auth import auth_register_v2
from src.channel import channel_details_v2, channel_join_v2, channel_invite_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.error import InputError, AccessError
from src.user import user_profile_v2
import pytest

def create_valid_user_data():
    """ Creates and returns a set of valid users.
    """
    user_data = (
        auth_register_v2("ericzheng@mail.com", "peterpiper", "Eric", "Zheng"),
        auth_register_v2("joshhatton@mail.com", "maryreider", "Josh", "Hatton"), 
        auth_register_v2("bunnydong@mail.com", "globalempire4", "Bunny", "Dong"), 
        auth_register_v2("deanzworestine@mail.com", "runescape4lyfe", "Dean", 
                         "Zworestine"), 
        auth_register_v2("jordanmilch@mail.com", "iheartnewyork", "Jordan", 
                         "Milch")
    ) 
    return user_data

def test_invalid_channel_id_exception():
    """ Tests for InputError when Channel ID is passed in as an invalid channel.
    """
    clear_v1()

    user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()
    
    channel = channels_create_v2(user_1['token'], "Silent Fox", True)
    channel_join_v2(user_2['token'], channel['channel_id'])
    channel_join_v2(user_3['token'], channel['channel_id'])
    channel_join_v2(user_4['token'], channel['channel_id'])
    channel_join_v2(user_5['token'], channel['channel_id'])

    with pytest.raises(InputError):
        channel_details_v2(user_1['token'], channel['channel_id'] + 1)
        channel_details_v2(user_2['token'], channel['channel_id'] + 5)
        channel_details_v2(user_3['token'], channel['channel_id'] + 5000)
        channel_details_v2(user_4['token'], channel['channel_id'] - 500)
        channel_details_v2(user_5['token'], channel['channel_id'] + 2)

    clear_v1()
    
def test_invalid_auth_id_exception():
    """ Tests when the authorised user is an invalid id
    """
    clear_v1()

    user = auth_register_v2("mangopineapple@mail.com", "mangofruit1", 
                            "Adam", "Apple")
    channel = channels_create_v2(user['token'], "Valid channel", True)

    with pytest.raises(AccessError):
        channel_details_v2(user['token'] + 'bug', channel['channel_id'])
        channel_details_v2(user['token'] + 'ttopk', channel['channel_id'])
        channel_details_v2(user['token'] + '12312', channel['channel_id'])
        channel_details_v2(user['token'] + '1', channel['channel_id'])
        channel_details_v2(user['token'] + 't324', channel['channel_id'])

    clear_v1()
    
def test_unauthorised_user_exception():
    """ Tests for AccessError when Authorised user is not a member of channel
        with channel_id.
    """
    clear_v1()

    user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()
    channel_1 = channels_create_v2(user_1['token'], "Gang gang", True)
    channel_2 = channels_create_v2(user_2['token'], "Beep boop", True)

    channel_join_v2(user_3['token'], channel_1['channel_id'])

    with pytest.raises(AccessError):
        channel_details_v2(user_3['token'], channel_2['channel_id'])
        channel_details_v2(user_1['token'], channel_2['channel_id'])
        channel_details_v2(user_4['token'], channel_1['channel_id'])
        channel_details_v2(user_5['token'], channel_2['channel_id'])
        channel_details_v2(user_2['token'], channel_1['channel_id'])

    clear_v1()
    
def test_order_of_exceptions():
    """ Tests that the function raises exceptions in the order as assumed. The order
        should be:
        1. AccessError from invalid token
        2. InputError from invalid channel id
        3. AccessError when any of the authorised user is not already part of
           the channel with channel_id
    """
    clear_v1()

    user_1 = auth_register_v2("gdfsgdfg@mail.com", "dfgsdgsdfgdf", "Dum",
                              "Doggo")
    user_2 = auth_register_v2("dummyone@mail.com", "password09123", "Dummy",
                            "Dog")
    channel = channels_create_v2(user_1['token'], "General", True)

    # Pass in invalid channel id, invalid auth id, auth_user who is not part 
    # of the channel. This should raise an access error.
    with pytest.raises(AccessError):
        channel_details_v2(user_2['token'] + 'bug', channel['channel_id'] + 5)

    # Pass in invalid channel id, valid auth id, auth_user who is not part 
    # of the channel. This should raise an input error.
    with pytest.raises(InputError):
        channel_details_v2(user_2['token'], channel['channel_id'] + 5)

    # Pass in valid channel id, valid auth id, auth_user who is not part 
    # of the channel. This should raise an access error.
    with pytest.raises(AccessError):
        channel_details_v2(user_2['token'], channel['channel_id'])

    clear_v1()
    
def test_correct_details():
    """ Tests for successful list of channel details.
    """
    clear_v1()

    user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()
    # Create 3 channels with owners user1, user2 & user3 respectively
    channel_1 = channels_create_v2(user_1['token'], "General", True)
    channel_2 = channels_create_v2(user_2['token'], "Music", True)
    channel_3 = channels_create_v2(user_3['token'], "Study", True)
    
    profile_1 = user_profile_v2(user_1['token'], user_1['auth_user_id'])['user']
    profile_2 = user_profile_v2(user_1['token'], user_2['auth_user_id'])['user']
    profile_3 = user_profile_v2(user_1['token'], user_3['auth_user_id'])['user']
    profile_4 = user_profile_v2(user_1['token'], user_4['auth_user_id'])['user']
    profile_5 = user_profile_v2(user_1['token'], user_5['auth_user_id'])['user']
    
    # User2, user3, user4 & user5 all join channel1
    channel_join_v2(user_2['token'], channel_1['channel_id'])
    channel_join_v2(user_3['token'], channel_1['channel_id'])
    channel_join_v2(user_4['token'], channel_1['channel_id'])
    channel_join_v2(user_5['token'], channel_1['channel_id'])
    # User4 & user5 join channel2
    channel_join_v2(user_4['token'], channel_2['channel_id'])
    channel_join_v2(user_5['token'], channel_2['channel_id'])
    # User1 & User5 join channel3
    channel_join_v2(user_1['token'], channel_3['channel_id'])
    channel_join_v2(user_5['token'], channel_3['channel_id'])
    
    assert channel_details_v2(user_1['token'], channel_1['channel_id']) == {
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
        
    assert channel_details_v2(user_2['token'], channel_2['channel_id']) == {
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
        
    assert channel_details_v2(user_3['token'], channel_3['channel_id']) == {
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
    assert channel_details_v2(user_1['token'], channel_1['channel_id']) == \
           channel_details_v2(user_2['token'], channel_1['channel_id'])
    assert channel_details_v2(user_2['token'], channel_2['channel_id']) == \
           channel_details_v2(user_4['token'], channel_2['channel_id'])
    assert channel_details_v2(user_3['token'], channel_3['channel_id']) == \
           channel_details_v2(user_1['token'], channel_3['channel_id'])
    assert channel_details_v2(user_3['token'], channel_3['channel_id']) == \
           channel_details_v2(user_1['token'], channel_3['channel_id'])
    assert channel_details_v2(user_4['token'], channel_1['channel_id']) == \
           channel_details_v2(user_3['token'], channel_1['channel_id'])
    # Test that channel_details returns different details for users from 
    # different channels
    assert channel_details_v2(user_1['token'], channel_1['channel_id']) != \
           channel_details_v2(user_5['token'], channel_2['channel_id'])
    assert channel_details_v2(user_2['token'], channel_1['channel_id']) != \
           channel_details_v2(user_2['token'], channel_2['channel_id'])
    assert channel_details_v2(user_3['token'], channel_3['channel_id']) != \
           channel_details_v2(user_4['token'], channel_2['channel_id'])
    assert channel_details_v2(user_1['token'], channel_1['channel_id']) != \
           channel_details_v2(user_1['token'], channel_3['channel_id'])
    assert channel_details_v2(user_5['token'], channel_2['channel_id']) != \
           channel_details_v2(user_5['token'], channel_3['channel_id'])
    
    clear_v1()
    
def test_private_channel_details():
    """ Assume channel_details is able to reveal details of private channels 
        as well 
    """
    clear_v1()
    user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()
    channel_1 = channels_create_v2(user_1['token'], "NSFW", False)
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_3['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_4['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_5['auth_user_id'])

    profile_1 = user_profile_v2(user_1['token'], user_1['auth_user_id'])['user']
    profile_2 = user_profile_v2(user_1['token'], user_2['auth_user_id'])['user']
    profile_3 = user_profile_v2(user_1['token'], user_3['auth_user_id'])['user']
    profile_4 = user_profile_v2(user_1['token'], user_4['auth_user_id'])['user']
    profile_5 = user_profile_v2(user_1['token'], user_5['auth_user_id'])['user']


    assert channel_details_v2(user_1['token'], channel_1['channel_id']) == {
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
    
    clear_v1()