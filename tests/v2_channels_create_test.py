import pytest
from src.error import InputError, AccessError
from src.channels import channels_create_v2, channels_listall_v2
from src.auth import auth_register_v2
from src.other import clear_v1

def test_create_channel_invalid_input():
    clear_v1()
    user1 = auth_register_v2("bunnydongao@gmail.com","abcdefg1234", "bunny", "dong")

    with pytest.raises(InputError):
        channels_create_v2(user1['token'], "dadfewfwefewfewfewfewfewfewfew", True)
        channels_create_v2(user1['token'], "fwefwewfewfwefefweefwefewfefwe", False)
        channels_create_v2(user1['token'], "A very very very very very long channel", True)
        
    with pytest.raises(AccessError):
        channels_create_v2(2.5, "fwegertgre", True)
        channels_create_v2(3.5, "oiefnweifpof", False)    

def test_create_channel_successfully():
    clear_v1()
    u1 = auth_register_v2("bunnydongao@gmail.com","abcdefg1234", "bunny", "dong")
    u2 = auth_register_v2("jamesdongao@gmail.com","abcdefg1234", "bunny", "dong")
    u3 = auth_register_v2("Mikedongao@gmail.com","abcdefg1234", "abcdef", "fwef")

    channel_1 = channels_create_v2(u1['token'], "The party channel 1", True)['channel_id']
    assert(channels_listall_v2(u1['token']) == {'channels' : [{'channel_id': channel_1, 'name': "The party channel 1",},]})
    
    channel_2 = channels_create_v2(u2['token'], "The party channel 2", True)['channel_id']

    assert(channels_listall_v2(u1['token']) == {'channels' : [{'channel_id': channel_1, 'name': "The party channel 1",},
                                      {'channel_id': channel_2, 'name': "The party channel 2",},]})

    channel_3 = channels_create_v2(u3['token'], "The party channel 3", True)['channel_id']

    assert(channels_listall_v2(u1['token']) == {'channels' : [{'channel_id': channel_1, 'name': "The party channel 1",},
                                      {'channel_id': channel_2, 'name': "The party channel 2",},
                                      {'channel_id': channel_3, 'name': "The party channel 3",},]})
    clear_v1()
