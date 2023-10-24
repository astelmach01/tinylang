from typing import Literal, Union

from tinylang.functions import function


@function
def get_current_weather(location: str, format: Union[Literal["celsius", "fahrenheit"]]):
    "Get the current weather"


@function
def get_n_day_weather_forecast(
    location: str, format: Union[Literal["celsius", "fahrenheit"]], num_days: int
):
    "Get an N-day weather forecast"


def test_get_current_weather():
    expected = {
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "format": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location", "format"],
        },
    }
    assert get_current_weather == expected


def test_get_n_day_weather_forecast():
    expected = {
        "name": "get_n_day_weather_forecast",
        "description": "Get an N-day weather forecast",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "format": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                "num_days": {"type": "integer"},
            },
            "required": ["location", "format", "num_days"],
        },
    }
    assert get_n_day_weather_forecast == expected


def test_get_articles_function():
    paper_dir_filepath = "arxiv_library.csv"

    @function
    def get_articles(query: str, library: str = paper_dir_filepath, top_k: int = 5):
        """This function gets the top_k articles based on a user's query, sorted by relevance.
        It also downloads the files and stores them in arxiv_library.csv to be retrieved
        by the read_article_and_summarize.
        """

    expected = {
        "name": "get_articles",
        "description": "This function gets the top_k articles based on a user's query,"
        " sorted by relevance.\n        It also downloads the files and "
        "stores them in arxiv_library.csv to be retrieved by the "
        "read_article_and_summarize.\n        ",
        "parameters": {
            "properties": {
                "query": {"type": "string"},
                "library": {"default": "arxiv_library.csv", "type": "string"},
                "top_k": {"default": 5, "type": "integer"},
            },
            "required": ["query"],
            "type": "object",
        },
    }
    assert get_articles == expected


def test_read_article_and_summarize_function():
    @function
    def read_article_and_summarize(query: str):
        """Use this function to read whole papers and provide a summary for users.
        You should NEVER call this function before get_articles
        has been called in the conversation.
        """

    expected = {
        "name": "read_article_and_summarize",
        "description": "Use this function to read whole papers and provide a "
        "summary for users.\n "
        "       You should NEVER call this function before get_articles has "
        "been called in the conversation.\n        ",
        "parameters": {
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
            "type": "object",
        },
    }
    assert read_article_and_summarize == expected
