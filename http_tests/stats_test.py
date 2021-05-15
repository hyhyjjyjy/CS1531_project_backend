#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 21:17:16 2021

@author: z5257847
"""

import pytest
import requests
from src import config
from http_tests.helper_function_for_http_test import user_stats, users_stats
from http_tests.helper_function_for_http_test import auth_register_v2
from http_tests.helper_function_for_http_test import channels_create_v2
from http_tests.helper_function_for_http_test import channel_invite_v2, channel_join_v2, channel_addowner_v1, channel_leave_v1, channel_removeowner_v1 
from http_tests.helper_function_for_http_test import dm_create_v1, dm_invite_v1,dm_leave_v1, dm_remove_v1
from http_tests.helper_function_for_http_test import message_send_v2, message_senddm_v1, message_remove_v1, message_edit_v2
from http_tests.helper_function_for_http_test import clear_v1

#Creating global variables for Input and Access errirs
INPUT_ERROR = 400
ACCESS_ERROR = 403

#Testing an AcessError is raised when an invalid token is passed
def test_invalid_token():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channels_create_v2(result1['token'], "The party channel 1", True)
    channels_create_v2(result1['token'], "The party channel 2", True)
    user_stats('abcdef').status_code == ACCESS_ERROR

#Testing channels create is correctly changing stats
def test_channels_create_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channels_create_v2(result1['token'], "The party channel 1", True)
    channels_create_v2(result1['token'], "The party channel 2", True)
    output = user_stats(result1['token']).json()
    print(output)
    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 2
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 2
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 1/2

#Testing channels invite is correctly changing stats
def test_channel_invite_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True).json()
    channel_invite_v2(result1['token'], channel1['channel_id'], result2['auth_user_id'])

    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    dreams = users_stats(result1['token']).json()

    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 1

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 2/2    

#Testing channels join is correctly changing stats
def test_channel_join_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True).json()
    channel_join_v2(result2['token'], channel1['channel_id'])

    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    dreams = users_stats(result1['token']).json()

    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 1

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 2/2 

#Testing channels addowner is correctly changing stats
def test_channel_addowner_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result2['token'], "The party channel 1", True).json()
    channel_addowner_v1(result2['token'], channel1['channel_id'], result1['auth_user_id'])

    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    dreams = users_stats(result1['token']).json()

    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 1

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 2/2     

#Testing channels removeowner is correctly changing stats
def test_channel_removeowner_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result2['token'], "The party channel 1", True).json()
    channel_addowner_v1(result2['token'], channel1['channel_id'], result1['auth_user_id'])
    channel_removeowner_v1(result1['token'], channel1['channel_id'], result2['auth_user_id'])

    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    dreams = users_stats(result1['token']).json()

    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 1

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 2/2 

#Testing channels leave is correctly changing stats
def test_channel_leave_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result2['token'], "The party channel 1", True).json()
    channel_addowner_v1(result2['token'], channel1['channel_id'], result1['auth_user_id'])
    channel_leave_v1(result2['token'], channel1['channel_id'])
    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    dreams = users_stats(result1['token']).json()

    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 0

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 1/2 

#Testing dm create is correctly changing stats
def test_dm_create_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student').json()

    dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']])

    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    output2 = user_stats(result3['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 1

    assert len(output2['user_stats']) == 4
    assert output2['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output2['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output2['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output2['user_stats']['involvement_rate'] == 1
    
    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 0
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 1

#Testing dm invite is correctly changing stats
def test_dm_invite_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student').json()

    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id']]).json()
    dm_invite_v1(result1['token'], dm1['dm_id'], result3['auth_user_id'])

    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    output2 = user_stats(result3['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 1

    assert len(output2['user_stats']) == 4
    assert output2['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output2['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output2['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output2['user_stats']['involvement_rate'] == 1
    
    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 0
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 1

#Testing dm leave is correctly changing stats
def test_dm_leave_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student').json()

    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']]).json()
    dm_leave_v1(result3['token'], dm1['dm_id'])

    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    output2 = user_stats(result3['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 1

    assert len(output2['user_stats']) == 4
    assert output2['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output2['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output2['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output2['user_stats']['involvement_rate'] == 0
    
    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 0
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 2/3

#Testing dm remove is correctly changing stats
def test_dm_remove_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student').json()

    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']]).json()
    message_senddm_v1(result1['token'], dm1['dm_id'], "helloooo")
    dm_remove_v1(result1['token'], dm1['dm_id'])

    output = user_stats(result1['token']).json()
    output1 = user_stats(result2['token']).json()
    output2 = user_stats(result3['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output['user_stats']['involvement_rate'] == 0

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 0

    assert len(output2['user_stats']) == 4
    assert output2['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output2['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output2['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output2['user_stats']['involvement_rate'] == 0
    
    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 0
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 0

#Testing message send is correctly changing stats
def test_message_send_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True).json()
    message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    output = user_stats(result1['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output['user_stats']['involvement_rate'] == 1

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 1
    assert dreams['dreams_stats']['utilization_rate'] == 1

#Testing message senddm is correctly changing stats
def test_message_senddm_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student').json()
    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']]).json()
    message_senddm_v1(result1['token'], dm1['dm_id'], 'Hello, how are you?')
    output = user_stats(result1['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output['user_stats']['involvement_rate'] == 1

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 0
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 1
    assert dreams['dreams_stats']['utilization_rate'] == 1

#Testing message remove is correctly changing stats
def test_message_remove_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student').json()
    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']]).json()
    message1 = message_senddm_v1(result1['token'], dm1['dm_id'], 'Hello, how are you?').json()
    message_remove_v1(result1['token'], message1['message_id'])

    output = user_stats(result1['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output['user_stats']['involvement_rate'] == 2

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 0
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 1

#Testing message edit is correctly changing stats
def test_message_edit_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True).json()
    message1 = message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?').json()
    message2 = message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?').json()
    message_edit_v2(result1['token'], message1['message_id'], 'Hi Im user 1')
    message_edit_v2(result1['token'], message2['message_id'], '')
    #message_remove_v1(result1['token'], message2['message_id'])
    output = user_stats(result1['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 2
    assert output['user_stats']['involvement_rate'] == 3/2

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 1
    assert dreams['dreams_stats']['utilization_rate'] == 1
   
#Testing a variety of functions is correctly changing stats
def test_mixed_basic():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')
    channels_create_v2(result1['token'], "The party channel 1", True)
    channels_create_v2(result1['token'], "The party channel 2", True)
    dm_create_v1(result1['token'], [result2['auth_user_id']])

    output = user_stats(result1['token']).json()

    dreams = users_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 2
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output['user_stats']['involvement_rate'] == 1

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 2
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 2/3

#Testing a harder variety of functions is correctly changing stats
def test_mixed_decrement():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True).json()['channel_id']
    message1 = message_send_v2(result1['token'], channel1, 'hello how are you').json()['message_id']
    
    message_remove_v1(result1['token'], message1)
    channel_join_v2(result2['token'], channel1)
    channel_leave_v1(result2['token'], channel1)

    output = user_stats(result1['token']).json()
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    output1 = user_stats(result2['token']).json()
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    dreams = users_stats(result1['token']).json()
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
       
#Testing a harder variety of functions is correctly changing stats
def test_mixed_harder():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True).json()['channel_id']
    message_send_v2(result1['token'], channel1, 'hello how are you')
    dm_create_v1(result1['token'], [result2['auth_user_id']])
    output = user_stats(result1['token']).json()
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output['user_stats']['involvement_rate'] == 1
    channels_create_v2(result1['token'], "The party channel 2", True)
    channel3 = channels_create_v2(result2['token'], "The party channel 3", True).json()['channel_id']
    channel_addowner_v1(result2['token'], channel3, result1['auth_user_id'])
    message_send_v2(result2['token'], channel3, 'hello how are you')
    output1 = user_stats(result1['token']).json()
    output2 = user_stats(result2['token']).json()
    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 3
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output1['user_stats']['involvement_rate'] == 5/6
    assert len(output2['user_stats']) == 4
    assert output2['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output2['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output2['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output2['user_stats']['involvement_rate'] == 3/6

    dreams = users_stats(result1['token']).json()
    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 3
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 2
    assert dreams['dreams_stats']['utilization_rate'] == 1    

#Testing a harder variety of functions is correctly changing stats
def test_further_mixed_harder():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student').json()
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student').json()
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student').json()
    result4 = auth_register_v2('fourthemail@gmail.com', 'password', 'comp', 'student').json()
    
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True).json()
    channel2 = channels_create_v2(result2['token'], "The party channel 2", True).json()
    dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']])
    dm_create_v1(result2['token'], [result4['auth_user_id'], result3['auth_user_id']])

    output1 = user_stats(result1['token']).json()
    output2 = user_stats(result2['token']).json()
    output3 = user_stats(result3['token']).json()
    output4 = user_stats(result4['token']).json()
    
    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output1['user_stats']['involvement_rate'] == 2/4
    
    assert len(output2['user_stats']) == 4
    assert output2['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output2['user_stats']['dms_joined'][-1]['num_dms_joined'] == 2
    assert output2['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output2['user_stats']['involvement_rate'] == 3/4
    
    assert len(output3['user_stats']) == 4
    assert output3['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output3['user_stats']['dms_joined'][-1]['num_dms_joined'] == 2
    assert output3['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output3['user_stats']['involvement_rate'] == 2/4
    
    assert len(output4['user_stats']) == 4
    assert output4['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output4['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output4['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output4['user_stats']['involvement_rate'] == 1/4

    dreams = users_stats(result1['token']).json()
    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 2
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 2
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 1    

    
    channel_invite_v2(result1['token'], channel1['channel_id'], result3['auth_user_id'])
    channel_invite_v2(result2['token'], channel2['channel_id'], result3['auth_user_id'])
    
    message1 = message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?').json()
    message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    message_send_v2(result2['token'], channel2['channel_id'], 'Hello, how are you?')
    message2 = message_send_v2(result3['token'], channel2['channel_id'], 'Hello, how are you?').json()
    message_remove_v1(result1['token'], message1['message_id'])
    message_remove_v1(result3['token'], message2['message_id'])
    
    auth_register_v2('fifthemail@gmail.com', 'password', 'comp', 'student')
    
    output1 = user_stats(result1['token']).json()
    output2 = user_stats(result2['token']).json()
    output3 = user_stats(result3['token']).json()
    output4 = user_stats(result4['token']).json()
    dreams = users_stats(result1['token']).json()

    assert len(output1['user_stats']) == 4
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output1['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output1['user_stats']['messages_sent'][-1]['num_messages_sent'] == 3
    assert output1['user_stats']['involvement_rate'] == 5/7
    
    assert len(output2['user_stats']) == 4
    assert output2['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output2['user_stats']['dms_joined'][-1]['num_dms_joined'] == 2
    assert output2['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output2['user_stats']['involvement_rate'] == 4/7
     
    assert len(output3['user_stats']) == 4
    assert output3['user_stats']['channels_joined'][-1]['num_channels_joined'] == 2
    assert output3['user_stats']['dms_joined'][-1]['num_dms_joined'] == 2
    assert output3['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output3['user_stats']['involvement_rate'] == 5/7
    
    assert len(output4['user_stats']) == 4
    assert output4['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output4['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output4['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert output4['user_stats']['involvement_rate'] == 1/7

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 2
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 2
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 3
    assert dreams['dreams_stats']['utilization_rate'] == 4/5     
    clear_v1()