from src.error import InputError, AccessError
from src.auth import findUser, getData, writeData
from src.notifications import new_added_notification
from src.wrapper import Authorisation
import json
import time
import datetime
from src.user import append_user_stats, append_dream_stats


INVALID_CHANNEL_ID = 0
INVALID_U_ID = 1
UNAUTHORISED_AUTH_U_ID = 2
INVALID_DM_ID = 3


@Authorisation
def channel_invite_v2(token, channel_id, u_id):
    """
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately.

    Arguments:
        token (str)           - token passed in to the function
        channel_id (int)      - the id of the channel to invite to
        u_id (int)            - the id of the user that is being invited

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel.
        InputError  - Occurs when u_id does not refer to a valid user.
        AccessError - Occurs when token pass in is not a valid id.
        AccessError - Occurs when the authorised user is not already a member of the channel.

    Return Value:
        Returns {} on successful invite

    """

    auth_user_id = findUser(token)

    database = getData()

    # Check for exceptions
    channel_index = check_validity(database["channels"], channel_id, "channel_id", INVALID_CHANNEL_ID)
    channel_src = database["channels"][channel_index]

    user_index = check_validity(database["users"], u_id, "u_id", INVALID_U_ID)
    user_src = database["users"][user_index]

    check_validity(channel_src["all_members"], auth_user_id, "u_id", UNAUTHORISED_AUTH_U_ID)

    # Only add the user if they are not already in the channel
    for member in channel_src["all_members"]:
        if u_id in member.values():
            return {}

    # Create a new dictionary for the added user with their details
    # and add them to the channel
    new_member = {
        "u_id": user_src["u_id"],
        "name_first": user_src["name_first"],
        "name_last": user_src["name_last"],
        "email": user_src["email"],
        "handle_str": user_src["handle_str"],
        "profile_img_url": user_src["profile_img_url"],
    }

    channel_src["all_members"].append(new_member)

    # Create a notification for the added user
    user_notification = new_added_notification(token, channel_id, -1, u_id)
    database["user_notifications"].append(user_notification)

    append_user_stats(u_id, database)
    append_dream_stats(u_id, database)

    writeData(database)

    return {}


@Authorisation
def channel_details_v2(token, channel_id):
    """
    Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel.

    Arguments:
        token (str)           - token passed in to the function
        channel_id (int)      - channel_id of the channel to show details of

    Exceptions:
        InputError  - Occurs when channel ID is not a valid channel.
        AccessError - Occurs when token does not refer to a valid user.
        AccessError - Occurs when authorised user is not a member of channel
                      with channel_id.

    Return Value:
        Returns a dictionary { name, owner_members, all_members } on successful
        call.

    """

    database = getData()

    auth_user_id = findUser(token)

    # Check for exceptions
    channel_index = check_validity(database["channels"], channel_id, "channel_id", INVALID_CHANNEL_ID)

    channel_src = database["channels"][channel_index]

    check_validity(channel_src["all_members"], auth_user_id, "u_id", UNAUTHORISED_AUTH_U_ID)

    # Copy details from "database" to empty dictionaries
    owner_members_list = []
    all_members_list = []

    owner_members_list = copy_channel_member_details(channel_src["owner_members"], owner_members_list, database)
    all_members_list = copy_channel_member_details(channel_src["all_members"], all_members_list, database)

    # Create and return a dictionary with copied data
    channel_details = {
        "name": channel_src.get("channel_name"),
        "owner_members": owner_members_list,
        "all_members": all_members_list,
    }

    return channel_details


@Authorisation
def channel_messages_v2(token, channel_id, start):
    """Given channel id, return up to 50 messages

    Arguments:
        token (string)              - token of an authenticated user who is
                                      part of the channel
        channel_id (integer)        - id of channel where messages come from
        start (integer)             - starting index (counting backwards, most
                                      recent messages returned first)

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
                    - Occurs when start is greater than total number of messages
        AccessError - Occurs when authorised user is not a member of the channel
                    - Occurs when token is not valid

    Return value:
        {
            messages,   - List of dictionaries,
                            where each dictionary contains types:
                            {message_id, u_id, message, time_created, reacts, is_pinned}
            start,      - integer
            end         - integer (value of start+50 or -1)
        }
    """
    current_time = int(time.time())

    # Load .json data store
    data_store = getData()

    # Check validity of channel_id
    ch_index = check_validity(data_store["channels"], channel_id, "channel_id", INVALID_CHANNEL_ID)
    ch_src = data_store["channels"][ch_index]

    # Check validity of token
    u_id = findUser(token)
    for user in data_store["users"]:
        if user["u_id"] == u_id:
            u_src = user

    # Check user is a member of channel
    check_validity(ch_src["all_members"], u_src["u_id"], "u_id", UNAUTHORISED_AUTH_U_ID)

    # Check start is less than total number of messages
    total_messages = len(ch_src["messages"])
    if total_messages > 0 and start > total_messages - 1:
        raise InputError(description="There aren't that many messages in this channel.")

    # Return type
    message_dict = {
        "messages": [],
        "start": start,
        "end": -1,
    }

    # Go through channel messages backwards
    msg_reverse = list(reversed(ch_src["messages"]))

    if start + 50 < total_messages - 1:
        message_dict["messages"] = msg_reverse[start : (start + 50)]
        message_dict["end"] = start + 50
    else:
        message_dict["messages"] = msg_reverse[start:]

    message_list = []
    for message_id in message_dict["messages"]:
        message_to_add = get_message_from_id(message_id, u_id, data_store)
        if message_to_add["time_created"] <= current_time:
            message_list.append(message_to_add)
    message_dict["messages"] = message_list

    return message_dict


@Authorisation
def channel_leave_v1(token, channel_id):
    """Given channel id, removes an authorised user from that channel.

    Arguments:
        token (string)              - token of an authenticated user
        channel_id (integer)        - id of channel to leave

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
                    - Occurs when the last owner tries to leave
        AccessError - Occurs when token refers to a user who is not
                      a member of the channel
                    - Occurs when token is not a valid

    Return value:
        {}
    """

    # Load .json data store
    data_store = getData()

    # Check validity of channel_id
    ch_index = check_validity(data_store["channels"], channel_id, "channel_id", INVALID_CHANNEL_ID)
    ch_src = data_store["channels"][ch_index]

    # Check validity of token
    u_index = findUser(token) - 1
    u_src = data_store["users"][u_index]

    # Check user is actually a member
    if not is_member(ch_src, u_src):
        raise AccessError(description="user is not a member of this channel.")

    # Check not last owner
    owner = is_owner(ch_src, u_src)
    if owner and len(ch_src["owner_members"]) == 1:
        raise InputError(description="last owner cannot leave the channel.")

    # Remove user from *_members
    user_remove = {
        "u_id": u_src["u_id"],
        "name_first": u_src["name_first"],
        "name_last": u_src["name_last"],
        "email": u_src["email"],
        "handle_str": u_src["handle_str"],
        "profile_img_url": u_src["profile_img_url"],
    }
    if owner:
        ch_src["owner_members"].remove(user_remove)
    ch_src["all_members"].remove(user_remove)

    append_user_stats(findUser(token), data_store)
    append_dream_stats(findUser(token), data_store)

    writeData(data_store)

    return {}


@Authorisation
def channel_join_v2(token, channel_id):
    """Given channel id, adds an authorised user to that channel.

    Arguments:
        token (string)              - token of an authenticated user
        channel_id (integer)        - id of channel to be joined

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
        AccessError - Occurs when channel_id refers to private channel
                      and user is not a global owner
                    - Occurs when token is not a valid id

    Return value:
        {}
    """

    # Load .json data store
    data_store = getData()

    # Check validity of channel_id
    ch_index = check_validity(data_store["channels"], channel_id, "channel_id", INVALID_CHANNEL_ID)
    ch_src = data_store["channels"][ch_index]

    # Check validity of token
    u_id = findUser(token)
    for user in data_store["users"]:
        if user["u_id"] == u_id:
            u_src = user

    # Check permissions of channel and user
    u_permission = u_src["permission_id"]

    if not ch_src["is_public"] and u_permission != 1:
        raise AccessError(description="Can't join a private channel")

    # Add user to the channel
    user_add = {
        "u_id": u_src["u_id"],
        "name_first": u_src["name_first"],
        "name_last": u_src["name_last"],
        "email": u_src["email"],
        "handle_str": u_src["handle_str"],
        "profile_img_url": u_src["profile_img_url"],
    }
    ch_src["all_members"].append(user_add)

    append_user_stats(findUser(token), data_store)
    append_dream_stats(findUser(token), data_store)

    writeData(data_store)

    return {}


@Authorisation
def channel_addowner_v1(token, channel_id, u_id):
    """Given channel id, makes a u_id owner of that channel.

    Arguments:
        token (string)              - token of an authenticated user who is
                                      either an owner of the channel or a global owner
        channel_id (integer)        - id of channel for ownership
        u_id (integer)              - id of user to be granted ownership of channel

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
                    - Occurs when u_id refers to a user who is already an owner
        AccessError - Occurs when token refers to a user who is not a global owner
                      or an owner of the target channel
                    - Occurs when token is not valid

    Return value:
        {}
    """

    # Load .json data store
    data_store = getData()

    # Check validity of channel_id
    ch_index = check_validity(data_store["channels"], channel_id, "channel_id", INVALID_CHANNEL_ID)
    ch_src = data_store["channels"][ch_index]

    # Check validity of token
    token_index = findUser(token) - 1
    token_src = data_store["users"][token_index]

    # Check validity of u_id
    u_index = check_validity(data_store["users"], u_id, "u_id", INVALID_U_ID)
    u_src = data_store["users"][u_index]

    # Check user to be added is not already an owner
    if is_owner(ch_src, u_src):
        raise InputError(description="user is already an owner of this channel.")

    # Check token user is either global owner
    # or an owner of the channel
    token_permission = token_src["permission_id"]
    if token_permission != 1 and not is_owner(ch_src, token_src):
        raise AccessError(description="token does not have permission to add owner")

    # Add user to owner_members
    owner_add = {
        "u_id": u_src["u_id"],
        "name_first": u_src["name_first"],
        "name_last": u_src["name_last"],
        "email": u_src["email"],
        "handle_str": u_src["handle_str"],
        "profile_img_url": u_src["profile_img_url"],
    }
    ch_src["owner_members"].append(owner_add)

    # If user was not originally member of channel,
    # add them to all_members too
    if not is_member(ch_src, u_src):
        ch_src["all_members"].append(owner_add)

        # Create a notification for the added user
        user_notification = new_added_notification(token, channel_id, -1, u_id)
        data_store["user_notifications"].append(user_notification)

    append_user_stats(u_id, data_store)
    append_dream_stats(u_id, data_store)

    writeData(data_store)

    return {}


@Authorisation
def channel_removeowner_v1(token, channel_id, u_id):
    """Given channel id, removes u_id from owners of the channel.

    Arguments:
        token (string)              - token of an authenticated user who is
                                      either an owner of the channel or a global owner
        channel_id (integer)        - id of channel with ownership
        u_id (integer)              - id of user to be removed of channel ownership

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
                    - Occurs when u_id refers to a user who is not an owner
                    - Occurs when u_id is currently the only owner
        AccessError - Occurs when token refers to a user who is not a global owner
                      or an owner of the target channel
                    - Occurs when token is not valid

    Return value:
        {}
    """

    # Load .json data store
    data_store = getData()

    # Check validity of channel_id
    ch_index = check_validity(data_store["channels"], channel_id, "channel_id", INVALID_CHANNEL_ID)
    ch_src = data_store["channels"][ch_index]

    # Check validity of token
    token_index = findUser(token) - 1
    token_src = data_store["users"][token_index]

    # Check validity of u_id
    u_index = check_validity(data_store["users"], u_id, "u_id", INVALID_U_ID)
    u_src = data_store["users"][u_index]

    # Check user to be removed of ownership is actually an owner
    if not is_owner(ch_src, u_src):
        raise InputError(description="user is not an owner of this channel.")

    # Check token user is either global owner or an owner of the channel
    token_permission = token_src["permission_id"]
    if token_permission != 1 and not is_owner(ch_src, token_src):
        raise AccessError(description="token does not have permission to remove owner.")

    # Check user is not the only owner
    if len(ch_src["owner_members"]) == 1:
        raise InputError(description="user is the only owner remaining.")

    # Remove user from owner_members
    owner_remove = {
        "u_id": u_src["u_id"],
        "name_first": u_src["name_first"],
        "name_last": u_src["name_last"],
        "email": u_src["email"],
        "handle_str": u_src["handle_str"],
        "profile_img_url": u_src["profile_img_url"],
    }
    ch_src["owner_members"].remove(owner_remove)

    append_user_stats(u_id, data_store)
    append_dream_stats(u_id, data_store)

    writeData(data_store)

    return {}


def check_validity(data_list, id_int, key_id, error_check):
    """
    Passes an id_int and checks if this value exists within the dictionary
    by searching through specified keys.

    Arguments:
        data_list (list)        - the list that we want to check
        id_int (int)            - the id that we want to find
        key_id (string)         - the associated key for that id
        error_check (int)       - if necessary, raises specified error:
            - INVALID_CHANNEL_ID:
                Occurs when channel_id does not refer to a valid channel.
            - INVALID_U_ID:
                Occurs when u_id does not refer to a valid user.
            - UNAUTHORISED_AUTH_U_ID:
                Occurs when the authorised user is not already a member of the channel.
            - INVALID_DM_ID:
                Occurs when dm_id does not refer to a valid dm.

    Return Value:
        Returns the index at which that id was found

    """
    valid = False
    for index, item in enumerate(data_list):
        if id_int == item[key_id]:
            valid = True
            break

    if not valid:
        if error_check == INVALID_CHANNEL_ID:
            raise InputError(description="channel_id does not refer to a valid channel.")
        elif error_check == INVALID_U_ID:
            raise InputError(description="u_id does not refer to a valid user.")
        elif error_check == UNAUTHORISED_AUTH_U_ID:
            raise AccessError(description="the authorised user is not already a member of the channel.")
        elif error_check == INVALID_DM_ID:
            raise InputError(description="dm_id does not refer to a valid dm.")

    return index


def copy_channel_member_details(src, target, data):
    for member in src:
        member_dic = {
            "u_id": member.get("u_id"),
            "name_first": member.get("name_first"),
            "name_last": member.get("name_last"),
            "email": member.get("email"),
            "handle_str": member.get("handle_str"),
            "profile_img_url": member.get("profile_img_url"),
        }
        for user in data["users"]:
            if member.get("u_id") == user["u_id"]:
                member_dic["profile_img_url"] = user["profile_img_url"]
        target.append(member_dic)
    return target


def get_message_from_id(message_id, u_id, data):
    for msg in data["messages"]:
        if msg["message_id"] == message_id:
            msg_dict = {
                "message_id": msg["message_id"],
                "u_id": msg["u_id"],
                "message": msg["message"],
                "time_created": msg["time_created"],
                "reacts": msg["reacts"],
                "is_pinned": msg["is_pinned"],
            }
            for index, reacts in enumerate(msg["reacts"]):
                if u_id in reacts["u_ids"]:
                    msg_dict["reacts"][index]["is_this_user_reacted"] = True
                else:
                    msg_dict["reacts"][index]["is_this_user_reacted"] = False

    return msg_dict


def is_owner(ch_src, user_src):
    for owners in ch_src["owner_members"]:
        if user_src["u_id"] == owners["u_id"]:
            return True
    return False


def is_member(ch_src, user_src):
    for members in ch_src["all_members"]:
        if user_src["u_id"] == members["u_id"]:
            return True
    return False
