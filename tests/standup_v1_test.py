from src.auth import auth_register_v2
from src.channel import channel_details_v2, channel_join_v2, channel_invite_v2, channel_messages_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.message import message_send_v2
from src.standups import standup_active_v1, standup_send_v1, standup_start_v1
from src.error import InputError, AccessError
from src.notifications import notifications_get_v1
import pytest
import time
import datetime


#create the data of users and channels 
@pytest.fixture()
def create_valid_user_data():
    """ Creates and returns a set of valid users.
    """
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'a', 'b')
    user2 = auth_register_v2('secondemail@gmail.com', '123abc!@#', 'c', 'd')
    user3 = auth_register_v2('thirdemail@gmail.com', '123abc!@#', 'e', 'f')
    user4 = auth_register_v2('fourthemail@gmail.com', '123abc!@#', 'g', 'h')
    users = [user1, user2, user3, user4]

    # Create 3 channels with owners user1, user2 & user3 respectively
    channel_1 = channels_create_v2(user1['token'], "General", True)
    channel_2 = channels_create_v2(user2['token'], "Music", True)
    channel_3 = channels_create_v2(user3['token'], "Study", True)

    # User2, user3 all join channel1
    channel_join_v2(user2['token'], channel_1['channel_id'])
    channel_join_v2(user3['token'], channel_1['channel_id'])

    # User4 join channel2
    channel_join_v2(user4['token'], channel_2['channel_id'])

    # User1 join channel3
    channel_join_v2(user1['token'], channel_3['channel_id'])

    channels = [channel_1, channel_2, channel_3]

    return {'users': users , 'channels': channels}


#test the function standup_start_v1's errors
def test_standup_start_error(create_valid_user_data):
    users = create_valid_user_data['users']
    channels = create_valid_user_data['channels']
    time_sleep = 2


    #channel ids are not valids
    with pytest.raises(InputError):
        standup_start_v1(users[0]['token'], 999, time_sleep)
    with pytest.raises(InputError):
        standup_start_v1(users[1]['token'], 111, time_sleep)
    with pytest.raises(InputError):
        standup_start_v1(users[0]['token'], 543, time_sleep)

    standup_start_v1(users[0]['token'], channels[0]['channel_id'], time_sleep)

    #a standup has been started
    with pytest.raises(InputError):
        standup_start_v1(users[0]['token'], channels[0]['channel_id'], time_sleep)
    with pytest.raises(InputError):
        standup_start_v1(users[1]['token'], channels[0]['channel_id'], time_sleep)
    with pytest.raises(InputError):
        standup_start_v1(users[2]['token'], channels[0]['channel_id'], time_sleep)
    time.sleep(time_sleep + 1)

    standup_start_v1(users[1]['token'], channels[1]['channel_id'], time_sleep)
    #a standup has been started
    with pytest.raises(InputError):
        standup_start_v1(users[1]['token'], channels[1]['channel_id'], time_sleep)
    with pytest.raises(InputError):
        standup_start_v1(users[3]['token'], channels[1]['channel_id'], time_sleep)
    time.sleep(time_sleep + 1)
    
    #user not in the channel
    with pytest.raises(AccessError):
        standup_start_v1(users[0]['token'], channels[1]['channel_id'], time_sleep)
    with pytest.raises(AccessError):
        standup_start_v1(users[2]['token'], channels[1]['channel_id'], time_sleep)
    with pytest.raises(AccessError):
        standup_start_v1(users[1]['token'], channels[2]['channel_id'], time_sleep)

    clear_v1()

#test the function standup_active_v1's error
def test_standup_active_error(create_valid_user_data):
    users = create_valid_user_data['users']
    #channels = create_valid_user_data['channels']

    #invalid channel id
    with pytest.raises(InputError):
        standup_active_v1(users[0]['token'], 999)
    with pytest.raises(InputError):
        standup_active_v1(users[1]['token'], 999)
    with pytest.raises(InputError):
        standup_active_v1(users[2]['token'], 999)
    with pytest.raises(InputError):
        standup_active_v1(users[3]['token'], 999)
    clear_v1()

#test the function standup_send_v1's error
def test_standup_send_error(create_valid_user_data):
    users = create_valid_user_data['users']
    channels = create_valid_user_data['channels']
    time_sleep = 2

    #channel ids are not valids
    with pytest.raises(InputError):
        standup_send_v1(users[0]['token'], 999, "aaa")
    with pytest.raises(InputError):
        standup_send_v1(users[1]['token'], 111, "bbb")
    with pytest.raises(InputError):
        standup_send_v1(users[0]['token'], 543, "ccc")

    very_long_message_1 = ""
    very_long_message_2 = ""
    very_long_message_3 = ""
    for i in range(1001):
        very_long_message_1 += "a"
    for i in range(2000):
        very_long_message_2 += "b"
    for i in range(3000):
        very_long_message_3 += "c"
    i = i
    #messages are too long
    with pytest.raises(InputError):
        standup_send_v1(users[0]['token'], channels[0]['channel_id'], very_long_message_1)
    with pytest.raises(InputError):
        standup_send_v1(users[1]['token'], channels[1]['channel_id'], very_long_message_2)
    with pytest.raises(InputError):
        standup_send_v1(users[2]['token'], channels[2]['channel_id'], very_long_message_3)

    #a standup is not running in the channel
    with pytest.raises(InputError):
        standup_send_v1(users[0]['token'], channels[0]['channel_id'], "aaa")
    with pytest.raises(InputError):
        standup_send_v1(users[1]['token'], channels[1]['channel_id'], "aaa")
    with pytest.raises(InputError):
        standup_send_v1(users[2]['token'], channels[2]['channel_id'], "aaa")


    standup_start_v1(users[0]['token'], channels[0]['channel_id'], time_sleep)
    standup_start_v1(users[1]['token'], channels[1]['channel_id'], time_sleep)
    standup_start_v1(users[2]['token'], channels[2]['channel_id'], time_sleep)

    #user not in the channel
    with pytest.raises(AccessError):
        standup_send_v1(users[0]['token'], channels[1]['channel_id'], "aaa")
    with pytest.raises(AccessError):
        standup_send_v1(users[2]['token'], channels[1]['channel_id'], "aaa")
    with pytest.raises(AccessError):
        standup_send_v1(users[1]['token'], channels[2]['channel_id'], "aaa")

    time.sleep(time_sleep + 1)
    clear_v1()


#test the correct standup behavior with short messages
def test_correct_standup_short_message(create_valid_user_data):

    users = create_valid_user_data['users']
    channels = create_valid_user_data['channels']
    time_sleep = 2

    #generate some pre-exist messages in the channel
    for i in range(10):
        message_send_v2(users[0]['token'], channels[0]['channel_id'], f"First channel message {i}.")
    
    ###################channel 1 strandup start######################
    rt_val = standup_start_v1(users[0]['token'], channels[0]['channel_id'], time_sleep)
    
    #calculate the time when the function should finish
    time_finish = (datetime.datetime.now()+datetime.timedelta(seconds=time_sleep)).strftime("%Y-%m-%d %H:%M:%S")
    time_finish = time.strptime(time_finish, "%Y-%m-%d %H:%M:%S")
    time_finish = time.mktime(time_finish)


    #send some messages to the standup
    standup_send_v1(users[0]['token'], channels[0]['channel_id'], "aaa")
    standup_send_v1(users[0]['token'], channels[0]['channel_id'], "aaa")
    standup_send_v1(users[0]['token'], channels[0]['channel_id'], "aaa")
    standup_send_v1(users[0]['token'], channels[0]['channel_id'], "aaa")
    standup_send_v1(users[1]['token'], channels[0]['channel_id'], "bbb")
    standup_send_v1(users[2]['token'], channels[0]['channel_id'], "ccc")

    #check the channel messages list so that the standup message has not been updated
    msgs = channel_messages_v2(users[0]['token'], channels[0]['channel_id'], 0)
    for i in range(10):
        assert msgs['messages'][9 - i]['message'] == f"First channel message {i}."

    time.sleep(time_sleep + 1)
    
    #####################channel 1 standup finishes##########################

    #check the channel messages list so that the standup message has been updated
    assert rt_val['time_finish'] == time_finish
    msgs = channel_messages_v2(users[0]['token'], channels[0]['channel_id'], 0)
    for i in range(10):
        assert msgs['messages'][10 - i]['message'] == f"First channel message {i}."
    #the most recent message is standup
    assert msgs['messages'][0]['message'] ==  "ab: aaa\nab: aaa\nab: aaa\nab: aaa\ncd: bbb\nef: ccc"


#test the correct standup behavior with very long messages
def test_correct_standup_long_message(create_valid_user_data):
    
    users = create_valid_user_data['users']
    channels = create_valid_user_data['channels']
    time_sleep = 6

    very_long_message_1 = ""
    very_long_message_2 = ""
    very_long_message_3 = ""
    for i in range(500):
        very_long_message_1 += "a"
    for i in range(500):
        very_long_message_2 += "b"
    for i in range(500):
        very_long_message_3 += "c"

    #generate some pre-exist messages in the channel
    for i in range(10):
        message_send_v2(users[0]['token'], channels[0]['channel_id'], f"{very_long_message_1}{i}.")
    
    ###################channel 1 standup start######################
    rt_val = standup_start_v1(users[0]['token'], channels[0]['channel_id'], time_sleep)
    
    #calculate the time when the function should finish
    time_finish = (datetime.datetime.now()+datetime.timedelta(seconds=time_sleep)).strftime("%Y-%m-%d %H:%M:%S")
    time_finish = time.strptime(time_finish, "%Y-%m-%d %H:%M:%S")
    time_finish = time.mktime(time_finish)

    #send some messages to the standup
    long_buffered_message = ""
    for i in range(100):
        standup_send_v1(users[0]['token'], channels[0]['channel_id'], very_long_message_1)
        standup_send_v1(users[1]['token'], channels[0]['channel_id'], very_long_message_2)
        standup_send_v1(users[2]['token'], channels[0]['channel_id'], very_long_message_3)
        long_buffered_message += f"ab: {very_long_message_1}\n"
        long_buffered_message += f"cd: {very_long_message_2}\n"
        long_buffered_message += f"ef: {very_long_message_3}\n"
    long_buffered_message = long_buffered_message[0:-1]#get rig of the \n at the end

    #check the channel messages list so that the standup message has not been updated
    msgs = channel_messages_v2(users[0]['token'], channels[0]['channel_id'], 0)
    for i in range(10):
        assert msgs['messages'][9 - i]['message'] == f"{very_long_message_1}{i}."

    time.sleep(time_sleep + 1)
    
    #####################channel 1 standup finishes##########################
    
    #check the channel messages list so that the standup message has been updated
    assert rt_val['time_finish'] == time_finish
    msgs = channel_messages_v2(users[0]['token'], channels[0]['channel_id'], 0)
    for i in range(10):
        assert msgs['messages'][10 - i]['message'] == f"{very_long_message_1}{i}."
    #the most recent message is standup message
    assert msgs['messages'][0]['message'] ==  long_buffered_message

    clear_v1()


def test_correct_standup_active(create_valid_user_data):
    
    users = create_valid_user_data['users']
    channels = create_valid_user_data['channels']
    time_sleep = 3


    for i in range(10):
        message_send_v2(users[0]['token'], channels[0]['channel_id'], f"First channel message {i}.")
    
    ###################channel 1 standup start######################
    standup_start_v1(users[0]['token'], channels[0]['channel_id'], time_sleep)
    
    #calculate the time when the function should finish
    time_finish = (datetime.datetime.now()+datetime.timedelta(seconds=time_sleep)).strftime("%Y-%m-%d %H:%M:%S")
    time_finish = time.strptime(time_finish, "%Y-%m-%d %H:%M:%S")
    time_finish = time.mktime(time_finish)

    assert standup_active_v1(users[0]['token'], channels[0]['channel_id'])['is_active'] == True
    assert standup_active_v1(users[0]['token'], channels[0]['channel_id'])['time_finish'] == time_finish
    
    time.sleep(time_sleep + 1)
    ###################channel 1 standup finishes######################
    assert standup_active_v1(users[0]['token'], channels[0]['channel_id'])['is_active'] == False
    assert standup_active_v1(users[0]['token'], channels[0]['channel_id'])['time_finish'] == None
   


    ###################channel 2 standup start######################
    standup_start_v1(users[1]['token'], channels[1]['channel_id'], time_sleep)
    
    #calculate the time when the function should finish
    time_finish = (datetime.datetime.now()+datetime.timedelta(seconds=time_sleep)).strftime("%Y-%m-%d %H:%M:%S")
    time_finish = time.strptime(time_finish, "%Y-%m-%d %H:%M:%S")
    time_finish = time.mktime(time_finish)

    assert standup_active_v1(users[1]['token'], channels[1]['channel_id'])['is_active'] == True
    assert standup_active_v1(users[1]['token'], channels[1]['channel_id'])['time_finish'] == time_finish
    
    time.sleep(time_sleep + 1)
    ###################channel 2 standup finishes######################
    assert standup_active_v1(users[1]['token'], channels[1]['channel_id'])['is_active'] == False
    assert standup_active_v1(users[1]['token'], channels[1]['channel_id'])['time_finish'] == None
    
    clear_v1()

def test_notification_in_standup(create_valid_user_data):
    users = create_valid_user_data['users']
    channels = create_valid_user_data['channels']
    time_sleep = 3

    #generate some pre-exist messages in the channel
    for i in range(10):
        message_send_v2(users[0]['token'], channels[0]['channel_id'], f"First channel message {i}.")
    
    ###################channel 1 strandup start######################
    standup_start_v1(users[0]['token'], channels[0]['channel_id'], time_sleep)

    #send some messages to the standup
    msg1 = "@cd Hi are you ok? And you? @ef"
    msg2 = "@ab Yes I am good."
    msg3 = "@cd That's great."
    msg4 = "aaa"
    msg5 = "bbb"
    msg6 = "@ab what are you doing?"
    standup_send_v1(users[0]['token'], channels[0]['channel_id'], msg1)
    standup_send_v1(users[1]['token'], channels[0]['channel_id'], msg2)
    standup_send_v1(users[0]['token'], channels[0]['channel_id'], msg3)
    standup_send_v1(users[1]['token'], channels[0]['channel_id'], msg4)
    standup_send_v1(users[1]['token'], channels[0]['channel_id'], msg5)
    standup_send_v1(users[2]['token'], channels[0]['channel_id'], msg6)
    buffered_msg = "ab: " + msg1 + "\n" + "cd: " + msg2 + "\n" + "ab: " + msg3 + "\n" + "cd: " + msg4 + "\n" + "cd: " + msg5 + "\n" + "ef: " + msg6

    time.sleep(time_sleep + 1)
    
    #####################channel 1 standup finishes##########################

    assert notifications_get_v1(users[0]['token']) == {
        'notifications': [
            {
                'channel_id': channels[0]['channel_id'],
                'dm_id': -1,
                'notification_message': f"ab tagged you in General: {buffered_msg[0:20]}"
            },
            {
                'channel_id': channels[0]['channel_id'],
                'dm_id': -1,
                'notification_message': f"ab tagged you in General: {buffered_msg[0:20]}"
            },
        ]
    }

    assert notifications_get_v1(users[1]['token']) == {
        'notifications': [
            {
                'channel_id': channels[0]['channel_id'],
                'dm_id': -1,
                'notification_message': f"ab tagged you in General: {buffered_msg[0:20]}"
            },
            {
                'channel_id': channels[0]['channel_id'],
                'dm_id': -1,
                'notification_message': f"ab tagged you in General: {buffered_msg[0:20]}"
            },
        ]
    }


    assert notifications_get_v1(users[2]['token']) == {
        'notifications': [
            {
                'channel_id': channels[0]['channel_id'],
                'dm_id': -1,
                'notification_message': f"ab tagged you in General: {buffered_msg[0:20]}"
            },
        ]
    }

    clear_v1()