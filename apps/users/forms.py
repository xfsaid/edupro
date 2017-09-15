# -*- coding: utf-8  -*-
__author__ = 'said'
__date__ = '2017/9/15 1:48'
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)
