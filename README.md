# I-m-Feeling-Lucky
Alexa search skill


Issues:

Newspaper has issues loading in Lambda, this PR solves it:

https://github.com/codelucas/newspaper/pull/532

```
# only /tmp is writable on lambda env
os.environ['NEWSPAPER_BASE_DIRECTORY'] = '/tmp'
os.environ['NLTK_DATA'] = '/tmp'

# https://stackoverflow.com/a/44532317/2523414
# no sqlite in lambda, needed by a small subset of nltk
import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")

from newspaper import Article
import nltk
```
