import configparser
from fastapi import APIRouter, Response

config = configparser.RawConfigParser()
configFilePath = [r'secret.config', r'QCA.config']
config.read(configFilePath)


class Keys:
    def __init__(self):
        # twitter keys and setup for @quietcorneralrt
        self.twitter_consumer_key = config.get('key','twitter_consumer_key')
        self.twitter_consumer_secret = config.get('key', 'twitter_consumer_secret')
        self.twitter_access_token = config.get('key', 'twitter_access_token')
        self.twitter_access_token_secret = config.get('key', 'twitter_access_secret')
        # twitter keys and setup for @QCA_National
        self.QCAnational_twitter_consumer_key = config.get('key', 'QCAnational_twitter_api_key')
        self.QCAnational_twitter_consumer_secret = config.get('key', 'QCAnational_twitter_api_secret')
        self.QCAnational_twitter_access_token = config.get('key', 'QCAnational_twitter_access_token')
        self.QCAnational_twitter_access_token_secret = config.get('key', 'QCAnational_twitter_access_secret')
        # facebook key and setup
        # this token expires on 172sep2!!!
        facebook_token = config.get('key', 'facebook_token')


class Cad:
    def new_incident(self):
        pass

