# Python Programming Test

## Your Task: A News Search Engine
Your task is to write an application that, when executed, prompts the user for an arbitrary topic (free text defined by the user) and subsequently searches the web for suitable recent news articles that fit the given topic. 

You may use any 3rd API to retrieve news content and don’t have to implement your own indexing/search or database system. 

The output of your application should consist of the following: 
a) the list of titles, URLs and publication dates of the top-15 matching news articles from (at least) the last month and sorted by relevancy w.r.t. the given topic; 
b) a csv file containing the full list of titles, URLs and publication dates of matching articles from (at least) the last month (the file should be written right after search); and 
c) an automatically generated summary (you may use another 3rd party API or library) of the (top-15) article headlines, along with a list of all named entities mentioned in the (top-15) article headlines, sorted by frequency.

User prompts and outputs may be given on the commandline or via other means (no need to implement a UI or web interface). However, users should be able to search multiple times (for different topics) at runtime.
The overall project should contain a simple README (with installation and execution specifics) and a requirements file. Do **NOT use Conda**. Instead, use Python **venv** for your work and instructions in the README.

## Hints
* If you use a secret key to access a third party API, don't submit your secret key, but add an explanation how to get a new one.

## Bonus points for:
* Ability to choose language before search (e.g. German and English), to limit results to a particular language.
* Unit Tests
