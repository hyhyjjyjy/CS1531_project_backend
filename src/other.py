from src.auth import findUser
from src.channel import channel_messages_v2
from src.channels import channels_list_v2
from src.dms import dm_list_v1, dm_messages_v1
from src.error import InputError, AccessError
from src.wrapper import Authorisation
import json
import time

def clear_v1():
    '''
    Arguments:
        nothing

    Exception:
        nothing

    Return values:
        empty dictionary 
    '''
    timestamp = int(time.time())
    initial_state = {
        'session_id': -1,
        'users': [],
        'removed_users' : [],
        'channels': [],
        'messages': [],
        'dms': [],
        'user_notifications': [],
        'dream_stats' : { 'channels_exist' : [{'num_channels_exist' :0, 'time_stamp' : timestamp,}],
                         'dms_exist' : [{'num_dms_exist' :0, 'time_stamp' : timestamp,}],
                         'messages_exist' : [{'num_messages_exist' :0, 'time_stamp' : timestamp,}],
                         'utilization_rate' : 0,
                        }
    }
    
    with open('src/export.json', 'w') as outfile:
        json.dump(initial_state, outfile)

    return {}

@Authorisation
def search_v2(token, query_str):
    """ Given a query string, return a collection of messages in
    all the channels/DMs that the authorised user has joined
    that match the query

    Arguments:
        token (string)          - token of authenticated user
        query_str (string)      - string to be searched for

    Exceptions:
        InputError  - Occurs when query_str is above 1000 characters
                    - Occurs when query_str is empty
        AccessError - Occurs when token is invalid

    Return value:
        {
            messages      - List of dictionaries, 
                            where each dictionary contains types: 
                            {message_id, u_id, message, time_created}
        }
    """

    # Check validity of token
    findUser(token)

    # Check query_str is less than 1000 characters or not empty
    if len(query_str) > 1000:
        raise InputError(description="query string can't be over 1000 characters")
    if len(query_str) == 0:
        raise InputError(description="query string can't be empty")

    # Define messages return type
    message_dict = {
        "messages" : []
    }

    # Go through channels
    u_channels_list = channels_list_v2(token)["channels"]
    for channel in u_channels_list:
        msgs = channel_messages_v2(token, channel["channel_id"], 0)
        look_for_message(query_str, msgs, message_dict)
        while msgs["end"] != -1:
            msgs = channel_messages_v2(token, channel["channel_id"], msgs["end"])
            look_for_message(query_str, msgs, message_dict)

    # Go through dms
    u_dms_list = dm_list_v1(token)["dms"]
    for dm in u_dms_list:
        msgs = dm_messages_v1(token, dm["dm_id"], 0)
        look_for_message(query_str, msgs, message_dict)
        while msgs["end"] != -1:
            msgs = dm_messages_v1(token, dm["dm_id"], msgs["end"])
            look_for_message(query_str, msgs, message_dict)
    
    return message_dict

def look_for_message(query_str, msgs, message_dict):
    for messages in msgs["messages"]:
        if query_str in messages["message"]:
            message_dict["messages"].append(messages)
