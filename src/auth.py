import re
regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
secret = 'COMP1531Dorito2021'
import hashlib
from json import dumps,loads
from src.error import InputError, AccessError
from src import config
import jwt
import smtplib
import random
import time

#def auth_login_v1(email, password):
#    """ 
#    Given an email and a password, log a user into the system.
#
#    Arguments:
#        email (string) - email inputted by user
#        password (string) - password inputted by user
#
#    Exceptions:
#        InputError - Occurs when an invalid email is entered, a valid but unregistered email is entered or when an
#                    incorrect password is entered.  
#
#
#    Return value:
#        {'auth_user_id' : u_id}
#    """
#    #Setting the default status that the email does not match any in the dictionary
#    email_status = False
#    #checking if it is a valid email
#    if check_email(email) == False:
#        raise InputError(description="Email is not valid") #Error
#    #searching users in the data.data_dic dictionary     
#    for user in data.data_dic .get('users'):
#        #checking if the provided email matches an existing user's email
#        if email == user.get('email'):
#            #if the email is found changing email_status and getting the users id
#            email_status = True
#            user_id = user.get('u_id')
#            #checking if the password matches the account's password
#            if password == user.get('user_password'):                    
#                return {'auth_user_id':user_id}
#            else:
#                raise InputError(description="Password incorrect") #Error
#    #raising an error if the email could not be found        
#    if email_status == False:
#        raise InputError(description="Cannot find email") #Error
#
#
#def auth_register_v1(email, password, name_first, name_last):
#    """ 
#    Given user-inputted information, register a user provided the input is valid.
#
#    Arguments:
#        email (string) - email inputted by user
#        password (string) - password inputted by user
#        name_first (string) - first name inputted by user
#        name_last (string) - last name inputted by user
#
#    Exceptions:
#        InputError - Occurs when an invalid email is entered, the email provided is already in use by another
#        registered user, the password is less than 6 characters long or if the first/last name is less than 1 or
#        greater than 50 characters in length.
#
#    Return value:
#        {'auth_user_id' : u_id}
#    """
#    #creating an initial handle with the users first and last names
#    handle = name_first + name_last
#    #checking variety of error conditions
#    if check_email(email) == False:
#        raise InputError(description="Email is not valid")
#    elif len(password) < 6:
#        raise InputError(description="Error password too short")
#    elif len(name_first) > 50 or len(name_first) < 1:
#        raise InputError(description="Length of first name is not valid")
#    elif len(name_last) > 50 or len(name_last) < 1:
#        raise InputError(description="Length of last name is not valid")
#    #limiting handle to maximum 20 characters
#    if len(handle) > 20:
#        handle = handle[0:20]
#    
#    #making the handle fully lowercase    
#    handle = handle.lower()
#    #defining variables    
#    pad_counter = 0    
#    initial_length = len(handle)
#    prev_id = 0
#    permission_status = 2
#    #searching through users in data.data_dic  dictionary
#    for user in data.data_dic .get('users'):
#        #checking if the users email is already in use
#        if email == user.get('email'):
#            raise InputError(description="email already in use") #Error
#        #checking if the users handle already exists
#        if user.get('handle_str') == handle:
#            #if the handle already exists, adding an integer to the end of the handle
#            #to differentiate it
#            trailingint = 0 + pad_counter
#            pad_counter += 1
#            if pad_counter == 0:            
#                handle += str(trailingint) 
#            elif len(handle) == 20:
#                handle = handle[0:(20-len(str(trailingint)))]
#                handle += str(trailingint)
#            else:
#                handle = handle[0:initial_length]
#                handle += str(trailingint) 
#        #finding the last user id in the data.data_dic  dictionary
#        prev_id = user.get('u_id')
#    #If this is the first user entered, granting them 'owner' status
#    if len(data.data_dic ['users']) == 0:
#        permission_status = 1
#        prev_id = 0
#    #assigning the user a new, unique id
#    new_id = prev_id + 1
#    #adding the new user to the dictionary provided no errors have been raised    
#    data.data_dic .get('users').append(
#    {
#            'u_id':new_id,
#            'name_first': name_first,
#            'name_last':name_last,
#            'email':email,
#            'handle_str':handle,
#            'user_password':password,
#            'permission_id':permission_status,
#            'token':'',
#    })
#    return {'auth_user_id':new_id}

def findUser(token):
    #Retrieving data
    data = getData()
    #Checking if token is valid and if so, who is the user associated with the token
    for user in data['users']:
        for validtoken in user['token_list']:
            if token == validtoken:
                return user['u_id']
    raise AccessError(description = "Invalid access token")

def getData():
    #Retrieving data from export.json
    with open('src/export.json', 'r') as file: 
        data = loads(file.read())   
    return data

def writeData(data):
    #Writing data to export.json
    with open('src/export.json', 'w') as file:
        file.write(dumps(data))    
    
def hashstr(string):
    return hashlib.sha256(string.encode()).hexdigest()

def createtoken(payload):
    return jwt.encode(payload, secret, algorithm='HS256')

def getSessionId():
    #Incrementing session_id
    data = getData()
    session_id = data['session_id']
    return session_id + 1
        
def check_email(email):
    #Checking if the email is of valid format
    if(re.search(regex,email)):
        return True
    else:
        return False

def auth_register_v2(email, password, name_first, name_last):
    """Given user-inputted information, register a user provided the input is valid.

    Arguments:
        email (string) - email inputted by user
        password (string) - password inputted by user
        name_first (string) - first name inputted by user
        name_last (string) - last name inputted by user

    Exceptions:
        InputError - Occurs when an invalid email is entered, the email provided is already in use by another
        registered user, the password is less than 6 characters long or if the first/last name is less than 1 or
        greater than 50 characters in length.

    Return value:
        {'token': token,
        'auth_user_id' : u_id}
    """
    #Retrieving data from export.json
    data = getData()

    #Incrementing session_id
    session_id = getSessionId()
    data['session_id'] = session_id
    #Creating the users handle - removing @ and whitespace
    handle = name_first + name_last
    handle = handle.replace('@','')
    handle = handle.replace(' ','')
    #checking variety of error conditions
    if check_email(email) == False:
        raise InputError(description="Email is not valid")
    elif len(password) < 6:
        raise InputError(description="Error password too short")
    elif len(name_first) > 50 or len(name_first) < 1:
        raise InputError(description="Length of first name is not valid")
    elif len(name_last) > 50 or len(name_last) < 1:
        raise InputError(description="Length of last name is not valid")
    #limiting handle to maximum 20 characters
    if len(handle) > 20:
        handle = handle[0:20]

    timestamp = int(time.time())  
    
    handle = handle.lower()
    pad_counter = 0    
    initial_length = len(handle)
    prev_valid_id = 0
    prev_removed_id = 0
    prev_id = 0
    permission_status = 2
    #searching through users in data.data_dic  dictionary
    for user in data['users']:
        #checking if the users email is already in use
        if email == user.get('email'):
            raise InputError(description="email already in use") #Error
        #checking if the users handle already exists
        if user.get('handle_str') == handle:
            #if the handle already exists, adding an integer to the end of the handle
            #to differentiate it
            trailingint = 0 + pad_counter
            pad_counter += 1
            if len(handle) == 20:
                handle = handle[0:(20-len(str(trailingint)))]
                handle += str(trailingint)
            else:
                handle = handle[0:initial_length]
                handle += str(trailingint) 
        #finding the last user id in the data.data_dic  dictionary
        prev_valid_id = user.get('u_id')
        
    for user in data['removed_users']:
        prev_removed_id = user.get('u_id')
    #If this is the first user entered, granting them 'owner' status
    if len(data['users']) == 0:
        permission_status = 1
        prev_id = 0
        
    if prev_valid_id >= prev_removed_id:
        prev_id = prev_valid_id
    else:
        prev_id = prev_removed_id
    #assigning the user a new, unique id
    new_id = prev_id + 1
    #Creating a token with the secret and session_id
    payload = {'session' : session_id}
    token = createtoken(payload)
    #Adding the user to users
    data['users'].append({
            'u_id' : new_id,
            'email' : email,#uinfo['email'],
            'user_password': hashstr(password),#hashstr(uinfo['password']),
            'name_first': name_first,#uinfo['name_first'],
            'name_last': name_last,#uinfo['name_last'],
            'token_list': [token],
            'handle_str' : handle,
            'session_list' : [session_id],
            'permission_id' : permission_status,
            'reset_code' : None,
            'profile_img_url' : f'{config.url}/images/default.jpg',
            'user_stats' : {'channels_joined': [{'num_channels_joined': 0, 'time_stamp': timestamp}],
                          'dms_joined': [{'num_dms_joined': 0, 'time_stamp': timestamp}], 
                          'messages_sent': [{'num_messages_sent': 0, 'time_stamp': timestamp}], 
                          'involvement_rate' : 0,
                          }
            })
    total_users = len(data['users'])        
    involved_users = data['dream_stats']['utilization_rate']*(total_users-1)                
    data['dream_stats']['utilization_rate'] = involved_users/total_users
    #Writing data to export.json
    writeData(data)
    #Returning token and auth_user_id
    return {'token': token,
            'auth_user_id' : new_id,
            }

def auth_login_v2(email, password):
    """ 
    Given an email and a password, log a user into the system.

    Arguments:
        email (string) - email inputted by user
        password (string) - password inputted by user

    Exceptions:
        InputError - Occurs when an invalid email is entered, a valid but unregistered email is entered or when an
                    incorrect password is entered.  


    Return value:
        {'token': token,
        'auth_user_id' : u_id}
    """
    #Retrieving data from expor.json
    data = getData()
    session_id = getSessionId()
    data['session_id'] = session_id
    #Setting the default status that the email does not match any in the dictionary
    email_status = False
    #checking if it is a valid email
    if check_email(email) == False:
        raise InputError(description="Email is not valid") #Error
    #searching users in the data.data_dic dictionary     
    for user in data.get('users'):
        #checking if the provided email matches an existing user's email
        if email == user.get('email'):
            #if the email is found changing email_status and getting the users id
            email_status = True
            user_id = user.get('u_id')
            #checking if the password matches the account's password
            if hashstr(password) == user.get('user_password'):   
                #Creating a token for this session and appending the token and session to the user's info
                payload = {'session' : session_id}
                token = createtoken(payload)
                user['session_list'].append(session_id)
                user['token_list'].append(token)
                #Writing data to export.json
                writeData(data)
                #Returning token and auth_user_id
                return {'token': token,
                        'auth_user_id': user_id,
                        }
            else:
                raise InputError(description="Password incorrect") #Error
    #raising an error if the email could not be found        
    if email_status == False:
        raise InputError(description="Cannot find email") #Error

def auth_logout_v1(token):
    """ 
    Given a valid token, log a user out of the system.

    Arguments:
        token (string) - valid token indicating a user is currently logged into the system

    Return value:
        {'is_success' : True/False}
    """
    #Retrieving data from export.json
    data = getData()
    #Checking token validity
    findUser(token)
    #Finding the user in the data dictionary
    for user in data['users']:
        tokenCounter = 0
        for valid_token in user['token_list']:
            #Once the user is found, removing the token and session from the dictionary
            if token == valid_token:
                user['token_list'].remove(token)
                user['session_list'].remove(user['session_list'][tokenCounter])
                #Writing data to export.json
                writeData(data)
                #Returning a success statement
                return {'is_success' :True,}
            #Incrementing token counter
            tokenCounter += 1

def auth_password_reset_request(email):
    """ 
    Given a valid email, request a password reset for the associated user - sending a code to the email.

    Arguments:
        email (string) - valid email associated with a current user

    Return value:
        {}
    """
    #Retrieving data from export.json
    data = getData()
    #Assuming the email is invalid initially
    email_status = False
    #Searching through users in the dictionary
    for user in data.get('users'):
        #checking if the provided email matches an existing user's email
        if email == user.get('email'):
            #Changing email_status to show email is valid
            email_status = True
            
            #Sending an email to the provided email, containing a reset code
            from_user = 'wed13bdorito@gmail.com'
            from_password = 'Garythegoat1'
            
            #Generating a random 4 digit reset code
            reset_code = random.randint(1000,9999)
            #Storing reset code as a hash to make it more secure
            user['reset_code'] = hashstr(str(reset_code))
            
            to = [f"{email}"]
            subject = 'Password Reset'
            body = f"Hi,\n Your password reset code is {reset_code}"
   
            header  = 'From: %s\n' % from_user
            header += 'To: %s\n' % ','.join(to)
            header += 'Subject: %s\n\n' % subject
            message = header + body
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(from_user, from_password)
            server.sendmail(from_user, to, message)
            server.close()

    #Writing data to dictionary
    writeData(data)
    #Raising an input error if the email is invalid
    if email_status == False:
        raise InputError(description="Invalid email")
    
    return {}

def auth_password_reset(reset_code, new_password):
    """ 
    Given a valid reset code and a new password, changes a users password through the reset code.

    Arguments:
        reset_code (int) - a number emailed to the user allowing them to change their passowrd
        new_password (string) - user's new desired password

    Exceptions:
        InputError - Occurs when reset_code is not a valid reset code
        InputError - Occurs when password entered is less than 6 characters long  
  
    Return value:
        {}
    """
    #Retrieving data from server
    data = getData()
    #Assuming provided code is invalid
    valid_code = False
    none_counter = 0
    #Raising an error if the password is too short
    if len(new_password) < 6:
        raise InputError(description="Password too short")
    #Looping through users in the dictionary, checking if the reset code matches any users
    for user in data.get('users'):
        if user['reset_code'] == None:
            none_counter += 1
        if hashstr(str(reset_code)) == user['reset_code']:
            valid_code = True
            user['reset_code'] = None
            user['user_password'] = hashstr(new_password)
    #Raising an accesserror if no password reset has been requested
    if none_counter == len(data['users']):
        raise AccessError(description="No password reset requested")
    #Raising an error if the code is invalid
    if valid_code == False:
        raise InputError(description="Invalid reset_code")
    #Writing data to the dictionary
    writeData(data)
    return {}