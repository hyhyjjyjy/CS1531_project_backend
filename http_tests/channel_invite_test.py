import pytest
import requests
from src import config
from http_tests.helper_function_for_http_test import clear_v1, auth_register_v2, channels_create_v2, \
                                             channel_invite_v2, channel_details_v2, \
                                             channel_addowner_v1

SUCCESS = 200
INPUT_ERROR = 400
ACCESS_ERROR = 403

@pytest.fixture
def create_input():
    clear_v1()
    
    data_test_users = [
        auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json(),
        auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json(),
        auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong").json(),
        auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch").json(),
        auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine").json(),
    ]

    data_test_channels = [
        channels_create_v2(data_test_users[0]['token'], "General", True).json(),
        channels_create_v2(data_test_users[1]['token'], "Party", True).json(),
        channels_create_v2(data_test_users[2]['token'], "Private", False).json(),
    ]

    return [data_test_users, data_test_channels]

def test_invalid_channel_id_exception():
    """ Tests when channel_id does not refer to a valid channel.
    """
    clear_v1()
    
    user_1 = auth_register_v2("ericzheng@gmail.com", "password34", "Eric",
                              "Zheng").json()
    user_2 = auth_register_v2("jordanmilch@mail.com", "password3", "Jordan",
                              "Milch").json()

    channel_invite_1 = channel_invite_v2(user_1['token'], 0, user_2['auth_user_id'])
    channel_invite_2 = channel_invite_v2(user_2['token'], 1, user_1['auth_user_id'])
    
    assert channel_invite_1.status_code == INPUT_ERROR
    assert channel_invite_2.status_code == INPUT_ERROR        

def test_invalid_user_id_exception():
    """ Tests when u_id does not refer to a valid user.
    """
    clear_v1()

    # Create a valid user and add them to a valid channel
    user = auth_register_v2("ericzheng@mail.com", "peterpiper", "Eric",
                              "Zheng").json()
    channel = channels_create_v2(user['token'], "Lalaland", True).json()

    # Test for InputError when invalid users are invited to channel
     
    assert channel_invite_v2(user['token'], channel['channel_id'],
     user['auth_user_id'] + 5).status_code == INPUT_ERROR
    assert channel_invite_v2(user['token'], channel['channel_id'],
     user['auth_user_id'] + 500).status_code == INPUT_ERROR
    assert channel_invite_v2(user['token'], channel['channel_id'],
     user['auth_user_id'] - 5).status_code == INPUT_ERROR
    assert channel_invite_v2(user['token'], channel['channel_id'],
     user['auth_user_id'] - 5000).status_code == INPUT_ERROR
    assert channel_invite_v2(user['token'], channel['channel_id'],
     user['auth_user_id'] + 50000).status_code == INPUT_ERROR

def test_invalid_token_exception():
    """ Tests when the authorised user is an invalid id
    """
    clear_v1()

    # Create a valid channel with user as owner
    user = auth_register_v2("mangopineapple@mail.com", "mangofruit1", 
                            "Adam", "Apple").json()
    channel = channels_create_v2(user['token'], "Valid channel", True).json()

    assert channel_invite_v2(user['token'] + 'bug', channel['channel_id'],
                             user['auth_user_id']).status_code == ACCESS_ERROR
    assert channel_invite_v2(user['token'] + 'pipswe23', channel['channel_id'],
                             user['auth_user_id']).status_code == ACCESS_ERROR
    assert channel_invite_v2(user['token'] + '5000', channel['channel_id'],
                             user['auth_user_id']).status_code == ACCESS_ERROR
    assert channel_invite_v2(user['token'] + '689d', channel['channel_id'],
                             user['auth_user_id']).status_code == ACCESS_ERROR
    assert channel_invite_v2(user['token'] + 'd', channel['channel_id'],
                             user['auth_user_id']).status_code == ACCESS_ERROR

def test_unauthorised_user_exception(create_input):
    """ Tests when the authorised user is not already a member of the channel
    """
    
    user_1, user_2, user_3, user_4, user_5 = create_input[0]
    
    # Create a channel with user_in_channel as the only member
    user_in_channel = auth_register_v2("existence@mail.com", "wawaweewa", 
                                       "Already", "Exists").json()
    channel = channels_create_v2(user_in_channel['token'], "Library", True).json()

    assert channel_invite_v2(user_1['token'], channel['channel_id'],
     user_2['auth_user_id']).status_code == ACCESS_ERROR
    assert channel_invite_v2(user_2['token'], channel['channel_id'],
     user_3['auth_user_id']).status_code == ACCESS_ERROR
    assert channel_invite_v2(user_3['token'], channel['channel_id'],
     user_4['auth_user_id']).status_code == ACCESS_ERROR
    assert channel_invite_v2(user_4['token'], channel['channel_id'],
     user_5['auth_user_id']).status_code == ACCESS_ERROR
    assert channel_invite_v2(user_5['token'], channel['channel_id'],
     user_1['auth_user_id']).status_code == ACCESS_ERROR

def test_order_of_exceptions():
    """ Tests that the function raises exceptions in the order as assumed. The order
    should be:
        1. AccessError from invalid token
        2. InputError from invalid channel id
        3. InputError from invalid user id
        4. AccessError when any of the authorised user is not already part of a 
            channel
    """
    clear_v1()

    user_1 = auth_register_v2("asdfsadfasdf@mail.com", "f244332fsd", "Tom",
                              "Cruise").json()
    user_2 = auth_register_v2("dummyone@mail.com", "password09123", "Dummy",
                              "Dog").json()
    channel = channels_create_v2(user_1['token'], "General", True).json()
    user_test = auth_register_v2("testuserone@mail.com", "watermelon", "Max", 
                                    "Rex").json()

    # Pass in invalid user_id, invalid auth_user_id, invalid channel_id,
    # auth_user not part of the channel. This should raise an access error.
    assert channel_invite_v2(user_2['token'] + 'bug', channel['channel_id'] + 5,
                            user_test['auth_user_id'] + 5).status_code == ACCESS_ERROR
    
    # Pass in invalid user_id, valid token, invalid channel_id,
    # auth_user not part of the channel. This should raise an access error.
    assert channel_invite_v2(user_2['token'], channel['channel_id'] + 5,
                            user_test['auth_user_id'] + 5).status_code == INPUT_ERROR

    # Pass in valid user_id, valid token, valid channel_id,
    # auth_user not part of the channel. This should raise an input error.                          
    assert channel_invite_v2(user_2['token'], channel['channel_id'],
                            user_test['auth_user_id'] + 5).status_code == INPUT_ERROR
        

    # Pass in valid user_id, valid token, valid channel_id,
    # auth_user not part of the channel. This should raise an access error.                          
    assert channel_invite_v2(user_2['token'], channel['channel_id'],
                            user_test['auth_user_id']).status_code == ACCESS_ERROR

def test_successful_invites(create_input):
    """ Tests for multiple successful invites to a channel
    """

    # Create a set of users not in the channel yet
    user_1, user_2, user_3, user_4, user_5 = create_input[0]

    channel_1, channel_2, channel_3 = create_input[1]

    # Test for successful calls and that users have been immediately added into
    # their channels

    # Invite user2, user3, user4, user5 to channel 1
    assert channel_invite_v2(user_1['token'], channel_1['channel_id'],
                             user_2['auth_user_id']).status_code == SUCCESS
    assert channel_invite_v2(user_1['token'], channel_1['channel_id'],
                             user_3['auth_user_id']).status_code == SUCCESS
    assert channel_invite_v2(user_1['token'], channel_1['channel_id'],
                             user_4['auth_user_id']).status_code == SUCCESS
    assert channel_invite_v2(user_1['token'], channel_1['channel_id'],
                             user_5['auth_user_id']).status_code == SUCCESS

    # Invite user4, user5 to channel 2
    assert channel_invite_v2(user_2['token'], channel_2['channel_id'],
                             user_4['auth_user_id']).status_code == SUCCESS
    assert channel_invite_v2(user_2['token'], channel_2['channel_id'],
                             user_5['auth_user_id']).status_code == SUCCESS

    # Invite user1 to channel 3
    assert channel_invite_v2(user_3['token'], channel_3['channel_id'],
                             user_1['auth_user_id']).status_code == SUCCESS

    # Check that users have been added to channels
    channel_detail_1 = channel_details_v2(user_1['token'],
                                          channel_1['channel_id']).json()
    channel_detail_2 = channel_details_v2(user_2['token'],
                                          channel_2['channel_id']).json()
    channel_detail_3 = channel_details_v2(user_3['token'],
                                          channel_3['channel_id']).json()

    # Check channel 1
    assert channel_detail_1['all_members'][0]['u_id'] == user_1['auth_user_id']
    assert channel_detail_1['all_members'][1]['u_id'] == user_2['auth_user_id']
    assert channel_detail_1['all_members'][2]['u_id'] == user_3['auth_user_id']
    assert channel_detail_1['all_members'][3]['u_id'] == user_4['auth_user_id']
    assert channel_detail_1['all_members'][4]['u_id'] == user_5['auth_user_id']

    # Check channel 2
    assert channel_detail_2['all_members'][0]['u_id'] == user_2['auth_user_id']
    assert channel_detail_2['all_members'][1]['u_id'] == user_4['auth_user_id']
    assert channel_detail_2['all_members'][2]['u_id'] == user_5['auth_user_id']

    # Check channel 3
    assert channel_detail_3['all_members'][0]['u_id'] == user_3['auth_user_id']
    assert channel_detail_3['all_members'][1]['u_id'] == user_1['auth_user_id']

def test_self_invite(create_input):
    """ Test for user trying to invite themselves. The function should call
        successfully and not add the user again to the channel.
    """   
        
    user_1, user_2, user_3, user_4, user_5 = create_input[0]

    channel_1, channel_2, channel_3 = create_input[1]
    
    # Owner inviting themselves
    assert channel_invite_v2(user_1['token'], channel_1['channel_id'], 
                             user_1['auth_user_id']).status_code == SUCCESS
    channel_1_details = channel_details_v2(user_1['token'], 
                                           channel_1['channel_id']).json()
    assert len(channel_1_details['all_members']) == 1

    assert channel_invite_v2(user_2['token'], channel_2['channel_id'], 
                             user_2['auth_user_id']).status_code == SUCCESS
    channel_2_details = channel_details_v2(user_2['token'], 
                                           channel_2['channel_id']).json()
    assert len(channel_2_details['all_members']) == 1
    
    assert channel_invite_v2(user_3['token'], channel_3['channel_id'], 
                             user_3['auth_user_id']).status_code == SUCCESS
    channel_3_details = channel_details_v2(user_3['token'], 
                                           channel_3['channel_id']).json()
    assert len(channel_3_details['all_members']) == 1

    # User 4 inviting themselves after being invited by user 1
    assert channel_invite_v2(user_1['token'], channel_1['channel_id'],
                             user_4['auth_user_id']).status_code == SUCCESS
    assert channel_invite_v2(user_4['token'], channel_1['channel_id'],
                             user_4['auth_user_id']).status_code == SUCCESS
    channel_1_details = channel_details_v2(user_1['token'], 
                                           channel_1['channel_id']).json()
    assert len(channel_1_details['all_members']) == 2

    # User 5 inviting themselves after being invited by user 4
    assert channel_invite_v2(user_4['token'], channel_1['channel_id'],
                             user_5['auth_user_id']).status_code == SUCCESS
    assert channel_invite_v2(user_5['token'], channel_1['channel_id'],
                             user_5['auth_user_id']).status_code == SUCCESS
    channel_1_details = channel_details_v2(user_1['token'], 
                                           channel_1['channel_id']).json()
    assert len(channel_1_details['all_members']) == 3

def test_invite_global_owner(create_input):
    """ Tests that when a global owner is invited to a channel, they will have
        owner permissions in that channel.
    """
    
    channel_1 = create_input[1][1]
    
    assert channel_invite_v2(create_input[0][1]['token'], channel_1['channel_id'],
                             create_input[0][0]['auth_user_id']).status_code == SUCCESS
    assert channel_invite_v2(create_input[0][1]['token'], channel_1['channel_id'],
                             create_input[0][2]['auth_user_id']).status_code == SUCCESS
    
    # create_input[0][0] is a global owner, so when invited, they should join 
    # as a member but have owner permissions
    # create_input[0][2] is a member
    assert len(channel_details_v2(create_input[0][1]['token'], 
                                  channel_1['channel_id']).json()['owner_members']) == 1
    assert len(channel_details_v2(create_input[0][1]['token'], 
                                  channel_1['channel_id']).json()['all_members']) == 3

    # create_input[0][0] should be able to promote create_input[0][2] to a
    # channel owner
    assert channel_addowner_v1(create_input[0][0]['token'],
                               channel_1['channel_id'],
                               create_input[0][2]['auth_user_id']).status_code == SUCCESS

def test_success_private_channel(create_input):
    """ Tests that users can be invited into private channels too.
    """
    
    channel_private = create_input[1][2]
    
    assert channel_invite_v2(create_input[0][2]['token'], channel_private['channel_id'],
                             create_input[0][0]['auth_user_id']).status_code == SUCCESS
    
    assert len(channel_details_v2(create_input[0][2]['token'], 
                                  channel_private['channel_id']).json()['owner_members']) == 1
    assert len(channel_details_v2(create_input[0][2]['token'], 
                                  channel_private['channel_id']).json()['all_members']) == 2