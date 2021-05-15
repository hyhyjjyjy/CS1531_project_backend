# import pytest
# from src.error import InputError, AccessError
# from src.channels import channels_create_v1, channels_listall_v1
# from src.auth import auth_register_v1
# from src.other import clear_v1

# def test_create_channel_invalid_input():
#     clear_v1()
#     auth_register_v1("bunnydongao@gmail.com","abcdefg1234", "bunny", "dong")
#     auth_register_v1("jamesdongao@gmail.com","abcdefg1234", "bunny", "dong")
#     auth_register_v1("Mikedongao@gmail.com","abcdefg1234", "abcdef", "fwef")

#     with pytest.raises(InputError):
#         channels_create_v1(1, "dadfewfwefewfewfewfewfewfewfew", True)
#         channels_create_v1(1, "fwefwewfewfwefefweefwefewfefwe", False)
#         channels_create_v1(1, "A very very very very very long channel", True)

#     with pytest.raises(AccessError):
#         channels_create_v1(5, "fwegertgre", True)
#         channels_create_v1(6, "oiefnweifpof", False)

    

# def test_create_channel_successfully():
#     clear_v1()
#     auth_register_v1("bunnydongao@gmail.com","abcdefg1234", "bunny", "dong")
#     auth_register_v1("jamesdongao@gmail.com","abcdefg1234", "bunny", "dong")
#     auth_register_v1("Mikedongao@gmail.com","abcdefg1234", "abcdef", "fwef")
#     auth_register_v1("indexsam@gmail.com","abcdefg1234", "index", "sam")
#     auth_register_v1("jhony@gmail.com","abcdefg1234", "awe", "some")

#     channel_id_1 = channels_create_v1(1, "The party channel 1", True)['channel_id']
#     assert(channels_listall_v1(1) == [{'channel_id': channel_id_1, 'name': "The party channel 1",},])

#     channel_id_2 = channels_create_v1(2, "The party channel 2", True)['channel_id']

#     assert(channels_listall_v1(1) == [{'channel_id': channel_id_1, 'name': "The party channel 1",},
#                                       {'channel_id': channel_id_2, 'name': "The party channel 2",},])

#     channel_id_3 = channels_create_v1(3, "The party channel 3", True)['channel_id']

#     assert(channels_listall_v1(1) == [{'channel_id': channel_id_1, 'name': "The party channel 1",},
#                                       {'channel_id': channel_id_2, 'name': "The party channel 2",},
#                                       {'channel_id': channel_id_3, 'name': "The party channel 3",},])

