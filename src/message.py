from src.error import InputError, AccessError
from src.auth import findUser, writeData, getData
from src.channel import check_validity
from src.notifications import new_tagged_notification, new_react_notification
from src.wrapper import Authorisation
from threading import Timer
import time
from src.user import append_user_stats, append_dream_stats

@Authorisation
def message_send_v2(token, channel_id, message):
    
    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        channel_id (int) - the id of the channel the message is being sent to
        message (string) - the message being sent

    Exceptions:
        InputError - Message is more than 1000 characters
        AccessError - The authorised user has not joined the channel they are trying to post to

    Return value:
        Returns {'message_id': message_id}
    '''    
    
    # Get data
    data = getData()
    
    # Get user id
    auth_user_id = findUser(token) 
    
    # Checks the message is not more than 1000 characters
    if len(message) > 1000:
        raise InputError(description="Message must be less than 1000 characters")

    # Checks the auth_user_id is part of the channel
    channel_members = get_channel_members(channel_id, data)
    if auth_user_id not in channel_members:
        raise AccessError(description="User not in channel!")
    
    # Get new message id
    new_message_id = get_new_message_id(data)
    
    # Adds message to data dictionary
    add_data(data, new_message_id, auth_user_id, channel_id, -1, message, int(time.time()), [], False)

    # Adds message to channel
    for chan in data['channels']:        
        if channel_id == chan['channel_id']:
            chan['messages'].append(new_message_id)

    # Sends notification
    send_msg_notification(data, token, message, channel_id, -1, False, -1)

    # Adds message to channel and makes notification
    append_user_stats(findUser(token), data)
    append_dream_stats(findUser(token), data)       

    writeData(data)

    return {
        'message_id': new_message_id,
    }

@Authorisation
def message_sendlater_v1(token, channel_id, message, time_sent):
    ''' Send a message from authorised user to the channel, 
    automatically at a specified time in the future

    Arguments:
        token (string)              - token of an authenticated user
                                      who is part of the channel
        channel_id (integer)        - id of channel to send message in
        message (string)            - actual message content
        time_sent (integer)         - unix timestamp of when message will be sent
    
    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
                    - Occurs when message is more than 1000 characters
                    - Occurs when time_sent before current time
        AccessError - Occurs when authorised user is not a member of channel
                    - Occurs when token is not valid

    Return value:
        {
            message_id
        }
    '''
    current_time = int(time.time())

    # Load .json data store
    data_store = getData()

    # Check validity of channel_id
    check_validity(data_store["channels"], channel_id, "channel_id", 0)

    # Check message is less than 1000 characters
    if len(message) > 1000:
        raise InputError(description="Message must be less than 1000 characters")

    # Check time_sent is in the future
    if time_sent < current_time:
        raise InputError(description="Cannot send a message in the past")

    # Get user from token and check they are member of channel
    u_id = findUser(token)
    channel_members = get_channel_members(channel_id, data_store)
    if u_id not in channel_members:
        raise AccessError(description="User not in channel!")
    
    # Get new message_id
    new_message_id = get_new_message_id(data_store)

    # Add message to data_store
    add_data(data_store, new_message_id, u_id, channel_id, -1, message, time_sent, [], False)

    # Set up thread to send message in channel later
    if (time_sent == current_time):
            # Append message to channel messages
        for channel in data_store["channels"]:
            if channel_id == channel["channel_id"]:
                channel["messages"].append(new_message_id) 
        send_msg_notification(data_store, token, message, channel_id, -1, False, new_message_id)
    else:
        sendlater_thread = Timer(time_sent - current_time, send_msg_notification, args=[data_store, token, message, channel_id, -1, True, new_message_id])
        sendlater_thread.start()

    append_user_stats(findUser(token), data_store)
    append_dream_stats(findUser(token), data_store)    

    writeData(data_store)

    return {
        "message_id" : new_message_id
    }

@Authorisation
def message_remove_v1(token, message_id):

    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        message_id (int) - the id of the message being removed

    Exceptions:
        InputError - Message id no longer exists
        AccessError - User did not send message and is not an owner of the channel/dm or dreams

    Return value:
        Returns {}
    '''        
    
    # get data
    data = getData()
    
    # get id
    auth_user_id = findUser(token)
    
    # Checks the message was sent by the user requesting to edit it or 
    # the user is a channel owner
    msg = get_message(message_id, data)
    
    if msg == -1:
        raise AccessError(description="Message does not exist")   
    
    chan_owners = []
    if msg['channel_id'] != -1:
        chan = get_channel_details(msg, data)
        chan_owners = get_channel_owners(chan['channel_id'], data)
    
    if msg['u_id'] != auth_user_id and get_user_details(auth_user_id, data)['permission_id'] != 1 and auth_user_id not in chan_owners:
        raise AccessError(description="User requesting edit did not post message or not channel/DREAMS owner")
    
    # Remove from channels/dms list    
    remove_msg_from_channel_or_dm(data, msg)

    append_user_stats(findUser(token), data)
    append_dream_stats(findUser(token), data)  
    
    writeData(data)
    
    return {
    }

@Authorisation
def message_edit_v2(token, message_id, message):

    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        message_id (int) - the id of the message being edited
        message (string) - the new message

    Exceptions:
        InputError - Message is more than 1000 characters or the message id refers to a deleted message
        AccessError - The authorised user has not joined the channel they are trying to post to

    Return value:
        Returns {}
    '''    
    
    # get data
    data = getData()
    
    # get id
    auth_user_id = findUser(token)    
    
    # Checks that the length is not above 1000 characters
    if len(message) > 1000:
        raise InputError(description="Message must be less than 1000 characters")

    # Finds the message
    msg = get_message(message_id, data)    

    if msg == -1:
        raise AccessError(description="Message does not exist")
    
    # Checks the message was sent by the user requesting to edit it or 
    # the user is a channel owner
    if msg['u_id'] != auth_user_id and get_user_details(auth_user_id, data)['permission_id'] != 1:
        raise AccessError(description="User requesting edit did not post message or not channel owner")
        
    # Delete the message if message is empty, updates the message if it isn't
    if message == '':        
        remove_msg_from_channel_or_dm(data, msg)
    else:
        msg_key = data['messages'].index(msg)
        data['messages'][msg_key]['message'] = message

    # Sends notification
    send_msg_notification(data, token, message, msg['channel_id'], msg['dm_id'], False, -1)
   
    append_user_stats(findUser(token), data)
    append_dream_stats(findUser(token), data) 
        
    writeData(data)
        
    return {
    }

@Authorisation
def message_senddm_v1(token, dm_id, message):

    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        dm_id (int) - the id of the dm the message is being sent to
        message (string) - the message being sent

    Exceptions:
        InputError - Message is more than 1000 characters
        AccessError - The authorised user has not joined the dm they are trying to post to

    Return value:
        Returns {'message_id': message_id}
    '''        
    
    # get data
    data = getData()
    
    # get id
    auth_user_id = findUser(token)     
    
    # Checks the message is not more than 1000 characters
    if len(message) > 1000:
        raise InputError(description="Message must be less than 1000 characters")

    # Checks the auth_user_id is part of the dm
    dm_members = get_dm_members(dm_id, data)
    if auth_user_id not in dm_members:
        raise AccessError(description="User not in DM being posted to")
    
    # Get new message id
    new_message_id = get_new_message_id(data)
    
    # Adds message to data dictionary
    add_data(data, new_message_id, auth_user_id, -1, dm_id, message, int(time.time()), [], False)

    # Adds message to dm
    for dm in data['dms']:
        if dm_id == dm['dm_id']:
            dm['message_ids'].append(new_message_id)    
    
    # Sends notification
    send_msg_notification(data, token, message, -1, dm_id, False, -1)

    append_user_stats(findUser(token), data)
    append_dream_stats(findUser(token), data)      

    # Adds message to dm and makes notification
    writeData(data)
    
    return {
        'message_id': new_message_id,
    } 

@Authorisation
def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    ''' Send a message from authorised user to the dm, 
    automatically at a specified time in the future

    Arguments:
        token (string)         - token of an authenticated user
                                 who is part of the dm
        dm_id (integer)        - id of dm to send message in
        message (string)       - actual message content
        time_sent (integer)    - unix timestamp of when message will be sent
    
    Exceptions:
        InputError  - Occurs when dm_id is not a valid dm
                    - Occurs when message is more than 1000 characters
                    - Occurs when time_sent before current time
        AccessError - Occurs when authorised user is not a member of dm
                    - Occurs when token is not valid

    Return value:
        {
            message_id
        }
    '''
    current_time = int(time.time())

    # Load .json data store
    data_store = getData()

    # Check validity of dm_id
    check_validity(data_store["dms"], dm_id, "dm_id", 3)

    # Check message is less than 1000 characters
    if len(message) > 1000:
        raise InputError(description="Message must be less than 1000 characters")

    # Check time_sent is in the future
    if time_sent < current_time:
        raise InputError(description="Cannot send a message in the past")

    # Get user from token and check they are member of channel
    u_id = findUser(token)
    dm_members = get_dm_members(dm_id, data_store)
    if u_id not in dm_members:
        raise AccessError(description="User not in dm being posted to")
    
    # Get new message_id
    new_message_id = get_new_message_id(data_store)

    # Add message to data_store
    add_data(data_store, new_message_id, u_id, -1, dm_id, message, time_sent, [], False)

    # Set up thread to send message in dm later
    if (time_sent == current_time):
        for dm in data_store["dms"]:
            if dm_id == dm["dm_id"]:
                dm["message_ids"].append(new_message_id)
        send_msg_notification(data_store, token, message, -1, dm_id, False, new_message_id)
    else:
        sendlater_thread = Timer(time_sent - current_time, send_msg_notification, args=[data_store, token, message, -1, dm_id, True, new_message_id])
        sendlater_thread.start()

    append_user_stats(findUser(token), data_store)
    append_dream_stats(findUser(token), data_store)      

    writeData(data_store)

    return {
        "message_id" : new_message_id
    }

@Authorisation
def message_share_v1(token, og_message_id, message, channel_id, dm_id):

    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        og_message_id - the id of the inital message
        message (string) - the message being appended at the end of the share
        channel_id (int) - the id of the channel the message is being sent to
        dm_id (int) - the id of the dm the message is being sent to

    Exceptions:
        InputError - Message is more than 1000 characters
        AccessError - The authorised user has not joined the channel/dm they are trying to share to

    Return value:
        Returns {'shared_message_id': shared_message_id}
    '''        
    
    # get data
    data = getData()
    
    # get id
    auth_user_id = findUser(token)  
    
    # Checks that the user is part of the channel or dm they are sharing to    
    channel_members = get_channel_members(channel_id, data)
    dm_members = get_dm_members(dm_id, data)

    if auth_user_id not in channel_members and auth_user_id not in dm_members:
        raise AccessError(description="User not member of channel")
        
    # Get og message
    msg = get_message(og_message_id, data)

    # Check user has access to og message
    if auth_user_id != msg['u_id']:
        raise AccessError("User not member of channel from which the message comes from")

    # Checks the new message is not more than 1000 characters
    if len(msg['message'] + '\n' + message) > 1000 and message != '':
        raise InputError(description="Message must be less than 1000 characters")
    
    # Get new message id
    new_message_id = get_new_message_id(data)
    
    # Copies og message
    new_msg = msg['message']
    
    # Add optional message at end
    if message != '':
        new_msg = msg['message'] + '\n' + message

    # Adds message to data dictionary field 'messages'
    add_data(data, new_message_id, auth_user_id, channel_id, -1, new_msg, int(time.time()), [], False)
    
    # Share to DM/Channel
    if channel_id != -1 and dm_id != -1:
        raise InputError("Usage: One of channel_id or dm_id must be -1.")
    elif channel_id == -1:
        # Adds message to dm
        for dm in data['dms']:        
            if dm_id == dm['dm_id']:
                dm['message_ids'].append(new_message_id)
     
    else:        
        # Adds message to channel
        for chan in data['channels']:        
            if channel_id == chan['channel_id']:
                chan['messages'].append(new_message_id)  

    # Sends notification
    send_msg_notification(data, token, new_msg, channel_id, dm_id, False, -1)

    append_user_stats(findUser(token), data)
    append_dream_stats(findUser(token), data)  
    
    writeData(data)
    
    return {
        'shared_message_id': new_message_id     
    }

def message_react_v1(token, message_id, react_id):

    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        message_id - the id of the message being reacted to
        react_id (int) - the id of the react

    Exceptions:
        InputError - message_id is not a valid message within a channel or DM that the authorised user has joined
        InputError - react_id is not a valid React ID. The only valid react ID the frontend has is 1
        InputError - Message with ID message_id already contains an active React with ID react_id from the authorised user
        AccessError - The authorised user is not a member of the channel or DM that the message is within

    Return value:
        Returns {}
    '''   
    
    # get data
    data = getData()
    
    # get id
    auth_user_id = findUser(token)
    
    # Gets message
    msg = get_message(message_id, data)
    
    # Message does not exist (has been removed or invalid message_id passed in)
    if msg == -1:
        raise InputError("Message is not a valid.")
    
    # Gets message key
    msg_key = data['messages'].index(msg)

    # Gets list of dictionary containing all the reacts for that message
    react_list = data['messages'][msg_key]['reacts']

    # Checks react id is valid and not in use already
    if react_id != 1:
        raise InputError("React ID is not valid.")
    elif has_user_reacted(auth_user_id, react_id, react_list, data):
        raise InputError("User has already reacted with this react.")
    
    # Checks the user is part of the channel/dm
    check_user_permissions(data, msg_key, auth_user_id)
    
    # Add/update react
    react_key = get_react(react_id, react_list, msg_key, data)
    if react_key == -1:
        data['messages'][msg_key]['reacts'].append({
            'react_id' : react_id,
            'u_ids' : [auth_user_id]
        })
    else:
        data['messages'][msg_key]['reacts'][react_key]['u_ids'].append(auth_user_id)
        
    # Send notification
    user_notification = new_react_notification(token, msg['channel_id'], msg['dm_id'], msg['u_id'])
    data['user_notifications'].append(user_notification)    
    
    writeData(data)
        
    return {}

def message_unreact_v1(token, message_id, react_id):

    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        message_id - the id of the message being reacted to
        react_id (int) - the id of the react

    Exceptions:
        InputError - message_id is not a valid message within a channel or DM that the authorised user has joined
        InputError - react_id is not a valid React ID. The only valid react ID the frontend has is 1
        InputError - Message with ID message_id does not contain an active React with ID react_id from the authorised user
        AccessError - The authorised user is not a member of the channel or DM that the message is within

    Return value:
        Returns {}
    '''  
    
    # get data
    data = getData()
    
    # get id
    auth_user_id = findUser(token)
    
    # Gets message
    msg = get_message(message_id, data)
    
    # Message does not exist (has been removed or invalid message_id passed in)
    if msg == -1:
        raise InputError("Message is not a valid.")
    
    # Gets message key
    msg_key = data['messages'].index(msg)

    # Gets list of dictionary containing all the reacts for that message
    react_list = data['messages'][msg_key]['reacts']

    # Checks react id is valid and in use already
    if react_id != 1:
        raise InputError("React ID is not valid.")
    elif not has_user_reacted(auth_user_id, react_id, react_list, data):
        raise InputError("User has not already reacted with this react.")
    
    # Checks the user is part of the channel/dm
    check_user_permissions(data, msg_key, auth_user_id)        
    
    # Remove/update react
    react_key = get_react(react_id, react_list, msg_key, data)
    data['messages'][msg_key]['reacts'][react_key]['u_ids'].remove(auth_user_id)
    if data['messages'][msg_key]['reacts'][react_key]['u_ids'] == []:
        data['messages'][msg_key]['reacts'].remove({'react_id' : react_id, 'u_ids' : []})
        
    writeData(data)
    
    return {}

def message_pin_v1(token, message_id):

    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        message_id - the id of the message being pinned

    Exceptions:
        InputError - message_id is not a valid message
        InputError - Message with ID message_id is already pinned
        AccessError - The authorised user is not a member of the channel or DM that the message is within or the authorised user is not an owner of the channel or DM

    Return value:
        Returns {}
    '''  
    
    # get data
    data = getData()
    
    # get id
    auth_user_id = findUser(token)
    
    # Gets message
    msg = get_message(message_id, data)
    
    # Message does not exist (has been removed or invalid message_id passed in)
    if msg == -1:
        raise InputError("Message is not a valid.")
    
    # Gets message key
    msg_key = data['messages'].index(msg)

    # Checks if message is already pinned
    if data['messages'][msg_key]['is_pinned']:
        raise InputError("Message is already pinned.")
    
    # Checks the user is part of/an owner of the channel/dm
    check_user_owners_permissions(data, msg_key, auth_user_id)
    
    # Add pin
    data['messages'][msg_key]['is_pinned'] = True
        
    writeData(data)
    
    return {}    
    
def message_unpin_v1(token, message_id):

    '''
    Arguments:
        token (string) - the token of the user who wants to create a channel
        message_id - the id of the message being pinned

    Exceptions:
        InputError - message_id is not a valid message
        InputError - Message with ID message_id is already unpinned
        AccessError - The authorised user is not a member of the channel or DM that the message is within or the authorised user is not an owner of the channel or DM

    Return value:
        Returns {}
    '''  
    
    # get data
    data = getData()
    
    # get id
    auth_user_id = findUser(token)
    
    # Gets message
    msg = get_message(message_id, data)
    
    # Message does not exist (has been removed or invalid message_id passed in)
    if msg == -1:
        raise InputError("Message is not a valid.")
    
    # Gets message key
    msg_key = data['messages'].index(msg)

    # Checks if message is already unpinned
    if not data['messages'][msg_key]['is_pinned']:
        raise InputError("Message is already unpinned.")
    
    # Checks the user is part of/an owner of the channel/dm
    check_user_owners_permissions(data, msg_key, auth_user_id)
    
    # Add pin
    data['messages'][msg_key]['is_pinned'] = False
        
    writeData(data)
    
    return {}

def add_data(data, message_id, u_id, channel_id, dm_id, message, time_created, reacts, is_pinned):
    data['messages'].append({
        'message_id' : message_id,
        'u_id' : u_id,
        'channel_id': channel_id,
        'dm_id' : dm_id,
        'message' : message,         
        'time_created' : time_created,    
        'reacts' : reacts,
        'is_pinned' : is_pinned,
    })
    return

def get_channel_members(channel_id, data):
    member_list = []
    for chan in data['channels']:
        if chan['channel_id'] == channel_id:
            for user in chan['all_members']:
                member_list.append(user['u_id'])
        
    return member_list

def get_channel_owners(channel_id, data):
    owner_list = []
    for chan in data['channels']:
        if chan['channel_id'] == channel_id:
            for user in chan['owner_members']:
                owner_list.append(user['u_id'])
        
    return owner_list
        
def get_message(message_id, data):
    for msg in data['messages']:
        if msg['message_id'] == message_id:
            return msg
    
    return -1
        
def get_channel_details(msg, data):
    for chan in data['channels']:
        if msg['channel_id'] == chan['channel_id']:
            return chan
        
def get_dm_details(msg, data):
    for dm in data['dms']:
        if msg['dm_id'] == dm['dm_id']:
            return dm
        
def get_user_details(auth_user_id, data):
    for user in data['users']:
        if auth_user_id == user['u_id']:
            return user
        
def get_dm_members(dm_id, data):
    member_list = []
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            member_list = dm['dm_members']
                
    return member_list

def get_dm_owner(dm_id, data):
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            return dm['dm_owner']

def get_new_message_id(data):
    if data["messages"] == []:
        new_message_id = 1
    else:
        new_message_id = data["messages"][-1]["message_id"] + 1
    return new_message_id

def send_msg_notification(data, token, message, channel_id, dm_id, is_sendlater, new_message_id):
    if (is_sendlater):
        data = getData()
        if dm_id == -1:
            # Append message to channel messages
            for channel in data["channels"]:
                if channel_id == channel["channel_id"]:
                    channel["messages"].append(new_message_id) 
        else:
            # Append message to dm messages
            for dm in data["dms"]:
                if dm_id == dm["dm_id"]:
                    dm["message_ids"].append(new_message_id)                        

    words = message.split()
    handle_list = []
    for word in words:
        if word[0] == '@':
            word = word.replace(',','')
            handle_list.append(word[1:])
    
    u_id = -1
    handle_status = False
    member_status = False   
    for handle in handle_list:
        u_id = -1
        handle_status = False
        member_status = False  
        for user in data['users']:
            if handle == user['handle_str']:
                handle_status = True
                u_id = user['u_id']
        
        if dm_id == -1:        
            channel_ids = {'channel_id' : channel_id}
            channel = get_channel_details(channel_ids, data)
            for members in channel['all_members']:
                if u_id == members['u_id']:
                    member_status = True
        else:
            dm_ids = {'dm_id' : dm_id}
            dm = get_dm_details(dm_ids, data)
            
            if u_id in dm['dm_members']:  
                member_status = True            

        if handle_status == True and member_status == True:
            user_notification = new_tagged_notification(token, channel_id, dm_id, u_id, message)
            data['user_notifications'].append(user_notification)

    writeData(data)


def has_user_reacted(auth_user_id, react_id, react_list, data):
    for reacts in react_list:
        if react_id == reacts['react_id']:
            if auth_user_id in reacts['u_ids']:    
                return True
    return False

def get_react(react_id, react_list, msg_key, data):
    for reacts in react_list:
        if react_id == reacts['react_id']:
            return data['messages'][msg_key]['reacts'].index(reacts)
    return -1

def remove_msg_from_channel_or_dm(data, msg):
    if msg['dm_id'] == -1:
        chan = get_channel_details(msg, data)
        chan_key = data['channels'].index(chan)
        data['channels'][chan_key]['messages'].remove(msg['message_id'])         
    else:
        dm = get_dm_details(msg, data)
        dm_key = data['dms'].index(dm)
        data['dms'][dm_key]['message_ids'].remove(msg['message_id'])
    data['messages'].remove(msg)

def check_user_permissions(data, msg_key, auth_user_id):
    if data['messages'][msg_key]['dm_id'] == -1:
        channel_members = get_channel_members(data['messages'][msg_key]['channel_id'], data)
        if auth_user_id not in channel_members:
            raise AccessError("User not in channel")
    else:
        dm_members = get_dm_members(data['messages'][msg_key]['dm_id'], data)
        if auth_user_id not in dm_members:
            raise AccessError("User not in DM")       
    
def check_user_owners_permissions(data, msg_key, auth_user_id):
    if data['messages'][msg_key]['dm_id'] == -1:
        channel_members = get_channel_members(data['messages'][msg_key]['channel_id'], data)
        owner_members = get_channel_owners(data['messages'][msg_key]['channel_id'], data)
        if auth_user_id not in channel_members or auth_user_id not in owner_members:
            raise AccessError("User not in channel or not channel owner")
    else:
        dm_members = get_dm_members(data['messages'][msg_key]['dm_id'], data)
        if auth_user_id not in dm_members or auth_user_id != get_dm_owner(data['messages'][msg_key]['dm_id'], data):
            raise AccessError("User not in DM or not DM owner") 
