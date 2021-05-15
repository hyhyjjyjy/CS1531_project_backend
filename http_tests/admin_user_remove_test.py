import pytest
import requests
from src import config

from http_tests.helper_function_for_http_test import clear_v1
from http_tests.helper_function_for_http_test import dm_messages_v1, dm_create_v1, dm_invite_v1, dm_details_v1
from http_tests.helper_function_for_http_test import message_send_v2, message_senddm_v1
from http_tests.helper_function_for_http_test import user_profile_v2, users_all_v1
from http_tests.helper_function_for_http_test import (
    channels_create_v2,
    channels_list_v2,
    channel_messages_v2,
    channel_join_v2,
    channel_invite_v2,
    channel_details_v2,
)
from http_tests.helper_function_for_http_test import (
    auth_register_v2,
    admin_user_remove_v1,
    admin_userpermission_change_v1,
)

SUCCESS = 200
INPUT_ERROR = 400
ACCESS_ERROR = 403


@pytest.fixture
def create_input():
    clear_v1()

    data_test_users = [
        auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json(),
        auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json(),
        auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong").json(),
        auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch").json(),
        auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine").json(),
    ]

    data_test_channels = [
        channels_create_v2(data_test_users[0]["token"], "Channel 1", True).json(),
        channels_create_v2(data_test_users[1]["token"], "Private", False).json(),
    ]

    # User1, User3, User 4 in channel 1
    # User2, User 5 in channel 2
    channel_join_v2(data_test_users[2]["token"], data_test_channels[0]["channel_id"])
    channel_join_v2(data_test_users[3]["token"], data_test_channels[0]["channel_id"])
    channel_invite_v2(
        data_test_users[1]["token"], data_test_channels[1]["channel_id"], data_test_users[4]["auth_user_id"]
    )

    # User 1, user3, user4 sends a message to channel 1
    # User2, user5 sends a message to channel 2
    data_test_channel_messages = [
        message_send_v2(
            data_test_users[0]["token"],
            data_test_channels[0]["channel_id"],
            "Look, I was gonna go easy on you \
                                 Not to hurt your feelings \
                                 But I'm only going to get this one chance \
                                 Something's wrong, I can feel it",
        ).json(),
        message_send_v2(
            data_test_users[1]["token"],
            data_test_channels[1]["channel_id"],
            "Can we pretend that airplanes in the night \
                                 sky are like shootin' stars \
                                 I could really use a wish right now, wish right \
                                 now, wish right now Can we pretend that \
                                 airplanes in the night sky are like shootin'",
        ).json(),
        message_send_v2(
            data_test_users[2]["token"],
            data_test_channels[0]["channel_id"],
            "All I want is nothing more \
                                  To hear you knocking at my door \
                                  'Cause if I could see your face once more \
                                  I could die a happy man I'm sure",
        ).json(),
        message_send_v2(
            data_test_users[3]["token"],
            data_test_channels[0]["channel_id"],
            "I've been staring at the edge of the water \
                                  'Long as I can remember \
                                  Never really knowing why",
        ).json(),
        message_send_v2(
            data_test_users[4]["token"],
            data_test_channels[1]["channel_id"],
            "I am so so so so so sick of writing these tests \
                                  someone please send help i am so tired lol.",
        ).json(),
    ]

    # user 1 has dm with user 2
    # user 3 has dm with user 4
    # user 5 has dm with user 2
    data_test_dms = [
        dm_create_v1(data_test_users[0]["token"], [data_test_users[1]["auth_user_id"]]).json(),
        dm_create_v1(data_test_users[2]["token"], [data_test_users[3]["auth_user_id"]]).json(),
        dm_create_v1(data_test_users[4]["token"], [data_test_users[1]["auth_user_id"]]).json(),
    ]

    # user 1, user_2 sends dm to dm_1
    # user 3, user 4 sends dm to dm_2
    # user 5 sends dm to dm_3
    data_test_dm_messages = [
        message_senddm_v1(data_test_users[0]["token"], data_test_dms[0]["dm_id"], "Hello user 2!").json(),
        message_senddm_v1(data_test_users[1]["token"], data_test_dms[0]["dm_id"], "Hi user 1!").json(),
        message_senddm_v1(data_test_users[2]["token"], data_test_dms[1]["dm_id"], "How are you user 4?").json(),
        message_senddm_v1(data_test_users[3]["token"], data_test_dms[1]["dm_id"], "I am fine user 3!").json(),
        message_senddm_v1(data_test_users[4]["token"], data_test_dms[2]["dm_id"], "Shut up user 2.").json(),
    ]

    return [data_test_users, data_test_channels, data_test_channel_messages, data_test_dms, data_test_dm_messages]


def test_successful_remove(create_input):
    user_1, user_2, user_3, user_4, user_5 = create_input[0]

    assert admin_user_remove_v1(user_1["token"], user_2["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_3["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_4["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_5["auth_user_id"]).status_code == SUCCESS

    # check to see that these users are indeed removed

    # only user_1 should be shown when calling users_all
    assert users_all_v1(user_1["token"]).json() == {
        "users": [user_profile_v2(user_1["token"], user_1["auth_user_id"]).json()["user"]]
    }

    # calling channels list should raise an input error as their u_id's are invalid
    assert channels_list_v2(user_2["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_3["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_4["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_5["token"]).status_code == ACCESS_ERROR

    # Check to see each removed user's profile is retrievable and their name is
    # now 'Removed user'
    for user in [user_2, user_3, user_4, user_5]:
        user_profile = user_profile_v2(user_1["token"], user["auth_user_id"]).json()
        assert type(user_profile) == dict
        assert (
            f"{user_profile['user']['name_first']}{user_profile['user']['name_last']}" == "Removed user"
            or f"{user_profile['user']['name_first']} {user_profile['user']['name_last']}" == "Removed user"
        )

    # CHECK THAT MESSAGES SENT ARE 'REMOVED USER'
    # check channel messages for user 2
    channel_join_v2(user_1["token"], create_input[1][1]["channel_id"])
    channel_1_messages = channel_messages_v2(user_1["token"], create_input[1][1]["channel_id"], 0).json()
    for message in channel_1_messages["messages"]:
        if message["message_id"] == create_input[2][1]:
            assert message["message"] == "Removed user"

    # check channel messages for user 3
    channel_join_v2(user_1["token"], create_input[1][0]["channel_id"])
    channel_2_messages = channel_messages_v2(user_1["token"], create_input[1][0]["channel_id"], 0).json()
    for message in channel_2_messages["messages"]:
        if message["message_id"] == create_input[2][2]:
            assert message["message"] == "Removed user"

    clear_v1()


def test_invalid_u_id():
    """Raise an input error when u_id does not refer to a valid user id"""
    clear_v1()

    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json()
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json()

    assert admin_user_remove_v1(user_1["token"], user_1["auth_user_id"] + 5).status_code == INPUT_ERROR
    assert admin_user_remove_v1(user_1["token"], user_1["auth_user_id"] + 50).status_code == INPUT_ERROR
    assert admin_user_remove_v1(user_1["token"], user_2["auth_user_id"] + 1).status_code == INPUT_ERROR
    assert admin_user_remove_v1(user_1["token"], user_2["auth_user_id"] + 50).status_code == INPUT_ERROR
    assert admin_user_remove_v1(user_1["token"], user_2["auth_user_id"] + 500).status_code == INPUT_ERROR

    clear_v1()


def test_only_owner():
    """Raise an input error when the user is currently the only owner"""
    clear_v1()

    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json()

    assert admin_user_remove_v1(user_1["token"], user_1["auth_user_id"]).status_code == INPUT_ERROR

    clear_v1()


def test_auth_not_owner():
    """Raise an access error when the authorised user is not an owner"""
    clear_v1()

    # Register the Dreams owner first
    auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng")
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json()
    user_3 = auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong").json()

    assert admin_user_remove_v1(user_2["token"], user_3["auth_user_id"]).status_code == ACCESS_ERROR
    assert admin_user_remove_v1(user_3["token"], user_2["auth_user_id"]).status_code == ACCESS_ERROR

    clear_v1()


def test_invalid_token():
    """Raise an access error when the token passed in does not refer to a
    valid user
    """
    clear_v1()

    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json()
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json()

    assert admin_user_remove_v1(user_1["token"] + "bug", user_2["auth_user_id"]).status_code == ACCESS_ERROR
    assert admin_user_remove_v1(user_1["token"] + "yum", user_2["auth_user_id"]).status_code == ACCESS_ERROR
    assert admin_user_remove_v1(user_1["token"] + "discodisco", user_2["auth_user_id"]).status_code == ACCESS_ERROR
    assert admin_user_remove_v1(user_1["token"] + "34897", user_2["auth_user_id"]).status_code == ACCESS_ERROR
    assert admin_user_remove_v1(user_1["token"] + "t", user_2["auth_user_id"]).status_code == ACCESS_ERROR

    clear_v1()


def test_remove_already_removed(create_input):
    """Trying to remove an already removed user should raise an input error."""
    user_1, user_2, user_3, user_4, user_5 = create_input[0]

    assert admin_user_remove_v1(user_1["token"], user_2["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_3["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_4["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_5["auth_user_id"]).status_code == SUCCESS

    assert admin_user_remove_v1(user_1["token"], user_2["auth_user_id"]).status_code == INPUT_ERROR
    assert admin_user_remove_v1(user_1["token"], user_3["auth_user_id"]).status_code == INPUT_ERROR
    assert admin_user_remove_v1(user_1["token"], user_4["auth_user_id"]).status_code == INPUT_ERROR
    assert admin_user_remove_v1(user_1["token"], user_5["auth_user_id"]).status_code == INPUT_ERROR

    clear_v1()


def test_remove_dreams_owner(create_input):
    """Test to see we can also remove dreams owners, as long as they are not the
    last owner.
    """

    user_1, user_2, user_3, user_4, user_5 = create_input[0]

    admin_userpermission_change_v1(user_1["token"], user_2["auth_user_id"], 1)
    admin_userpermission_change_v1(user_1["token"], user_3["auth_user_id"], 1)
    admin_userpermission_change_v1(user_1["token"], user_4["auth_user_id"], 1)
    admin_userpermission_change_v1(user_1["token"], user_5["auth_user_id"], 1)

    assert admin_user_remove_v1(user_1["token"], user_2["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_3["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_4["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_5["auth_user_id"]).status_code == SUCCESS

    # only user_1 should be shown when calling users_all
    assert users_all_v1(user_1["token"]).json() == {
        "users": [user_profile_v2(user_1["token"], user_1["auth_user_id"]).json()["user"]]
    }

    # check to see that these users are indeed removed
    # calling channels list should raise an input error as their u_ids's are invalid
    assert channels_list_v2(user_2["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_3["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_4["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_5["token"]).status_code == ACCESS_ERROR

    # Check to see each removed user's profile is retrievable and their name is
    # now 'Removed user'
    for user in [user_2, user_3, user_4, user_5]:
        user_profile = user_profile_v2(user_1["token"], user["auth_user_id"]).json()
        assert type(user_profile) == dict
        assert (
            f"{user_profile['user']['name_first']}{user_profile['user']['name_last']}" == "Removed user"
            or f"{user_profile['user']['name_first']} {user_profile['user']['name_last']}" == "Removed user"
        )

    # CHECK THAT MESSAGES SENT ARE 'REMOVED USER'
    # check channel messages for user 2
    channel_join_v2(user_1["token"], create_input[1][1]["channel_id"])
    channel_1_messages = channel_messages_v2(user_1["token"], create_input[1][1]["channel_id"], 0).json()
    for message in channel_1_messages["messages"]:
        if message["message_id"] == create_input[2][1]:
            assert message["message"] == "Removed user"

    # check channel messages for user 3
    channel_join_v2(user_1["token"], create_input[1][0]["channel_id"])
    channel_2_messages = channel_messages_v2(user_1["token"], create_input[1][0]["channel_id"], 0).json()
    for message in channel_2_messages["messages"]:
        if message["message_id"] == create_input[2][2]:
            assert message["message"] == "Removed user"

    clear_v1()


def test_remove_self(create_input):
    """An owner should be allowed to remove themselves with no errors
    as long as they are not the last owner left
    """

    user_1, user_2, user_3, user_4, user_5 = create_input[0]

    admin_userpermission_change_v1(user_1["token"], user_2["auth_user_id"], 1)
    admin_userpermission_change_v1(user_1["token"], user_3["auth_user_id"], 1)
    admin_userpermission_change_v1(user_1["token"], user_4["auth_user_id"], 1)
    admin_userpermission_change_v1(user_1["token"], user_5["auth_user_id"], 1)

    assert admin_user_remove_v1(user_2["token"], user_2["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_3["token"], user_3["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_4["token"], user_4["auth_user_id"]).status_code == SUCCESS
    assert admin_user_remove_v1(user_1["token"], user_1["auth_user_id"]).status_code == SUCCESS

    # only user_5 should be shown when calling users_all
    assert users_all_v1(user_5["token"]).json() == {
        "users": [user_profile_v2(user_5["token"], user_5["auth_user_id"]).json()["user"]]
    }

    # check to see that these users are indeed removed
    # calling channels list should raise an input error as their u_id's are invalid
    assert channels_list_v2(user_2["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_3["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_4["token"]).status_code == ACCESS_ERROR
    assert channels_list_v2(user_1["token"]).status_code == ACCESS_ERROR

    # Check to see each removed user's profile is retrievable and their name is
    # now 'Removed user'
    for user in [user_1, user_2, user_3, user_4]:
        user_profile = user_profile_v2(user_5["token"], user["auth_user_id"]).json()
        assert type(user_profile) == dict
        assert (
            f"{user_profile['user']['name_first']}{user_profile['user']['name_last']}" == "Removed user"
            or f"{user_profile['user']['name_first']} {user_profile['user']['name_last']}" == "Removed user"
        )

    # CHECK THAT MESSAGES SENT ARE 'REMOVED USER'
    # check channel messages for user 2
    channel_join_v2(user_5["token"], create_input[1][1]["channel_id"])
    channel_1_messages = channel_messages_v2(user_5["token"], create_input[1][1]["channel_id"], 0).json()
    for message in channel_1_messages["messages"]:
        if message["message_id"] == create_input[2][1]:
            assert message["message"] == "Removed user"

    # check channel messages for user 3
    channel_join_v2(user_5["token"], create_input[1][0]["channel_id"])
    channel_2_messages = channel_messages_v2(user_5["token"], create_input[1][0]["channel_id"], 0).json()
    for message in channel_2_messages["messages"]:
        if message["message_id"] == create_input[2][2]:
            assert message["message"] == "Removed user"

    clear_v1()


def test_removed_dms():
    """Tests that sent dm messages are now 'Removed user' after the user is
    removed
    """
    clear_v1()
    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json()
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json()

    dm_1 = dm_create_v1(user_1["token"], [user_2["auth_user_id"]]).json()

    message_senddm_v1(user_1["token"], dm_1["dm_id"], "Hello user 2!")
    message_2 = message_senddm_v1(user_2["token"], dm_1["dm_id"], "Nice to meet you user 1").json()
    message_senddm_v1(user_2["token"], dm_1["dm_id"], "you are a donkey :)")

    assert admin_user_remove_v1(user_1["token"], user_2["auth_user_id"]).status_code == SUCCESS

    dm_1_messages = dm_messages_v1(user_1["token"], dm_1["dm_id"], 0).json()
    for dm in dm_1_messages["messages"]:
        if dm["message_id"] == message_2["message_id"]:
            assert dm["message"] == "Removed user"

    clear_v1()


def test_removed_from_channel():
    """Tests that a user is removed from a channel"""
    clear_v1()
    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json()
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json()

    channel_1 = channels_create_v2(user_1["token"], "Test", True).json()
    channel_join_v2(user_2["token"], channel_1["channel_id"])

    admin_user_remove_v1(user_1["token"], user_2["auth_user_id"])

    members = channel_details_v2(user_1["token"], channel_1["channel_id"]).json()["all_members"]

    assert user_2["auth_user_id"] not in [m["u_id"] for m in members]


def test_removed_from_dm():
    """Tests that a user is removed from a dm"""
    clear_v1()
    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json()
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json()

    dm_1 = dm_create_v1(user_1["token"], []).json()
    dm_invite_v1(user_1["token"], dm_1["dm_id"], user_2["auth_user_id"])

    admin_user_remove_v1(user_1["token"], user_2["auth_user_id"])

    members = dm_details_v1(user_1["token"], dm_1["dm_id"]).json()["members"]

    assert user_2["auth_user_id"] not in [m["u_id"] for m in members]


def test_remove_from_users_all():
    """ Tests that a user is removed from users_all list"""
    clear_v1()
    user_1 = auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng").json()
    user_2 = auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton").json()

    admin_user_remove_v1(user_1["token"], user_2["auth_user_id"])
    users = users_all_v1(user_1["token"]).json()["users"]

    assert user_2["auth_user_id"] not in [u["u_id"] for u in users]
