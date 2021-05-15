#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 19:58:04 2021

@author: z5257847
"""

import pytest
import requests
from src import config

#Creating global variables for Input and Access errirs
INPUT_ERROR = 400
ACCESS_ERROR = 403


def test_invalid_token():
    url = config.url
    requests.delete(f"{url}clear/v1")
    requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    output = requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': 'abcdef',  'img_url' : 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg', 'x_start' : 0, 'y_start' : 0, 'x_end' : 50, 'y_end' : 50,})
    assert output.status_code == ACCESS_ERROR
    
def test_crop_error():
    url = config.url
    requests.delete(f"{url}clear/v1")
    result1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',}).json()
    output = requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': result1['token'],  'img_url' : 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg', 'x_start' : -1, 'y_start' : 0, 'x_end' : 50, 'y_end' : 50,})
    assert output.status_code == INPUT_ERROR
    output1 = requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': result1['token'],  'img_url' : 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg', 'x_start' : 0, 'y_start' : -1, 'x_end' : 50, 'y_end' : 50,})
    assert output1.status_code == INPUT_ERROR
    output2 = requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': result1['token'],  'img_url' : 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg', 'x_start' : 0, 'y_start' : 0, 'x_end' : 10000, 'y_end' : 50,})
    assert output2.status_code == INPUT_ERROR    
    output2 = requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': result1['token'],  'img_url' : 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg', 'x_start' : 0, 'y_start' : 0, 'x_end' : 50, 'y_end' : 10000,})
    assert output2.status_code == INPUT_ERROR

def test_not_jpg():
    url = config.url
    requests.delete(f"{url}clear/v1")
    result1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',}).json()
    output = requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': result1['token'],  'img_url' : 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png', 'x_start' : 0, 'y_start' : 0, 'x_end' : 50, 'y_end' : 50,})
    assert output.status_code == INPUT_ERROR    

def test_invalid_url():
    url = config.url
    requests.delete(f"{url}clear/v1")
    result1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',}).json()
    output = requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': result1['token'],  'img_url' : 'abcdef', 'x_start' : 0, 'y_start' : 0, 'x_end' : 50, 'y_end' : 50,})
    assert output.status_code == INPUT_ERROR 
    
def test_simple():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',})
    user1 = user1.json()
    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output2 = output2.json()
    requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': user1['token'],  'img_url' : 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg', 'x_start' : 0, 'y_start' : 0, 'x_end' : 50, 'y_end' : 50,})
    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()

    assert output1['user']['profile_img_url'] != output2['user']['profile_img_url']

def test_multiple():
    url = config.url
    requests.delete(f"{url}clear/v1")
    user1 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jordan.milch@gmail.com', 'password' : 'random',}).json()
    user2 = requests.post(f"{url}auth/register/v2", json = { 'name_first' : 'jordan', 'name_last' : 'milch', 'email' : 'jilch@gmail.com', 'password' : 'random',}).json()

    output1 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output1 = output1.json()
    requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': user1['token'],  'img_url' : 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg', 'x_start' : 0, 'y_start' : 0, 'x_end' : 50, 'y_end' : 50,})
    output2 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user1['auth_user_id']})
    output2 = output2.json()

    output3 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output3 = output3.json()
    requests.post(f"{url}user/profile/uploadphoto/v1", json = {'token': user2['token'],  'img_url' : 'https://media.vanityfair.com/photos/5a9069131d14714f6de43ff5/7:3/w_1995,h_855,c_limit/tout-and-lede_Lisa-Simpson.jpg', 'x_start' : 0, 'y_start' : 0, 'x_end' : 50, 'y_end' : 50,})
    output4 = requests.get(f"{url}user/profile/v2", params = {'token' : user1['token'], 'u_id' : user2['auth_user_id']})
    output4 = output4.json()

    assert output1['user']['profile_img_url'] == output3['user']['profile_img_url']
    assert output1['user']['profile_img_url'] != output2['user']['profile_img_url']
    assert output3['user']['profile_img_url'] != output4['user']['profile_img_url']
    assert output2['user']['profile_img_url'] != output4['user']['profile_img_url']

    requests.delete(f"{url}clear/v1")
