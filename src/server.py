import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src import config
from src.error import InputError
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1, auth_password_reset_request, auth_password_reset, findUser
from src.channel import channel_join_v2, channel_leave_v1, channel_addowner_v1, channel_removeowner_v1, channel_messages_v2, channel_details_v2, channel_invite_v2
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.dms import dm_messages_v1, dm_create_v1, dm_invite_v1, dm_remove_v1, dm_details_v1, dm_list_v1, dm_leave_v1
from src.user import users_all_v1, user_profile_setemail_v2, user_profile_sethandle_v1, user_profile_setname_v2, user_profile_v2, user_profile_uploadphoto_v1, user_stats, users_stats
from src.message import message_send_v2, message_edit_v2, message_remove_v1, message_share_v1, message_senddm_v1, message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1
from src.other import clear_v1, search_v2
from src.admin import admin_userpermission_change_v1, admin_user_remove_v1
from src.notifications import notifications_get_v1
from src.standups import standup_active_v1, standup_send_v1, standup_start_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path = '/images/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


################################################################################
##################             ITERATION 2 ROUTES                ###############
################################################################################
@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    return dumps(clear_v1())

################################################################################
##################               AUTH ROUTES                 ###################
################################################################################
@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    data = request.get_json()
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    email = data['email']

    output = auth_register_v2(email, password, name_first, name_last)

    return dumps(output)

@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    data = request.get_json()
    password = data['password']
    email = data['email']

    output = auth_login_v2(email, password)

    return dumps(output)

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    data = request.get_json()
    token = data['token']

    output = auth_logout_v1(token)

    return dumps(output)


@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def auth_request():
    data = request.get_json()
    email = data['email']

    output = auth_password_reset_request(email)

    return dumps(output)

@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def auth_reset():
    data = request.get_json()
    new_password = data['new_password']
    reset_code = data['reset_code']
    output = auth_password_reset(reset_code, new_password)

    return dumps(output)

################################################################################
##################             CHANNEL ROUTES               ####################
################################################################################
@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    
    return dumps(channel_details_v2(token, channel_id))

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    
    return dumps(channel_invite_v2(token, channel_id, u_id))

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    token = data["token"]
    channel_id = data["channel_id"]
    return dumps(channel_join_v2(token, channel_id))

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    data = request.get_json()
    token = data["token"]
    channel_id = data["channel_id"]
    return dumps(channel_leave_v1(token, channel_id))

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    data = request.get_json()
    token = data["token"]
    channel_id = data["channel_id"]
    u_id = data["u_id"]
    return dumps(channel_addowner_v1(token, channel_id, u_id))

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    data = request.get_json()
    token = data["token"]
    channel_id = data["channel_id"]
    u_id = data["u_id"]
    return dumps(channel_removeowner_v1(token, channel_id, u_id))

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))
    start = int(request.args.get("start"))
    return dumps(channel_messages_v2(token, channel_id, start))

################################################################################
##################              CHANNELS ROUTES                #################
################################################################################
@APP.route("/channels/list/v2", methods=['GET'])
def channels_list():
    token = request.args.get('token')  
    
    output = channels_list_v2(token)

    return dumps(output)

@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    token = request.args.get('token') 
    
    output = channels_listall_v2(token)

    return dumps(output)

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    data = request.get_json()
    token = data['token']    
    name = data['name']
    is_public = data['is_public']
    
    output = channels_create_v2(token, name, is_public)

    return dumps(output)

################################################################################
##################               USER ROUTES                 ###################
################################################################################
@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    token = request.args.get('token')
    output = users_all_v1(token)
    
    return dumps(output)   

@APP.route("/user/profile/v2", methods=['GET'])
def users_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    
    output = user_profile_v2(token, int(u_id))
    
    return dumps(output)  

@APP.route("/user/profile/setname/v2", methods=['PUT'])
def users_setname():
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    output = user_profile_setname_v2(token, name_first, name_last)
    
    return dumps(output)  

@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def users_setemail():
    data = request.get_json()
    token = data['token']
    email = data['email']

    output = user_profile_setemail_v2(token,email)
    
    return dumps(output)

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def users_sethandle():
    data = request.get_json()
    token = data['token']
    handle_str = data['handle_str']

    output = user_profile_sethandle_v1(token,handle_str)
    
    return dumps(output)

@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_uploadphoto():
    data = request.get_json()
    token = data['token']
    img_url = data['img_url']
    print(data)
    x_start = int(data['x_start'])
    y_start = int(data['y_start'])
    x_end = int(data['x_end'])
    y_end = int(data['y_end'])
    output = user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end)
    
    return dumps(output)

@APP.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('', path)

@APP.route("/user/stats/v1", methods=['GET'])
def user_individual_stats():
    token = request.args.get('token')


    output = user_stats(token)
    
    return dumps(output)

@APP.route("/users/stats/v1", methods=['GET'])
def user_dream_stats():
    token = request.args.get('token')

    output = users_stats(token)
    
    return dumps(output)
################################################################################
##################               DM ROUTES                ######################
################################################################################
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create_v1_http():
    data = request.get_json()
    token = str(data.get('token'))
    u_ids = data.get('u_ids')

    return_val = dm_create_v1(token, u_ids)
    
    return dumps(return_val)

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details_v1_http():
    data = request.args
    token = str(data['token'])#the pass in value
    dm_id = int(data['dm_id'])#the pass in value

    return_val = dm_details_v1(token, dm_id)# get the return value, which is not dumped

    return dumps(return_val)


@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove_v1_http():
    data = request.get_json()
    token = str(data['token'])
    dm_id = int(data['dm_id'])

    return_val = dm_remove_v1(token, dm_id)

    return dumps(return_val)



@APP.route("/dm/invite/v1", methods=['POST'])
def dm_invite_v1_http():
    data = request.get_json()
    token = str(data['token'])
    dm_id = int(data['dm_id'])
    u_id = int(data['u_id'])

    return_val = dm_invite_v1(token, dm_id, u_id)

    return dumps(return_val)

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list_v1_http():
    token = request.args.get('token')

    return_val = dm_list_v1(token)

    return dumps(return_val)

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave_v1_http():
    data = request.get_json()
    token = str(data['token'])
    dm_id = int(data['dm_id'])

    return_val = dm_leave_v1(token, dm_id)

    return dumps(return_val)

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages_v1_http():
    data = request.args
    token = str(data['token'])
    dm_id = int(data['dm_id'])
    start = int(data['start'])

    return_val = dm_messages_v1(token, dm_id, start)

    return dumps(return_val)

################################################################################
##################              MESSAGE ROUTES                ##################
################################################################################
@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']

    output = message_send_v2(token, channel_id, message)

    return dumps(output)

@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    data = request.get_json()
    token = data["token"]
    channel_id = data["channel_id"]
    message = data["message"]
    time_sent = data["time_sent"]
    return dumps(message_sendlater_v1(token, channel_id, message, time_sent))

@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    message = data['message']

    output = message_edit_v2(token, message_id, message)

    return dumps(output)
 
@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']

    output = message_remove_v1(token, message_id)

    return dumps(output)    

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    data = request.get_json()
    token = data['token']
    og_message_id = data['og_message_id']    
    message = data['message']
    channel_id = data['channel_id']
    dm_id = data['dm_id']
    
    output = message_share_v1(token, og_message_id, message, channel_id, dm_id)

    return dumps(output)

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    data = request.get_json()
    token = data['token']    
    dm_id = data['dm_id']
    message = data['message']
    
    output = message_senddm_v1(token, dm_id, message)

    return dumps(output)

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    data = request.get_json()
    token = data["token"]
    dm_id = data["dm_id"]
    message = data["message"]
    time_sent = data["time_sent"]
    return dumps(message_sendlaterdm_v1(token, dm_id, message, time_sent))

@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']
    
    output= message_react_v1(token, message_id, react_id)
    
    return dumps(output)

@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']
    
    output= message_unreact_v1(token, message_id, react_id)
    
    return dumps(output)

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    
    output= message_pin_v1(token, message_id)
    
    return dumps(output)

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    
    output= message_unpin_v1(token, message_id)
    
    return dumps(output)

################################################################################
##################              SEARCH ROUTES                ###################
################################################################################
@APP.route("/search/v2", methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    
    return dumps(search_v2(token, query_str))

################################################################################
##################              ADMIN ROUTES                ####################
################################################################################
@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change():
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    permission_id = data['permission_id']

    return dumps(admin_userpermission_change_v1(token, u_id, permission_id))

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    
    return dumps(admin_user_remove_v1(token, u_id))

################################################################################
##################             NOTIFICATION ROUTE               ################
################################################################################
@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get():
    token = request.args.get('token')
    return dumps(notifications_get_v1(token))


################################################################################
##################             STANDUP ROUTE                    ################
################################################################################
@APP.route("/standup/start/v1", methods=['POST'])
def standup_start_v1_http():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    length = data['length']
    rt_val = standup_start_v1(token, channel_id, length)
    return dumps(rt_val)

@APP.route("/standup/active/v1", methods=['GET'])
def standup_active_v1_http():
    data = request.args
    token = str(data['token'])
    channel_id = int(data['channel_id'])
    return dumps(standup_active_v1(token, channel_id))

@APP.route("/standup/send/v1", methods=['POST'])
def standup_send_v1_http():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    return dumps(standup_send_v1(token, channel_id, message))

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port


