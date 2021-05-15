import pytest
import requests
from src import config
from http_tests.helper_function_for_http_test import auth_register_v2, channel_messages_v2, channel_join_v2, channel_leave_v1, channel_invite_v2, channels_create_v2, channels_list_v2, message_send_v2, message_senddm_v1, dm_create_v1, dm_leave_v1, dm_invite_v1, clear_v1, search_v2, dm_messages_v1

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
    ]

    data_test_dms = [
        dm_create_v1(data_test_users[0]["token"], [data_test_users[1]["auth_user_id"], data_test_users[2]["auth_user_id"]]).json(),
        dm_create_v1(data_test_users[3]["token"], [data_test_users[0]["auth_user_id"], data_test_users[4]["auth_user_id"]]).json(),
    ]

    # Add everyone to First Channel
    channel_join_v2(data_test_users[1]["token"], data_test_channels[0]["channel_id"])
    channel_join_v2(data_test_users[2]["token"], data_test_channels[0]["channel_id"])
    channel_join_v2(data_test_users[3]["token"], data_test_channels[0]["channel_id"])
    channel_join_v2(data_test_users[4]["token"], data_test_channels[0]["channel_id"])

    # Add users 0 and 3 to Second Channel
    channel_join_v2(data_test_users[0]["token"], data_test_channels[1]["channel_id"])
    channel_join_v2(data_test_users[3]["token"], data_test_channels[1]["channel_id"])

    # Send messages to First Channel
    message_send_v2(data_test_users[0]["token"], data_test_channels[0]["channel_id"], "Hey there")
    message_send_v2(data_test_users[1]["token"], data_test_channels[0]["channel_id"], "Hey nice to meet you")
    message_send_v2(data_test_users[2]["token"], data_test_channels[0]["channel_id"], "I'm excited to be here!")
    message_send_v2(data_test_users[3]["token"], data_test_channels[0]["channel_id"], "Me too!")

    # Send messages to Second Channel
    message_send_v2(data_test_users[1]["token"], data_test_channels[1]["channel_id"], "hey")
    message_send_v2(data_test_users[0]["token"], data_test_channels[1]["channel_id"], "sup")
    message_send_v2(data_test_users[3]["token"], data_test_channels[1]["channel_id"], "Nice weather today aye...")

    # Send messages to dm_1
    message_senddm_v1(data_test_users[0]["token"], data_test_dms[0]["dm_id"], "Hey there")
    message_senddm_v1(data_test_users[1]["token"], data_test_dms[0]["dm_id"], "Oh hi Mark")
    message_senddm_v1(data_test_users[2]["token"], data_test_dms[0]["dm_id"], "Lol")

    # Send messages to dm_2
    message_senddm_v1(data_test_users[0]["token"], data_test_dms[1]["dm_id"], "Hey again. This is getting repetitive...")
    message_senddm_v1(data_test_users[3]["token"], data_test_dms[1]["dm_id"], "Yeah true lol")
    message_senddm_v1(data_test_users[4]["token"], data_test_dms[1]["dm_id"], "Haha")

    return [data_test_users, data_test_channels, data_test_dms]


def test_success_one_exact_match_channel(create_input):
    result = search_v2(create_input[0][1]["token"], "Hey nice to meet you").json()
    assert type(result) == dict
    assert len(result["messages"]) == 1
    assert result["messages"][0]["u_id"] == create_input[0][1]["auth_user_id"]
    assert result["messages"][0]["message"] == "Hey nice to meet you"

def test_success_one_exact_match_dm(create_input):
    result = search_v2(create_input[0][1]["token"], "Oh hi Mark").json()
    assert type(result) == dict
    assert len(result["messages"]) == 1
    assert result["messages"][0]["u_id"] == create_input[0][1]["auth_user_id"]
    assert result["messages"][0]["message"] == "Oh hi Mark"

def test_success_one_substr_match_channel(create_input):
    result = search_v2(create_input[0][3]["token"], "weather").json()
    assert type(result) == dict
    assert len(result["messages"]) == 1
    assert result["messages"][0]["u_id"] == create_input[0][3]["auth_user_id"]
    assert result["messages"][0]["message"] == "Nice weather today aye..."

def test_success_one_substr_match_dm(create_input):
    result = search_v2(create_input[0][4]["token"], "lol").json()
    assert type(result) == dict
    assert len(result["messages"]) == 1
    assert result["messages"][0]["u_id"] == create_input[0][3]["auth_user_id"]
    assert result["messages"][0]["message"] == "Yeah true lol"

def test_success_multiple_exact(create_input):
    result = search_v2(create_input[0][0]["token"], "Hey there").json()
    assert type(result) == dict
    assert len(result["messages"]) == 2
    assert result["messages"][0]["u_id"] == create_input[0][0]["auth_user_id"]
    assert result["messages"][1]["u_id"] == create_input[0][0]["auth_user_id"]
    assert result["messages"][0]["message"] == "Hey there"
    assert result["messages"][1]["message"] == "Hey there"

def test_success_multiple_substr(create_input):
    result = search_v2(create_input[0][0]["token"], "Hey").json()
    assert type(result) == dict
    assert len(result["messages"]) == 4
    assert result["messages"][0]["u_id"] == create_input[0][1]["auth_user_id"]
    assert result["messages"][1]["u_id"] == create_input[0][0]["auth_user_id"]
    assert result["messages"][2]["u_id"] == create_input[0][0]["auth_user_id"]
    assert result["messages"][3]["u_id"] == create_input[0][0]["auth_user_id"]
    assert result["messages"][0]["message"] == "Hey nice to meet you"
    assert result["messages"][1]["message"] == "Hey there"
    assert result["messages"][2]["message"] == "Hey there"
    assert result["messages"][3]["message"] == "Hey again. This is getting repetitive..."

def test_success_user_added_after_msg_send(create_input):
    assert channel_join_v2(create_input[0][4]["token"], create_input[1][1]["channel_id"]).json() == {}
    result = search_v2(create_input[0][4]["token"], "to").json()
    assert type(result) == dict
    assert len(result["messages"]) == 4
    assert result["messages"][0]["u_id"] == create_input[0][3]["auth_user_id"]
    assert result["messages"][1]["u_id"] == create_input[0][2]["auth_user_id"]
    assert result["messages"][2]["u_id"] == create_input[0][1]["auth_user_id"]
    assert result["messages"][3]["u_id"] == create_input[0][3]["auth_user_id"]
    assert result["messages"][0]["message"] == "Me too!"
    assert result["messages"][1]["message"] == "I'm excited to be here!"
    assert result["messages"][2]["message"] == "Hey nice to meet you"
    assert result["messages"][3]["message"] == "Nice weather today aye..."

def test_success_over_fifty_msgs_channel(create_input):
    for i in range(0, 110):
        message_send_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], f"First channel extra message {i}.")
    result = search_v2(create_input[0][1]["token"], "First").json()
    assert type(result) == dict
    assert len(result["messages"]) == 110

def test_success_over_fifty_msgs_dm(create_input):
    for i in range(0, 167):
        message_senddm_v1(create_input[0][3]["token"], create_input[2][1]["dm_id"], f"Second dm extra message {i}.")
    result = search_v2(create_input[0][4]["token"], "Second").json()
    assert type(result) == dict
    assert len(result["messages"]) == 167

def test_user_leave(create_input):
    assert channel_leave_v1(create_input[0][1]["token"], create_input[1][0]["channel_id"]).json() == {}
    result = search_v2(create_input[0][1]["token"], "Hey nice to meet you").json()
    assert type(result) == dict
    assert len(result["messages"]) == 0

def test_fail_over_1000(create_input):
    query = "x" * 1001
    assert search_v2(create_input[0][0]["token"], query).status_code == INPUT_ERROR

def test_fail_empty_str(create_input):
    assert search_v2(create_input[0][0]["token"], "").status_code == INPUT_ERROR

def test_invalid_token(create_input):
    assert search_v2("invalidtokenhere", "Hey").status_code == ACCESS_ERROR

