from src.admin import admin_userpermission_change_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.error import InputError, AccessError
import pytest

@pytest.fixture
def create_input():
    clear_v1()
    
    data_test_users = [
        auth_register_v2("ericzheng@mail.com", "peterpiper", "Eric", "Zheng"),
        auth_register_v2("joshhatton@mail.com", "maryreider", "Josh", "Hatton"), 
        auth_register_v2("bunnydong@mail.com", "globalempire4", "Bunny", "Dong"), 
        auth_register_v2("deanzworestine@mail.com", "runescape4lyfe", "Dean", 
                         "Zworestine"), 
        auth_register_v2("jordanmilch@mail.com", "iheartnewyork", "Jordan", 
                         "Milch")
    ]
    
    data_test_channels = [
        channels_create_v2(data_test_users[0]['token'], "General", True),
        channels_create_v2(data_test_users[1]['token'], "Party", True),
        channels_create_v2(data_test_users[2]['token'], "Private", False)
    ]
    
    return [data_test_users, data_test_channels]

def test_promote_member_to_owner(create_input):
    """ Tests that the first owner of Dreams is able to successfully promote
        a member of Dreams to an owner.
    """
    
    user_1 = create_input[0][0] # Dreams owner
    user_2 = create_input[0][1] # Dreams member
    
    private_channel = create_input[1][2]
    
    # Promote user_2 to an owner
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_2['auth_user_id'], 1) == {}
    
    # user_2 should be able to join private channels now as an owner
    assert channel_join_v2(user_2['token'], private_channel['channel_id']) == {}

def test_multiple_members_to_owners(create_input):
    """ Tests that the first owner of Dreams is able to promote several members of
        Dreams to an owner. These new owners should also be able to promote
        other members.
    """
    # user_1 is a dreams owner, everyone else is a member
    user_1, user_2, user_3, user_4, user_5 = create_input[0]
    
    private_channel = create_input[1][2]
    
    # Promote user_2 to owner
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_2['auth_user_id'], 1) == {}
    
    # user_2 should be able to promote other members to owners as well
    assert admin_userpermission_change_v1(user_2['token'],
                                          user_3['auth_user_id'], 1) == {}
    assert admin_userpermission_change_v1(user_2['token'],
                                          user_4['auth_user_id'], 1) == {}
    
    # user_3 should also be able to promote members to owners
    assert admin_userpermission_change_v1(user_3['token'],
                                          user_5['auth_user_id'], 1) == {}
    
    # everyone should be able to join a private channel
    assert channel_join_v2(user_2['token'], private_channel['channel_id']) == {}
    assert channel_join_v2(user_3['token'], private_channel['channel_id']) == {}
    assert channel_join_v2(user_4['token'], private_channel['channel_id']) == {}
    assert channel_join_v2(user_5['token'], private_channel['channel_id']) == {}

def test_demote_owner_to_member(create_input):
    """ Test for demoting owners to members.
    """
    
    user_1 = create_input[0][0]
    user_2 = create_input[0][1]
    
    private_channel = create_input[1][2]
    
    # first make user_2 an owner
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_2['auth_user_id'], 1) == {}

    # now demote user_1 to member
    assert admin_userpermission_change_v1(user_2['token'],
                                          user_1['auth_user_id'], 2) == {}
    
    # user_1 should not be able to join private channels
    with pytest.raises(AccessError):
        channel_join_v2(user_1['token'], private_channel['channel_id'])
        
def test_multiple_owners_to_members(create_input):
    """ Tests for demoting multiple owners to members.
    """
    
    user_1, user_2, user_3, user_4, user_5 = create_input[0]

    private_channel = create_input[1][2]
    
    # make user 2,3,4 all owners
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_2['auth_user_id'], 1) == {}
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_3['auth_user_id'], 1) == {}
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_4['auth_user_id'], 1) == {}
    
    # as user 2, demote user1,3,4
    assert admin_userpermission_change_v1(user_2['token'],
                                          user_1['auth_user_id'], 2) == {}
    assert admin_userpermission_change_v1(user_2['token'],
                                          user_3['auth_user_id'], 2) == {}
    assert admin_userpermission_change_v1(user_2['token'],
                                          user_4['auth_user_id'], 2) == {}
    
    # user1,3,4,5 should not be able to join private channels
    with pytest.raises(AccessError):
        channel_join_v2(user_1['token'], private_channel['channel_id'])
        channel_join_v2(user_3['token'], private_channel['channel_id'])
        channel_join_v2(user_4['token'], private_channel['channel_id'])
        channel_join_v2(user_5['token'], private_channel['channel_id'])        
    
def test_invalid_u_id():
    """ Should raise an InputError when passed in an invalid user id
    """
    clear_v1()
    
    user_1 = auth_register_v2("ericzheng@gmail.com", "WaffleNow!", "Eric", "Zheng")
    
    # Invalid u_id should raise an InputError
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user_1['token'],
                                       user_1['auth_user_id'] + 5, 2)
        admin_userpermission_change_v1(user_1['token'],
                                       user_1['auth_user_id'] + 10, 2)
        admin_userpermission_change_v1(user_1['token'],
                                       user_1['auth_user_id'] - 5, 1)
        admin_userpermission_change_v1(user_1['token'],
                                       user_1['auth_user_id'] - 500, 1)

def test_invalid_permission_id(create_input):
    """ Raises an InputError when passed in an invalid permission id
    """
    
    user_1 = create_input[0][0]
    user_2 = create_input[0][1]
    
    # only 1 and 2 are valid permission ids
    # invalid permissions shoould raise an input error
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user_1['token'],
                                       user_2['auth_user_id'], 3)
        admin_userpermission_change_v1(user_1['token'],
                                       user_2['auth_user_id'], -1)
        admin_userpermission_change_v1(user_1['token'],
                                       user_2['auth_user_id'], 4)
        admin_userpermission_change_v1(user_1['token'],
                                       user_2['auth_user_id'], 5)

def test_auth_user_not_owner(create_input):
    """ Raises an AccessError when auth user is not an owner of Dreams.
    """
    
    user_1 = create_input[0][0]
    user_2 = create_input[0][1]
    user_3 = create_input[0][2]
    
    # access error should be raised when authorised user is not an owner
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user_2['token'], user_1['auth_user_id'], 1)
        admin_userpermission_change_v1(user_2['token'], user_1['auth_user_id'], 2)
        admin_userpermission_change_v1(user_3['token'], user_1['auth_user_id'], 1)
        admin_userpermission_change_v1(user_3['token'], user_2['auth_user_id'], 2)

def test_invalid_token_id():
    """ Raises an AccessError when the token passed in does not refer to a valid
        user.
    """
    clear_v1()
    
    user_1 = auth_register_v2("ericzheng@gmail.com", "Helalfs432", "Eric", "Zheng")
    user_2 = auth_register_v2("joshhatton@gmail.com", "ccas1122", "Joshua", "Hatton")
    
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user_1['token'] + 'bug',
                                       user_2['auth_user_id'], 1)
        admin_userpermission_change_v1(user_1['token'] + 'sadf',
                                       user_2['auth_user_id'], 2)
        admin_userpermission_change_v1(user_1['token'] + '1',
                                       user_2['auth_user_id'], 2)
        admin_userpermission_change_v1(user_1['token'] + '7455',
                                       user_2['auth_user_id'], 1)

def test_exception_priority():
    """ When there are multiple errors, an AccessError should be the first one
        raised for invalid token.
    """
    clear_v1()
    
    auth_register_v2("ericzheng@gmail.com", "Hihjile", "Eric", "Zheng")
    user_2 = auth_register_v2("joshhatton@gmail.com", "ccas1122", "Joshua", "Hatton")
    user_3 = auth_register_v2("bunnydong@gmail.com", "bunnyyipyip", "Bunny", "Dong")

    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user_3['token'] + 'bug',
                                       user_2['auth_user_id'] + 5, 3)

def test_self_permission_change(create_input):
    """ Assume owners are able to change their own permission to member 
        permissions. 
        
        Assume if there is only one Owner of Dreams, they are not able to change
        their own permission to 2.
    """
    user_1 = create_input[0][0]
    user_2 = create_input[0][1]
    user_3 = create_input[0][2]
    private_channel = create_input[1][2]
    
    # promote user2 and user3 to owners
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_2['auth_user_id'], 1) == {}
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_3['auth_user_id'], 1) == {}
    
    # user1, user2 should both be able to change their own permissions to 2
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_1['auth_user_id'], 2) == {}
    assert admin_userpermission_change_v1(user_2['token'],
                                          user_2['auth_user_id'], 2) == {}
    
    # user3 shouldn't have their permissions changed despite function returning
    # expected output
    assert admin_userpermission_change_v1(user_3['token'],
                                          user_3['auth_user_id'], 2) == {}
    
    # user1 & user2 should now be members and can't join private channels
    with pytest.raises(AccessError):
        channel_join_v2(user_1['token'], private_channel['channel_id'])
        channel_join_v2(user_2['token'], private_channel['channel_id'])
        
    # user3 should still be able to join private channels
    assert channel_join_v2(user_3['token'], private_channel['channel_id']) == {}

def test_no_change(create_input):
    """ Assume owners are able to set the new permissions of others and 
        themselves to be the same permissions they already had, with no errors
        occurring.
    """
    user_1, user_2, user_3, user_4, user_5 = create_input[0]
    private_channel = create_input[1][2]
    
    # change permissions of user2 and user3 to owners
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_2['auth_user_id'], 1) == {}
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_3['auth_user_id'], 1) == {}
    
    # call function on user2,3,4,5 but "change" their permissions to their 
    # original permissions
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_2['auth_user_id'], 1) == {}
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_3['auth_user_id'], 1) == {}
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_4['auth_user_id'], 2) == {}
    assert admin_userpermission_change_v1(user_1['token'],
                                          user_5['auth_user_id'], 2) == {}
    
    # user2,3 should still be able to join private channels
    assert channel_join_v2(user_2['token'], private_channel['channel_id']) == {}
    assert channel_join_v2(user_3['token'], private_channel['channel_id']) == {}
    
    # user4,5 should still not be able to join private channels
    with pytest.raises(AccessError):
        channel_join_v2(user_4['token'], private_channel['channel_id'])
        channel_join_v2(user_5['token'], private_channel['channel_id'])

    