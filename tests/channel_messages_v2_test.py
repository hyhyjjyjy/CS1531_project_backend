import pytest

from src.auth import auth_register_v2
from src.channel import channel_messages_v2
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.other import clear_v1
from src.error import InputError, AccessError

@pytest.fixture
def create_input():
    clear_v1()

    data_test_users = [auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton"),
        auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong"),
        auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch"),
        auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine"),
        auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng"),
    ]

    data_test_channels = [channels_create_v2(data_test_users[0]["token"], "First Channel", True),
        channels_create_v2(data_test_users[1]["token"], "Second Channel", True),
        channels_create_v2(data_test_users[2]["token"], "Third Channel", False),
    ]

    # Send 10 messages to First Channel
    for i in range(0, 10):
        message_send_v2(data_test_users[0]["token"], data_test_channels[0]["channel_id"], f"First channel message {i}.")

    # Send 55 messages to Second Channel
    for i in range(0, 55):
        message_send_v2(data_test_users[1]["token"], data_test_channels[1]["channel_id"], f"Second channel message {i}.")

    # Send 120 messages to Third Channel
    for i in range(0, 120):
        message_send_v2(data_test_users[2]["token"], data_test_channels[2]["channel_id"], f"Third channel message {i}.")

    return [data_test_users, data_test_channels]


def test_success_less_than_fifty(create_input):
    results = channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)
    assert type(results) == dict
    assert len(results["messages"]) == 10
    assert results["messages"][0]["u_id"] == create_input[0][0]["auth_user_id"]
    assert results["messages"][0]["message"] == "First channel message 9."      # Most recent message is last one sent
    assert results["start"] == 0
    assert results["end"] == -1

def test_success_more_than_fifty(create_input):
    results = channel_messages_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"], 0)
    assert type(results) == dict
    assert len(results["messages"]) == 50
    assert results["messages"][1]["u_id"] == create_input[0][1]["auth_user_id"]
    assert results["messages"][1]["message"] == "Second channel message 53."
    assert results["start"] == 0
    assert results["end"] == 50

    results = channel_messages_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"], 50)
    assert type(results) == dict
    assert len(results["messages"]) == 5
    assert results["messages"][2]["u_id"] == create_input[0][1]["auth_user_id"]
    assert results["messages"][2]["message"] == "Second channel message 2."
    assert results["start"] == 50
    assert results["end"] == -1

def test_success_more_than_hundred(create_input):
    results = channel_messages_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"], 0)
    assert type(results) == dict
    assert len(results["messages"]) == 50
    assert results["messages"][2]["u_id"] == create_input[0][2]["auth_user_id"]
    assert results["messages"][2]["message"] == "Third channel message 117."
    assert results["start"] == 0
    assert results["end"] == 50

    results = channel_messages_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"], 50)
    assert type(results) == dict
    assert len(results["messages"]) == 50
    assert results["messages"][2]["u_id"] == create_input[0][2]["auth_user_id"]
    assert results["messages"][0]["message"] == "Third channel message 69."
    assert results["start"] == 50
    assert results["end"] == 100

    results = channel_messages_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"], 100)
    assert type(results) == dict
    assert len(results["messages"]) == 20
    assert results["messages"][0]["u_id"] == create_input[0][2]["auth_user_id"]
    assert results["messages"][0]["message"] == "Third channel message 19."
    assert results["start"] == 100
    assert results["end"] == -1

def test_success_start_not_zero_less_fifty(create_input):
    results = channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 6)
    assert type(results) == dict
    assert len(results["messages"]) == 4
    assert results["messages"][0]["u_id"] == create_input[0][0]["auth_user_id"]
    assert results["messages"][0]["message"] == "First channel message 3."
    assert results["messages"][3]["message"] == "First channel message 0."
    assert results["start"] == 6
    assert results["end"] == -1

def test_success_start_not_zero_more_fifty(create_input):
    results = channel_messages_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"], 48)
    assert type(results) == dict
    assert len(results["messages"]) == 7
    assert results["messages"][0]["u_id"] == create_input[0][1]["auth_user_id"]
    assert results["messages"][0]["message"] == "Second channel message 6."
    assert results["start"] == 48
    assert results["end"] == -1

    results = channel_messages_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"], 60)
    assert type(results) == dict
    assert len(results["messages"]) == 50
    assert results["messages"][0]["u_id"] == create_input[0][2]["auth_user_id"]
    assert results["messages"][0]["message"] == "Third channel message 59."
    assert results["start"] == 60
    assert results["end"] == 110

    results = channel_messages_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"], 110)
    assert type(results) == dict
    assert len(results["messages"]) == 10
    assert results["messages"][0]["u_id"] == create_input[0][2]["auth_user_id"]
    assert results["messages"][0]["message"] == "Third channel message 9."
    assert results["start"] == 110
    assert results["end"] == -1

def test_start_greater_than_total_messages(create_input):
    with pytest.raises(InputError):
        channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 23)
        channel_messages_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"], 77)
        channel_messages_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"], 4235)

def test_not_member(create_input):
    with pytest.raises(AccessError):
        channel_messages_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"], 0)
        channel_messages_v2(create_input[0][1]["token"], create_input[1][2]["channel_id"], 0)
        channel_messages_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"], 0)

def test_channel_id_invalid(create_input):
    # channel_id 5 has not been created
    with pytest.raises(InputError):
        channel_messages_v2(create_input[0][0]["token"], 5, 0)

def test_token_invalid(create_input):
    # token does not exist
    with pytest.raises(AccessError):
        channel_messages_v2("invalidtoken", create_input[1][0]["channel_id"], 0)
