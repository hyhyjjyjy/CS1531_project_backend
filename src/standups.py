import json
from src.error import InputError, AccessError
from src.admin import getData, findUser
from src.notifications import new_tagged_notification
from src.wrapper import Authorisation
import time
import datetime
import threading
from src.user import append_user_stats, append_dream_stats

file_address = "src/export.json"

@Authorisation
def standup_start_v1(user_token, channel_id, length):
    """The function start a standup and will last for some seconds. All the message sent in
    that time period will be buffered and send together afer that.

    Args:
        user_token (string): a token string used to authorise and get the user id
        channel_id (int): the channel id where the standup starts
        length (int): the number of seconds

    Raises:
        InputError: channel id invalid
        InputError: standup already starts
        AccessError: user not in the

    Returns:
        dictionary: {'time_finish': time_finish}
    """

    database = getData()

    auth_user_id = findUser(user_token)

    if is_channel_valid(database, channel_id) == False:
        raise InputError(description="Channel id is not valid")
    
    index = get_channel_index(database, channel_id)
    channel = database['channels'][index]

    if channel['standup']['is_active'] == True:
        raise InputError(description="Standup is already active")

    if is_user_in_channel(auth_user_id, channel) == False:
        raise AccessError(description="You are no in the channel")

    time_finish = (datetime.datetime.now()+datetime.timedelta(seconds=length)).strftime("%Y-%m-%d %H:%M:%S")
    time_finish = time.strptime(time_finish, "%Y-%m-%d %H:%M:%S")
    time_finish = time.mktime(time_finish)

    standup_length = length

    database['channels'][index]['standup']['is_active'] = True
    database['channels'][index]['standup']['standup_length'] = standup_length
    database['channels'][index]['standup']['time_finish'] = time_finish
    database['channels'][index]['standup']['messages'] = ""

    with open(file_address, "w") as f:
        json.dump(database, f)

    new_thread = threading.Timer(length, standup_package, args=[index, user_token, channel_id, time_finish])
    new_thread.start()

    return {'time_finish': time_finish}


@Authorisation
def standup_active_v1(user_token, channel_id):
    """check if the standup has started

    Args:
        user_token (string): a token string used to authorise and get the user id
        channel_id (int): the channel id where the standup starts

    Raises:
        InputError: channel id invalid

    Returns:
        dic: {'is_active': is_active,
             'time_finish': time_finish,
            }, bool for is_active, time_finish for the time when standup finishes
    """

    database = getData()

    #auth_user_id = findUser(user_token)

    if is_channel_valid(database, channel_id) == False:
        raise InputError("Channel id is not valid")
    
    index = get_channel_index(database, channel_id)
    channel = database['channels'][index]

    is_active = channel['standup']['is_active']

    if is_active == True:
        time_finish = channel['standup']['time_finish']
    else:
        time_finish = None

    return {'is_active': is_active,
            'time_finish': time_finish,
            }

@Authorisation
def standup_send_v1(user_token, channel_id, message):
    """get the messages that will be buffered

    Args:
        user_token (string): a token string used to authorise and get the user id
        channel_id (int): the channel id where the standup starts
        message (string): the message

    Raises:
        InputError: channel id invalid
        InputError: message too long
        InputError: standup not started yet
        AccessError: user not in the channel
    
    Returns:
        dic: {}
    """


    database = getData()
    auth_user_id = findUser(user_token)

    if is_channel_valid(database, channel_id) == False:
        raise InputError(description="Channel id is not valid")

    if len(message) > 1000:
        raise InputError(description="Too much charecters in message")
         
    index = get_channel_index(database, channel_id)
    channel = database['channels'][index]

    if channel['standup']['is_active'] == False:
        raise InputError(description="The channel does not have an active standup")

    if is_user_in_channel(auth_user_id, channel) == False:
        raise AccessError(description="You are no in the channel")

    user = use_id_to_find_user(auth_user_id)

    original_msg = database['channels'][index]['standup']['messages']
    if original_msg == "":
        original_msg = user['handle_str'] + ": " + message
    else:
        original_msg = original_msg + "\n" + user['handle_str'] + ": " + message 
    
    database['channels'][index]['standup']['messages'] = original_msg

    with open(file_address, "w") as f:
        json.dump(database, f)

    return {}


def standup_package(index, user_token, channel_id, time_finish):
    """a helper function to store the messages sent in the standup period
    """

    database = getData()
    new_message = database['channels'][index]['standup']['messages']
    
    auth_user_id = findUser(user_token)

    if database['messages'] == []:
        new_message_id = 1
    else:
        new_message_id = database['messages'][-1]['message_id'] + 1
    
    database['messages'].append({
        'message_id' : new_message_id,
        'u_id' : auth_user_id,
        'channel_id': channel_id,
        'dm_id' : -1,
        'message' : new_message,         
        'time_created' : time_finish,
        'reacts' : [],
        'is_pinned' : False,           
    })

    database['channels'][index]['messages'].append(new_message_id)

    database['channels'][index]['standup']['is_active'] = False
    database['channels'][index]['standup']['standup_length'] = 0
    database['channels'][index]['standup']['time_finish'] = 0
    database['channels'][index]['standup']['messages'] = ""

    append_user_stats(auth_user_id, database)
    append_dream_stats(auth_user_id, database)
    
    words = new_message.split()
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
        for user in database['users']:
            if handle == user['handle_str']:
                handle_status = True
                u_id = user['u_id']
                
        channel_ids = {'channel_id' : channel_id}
        channel = get_channel_details(channel_ids, database)
        for members in channel['all_members']:
            if u_id == members['u_id']:
                member_status = True

        with open(file_address, "w") as f:
            json.dump(database, f)

        if handle_status == True and member_status == True:
            user_notification = new_tagged_notification(user_token, channel_id, -1, u_id, new_message)
            database['user_notifications'].append(user_notification)


    with open(file_address, "w") as f:
        json.dump(database, f)
    




    
    



def is_channel_valid(database, channel_id):
    for channel in database['channels']:
        if channel['channel_id'] == channel_id:
            return True
    
    return False

def get_channel_index(database, channel_id):
    l = 0
    for channel in database['channels']:
        if channel['channel_id'] == channel_id:
            return l
        l = l + 1

def is_user_in_channel(u_id, channel):
    for user in channel['all_members']:
        if user['u_id'] == u_id:
            return True

    return False

def use_id_to_find_user(u_id):
    data = getData()
    for user in data['users']:
        if user['u_id'] == u_id:
            return user

def get_channel_details(msg, data):
    for chan in data['channels']:
        if msg['channel_id'] == chan['channel_id']:
            return chan