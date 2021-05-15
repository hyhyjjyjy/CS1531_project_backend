import pytest
import time
from src.auth import auth_register_v2
from src.channel import channel_messages_v2, channel_join_v2
from src.channels import channels_create_v2
from src.message import message_sendlater_v1, message_send_v2
from src.other import clear_v1
from src.error import InputError, AccessError

@pytest.fixture
def create_input():
    clear_v1()

    data_test_users = [
        auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton"),
        auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong"),
        auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch"),
        auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine"),
        auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng"),
    ]

    data_test_channels = [
        channels_create_v2(data_test_users[0]["token"], "First Channel", True),
        channels_create_v2(data_test_users[1]["token"], "Second Channel", True),
    ]

    channel_join_v2(data_test_users[1]["token"], data_test_channels[0]["channel_id"])
    channel_join_v2(data_test_users[2]["token"], data_test_channels[0]["channel_id"])
    channel_join_v2(data_test_users[3]["token"], data_test_channels[1]["channel_id"])

    return [data_test_users, data_test_channels]


def test_simple_success(create_input):
    assert channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)["messages"] == []
    current_time = int(time.time())
    msg = message_sendlater_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], "Hey there!", current_time + 2)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int

    # Make sure message has not been sent yet
    assert channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)["messages"] == []

    # Wait 2.5 seconds and check again; message should be there
    time.sleep(2.5)
    msgs = channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)["messages"]
    assert len(msgs) == 1
    assert msgs[0]["message"] == "Hey there!"
    assert msgs[0]["time_created"] == current_time + 2

def test_mixed_success(create_input):
    current_time = int(time.time())
    message_send_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], "This is the first normal message")
    assert len(channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)["messages"]) == 1
    msg = message_sendlater_v1(create_input[0][1]["token"], create_input[1][0]["channel_id"], "Hey there, I'm from the past!", current_time + 2)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int
    message_send_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"], "This is the second normal message")

    # Make sure delayed message has not been sent yet
    msgs = channel_messages_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"], 0)["messages"]
    assert len(msgs) == 2

    # Wait 2.5 seconds and check again; delayed message should be there
    time.sleep(2.5)
    msgs = channel_messages_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"], 0)["messages"]
    assert len(msgs) == 3
    assert msgs[0]["message"] == "Hey there, I'm from the past!"
    assert msgs[0]["time_created"] == current_time + 2
    assert msgs[1]["message"] == "This is the second normal message"
    assert msgs[1]["time_created"] == current_time
    assert msgs[2]["message"] == "This is the first normal message"
    assert msgs[2]["time_created"] == current_time

def test_multiple_success(create_input):
    message_send_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], "This is the first normal message")
    assert len(channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)["messages"]) == 1
    current_time = int(time.time())
    msg = message_sendlater_v1(create_input[0][1]["token"], create_input[1][0]["channel_id"], "Hey there, I'm from the past!", current_time + 2)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int
    msg = message_sendlater_v1(create_input[0][2]["token"], create_input[1][0]["channel_id"], "Hey, I'm from the distant past!", current_time + 4)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int
    msg = message_sendlater_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], "Hey there, I'm from the past past!!", current_time + 3)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int
    message_send_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"], "This is the second normal message")

    # Make sure delayed message has not been sent yet
    assert len(channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)["messages"]) == 2

    # Wait 2.5 seconds and check again; first delayed message should be there
    time.sleep(2.5)
    msgs = channel_messages_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"], 0)["messages"]
    assert len(msgs) == 3
    assert msgs[0]["message"] == "Hey there, I'm from the past!"
    assert msgs[0]["time_created"] == current_time + 2
    assert msgs[1]["message"] == "This is the second normal message"
    assert msgs[1]["time_created"] == current_time
    assert msgs[2]["message"] == "This is the first normal message"
    assert msgs[2]["time_created"] == current_time

    # Wait 1 second; second delayed message should be there
    time.sleep(1)
    msgs = channel_messages_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"], 0)["messages"]
    assert len(msgs) == 4
    assert msgs[0]["message"] == "Hey there, I'm from the past past!!"
    assert msgs[0]["time_created"] == current_time + 3
    assert msgs[1]["message"] == "Hey there, I'm from the past!"
    assert msgs[1]["time_created"] == current_time + 2
    assert msgs[2]["message"] == "This is the second normal message"
    assert msgs[2]["time_created"] == current_time
    assert msgs[3]["message"] == "This is the first normal message"
    assert msgs[3]["time_created"] == current_time

    # Wait 1 more seconds; final delayed message should be there
    time.sleep(1)
    msgs = channel_messages_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"], 0)["messages"]
    assert len(msgs) == 5
    assert msgs[0]["message"] == "Hey, I'm from the distant past!"
    assert msgs[0]["time_created"] == current_time + 4
    assert msgs[1]["message"] == "Hey there, I'm from the past past!!"
    assert msgs[1]["time_created"] == current_time + 3
    assert msgs[2]["message"] == "Hey there, I'm from the past!"
    assert msgs[2]["time_created"] == current_time + 2
    assert msgs[3]["message"] == "This is the second normal message"
    assert msgs[3]["time_created"] == current_time
    assert msgs[4]["message"] == "This is the first normal message"
    assert msgs[4]["time_created"] == current_time

def test_success_no_delay(create_input):
    assert channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)["messages"] == []
    current_time = int(time.time())
    msg = message_sendlater_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], "Hey there!", current_time)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int

    # Message should have been sent already
    msgs = channel_messages_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"], 0)["messages"]
    assert len(msgs) == 1
    assert msgs[0]["message"] == "Hey there!"
    assert msgs[0]["time_created"] == current_time

def test_invalid_channel(create_input):
    with pytest.raises(InputError):
        message_sendlater_v1(create_input[0][0]["token"], 123, "This message won't be sent", int(time.time()) + 2)

def test_message_too_long(create_input):
    msg = 'x' * 1001
    with pytest.raises(InputError):
        message_sendlater_v1(create_input[0][1]["token"], create_input[1][1]["channel_id"], msg, int(time.time()) + 2)

def test_time_sent_past(create_input):
    with pytest.raises(InputError):
        message_sendlater_v1(create_input[0][1]["token"], create_input[1][1]["channel_id"], "Hey from the future!", int(time.time()) - 20)

def test_not_member(create_input):
    with pytest.raises(AccessError):
        message_sendlater_v1(create_input[0][4]["token"], create_input[1][0]["channel_id"], "I'm not in this channel :(", int(time.time()) + 2)

def test_invalid_token(create_input):
    with pytest.raises(AccessError):
        message_sendlater_v1(123, create_input[1][1]["channel_id"], "I don't exist :(((", int(time.time()) + 2)
