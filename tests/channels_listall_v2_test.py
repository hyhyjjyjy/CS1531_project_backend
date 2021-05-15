from src.auth import auth_register_v2
from src.other import clear_v1
from src.channels import channels_create_v2, channels_listall_v2
from src.channel import channel_invite_v2

# Tests an empty list - where there are no channels
def test_empty():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa1', 'a', 'a')
    assert channels_listall_v2(user_1['token']) == {'channels' : []}
    
# Tests one channel with the user part of that channel
def test_single_channel_including_user():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa1', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    assert channels_listall_v2(user_1['token']) == {'channels' : [{'channel_id': channel_1['channel_id'],
                                             'name': 'Channel 1'}]}
    
# Tests one channel with the user not part of that channel
def test_single_channel_excluding_user():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa1', 'a', 'a')
    user_2 = auth_register_v2('bb@b.com', 'bbbbbb1', 'b', 'b')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    assert channels_listall_v2(user_2['token']) == {'channels' : [{'channel_id': channel_1['channel_id'],
                                             'name': 'Channel 1'}]}

# Tests a range of channels with different permissions and checks that everyone gets the same list containing all channels
def test_multiple_channels_different_permissions():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa1', 'a', 'a')
    user_2 = auth_register_v2('bb@b.com', 'bbbbbb1', 'b', 'b')
    user_3 = auth_register_v2('cb@c.com', 'aaaaaa1', 'a', 'a')
    user_4 = auth_register_v2('db@d.com', 'bbbbbb1', 'b', 'b')
    user_5 = auth_register_v2('eb@e.com', 'aaaaaa1', 'a', 'a')
    user_6 = auth_register_v2('fb@f.com', 'bbbbbb1', 'b', 'b')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_2 = channels_create_v2(user_2['token'], 'Channel 2', True)
    channel_3 = channels_create_v2(user_3['token'], 'Channel 3', False)
    channel_4 = channels_create_v2(user_4['token'], 'Channel 4', False)
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_5['auth_user_id'])
    assert channels_listall_v2(user_1['token']) == {'channels' : [{'channel_id': channel_1['channel_id'],
                                            'name': 'Channel 1'},
                                           {'channel_id': channel_2['channel_id'],
                                            'name': 'Channel 2'},
                                           {'channel_id': channel_3['channel_id'],
                                            'name': 'Channel 3'},
                                           {'channel_id': channel_4['channel_id'],
                                            'name': 'Channel 4'}]}
    assert channels_listall_v2(user_1['token']) == channels_listall_v2(user_2['token'])
    assert channels_listall_v2(user_1['token']) == channels_listall_v2(user_3['token'])
    assert channels_listall_v2(user_1['token']) == channels_listall_v2(user_4['token'])
    assert channels_listall_v2(user_1['token']) == channels_listall_v2(user_5['token']) 
    assert channels_listall_v2(user_1['token']) == channels_listall_v2(user_6['token'])
