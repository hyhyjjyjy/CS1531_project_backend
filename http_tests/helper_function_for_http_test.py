import requests
from src import config


def clear_v1():
    url = config.url
    return requests.delete(f"{url}clear/v1")


def auth_register_v2(email, password, name_first, name_last):
    url = config.url
    return requests.post(
        f"{url}auth/register/v2",
        json={"email": email, "password": password, "name_first": name_first, "name_last": name_last},
    )


def user_stats(token):
    url = config.url
    return requests.get(
        f"{url}/user/stats/v1",
        params={
            "token": token,
        },
    )


def users_stats(token):
    url = config.url
    return requests.get(
        f"{url}/users/stats/v1",
        params={
            "token": token,
        },
    )


def channels_create_v2(token, name, is_public):
    url = config.url
    return requests.post(f"{url}channels/create/v2", json={"token": token, "name": name, "is_public": is_public})


def channel_invite_v2(token, channel_id, u_id):
    url = config.url
    return requests.post(f"{url}channel/invite/v2", json={"token": token, "channel_id": channel_id, "u_id": u_id})


def channel_details_v2(token, channel_id):
    url = config.url
    return requests.get(f"{url}channel/details/v2", params={"token": token, "channel_id": channel_id})


def channel_addowner_v1(token, channel_id, u_id):
    url = config.url
    return requests.post(f"{url}channel/addowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})


def channel_removeowner_v1(token, channel_id, u_id):
    url = config.url
    return requests.post(f"{url}channel/removeowner/v1", json={"token": token, "channel_id": channel_id, "u_id": u_id})


def channel_join_v2(token, channel_id):
    url = config.url
    return requests.post(f"{url}channel/join/v2", json={"token": token, "channel_id": channel_id})


def admin_userpermission_change_v1(token, u_id, permission_id):
    url = config.url
    return requests.post(
        f"{url}admin/userpermission/change/v1", json={"token": token, "u_id": u_id, "permission_id": permission_id}
    )


def channels_list_v2(token):
    url = config.url
    return requests.get(f"{url}channels/list/v2", params={"token": token})


def channel_messages_v2(token, channel_id, start):
    url = config.url
    return requests.get(f"{url}channel/messages/v2", params={"token": token, "channel_id": channel_id, "start": start})


def message_send_v2(token, channel_id, message):
    url = config.url
    return requests.post(f"{url}message/send/v2", json={"token": token, "channel_id": channel_id, "message": message})


def channel_leave_v1(token, channel_id):
    url = config.url
    return requests.post(f"{url}channel/leave/v1", json={"token": token, "channel_id": channel_id})


def message_senddm_v1(token, dm_id, message):
    url = config.url
    return requests.post(f"{url}message/senddm/v1", json={"token": token, "dm_id": dm_id, "message": message})


def message_remove_v1(token, message_id):
    url = config.url
    return requests.delete(
        f"{url}message/remove/v1",
        json={
            "token": token,
            "message_id": message_id,
        },
    )


def message_edit_v2(token, message_id, message):
    url = config.url
    return requests.put(f"{url}message/edit/v2", json={"token": token, "message_id": message_id, "message": message})


def message_react_v1(token, message_id, react_id):
    url = config.url
    return requests.post(
        f"{url}message/react/v1", json={"token": token, "message_id": message_id, "react_id": react_id}
    )


def message_unreact_v1(token, message_id, react_id):
    url = config.url
    return requests.post(
        f"{url}message/unreact/v1", json={"token": token, "message_id": message_id, "react_id": react_id}
    )


def message_pin_v1(token, message_id):
    url = config.url
    return requests.post(f"{url}message/pin/v1", json={"token": token, "message_id": message_id})


def message_unpin_v1(token, message_id):
    url = config.url
    return requests.post(f"{url}message/unpin/v1", json={"token": token, "message_id": message_id})


def dm_create_v1(token, u_ids):
    url = config.url
    return requests.post(f"{url}dm/create/v1", json={"token": token, "u_ids": u_ids})


def dm_leave_v1(token, dm_id):
    url = config.url
    return requests.post(f"{url}dm/leave/v1", json={"token": token, "dm_id": dm_id})


def dm_invite_v1(token, dm_id, u_id):
    url = config.url
    return requests.post(f"{url}dm/invite/v1", json={"token": token, "dm_id": dm_id, "u_id": u_id})


def dm_remove_v1(token, dm_id):
    url = config.url
    return requests.delete(f"{url}dm/remove/v1", json={"token": token, "dm_id": dm_id})


def search_v2(token, query_str):
    url = config.url
    return requests.get(f"{url}search/v2", params={"token": token, "query_str": query_str})


def dm_messages_v1(token, dm_id, start):
    url = config.url
    return requests.get(f"{url}dm/messages/v1", params={"token": token, "dm_id": dm_id, "start": start})


def user_profile_v2(token, u_id):
    url = config.url
    return requests.get(f"{url}user/profile/v2", params={"token": token, "u_id": u_id})


def users_all_v1(token):
    url = config.url
    return requests.get(f"{url}users/all/v1", params={"token": token})


def admin_user_remove_v1(token, u_id):
    url = config.url
    return requests.delete(f"{url}admin/user/remove/v1", json={"token": token, "u_id": u_id})


def notifications_get_v1(token):
    url = config.url
    return requests.get(f"{url}notifications/get/v1", params={"token": token})


def message_sendlater_v1(token, channel_id, message, time_sent):
    url = config.url
    return requests.post(
        f"{url}message/sendlater/v1",
        json={"token": token, "channel_id": channel_id, "message": message, "time_sent": time_sent},
    )


def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    url = config.url
    return requests.post(
        f"{url}message/sendlaterdm/v1",
        json={"token": token, "dm_id": dm_id, "message": message, "time_sent": time_sent},
    )


def dm_details_v1(token, dm_id):
    url = config.url
    return requests.get(f"{url}dm/details/v1", params={"token": token, "dm_id": dm_id})