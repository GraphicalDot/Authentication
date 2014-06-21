# -*- coding: utf-8 -*-
import os

from flask import Config

# Debug Mode
DEBUG = True
DEBUG_HOST = '0.0.0.0'
DEBUG_PORT = 8080

# MongoDB config
# TODO: move to flask-pymongo
MONGODB_DB = 'bangology'
MONGODB_USERS_COLLECTION = 'users'

# AWS Details (for SES)
AWS_ACCESS_KEY = 'AKIAJ3DV7FPGXTSLWWEA'
AWS_ACCESS_SECRET = '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'

# Invite E-Mails
INVITE_MAIL_SOURCE = 'Rishabh Verma <rishabh95verma@gmail.com>'
INVITE_MAIL_SUBJECT = 'Just another banging eMail.'

# GCM Details
AUTHORIZATION_KEY= 'AIzaSyAgcWUZk26CoMQG7l3fBwPxBn-1KkXyJ24'
GCM_URL= 'https://android.googleapis.com/gcm/send'
