import pytest
import requests
from src import config
from http_tests.helper_function_for_http_test import clear_v1, auth_register_v2, channels_create_v2, channel_join_v2, channel_details_v2, channels_list_v2

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

    return [data_test_users, data_test_channels]


def test_success_one_join(create_input):
    # length of *_members for First Channel before join
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 1

    assert channel_join_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json() == {}
    
    # length of *_members for First Channel after join; testing for both users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 2
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 2

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"]).json()["channels"]) == 1 
    assert len(channels_list_v2(create_input[0][1]["token"]).json()["channels"]) == 2

def test_success_multiple_join(create_input):
    # length of *_members for Second Channel before join
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"]).json()["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"]).json()["all_members"]) == 1

    assert channel_join_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"]).json() == {}
    assert channel_join_v2(create_input[0][2]["token"], create_input[1][1]["channel_id"]).json() == {}
    assert channel_join_v2(create_input[0][3]["token"], create_input[1][1]["channel_id"]).json() == {}

    # length of *_members for Second Channel after join; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][1]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][1]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][1]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][1]["channel_id"]).json()["all_members"]) == 4
    
    assert channel_details_v2(create_input[0][4]["token"], create_input[1][1]["channel_id"]).status_code == ACCESS_ERROR

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"]).json()["channels"]) == 2 
    assert len(channels_list_v2(create_input[0][1]["token"]).json()["channels"]) == 1
    assert len(channels_list_v2(create_input[0][2]["token"]).json()["channels"]) == 2 
    assert len(channels_list_v2(create_input[0][3]["token"]).json()["channels"]) == 1
    assert len(channels_list_v2(create_input[0][4]["token"]).json()["channels"]) == 0

def test_fail_private_channel(create_input):
    # length of *_members for Third Channel before join
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["all_members"]) == 1

    # AccessError becuase these users are not global owners
    assert channel_join_v2(create_input[0][1]["token"], create_input[1][2]["channel_id"]).status_code == ACCESS_ERROR
    assert channel_join_v2(create_input[0][3]["token"], create_input[1][2]["channel_id"]).status_code == ACCESS_ERROR
    assert channel_join_v2(create_input[0][4]["token"], create_input[1][2]["channel_id"]).status_code == ACCESS_ERROR

def test_success_private_channel(create_input):
    # length of *_members for Third Channel before join
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["all_members"]) == 1

    assert channel_join_v2(create_input[0][0]["token"], create_input[1][2]["channel_id"]).json() == {}

    # create_input[0][0] is a global owner so will pass test
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["all_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][2]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][2]["channel_id"]).json()["all_members"]) == 2

def test_channel_id_invalid(create_input):
    # channel_id 5 has not been created
    assert channel_join_v2(create_input[0][0]["token"], 5).status_code == INPUT_ERROR

def test_token_invalid(create_input):
    # token is invalid
    assert channel_join_v2('insertinvalidtokenhere', create_input[1][0]["channel_id"]).status_code == ACCESS_ERROR

def test_both_invalid(create_input):
    # token and channel_id both invalid,
    # ACCESS_ERROR is prioritised
    assert channel_join_v2('insertanotherinvalidtokenhere', 321).status_code == ACCESS_ERROR
