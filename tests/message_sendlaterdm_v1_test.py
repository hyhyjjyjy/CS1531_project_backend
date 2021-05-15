import pytest
import time
from src.auth import auth_register_v2
from src.dms import dm_create_v1, dm_messages_v1
from src.message import message_sendlaterdm_v1, message_senddm_v1
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

    data_test_dms = [
        dm_create_v1(data_test_users[0]["token"], [data_test_users[1]["auth_user_id"], data_test_users[2]["auth_user_id"]]),
        dm_create_v1(data_test_users[1]["token"], [data_test_users[3]["auth_user_id"]]),
    ]

    return [data_test_users, data_test_dms]


def test_simple_success(create_input):
    assert dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"] == []
    current_time = int(time.time())
    msg = message_sendlaterdm_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], "Hey there!", current_time + 2)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int

    # Make sure message has not been sent yet
    assert dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"] == []

    # Wait 2.5 seconds and check again; message should be there
    time.sleep(2.5)
    msgs = dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"]
    assert len(msgs) == 1
    assert msgs[0]["message"] == "Hey there!"
    assert msgs[0]["time_created"] == current_time + 2

def test_mixed_success(create_input):
    current_time = int(time.time())
    message_senddm_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], "This is the first normal message")
    assert len(dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"]) == 1
    msg = message_sendlaterdm_v1(create_input[0][1]["token"], create_input[1][0]["dm_id"], "Hey there, I'm from the past!", current_time + 2)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int
    message_senddm_v1(create_input[0][2]["token"], create_input[1][0]["dm_id"], "This is the second normal message")

    # Make sure delayed message has not been sent yet
    msgs = dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"]
    assert len(msgs) == 2

    # Wait 2.5 seconds and check again; delayed message should be there
    time.sleep(2.5)
    msgs = dm_messages_v1(create_input[0][1]["token"], create_input[1][0]["dm_id"], 0)["messages"]
    assert len(msgs) == 3
    assert msgs[0]["message"] == "Hey there, I'm from the past!"
    assert msgs[0]["time_created"] == current_time + 2
    assert msgs[1]["message"] == "This is the second normal message"
    assert msgs[1]["time_created"] == current_time
    assert msgs[2]["message"] == "This is the first normal message"
    assert msgs[2]["time_created"] == current_time

def test_multiple_success(create_input):
    message_senddm_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], "This is the first normal message")
    assert len(dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"]) == 1
    current_time = int(time.time())
    msg = message_sendlaterdm_v1(create_input[0][1]["token"], create_input[1][0]["dm_id"], "Hey there, I'm from the past!", current_time + 2)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int
    msg = message_sendlaterdm_v1(create_input[0][2]["token"], create_input[1][0]["dm_id"], "Hey, I'm from the distant past!", current_time + 4)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int
    msg = message_sendlaterdm_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], "Hey there, I'm from the past past!!", current_time + 3)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int
    message_senddm_v1(create_input[0][2]["token"], create_input[1][0]["dm_id"], "This is the second normal message")

    # Make sure delayed message has not been sent yet
    assert len(dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"]) == 2

    # Wait 2.5 seconds and check again; first delayed message should be there
    time.sleep(2.5)
    msgs = dm_messages_v1(create_input[0][1]["token"], create_input[1][0]["dm_id"], 0)["messages"]
    assert len(msgs) == 3
    assert msgs[0]["message"] == "Hey there, I'm from the past!"
    assert msgs[0]["time_created"] == current_time + 2
    assert msgs[1]["message"] == "This is the second normal message"
    assert msgs[1]["time_created"] == current_time
    assert msgs[2]["message"] == "This is the first normal message"
    assert msgs[2]["time_created"] == current_time

    # Wait 1 second; second delayed message should be there
    time.sleep(1)
    msgs = dm_messages_v1(create_input[0][1]["token"], create_input[1][0]["dm_id"], 0)["messages"]
    assert len(msgs) == 4
    assert msgs[0]["message"] == "Hey there, I'm from the past past!!"
    assert msgs[0]["time_created"] == current_time + 3
    assert msgs[1]["message"] == "Hey there, I'm from the past!"
    assert msgs[1]["time_created"] == current_time + 2
    assert msgs[2]["message"] == "This is the second normal message"
    assert msgs[2]["time_created"] == current_time
    assert msgs[3]["message"] == "This is the first normal message"
    assert msgs[3]["time_created"] == current_time

    # Wait 1 more second; final delayed message should be there
    time.sleep(1)
    msgs = dm_messages_v1(create_input[0][1]["token"], create_input[1][0]["dm_id"], 0)["messages"]
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
    assert dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"] == []
    current_time = int(time.time())
    msg = message_sendlaterdm_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], "Hey there!", current_time)
    assert type(msg) == dict
    assert type(msg["message_id"]) == int

    # Message should have been sent already
    msgs = dm_messages_v1(create_input[0][0]["token"], create_input[1][0]["dm_id"], 0)["messages"]
    assert len(msgs) == 1
    assert msgs[0]["message"] == "Hey there!"
    assert msgs[0]["time_created"] == current_time

def test_invalid_dm(create_input):
    with pytest.raises(InputError):
        message_sendlaterdm_v1(create_input[0][0]["token"], 123, "This message won't be sent", int(time.time()) + 2)

def test_message_too_long(create_input):
    msg = 'x' * 1001
    with pytest.raises(InputError):
        message_sendlaterdm_v1(create_input[0][1]["token"], create_input[1][1]["dm_id"], msg, int(time.time()) + 2)

def test_time_sent_past(create_input):
    with pytest.raises(InputError):
        message_sendlaterdm_v1(create_input[0][1]["token"], create_input[1][1]["dm_id"], "Hey from the future!", int(time.time()) - 20)

def test_not_member(create_input):
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(create_input[0][4]["token"], create_input[1][0]["dm_id"], "I'm not in this dm :(", int(time.time()) + 2)

def test_invalid_token(create_input):
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(123, create_input[1][1]["dm_id"], "I don't exist :(((", int(time.time()) + 2)
