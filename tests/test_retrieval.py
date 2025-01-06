from retrieval import news_api_request, model_api_request, retrieve_news, get_keywords

def test_news_api_request():
    # test the news_api_request function
    json_data = news_api_request("Taylor Swift + Eras Tour + End Date", "en", 1)
    assert type(json_data) == dict
    assert "data" in json_data.keys()

def test_model_api_request():
    # test the model_api_request function
    model_input = """After 149 shows across five continents, Taylor Swift's Eras Tour came to a close last night in Vancouver. Here's how the internet reacted.
    Taylor Swift took the stage for her final Eras Tour concert in Vancouver, Canada, on Sunday, December 8.
    Taylor Swift ended her Eras Tour on Sunday, December 8, performing in Vancouver, Canada."""
    summary = model_api_request(model_input, getSummary=True)
    assert type(summary) == str

    model_input = "I want to know about the latest news on Taylor Swift's Eras Tour ending."
    search_term = model_api_request(model_input, getSummary=False)
    assert type(search_term) == str

def test_get_keywords():
    # test the get_keywords function
    keywords = get_keywords("Taylor Swift's Eras Tour came to a close last night in Vancouver. Here's how the internet reacted.", "en")
    assert type(keywords) == list
    assert len(keywords) > 0

def test_retrieve_news():
    # test the retrieve_news function
    user_input = "I want to know about the latest news on Taylor Swift's Eras Tour ending."
    summary, keywords = retrieve_news(user_input, "en")
    assert type(summary) == str
    assert type(keywords) == list
    assert len(keywords) > 0