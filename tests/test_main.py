import sys
import io
from main import get_language, get_topic

def test_get_language():
    # test the get_language function
    sys.stdin = io.StringIO("en\n")
    lang = get_language()
    assert lang == "en"

    sys.stdin = io.StringIO("de\n")
    lang = get_language()
    assert lang == "de"

def test_get_topic():
    # test the get_topic function
    sys.stdin = io.StringIO("I want to know about the latest news on Taylor Swift's Eras Tour ending.\n")
    topic = get_topic()
    assert topic == "I want to know about the latest news on Taylor Swift's Eras Tour ending."
