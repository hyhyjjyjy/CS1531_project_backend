import pytest
from src.auth import auth_register_v2
from src.channel import channel_addowner_v1, channel_join_v2, channel_details_v2
from src.channels import channels_create_v2, channels_list_v2
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
        channels_create_v2(data_test_users[2]["token"], "Third Channel", True),
        channels_create_v2(data_test_users[3]["token"], "Fourth Channel", False),
    ]

    return [data_test_users, data_test_channels]


def test_success_owner_one_add(create_input):
    # length of *_members for First Channel before add
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 1

    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][1]["auth_user_id"]) == {}

    # length of *_members for First Channel after join; testing for both users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 2
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["all_members"]) == 2

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 2

def test_success_owner_multiple_add(create_input):
    # length of *_members for Second Channel before add
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["all_members"]) == 1

    assert channel_addowner_v1(create_input[0][1]["token"], create_input[1][1]["channel_id"], create_input[0][0]["auth_user_id"]) == {}
    assert channel_addowner_v1(create_input[0][1]["token"], create_input[1][1]["channel_id"], create_input[0][2]["auth_user_id"]) == {}
    assert channel_addowner_v1(create_input[0][1]["token"], create_input[1][1]["channel_id"], create_input[0][3]["auth_user_id"]) == {}

    # length of *_members for Second Channel after add; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 4
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][1]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 4
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][1]["channel_id"])["all_members"]) == 4
    with pytest.raises(AccessError):
        channel_details_v2(create_input[0][4]["token"], create_input[1][1]["channel_id"])["owner_members"]
        channel_details_v2(create_input[0][4]["token"], create_input[1][1]["channel_id"])["all_members"]

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 2 
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][2]["token"])["channels"]) == 2 
    assert len(channels_list_v2(create_input[0][3]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][4]["token"])["channels"]) == 0

def test_success_global_owner_add(create_input):
    # length of *_members for Third Channel before add
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["all_members"]) == 1

    # create_input[0][0]["token"] is a global owner; can add owners even if they aren't members of the channel
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][2]["channel_id"], create_input[0][1]["auth_user_id"]) == {}
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][2]["channel_id"], create_input[0][3]["auth_user_id"]) == {}
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][2]["channel_id"], create_input[0][0]["auth_user_id"]) == {}

    # length of *_members for Third Channel after add; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 4
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][2]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][2]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 4
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][2]["channel_id"])["all_members"]) == 4
    with pytest.raises(AccessError):
        channel_details_v2(create_input[0][4]["token"], create_input[1][2]["channel_id"])["owner_members"]
        channel_details_v2(create_input[0][4]["token"], create_input[1][2]["channel_id"])["all_members"]

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 2 
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][2]["token"])["channels"]) == 1 
    assert len(channels_list_v2(create_input[0][3]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][4]["token"])["channels"]) == 0

def test_success_private_add(create_input):
    # length of *_members for Fourth Channel before add
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][3]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][3]["channel_id"])["all_members"]) == 1

    assert channel_addowner_v1(create_input[0][3]["token"], create_input[1][3]["channel_id"], create_input[0][0]["auth_user_id"]) == {}
    assert channel_addowner_v1(create_input[0][3]["token"], create_input[1][3]["channel_id"], create_input[0][1]["auth_user_id"]) == {}

    # length of *_members for Fourth Channel after add; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][3]["channel_id"])["owner_members"]) == 3
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][3]["channel_id"])["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][3]["channel_id"])["owner_members"]) == 3 
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][3]["channel_id"])["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][3]["channel_id"])["owner_members"]) == 3
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][3]["channel_id"])["all_members"]) == 3
    with pytest.raises(AccessError):
        channel_details_v2(create_input[0][4]["token"], create_input[1][2]["channel_id"])["owner_members"]
        channel_details_v2(create_input[0][4]["token"], create_input[1][2]["channel_id"])["all_members"]

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][2]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][3]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][4]["token"])["channels"]) == 0

def test_success_user_is_member(create_input):
    # Add member to First Channel before making them owner
    assert channel_join_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]) == {}
    assert channel_join_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"]) == {}

    # length of *_members for First Channel before add
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][1]["auth_user_id"]) == {}

    # length of *_members for First Channel after add; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2 
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][2]["token"])["channels"]) == 2
    assert len(channels_list_v2(create_input[0][3]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][4]["token"])["channels"]) == 0

def test_fail_user_already_owner(create_input):
    # length of *_members for Second Channel before add
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["all_members"]) == 1

    assert channel_addowner_v1(create_input[0][1]["token"], create_input[1][1]["channel_id"], create_input[0][2]["auth_user_id"]) == {}

    with pytest.raises(InputError):
        channel_addowner_v1(create_input[0][1]["token"], create_input[1][1]["channel_id"], create_input[0][2]["auth_user_id"])

def test_fail_token_not_owner(create_input):
    # length of *_members for Second Channel before add
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["all_members"]) == 1

    with pytest.raises(AccessError):
        channel_addowner_v1(create_input[0][2]["token"], create_input[1][1]["channel_id"], create_input[0][3]["auth_user_id"])

def test_channel_id_invalid(create_input):
    # channel_id 5 has not been created
    with pytest.raises(InputError):
        channel_addowner_v1(create_input[0][0]["token"], 5, create_input[0][0]["auth_user_id"])

def test_token_invalid(create_input):
    # token does not exist
    with pytest.raises(AccessError):
        channel_addowner_v1("invalidtoken", create_input[1][0]["channel_id"], create_input[0][0]["auth_user_id"])

def test_uid_invalid(create_input):
    # u_id 10 does not exist
    with pytest.raises(InputError):
        channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], 10)

def test_all_invalid(create_input):
    # token, channel_id, u_id do not exist.
    # AccessError is prioritised
    with pytest.raises(AccessError):
        channel_addowner_v1("anotherinvalidtoken", 321, 42)
