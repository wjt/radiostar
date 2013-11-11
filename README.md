A tiny Twitter archiver. Scrapes a user's timeline; and produces a CSV from it.
Includes retweet and favourite counts, which the Twitter archive does not.

* `pip install -r requirements.txt`
* Get Twitter API keys from <https://dev.twitter.com/apps/>
* Plug 'em into `tokens.py`
* Run `python oauth.py grab USERNAME`
* When it's done, run `python csvify.py`
