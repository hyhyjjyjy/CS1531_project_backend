import pytest
import requests
from src import config

#####
#Helper Functions
#####

SUCCESS = 200
INPUT_ERROR = 400
ACCESS_ERROR = 403

def clear_v1():
    url = config.url
    return requests.delete(f"{url}clear/v1")

def auth_register_v2(email, password, name_first, name_last):
    url = config.url
    return requests.post(f"{url}auth/register/v2", json={'email': email, 'password': password, 'name_first': name_first, 'name_last': name_last})

def channels_create_v2(token, name, is_public):
    url = config.url
    return requests.post(f"{url}channels/create/v2", json={'token': token, 'name': name, 'is_public': is_public})

def channel_messages_v2(token, channel_id, start):
    url = config.url
    return requests.get(f"{url}channel/messages/v2", params={'token': token, 'channel_id': channel_id, 'start': start})

def channel_invite_v2(token, channel_id, u_id):
    url = config.url
    return requests.post(f"{url}channel/invite/v2", json={'token': token, 'channel_id': channel_id, 'u_id': u_id})

def message_send_v2(token, channel_id, message):
    url = config.url
    return requests.post(f"{url}message/send/v2", json={'token': token, 'channel_id': channel_id, 'message': message})

def message_edit_v2(token, message_id, message):
    url = config.url
    return requests.put(f"{url}message/edit/v2", json={'token': token, 'message_id': message_id, 'message': message})

def message_remove_v1(token, message_id):
    url = config.url
    return requests.delete(f"{url}message/remove/v1", json={'token': token, 'message_id': message_id})

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    url = config.url
    return requests.post(f"{url}message/share/v1", json={'token': token, 'og_message_id': og_message_id, 'message': message, 'channel_id': channel_id, 'dm_id': dm_id})

def message_senddm_v1(token, dm_id, message):
    url = config.url
    return requests.post(f"{url}message/senddm/v1", json={'token': token, 'dm_id': dm_id, 'message': message})

def dm_create_v1(token, u_ids):
    url = config.url
    return requests.post(f"{url}dm/create/v1", json={'token': token, 'u_ids': u_ids})

def dm_messages_v1(token, dm_id, start):
    url = config.url
    return requests.get(f"{url}dm/messages/v1", params={'token': token, 'dm_id': dm_id, 'start': start})


# Tests an error is raised for long messages
def test_long_message():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    assert message_send_v2(user_1['token'], channel_1['channel_id'], 'a' * 1001).status_code == INPUT_ERROR
    assert message_send_v2(user_1['token'], channel_1['channel_id'], 'b' * 1001).status_code == INPUT_ERROR
    assert message_send_v2(user_1['token'], channel_1['channel_id'], 'c' * 1001).status_code == INPUT_ERROR
    clear_v1()

# Tests an error is raised when a message is sent to a channel a user is not in
def test_not_in_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()    
    user_2 = auth_register_v2('cd@c.com', 'aaaaaa', 'a', 'a').json()
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', True).json()
    assert message_send_v2(user_2['token'], channel_2['channel_id'], 'Hey!').status_code == ACCESS_ERROR
    assert message_send_v2(user_2['token'], channel_1['channel_id'], 'Imposter').status_code == ACCESS_ERROR
    clear_v1()
        
# Tests multiple errors and ensure they are being addressed in order
def test_multiple_errors():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()    
    user_2 = auth_register_v2('cd@c.com', 'aaaaaa', 'a', 'a').json()
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', True).json()
    assert message_send_v2(user_1['token'], channel_2['channel_id'], 'a' * 1001).status_code == INPUT_ERROR
    assert message_send_v2(user_2['token'], channel_1['channel_id'], 'b' * 1001).status_code == INPUT_ERROR
    clear_v1()
        
# Tests a single message being sent
def test_single_message():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!').json()    
    assert type(msg1) == dict
    assert type(msg1['message_id']) == int
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Hello World!"
    clear_v1()

# Tests multiple messages to a single channel
def test_multiple_messages_same_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!').json()  
    msg2 = message_send_v2(user_1['token'], channel_1['channel_id'], 'I').json()
    msg3 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Love').json()  
    msg4 = message_send_v2(user_1['token'], channel_1['channel_id'], 'COMP').json()  
    assert type(msg1) == dict
    assert type(msg1['message_id']) == int
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "COMP"
    assert type(msg2) == dict
    assert type(msg2['message_id']) == int  
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 1).json()['messages'][0]['message'] == "Love"
    assert type(msg3) == dict
    assert type(msg3['message_id']) == int 
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 2).json()['messages'][0]['message'] == "I"
    assert type(msg4) == dict
    assert type(msg4['message_id']) == int    
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 3).json()['messages'][0]['message'] == "Hello World!"
    assert msg1['message_id'] != msg2['message_id']
    assert msg1 != msg3
    assert msg1 != msg4
    assert msg2 != msg3
    assert msg2 != msg4
    assert msg3 != msg4
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages']) == 4
    clear_v1()    

# Tests the same messages being sent to different channels
def test_messages_different_channels():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_2 = channels_create_v2(user_2['token'], 'Channel 2', True).json()
    channel_3 = channels_create_v2(user_3['token'], 'Channel 3', True).json()
    
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!').json()
    msg2 = message_send_v2(user_2['token'], channel_2['channel_id'], 'Hello World!').json()
    msg3 = message_send_v2(user_3['token'], channel_3['channel_id'], 'Hello World!').json()   
    assert type(msg1) == dict
    assert type(msg1['message_id']) == int
    assert type(msg2) == dict
    assert type(msg2['message_id']) == int
    assert type(msg3) == dict
    assert type(msg3['message_id']) == int    
    assert msg1 != msg2
    assert msg1 != msg3
    assert msg2 != msg3 
    clear_v1()

# Tests editing a message that is too long    
def test_long_edit():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!').json()
    assert message_edit_v2(user_1['token'], msg1['message_id'], 'a' * 1001).status_code == INPUT_ERROR
    assert message_edit_v2(user_1['token'], msg1['message_id'], 'b' * 1001).status_code == INPUT_ERROR
    assert message_edit_v2(user_1['token'], msg1['message_id'], 'c' * 1001).status_code == INPUT_ERROR 
    clear_v1()
        
# Tests editing a deleted message
def test_deleted_edit():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!').json()
    message_remove_v1(user_1['token'], msg1['message_id'])
    assert message_edit_v2(user_1['token'], msg1['message_id'], 'a' * 1001).status_code == INPUT_ERROR
    assert message_edit_v2(user_1['token'], msg1['message_id'], 'I am a ghost').status_code == ACCESS_ERROR
    clear_v1()

# Tests different users with different permissions
def test_different_permissions_edit():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_3['auth_user_id'])
    msg1 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello World!').json()
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Hello World!"
    assert message_edit_v2(user_1['token'], msg1['message_id'], 'Goodbye World!').json() == {}
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Goodbye World!"
    assert message_edit_v2(user_2['token'], msg1['message_id'], 'Hello Again World!').json() == {}
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Hello Again World!"
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages']) == 1
    assert message_edit_v2(user_3['token'], msg1['message_id'], 'Goodbye Again!').status_code == ACCESS_ERROR
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Hello Again World!"    
    clear_v1()

# Tests a user cannot edit another user's message
def test_edit_other_users_message():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    user_2 = auth_register_v2('cd@c.com', 'aaaaaa', 'a', 'a').json()
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hey!').json()
    assert message_edit_v2(user_2['token'], msg1['message_id'], 'I did not say this').status_code == ACCESS_ERROR
    clear_v1()
 
# Tests editing from DM
def test_edit_from_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']]).json()
    msg_1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Sliding in').json()
    message_edit_v2(user_1['token'], msg_1['message_id'], 'Beep beep lettuce')
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages'][0]['message'] == 'Beep beep lettuce'    
    clear_v1()
    
# Tests deleting messages with the edit function
def test_different_permissions_edit_remove():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_3['auth_user_id'])
    msg1 = message_send_v2(user_2['token'], channel_1['channel_id'], 'First Message').json()
    msg2 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Second Message').json()
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages']) == 2
    assert message_edit_v2(user_1['token'], msg1['message_id'], '').json() == {}
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages']) == 1
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Second Message"
    assert message_edit_v2(user_2['token'], msg2['message_id'], '').json() == {}
    msg3 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Third Message').json()
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Third Message"
    assert message_edit_v2(user_3['token'], msg3['message_id'], '').status_code == ACCESS_ERROR
    assert message_remove_v1(user_3['token'], msg3['message_id']).status_code == ACCESS_ERROR
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Third Message"    
    clear_v1()
       
# Tests removing from DM
def test_remove_from_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']]).json()
    msg_1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Sliding in').json()
    message_remove_v1(user_1['token'], msg_1['message_id'])
    assert len(dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages']) == 0
    msg_2 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Pls dont block me').json()
    message_edit_v2(user_1['token'], msg_2['message_id'], '')    
    assert len(dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages']) == 0
    clear_v1()
    
# Tests deleting a deleted message
def test_deleted_delete():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hello World!').json()
    assert message_remove_v1(user_1['token'], msg1['message_id']).json() == {}
    assert message_remove_v1(user_1['token'], msg1['message_id']).status_code == ACCESS_ERROR
    assert message_edit_v2(user_1['token'], msg1['message_id'], '').status_code == ACCESS_ERROR
    clear_v1()
        
# Tests different users with different permissions in a channel
def test_different_permissions_remove_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_2['auth_user_id'])
    channel_invite_v2(user_1['token'], channel_1['channel_id'], user_3['auth_user_id'])
    message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello World! 0')
    msg1 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello World! 1').json()
    assert message_remove_v1(user_1['token'], msg1['message_id']).json() == {}
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Hello World! 0"
    msg1 = message_send_v2(user_2['token'], channel_1['channel_id'], 'Hello World! 2').json()
    assert message_remove_v1(user_2['token'], msg1['message_id']).json() == {}
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Hello World! 0"
    assert message_remove_v1(user_3['token'], msg1['message_id']).status_code == ACCESS_ERROR
    clear_v1()

# Tests message sharing with user not in channel being shared to
def test_share_message_not_in_receiving_channel():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_2 = channels_create_v2(user_2['token'], 'Channel 2', True).json()
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hi Chan 1').json()
    msg2 = message_send_v2(user_2['token'], channel_2['channel_id'], 'Hi Chan 2').json()
    assert message_share_v1(user_1['token'], msg2['message_id'], '', channel_2['channel_id'], -1).status_code == ACCESS_ERROR
    assert message_share_v1(user_2['token'], msg1['message_id'], 'SPAM!', channel_1['channel_id'], -1).status_code == ACCESS_ERROR
    clear_v1()

# Tests message sharing with user not in dm being shared to
def test_share_message_not_in_receiving_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    dm_1 = dm_create_v1(user_1['token'], []).json()
    dm_2 = dm_create_v1(user_2['token'], []).json()
    msg1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Hi DM 1').json()
    msg2 = message_senddm_v1(user_2['token'], dm_2['dm_id'], 'Hi DM 2').json()
    assert message_share_v1(user_1['token'], msg2['message_id'], '', -1, dm_1['dm_id']).status_code == ACCESS_ERROR
    assert message_share_v1(user_2['token'], msg1['message_id'], 'SPAM!', -1, dm_1['dm_id']).status_code == ACCESS_ERROR
    clear_v1()
    
# Tests message sharing to a channel
def test_share_multiple_message():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    channel_1 = channels_create_v2(user_1['token'], 'Channel 1', True).json()
    channel_2 = channels_create_v2(user_1['token'], 'Channel 2', True).json()
    msg1 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Hi Chan 1').json()
    msg2 = message_send_v2(user_1['token'], channel_2['channel_id'], 'Hi Chan 2').json()
    msg3 = message_share_v1(user_1['token'], msg1['message_id'], '', channel_2['channel_id'], -1).json()
    msg4 = message_share_v1(user_1['token'], msg2['message_id'], 'SPAM!', channel_1['channel_id'], -1).json()
    
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Hi Chan 2\nSPAM!"
    assert channel_messages_v2(user_1['token'], channel_2['channel_id'], 0).json()['messages'][0]['message'] == "Hi Chan 1"
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages']) == 2
    assert len(channel_messages_v2(user_1['token'], channel_2['channel_id'], 0).json()['messages']) == 2
    assert msg1 != msg4
    assert msg1 != msg3
    
    assert message_share_v1(user_1['token'], msg1['message_id'], 'a' * 991, channel_2['channel_id'], -1).status_code == INPUT_ERROR
    message_share_v1(user_1['token'], msg1['message_id'], 'a' * 1000, channel_2['channel_id'], -1).status_code == INPUT_ERROR
    message_share_v1(user_1['token'], msg1['message_id'], 'a', -1, -1).status_code == ACCESS_ERROR
    message_share_v1(user_1['token'], msg1['message_id'], 'a', channel_2['channel_id'], -2).status_code == INPUT_ERROR
    
    msg5 = message_send_v2(user_1['token'], channel_1['channel_id'], 'Channel 1 > Channel 2').json()
    msg6 = message_send_v2(user_1['token'], channel_2['channel_id'], 'Channel 1 stinkyyyy').json()
    msg7 = message_share_v1(user_1['token'], msg5['message_id'], '123', channel_2['channel_id'], -1).json()
    msg8 = message_share_v1(user_1['token'], msg6['message_id'], '', channel_1['channel_id'], -1).json()
    
    assert channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages'][0]['message'] == "Channel 1 stinkyyyy"
    assert channel_messages_v2(user_1['token'], channel_2['channel_id'], 0).json()['messages'][0]['message'] == "Channel 1 > Channel 2\n123"
    assert len(channel_messages_v2(user_1['token'], channel_1['channel_id'], 0).json()['messages']) == 4
    assert len(channel_messages_v2(user_1['token'], channel_2['channel_id'], 0).json()['messages']) == 4
    assert msg5 != msg8
    assert msg5 != msg7    
    clear_v1()
    
# Tests message sharing to a dm
def test_share_multiple_message_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    dm_1 = dm_create_v1(user_1['token'], []).json()
    dm_2 = dm_create_v1(user_1['token'], []).json()
    msg1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Hi DM 1').json()
    msg2 = message_senddm_v1(user_1['token'], dm_2['dm_id'], 'Hi DM 2').json()
    msg3 = message_share_v1(user_1['token'], msg1['message_id'], '', -1, dm_2['dm_id']).json()
    msg4 = message_share_v1(user_1['token'], msg2['message_id'], 'SPAM!', -1, dm_1['dm_id']).json()
    
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages'][0]['message'] == "Hi DM 2\nSPAM!"
    assert dm_messages_v1(user_1['token'], dm_2['dm_id'], 0).json()['messages'][0]['message'] == "Hi DM 1"
    assert len(dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages']) == 2
    assert len(dm_messages_v1(user_1['token'], dm_2['dm_id'], 0).json()['messages']) == 2
    assert msg1 != msg4
    assert msg1 != msg3
    
    msg5 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'DM 1 > DM 2').json()
    msg6 = message_senddm_v1(user_1['token'], dm_2['dm_id'], 'DM 1 stinkyyyy').json()
    msg7 = message_share_v1(user_1['token'], msg5['message_id'], '123', -1, dm_2['dm_id']).json()
    msg8 = message_share_v1(user_1['token'], msg6['message_id'], '', -1, dm_1['dm_id']).json()
    
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages'][0]['message'] == "DM 1 stinkyyyy"
    assert dm_messages_v1(user_1['token'], dm_2['dm_id'], 0).json()['messages'][0]['message'] == "DM 1 > DM 2\n123"
    assert len(dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages']) == 4
    assert len(dm_messages_v1(user_1['token'], dm_2['dm_id'], 0).json()['messages']) == 4
    assert msg5 != msg8
    assert msg5 != msg7       
    clear_v1()
            
# Tests different users with different permissions in a dm
def test_different_permissions_remove_dm():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c').json()
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']]).json()
    dmsg1 = message_senddm_v1(user_2['token'], dm_1['dm_id'], 'Hello World! 1').json()
    assert message_remove_v1(user_2['token'], dmsg1['message_id']).json() == {}
    dmsg2 = message_senddm_v1(user_2['token'], dm_1['dm_id'], 'Hello World! 2').json()
    assert message_remove_v1(user_3['token'], dmsg2['message_id']).status_code == ACCESS_ERROR
    clear_v1()


# Tests invalid input
def test_senddm_invalid_input():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']]).json()
    assert message_senddm_v1(user_1['token'], dm_1['dm_id'], 'a' * 1001).status_code == INPUT_ERROR
    assert message_senddm_v1(user_1['token'], dm_1['dm_id'], 'b' * 1001).status_code == INPUT_ERROR
    assert message_senddm_v1(user_1['token'], dm_1['dm_id'], 'b' * 1001).status_code == INPUT_ERROR
    clear_v1()

# Tests invalid access
def test_senddm_invalid_access():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c').json()
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']]).json()
    assert message_senddm_v1(user_3['token'], dm_1['dm_id'], 'Sliding in').status_code == ACCESS_ERROR
    assert message_senddm_v1(user_3['token'], dm_1['dm_id'], 'Back again').status_code == ACCESS_ERROR
    clear_v1()

# Tests basic dm send
def test_senddm_basic():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']]).json()
    msg_1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Sliding in').json()
    assert type(msg_1) == dict
    assert type(msg_1['message_id']) == int
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages'][0]['message'] == "Sliding in"
    clear_v1()
    
# Tests sending the same message to multiple different channels
def test_senddm_different_channels():
    clear_v1()
    user_1 = auth_register_v2('ab@a.com', 'aaaaaa', 'a', 'a').json()
    user_2 = auth_register_v2('cd@c.com', 'bbbbbb', 'b', 'b').json()
    user_3 = auth_register_v2('ef@e.com', 'cccccc', 'c', 'c').json()
    dm_1 = dm_create_v1(user_1['token'], [user_2['auth_user_id']]).json()
    dm_2 = dm_create_v1(user_2['token'], [user_3['auth_user_id']]).json()
    dm_3 = dm_create_v1(user_3['token'], [user_1['auth_user_id']])  .json()  
    msg1 = message_senddm_v1(user_1['token'], dm_1['dm_id'], 'Hello World!').json()
    msg2 = message_senddm_v1(user_2['token'], dm_2['dm_id'], 'Hello World!').json()   
    msg3 = message_senddm_v1(user_3['token'], dm_3['dm_id'], 'Hello World!').json() 
    assert type(msg1) == dict
    assert type(msg1['message_id']) == int
    assert type(msg2) == dict
    assert type(msg2['message_id']) == int
    assert type(msg3) == dict
    assert type(msg3['message_id']) == int    
    assert dm_messages_v1(user_1['token'], dm_1['dm_id'], 0).json()['messages'][0]['message'] == "Hello World!"
    assert dm_messages_v1(user_2['token'], dm_2['dm_id'], 0).json()['messages'][0]['message'] == "Hello World!"
    assert dm_messages_v1(user_3['token'], dm_3['dm_id'], 0).json()['messages'][0]['message'] == "Hello World!"
    assert msg1 != msg2
    assert msg1 != msg3
    assert msg2 != msg3 
    clear_v1()
