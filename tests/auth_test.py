# import pytest
# from src.auth import auth_login_v1, auth_register_v1
# from src.other import clear_v1
# from src.error import InputError
# from src.channels import channels_create_v1
# from src.channel import channel_join_v1, channel_details_v1
# from src.data import data_dic

# #Fixture to register 3 users to prevent repeating code
# @pytest.fixture
# def register_three_users():
#     clear_v1()
#     auth_register_v1('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     auth_register_v1('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     auth_register_v1('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student')    

# #Testing multiple invalid emails to determine if auth_register_v1 is correctly identifying this error
# def test_invalid_email_register():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1('invalidemailgmail.com', '123abc!@#', 'Comp', 'Student')
#         auth_register_v1('invalid#email@gmail.com', '123abc!@#', 'Comp', 'Student')              

# #Testing passwords less than 6 characters long to determine if auth_register_v1 is correctly identifying this error
# def test_short_password():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1('pwdshortemail1@gmail.com', 'hi', 'Comp', 'Student')
#         auth_register_v1('pwdshortemail2@gmail.com', '', 'Comp', 'Student')
#         auth_register_v1('pwdshortemail3@gmail.com', 'COMP', 'Comp', 'Student')

# #Testing first names less than 1 character and more than 50 characters long to determine if auth_register_v1 is correctly identifying this error
# def test_invalid_first_name():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1('fnameshortemail1@gmail.com', 'hello123', '', 'Student')
#         auth_register_v1('fnamelongemail1@gmail.com', 'hello123', 
#                          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 
#                          'Student')

# #Testing last names less than 1 character and more than 50 characters long to determine if auth_register_v1 is correctly identifying this error
# def test_invalid_last_name():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1('lnameshortemail1@gmail.com', 'hello123', 'Comp',
#                          'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz') 

# #Registering one user and determing if the output is as expected - returning a dictionary with key 'auth_user_id' with a unique int value
# def test_basic_register():
#     clear_v1()
#     result = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     assert type(result) == dict
#     assert type(result['auth_user_id']) == int

# #Registering multiple users and checking that the output from each is correct and the u_id returned is unique to each user
# def test_multiple_register():
#     clear_v1()
#     result1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     result2 = auth_register_v1('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     result3 = auth_register_v1('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     assert result1 != result2
#     assert result1['auth_user_id'] != result2['auth_user_id']
#     assert result1 != result3
#     assert result1['auth_user_id'] != result3['auth_user_id']
#     assert result3 != result2
#     assert result3['auth_user_id'] != result2['auth_user_id']
#     assert type(result1) == dict
#     assert type(result1['auth_user_id']) == int
#     assert type(result2) == dict
#     assert type(result2['auth_user_id']) == int
#     assert type(result3) == dict
#     assert type(result3['auth_user_id']) == int    

# #Testing for multiple users, whilst an error is raised, to ensure the code continues to function as expected
# def test_multiple_register_with_error(register_three_users):

#     result1 = auth_register_v1('fourthemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     with pytest.raises(InputError):   
#         auth_register_v1('invalidemailgmail.com', '123abc!@#', 'Comp', 'Student')                      
#     result2 = auth_register_v1('fifthemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     assert result1 != result2
#     assert result1['auth_user_id'] != result2['auth_user_id']

# #Registering a valid user and then checking that auth_login_v1 correctly identifies an invalid email and raises an InputError
# def test_invalid_email_login():
#     clear_v1()
#     auth_register_v1('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')    
#     with pytest.raises(InputError):
#         auth_login_v1('invalidemailgmail.com', '123abc!@#')
#         auth_login_v1('invalid#email@gmail.com', '123abc!@#')   

# #Using the aforementioned fixture and checking that auth_login_v1 raises an error when an un-registered email is used to try log in
# def test_email_doesnt_belong(register_three_users):
   
#     with pytest.raises(InputError):
#         auth_login_v1('comp@gmail.com','random')
#         auth_login_v1('unsw@gmail.com','random')
#         auth_login_v1('sydney@gmail.com','random')

# #Testing multiple invalid emails
# def test_multiple_invalid_inputs(register_three_users):
#     with pytest.raises(InputError):
#         auth_login_v1('invalidemailgmail.com', 'incorrect')
#         auth_login_v1('validemail@gmail.com','incorrect')

# #Testing auth_register_v1 to check that an error is raised when an already registered email is used again
# def test_email_in_use_register(register_three_users):
    
#     with pytest.raises(InputError):                         
#         auth_register_v1('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')               
#         auth_register_v1('secondemail@gmail.com', 'random', 'Comp', 'Student')               
#         auth_register_v1('thirdemail@gmail.com', 'random', 'Comp', 'Student') 

# #Testing that auth_login_v1 raises an error when a registered email but incorrect password is used
# def test_password_doesnt_match(register_three_users):

#     with pytest.raises(InputError):
#         auth_login_v1('validemail@gmail.com','incorrect')
#         auth_login_v1('secondemail@gmail.com','wrongpass')
#         auth_login_v1('thirdemail@gmail.com','errorexpect')

# #Trying to log in without there being any registered users
# def test_empty_login():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_login_v1('validemail@gmail.com','incorrect')        

# #Testing basic login functionality to ensure that the output is identical to that of auth_register_v1 and that it consists of a dictionary with key 'auth_user_id' and a corresponding integer value
# def test_login_basic():
#     clear_v1()
#     result1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')    
#     result2 = auth_login_v1('validemail@gmail.com', '123abc!@#')
#     assert result1 == result2
#     assert type(result1) == dict
#     assert type(result1['auth_user_id']) == int
#     assert type(result2) == dict
#     assert type(result2['auth_user_id']) == int

# #Testing multiple log-in to ensure functionality remains as expected and no errors are raised
# def test_login_multiple():
#     clear_v1()
#     result1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     result2 = auth_register_v1('secondemail@gmail.com', '123abc!@#', 'Comp', 'Student')
#     result3 = auth_register_v1('thirdemail@gmail.com', '123abc!@#', 'Comp', 'Student') 
#     result1a = auth_login_v1('validemail@gmail.com', '123abc!@#')
#     result2a = auth_login_v1('secondemail@gmail.com', '123abc!@#')
#     result3a = auth_login_v1('thirdemail@gmail.com', '123abc!@#')
#     assert result1 == result1a
#     assert result2 == result2a
#     assert result3 == result3a
#     assert result1 != result2
#     assert result2 != result3
#     assert result1a != result2a
#     assert result3a != result2a



# #Testing the basic generation of a user handle
# def test_basic_handle():
#     clear_v1()
#     user_1 = auth_register_v1('jordanmilch@gmail.com', 'random', 'Jordan', 'Milch')
#     channel_1 = channels_create_v1(user_1['auth_user_id'], "General", True)
#     channel_detail = channel_details_v1(user_1['auth_user_id'], channel_1['channel_id'])
#     assert channel_detail['all_members'][0].get('handle_str') == 'jordanmilch'
#     clear_v1()

# #Testing that the handle correctly adds a trailing integer when a name is repeated
# def test_trailing_int_handle():
#     clear_v1()
#     auth_register_v1('jordanmilch@gmail.com', 'random', 'Jordan', 'Milch')
#     user_2 = auth_register_v1('jmilch@gmail.com', 'random', 'Jordan', 'Milch')
#     channel_1 = channels_create_v1(user_2['auth_user_id'], "General", True)
#     channel_detail = channel_details_v1(user_2['auth_user_id'], channel_1['channel_id'])
#     assert channel_detail['all_members'][0].get('handle_str') == 'jordanmilch0'
#     clear_v1()

# #Testing that the handle is limited to 20 characters
# def test_handle_with_name_over_20_characters():
#     clear_v1()
#     user_1 = auth_register_v1('jordanmilch@gmail.com', 'random', 'Jordan', 'Milchabcdefghijk')
#     channel_1 = channels_create_v1(user_1['auth_user_id'], "General", True)
#     channel_detail = channel_details_v1(user_1['auth_user_id'], channel_1['channel_id'])
#     assert channel_detail['all_members'][0].get('handle_str') == 'jordanmilchabcdefghi'
#     clear_v1()

# #Testing that the handle does not exceed 20 characters even with a trailing integer added
# def test_handle_with_name_over_20_characters_and_trailing_int():
#     clear_v1()
#     auth_register_v1('jordanmilch@gmail.com', 'random', 'Jordan', 'Milchabcdefghijk')
#     user_2 = auth_register_v1('jmilch@gmail.com', 'random', 'Jordan', 'Milchabcdefghijk')
#     channel_1 = channels_create_v1(user_2['auth_user_id'], "General", True)
#     channel_detail = channel_details_v1(user_2['auth_user_id'], channel_1['channel_id'])
#     assert channel_detail['all_members'][0].get('handle_str') == 'jordanmilchabcdefgh0'
#     clear_v1()

# #Testing multiple advanced handles - such as double digit trailing integers with handles already 20 characters long
# def test_advanced_handle_creation():
#     clear_v1()
#     user_1 = auth_register_v1('jordanmilch@gmail.com', 'random', 'Jordan', 'Milch')
#     user_2 = auth_register_v1('jordanmilch1@gmail.com', 'random', 'Jordan', 'Milch')
#     user_3 = auth_register_v1('jordanmilch2@gmail.com', 'random', 'Jordan', 'Milch')
#     user_4 = auth_register_v1('jordanmilch3@gmail.com', 'random', 'Jordan', 'Milch')
#     user_5 = auth_register_v1('random@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_6 = auth_register_v1('random1@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_7 = auth_register_v1('random2@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_8 = auth_register_v1('random3@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_9 = auth_register_v1('random4@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_10 = auth_register_v1('random5@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_11 = auth_register_v1('random6@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_12 = auth_register_v1('random7@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_13 = auth_register_v1('random8@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_14 = auth_register_v1('random9@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_15 = auth_register_v1('random10@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
#     user_16 = auth_register_v1('random11@mail.com', 'random', 'UNSWCOMPSTUDENT' , 'Studyingtwentytwenty')
    
#     channel_1 = channels_create_v1(user_1['auth_user_id'], "General", True)
    
#     channel_join_v1(user_2['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_3['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_4['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_5['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_6['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_7['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_8['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_9['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_10['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_11['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_12['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_13['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_14['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_15['auth_user_id'], channel_1['channel_id'])
#     channel_join_v1(user_16['auth_user_id'], channel_1['channel_id'])
    
#     channel_detail = channel_details_v1(user_1['auth_user_id'], channel_1['channel_id'])

#     assert channel_detail['all_members'][0].get('handle_str') == 'jordanmilch'
#     assert channel_detail['all_members'][1].get('handle_str') == 'jordanmilch0'
#     assert channel_detail['all_members'][2].get('handle_str') == 'jordanmilch1'
#     assert channel_detail['all_members'][3].get('handle_str') == 'jordanmilch2'
#     assert channel_detail['all_members'][4].get('handle_str') == 'unswcompstudentstudy'
#     assert channel_detail['all_members'][5].get('handle_str') == 'unswcompstudentstud0'
#     assert channel_detail['all_members'][6].get('handle_str') == 'unswcompstudentstud1'
#     assert channel_detail['all_members'][7].get('handle_str') == 'unswcompstudentstud2'
#     assert channel_detail['all_members'][8].get('handle_str') == 'unswcompstudentstud3'
#     assert channel_detail['all_members'][9].get('handle_str') == 'unswcompstudentstud4'
#     assert channel_detail['all_members'][10].get('handle_str') == 'unswcompstudentstud5'
#     assert channel_detail['all_members'][11].get('handle_str') == 'unswcompstudentstud6'
#     assert channel_detail['all_members'][12].get('handle_str') == 'unswcompstudentstud7'
#     assert channel_detail['all_members'][13].get('handle_str') == 'unswcompstudentstud8'
#     assert channel_detail['all_members'][14].get('handle_str') == 'unswcompstudentstud9'
#     assert channel_detail['all_members'][15].get('handle_str') == 'unswcompstudentstu10'
#     clear_v1()
