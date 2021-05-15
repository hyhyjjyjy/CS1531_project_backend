import pytest
import requests
from src import config
from http_tests.helper_function_for_http_test import auth_register_v2, channel_join_v2, channel_details_v2, channel_leave_v1, channel_addowner_v1, channels_create_v2, channels_list_v2, clear_v1

SUCCESS = 200
INPUT_ERROR = 400
ACCESS_ERROR = 403

@pytest.fixture
def create_input():
    clear_v1()

    data_test_users = [
        auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json(),
        auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong").json(),
        auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch").json(),
        auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine").json(),
        auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json(),
    ]

    data_test_channels = [
        channels_create_v2(data_test_users[0]["token"], "First Channel", True).json(),
        channels_create_v2(data_test_users[1]["token"], "Second Channel", True).json(),
        channels_create_v2(data_test_users[2]["token"], "Third Channel", False).json(),
    ]

    channel_join_v2(data_test_users[1]["token"], data_test_channels[0]["channel_id"])
    channel_join_v2(data_test_users[2]["token"], data_test_channels[0]["channel_id"])

    return [data_test_users, data_test_channels]


def test_success_one_leave(create_input):
    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

    assert channel_leave_v1(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json() == {}

    # length of *_members for First Channel after leave; testing for all involved users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 2
    
    assert channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).status_code == ACCESS_ERROR

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"]).json()["channels"]) == 1
    assert len(channels_list_v2(create_input[0][1]["token"]).json()["channels"]) == 1
    assert len(channels_list_v2(create_input[0][2]["token"]).json()["channels"]) == 2

def test_success_multiple_leave(create_input):
    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

    assert channel_leave_v1(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json() == {}
    assert channel_leave_v1(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json() == {}

    # length of *_members for First Channel after leave; testing for all involved users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 1
    
    assert channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).status_code == ACCESS_ERROR
    assert channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).status_code == ACCESS_ERROR

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"]).json()["channels"]) == 1
    assert len(channels_list_v2(create_input[0][1]["token"]).json()["channels"]) == 1
    assert len(channels_list_v2(create_input[0][2]["token"]).json()["channels"]) == 1

def test_success_owner_leave(create_input):
    # Add another owner to First Channel
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][4]["auth_user_id"]).json() == {}

    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4

    # One owner leaves
    assert channel_leave_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json() == {}

    # length of *_members for First Channel after leave; testing for all involved users
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

    assert channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).status_code == ACCESS_ERROR

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"]).json()["channels"]) == 0
    assert len(channels_list_v2(create_input[0][1]["token"]).json()["channels"]) == 2
    assert len(channels_list_v2(create_input[0][2]["token"]).json()["channels"]) == 2
    assert len(channels_list_v2(create_input[0][4]["token"]).json()["channels"]) == 1

def test_fail_not_member(create_input):
    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

    assert channel_leave_v1(create_input[0][4]["token"], create_input[1][0]["channel_id"]).status_code == ACCESS_ERROR

def test_fail_last_owner_leave(create_input):
    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

    assert channel_leave_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"]).status_code == INPUT_ERROR

def test_channel_id_invalid(create_input):
    # channel_id 5 has not been created
    assert channel_leave_v1(create_input[0][0]["token"], 5).status_code == INPUT_ERROR

def test_token_invalid(create_input):
    # token does not exist
    assert channel_leave_v1('insertinvalidtokenhere', create_input[1][0]["channel_id"]).status_code == ACCESS_ERROR

def test_both_invalid(create_input):
    # token, channel_id do not exist,
    # ACCESS_ERROR is prioritised
    assert channel_leave_v1('insertanotherinvalidtokenhere', 321).status_code == ACCESS_ERROR
