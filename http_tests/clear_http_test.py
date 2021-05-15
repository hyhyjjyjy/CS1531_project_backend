import pytest
import requests
from src import config

SUCCESS = 200
INPUT_ERROR = 400
ACCESS_ERROR = 403


def test_clear_empty():
    """Call the function twice to ensure no errors occur when we call clear on
    an empty database
    """
    url = config.url
    clear_result_1 = requests.delete(f"{url}clear/v1").json()
    assert clear_result_1 == {}

    clear_result_2 = requests.delete(f"{url}clear/v1").json()
    assert clear_result_2 == {}


def test_clear_user_login():
    """Tests that calling clear on registered users will not let them login
    as their data has been cleared.
    """
    url = config.url
    requests.delete(f"{url}clear/v1")

    requests.post(
        f"{url}auth/register/v2",
        json={"email": "ericzheng@gmail.com", "password": "peterpiper", "name_first": "Eric", "name_last": "Zheng"},
    )
    requests.post(
        f"{url}auth/register/v2",
        json={"email": "joshhatton@gmail.com", "password": "maryreider", "name_first": "Josh", "name_last": "Hatton"},
    )
    requests.post(
        f"{url}auth/register/v2",
        json={
            "email": "deanzworestine@gmail.com",
            "password": "runescape4lyfe",
            "name_first": "Dean",
            "name_last": "Zworestine",
        },
    )
    requests.post(
        f"{url}auth/register/v2",
        json={
            "email": "jordanmilch@gmail.com",
            "password": "iheartnewyork",
            "name_first": "Jordan",
            "name_last": "Milch",
        },
    )
    requests.post(
        f"{url}auth/register/v2",
        json={"email": "bunnydong@gmail.com", "password": "yesyesyes", "name_first": "Bunny", "name_last": "Dong"},
    )

    clear_result = requests.delete(f"{url}clear/v1").json()
    assert clear_result == {}

    # Users should not be able to login because data has been cleared
    login_1 = requests.post(f"{url}auth/login/v2", json={"email": "ericzheng@gmail.com", "password": "peterpiper"})
    login_2 = requests.post(f"{url}auth/login/v2", json={"email": "joshhatton@gmail.com", "password": "peterpiper"})
    login_3 = requests.post(f"{url}auth/login/v2", json={"email": "deanzworestine@gmail.com", "password": "peterpiper"})
    login_4 = requests.post(f"{url}auth/login/v2", json={"email": "jordanmilch@gmail.com", "password": "peterpiper"})
    login_5 = requests.post(f"{url}auth/login/v2", json={"email": "bunnydong@gmail.com", "password": "yesyesyes"})

    assert login_1.status_code == INPUT_ERROR
    assert login_2.status_code == INPUT_ERROR
    assert login_3.status_code == INPUT_ERROR
    assert login_4.status_code == INPUT_ERROR
    assert login_5.status_code == INPUT_ERROR

    requests.delete(f"{url}clear/v1")


def test_clear_everything():
    """Tests that calling clear on database filled with channels and channel
    members does indeed clear everything.
    """

    url = config.url
    requests.delete(f"{url}clear/v1")

    user_1 = requests.post(
        f"{url}auth/register/v2",
        json={"email": "ericzheng@gmail.com", "password": "peterpiper", "name_first": "Eric", "name_last": "Zheng"},
    ).json()
    user_2 = requests.post(
        f"{url}auth/register/v2",
        json={"email": "joshhatton@gmail.com", "password": "maryreider", "name_first": "Josh", "name_last": "Hatton"},
    ).json()
    user_3 = requests.post(
        f"{url}auth/register/v2",
        json={
            "email": "deanzworestine@gmail.com",
            "password": "runescape4lyfe",
            "name_first": "Dean",
            "name_last": "Zworestine",
        },
    ).json()
    user_4 = requests.post(
        f"{url}auth/register/v2",
        json={
            "email": "jordanmilch@gmail.com",
            "password": "iheartnewyork",
            "name_first": "Jordan",
            "name_last": "Milch",
        },
    ).json()
    requests.post(
        f"{url}auth/register/v2",
        json={"email": "bunnydong@gmail.com", "password": "yesyesyes", "name_first": "Bunny", "name_last": "Dong"},
    ).json()

    channel_1 = requests.post(
        f"{url}channels/create/v2", json={"token": user_1["token"], "name": "Party Channel", "is_public": True}
    ).json()
    channel_2 = requests.post(
        f"{url}channels/create/v2", json={"token": user_3["token"], "name": "General", "is_public": True}
    ).json()

    requests.post(f"{url}channel/join/v2", json={"token": user_2["token"], "channel_id": channel_2["channel_id"]})
    requests.post(f"{url}channel/join/v2", json={"token": user_3["token"], "channel_id": channel_1["channel_id"]})
    requests.post(f"{url}channel/join/v2", json={"token": user_4["token"], "channel_id": channel_1["channel_id"]})

    # Clear the data
    clear_result = requests.delete(f"{url}clear/v1")
    assert clear_result.status_code == SUCCESS
    assert clear_result.json() == {}

    # All data should have been reset so no users should be able to log in
    login_1 = requests.post(f"{url}auth/login/v2", json={"email": "ericzheng@gmail.com", "password": "peterpiper"})
    login_2 = requests.post(f"{url}auth/login/v2", json={"email": "joshhatton@gmail.com", "password": "peterpiper"})
    login_3 = requests.post(f"{url}auth/login/v2", json={"email": "deanzworestine@gmail.com", "password": "peterpiper"})
    login_4 = requests.post(f"{url}auth/login/v2", json={"email": "jordanmilch@gmail.com", "password": "peterpiper"})
    login_5 = requests.post(f"{url}auth/login/v2", json={"email": "bunnydong@gmail.com", "password": "yesyesyes"})

    assert login_1.status_code == INPUT_ERROR
    assert login_2.status_code == INPUT_ERROR
    assert login_3.status_code == INPUT_ERROR
    assert login_4.status_code == INPUT_ERROR
    assert login_5.status_code == INPUT_ERROR

    # Should also be unable to access list of channels as there are no valid tokens
    channels_listall_resp = requests.get(f"{url}channels/listall/v2", params={"token": user_1["token"]})
    assert channels_listall_resp.status_code == ACCESS_ERROR

    # Should be able to open a list of channels with a new valid token
    user_1 = requests.post(
        f"{url}auth/register/v2",
        json={"email": "ericzheng@gmail.com", "password": "peterpiper", "name_first": "Eric", "name_last": "Zheng"},
    ).json()

    channels_listall_resp_2 = requests.get(f"{url}channels/listall/v2", params={"token": user_1["token"]})
    assert channels_listall_resp_2.status_code == SUCCESS

    requests.delete(f"{url}clear/v1")