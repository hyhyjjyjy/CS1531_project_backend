#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:44:40 2021

@author: z5257847
"""
import pytest
from src.user import user_stats, users_stats
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_join_v2, channel_addowner_v1, channel_leave_v1, channel_removeowner_v1 
from src.dms import dm_create_v1, dm_invite_v1,dm_leave_v1, dm_remove_v1
from src.message import message_send_v2, message_senddm_v1, message_remove_v1, message_edit_v2
from src.other import clear_v1
from src.error import AccessError

def test_invalid_token():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channels_create_v2(result1['token'], "The party channel 1", True)
    channels_create_v2(result1['token'], "The party channel 2", True)
    with pytest.raises(AccessError):
        user_stats('abcdef')


def test_channels_create_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channels_create_v2(result1['token'], "The party channel 1", True)
    channels_create_v2(result1['token'], "The party channel 2", True)
    output = user_stats(result1['token'])

    dreams = users_stats(result1['token'])
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

def test_channel_invite_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True)
    channel_invite_v2(result1['token'], channel1['channel_id'], result2['auth_user_id'])

    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    dreams = users_stats(result1['token'])

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

def test_channel_join_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True)
    channel_join_v2(result2['token'], channel1['channel_id'])

    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    dreams = users_stats(result1['token'])

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

def test_channel_addowner_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result2['token'], "The party channel 1", True)
    channel_addowner_v1(result2['token'], channel1['channel_id'], result1['auth_user_id'])

    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    dreams = users_stats(result1['token'])

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

def test_channel_removeowner_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result2['token'], "The party channel 1", True)
    channel_addowner_v1(result2['token'], channel1['channel_id'], result1['auth_user_id'])
    channel_removeowner_v1(result1['token'], channel1['channel_id'], result2['auth_user_id'])

    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    dreams = users_stats(result1['token'])

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

def test_channel_leave_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result2['token'], "The party channel 1", True)
    channel_addowner_v1(result2['token'], channel1['channel_id'], result1['auth_user_id'])
    channel_leave_v1(result2['token'], channel1['channel_id'])
 
    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    dreams = users_stats(result1['token'])

    

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

def test_dm_create_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')

    dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']])

    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    output2 = user_stats(result3['token'])

    dreams = users_stats(result1['token'])
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

def test_dm_invite_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')

    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id']])
    dm_invite_v1(result1['token'], dm1['dm_id'], result3['auth_user_id'])

    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    output2 = user_stats(result3['token'])

    dreams = users_stats(result1['token'])
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

def test_dm_leave_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')

    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']])
    dm_leave_v1(result3['token'], dm1['dm_id'])

    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    output2 = user_stats(result3['token'])

    dreams = users_stats(result1['token'])
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

def test_dm_remove_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')

    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']])
    message_senddm_v1(result1['token'], dm1['dm_id'], 'Hello, how are you?')
    dm_remove_v1(result1['token'], dm1['dm_id'])

    output = user_stats(result1['token'])
    output1 = user_stats(result2['token'])
    output2 = user_stats(result3['token'])

    dreams = users_stats(result1['token'])
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

def test_message_send_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True)
    message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    output = user_stats(result1['token'])

    dreams = users_stats(result1['token'])
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
    
def test_message_senddm_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')
    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']])
    message_senddm_v1(result1['token'], dm1['dm_id'], 'Hello, how are you?')
    output = user_stats(result1['token'])

    dreams = users_stats(result1['token'])
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

def test_message_remove_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')
    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']])
    message1 = message_senddm_v1(result1['token'], dm1['dm_id'], 'Hello, how are you?')
    message_remove_v1(result1['token'], message1['message_id'])

    output = user_stats(result1['token'])

    dreams = users_stats(result1['token'])
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

def test_message_edit_stat():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True)
    message1 = message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    message2 = message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    message_edit_v2(result1['token'], message1['message_id'], 'Hi Im user 1')
    message_edit_v2(result1['token'], message2['message_id'], '')

    output = user_stats(result1['token'])

    dreams = users_stats(result1['token'])
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
    
def test_mixed_basic():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')
    channels_create_v2(result1['token'], "The party channel 1", True)
    channels_create_v2(result1['token'], "The party channel 2", True)
    dm_create_v1(result1['token'], [result2['auth_user_id']])

    output = user_stats(result1['token'])

    dreams = users_stats(result1['token'])
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

def test_mixed_decrement():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True)['channel_id']
    message1 = message_send_v2(result1['token'], channel1, 'hello how are you')['message_id']
    
    message_remove_v1(result1['token'], message1)
    channel_join_v2(result2['token'], channel1)
    channel_leave_v1(result2['token'], channel1)

    output = user_stats(result1['token'])
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    output1 = user_stats(result2['token'])
    assert output1['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    dreams = users_stats(result1['token'])
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
       

def test_mixed_harder():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True)['channel_id']
    message_send_v2(result1['token'], channel1, 'hello how are you')
    dm_create_v1(result1['token'], [result2['auth_user_id']])
    output = user_stats(result1['token'])
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 1
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 1
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output['user_stats']['involvement_rate'] == 1
    channels_create_v2(result1['token'], "The party channel 2", True)
    channel3 = channels_create_v2(result2['token'], "The party channel 3", True)['channel_id']
    channel_addowner_v1(result2['token'], channel3, result1['auth_user_id'])
    message_send_v2(result2['token'], channel3, 'hello how are you')
    output1 = user_stats(result1['token'])
    output2 = user_stats(result2['token'])
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

    dreams = users_stats(result1['token'])
    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 3
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 1
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 2
    assert dreams['dreams_stats']['utilization_rate'] == 1    

def test_further_mixed_harder():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    result3 = auth_register_v2('thirdemail@gmail.com', 'password', 'comp', 'student')
    result4 = auth_register_v2('fourthemail@gmail.com', 'password', 'comp', 'student')
    
    channel1 = channels_create_v2(result1['token'], "The party channel 1", True)
    channel2 = channels_create_v2(result2['token'], "The party channel 2", True)
    dm_create_v1(result1['token'], [result2['auth_user_id'], result3['auth_user_id']])
    dm_create_v1(result2['token'], [result4['auth_user_id'], result3['auth_user_id']])

    output1 = user_stats(result1['token'])
    output2 = user_stats(result2['token'])
    output3 = user_stats(result3['token'])
    output4 = user_stats(result4['token'])
    
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

    dreams = users_stats(result1['token'])
    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 2
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 2
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 1    

    
    channel_invite_v2(result1['token'], channel1['channel_id'], result3['auth_user_id'])
    channel_invite_v2(result2['token'], channel2['channel_id'], result3['auth_user_id'])
    
    message1 = message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    message_send_v2(result1['token'], channel1['channel_id'], 'Hello, how are you?')
    message_send_v2(result2['token'], channel2['channel_id'], 'Hello, how are you?')
    message2 = message_send_v2(result3['token'], channel2['channel_id'], 'Hello, how are you?')
    message_remove_v1(result1['token'], message1['message_id'])
    message_remove_v1(result3['token'], message2['message_id'])
    
    auth_register_v2('fifthemail@gmail.com', 'password', 'comp', 'student')
    
    output1 = user_stats(result1['token'])
    output2 = user_stats(result2['token'])
    output3 = user_stats(result3['token'])
    output4 = user_stats(result4['token'])
    dreams = users_stats(result1['token'])

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

def test_zero_division():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    dm1 = dm_create_v1(result1['token'], [result2['auth_user_id']])
    message_senddm_v1(result1['token'], dm1['dm_id'], "Pls")
    dm_remove_v1(result1['token'], dm1['dm_id'])
    output = user_stats(result1['token'])

    dreams = users_stats(result1['token'])
    assert len(output['user_stats']) == 4
    assert output['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert output['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert output['user_stats']['messages_sent'][-1]['num_messages_sent'] == 1
    assert output['user_stats']['involvement_rate'] == 0

    assert len(dreams['dreams_stats']) == 4
    assert dreams['dreams_stats']['channels_exist'][-1]['num_channels_exist'] == 0
    assert dreams['dreams_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert dreams['dreams_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert dreams['dreams_stats']['utilization_rate'] == 0