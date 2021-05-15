from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_listall_v2, channels_create_v2
from src.channel import channel_join_v2
from src.error import InputError, AccessError
import pytest

def test_clear_empty():
    """ Call the function twice to ensure no errors occur when we call clear on 
        an empty database 
    """
    assert clear_v1() == {}
    assert clear_v1() == {}

def test_clear_user_login():
    """ Tests that calling clear on registered users will not let them login 
        as their data has been cleared.
    """
    clear_v1()
    auth_register_v2("bunnydongao@gmail.com", "asdfg123456", "Bunny", "Dong")
    auth_register_v2("jamesdongao@gmail.com", "asdfg123456", "James", "Dong")
    auth_register_v2("christindongao@gmail.com", "asdfg123456", "gerht", "grg")
    auth_register_v2("Leonard@gmail.com", "asdfg123456", "fwef", "erggre")

    assert(clear_v1() == {})
    
    # Users should not be able to login because data has been cleared
    with pytest.raises(InputError):
        auth_login_v2("bunnydongao@gmail.com", "asdfg123456")
        auth_login_v2("jamesdongao@gmail.com", "asdfg123456")
        auth_login_v2("christindongao@gmail.com", "asdfg123456")
        auth_login_v2("Leonard@gmail.com", "asdfg123456")
    
    clear_v1()
    
def test_clear_everything():
    """ Tests that calling clear on database filled with channels and channel
        members does indeed clear everything.
    """
    clear_v1()
    user_1 = auth_register_v2("ericzheng@gmail.com", "peterpiper", "Eric",
                              "Zheng")
    user_2 = auth_register_v2("joshhatton@gmail.com", "maryreider", "Josh",
                              "Hatton")
    user_3 = auth_register_v2("deanzworestine@gmail.com", "runescape4lyfe",
                              "Dean", "Zworestine")
    user_4 = auth_register_v2("jordanmilch@gmail.com", "iheartnewyork", "Jordan", 
                              "Milch")
    
    channel_1 = channels_create_v2(user_1["token"], "Party Channel", True)
    channel_2 = channels_create_v2(user_3["token"], "General", True)
    
    channel_join_v2(user_2["token"], channel_2['channel_id'])
    channel_join_v2(user_3["token"], channel_1['channel_id'])
    channel_join_v2(user_4["token"], channel_1['channel_id'])
    
    assert clear_v1() == {}
    
    with pytest.raises(InputError):
        # All data should have been reset so no users should be able to log in        
        auth_login_v2("ericzheng@gmail.com", "peterpiper")
        auth_login_v2("joshhatton@gmail.com", "maryreider")
        auth_login_v2("bunnydong@gmail.com", "globalempire4")
        auth_login_v2("deanzworestine@gmail.com", "runescape4lyfe")
        auth_login_v2("jordanmilch@gmail.com", "iheartnewyork")
        
    with pytest.raises(AccessError):
        # Should also be unable to access list of channels as there are no valid
        # tokens
        channels_listall_v2(user_1["token"])
        
    # Should be able to open a list of channels with a new valid token
    user_1 = auth_register_v2("ericzheng@gmail.com", "peterpiper", "Eric",
                              "Zheng")

    channels_listall_v2(user_1["token"])

    clear_v1()
    

