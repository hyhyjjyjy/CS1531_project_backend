import pytest
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_details_v2, channel_leave_v1, channel_addowner_v1
from src.channels import channels_create_v2
from src.channels import channels_list_v2
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

    channel_join_v2(data_test_users[1]["token"], data_test_channels[0]["channel_id"])
    channel_join_v2(data_test_users[2]["token"], data_test_channels[0]["channel_id"])

    return [data_test_users, data_test_channels]


def test_success_one_leave(create_input):
    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    assert channel_leave_v1(create_input[0][1]["token"], create_input[1][0]["channel_id"]) == {}

    # length of *_members for First Channel after leave; testing for all involved users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["all_members"]) == 2
    with pytest.raises(AccessError):
        channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][2]["token"])["channels"]) == 2

def test_success_multiple_leave(create_input):
    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    assert channel_leave_v1(create_input[0][1]["token"], create_input[1][0]["channel_id"]) == {}
    assert channel_leave_v1(create_input[0][2]["token"], create_input[1][0]["channel_id"]) == {}

    # length of *_members for First Channel after leave; testing for all involved users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 1
    with pytest.raises(AccessError):
        channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])
        channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][2]["token"])["channels"]) == 1

def test_success_owner_leave(create_input):
    # Add another owner to First Channel
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][4]["auth_user_id"]) == {}

    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4

    # One owner leaves
    assert channel_leave_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"]) == {}

    # length of *_members for First Channel after leave; testing for all involved users
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3
    with pytest.raises(AccessError):
        channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 0
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][2]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][4]["token"])["channels"]) == 1

def test_fail_not_member(create_input):
    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    with pytest.raises(AccessError):
        channel_leave_v1(create_input[0][4]["token"], create_input[1][0]["channel_id"])

def test_fail_last_owner_leave(create_input):
    # length of *_members for First Channel before leave
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    with pytest.raises(InputError):
        channel_leave_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"])

def test_channel_id_invalid(create_input):
    # channel_id 5 has not been created
    with pytest.raises(InputError):
        channel_leave_v1(create_input[0][0]["token"], 5)

def test_token_invalid(create_input):
    # token does not exist
    with pytest.raises(AccessError):
        channel_leave_v1('insertinvalidtokenhere', create_input[1][0]["channel_id"])

def test_both_invalid(create_input):
    # token, channel_id do not exist,
    # AccessError is prioritised
    with pytest.raises(AccessError):
        channel_leave_v1('insertanotherinvalidtokenhere', 321)
