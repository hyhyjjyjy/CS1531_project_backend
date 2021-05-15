import pytest
from src.auth import auth_register_v2
from src.channel import channel_removeowner_v1, channel_addowner_v1, channel_join_v2, channel_details_v2
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

    channel_addowner_v1(data_test_users[0]["token"], data_test_channels[0]["channel_id"], data_test_users[1]["auth_user_id"])
    channel_addowner_v1(data_test_users[1]["token"], data_test_channels[1]["channel_id"], data_test_users[0]["auth_user_id"])
    channel_addowner_v1(data_test_users[2]["token"], data_test_channels[2]["channel_id"], data_test_users[3]["auth_user_id"])
    channel_join_v2(data_test_users[4]["token"], data_test_channels[0]["channel_id"])

    return [data_test_users, data_test_channels]


def test_success_remove_one(create_input):
    # length of *_members for First Channel before remove
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][1]["auth_user_id"]) == {}

    # length of *_members for First Channel after remove; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

def test_success_remove_multiple(create_input):
    # Add extra owner to First Channel
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][2]["auth_user_id"]) == {}

    # length of *_members for First Channel before remove
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 3
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][1]["auth_user_id"]) == {}
    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][2]["auth_user_id"]) == {}

    # length of *_members for First Channel after remove; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4

def test_success_remove_self(create_input):
    # Add extra owner to First Channel
    assert channel_addowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][2]["auth_user_id"]) == {}

    # length of *_members for First Channel before remove
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 3
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][0]["auth_user_id"]) == {}

     # length of *_members for First Channel after remove; testing for all users
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][1]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][4]["token"], create_input[1][0]["channel_id"])["all_members"]) == 4

def test_success_remove_with_global_owner(create_input):
    # length of *_members for Third Channel before remove
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["all_members"]) == 2

    # Global owner is not part of Third Channel, yet can still remove owners 
    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][2]["channel_id"], create_input[0][2]["auth_user_id"]) == {}

    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 1
    assert len(channel_details_v2(create_input[0][3]["token"], create_input[1][2]["channel_id"])["all_members"]) == 2

def test_fail_user_not_owner(create_input):
    # length of *_members for First Channel
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    with pytest.raises(InputError):
        channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][4]["auth_user_id"])

def test_fail_user_only_owner(create_input):
    # length of *_members for First Channel
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][0]["token"], create_input[1][0]["channel_id"])["all_members"]) == 3

    assert channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][1]["auth_user_id"]) == {}

    with pytest.raises(InputError):
        channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], create_input[0][0]["auth_user_id"])

def test_fail_no_permission(create_input):
    # length of *_members for Third Channel before remove
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["owner_members"]) == 2
    assert len(channel_details_v2(create_input[0][2]["token"], create_input[1][2]["channel_id"])["all_members"]) == 2

    assert channel_join_v2(create_input[0][4]["token"], create_input[1][2]["channel_id"]) == {}

    with pytest.raises(AccessError):
        channel_removeowner_v1(create_input[0][4]["token"], create_input[1][2]["channel_id"], create_input[0][2]["auth_user_id"])

def test_channel_id_invalid(create_input):
    # channel_id 5 has not been created
    with pytest.raises(InputError):
        channel_removeowner_v1(create_input[0][0]["token"], 5, create_input[0][1]["auth_user_id"])

def test_token_invalid(create_input):
    # token does not exist
    with pytest.raises(AccessError):
        channel_removeowner_v1("invalidtoken", create_input[1][0]["channel_id"], create_input[0][0]["auth_user_id"])

def test_uid_invalid(create_input):
    # u_id 20 does not exist
    with pytest.raises(InputError):
        channel_removeowner_v1(create_input[0][0]["token"], create_input[1][0]["channel_id"], 20)

def test_all_invalid(create_input):
    # token, channel_id, u_id do not exist,
    # AccessError is prioritised
    with pytest.raises(AccessError):
        channel_removeowner_v1("anotherinvalidtoken", 321, 13)
