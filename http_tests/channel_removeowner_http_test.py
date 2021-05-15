import pytest
import requests
from src import config
from http_tests.helper_function_for_http_test import auth_register_v2, channel_removeowner_v1, channel_addowner_v1, channel_join_v2, channel_details_v2, channels_create_v2, channels_list_v2, clear_v1

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
        channels_create_v2(data_test_users[2]["token"], "Third Channel", True).json(),
        channels_create_v2(data_test_users[3]["token"], "Fourth Channel", False).json(),
    ]

    channel_addowner_v1(data_test_users[0]["token"], data_test_channels[0]["channel_id"], data_test_users[1]["auth_user_id"])
    channel_addowner_v1(data_test_users[1]["token"], data_test_channels[1]["channel_id"], data_test_users[0]["auth_user_id"])
    channel_addowner_v1(data_test_users[2]["token"], data_test_channels[2]["channel_id"], data_test_users[3]["auth_user_id"])
    channel_join_v2(data_test_users[4]["token"], data_test_channels[0]["channel_id"])

    return [data_test_users, data_test_channels]


def test_success_remove_one(create_input):
    # length of *_members for First Channel before remove
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][1]["auth_user_id"]).json() == {}

    # length of *_members for First Channel after remove; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

def test_success_remove_multiple(create_input):
    # Add extra owner to First Channel
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][2]["auth_user_id"]).json() == {}

    # length of *_members for First Channel before remove
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 3
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][1]["auth_user_id"]).json() == {}
    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][2]["auth_user_id"]).json() == {}

    # length of *_members for First Channel after remove; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4

def test_success_remove_self(create_input):
    # Add extra owner to First Channel
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][2]["auth_user_id"]).json() == {}

    # length of *_members for First Channel before remove
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 3
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][0]["auth_user_id"]).json() == {}

     # length of *_members for First Channel after remove; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 4

def test_success_remove_with_global_owner(create_input):
    # length of *_members for Third Channel before remove
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["all_members"]) == 2

    # Global owner is not part of Third Channel, yet can still remove owners 
    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][2]["channel_id"], create_input[0][2]["auth_user_id"]).json() == {}

    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][2]["channel_id"]).json()["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][2]["channel_id"]).json()["all_members"]) == 2

def test_fail_user_not_owner(create_input):
    # length of *_members for First Channel
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][4]["auth_user_id"]).status_code == INPUT_ERROR

def test_fail_user_only_owner(create_input):
    # length of *_members for First Channel
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"]).json()["all_members"]) == 3

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][1]["auth_user_id"]).json() == {}

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][0]["auth_user_id"]).status_code == INPUT_ERROR

def test_fail_no_permission(create_input):
    # length of *_members for Third Channel before remove
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"]).json()["all_members"]) == 2

    assert channel_join_v2(create_input[0][4]["token"], create_input[1][2]["channel_id"]).json() == {}

    assert channel_removeowner_v1(create_input[0][4]["token"], create_input[1][2]["channel_id"], create_input[0][2]["auth_user_id"]).status_code == ACCESS_ERROR

def test_channel_id_invalid(create_input):
    # channel_id 5 has not been created
    assert channel_removeowner_v1(create_input[0][0]["token"], 5, create_input[0][1]["auth_user_id"]).status_code == INPUT_ERROR

def test_token_invalid(create_input):
    # token does not exist
    assert channel_removeowner_v1("invalidtoken", create_input[1][0]["channel_id"], create_input[0][0]["auth_user_id"]).status_code == ACCESS_ERROR

def test_uid_invalid(create_input):
    # u_id 20 does not exist
    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], 20).status_code == INPUT_ERROR

def test_all_invalid(create_input):
    # token, channel_id, u_id do not exist,
    # ACCESS_ERROR is prioritised
    assert channel_removeowner_v1("anotherinvalidtoken", 321, 13).status_code == ACCESS_ERROR
