from flask import Blueprint, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_required
from database.models import User, Posts
from resources.mail import send_auth_email
import logging
from mongoengine.queryset.visitor import Q
import os
import datetime
from time import strftime
from pytz import timezone
from app import ckeditor

news = Blueprint('news', __name__, template_folder='templates')

@news.route('/')
@news.route('/news', methods=('GET', 'POST'))
def index():
    posts = Posts.objects.filter(status='live')
    post_list = []
    for post in reversed(posts):
        post_list.append({'title': post.title, 'body': post.body[0:500], 'username': post.username, 'created': post.created, 'keywords':post.keywords, 'authorid':post.authorid, 'id': post.id})
    return render_template('news.html', posts = post_list)


@news.route('/news/create', methods=('GET', 'POST'))
@jwt_required()
def create():
    if request.method == 'POST':
        est = timezone('US/Eastern')
        dt = datetime.datetime.now(tz=est)
        time_str = dt.strftime('%H:%M')
        d3 = dt.strftime('%m/%d/%y')
        d4 = dt.strftime('%m/%d/%y, %H:%M:%S')
        post = Posts()
        user = User.objects.get(id=get_jwt_identity())
        post.title = request.form['title']
        post.body = request.form.get('ckeditor')
        post.username = user.dispatcherid
        post.authorid = "Quiet Corner Alerts"
        post.created = d4
        keywords = []
        form_keywords = request.form['keywords'].split('#')
        for word in form_keywords:
            stripped = word.strip()
            if stripped != '':
                keywords.append(stripped)
        post.keywords = keywords
        post.status = 'draft'
        post.save()
        return redirect('/news/drafts')
    return render_template('create.html')

@news.route('/news/drafts', methods=('GET', 'POST'))
@jwt_required()
def drafts():
    user = User.objects.get(id=get_jwt_identity())
    posts = Posts.objects.filter((Q(status='draft') & Q(username=user.dispatcherid)))
    post_list = []
    for post in reversed(posts):
        post_list.append({'title': post.title, 'body': post.body, 'authorid':post.authorid, 'username': post.username, 'created': post.created, 'id': post.id, 'keywords':post.keywords})
    return render_template('drafts.html', posts=post_list, username=user.dispatcherid)

@news.route('/news/post/<id>')
@jwt_required()
def post(id):
    print(id)
    posts = Posts.objects.filter(id=id)
    for post in posts:
        print(post.status)
        post.status = 'live'
        post.save()
        print(post.status)
    return redirect(url_for('news.drafts'))

@news.route('/article/<id>')
def article(id):
    print(id)
    posts = Posts.objects.filter(id=id)
    post_list = []
    for post in posts:
        post_list.append(
            {'title': post.title, 'body': post.body, 'username': post.username, 'created': post.created,
             'keywords': post.keywords, 'authorid': post.authorid, 'id': post.id})
    print(post_list)
    return render_template('article.html', posts=post_list)