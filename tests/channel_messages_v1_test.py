# import pytest

# from src.auth import auth_register_v1
# from src.channel import channel_messages_v1
# from src.channels import channels_create_v1
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


#     #for i in range(0, 120):
#      #   message_send_v1(data_test_users[0]["auth_user_id"], data_test_channels[0]["channel_id"], f"This is message {i}.")

#     return [data_test_users, data_test_channels]

# # NOT ALL TESTS HAVE TO BE IMPLEMENTED FOR channel_messages_v1 IN ITERATION 1
# '''
# def test_success_less_than_fifty(create_input):
#     pass

# def test_success_more_than_fifty(create_input):
#     pass

# def test_success_start_not_zero(create_input):
#     pass

# def test_start_invalid(create_input):
#     pass
# '''

# def test_not_member(create_input):
#     # Second user is not member of first channel
#     with pytest.raises(AccessError):
#         channel_messages_v1(create_input[0][1]["auth_user_id"], create_input[1][0]["channel_id"], 0)

# def test_channel_id_invalid(create_input):
#     # channel_id 5 has not been created
#     with pytest.raises(InputError):
#         channel_messages_v1(create_input[0][0]["auth_user_id"], 5, 0)

# def test_auth_user_id_invalid(create_input):
#     # auth_user_id 7 does not exist
#     with pytest.raises(AccessError):
#         channel_messages_v1(7, create_input[1][0]["channel_id"], 0)
