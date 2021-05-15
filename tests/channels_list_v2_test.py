from src.auth import auth_register_v2
from src.other import clear_v1
from src.channels import channels_create_v2, channels_list_v2
from src.channel import channel_invite_v2

# Tests the empty case where a user is not part of any channel
def test_empty_list():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    assert channels_list_v2(user_1['token']) == {'channels' : []}
    clear_v1()

# Tests a single case where the user is part of only one channel and only 
# one channel exists
def test_single_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    assert channels_list_v2(user_1['token']) == {'channels' : [{'channel_id': channel_1['channel_id'],
                                        'name': 'Channel 1'}]}
    clear_v1()

# Tests a single case again but the user is not part of the channel
def test_non_member_single_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('bb@b.com', 'bbbbbb', 'b', 'b')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    assert channels_list_v2(user_2['token']) == {'channels' : []}
    assert channels_list_v2(user_1['token']) == {'channels' : [{'channel_id': channel_1['channel_id'],
                                        'name': 'Channel 1'}]}
    clear_v1()

# Adds a user to multiple channels with varying permissions and ensures 
# all the channels are displayed 
def test_multiple_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', False)
    channel_3 = channels_create_v2(user_1['token'], 'Channel 3', True)
    assert channels_list_v2(user_1['token']) == {'channels' : [{'channel_id': channel_1['channel_id'],
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
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('bb@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', True)
    channel_3 = channels_create_v2(user_1['token'], 'Channel 3', False)
    channel_4 = channels_create_v2(user_1['token'], 'Channel 4', False)
    channel_5 = channels_create_v2(user_1['token'], 'Channel 5', True)
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_3['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_5['channel_id'], user_2['auth_user_id'])
    assert channels_list_v2(user_1['token']) == {'channels' : [{'channel_id': channel_1['channel_id'],
                                         'name': 'Channel 1'},
                                        {'channel_id': channel_2['channel_id'],
                                         'name': 'Channel 2'},
                                        {'channel_id': channel_3['channel_id'],
                                         'name': 'Channel 3'},
                                        {'channel_id': channel_4['channel_id'],
                                         'name': 'Channel 4'},
                                        {'channel_id': channel_5['channel_id'],
                                         'name': 'Channel 5'}]}  
    assert channels_list_v2(user_2['token']) == {'channels' : [{'channel_id': channel_1['channel_id'],
                                         'name': 'Channel 1'},
                                        {'channel_id': channel_3['channel_id'],
                                         'name': 'Channel 3'},
                                        {'channel_id': channel_5['channel_id'],
                                         'name': 'Channel 5'}]}    
    clear_v1()