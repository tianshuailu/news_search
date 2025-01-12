import http.client, urllib.parse, urllib.request
import json
import pandas as pd
import requests
import spacy
import sys
from  datetime import datetime, timedelta


def news_api_request(search_term: str, lang: str, page_number: int) -> dict:
    conn = http.client.HTTPSConnection('api.thenewsapi.com')

    # add your API token here, you can get it for free at https://www.thenewsapi.com/
    API_token = "Y8VdjfCTRnO32U1rSy2pQJfKvTmaXZK7PtmIvCzS"
    last_month = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    params = urllib.parse.urlencode({
        'api_token': API_token,
        'search': search_term,
        'language': lang,
        'published_after': last_month,
        'page': page_number,
        })

    for _ in range(3):
        try:
            conn.request('GET', '/v1/news/all?{}'.format(params))
            break
        except:
            pass
    else:
        print("Failed to connect to the news API, please try again later.")
        sys.exit(1)

    res = conn.getresponse()
    news_data = res.read().decode('utf-8')
    json_data = json.loads(news_data)

    return json_data


def model_api_request(model_input: str, getSummary=False, lang='en') -> str:
    # if getSummary is True, model input is headlines, else it is the user input
    lang = 'English' if lang == 'en' else 'German'
    if getSummary:
        systemPrompt = f"You are a helpful assistant. You will summarize the following news headlines with no more than 3 sentences. You will only reply with the summary in {lang}."
    else:
        systemPrompt = f"You are a helpful assistant. You will summarize the user input with no more than 3 keywords. You will only reply with the keywords in {lang}."
    
    url = "https://api.arliai.com/v1/chat/completions"

    payload = json.dumps({
    "model": "Mistral-Nemo-12B-Instruct-2407",
    "messages": [
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi!, how can I help you today?"},
        {"role": "user", "content": model_input},
    ],
    "repetition_penalty": 1.1,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_tokens": 1024,
    "stream": False
    })

    # add your API key here, you can get it for free at https://www.arliai.com/
    ARLIAI_API_KEY = "2f65bfc7-f1a1-4911-98ea-01f892a6e52b"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {ARLIAI_API_KEY}"
    }
    
    for _ in range(3):
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            break
        except:
            pass
    else:
        print("Failed to connect to the model API, please try again later.")
        sys.exit(1)
        
    if response.status_code == 500:
        print("Failed to connect to the model API, please try again later.")
        sys.exit(1)
    
    # get model output from the response, a string that could be a summary or keywords separated by commas
    output = json.loads(response.text)['choices'][0]['message']['content']

    if getSummary:
        return output
    
    # concatenate the keywords with a "+" sign to match the url format
    search_term = " + ".join(output.split(","))

    return search_term


def get_keywords(headlines: str, lang: str) -> list:
    # use spacy for named entity recognition
    # return the keywords
    if lang == "en":
        nlp = spacy.load("en_core_web_md")
    else:
        nlp = spacy.load("de_core_news_md")
    doc = nlp(headlines)

    keywords = set([t.text for t in doc.ents])
    counter = {}
    for w in keywords:
        counter[w] = headlines.count(w)
    sorted_counter = sorted(counter.items(), key=lambda pair: pair[1], reverse=True)
    sorted_keywords = [pair[0] for pair in sorted_counter]
    return sorted_keywords
    

def retrieve_news(user_input: str, lang: str) -> tuple[str, list]:

    search_term = model_api_request(user_input)
    print(f"Searching for news articles on {search_term}...")
    # page_number starts at 1 and increase after each request until we have 15 news articles or there are no more articles
    page_number = 1

    # we want to make sure each url returned is valid and can be accessed
    # max_try is the number of times we try the news article url before moving to the next article
    max_try = 1

    result_list = []
    headline_list = []

    # get the news articles with the news api
    while True:
        json_data = news_api_request(search_term, lang, page_number)
        page_number += 1
        
        # if there are no more news articles in the page, break the loop
        if ('data' not in json_data) or (json_data['data'] == []):
            break

        for news_article in json_data['data']:
            for _ in range(max_try):
                try:
                    requests.get(news_article['url'], timeout=5)
                    headline_list.append(news_article['description'])
                    news_article = {key: news_article[key] for key in ['title', 'url', 'published_at']}
                    news_article['published_at'] = news_article['published_at'][:10]
                    result_list.append(news_article)
                    break
                except:
                    pass
        
        # Due to the limit of the API, we only get around 30 news articles for each search term
        if len(result_list) >= 6:
            break
    
    if len(result_list) < 15:
        print(f"{len(result_list)} news articles were found on this ropic, and have been written to a csv file named {search_term.replace(' ', '')}.csv.")
    else:
        print(f"Here is the top 15 most relevant news articles and a full list of all {len(result_list)} articles have been written to a csv file named {search_term.replace(' ', '')}.csv.")

    """
    df = pd.DataFrame(result_list)
    df = df[['title', 'url', 'published_at']]
    # change the date format to only include the date without the time
    df['published_at'] = df['published_at'].map(lambda date: date[:10])
    # save all the news url to a csv file
    df.to_csv(search_term.replace(" ", "")+'.csv', index=False)

    # print the top 15 news articles
    df = df.head(15)
    print(df.to_string())
    """
    # get the summary of the news headlines
    summary = model_api_request("\n".join(headline_list), getSummary=True)
    
    # get the named entities from the news headlines
    keywords = get_keywords("\n".join(headline_list), lang)
    
    return summary, keywords, result_list