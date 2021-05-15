from src.auth import findUser, writeData, getData
from src.error import InputError, AccessError
from src.wrapper import Authorisation


@Authorisation
def admin_user_remove_v1(token, u_id):
    """
    Given a User by their user ID, remove the user from the Dreams. Dreams
    owners can remove other **Dreams** owners (including the original first
    owner). Once users are removed from **Dreams**, the contents of the messages
    they sent will be replaced by 'Removed user'. Their profile must still be
    retrievable with user/profile/v2, with their name replaced by 'Removed user'

    Arguments:
        token (str) - token passed in to the function
        u_id (int)  - id of user to remove

    Exceptions:
        AccessError - when token passed in is not a valid id
        InputError  - when u_id does not refer to a valid user
        InputError  - when the user is currently the only owner
        AccessError - when the authorised user is not an owner

    Return value:
        {}
    """

    data_store = getData()

    # Check for exceptions
    # validate token
    auth_user_id = findUser(token)

    # check if u_id is a valid user, and also get index of position if valid
    valid = False
    for user_index, user in enumerate(data_store["users"]):
        if user["u_id"] == u_id:
            valid = True
            break

    if not valid:
        raise InputError(description="u_id does not refer to a valid user")

    # Check if authorised user is an owner (with permission 1)
    for user in data_store["users"]:
        if user["u_id"] == auth_user_id:
            if user["permission_id"] != 1:
                raise AccessError(description="Authorised user is not an owner.")
            break

    # Check if the user is currently the only owner
    if get_dream_owners_count(data_store) == 1 and auth_user_id == u_id:
        raise InputError(description="user is currently the only owner.")

    # Move user dictionary from users list to removed_users list
    data_store["removed_users"].append(data_store["users"][user_index])
    del data_store["users"][user_index]

    # Remove user from all channels
    for channel in data_store["channels"]:
        for member in channel["all_members"]:
            if member["u_id"] == u_id:
                channel["all_members"].remove(member)
                break
        for owner in channel["owner_members"]:
            if owner["u_id"] == u_id:
                channel["owner_members"].remove(owner)
                break

    # Remove user from all dms
    for dm in data_store["dms"]:
        for member in dm["dm_members"]:
            if member == u_id:
                dm["dm_members"].remove(member)
                break

    # Replace name of user with "Removed user", and also clear token and
    # session lists
    removed_user_index = len(data_store["removed_users"]) - 1
    removed_user_profile = data_store["removed_users"][removed_user_index]

    removed_user_profile["name_first"] = "Removed user"
    removed_user_profile["name_last"] = ""
    removed_user_profile["token_list"] = []
    removed_user_profile["sessions_lists"] = []

    # Replace the contents that the user sent with "Removed user"
    for user_message in data_store["messages"]:
        if user_message["u_id"] == u_id:
            user_message["message"] = "Removed user"

    writeData(data_store)

    return {}


@Authorisation
def admin_userpermission_change_v1(token, u_id, permission_id):
    """
    Given a User by their user ID, set their permissions to new permissions
    described by permission_id.

    Arguments:
        token (str)          - token passed in to the function
        u_id (int)           - id of user to change permission of
        permission_id (int)  - new permission id

    Exceptions:
        AccessError - when token passed in is not a valid id
        InputError  - when u_id does not refer to a valid user
        InputError  - when permission_id does not refer to a valid permission
        AccessError - when authorised user is not an owner

    Return value:
        {}
    """

    data_store = getData()

    # Check for exceptions
    # validate token
    auth_user_id = findUser(token)

    # check if u_id is a valid user, and also get index of position if valid
    valid = False
    for user_index, user in enumerate(data_store["users"]):
        if user["u_id"] == u_id:
            valid = True
            break

    if not valid:
        raise InputError(description="u_id does not refer to a valid user")

    # Check permission_id is valid
    if permission_id != 1 and permission_id != 2:
        raise InputError(description="Invalid permission_id")

    # Check if authorised user is an owner (with permission 1)
    for user in data_store["users"]:
        if user["u_id"] == auth_user_id:
            if user["permission_id"] != 1:
                raise AccessError(description="Authorised user is not an owner.")

    # Cannot change permission to permission_id 2 if there is only one
    # owner remaining in Dreams
    if permission_id == 2:
        if get_dream_owners_count(data_store) > 1:
            data_store["users"][user_index]["permission_id"] = permission_id
    else:
        data_store["users"][user_index]["permission_id"] = permission_id

    writeData(data_store)

    return {}


def get_dream_owners_count(data_store):
    count = 0

    for user in data_store["users"]:
        if user["permission_id"] == 1:
            count += 1

    return count