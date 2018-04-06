# I-m-Feeling-Lucky
Alexa web search skill

## About the skill:

```
Its your daily scenario with Alexa. 
you have a question, you just ask alexa and find the answer. 
The only difference is, I am feeling lucky looksup online like 
your favourite search engines and finds the best webpage out there. 
It condenses the content from this page and reads it out, 
keeping your web search experience the closest 
to how you normally do on your "screen devices".
```
To invoke the skill, you can say:

`Alexa, open I'm Feeling Lucky` after which you can prompt it with any search query, say
`Search for Sea dragons` 

(*sea dragons are cute creatures, you should google them if you haven't)

Here are some examples. Open I am feeling lucky and try these queries:

`lookup how do fashion designers gain fame when they start out?`
`search for Why do people talk in their sleep?`
`lookup How do people know what vitamins they are lacking?`

The conversations are designed in such a way that you have to use the words `lookup` or `search for` followed by your query to get proper results.

This version of the code is still buggy in my opinion and doesn't produce a great experience yet. But, its a good start.

## Issues:

1. The basic method of search is using `pygoogling` which scrapes google for the lucky link. We need to go employ better methods than scraping, that is still cheap to do. Any ideas?

2. Using a simple summarization algorithm (Luhn's algorithm) when `newspaper` is unable to extract a summary from the webpage. Luhn's algo is old and doesn't produce great results by current standards. I need to work here.

3. The problem with using TextRank based python libs or more advanced summarizers are, they depend on a bulky dataset, which sizes up the code bundle and Lambda functions are not designed to handle large bundles. Zappa threw error for a 90MB bundle upload.

4. Newspaper has issues loading in Lambda, this PR solves it. To incorporate this PR, had to pip install the development version from github. 

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
