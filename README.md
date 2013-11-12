A tiny Twitter archiver. Downloads a user's timeline; and, in a separate program, produces a CSV from it. The former may be useful without the latter.
Includes retweet and favourite counts, which the Twitter archive does not.

* `pip install -r requirements.txt`
* Get Twitter API keys from <https://dev.twitter.com/apps/>
* Plug 'em into `tokens.py`
* Run `python oauth.py grab USERNAME`
* When it's done, run `python csvify.py`
