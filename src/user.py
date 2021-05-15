regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
secret = 'COMP1531Dorito2021'
from src.wrapper import Authorisation
from src.auth import findUser, writeData, check_email, getData
from src.error import InputError
from src import config
from PIL import Image
import urllib.request
import time
import requests

@Authorisation
def user_profile_v2(token, u_id):
    """ 
    Given  valid token and u_id, returns information regarding the user with u_id 'u_id'

    Arguments:
        token (string) - valid token associated with a registered user's session
        u_id (int) - user id associated with a registered user

    Exceptions:
        InputError - Occurs when u_id is not associated with a valid user
        AccessError - Occurs if token is invalid


    Return value:
        {'user' : {'u_id' : u_id, 
                   'email' :email,
                   'name_first' : name_first,
                   'name_last' : name_last,
                   'handle_str' : handle_str,} 
        }
    """
    #Retrieving data from export.json
    data = getData()
    #Testing for a valid token
    findUser(token)
    #Cycling through all users to find the user with user id u_id
    for user in data['users']:
        if u_id == user['u_id']:            
            #Returning the users information
            return {
                'user': {
                    'u_id': user['u_id'],
                    'email': user['email'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last'],
                    'handle_str': user['handle_str'],
                    'profile_img_url': user['profile_img_url']
                },
            }
    #Repeating the process with 'removed_users' to assist in other functions
    for user in data['removed_users']:
        if u_id == user['u_id']:            
            return {
                'user': {
                    'u_id': user['u_id'],
                    'email': user['email'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last'],
                    'handle_str': user['handle_str'],
                    'profile_img_url': user['profile_img_url']
                },
            }
    #Raising an input error if the user could not be found
    raise InputError(description="User with u_id is not a valid user")

@Authorisation
def user_profile_setname_v2(token, name_first, name_last):
    """ 
    Given  valid token and first/last names, changes a registered users name

    Arguments:
        token (string) - valid token associated with a registered user's session
        name_first (string) - first name the user wants to update to
        name_last (string) - last name the user wants to update to

    Exceptions:
        InputError - When either name_first or name_last is not between 1 and 50 characters, inclusive
        AccessError - Occurs if token is invalid


    Return value:
        {}
    """
    #Retrieving data from export.json
    data = getData()
    #Testing for a valid token and finding the associated u_id
    u_id = findUser(token)
    #Checking if the names are of valid length
    if len(name_first) > 50 or len(name_first) < 1:
        raise InputError(description="Length of first name is not valid")
    elif len(name_last) > 50 or len(name_last) < 1:
        raise InputError(description="Length of last name is not valid")    
    #Finding the user and changing their names
    for user in data['users']:
        if u_id == user['u_id']:
            user['name_first'] = name_first
            user['name_last'] = name_last
            #Writing data to export.json
            writeData(data) 
    return {
    }

@Authorisation
def user_profile_setemail_v2(token, email):
    """ 
    Given  valid token and email, changes a registered users email

    Arguments:
        token (string) - valid token associated with a registered user's session
        email (string) - email the user wants to update to


    Exceptions:
        InputError - Occurs if the email is not of valid formation
        InputError - Occurs if the email is already in use
        AccessError - Occurs if token is invalid


    Return value:
        {}
    """
    #Retrieving data from export.json
    data = getData()
    #Checking for an invalid token
    u_id = findUser(token)
    #Checking if the inputted email is valid
    if check_email(email) == False:
        raise InputError(description='Invalid email')
    #Checking if the email is already in use
    for user in data['users']:
        if email == user['email']:
            raise InputError(description='Email address is already in use')
    #Changing the given users email
    for user in data['users']:
        if u_id == user['u_id']:
            user['email'] = email
            #Writing data to export.json
            writeData(data) 
    return {
    }

@Authorisation
def user_profile_sethandle_v1(token, handle_str):
    """ 
    Given  valid token and handle, changes a registered users handle

    Arguments:
        token (string) - valid token associated with a registered user's session
        handle (string) - handle the user wants to update to


    Exceptions:
        InputError - Occurs if the handle is not between 3 and 20 characters, inclusive
        InputError - Occurs if the handle is already in use
        AccessError - Occurs if token is invalid


    Return value:
        {}
    """
    #Retrieving data from export.json
    data = getData()
    #Checking for an invalid token
    u_id = findUser(token)
    #Checking for @ and whitespace - as per the assumption in assumptions.md
    if handle_str.find('@') != -1:
        raise InputError(description="Handle cannot contain '@' symbol")
    elif handle_str.find(' ') != -1:
        raise InputError(description="Handle cannot contain whitespace")
    #Checking if the handle is of valid length
    elif len(handle_str) > 20 or len(handle_str) < 3:
        raise InputError(description="Length of handle is not valid")
    #Checking if the handle is in use
    for user in data['users']:
        if handle_str == user['handle_str']:
            raise InputError(description='Handle is already in use')
    #Changing the given users handle
    for user in data['users']:
        if u_id == user['u_id']:
            user['handle_str'] = handle_str
            #Writing data to export.json
            writeData(data) 
    return {
    }

@Authorisation
def users_all_v1(token):
    """ 
    Given  valid token, returns a list of all users and their associated details

    Arguments:
        token (string) - valid token associated with a registered user's session

    Exceptions:
        AccessError - Occurs if token is invalid


    Return value:
        { 'users' : [ user' : {'u_id' : u_id, 
                               'email' :email,
                               'name_first' : name_first,
                               'name_last' : name_last,
                               'handle_str' : handle_str,} 
                    ]
        }
    """
    #Retrieving data from export.json
    data = getData()
    #Checking for invalid token
    findUser(token)
    #Creating a user list
    user_list = []
    #Appending every user's info to the user_list
    for user in data['users']:
        info = {'u_id': user['u_id'],
                            'email': user['email'],
                            'name_first': user['name_first'],
                            'name_last': user['name_last'],
                            'handle_str': user['handle_str'],
                            'profile_img_url': user['profile_img_url']
                            }
        user_list.append(info)
    #Returning a dictionary with user_list
    return {'users': user_list,}


    
def user_stats(token):
    """ 
    Fetches the required statistics about this user's use of UNSW Dreams
    
    Arguments:
        token (string) - valid token associated with a registered user's session

  
    Return value:
        { users_stats }
    """
    #Retrieving data
    data = getData()
    #Finding a users id from their token
    u_id = findUser(token)
    #Retrieving total channel, dm and message counts for involvement rate calculation
    total_channel_count = data['dream_stats']['channels_exist'][-1]['num_channels_exist'] 
    total_dm_count = data['dream_stats']['dms_exist'][-1]['num_dms_exist'] 
    total_message_count = data['dream_stats']['messages_exist'][-1]['num_messages_exist'] 
    total_count = total_message_count + total_dm_count + total_channel_count
    
    #For the provided user, retrieve their personal message, channel and dm counts whilst also calculating their involvement rate
    for user in data['users']:
        if u_id == user['u_id']:
            message_count = user['user_stats']['messages_sent'][-1]['num_messages_sent']
            channel_count = user['user_stats']['channels_joined'][-1]['num_channels_joined']
            dm_count = user['user_stats']['dms_joined'][-1]['num_dms_joined']
            if total_count != 0:
                involve_rate = (message_count + dm_count + channel_count)/total_count
            else:
                involve_rate = 0
            user['user_stats']['involvement_rate'] = involve_rate
            stat_data = user['user_stats']

    return { 'user_stats' : stat_data }


def users_stats(token):
    """ 
    Fetches the required statistics about the use of UNSW Dreams
        
    Arguments:
        token (string) - valid token associated with a registered user's session

  
    Return value:
        { dreams_stats }
    """
    #Retreive data
    data = getData()
    #Retrieve and return dreams stats
    return { 'dreams_stats': data['dream_stats']}

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    """ 
    Given a URL of an image on the internet, crops the image within bounds (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
            
    Arguments:
        token (string) - valid token associated with a registered user's session
        img_url (string) - URl to a jpg online
        x_start (int) - indicates leftmost point on image
        y_start (int) - indicates topmost point on image
        x_end (int) - indicates righttmost point on image
        y_end (int) - indicates bottommost point on image
  
    Exceptions:
        InputError - img_url returns an HTTP status other than 200.
        InputError - any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
        InputError - Image uploaded is not a JPG

    Return value:
        { }
    """
    #Retrieving data from dictionary
    data = getData()
    #Find user id from their token
    u_id = findUser(token)
    #Define URL
    URL = f'{img_url}'
    #Define file path
    fileName = f'src/static/{u_id}.jpg'
    #Trying to open URL, if it fails raise an InputError
    try:
        status = requests.get(URL).status_code
    except:
        status = -1
    
    if status != 200:
        raise InputError(description='Invalid URL')
    #Raising an error if the URL does not point to a jpg
    if not URL.endswith('.jpg'):
        raise InputError(description = 'Image is not a jpg')
    #Retrieve the URL abd save the image as fileName
    urllib.request.urlretrieve(URL,fileName)
    #Open the image
    img = Image.open(fileName)
    #Define the size of the image
    width, height = img.size
    #Raising an error if the crop points aren't valid
    if x_start < 0 or y_start < 0 or x_end > width or y_end > height or x_end < x_start or y_end < y_start:
        raise InputError(description='Crop start or end points not valid')
    #Cropping and saving the image
    crop_img = img.crop((x_start, y_start, x_end, y_end))
    crop_img.save(fileName)
    #Changin the user's associated URL to the new image
    for user in data['users']:
        if u_id == user['u_id']:
            user['profile_img_url'] = f'{config.url}/images/{u_id}.jpg'
    #Writing data to dictionary
    writeData(data)     
    return {}

def append_user_stats(u_id, data):
    channel_count = channel_stats(data,u_id)[0]
    dm_count = dm_stats(data,u_id)[0]
    message_count= message_stats(data,u_id)[0]

    timestamp = int(time.time())  
    for users in data['users']:
        if u_id == users['u_id']:
            if len(users['user_stats']['messages_sent']) > 0:
                if users['user_stats']['messages_sent'][-1]['num_messages_sent'] > message_count:
                    message_count = users['user_stats']['messages_sent'][-1]['num_messages_sent'] 

            if users['user_stats']['channels_joined'][-1]['num_channels_joined'] !=  channel_count:
                users['user_stats']['channels_joined'].append({'num_channels_joined' : channel_count, 'time_stamp' : timestamp})
            if users['user_stats']['dms_joined'][-1]['num_dms_joined'] !=  dm_count:
                users['user_stats']['dms_joined'].append({'num_dms_joined' : dm_count, 'time_stamp' : timestamp})
            if users['user_stats']['messages_sent'][-1]['num_messages_sent'] !=  message_count:
                users['user_stats']['messages_sent'].append({'num_messages_sent': message_count, 'time_stamp': timestamp})

def append_dream_stats(u_id,data):
    [channel_count, total_channel_count] = channel_stats(data,u_id)
    [dm_count, total_dm_count] = dm_stats(data,u_id)
    total_message_count = message_stats(data,u_id)[1]
    involved_user_count = 0

    total_user_count = len(data['users'])
    
    for user in data['users']:
        u_id = user['u_id']
        [channel_count, total_channel_count] = channel_stats(data,u_id)
        [dm_count, total_dm_count] = dm_stats(data,u_id)
        total_message_count = message_stats(data,u_id)[1]
        if channel_count > 0 or dm_count > 0:
            involved_user_count += 1
          
    util_rate = involved_user_count/total_user_count
        
    timestamp = int(time.time())
    
    if data['dream_stats']['channels_exist'][-1]['num_channels_exist'] !=  total_channel_count:
        data['dream_stats']['channels_exist'].append({'num_channels_exist' : total_channel_count, 'time_stamp' : timestamp})
    if data['dream_stats']['dms_exist'][-1]['num_dms_exist'] !=  total_dm_count:
        data['dream_stats']['dms_exist'].append({'num_dms_exist' : total_dm_count, 'time_stamp' : timestamp})
    if data['dream_stats']['messages_exist'][-1]['num_messages_exist'] !=  total_message_count:
        data['dream_stats']['messages_exist'].append({'num_messages_exist': total_message_count, 'time_stamp': timestamp})
    data['dream_stats']['utilization_rate'] = util_rate



def channel_stats(data,u_id):
    channel_count = 0
    total_channel_count = 0
    for channels in data['channels']:
        # Checks if the user is a member in the channel
        for users in channels['all_members']:
            if u_id == users['u_id']:
                channel_count += 1
        total_channel_count += 1
    return [channel_count, total_channel_count]

def dm_stats(data,u_id):
    dm_count = 0
    total_dm_count = 0
    for dm in data['dms']:
        for dm_u_id in dm['dm_members']:
            if u_id == dm_u_id and dm['dm_id'] != -1:
                dm_count += 1  
        if dm['dm_id'] != -1:
            total_dm_count += 1
    return [dm_count, total_dm_count]

def message_stats(data,u_id):
    message_count = 0
    total_message_count = 0
    for messages in data['messages']:
        if u_id == messages['u_id']:
            message_count += 1
        total_message_count += 1
    return [message_count, total_message_count]
