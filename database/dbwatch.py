from flask import Blueprint, request, render_template, redirect, url_for
from database.models import User, Calls

def dbwatch():
    while True:
        cursor = Calls.watch()
        document = next(cursor)
        print(document)