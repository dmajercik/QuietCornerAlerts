from flask import Blueprint, request, render_template, redirect, url_for
from database.models import User, Chat
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_required
from datetime import date
import datetime
from time import strftime
import logging
from pytz import timezone
import mongoengine
from mongoengine.queryset.visitor import Q



@cad.route('/chat')
@jwt_required()
def chat():
    chatlog = Chat.objects()
    chat_data = []
    for msg in chatlog():
        messageline = [Chat.dispatcher, Chat.message]
        chat_data.append(messageline)