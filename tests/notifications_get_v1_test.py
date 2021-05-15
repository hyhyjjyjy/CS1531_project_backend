from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_invite_v2, channel_details_v2, channel_addowner_v1
from src.channels import channels_create_v2
from src.dms import dm_create_v1, dm_invite_v1
from src.message import message_send_v2, message_senddm_v1, message_react_v1, message_share_v1, message_edit_v2, message_sendlaterdm_v1, message_sendlater_v1
from src.notifications import notifications_get_v1
from src.user import user_profile_v2
from src.other import clear_v1
from src.error import AccessError
import pytest
import time

@pytest.fixture
def create_input():
    clear_v1()
    
    data_test_users = [
        auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng"),
        auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton"),
        auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong"),
        auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch"),
        auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine"),
    ]
    
    data_test_users_handles = [
        user_profile_v2(data_test_users[0]['token'], data_test_users[0]['auth_user_id']),
        user_profile_v2(data_test_users[0]['token'], data_test_users[1]['auth_user_id']),
        user_profile_v2(data_test_users[0]['token'], data_test_users[2]['auth_user_id']),
        user_profile_v2(data_test_users[0]['token'], data_test_users[3]['auth_user_id']),
        user_profile_v2(data_test_users[0]['token'], data_test_users[4]['auth_user_id']),
    ]
    
    # user 1 is owner of channel 1
    # user 2 is owner of channel 2
    # user 3 is owner of channel 3 (private channel)
    data_test_channels = [
        channels_create_v2(data_test_users[0]['token'], 'Channel 1', True),
        channels_create_v2(data_test_users[1]['token'], 'Channel 2', True),
        channels_create_v2(data_test_users[2]['token'], 'Private', False)    
    ]
    
    # user 1 has dm with user 2 in dm 1
    # user 3 has dm with user 4 in dm2
    # user 5 has dm with user 2 in dm3
    data_test_dms = [
        dm_create_v1(data_test_users[0]['token'], [data_test_users[1]['auth_user_id']]),
        dm_create_v1(data_test_users[2]['token'], [data_test_users[3]['auth_user_id']]),
        dm_create_v1(data_test_users[4]['token'], [data_test_users[1]['auth_user_id']])
    ]
    
    data_test_messages = [
        f"Hello @{data_test_users_handles[0]}, how are you on such a fine lovely day? I hope you are well!",
        f"Hello @{data_test_users_handles[1]}, can you send me homework answers from yesterday please? Thanks!",
        f"Hello @{data_test_users_handles[2]}, I heard that your knees are the finest knees in all of Australia, is this true?",
        f"@{data_test_users_handles[3]} is cool.",
        f"@{data_test_users_handles[4]} is a donkey.",
        f"@{data_test_users_handles[2]} is an even bigger donkey than @{data_test_users_handles[4]}"
    ]

    return [data_test_users, data_test_users_handles, data_test_channels, data_test_dms, data_test_messages]


def test_simple_tag():
    clear_v1()
    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    
    message_1 = "@ericzheng, how are you doing today?"
    
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_join_v2(user_2['token'], channel_1['channel_id'])
    message_send_v2(user_2['token'], channel_1['channel_id'], message_1)
    
    assert notifications_get_v1(user_1['token']) == {
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"joshhatton tagged you in Channel 1: {message_1[0:20]}"
            }
        ]
    } 
        
def test_channel_tagged_user(create_input):
    """ Tests correct return of notifications when user is tagged in a channel.
    """
    user_1, user_2, user_3, user_4, user_5 = create_input[0]
    
    user_1_handle = create_input[1][0]
    user_2_handle = create_input[1][1]
    user_3_handle = create_input[1][2]
    user_4_handle = create_input[1][3]
    user_5_handle = create_input[1][4]

    
    channel_1, channel_2, channel_3 = create_input[2]
    
    message_1 = f"@{user_1_handle['user']['handle_str']}, how are you on such a fine lovely day? I hope you are well!"
    message_2 = f"@{user_2_handle['user']['handle_str']}, can you send me homework answers from yesterday please? Thanks!"
    message_3 = f"@{user_3_handle['user']['handle_str']}, I heard that your knees are the finest knees in all of Australia, is this true?"
    message_4 = f"@{user_4_handle['user']['handle_str']} is cool."
    message_5 = f"@{user_5_handle['user']['handle_str']} is a donkey."
    message_6 = f"@{user_3_handle['user']['handle_str']} is an even bigger donkey than @{user_4_handle['user']['handle_str']}"
        
    dm_1, dm_2, dm_3 = create_input[3]
    
    channel_join_v2(user_2['token'], channel_1['channel_id'])
    channel_join_v2(user_3['token'], channel_1['channel_id'])
    channel_join_v2(user_4['token'], channel_1['channel_id'])
    channel_join_v2(user_4['token'], channel_2['channel_id'])
    channel_join_v2(user_5['token'], channel_2['channel_id'])
    channel_join_v2(user_1['token'], channel_3['channel_id'])
    
    message_send_v2(user_1['token'], channel_1['channel_id'], message_2)
    message_send_v2(user_1['token'], channel_1['channel_id'], message_3)
    message_send_v2(user_2['token'], channel_2['channel_id'], message_4)
    message_send_v2(user_2['token'], channel_2['channel_id'], message_5)
    message_send_v2(user_3['token'], channel_1['channel_id'], message_1)
    message_send_v2(user_1['token'], channel_1['channel_id'], message_6)
    
    
    assert notifications_get_v1(user_2['token']) == {
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Channel 1: {message_2[0:20]}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_3['dm_id'],
                'notification_message': f"{user_5_handle['user']['handle_str']} added you to {dm_3['dm_name']}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_1['dm_id'],
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to {dm_1['dm_name']}"
            }
        ]
    }
    
    assert notifications_get_v1(user_3['token']) == {
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Channel 1: {message_6[0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Channel 1: {message_3[0:20]}"
            },
        ]
    }
    
    assert notifications_get_v1(user_4['token']) == {
        
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Channel 1: {message_6[0:20]}"
            
            },
            
            {
            
                'channel_id': channel_2['channel_id'],
                'dm_id': -1,    
                'notification_message': f"{user_2_handle['user']['handle_str']} tagged you in Channel 2: {message_4[0:20]}"    
            },
            
            {    
                'channel_id': -1,    
                'dm_id': dm_2['dm_id'],    
                'notification_message': f"{user_3_handle['user']['handle_str']} added you to {dm_2['dm_name']}"    
            }
        
        ]
        
    }
        
    assert notifications_get_v1(user_5['token']) == {
            'notifications': [
                {
                    'channel_id' : channel_2['channel_id'],
                    'dm_id': -1,
                    'notification_message': f"{user_2_handle['user']['handle_str']} tagged you in Channel 2: {message_5[0:20]}"
                }
            ]
    }
    
def test_dm_tagged_user(create_input):
    """ Tests correct returns of notifications when user is tagged in a dm
    """
    user_1, user_2, user_3, user_4, user_5 = create_input[0]
    
    user_1_handle = create_input[1][0]
    user_2_handle = create_input[1][1]
    user_3_handle = create_input[1][2]
    user_4_handle = create_input[1][3]
    user_5_handle = create_input[1][4]
    
    dm_1, dm_2, dm_3 = create_input[3]
        
    message_2 = f"@{user_2_handle['user']['handle_str']}, can you send me homework answers from yesterday please? Thanks!"
    message_4 = f"@{user_4_handle['user']['handle_str']} is cool."
    
    message_senddm_v1(user_1['token'], dm_1['dm_id'], message_2)
    message_senddm_v1(user_3['token'], dm_2['dm_id'], message_4)
    message_senddm_v1(user_5['token'], dm_3['dm_id'], message_2)
    
    assert notifications_get_v1(user_2['token']) == {
        'notifications': [
            {  
                'channel_id': -1,
                'dm_id': dm_3['dm_id'],
                'notification_message': f"{user_5_handle['user']['handle_str']} tagged you in {dm_3['dm_name']}: {message_2[0:20]}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_1['dm_id'],
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in {dm_1['dm_name']}: {message_2[0:20]}"
            },
            {   
                'channel_id': -1,
                'dm_id': dm_3['dm_id'],
                'notification_message': f"{user_5_handle['user']['handle_str']} added you to {dm_3['dm_name']}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_1['dm_id'],
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to {dm_1['dm_name']}"
            }
        ]
    }
    
    assert notifications_get_v1(user_4['token']) == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': dm_2['dm_id'],
                'notification_message': f"{user_3_handle['user']['handle_str']} tagged you in {dm_2['dm_name']}: {message_4[0:20]}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_2['dm_id'],
                'notification_message': f"{user_3_handle['user']['handle_str']} added you to {dm_2['dm_name']}"
            }
        ]
    }

def test_no_notifications():
    """ Assume that notifications_get_v1 returns an empty dictionary of list
        when there are no notifiactions to display
    """
    clear_v1()
    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    user_3 = auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong")
    user_4 = auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch")
    user_5 = auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine")
    
    assert notifications_get_v1(user_1['token']) == {'notifications': []}
    assert notifications_get_v1(user_2['token']) == {'notifications': []}
    assert notifications_get_v1(user_3['token']) == {'notifications': []}
    assert notifications_get_v1(user_4['token']) == {'notifications': []}
    assert notifications_get_v1(user_5['token']) == {'notifications': []}

def test_invalid_token():
    """ Tests return of expected output when given a token that doesn't exist,
        or if the user is not in the channel/dm.
    """
    clear_v1()
    # Token doesnt exist
    user_1 = auth_register_v2('ericzheng@gmail.com', 'happydays1', 'Eric', 'Zheng')
    
    with pytest.raises(AccessError):
        notifications_get_v1(user_1['token'] + 'bug') 
        
    # User not in channel
    user_2 = auth_register_v2('joshhatton@gmail.com', 'happydays2', 'Josh', 'Hatton')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    
    user_2_handle = user_profile_v2(user_1['token'], user_2['auth_user_id'])
    
    message_send_v2(user_1['token'], channel_1['channel_id'], f"Hi @{user_2_handle['user']['handle_str']}")
    
    assert notifications_get_v1(user_2['token']) == {'notifications': []}
    
    # User not in dm
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    user_3 = auth_register_v2('bunnydong@gmail.com', 'hihihi!!!', 'Bunny', 'Dong')
    user_3_handle = user_profile_v2(user_1['token'], user_3['auth_user_id'])
    
    message_senddm_v1(user_1['token'], dm_1['dm_id'], f"Hello @{user_3_handle['user']['handle_str']}")
    
    assert notifications_get_v1(user_3['token']) == {'notifications': []}
    
def test_added_to_channel(create_input):
    """ Tests the expected return value when a user is added to a channel
    """
    user_1, user_2, user_3, user_4, user_5 = create_input[0]
    user_1_handle, _, user_3_handle, _, user_5_handle = create_input[1]

    channel_1 = create_input[2][0]
    dm_1, dm_2, dm_3 = create_input[3]
    
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_3['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_4['auth_user_id'])
    
    # Also test for channel_addowner
    channel_addowner_v1(user_1['token'], channel_1['channel_id'], user_5['auth_user_id'])
    

    assert notifications_get_v1(user_2['token']) == {
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to Channel 1"
            },
            {
                'channel_id': -1,
                'dm_id': dm_3['dm_id'],
                'notification_message': f"{user_5_handle['user']['handle_str']} added you to {dm_3['dm_name']}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_1['dm_id'],
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to {dm_1['dm_name']}"
            }
        ]
    }
    assert notifications_get_v1(user_3['token']) == {
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to Channel 1"
            }
        ]
    }
    assert notifications_get_v1(user_4['token']) == {
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to Channel 1"
            },
            {
                'channel_id': -1,
                'dm_id': dm_2['dm_id'],
                'notification_message': f"{user_3_handle['user']['handle_str']} added you to {dm_2['dm_name']}"
            }
        ]
    }
    assert notifications_get_v1(user_5['token']) == {
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to Channel 1"
            },

        ]
    }

def test_added_to_dm(create_input):
    """ Tests the expected return value when a user is added to a channel
    """
    user_1, user_2, user_3, user_4, user_5 = create_input[0]
    
    user_1_handle, _, user_3_handle, _, user_5_handle = create_input[1]
    
    dm_1, dm_2, dm_3 = create_input[3]
    
    dm_invite_v1(user_1['token'], dm_1['dm_id'], user_3['auth_user_id'])
    dm_invite_v1(user_1['token'], dm_1['dm_id'], user_5['auth_user_id'])
    dm_invite_v1(user_3['token'], dm_2['dm_id'], user_1['auth_user_id'])
    dm_invite_v1(user_3['token'], dm_2['dm_id'], user_2['auth_user_id'])
    dm_invite_v1(user_5['token'], dm_3['dm_id'], user_4['auth_user_id'])
    
    assert notifications_get_v1(user_1['token']) == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': dm_2['dm_id'],
                'notification_message': f"{user_3_handle['user']['handle_str']} added you to {dm_2['dm_name']}"
            },
            
        ]
    }
    
    assert notifications_get_v1(user_2['token']) == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': dm_2['dm_id'],
                'notification_message': f"{user_3_handle['user']['handle_str']} added you to {dm_2['dm_name']}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_3['dm_id'],
                'notification_message': f"{user_5_handle['user']['handle_str']} added you to {dm_3['dm_name']}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_1['dm_id'],
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to {dm_1['dm_name']}"
            }
        ]
    }
    
    assert notifications_get_v1(user_3['token']) == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': dm_1['dm_id'],
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to {dm_1['dm_name']}"
            },
        ]
    }
    
    assert notifications_get_v1(user_4['token']) == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': dm_3['dm_id'],
                'notification_message': f"{user_5_handle['user']['handle_str']} added you to {dm_3['dm_name']}"
            },
            {
                'channel_id': -1,
                'dm_id': dm_2['dm_id'],
                'notification_message': f"{user_3_handle['user']['handle_str']} added you to {dm_2['dm_name']}"
            }
        ]
    }
    
    assert notifications_get_v1(user_5['token']) == {
        'notifications': [
            {
                'channel_id': -1,
                'dm_id': dm_1['dm_id'],
                'notification_message': f"{user_1_handle['user']['handle_str']} added you to {dm_1['dm_name']}"
            },
        ]
    }
        
def test_greater_than_20_notifications():
    """ Tests for correctly displayed most recent 20 notifications
    """
    clear_v1()
    user_1 = auth_register_v2('ericzheng@gmail.com', 'kjhfbshjbdf', 'Eric', 'Zheng')
    user_1_handle = user_profile_v2(user_1['token'], user_1['auth_user_id'])
    channel_1 = channels_create_v2(user_1['token'], 'Test', True)
        
    # Send 25 message notifications
    sent_messages = []
    for i in range(25):
        message_send_v2(user_1['token'], channel_1['channel_id'], f"@{user_1_handle['user']['handle_str']} - this is notification {i}")
        sent_messages.append(f"@{user_1_handle['user']['handle_str']} - this is notification {i}")
        
    assert notifications_get_v1(user_1['token']) == {
        'notifications': [
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[24][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[23][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[22][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[21][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[20][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[19][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[18][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[17][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[16][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[15][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[14][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[13][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[12][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[11][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[10][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[9][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[8][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[7][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[6][0:20]}"
            },
            {
                'channel_id': channel_1['channel_id'],
                'dm_id': -1,
                'notification_message': f"{user_1_handle['user']['handle_str']} tagged you in Test: {sent_messages[5][0:20]}"
            },

        ]
    }

def test_single_react_notification():
    clear_v1()
    user1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    channel1 = channels_create_v2(user1['token'], 'Channel 1', True)
    channel_join_v2(user2['token'], channel1['channel_id'])   
    msg1 = message_send_v2(user1['token'], channel1['channel_id'], "1 like = 1 prayer")
    message_react_v1(user2['token'], msg1['message_id'], 1)

    assert notifications_get_v1(user1['token']) == {
        'notifications': [
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "joshhatton reacted to your message in Channel 1"
            }
        ]
    }     

def test_multiple_react_notification():
    clear_v1()
    user1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    user3 = auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong")
    user4 = auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch")
    user5 = auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine")
    channel1 = channels_create_v2(user1['token'], 'Channel 1', True)
    channel_join_v2(user2['token'], channel1['channel_id'])
    channel_join_v2(user3['token'], channel1['channel_id'])
    channel_join_v2(user4['token'], channel1['channel_id'])
    channel_join_v2(user5['token'], channel1['channel_id'])
    msg1 = message_send_v2(user1['token'], channel1['channel_id'], "1 like = 1 prayer")
    message_react_v1(user1['token'], msg1['message_id'], 1)
    message_react_v1(user2['token'], msg1['message_id'], 1)
    message_react_v1(user3['token'], msg1['message_id'], 1)
    message_react_v1(user4['token'], msg1['message_id'], 1)
    message_react_v1(user5['token'], msg1['message_id'], 1)

    assert notifications_get_v1(user1['token']) == {
        'notifications': [
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "deanzworestine reacted to your message in Channel 1"
            },
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "jordanmilch reacted to your message in Channel 1"
            },
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "bunnydong reacted to your message in Channel 1"
            },
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "joshhatton reacted to your message in Channel 1"
            },
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "ericzheng reacted to your message in Channel 1"
            }
        ]
    }    

def test_two_tags():
    clear_v1()
    user1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    channel1 = channels_create_v2(user1['token'], 'Channel 1', True)
    channel_join_v2(user2['token'], channel1['channel_id'])
    msg1str = "@ericzheng @joshhatton" 
    message_send_v2(user1['token'], channel1['channel_id'], msg1str)
    
    
    assert notifications_get_v1(user1['token']) == {
        'notifications': [
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': f"ericzheng tagged you in Channel 1: {msg1str[0:20]}"
            }
        ]
    } 
    assert notifications_get_v1(user2['token']) == {
        'notifications': [
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': f"ericzheng tagged you in Channel 1: {msg1str[0:20]}"
            }
        ]
    }    
        
def test_assorted_notifications():
    clear_v1()
    user1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    channel1 = channels_create_v2(user1['token'], 'Channel 1', True)    
    channel_invite_v2(user1['token'], channel1['channel_id'], user2['auth_user_id'])
    msg1str = "Welcome to the channel @joshhatton"
    msg1 = message_send_v2(user1['token'], channel1['channel_id'], msg1str)
    message_react_v1(user2['token'], msg1['message_id'], 1)   
    msg2str = "Thanks for having me @ericzheng"
    msg2 = message_send_v2(user2['token'], channel1['channel_id'], msg2str)
    message_react_v1(user1['token'], msg2['message_id'], 1)    

    assert notifications_get_v1(user1['token']) == {
        'notifications': [
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': f"joshhatton tagged you in Channel 1: {msg2str[0:20]}"
            },
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "joshhatton reacted to your message in Channel 1"
            }
        ]
    } 
    assert notifications_get_v1(user2['token']) == {
        'notifications': [
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "ericzheng reacted to your message in Channel 1"
            },
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': f"ericzheng tagged you in Channel 1: {msg1str[0:20]}"
            },
            {
                'channel_id': channel1['channel_id'],
                'dm_id': -1,
                'notification_message': "ericzheng added you to Channel 1"
            },                    
        ]
    }    

def test_message_share_with_tag():
    clear_v1()
    user1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    channel1 = channels_create_v2(user1['token'], 'Channel 1', True)
    channel_join_v2(user2['token'], channel1['channel_id'])
    channel2 = channels_create_v2(user1['token'], 'Channel 2', True)
    channel_join_v2(user2['token'], channel2['channel_id'])
    msg1str = "@joshhatton Hi friend"
    msg1 = message_send_v2(user1['token'], channel1['channel_id'], msg1str)
    message_share_v1(user1['token'], msg1['message_id'], '', channel2['channel_id'], -1)
    assert len(notifications_get_v1(user2['token'])['notifications']) == 2

def test_tag_edit():
    clear_v1()
    user1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    channel1 = channels_create_v2(user1['token'], 'Channel 1', True)
    channel_join_v2(user2['token'], channel1['channel_id'])
    msg1str = "Hi friend"
    msg1 = message_send_v2(user1['token'], channel1['channel_id'], msg1str)
    assert len(notifications_get_v1(user2['token'])['notifications']) == 0
    message_edit_v2(user1['token'], msg1['message_id'], "@joshhatton")
    assert len(notifications_get_v1(user2['token'])['notifications']) == 1

def test_tag_sendlater():
    clear_v1()
    user1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    channel1 = channels_create_v2(user1['token'], 'Channel 1', True)
    channel_join_v2(user2['token'], channel1['channel_id'])
    msg1str = "@joshhatton sup"
    current_time = int(time.time())
    message_sendlater_v1(user1['token'], channel1['channel_id'], msg1str, current_time + 2)
    assert len(notifications_get_v1(user2['token'])['notifications']) == 0
    time.sleep(3)
    assert len(notifications_get_v1(user2['token'])['notifications']) == 1

def test_tag_sendlaterdm():
    clear_v1()
    user1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton")
    dm1 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    msg1str = "@joshhatton sup"
    current_time = int(time.time())
    message_sendlaterdm_v1(user1['token'], dm1['dm_id'], msg1str, current_time + 2)
    assert len(notifications_get_v1(user2['token'])['notifications']) == 1
    time.sleep(3)
    assert len(notifications_get_v1(user2['token'])['notifications']) == 2        