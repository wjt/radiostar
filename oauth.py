#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import tweepy
import time
import codecs
import os
import sys

# Should contain the four fields used in sign_in()
import tokens

from tweepy.utils import import_simplejson
json = import_simplejson()

TWEET_DIR = os.path.join('tweets', '%s')

def sign_in():
    auth = tweepy.OAuthHandler(tokens.consumer_key, tokens.consumer_secret)
    auth.set_access_token(tokens.access_token, tokens.access_token_secret)

    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    print "Logged in as %s" % api.me()
    return api

def grab_tweets_with(api, username, since_id=None, max_id=None):
    for i in range(0, 200):
        print "request %d (since_id=%s, max_id=%s)" % (i, since_id, max_id)

        page = api.user_timeline(username, count=200, max_id=max_id, since_id=since_id)

        if not page:
            print "no more tweets here!"
            break

        for status in page:
            id = status['id']
            print "  %d" % id
            with codecs.open(os.path.join(TWEET_DIR, '%s.json') % (username, id),
                             mode='w', encoding='utf-8') as f:
                json.dump(status, f)

        max_id = page[-1]['id'] - 1
        time.sleep(10)

def grab_tweets(api, username):
    try:
        tweet_ids = [int(os.path.splitext(filename)[0])
                     for filename in os.listdir(TWEET_DIR % username)
                     if filename.endswith(".json")
                    ]
    except OSError, e:
        os.makedirs(TWEET_DIR % username)
        tweet_ids = []

    if tweet_ids:
        bottom = min(tweet_ids)
        top = max(tweet_ids)
    else:
        bottom = None
        top = None

    print "Grabbing new tweets since %s…" % top
    grab_tweets_with(api, username, since_id=top)

    print "Grabbing old tweets before %s…" % bottom
    grab_tweets_with(api, username, max_id=bottom)

commands = {
    'grab': grab_tweets,
}

def usage():
    print "usage:"
    for subcommand in commands.keys():
        print "  %s %s USERNAME" % (sys.argv[0], subcommand)
    sys.exit(1)

if __name__ == '__main__':
    try:
        command, username = sys.argv[1:]
        func = commands[command]
    except IndexError:
        usage()
    except KeyError:
        usage()
    except ValueError:
        usage()

    api = sign_in()
    func(api=api, username=username)
