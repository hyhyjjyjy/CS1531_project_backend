# import pytest

# from src.auth import auth_register_v1
# from src.channel import channel_invite_v1, channel_details_v1
# from src.channels import channels_create_v1
# from src.other import clear_v1
# from src.error import InputError, AccessError

# def create_valid_user_data():
#     """ Creates and returns a set of valid users.
#     """
#     user_data = (
#         auth_register_v1("ericzheng@mail.com", "peterpiper", "Eric", "Zheng"),
#         auth_register_v1("joshhatton@mail.com", "maryreider", "Josh", "Hatton"), 
#         auth_register_v1("bunnydong@mail.com", "globalempire4", "Bunny", "Dong"), 
#         auth_register_v1("deanzworestine@mail.com", "runescape4lyfe", "Dean", 
#                          "Zworestine"), 
#         auth_register_v1("jordanmilch@mail.com", "iheartnewyork", "Jordan", 
#                          "Milch")
#     ) 
#     return user_data

# def test_invalid_channel_id_exception():
#     """ Tests when channel_id does not refer to a valid channel.
#     """
#     clear_v1()

#     user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()

#     channel = channels_create_v1(user_1['auth_user_id'], "Party Time", True)

#     with pytest.raises(InputError):
#         channel_invite_v1(user_1['auth_user_id'], channel['channel_id'] + 5,
#                           user_2['auth_user_id'])
#         channel_invite_v1(user_1['auth_user_id'], channel['channel_id'] + 500,
#                           user_3['auth_user_id'])
#         channel_invite_v1(user_1['auth_user_id'], channel['channel_id'] - 5,
#                           user_4['auth_user_id'])
#         channel_invite_v1(user_1['auth_user_id'], channel['channel_id'] - 500,
#                           user_5['auth_user_id'])

# def test_invalid_user_id_exception():
#     """ Tests when u_id does not refer to a valid user.
#     """
#     clear_v1()

#     # Create a valid user and add them to a valid channel
#     user = auth_register_v1("ericzheng@mail.com", "peterpiper", "Eric",
#                               "Zheng")
#     channel = channels_create_v1(user['auth_user_id'], "Lalaland", True)

#     # Test for InputError when invalid users are invited to channel
#     with pytest.raises(InputError):
#         channel_invite_v1(user['auth_user_id'], channel['channel_id'],
#                           user['auth_user_id'] + 5)
#         channel_invite_v1(user['auth_user_id'], channel['channel_id'],
#                           user['auth_user_id'] + 500)
#         channel_invite_v1(user['auth_user_id'], channel['channel_id'],
#                           user['auth_user_id'] - 5)
#         channel_invite_v1(user['auth_user_id'], channel['channel_id'],
#                           user['auth_user_id'] - 5000)
#         channel_invite_v1(user['auth_user_id'], channel['channel_id'],
#                           user['auth_user_id'] + 50000)

# def test_invalid_auth_id_exception():
#     """ Tests when the authorised user is an invalid id
#     """
#     clear_v1()

#     user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()

#     # Create a valid channel with user as owner
#     user = auth_register_v1("mangopineapple@mail.com", "mangofruit1", 
#                             "Adam", "Apple")
#     channel = channels_create_v1(user['auth_user_id'], "Valid channel", True)

#     with pytest.raises(AccessError):
#         channel_invite_v1(user['auth_user_id'] + 50, channel['channel_id'],
#                           user_1['auth_user_id'])
#         channel_invite_v1(user['auth_user_id'] + 500, channel['channel_id'],
#                           user_2['auth_user_id'])
#         channel_invite_v1(user['auth_user_id'] + 5000, channel['channel_id'],
#                           user_3['auth_user_id'])
#         channel_invite_v1(user['auth_user_id'] - 50, channel['channel_id'],
#                           user_4['auth_user_id'])
#         channel_invite_v1(user['auth_user_id'] - 5000, channel['channel_id'],
#                           user_5['auth_user_id'])

# def test_unauthorised_user_exception():
#     """ Tests when the authorised user is not already a member of the channel
#     """
#     clear_v1()

#     user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()

#     # Create a channel with user_in_channel as the only member
#     user_in_channel = auth_register_v1("existence@mail.com", "wawaweewa", 
#                                        "Already", "Exists")
#     channel = channels_create_v1(user_in_channel['auth_user_id'], "Library", True)
    
#     with pytest.raises(AccessError):
#         channel_invite_v1(user_1['auth_user_id'], channel['channel_id'],
#                           user_2['auth_user_id'])
#         channel_invite_v1(user_2['auth_user_id'], channel['channel_id'],
#                           user_3['auth_user_id'])
#         channel_invite_v1(user_3['auth_user_id'], channel['channel_id'],
#                           user_4['auth_user_id'])
#         channel_invite_v1(user_4['auth_user_id'], channel['channel_id'],
#                           user_5['auth_user_id'])
#         channel_invite_v1(user_5['auth_user_id'], channel['channel_id'],
#                           user_1['auth_user_id'])

# def test_order_of_exceptions():
#     """ Tests that the function raises exceptions in the order as assumed. The order
#     should be:
#         1. InputError from invalid channel id
#         2. InputError from invalid user id
#         3. AccessError when any of the authorised user is not already part of a 
#             channel
#     """
#     clear_v1()

#     user_1 = auth_register_v1("asdfsadfasdf@mail.com", "f244332fsd", "Tom",
#                               "Cruise")
#     user_2 = auth_register_v1("dummyone@mail.com", "password09123", "Dummy",
#                               "Dog")
#     channel = channels_create_v1(user_1['auth_user_id'], "General", True)
#     user_test = auth_register_v1("testuserone@mail.com", "watermelon", "Max", 
#                                     "Rex")

#     # Pass in invalid user_id, invalid auth_user_id, invalid channel_id,
#     # auth_user not part of the channel. This should raise an input error.
#     with pytest.raises(InputError):
#         channel_invite_v1(user_2['auth_user_id'] + 5, channel['channel_id'] + 5,
#                             user_test['auth_user_id'] + 5)

#     # Pass in invalid user_id, invalid auth_user_id, valid channel_id,
#     # auth_user not part of the channel. This should raise an access error.
#     with pytest.raises(AccessError):
#         channel_invite_v1(user_2['auth_user_id'] + 5, channel['channel_id'],
#                             user_test['auth_user_id'] + 5)

#     # Pass in valid user_id, invalid auth_user_id, valid channel_id,
#     # auth_user not part of the channel. This should raise an input error.                          
#     with pytest.raises(AccessError):
#         channel_invite_v1(user_2['auth_user_id'] + 5, channel['channel_id'],
#                             user_test['auth_user_id'])

#     # Pass in valid user_id, valid auth_user_id, valid channel_id,
#     # auth_user not part of the channel. This should raise an access error.                          
#     with pytest.raises(AccessError):
#         channel_invite_v1(user_2['auth_user_id'], channel['channel_id'],
#                             user_test['auth_user_id'])

# def test_successful_invites():
#     """ Tests for multiple successful invites to a channel
#     """
#     clear_v1()

#     # Create a set of users not in the channel yet
#     user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()

#     # Create channels with user_auth_X as owner
#     user_auth_1 = auth_register_v1("daboss89@mail.com", "iamlegend", "Daniel",
#                                    "Dapman")
#     user_auth_2 = auth_register_v1("test2@mail.com", "sfdfadsfs2", "David",
#                                    "Bonzales")
#     user_auth_3 = auth_register_v1("ClaraFang@mail.com", "cheesecake2", "Clara",
#                                    "Fang")

#     channel_1 = channels_create_v1(user_auth_1['auth_user_id'], "Partee", True)
#     channel_2 = channels_create_v1(user_auth_2['auth_user_id'], "Silent", True)
#     channel_3 = channels_create_v1(user_auth_3['auth_user_id'], "AFK", True)

#     # Test for successful calls and that users have been immediately added into
#     # their channels

#     # Invite user1, user2, user3, user4, user5 to channel 1
#     assert channel_invite_v1(user_auth_1['auth_user_id'], channel_1['channel_id'],
#                              user_1['auth_user_id']) == {}
#     assert channel_invite_v1(user_auth_1['auth_user_id'], channel_1['channel_id'],
#                              user_2['auth_user_id']) == {}
#     assert channel_invite_v1(user_auth_1['auth_user_id'], channel_1['channel_id'],
#                              user_3['auth_user_id']) == {}
#     assert channel_invite_v1(user_auth_1['auth_user_id'], channel_1['channel_id'],
#                              user_4['auth_user_id']) == {}
#     assert channel_invite_v1(user_auth_1['auth_user_id'], channel_1['channel_id'],
#                              user_5['auth_user_id']) == {}

#     # Invite user4, user5 to channel 2
#     assert channel_invite_v1(user_auth_2['auth_user_id'], channel_2['channel_id'],
#                              user_4['auth_user_id']) == {}
#     assert channel_invite_v1(user_auth_2['auth_user_id'], channel_2['channel_id'],
#                              user_5['auth_user_id']) == {}

#     # Invite user1 to channel 3
#     assert channel_invite_v1(user_auth_3['auth_user_id'], channel_3['channel_id'],
#                              user_1['auth_user_id']) == {}

#     # Check that users have been added to channels
#     channel_detail_1 = channel_details_v1(user_auth_1['auth_user_id'],
#                                           channel_1['channel_id'])
#     channel_detail_2 = channel_details_v1(user_auth_2['auth_user_id'],
#                                           channel_2['channel_id'])
#     channel_detail_3 = channel_details_v1(user_auth_3['auth_user_id'],
#                                           channel_3['channel_id'])

#     # Check channel 1
#     assert channel_detail_1['all_members'][0]['u_id'] == user_auth_1['auth_user_id']
#     assert channel_detail_1['all_members'][1]['u_id'] == user_1['auth_user_id']
#     assert channel_detail_1['all_members'][2]['u_id'] == user_2['auth_user_id']
#     assert channel_detail_1['all_members'][3]['u_id'] == user_3['auth_user_id']
#     assert channel_detail_1['all_members'][4]['u_id'] == user_4['auth_user_id']
#     assert channel_detail_1['all_members'][5]['u_id'] == user_5['auth_user_id']

#     # Check channel 2
#     assert channel_detail_2['all_members'][0]['u_id'] == user_auth_2['auth_user_id']
#     assert channel_detail_2['all_members'][1]['u_id'] == user_4['auth_user_id']
#     assert channel_detail_2['all_members'][2]['u_id'] == user_5['auth_user_id']

#     # Check channel 3
#     assert channel_detail_3['all_members'][0]['u_id'] == user_auth_3['auth_user_id']
#     assert channel_detail_3['all_members'][1]['u_id'] == user_1['auth_user_id']

# def test_self_invite():
#     """ Test for user trying to invite themselves. The function should call
#         successfully and not add the user again to the channel.
#     """   
#     clear_v1()                            
    
#     user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()

#     channel_1 = channels_create_v1(user_1['auth_user_id'], "Part D", True)
#     channel_2 = channels_create_v1(user_2['auth_user_id'], "PartE!!!", True)
#     channel_3 = channels_create_v1(user_3['auth_user_id'], "Part F", True)
    
#     # Owner inviting themselves
#     assert channel_invite_v1(user_1['auth_user_id'], channel_1['channel_id'], 
#                              user_1['auth_user_id']) == {}
#     channel_1_details = channel_details_v1(user_1['auth_user_id'], 
#                                            channel_1['channel_id'])
#     assert len(channel_1_details['all_members']) == 1

#     assert channel_invite_v1(user_2['auth_user_id'], channel_2['channel_id'], 
#                              user_2['auth_user_id']) == {}
#     channel_2_details = channel_details_v1(user_2['auth_user_id'], 
#                                            channel_2['channel_id'])
#     assert len(channel_2_details['all_members']) == 1
    
#     assert channel_invite_v1(user_3['auth_user_id'], channel_3['channel_id'], 
#                              user_3['auth_user_id']) == {}
#     channel_3_details = channel_details_v1(user_3['auth_user_id'], 
#                                            channel_3['channel_id'])
#     assert len(channel_3_details['all_members']) == 1

#     # User 4 inviting themselves after being invited by user 1
#     assert channel_invite_v1(user_1['auth_user_id'], channel_1['channel_id'],
#                              user_4['auth_user_id']) == {}
#     assert channel_invite_v1(user_4['auth_user_id'], channel_1['channel_id'],
#                              user_4['auth_user_id']) == {}
#     channel_1_details = channel_details_v1(user_1['auth_user_id'], 
#                                            channel_1['channel_id'])
#     assert len(channel_1_details['all_members']) == 2

#     # User 5 inviting themselves after being invited by user 4
#     assert channel_invite_v1(user_4['auth_user_id'], channel_1['channel_id'],
#                              user_5['auth_user_id']) == {}
#     assert channel_invite_v1(user_5['auth_user_id'], channel_1['channel_id'],
#                              user_5['auth_user_id']) == {}
#     channel_1_details = channel_details_v1(user_1['auth_user_id'], 
#                                            channel_1['channel_id'])
#     assert len(channel_1_details['all_members']) == 3

# def test_invite_private_channel():
#     """ Tests that users can be invited into private channels too.
#     """
#     clear_v1()

#     user_1, user_2, user_3, user_4, user_5 = create_valid_user_data()

#     channel_private = channels_create_v1(user_1['auth_user_id'], "Secret", False)

#     assert channel_invite_v1(user_1['auth_user_id'], 
#                              channel_private['channel_id'], 
#                              user_2['auth_user_id']) == {}
#     assert channel_invite_v1(user_2['auth_user_id'], 
#                              channel_private['channel_id'], 
#                              user_3['auth_user_id']) == {}

#     channel_private_details = channel_details_v1(user_1['auth_user_id'], 
#                                                  channel_private['channel_id'])
#     assert channel_private_details['all_members'][0]['u_id'] == user_1['auth_user_id']
#     assert channel_private_details['all_members'][1]['u_id'] == user_2['auth_user_id']
#     assert channel_private_details['all_members'][2]['u_id'] == user_3['auth_user_id']

#     assert channel_invite_v1(user_3['auth_user_id'], 
#                             channel_private['channel_id'], 
#                             user_4['auth_user_id']) == {}
#     assert channel_invite_v1(user_4['auth_user_id'], 
#                             channel_private['channel_id'], 
#                             user_5['auth_user_id']) == {}
#     channel_private_details = channel_details_v1(user_1['auth_user_id'], 
#                                                 channel_private['channel_id'])
#     assert channel_private_details['all_members'][3]['u_id'] == user_4['auth_user_id']
#     assert channel_private_details['all_members'][4]['u_id'] == user_5['auth_user_id']
