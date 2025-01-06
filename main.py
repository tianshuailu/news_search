from retrieval import retrieve_news


def get_language() -> str:
    # Get the language from the user.
    while True:
        lang = input("Enter the language you want to search for news in. Please enter 'en' for English, or 'de' for German: ").lower()
        if lang in ["en", "de"]:
            return lang
        else:
            print("The input language is not supported yet. Please try again.")

def get_topic() -> str:
    # Get the topic from the user.
    while True:
        topic = input("Please describe the news topic in the language you chose: ")
        if topic:
            return topic
        else:
            print("Seems like you didn't type a topic.")

def main():
    print("Welcome to the News Search Engine.")
    while True:
        lang = get_language()
        print(f"Language selected: {lang}")

        topic = get_topic()
        print("Searching for news...")

        summary, keywords = retrieve_news(topic, lang)
        print(f"A summary of the news headlines: \n{summary}")
        print(f"Full list of named entities in the news headlines sorted by frequency: \n{keywords}")

        input_ = input("Do you want to search for news on another topic or language? (yes/no): ")
        if input_.lower() != "yes":
            print("Thank you for using the News Search Engine.")
            break


if __name__ == "__main__":
    main()