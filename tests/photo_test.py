#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 18:44:40 2021

@author: z5257847
"""
import pytest
from src.user import user_profile_uploadphoto_v1, user_profile_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import InputError, AccessError

def test_invalid_token():
    clear_v1()    
    auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    with pytest.raises(AccessError):
        user_profile_uploadphoto_v1('abcdef', 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg',0,0,200,200)
    
def test_crop_error():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(result1['token'], 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg',-1,0,200,200)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(result1['token'], 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg',0,-1,200,200)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(result1['token'], 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg',0,0,100000,200)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(result1['token'], 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg',-1,0,100000,100000)
    
def test_not_jpg():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(result1['token'], 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png',0,0,200,200)

def test_invalid_url():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(result1['token'], 'abcdef',0,0,200,200)
    
def test_simple():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    user1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    user_profile_uploadphoto_v1(result1['token'], 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg',0,0,200,200)
    user2 = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert user1['user']['profile_img_url'] != user2['user']['profile_img_url']

def test_multiple():
    clear_v1()    
    result1 = auth_register_v2('firstemail@gmail.com', 'password', 'comp', 'student')
    result2 = auth_register_v2('secondemail@gmail.com', 'password', 'comp', 'student')
    user1 = user_profile_v2(result1['token'], result1['auth_user_id'])
    user2 = user_profile_v2(result1['token'], result2['auth_user_id'])
    user_profile_uploadphoto_v1(result1['token'], 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg',0,0,200,200)
    user_profile_uploadphoto_v1(result2['token'], 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg',0,0,200,200)
    user2 = user_profile_v2(result1['token'], result1['auth_user_id'])
    assert user1['user']['profile_img_url'] != user2['user']['profile_img_url']
    clear_v1()