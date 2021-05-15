from src.auth import auth_register_v2
from src.other import clear_v1
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_messages_v2, channel_join_v2, channel_leave_v1
from src.message import message_send_v2, message_remove_v1, message_senddm_v1, message_react_v1,message_unreact_v1, message_pin_v1, message_unpin_v1
from src.dms import dm_create_v1, dm_messages_v1, dm_leave_v1, dm_invite_v1
import pytest
from src.error import InputError, AccessError

# Fixture to create a few channels and dms and send messages
@pytest.fixture
def create_input():
    clear_v1()

    users = [auth_register_v2("joshhatton@mail.com", "validpassword", "Josh", "Hatton"),
        auth_register_v2("bunnydong@mail.com", "anotherpassword", "Bunny", "Dong"),
        auth_register_v2("jordanmilch@mail.com", "password3", "Jordan", "Milch"),
        auth_register_v2("deanzworestine@mail.com", "4thpassword", "Dean", "Zworestine"),
        auth_register_v2("ericzheng@mail.com", "finalpassword", "Eric", "Zheng"),
    ]

    channels = [channels_create_v2(users[0]["token"], "First Channel", True)['channel_id'],
        channels_create_v2(users[1]["token"], "Second Channel", False)['channel_id']
    ]
    
    dms = [dm_create_v1(users[0]['token'], [users[2]['auth_user_id']])['dm_id'],
            dm_create_v1(users[1]['token'], [users[3]['auth_user_id'], users[4]['auth_user_id']])['dm_id']
    ]

    # Send 5 messages to First Channel
    channel_1_messages = []
    for i in range(0, 5):
        channel_1_messages.append(message_send_v2(users[0]["token"], channels[0], f"First channel message {i}.")['message_id'])

    # Send 5 messages to Second Channel
    for i in range(0, 5):
        message_send_v2(users[1]["token"], channels[1], f"Second channel message {i}.")

    # Send 5 messages to First DM
    dm_1_messages = []
    for i in range(0, 5):
        dm_1_messages.append(message_senddm_v1(users[0]["token"], dms[0], f"First dm message {i}.")['message_id'])

    # Send 5 messages to Second DM
    for i in range(0, 5):
        message_senddm_v1(users[1]["token"], dms[1], f"Second dm message {i}.")

    return [users, channels, dms, channel_1_messages, dm_1_messages]



# Test reacting to an invalid message
def test_react_invalid_message(create_input):
    message_remove_v1(create_input[0][0]['token'], create_input[3][0])
    message_remove_v1(create_input[0][0]['token'], create_input[4][0])
    with pytest.raises(InputError):
        message_react_v1(create_input[0][0]['token'], create_input[3][0], 1)
    with pytest.raises(InputError):
        message_react_v1(create_input[0][0]['token'], create_input[4][0], 1)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][0]['token'], create_input[3][0], 1)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][0]['token'], create_input[4][0], 1)
        
# Test react and unreact when react_id is not valid
def test_invalid_reactid(create_input):
    with pytest.raises(InputError):
        message_react_v1(create_input[0][0]['token'], create_input[3][0], 2)
    with pytest.raises(InputError):
        message_react_v1(create_input[0][1]['token'], create_input[3][1], 3)
    with pytest.raises(InputError):
        message_react_v1(create_input[0][1]['token'], create_input[3][4], 5)
    with pytest.raises(InputError):
        message_react_v1(create_input[0][0]['token'], create_input[4][0], 2)
    with pytest.raises(InputError):
        message_react_v1(create_input[0][2]['token'], create_input[4][1], 3)
    with pytest.raises(InputError):
        message_react_v1(create_input[0][2]['token'], create_input[4][4], 5)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][0]['token'], create_input[3][0], 2)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][1]['token'], create_input[3][1], 3)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][1]['token'], create_input[3][4], 5)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][0]['token'], create_input[4][0], 2)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][2]['token'], create_input[4][1], 3)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][2]['token'], create_input[4][4], 5)
    
# Test react when a message has already been reacted to with the same id
def test_duplicate_react(create_input):
    message_react_v1(create_input[0][0]['token'], create_input[3][0], 1)
    message_react_v1(create_input[0][0]['token'], create_input[4][0], 1)
    with pytest.raises(InputError):
        message_react_v1(create_input[0][0]['token'], create_input[3][0], 1)
    with pytest.raises(InputError):
        message_react_v1(create_input[0][0]['token'], create_input[4][0], 1)    

# Test unreact when a message has not already been reacted to with the same id
def test_missing_unreact(create_input):
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][0]['token'], create_input[3][0], 1)
    with pytest.raises(InputError):
        message_unreact_v1(create_input[0][0]['token'], create_input[4][0], 1)

# Test react and unreact when not in channel
def test_not_channel_member_react(create_input):
    with pytest.raises(AccessError):
        message_react_v1(create_input[0][2]['token'], create_input[3][0], 1)
    with pytest.raises(AccessError):
        message_react_v1(create_input[0][3]['token'], create_input[3][1], 1)
    with pytest.raises(AccessError):
        message_react_v1(create_input[0][3]['token'], create_input[3][4], 1)
    with pytest.raises(AccessError):
        message_react_v1(create_input[0][4]['token'], create_input[4][3], 1)
    with pytest.raises(AccessError):
        message_react_v1(create_input[0][3]['token'], create_input[4][1], 1)
    with pytest.raises(AccessError):
        message_react_v1(create_input[0][3]['token'], create_input[4][4], 1)        
# Cannot occur (if the are not a member they can't have reacted - unless removed from channel)
    channel_join_v2(create_input[0][2]['token'], create_input[1][0])
    message_react_v1(create_input[0][2]['token'], create_input[3][0], 1)
    channel_leave_v1(create_input[0][2]['token'], create_input[1][0])
    with pytest.raises(AccessError):
        message_unreact_v1(create_input[0][2]['token'], create_input[3][0], 1)
    message_react_v1(create_input[0][2]['token'], create_input[4][0], 1)
    dm_leave_v1(create_input[0][2]['token'], create_input[3][0])
    with pytest.raises(AccessError):
        message_unreact_v1(create_input[0][2]['token'], create_input[4][0], 1)    

# Tests a single react into a channel
def test_simple_channel_react(create_input):
    message_react_v1(create_input[0][0]['token'], create_input[3][0], 1)
    assert len(channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts']) == 1
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['react_id'] == 1
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['is_this_user_reacted'] == True
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['u_ids'][0] == create_input[0][0]['auth_user_id']
    
# Tests a single react into a dm
def test_simple_dm_react(create_input):
    message_react_v1(create_input[0][0]['token'], create_input[4][0], 1)
    assert len(dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts']) == 1
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['react_id'] == 1
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['is_this_user_reacted'] == True
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids'][0] == create_input[0][0]['auth_user_id']

# Tests multiple people reacting to a mesasge in a channel
def test_multiple_channel_react(create_input):
    channel_invite_v2(create_input[0][0]['token'], create_input[1][0], create_input[0][1]['auth_user_id'])
    channel_invite_v2(create_input[0][0]['token'], create_input[1][0], create_input[0][2]['auth_user_id'])
    channel_invite_v2(create_input[0][0]['token'], create_input[1][0], create_input[0][3]['auth_user_id'])
    channel_invite_v2(create_input[0][0]['token'], create_input[1][0], create_input[0][4]['auth_user_id'])
    message_react_v1(create_input[0][0]['token'], create_input[3][0], 1)
    message_react_v1(create_input[0][1]['token'], create_input[3][0], 1)
    message_react_v1(create_input[0][2]['token'], create_input[3][0], 1)
    assert len(channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts']) == 1
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['react_id'] == 1
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['is_this_user_reacted'] == True
    assert len(channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['u_ids']) == 3
    assert create_input[0][0]['auth_user_id'] in channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['u_ids']
    assert create_input[0][1]['auth_user_id'] in channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['u_ids']
    assert create_input[0][2]['auth_user_id'] in channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts'][0]['u_ids']

# Tests multiple people reacting to a mesasge in a dm
def test_multiple_dm_react(create_input):
    dm_invite_v1(create_input[0][0]['token'], create_input[2][0], create_input[0][1]['auth_user_id'])
    dm_invite_v1(create_input[0][0]['token'], create_input[2][0], create_input[0][3]['auth_user_id'])
    dm_invite_v1(create_input[0][0]['token'], create_input[2][0], create_input[0][4]['auth_user_id'])
    message_react_v1(create_input[0][0]['token'], create_input[4][0], 1)
    message_react_v1(create_input[0][1]['token'], create_input[4][0], 1)
    message_react_v1(create_input[0][2]['token'], create_input[4][0], 1)
    assert len(dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts']) == 1
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['react_id'] == 1
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['is_this_user_reacted'] == True
    assert len(dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']) == 3
    assert create_input[0][0]['auth_user_id'] in dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']
    assert create_input[0][1]['auth_user_id'] in dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']
    assert create_input[0][2]['auth_user_id'] in dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']
    
# Tests multiple people reacting to a mesasge in a dm
def test_multiple_dm_react_then_remove_one(create_input):
    dm_invite_v1(create_input[0][0]['token'], create_input[2][0], create_input[0][1]['auth_user_id'])
    dm_invite_v1(create_input[0][0]['token'], create_input[2][0], create_input[0][3]['auth_user_id'])
    dm_invite_v1(create_input[0][0]['token'], create_input[2][0], create_input[0][4]['auth_user_id'])
    message_react_v1(create_input[0][0]['token'], create_input[4][0], 1)
    message_react_v1(create_input[0][1]['token'], create_input[4][0], 1)
    message_react_v1(create_input[0][2]['token'], create_input[4][0], 1)
    assert len(dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts']) == 1
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['react_id'] == 1
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['is_this_user_reacted'] == True
    assert len(dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']) == 3
    assert create_input[0][0]['auth_user_id'] in dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']
    assert create_input[0][1]['auth_user_id'] in dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']
    assert create_input[0][2]['auth_user_id'] in dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']
    message_unreact_v1(create_input[0][0]['token'], create_input[4][0], 1)
    assert len(dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']) == 2
    assert create_input[0][0]['auth_user_id'] not in dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts'][0]['u_ids']
    
# Tests a single unreact in a channel
def test_simple_channel_unreact(create_input):
    message_react_v1(create_input[0][0]['token'], create_input[3][0], 1)
    message_unreact_v1(create_input[0][0]['token'], create_input[3][0], 1)
    assert len(channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['reacts']) == 0

# Tests a single unreact in a dm
def test_simple_dm_unreact(create_input):
    message_react_v1(create_input[0][0]['token'], create_input[4][0], 1)
    message_unreact_v1(create_input[0][0]['token'], create_input[4][0], 1)
    assert len(dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['reacts']) == 0

# Tests pinning a message that doesn't exist
def test_pinning_invalid_message(create_input):
    message_remove_v1(create_input[0][0]['token'], create_input[3][0])
    message_remove_v1(create_input[0][0]['token'], create_input[4][0])
    with pytest.raises(InputError):
        message_pin_v1(create_input[0][0]['token'], create_input[3][0])
    with pytest.raises(InputError):
        message_pin_v1(create_input[0][0]['token'], create_input[4][0])    
    
# Tests unpinning a message that doesn't exist
def test_unpinning_invalid_message(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[3][0])
    message_pin_v1(create_input[0][0]['token'], create_input[4][0])
    message_remove_v1(create_input[0][0]['token'], create_input[3][0])
    message_remove_v1(create_input[0][0]['token'], create_input[4][0])
    with pytest.raises(InputError):
        message_unpin_v1(create_input[0][0]['token'], create_input[3][0])
    with pytest.raises(InputError):
        message_unpin_v1(create_input[0][0]['token'], create_input[4][0]) 

# Tests pinning a message that is already pinned
def test_pinning_already_pinned(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[3][0])
    message_pin_v1(create_input[0][0]['token'], create_input[4][0])
    with pytest.raises(InputError):
        message_pin_v1(create_input[0][0]['token'], create_input[3][0])
    with pytest.raises(InputError):
        message_pin_v1(create_input[0][0]['token'], create_input[4][0])

# Tests unpinning a message that is already unpinned
def test_unpinning_already_unpinned(create_input):
    with pytest.raises(InputError):
        message_unpin_v1(create_input[0][0]['token'], create_input[3][0])
    with pytest.raises(InputError):
        message_unpin_v1(create_input[0][0]['token'], create_input[4][0])
        
# Tests pinning when a member is not a part of the channel/dm        
def test_pinning_non_member(create_input):
    with pytest.raises(AccessError):
        message_pin_v1(create_input[0][4]['token'], create_input[3][0])
    with pytest.raises(AccessError):
        message_pin_v1(create_input[0][4]['token'], create_input[4][0])

# Tests unpinning when a member is not a part of the channel/dm        
def test_unpinning_non_member(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[3][0])
    message_pin_v1(create_input[0][0]['token'], create_input[4][0])
    with pytest.raises(AccessError):
        message_unpin_v1(create_input[0][4]['token'], create_input[3][0])
    with pytest.raises(AccessError):
        message_unpin_v1(create_input[0][4]['token'], create_input[4][0])

# Tests pinning when a member is not an owner of the channel/dm        
def test_pinning_non_owner(create_input):
    channel_invite_v2(create_input[0][0]['token'], create_input[1][0], create_input[0][1]['auth_user_id'])
    with pytest.raises(AccessError):
        message_pin_v1(create_input[0][1]['token'], create_input[3][0])
    with pytest.raises(AccessError):
        message_pin_v1(create_input[0][2]['token'], create_input[4][0])

# Tests unpinning when a member is not an owner of the channel/dm        
def test_unpinning_non_owner(create_input):
    channel_invite_v2(create_input[0][0]['token'], create_input[1][0], create_input[0][1]['auth_user_id'])
    message_pin_v1(create_input[0][0]['token'], create_input[3][0])
    message_pin_v1(create_input[0][0]['token'], create_input[4][0])
    with pytest.raises(AccessError):
        message_unpin_v1(create_input[0][1]['token'], create_input[3][0])
    with pytest.raises(AccessError):
        message_unpin_v1(create_input[0][2]['token'], create_input[4][0])
        
# Tests pinning a single message in a channel
def test_simple_channel_pin(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[3][0])   
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['is_pinned'] == True
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][3]['is_pinned'] == False
    
# Tests pinning a single message in a dm
def test_simple_dm_pin(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[4][0])   
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['is_pinned'] == True
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][3]['is_pinned'] == False
    
# Tests pinning a few messages in a channel
def test_multiple_channel_pin(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[3][0])
    message_pin_v1(create_input[0][0]['token'], create_input[3][2])
    message_pin_v1(create_input[0][0]['token'], create_input[3][4])
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['is_pinned'] == True
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][3]['is_pinned'] == False  
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][2]['is_pinned'] == True
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][1]['is_pinned'] == False    
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][0]['is_pinned'] == True

# Tests pinning a few messages in a dm
def test_multiple_dm_pin(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[4][0])
    message_pin_v1(create_input[0][0]['token'], create_input[4][2])
    message_pin_v1(create_input[0][0]['token'], create_input[4][4])
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['is_pinned'] == True
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][3]['is_pinned'] == False  
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][2]['is_pinned'] == True
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][1]['is_pinned'] == False    
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][0]['is_pinned'] == True

# Tests a single unpin in a channel
def test_simple_channel_unpin(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[3][0])   
    message_unpin_v1(create_input[0][0]['token'], create_input[3][0])
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['is_pinned'] == False

# Tests a single unpin in a dm
def test_simple_dm_unpin(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[4][0])   
    message_unpin_v1(create_input[0][0]['token'], create_input[4][0])
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['is_pinned'] == False

# Tests pinning a few messages in a channel
def test_multiple_channel_unpin(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[3][0])
    message_pin_v1(create_input[0][0]['token'], create_input[3][1])
    message_pin_v1(create_input[0][0]['token'], create_input[3][2])
    message_pin_v1(create_input[0][0]['token'], create_input[3][4])
    message_unpin_v1(create_input[0][0]['token'], create_input[3][1])
    message_unpin_v1(create_input[0][0]['token'], create_input[3][2])
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][4]['is_pinned'] == True
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][3]['is_pinned'] == False  
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][2]['is_pinned'] == False
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][1]['is_pinned'] == False    
    assert channel_messages_v2(create_input[0][0]['token'], create_input[1][0], 0)['messages'][0]['is_pinned'] == True
    
# Tests pinning a few messages in a dm
def test_multiple_dm_unpin(create_input):
    message_pin_v1(create_input[0][0]['token'], create_input[4][0])
    message_pin_v1(create_input[0][0]['token'], create_input[4][1])
    message_pin_v1(create_input[0][0]['token'], create_input[4][2])
    message_pin_v1(create_input[0][0]['token'], create_input[4][4])
    message_unpin_v1(create_input[0][0]['token'], create_input[4][1])
    message_unpin_v1(create_input[0][0]['token'], create_input[4][2])
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][4]['is_pinned'] == True
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][3]['is_pinned'] == False  
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][2]['is_pinned'] == False
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][1]['is_pinned'] == False    
    assert dm_messages_v1(create_input[0][0]['token'], create_input[2][0], 0)['messages'][0]['is_pinned'] == True
    