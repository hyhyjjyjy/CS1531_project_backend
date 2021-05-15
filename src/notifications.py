from src.auth import findUser, getData
from src.user import user_profile_v2
from src.error import AccessError
from src.wrapper import Authorisation

@Authorisation
def notifications_get_v1(token):
    """
    Return the user's most recent 20 notifications
    
    Arguments:
        token (str) - token passed in to the function
    
    Exceptions:
        AccessError - when the token passed in is not a valid id
    
    Return value:
        {notifications} - a list of dictionaries, where each dictionary contains
                          types { channel_id, dm_id, notification_message }
                          where channel_id is the id of the channel that the
                          event happened in, and is -1 if it is being sent to a
                          DM. dm_id is the DM that the event happened in, and is
                          -1 if it is being sent to a channel. The list should
                          be ordered from most to least recent.
                          Notification_message is a string of the following
                          format for each trigger action:
                            tagged: "{User’s handle} tagged you in
                                     {channel/DM name}: {first 20 characters
                                     of the message}"
                            added to a channel/DM: "{User’s handle} added you to
                                                    {channel/DM name}"
    """

    auth_user_id = findUser(token)

    database = getData()

    # Extract all notifications relating to the concerned user from database, and
    # format each to expected "notifications type" as defined in the spec
    user_notifications_list = []

    for user_notification in database['user_notifications']:
        if user_notification['u_id'] == auth_user_id:
            formatted_notification = {
                'channel_id': user_notification['channel_id'],
                'dm_id': user_notification['dm_id'],
                'notification_message': user_notification['notification_message']
            }
            user_notifications_list.append(formatted_notification)
            
    # Reverse the user_notifications_list to get the reversed chronological order,
    # and return the 20 most recent notifications
    user_notifications_list.reverse()
    return {'notifications': user_notifications_list[0:20]}

def create_tag_notif(user_handle, src_name, message):
    '''
    Return the notification_message in the required format.
    
    Arguments:
        user_handle (str) - the tagged users' handle
        src_name (str)    - the channel/DM name from where the user was tagged
        message (str)     - the message in which the user was tagged
    
    Return value:
        (str) - the formatted notification_message
    '''
    
    return f"{user_handle} tagged you in {src_name}: {message[0:20]}"

def create_add_notif(user_handle, src_name):
    '''
    Return the notification_message in the required format.
    
    Arguments:
        user_handle (str) - the tagged users' handle
        src_name (str)    - the channel/DM name from where the user was tagged
    
    Return value:
        (str) - the formatted notification_message
    '''
    return f"{user_handle} added you to {src_name}"

def create_react_notif(user_handle, src_name):
    '''
    Return the notification_message in the required format.
    
    Arguments:
        user_handle (str) - the tagged users' handle
        src_name (str)    - the channel/DM name from where the user was tagged
    
    Return value:
        (str) - the formatted notification_message
    '''
    return f"{user_handle} reacted to your message in {src_name}"

def new_added_notification(token, channel_id, dm_id, u_id):
    '''
    Returns a notification dictionary in the expected format after a user is 
    added to a channel/dm
    
    Arguments:
        token (str) - token of the auth user who added the new user
        channel_id (int) - id of the channel in which it occured
        dm_id (int) - id of the dm in which it occured
        u_id (int) - id of the user being added
        
    Return value:
        {
            'u_id': u_id
            'channel_id': channel_id,
            'dm_id': dm_id,
            'notification_message': message
        }
    '''
    
    database = getData()
    
    auth_user_id = findUser(token)
    user_handle = user_profile_v2(token, auth_user_id)['user']['handle_str']
    
    # Find the channel/dm name given channel/dm id
    src_name = get_channel_dm_name(database, channel_id, dm_id)

    return {
        'u_id': u_id,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'notification_message': create_add_notif(user_handle, src_name)
    }

def new_tagged_notification(token, channel_id, dm_id, u_id, message):
    database = getData()
    
    auth_user_id = findUser(token)
    user_handle = user_profile_v2(token, auth_user_id)['user']['handle_str']
    
    # Find the channel/dm name given channel/dm id
    src_name = get_channel_dm_name(database, channel_id, dm_id)

    return {
        'u_id': u_id,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'notification_message': create_tag_notif(user_handle, src_name, message)
    }
    
def new_react_notification(token, channel_id, dm_id, u_id):
    database = getData()
    
    auth_user_id = findUser(token)
    user_handle = user_profile_v2(token, auth_user_id)['user']['handle_str']
    
    # Find the channel/dm name given channel/dm id
    src_name = get_channel_dm_name(database, channel_id, dm_id)    

    return {
        'u_id': u_id,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'notification_message': create_react_notif(user_handle, src_name)
    }
    
def get_channel_dm_name(database, channel_id, dm_id):
    if channel_id != -1 and dm_id == -1: # channel is the source
        for channel in database['channels']:
            if channel_id == channel['channel_id']:
                src_name = channel['channel_name']
    elif channel_id == -1 and dm_id != -1: # dm is the source
        for dm in database['dms']:
            if dm_id == dm['dm_id']:
                src_name = dm['dm_name']
    return src_name
    