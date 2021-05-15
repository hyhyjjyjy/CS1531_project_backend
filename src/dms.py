import json
import jwt
from src.notifications import new_added_notification
SECRET = 'sempai'
from src.error import InputError, AccessError
from src.admin import getData, findUser
from src.wrapper import Authorisation
from src.user import append_user_stats, append_dream_stats
from src.message import message_remove_v1, get_dm_details

file_address = "src/export.json"

@Authorisation
def dm_create_v1(user_token, u_id_list):

    '''
    the function is given a user_token, which is encoded and is a string. Also, the function
    is given a list of user id. We need to use the proper parameters to create a direct message\
    and return the dm_id as a integer
    Arguments:
        user_token (string)    - some encoded information about one auth user
        u_id_list (list of int)    -  a list of user ids who are going to be in the dm
    ...

    Exceptions:
        AccessError - Occurs when the token is not a valid token

    Return Value:
        Returns {'dm_id': dm_id,
                 'dm_name': dm_name,}

    '''

    database = {}
    with open(file_address, "r") as f:
        database = json.load(f)
    
    auth_user_id = findUser(user_token)


    #the user_id of the creater of the dm
    user_name_list = []
    u_id_list.append(auth_user_id)

    #check all if all the u_id is valid and get their handle to generate the name of dm
    for some_u_id in u_id_list:
        new_user = use_id_to_find_user(some_u_id)
        if new_user == {}:
            raise InputError(description="Invalid u_id in the u_ids list.")
        user_name_list.append(new_user['handle_str'])
    

    user_name_list.sort(reverse=False)

    #generate the name of the new dm
    dm_name = ""
    dm_name += user_name_list[0]
    for i in range(1, len(user_name_list)):
        dm_name += ", "
        dm_name += user_name_list[i]

    #generate the new dm_id
    if len(database['dms']) == 0:
        dm_id = 1
    else:
        dm_id = database['dms'][len(database['dms']) - 1]['dm_id'] + 1

    #store the new dm into the database
    new_dm = {'dm_id' : dm_id,
              'dm_name': dm_name,
              'dm_owner': auth_user_id,
              'dm_members': u_id_list,
              'message_ids':[],}
    
    database['dms'].append(new_dm)
    
    #put the data back to the data file
    with open(file_address, "w") as f:
        json.dump(database, f)

    # Open file again to get updated database
    with open(file_address, "r") as f:
        database = json.load(f)
    
    # Create a notification for the added users
    for user in u_id_list:
        if auth_user_id != user:    
            user_notification = new_added_notification(user_token, -1, dm_id, user)
            database['user_notifications'].append(user_notification)

    append_user_stats(findUser(user_token), database)
    for u_id in u_id_list:
            append_user_stats(u_id, database)
    append_dream_stats(findUser(user_token), database)   

    # Put the data back to the data file
    with open(file_address, "w") as f:
        json.dump(database, f)
        
    return {'dm_id': dm_id,
            'dm_name': dm_name,}



@Authorisation
def dm_remove_v1(user_token, dm_id):
    '''
    the function is given a token and a dm_id. we need to user the parameters to
    remove the exactly dm with the dm_id. also, we need to check the validity of the 
    paremeters. 
    Arguments:
        user_token (string)    - some encoded information about one auth user
        dm_id (int)    -  the id of the dm needed removing
    ...

    Exceptions:
        AccessError - Occurs when the token is not a valid token
        InputError - Occurs when dm_id is not valid
        AccessError - Occurs when the auth_user is not the owner of the dm

    Return Value:
        Returns {}
    '''


    database = {}
    with open(file_address, "r") as f:
        database = json.load(f)
    
    #get the required value
    kicker_id = findUser(user_token)

    #check if the input is valid
    if dm_id > database['dms'][len(database['dms']) - 1]['dm_id'] or database['dms'][dm_id - 1]['dm_id'] == -1:
        raise InputError(description="The dm_id is not valid.")

    
    if kicker_id != database['dms'][dm_id - 1]['dm_owner']:
        raise AccessError(description="The one who wants to remove the dm_id does not have right.")

    for msg_id in database['dms'][dm_id - 1]['message_ids']:
        for message in database['messages']:
            if message['message_id'] == msg_id:
                msg = message
                dm = get_dm_details(msg, database)
                dm_key = database['dms'].index(dm)
                database['dms'][dm_key]['message_ids'].remove(msg['message_id'])
                database['messages'].remove(msg)

    #remove the dm with some specific dm_id
    database['dms'][dm_id - 1]['dm_id'] = -1

    append_user_stats(findUser(user_token), database)
    for u_id in database['dms'][dm_id - 1]['dm_members']:
            append_user_stats(u_id, database)
    append_dream_stats(findUser(user_token), database) 

    #put the data back to the data file
    with open(file_address, "w") as f:
        json.dump(database, f)

    return {}

@Authorisation
def dm_details_v1(user_token, dm_id):
    '''
    the function is given a token and dm_id, we need to check the validity first
    and return the details of the dm in a dictionary in correct format.

    Arguments:
        user_token (string)    - some encoded information about one auth user
        dm_id (int)    -  the id of the dm needed removing
    ...

    Exceptions:
        AccessError - Occurs when the token is not a valid token
        InputError - Occurs when dm_id is not valid
        AccessError - Occurs when the auth_user is not the member of the dm

    Return Value:
        Returns {'name': dm_name,(the name of dm)
                'members': members,(the members of dm)}
    '''

    database = {}
    with open(file_address, "r") as f:
        database = json.load(f)
    
    #get the required value
    auth_user_id = findUser(user_token)


    #check if the input is valid
    if dm_id > database['dms'][len(database['dms']) - 1]['dm_id'] or database['dms'][dm_id - 1]['dm_id'] == -1:
        raise InputError(description="The dm_id is not valid.")

    if auth_user_id not in database['dms'][dm_id - 1]['dm_members']:
        raise AccessError(description="The one who wants to show the dm details is not in the dm.")


    dm_name = database['dms'][dm_id - 1]['dm_name']
    members = []
    for some_member_id in database['dms'][dm_id - 1]['dm_members']:
        some_user = use_id_to_find_user(some_member_id)
        name_first = some_user['name_first']
        name_last = some_user['name_last']
        u_id = some_user['u_id']
        email = some_user['email']
        handle_str = some_user['handle_str']
        new_member = {  'u_id': u_id,
                        'name_first': name_first,
                        'name_last': name_last,
                        'email': email,
                        'handle_str': handle_str,
                        'profile_img_url' : some_user['profile_img_url'],
                        }
        members.append(new_member)


    return {'name': dm_name,
            'members': members,}

@Authorisation
def dm_list_v1(user_token):
    '''
    the function is given a token and we need to return the dms which the user is in.
    the returned dictionary should be in right format.
    Arguments:
        user_token (string)    - some encoded information about one auth user

    Exceptions:
        AccessError - Occurs when the token is not a valid token

    Return Value:
        Returns {'dms': dms(a list of dm detail which the user is in)}
    '''
    database = {}
    with open(file_address, "r") as f:
        database = json.load(f)
    
    #get the required value
    auth_user_id = findUser(user_token)


    dms = []

    for some_dm in database['dms']:
        if auth_user_id in some_dm['dm_members'] and some_dm['dm_id'] != -1:
            dm_id = some_dm['dm_id']
            dm_name = some_dm['dm_name']
            dms.append({'dm_id': dm_id,
                        'name': dm_name,})


    return {'dms': dms,}

@Authorisation
def dm_leave_v1(user_token, dm_id):
    '''
    The function is given the token who is gonna leave the dm without destroy the dm.
    Arguments:
        user_token (string)    - some encoded information about one auth user
        dm_id (int)    -  the id of the dm needed removing
    ...

    Exceptions:
        AccessError - Occurs when the token is not a valid token
        InputError - Occurs when dm_id is not valid
        AccessError - Occurs when the auth_user is not the member of the dm

    Return Value:
        Returns {}
    '''
    database = {}
    with open(file_address, "r") as f:
        database = json.load(f)

    #get the required value
    auth_user_id = findUser(user_token)
    
    #check if the input is valid
    if dm_id > database['dms'][-1]['dm_id'] or database['dms'][dm_id - 1]['dm_id'] == -1:
        raise InputError(description="The dm_id is not valid.")

    
    if auth_user_id not in database['dms'][dm_id - 1]['dm_members']:
        raise AccessError(description="The one who wants to leave the dm is not in the dm.")

    #remove the dm with some specific dm_id

    pos = database['dms'][dm_id - 1]['dm_members'].index(auth_user_id, 0, len(database['dms'][dm_id - 1]['dm_members']))
    
    database['dms'][dm_id - 1]['dm_members'].pop(pos)

    if len(database['dms'][dm_id - 1]['dm_members']) == 0:
        database['dms'][dm_id - 1]['dm_id'] = -1
    elif database['dms'][dm_id - 1]['dm_owner'] == auth_user_id:
        database['dms'][dm_id - 1]['dm_owner'] = database['dms'][dm_id - 1]['dm_members'][0]
 
    append_user_stats(findUser(user_token), database)
    append_dream_stats(findUser(user_token), database)    
       
    #put the data back to the data file
    with open(file_address, "w") as f:
        json.dump(database, f)
        
    return {}

    
@Authorisation
def dm_invite_v1(user_token, dm_id, u_id):
    '''
    the function is given a invitor token, a dm id, and the invited's id.
    the invited id should be added into the member list in the dm.
    Arguments:
        user_token (string)    - some encoded information about one auth user
        dm_id (int)    -  the id of the dm needed removing
        u_id (int)    -  the id of the user been invited
    ...

    Exceptions:
        AccessError - Occurs when the token is not a valid token
        InputError - Occurs when dm_id is not valid
        InputsError - Occurs when the u_id is not valid
        AccessError - Occurs when the auth_user is not the member of the dm

    Return Value:
        Returns {}
    '''
    #get the value
    invited_id = u_id
    database = {}
    with open(file_address, "r") as f:
        database = json.load(f)
    
    #get the required value
    invitor_id = findUser(user_token)
    
    #check if the dm id valid
    if dm_id > database['dms'][len(database['dms']) - 1]['dm_id'] or database['dms'][dm_id - 1]['dm_id'] == -1:
        raise InputError(description="The dm_id is not valid.")

    invited_user = use_id_to_find_user(invited_id)
    if invited_user == {} or invited_id in database['dms'][dm_id - 1]['dm_members']:
        raise InputError(description="The user who will be invited does not have the correct id.")

    if invitor_id not in database['dms'][dm_id - 1]['dm_members']:
        raise AccessError(description="The one who wants to invite someone to the dm is not in the dm.")

    database['dms'][dm_id - 1]['dm_members'].append(invited_id)

    #put the data back to the data file
    with open(file_address, "w") as f:
        json.dump(database, f)
        
    # Open file again to get updated database
    with open(file_address, "r") as f:
        database = json.load(f)
    
    # Create a notification for the added user
    user_notification = new_added_notification(user_token, -1, dm_id, u_id)
    database['user_notifications'].append(user_notification)

    append_user_stats(invited_id, database)
    append_dream_stats(findUser(user_token), database)    
        
    # Put the data back to the data file
    with open(file_address, "w") as f:
        json.dump(database, f)
    
    return {}

@Authorisation
def dm_messages_v1(user_token, dm_id, start):
    '''
    the function is given a token, a dm_id and, a start number.
    We need to return the dm message in the specific dm and should start from some position.
    Arguments:
        user_token (string)    - some encoded information about one auth user
        dm_id (int)    -  the id of the dm needed removing
        start (int)    -  the position where the message should start with
    ...

    Exceptions:
        AccessError - Occurs when the token is not a valid token
        InputError - Occurs when dm_id is not valid
        InputsError - Occurs when the start is not valid
        AccessError - Occurs when the auth_user is not the member of the dm

    Return Value:
        Returns {'messages': messages,
                'start': start,
                'end': end,}
    '''
    database = getData()
    
    auth_user_id = findUser(user_token)

    

    #check if the dm id valid
    if dm_id > database['dms'][len(database['dms']) - 1]['dm_id'] or database['dms'][dm_id - 1]['dm_id'] == -1:
        raise InputError(description="The dm_id is not valid.")

    if start > len(database['dms'][dm_id - 1]['message_ids']):
        raise InputError(description="The start of the messages of dm exceed the least recent one.")
    
    if auth_user_id not in database['dms'][dm_id - 1]['dm_members']:
        raise AccessError(description="The one who wants to send the direct message is not in the dm.")

    

    messages = []
    dm_message_list =  database['dms'][dm_id - 1]['message_ids']
    dm_message_list = list(reversed(dm_message_list))
    end = min(start + 49, len(dm_message_list) - 1)
    for i in range(start, end + 1):
        message_id = dm_message_list[i]
        msg = {}
        for l in database['messages']:
            if message_id == l['message_id']:
                msg = l
        time_created = msg['time_created']
        u_id = msg['u_id']
        message = msg['message']
        reacts = get_react_from_id(message_id, u_id, database)
        messages.append({'message_id': message_id,
                        'u_id': u_id,
                        'message': message,
                        'time_created': time_created,
                        'reacts' : reacts,
                        'is_pinned' : msg['is_pinned']})

    if end == len(dm_message_list) - 1:
        end = -1
    else:
        end = start + 50
    return {'messages': messages,
            'start': start,
            'end': end,}


def use_id_to_find_user(u_id):
    data = getData()
    for user in data['users']:
        if user['u_id'] == u_id:
            return user

    return {}

def get_react_from_id(message_id, u_id, database):
    for msg in database['messages']:
        if msg['message_id'] == message_id:
            for index, reacts in enumerate(msg['reacts']):
                if u_id in reacts['u_ids']:
                    msg['reacts'][index]['is_this_user_reacted'] = True
                else:
                    msg['reacts'][index]['is_this_user_reacted'] = False
            return msg['reacts']
            