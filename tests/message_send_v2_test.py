from src.auth import auth_register_v2
from src.other import clear_v1
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_messages_v2
from src.message import message_send_v2, message_edit_v2, message_remove_v1, message_share_v1, message_senddm_v1
from src.dms import dm_create_v1, dm_messages_v1
import pytest
from src.error import InputError, AccessError

# Tests an error is raised for long messages
def test_long_message():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    with pytest.raises(InputError):
        message_send_v2(user_1['token'], channel_1['channel_id'], 'a' * 1001)
        message_send_v2(user_1['token'], channel_1['channel_id'], 'b' * 1001)
        message_send_v2(user_1['token'], channel_1['channel_id'], 'c' * 1001)


# Tests an error is raised when a message is sent to a channel a user is not in
def test_not_in_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)    
    user_2 = auth_register_v2('cd@c.com', 'aaaaaa', 'a', 'a')
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', True)
    with pytest.raises(AccessError):
        message_send_v2(user_1['token'], channel_2['channel_id'], 'Hey!')
        message_send_v2(user_2['token'], channel_1['channel_id'], 'Imposter')
        
# Tests multiple errors and ensure they are being addressed in order
def test_multiple_errors():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)    
    user_2 = auth_register_v2('cd@c.com', 'aaaaaa', 'a', 'a')
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', True)
    with pytest.raises(InputError):
        message_send_v2(user_1['token'], channel_2['channel_id'], 'a' * 1001)
        message_send_v2(user_2['token'], channel_1['channel_id'], 'b' * 1001)
        
# Tests a single message being sent
def test_single_message():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!')    
    assert type(msg1) == dict
    assert type(msg1['message_id']) == int
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Hello World!"

# Tests multiple messages to a single channel
def test_multiple_messages_same_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!')  
    msg2 = message_send_v2(user_1['token'], channel_1['channel_id'], 'I')     
    msg3 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Love')  
    msg4 = message_send_v2(user_1['token'], channel_1['channel_id'], 'COMP')  
    assert type(msg1) == dict
    assert type(msg1['message_id']) == int
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "COMP"
    assert type(msg2) == dict
    assert type(msg2['message_id']) == int  
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 1)['messages'][0]['message'] == "Love"
    assert type(msg3) == dict
    assert type(msg3['message_id']) == int 
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 2)['messages'][0]['message'] == "I"
    assert type(msg4) == dict
    assert type(msg4['message_id']) == int    
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 3)['messages'][0]['message'] == "Hello World!"
    assert msg1['message_id'] != msg2['message_id']
    assert msg1 != msg3
    assert msg1 != msg4
    assert msg2 != msg3
    assert msg2 != msg4
    assert msg3 != msg4
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages']) == 4
    

# Tests the same messages being sent to different channels
def test_messages_different_channels():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_2 = channels_create_v2(user_2['token'], 'Channel 2', True)
    channel_3 = channels_create_v2(user_3['token'], 'Channel 3', True)
    
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!')  
    msg2 = message_send_v2(user_2['token'], channel_2['channel_id'], 'Hello World!')     
    msg3 = message_send_v2(user_3['token'], channel_3['channel_id'], 'Hello World!')   
    assert type(msg1) == dict
    assert type(msg1['message_id']) == int
    assert type(msg2) == dict
    assert type(msg2['message_id']) == int
    assert type(msg3) == dict
    assert type(msg3['message_id']) == int    
    assert msg1 != msg2
    assert msg1 != msg3
    assert msg2 != msg3 


# Tests editing a message that is too long    
def test_long_edit():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!')
    with pytest.raises(InputError):
        message_edit_v2(user_1['token'], msg1['message_id'], 'a' * 1001)
        message_edit_v2(user_1['token'], msg1['message_id'], 'b' * 1001)
        message_edit_v2(user_1['token'], msg1['message_id'], 'c' * 1001)    
        
# Tests editing a deleted message
def test_deleted_edit():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!')
    message_remove_v1(user_1['token'], msg1['message_id'])
    with pytest.raises(InputError):
        message_edit_v2(user_1['token'], msg1['message_id'], 'a' * 1001)
    with pytest.raises(AccessError):    
        message_edit_v2(user_1['token'], msg1['message_id'], 'I am a ghost')

# Tests different users with different permissions
def test_different_permissions_edit():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_3['auth_user_id'])
    msg1 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello World!')
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Hello World!"
    assert message_edit_v2(user_1['token'], msg1['message_id'], 'Goodbye World!') == {}
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Goodbye World!"
    assert message_edit_v2(user_2['token'], msg1['message_id'], 'Hello Again World!') == {}
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Hello Again World!"
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages']) == 1
    with pytest.raises(AccessError):
        message_edit_v2(user_3['token'], msg1['message_id'], 'Goodbye Again!') 
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Hello Again World!"    

# Tests a user cannot edit another user's message
def test_edit_other_users_message():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)    
    user_2 = auth_register_v2('cd@c.com', 'aaaaaa', 'a', 'a')
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hey!')
    msg2 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello!')
    with pytest.raises(AccessError):
        message_edit_v2(user_1['token'], msg2['message_id'], 'He is stealing')
        message_edit_v2(user_2['token'], msg1['message_id'], 'I did not say this')   
 
# Tests editing from DM
def test_edit_from_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    msg_1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Sliding in')
    message_edit_v2(user_1['token'], msg_1['message_id'], 'Beep beep lettuce')
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages'][0]['message'] == 'Beep beep lettuce'    
    
# Tests deleting messages with the edit function
def test_different_permissions_edit_remove():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_3['auth_user_id'])
    msg1 = message_send_v2(user_2['token'], channel_1['channel_id'], 'First Message')
    msg2 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Second Message')
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages']) == 2
    assert message_edit_v2(user_1['token'], msg1['message_id'], '') == {}
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages']) == 1
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Second Message"
    assert message_edit_v2(user_2['token'], msg2['message_id'], '') == {}
    msg3 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Third Message')
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Third Message"
    with pytest.raises(AccessError):
        message_edit_v2(user_3['token'], msg3['message_id'], '') 
    with pytest.raises(AccessError):
        message_remove_v1(user_3['token'], msg3['message_id'])
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Third Message"    
       
# Tests removing from DM
def test_remove_from_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    msg_1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Sliding in')
    message_remove_v1(user_1['token'], msg_1['message_id'])
    assert len(dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages']) == 0
    msg_2 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Pls dont block me')
    message_edit_v2(user_1['token'], msg_2['message_id'], '')    
    assert len(dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages']) == 0
    
# Tests deleting a deleted message
def test_deleted_delete():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!')
    assert message_remove_v1(user_1['token'], msg1['message_id']) == {}
    with pytest.raises(AccessError):
        message_remove_v1(user_1['token'], msg1['message_id'])
    with pytest.raises(AccessError):
        message_edit_v2(user_1['token'], msg1['message_id'], '')
        
# Tests different users with different permissions in a channel
def test_different_permissions_remove_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_3['auth_user_id'])
    message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello World! 0')
    msg1 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello World! 1')
    assert message_remove_v1(user_1['token'], msg1['message_id']) == {}
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Hello World! 0"
    msg1 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello World! 2')
    assert message_remove_v1(user_2['token'], msg1['message_id']) == {}
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Hello World! 0"
    with pytest.raises(AccessError):
        message_remove_v1(user_3['token'], msg1['message_id']) 
 

# Tests message sharing with user not in channel being shared to
def test_share_message_not_in_receiving_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_2 = channels_create_v2(user_2['token'], 'Channel 2', True)
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hi Chan 1')
    msg2 = message_send_v2(user_2['token'], channel_2['channel_id'], 'Hi Chan 2')
    with pytest.raises(AccessError):
        message_share_v1(user_1['token'], msg2['message_id'], '', channel_2, -1)
        message_share_v1(user_2['token'], msg1['message_id'], 'SPAM!', channel_1, -1)

# Tests message sharing with user not in dm being shared to
def test_share_message_not_in_receiving_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    dm_1 = dm_create_v1(user_1['token'], [])
    dm_2 = dm_create_v1(user_2['token'], [])
    msg1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Hi DM 1')
    msg2 = message_senddm_v1(user_2['token'], dm_2['dm_id'], 'Hi DM 2')
    with pytest.raises(AccessError):
        message_share_v1(user_1['token'], msg2['message_id'], '', -1, dm_1['dm_id'])
        message_share_v1(user_2['token'], msg1['message_id'], 'SPAM!', -1, dm_1['dm_id'])
    
# Tests message sharing to a channel
def test_share_multiple_message():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True)
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', True)
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hi Chan 1')
    msg2 = message_send_v2(user_1['token'], channel_2['channel_id'], 'Hi Chan 2')
    msg3 = message_share_v1(user_1['token'], msg1['message_id'], '', channel_2['channel_id'], -1)
    msg4 = message_share_v1(user_1['token'], msg2['message_id'], 'SPAM!', channel_1['channel_id'], -1)  
    
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Hi Chan 2\nSPAM!"
    assert channel_messages_v2(user_1['token'], channel_2['channel_id'], 0)['messages'][0]['message'] == "Hi Chan 1"
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages']) == 2
    assert len(channel_messages_v2(user_1['token'], channel_2['channel_id'], 0)['messages']) == 2
    assert msg1['message_id'] != msg4['shared_message_id']
    assert msg1['message_id'] != msg3['shared_message_id']
    
    with pytest.raises(InputError):
        message_share_v1(user_1['token'], msg1['message_id'], 'a' * 991, channel_2['channel_id'], -1)
    with pytest.raises(InputError):
        message_share_v1(user_1['token'], msg1['message_id'], 'a' * 1000, channel_2['channel_id'], -1)
    with pytest.raises(AccessError):
        message_share_v1(user_1['token'], msg1['message_id'], 'a', -1, -1)
    with pytest.raises(InputError):
        message_share_v1(user_1['token'], msg1['message_id'], 'a', channel_2['channel_id'], -2)
    
    msg5 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Channel 1 > Channel 2')
    msg6 = message_send_v2(user_1['token'], channel_2['channel_id'], 'Channel 1 stinkyyyy')
    msg7 = message_share_v1(user_1['token'], msg5['message_id'], '123', channel_2['channel_id'], -1)
    msg8 = message_share_v1(user_1['token'], msg6['message_id'], '', channel_1['channel_id'], -1)  
    
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages'][0]['message'] == "Channel 1 stinkyyyy"
    assert channel_messages_v2(user_1['token'], channel_2['channel_id'], 0)['messages'][0]['message'] == "Channel 1 > Channel 2\n123"
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0)['messages']) == 4
    assert len(channel_messages_v2(user_1['token'], channel_2['channel_id'], 0)['messages']) == 4
    assert msg5['message_id'] != msg8['shared_message_id']
    assert msg5['message_id'] != msg7['shared_message_id']
    
# Tests message sharing to a dm
def test_share_multiple_message_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    dm_1 = dm_create_v1(user_1['token'], [])
    dm_2 = dm_create_v1(user_1['token'], [])
    msg1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Hi DM 1')
    msg2 = message_senddm_v1(user_1['token'], dm_2['dm_id'], 'Hi DM 2')
    msg3 = message_share_v1(user_1['token'], msg1['message_id'], '', -1, dm_2['dm_id'])
    msg4 = message_share_v1(user_1['token'], msg2['message_id'], 'SPAM!', -1, dm_1['dm_id'])  
    
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages'][0]['message'] == "Hi DM 2\nSPAM!"
    assert dm_messages_v1(user_1['token'], dm_2['dm_id'], 0)['messages'][0]['message'] == "Hi DM 1"
    assert len(dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages']) == 2
    assert len(dm_messages_v1(user_1['token'], dm_2['dm_id'], 0)['messages']) == 2
    assert msg1['message_id'] != msg4['shared_message_id']
    assert msg1['message_id'] != msg3['shared_message_id']
    
    msg5 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'DM 1 > DM 2')
    msg6 = message_senddm_v1(user_1['token'], dm_2['dm_id'], 'DM 1 stinkyyyy')
    msg7 = message_share_v1(user_1['token'], msg5['message_id'], '123', -1, dm_2['dm_id'])
    msg8 = message_share_v1(user_1['token'], msg6['message_id'], '', -1, dm_1['dm_id'])  
    
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages'][0]['message'] == "DM 1 stinkyyyy"
    assert dm_messages_v1(user_1['token'], dm_2['dm_id'], 0)['messages'][0]['message'] == "DM 1 > DM 2\n123"
    assert len(dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages']) == 4
    assert len(dm_messages_v1(user_1['token'], dm_2['dm_id'], 0)['messages']) == 4
    assert msg5['message_id'] != msg8['shared_message_id']
    assert msg5['message_id'] != msg7['shared_message_id']
            
# Tests different users with different permissions in a dm
def test_different_permissions_remove_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c')
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    dmsg1 = message_senddm_v1(user_2['token'], dm_1['dm_id'], 'Hello World! 1')
    assert message_remove_v1(user_2['token'], dmsg1['message_id']) == {}
    dmsg2 = message_senddm_v1(user_2['token'], dm_1['dm_id'], 'Hello World! 2')
    with pytest.raises(AccessError):
        message_remove_v1(user_1['token'], dmsg2['message_id'])
        message_remove_v1(user_3['token'], dmsg2['message_id'])     


# Tests invalid input
def test_senddm_invalid_input():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    with pytest.raises(InputError):
        message_senddm_v1(user_1['token'], dm_1['dm_id'], 'a' * 1001)
        message_senddm_v1(user_1['token'], dm_1['dm_id'], 'b' * 1001)
        message_senddm_v1(user_1['token'], dm_1['dm_id'], 'b' * 1001)

# Tests invalid access
def test_senddm_invalid_access():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c')
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    with pytest.raises(AccessError):
        message_senddm_v1(user_3['token'], dm_1['dm_id'], 'Sliding in') 
        message_senddm_v1(user_3['token'], dm_1['dm_id'], 'Back again')

# Tests basic dm send
def test_senddm_basic():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    msg_1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Sliding in')
    assert type(msg_1) == dict
    assert type(msg_1['message_id']) == int
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages'][0]['message'] == "Sliding in"
    
# Tests sending the same message to multiple different channels
def test_senddm_different_channels():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a')
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b')
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c')
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    dm_2 = dm_create_v1(user_2['token'], [user_3['auth_user_id']])
    dm_3 = dm_create_v1(user_3['token'], [user_1['auth_user_id']])    
    msg1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Hello World!')  
    msg2 = message_senddm_v1(user_2['token'], dm_2['dm_id'], 'Hello World!')     
    msg3 = message_senddm_v1(user_3['token'], dm_3['dm_id'], 'Hello World!')   
    assert type(msg1) == dict
    assert type(msg1['message_id']) == int
    assert type(msg2) == dict
    assert type(msg2['message_id']) == int
    assert type(msg3) == dict
    assert type(msg3['message_id']) == int    
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0)['messages'][0]['message'] == "Hello World!"
    assert dm_messages_v1(user_2['token'], dm_2['dm_id'], 0)['messages'][0]['message'] == "Hello World!"
    assert dm_messages_v1(user_3['token'], dm_3['dm_id'], 0)['messages'][0]['message'] == "Hello World!"
    assert msg1 != msg2
    assert msg1 != msg3
    assert msg2 != msg3 
