# import pytest
# from src.auth import auth_register_v1
# from src.channel import channel_join_v1, channel_details_v1
# from src.channels import channels_create_v1, channels_list_v1
# from src.other import clear_v1
# from src.error import InputError, AccessError

# @pytest.fixture
# def create_input():
#     clear_v1()

#     data_test_users = [auth_register_v1("joshhatton@mail.com", "validpassword", "Josh", "Hatton"),
#         auth_register_v1("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong"),
#         auth_register_v1("jordanmilch@mail.com", "password3", "Jordan", "Milch"),
#         auth_register_v1("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine"),
#         auth_register_v1("ericzheng@mail.com", "finalpassword", "Eric", "Zheng"),
#     ]

#     data_test_channels = [channels_create_v1(data_test_users[0]["auth_user_id"], "First Channel", True),
#         channels_create_v1(data_test_users[1]["auth_user_id"], "Second Channel", True),
#         channels_create_v1(data_test_users[2]["auth_user_id"], "Third Channel", False),
#     ]

#     return [data_test_users, data_test_channels]


# def test_success_one_join(create_input):
#     # length of *_members for First Channel before join
#     assert len(channel_details_v1(create_input[0][0]["auth_user_id"], create_input[1][0]["channel_id"])["owner_members"]) == 1 
#     assert len(channel_details_v1(create_input[0][0]["auth_user_id"], create_input[1][0]["channel_id"])["all_members"]) == 1 

#     assert channel_join_v1(create_input[0][1]["auth_user_id"], create_input[1][0]["channel_id"]) == {}
    
#     # length of *_members for First Channel after join; testing for both users
#     assert len(channel_details_v1(create_input[0][0]["auth_user_id"], create_input[1][0]["channel_id"])["owner_members"]) == 1
#     assert len(channel_details_v1(create_input[0][0]["auth_user_id"], create_input[1][0]["channel_id"])["all_members"]) == 2
#     assert len(channel_details_v1(create_input[0][1]["auth_user_id"], create_input[1][0]["channel_id"])["owner_members"]) == 1
#     assert len(channel_details_v1(create_input[0][1]["auth_user_id"], create_input[1][0]["channel_id"])["all_members"]) == 2

#     # number of channels each user is a part of
#     assert len(channels_list_v1(create_input[0][0]["auth_user_id"])) == 1 
#     assert len(channels_list_v1(create_input[0][1]["auth_user_id"])) == 2

# def test_success_multiple_join(create_input):
#     # length of *_members for Second Channel before join
#     assert len(channel_details_v1(create_input[0][1]["auth_user_id"], create_input[1][1]["channel_id"])["owner_members"]) == 1 
#     assert len(channel_details_v1(create_input[0][1]["auth_user_id"], create_input[1][1]["channel_id"])["all_members"]) == 1 

#     assert channel_join_v1(create_input[0][0]["auth_user_id"], create_input[1][1]["channel_id"]) == {}
#     assert channel_join_v1(create_input[0][2]["auth_user_id"], create_input[1][1]["channel_id"]) == {}
#     assert channel_join_v1(create_input[0][3]["auth_user_id"], create_input[1][1]["channel_id"]) == {}

#     # length of *_members for Second Channel after join; testing for all users
#     assert len(channel_details_v1(create_input[0][0]["auth_user_id"], create_input[1][1]["channel_id"])["owner_members"]) == 1
#     assert len(channel_details_v1(create_input[0][0]["auth_user_id"], create_input[1][1]["channel_id"])["all_members"]) == 4
#     assert len(channel_details_v1(create_input[0][1]["auth_user_id"], create_input[1][1]["channel_id"])["owner_members"]) == 1
#     assert len(channel_details_v1(create_input[0][1]["auth_user_id"], create_input[1][1]["channel_id"])["all_members"]) == 4
#     assert len(channel_details_v1(create_input[0][2]["auth_user_id"], create_input[1][1]["channel_id"])["owner_members"]) == 1
#     assert len(channel_details_v1(create_input[0][2]["auth_user_id"], create_input[1][1]["channel_id"])["all_members"]) == 4
#     assert len(channel_details_v1(create_input[0][3]["auth_user_id"], create_input[1][1]["channel_id"])["owner_members"]) == 1
#     assert len(channel_details_v1(create_input[0][3]["auth_user_id"], create_input[1][1]["channel_id"])["all_members"]) == 4
#     with pytest.raises(AccessError):
#         len(channel_details_v1(create_input[0][4]["auth_user_id"], create_input[1][1]["channel_id"])["all_members"])

#     # number of channels each user is a part of
#     assert len(channels_list_v1(create_input[0][0]["auth_user_id"])) == 2 
#     assert len(channels_list_v1(create_input[0][1]["auth_user_id"])) == 1
#     assert len(channels_list_v1(create_input[0][2]["auth_user_id"])) == 2 
#     assert len(channels_list_v1(create_input[0][3]["auth_user_id"])) == 1
#     assert len(channels_list_v1(create_input[0][4]["auth_user_id"])) == 0


# def test_fail_private_channel(create_input):
#     # length of *_members for Third Channel before join
#     assert len(channel_details_v1(create_input[0][2]["auth_user_id"], create_input[1][2]["channel_id"])["owner_members"]) == 1 
#     assert len(channel_details_v1(create_input[0][2]["auth_user_id"], create_input[1][2]["channel_id"])["all_members"]) == 1

#     # AccessError becuase these users are not global owners
#     with pytest.raises(AccessError):
#         channel_join_v1(create_input[0][1]["auth_user_id"], create_input[1][2]["channel_id"])
#         channel_join_v1(create_input[0][3]["auth_user_id"], create_input[1][2]["channel_id"])
#         channel_join_v1(create_input[0][4]["auth_user_id"], create_input[1][2]["channel_id"])

# def test_success_private_channel(create_input):
#     # length of *_members for Third Channel before join
#     assert len(channel_details_v1(create_input[0][2]["auth_user_id"], create_input[1][2]["channel_id"])["owner_members"]) == 1 
#     assert len(channel_details_v1(create_input[0][2]["auth_user_id"], create_input[1][2]["channel_id"])["all_members"]) == 1

#     assert channel_join_v1(create_input[0][0]["auth_user_id"], create_input[1][2]["channel_id"]) == {}

#     # create_input[0][0] is a global owner so will pass test
#     assert len(channel_details_v1(create_input[0][2]["auth_user_id"], create_input[1][2]["channel_id"])["owner_members"]) == 1 
#     assert len(channel_details_v1(create_input[0][2]["auth_user_id"], create_input[1][2]["channel_id"])["all_members"]) == 2
#     assert len(channel_details_v1(create_input[0][0]["auth_user_id"], create_input[1][2]["channel_id"])["owner_members"]) == 1
#     assert len(channel_details_v1(create_input[0][0]["auth_user_id"], create_input[1][2]["channel_id"])["all_members"]) == 2

# def test_channel_id_invalid(create_input):
#     # channel_id 5 has not been created
#     with pytest.raises(InputError):
#         channel_join_v1(create_input[0][0]["auth_user_id"], 5)

# def test_auth_user_id_invalid(create_input):
#     # auth_user_id 7 does not exist
#     with pytest.raises(AccessError):
#         channel_join_v1(7, create_input[1][0]["channel_id"])

# def test_both_invalid(create_input):
#     # auth_user_id 21 and channel_id 321 does not exist,
#     # InputError is prioritised
#     with pytest.raises(InputError):
#         channel_join_v1(21, 321)
