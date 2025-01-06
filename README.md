# News Search Engine

The News Search Engine takes user input and searches relevant news articles from the past month. It also allows the user to select the language of the news content.

## Installation Guide
First create a python virtual environment in the project folder, then install the required packages by running the command:
```sh
pip install -r requirements.txt
```

Please also install spacy models with the following commands
```sh
python -m spacy download en_core_web_md
```
and
```sh
python -m spacy download de_core_news_md
```

## API Keys
The app takes advantage of a news API and a model API, please get the news API key from https://www.thenewsapi.com/ and put it in file retrieval.py line 14, also model API key from https://www.arliai.com/ and put it in file retrieval.py line 68

## Run the App
To run the app, run the following command in the project folder and then follow the instructions.
```sh
python main.py
```

## Unit Tests
To run the unit tests, run the following command in the project folder
```sh
pytest
```
