#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 23:05:10 2021

@author: z5257847
"""

import pytest
from src.auth import auth_register_v2, auth_password_reset, auth_password_reset_request
from src.error import InputError, AccessError
from src.other import clear_v1

def test_invalid_token():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    with pytest.raises(InputError):
        auth_password_reset_request('validail@gmail.com')

def test_basic():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    output = auth_password_reset_request('validemail@gmail.com')
    assert output == {}

def test_newpass_too_short():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    auth_password_reset_request('validemail@gmail.com')
    with pytest.raises(InputError):    
        auth_password_reset(1, 'hi')

def test_reset_no_request():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    with pytest.raises(AccessError):    
        auth_password_reset(1, 'hello123')

def test_reset_incorrect_code():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Comp', 'Student')
    auth_password_reset_request('validemail@gmail.com')
    with pytest.raises(InputError):    
        auth_password_reset(1, 'hello123')