#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import datetime
import codecs
import os
import sys
import json
import unicodecsv as csv

fields = ('url', 'created_at', 'text', 'retweet_count', 'favorite_count', 'hashtags')

def csvify(username):
    directory = 'tweets/%s' % username
    tweet_ids = [filename
                 for filename in os.listdir(directory)
                 if filename.endswith(".json")
                ]
    tweet_ids.sort()

    with open('tweets/%s.csv' % username,
              mode='w') as f:
        stats_writer = csv.DictWriter(f, fields)
        stats_writer.writeheader()

        for tweet_filename in tweet_ids:
            with codecs.open(os.path.join(directory, tweet_filename),
                             mode='r', encoding='utf-8') as t:
                tweet = json.load(t)
                if 'retweeted_status' in tweet:
                    print "Skipping '%s'" % tweet_filename
                    continue

                # "created_at" : "Thu May 31 08:50:01 +0000 2012",
                created_at = tweet['created_at']
                # created_at = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y').isoformat()
                #     ValueError: 'z' is a bad directive in format '%a %b %d %H:%M:%S %z %Y'
                created_at = created_at[0:len("Thu May 31 08:50:01 ")] + created_at[len("Thu May 31 08:50:01 +0000 "):]
                created_at = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %Y').isoformat().replace('T', ' ')

                stats_writer.writerow({ 'url': 'https://twitter.com/%s/status/%s' % (username, tweet['id_str']),
                                        'created_at': created_at,
                                        'text': tweet['text'].replace('&amp;', '&'),
                                        'retweet_count': tweet['retweet_count'],
                                        'favorite_count': tweet['favorite_count'],
                                        'hashtags': ' '.join(h['text'] for h in tweet['entities']['hashtags']),
                                      })

if __name__ == '__main__':
    csvify(sys.argv[1])
