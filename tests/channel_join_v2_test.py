import pytest
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_details_v2
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

    return [data_test_users, data_test_channels]


def test_success_one_join(create_input):
    # length of *_members for First Channel before join
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 1 

    assert channel_join_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"]) == {}
    
    # length of *_members for First Channel after join; testing for both users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 2
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["all_members"]) == 2

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 1 
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 2

def test_success_multiple_join(create_input):
    # length of *_members for Second Channel before join
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["all_members"]) == 1

    assert channel_join_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"]) == {}
    assert channel_join_v2(create_input[0][2]["token"], create_input[1][1]["channel_id"]) == {}
    assert channel_join_v2(create_input[0][3]["token"], create_input[1][1]["channel_id"]) == {}

    # length of *_members for Second Channel after join; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][1]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][1]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][1]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][1]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][1]["channel_id"])["all_members"]) == 4
    with pytest.raises(AccessError):
        len(channel_details_v2(create_input[0][4]["token"], create_input[1][1]["channel_id"])["all_members"])

    # number of channels each user is a part of
    assert len(channels_list_v2(create_input[0][0]["token"])["channels"]) == 2 
    assert len(channels_list_v2(create_input[0][1]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][2]["token"])["channels"]) == 2 
    assert len(channels_list_v2(create_input[0][3]["token"])["channels"]) == 1
    assert len(channels_list_v2(create_input[0][4]["token"])["channels"]) == 0


def test_fail_private_channel(create_input):
    # length of *_members for Third Channel before join
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["all_members"]) == 1

    # AccessError becuase these users are not global owners
    with pytest.raises(AccessError):
        channel_join_v2(create_input[0][1]["token"], create_input[1][2]["channel_id"])
        channel_join_v2(create_input[0][3]["token"], create_input[1][2]["channel_id"])
        channel_join_v2(create_input[0][4]["token"], create_input[1][2]["channel_id"])

def test_success_private_channel(create_input):
    # length of *_members for Third Channel before join
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["all_members"]) == 1

    assert channel_join_v2(create_input[0][0]["token"], create_input[1][2]["channel_id"]) == {}

    # create_input[0][0] is a global owner so will pass test
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 1 
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["all_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][2]["channel_id"])["all_members"]) == 2

def test_channel_id_invalid(create_input):
    # channel_id 5 has not been created
    with pytest.raises(InputError):
        channel_join_v2(create_input[0][0]["token"], 5)

def test_token_invalid(create_input):
    # user_id 7 does not exist, so its token is invalid
    with pytest.raises(AccessError):
        channel_join_v2('insertinvalidtokenhere', create_input[1][0]["channel_id"])

def test_both_invalid(create_input):
    # user_id 21 and channel_id 321 does not exist,
    # AccessError is prioritised
    with pytest.raises(AccessError):
        channel_join_v2('insertanotherinvalidtokenhere', 321)
