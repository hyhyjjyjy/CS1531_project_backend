from src.error import AccessError
from json import loads

def Authorisation(func):

    def wrapper(*args):
        #Retrieving data
        data = getData()
        check = False
        token = args[0]
        #Checking if token is valid and if so, who is the user associated with the token
        for user in data['users']:
            for validtoken in user['token_list']:
                if token == validtoken:
                    check = True

        if check == False:
            raise AccessError(description = "Invalid access token")
        
        return func(*args)

    return wrapper

def getData():
    with open('src/export.json', 'r') as file: 
        data = loads(file.read())   
    return data