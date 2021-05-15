from src.auth import getData, writeData, findUser
from src.error import InputError
from src.wrapper import Authorisation
from src.user import append_user_stats, append_dream_stats


@Authorisation
def channels_list_v2(token):
    """ 
    Given a user's token, returns a list of all channels and their associated details that the user is in

    Arguments:
        token (string) - token of a registered user

    Return value:
        { channels }
    """
    
    # get data
    data = getData()
    
    # get user id
    auth_user_id = findUser(token)
    
    # Creates the return list
    channel_list = []
    
    # Iterates through all the channels in the data dictionary
    for channels in data['channels']:
        
        # Checks if the user is a member in the channel
        for users in channels['all_members']:
            if auth_user_id == users['u_id']:
            
                # If member - adds the channel details to the return list
                channel_dic = {'channel_id': channels['channel_id'],
                               'name': channels['channel_name']}
                
                channel_list.append(channel_dic)
          
    writeData(data)
            
    return {'channels' : channel_list}

@Authorisation
def channels_listall_v2(token):
    """ 
    Given a user's id, returns a list of all channels and their associated details

    Arguments:
        token (string) - token of a registered user

    Return value:
        { channels }
    """   
    
    # get data
    data = getData()
    
    findUser(token)
    
    # Creates the return list
    channel_list = []
    
    # Iterates through all the channels in the data dictionary
    for channels in data['channels']:

        # Adds the channel to the return list    
        channel_dic = {'channel_id': channels['channel_id'],
                       'name': channels['channel_name']}
        
        channel_list.append(channel_dic)
    
    writeData(data)
        
    return {'channels' : channel_list}

@Authorisation
def channels_create_v2(token, name, is_public):
    '''
    Arguments:
        token (string) - the token of the one who wants to create a channel
        name (string) - the name of the channel which is going to be created
        is_public (boolean) - whether the channel is public or private

    Exceptions:
        Inputerror - occur when the name of channel is larger than 20 characters
        Accesserror - occur when the token is not valid or hasn't been registered.

    Return value:
        Returns {'channel_id': } when there is no exception being raised
    '''
    
    data = getData()
    auth_user_id = findUser(token)
    
    if len(name) > 20:
        raise InputError(description="Name too long.")
    else:
        new_channel_id = len(data['channels']) + 1
        name_last = data['users'][auth_user_id - 1]['name_last']
        name_first = data['users'][auth_user_id - 1]['name_first']
        email = data['users'][auth_user_id - 1]['email']
        handle_str = data['users'][auth_user_id - 1]['handle_str']

        is_active = False
        stand_up_finished_time = 0
        stand_up_length = 0

        data['channels'].append({  
            'channel_id': new_channel_id,  
            'channel_name' : name,      
            'all_members':  [{
                                'u_id':auth_user_id,
                                'name_last': name_last,
                                'name_first': name_first,
                                'email': email,
                                'handle_str': handle_str,
                                'profile_img_url' : data['users'][auth_user_id - 1]['profile_img_url'],

                            },],   
            'owner_members':[{
                                'u_id':auth_user_id,
                                'name_last': name_last,
                                'name_first': name_first,
                                'email': email,
                                'handle_str': handle_str,
                                'profile_img_url' : data['users'][auth_user_id - 1]['profile_img_url'],

                            },],
            'is_public' : is_public,
            'standup': {        
                                'is_active': is_active,
                                'messages':"",
                                'time_finish': stand_up_finished_time,
                                'stand_up_length': stand_up_length,
                        },

            'messages' : [],
        })

        append_user_stats(auth_user_id, data)
        append_dream_stats(auth_user_id, data)  
    
        writeData(data)
    
        return {
            'channel_id': new_channel_id,
        }
