from types import SimpleNamespace

default_emojis = {
    "like": "\U0001F44D",
    "dislike": "\U0001F44E",
    "channel": "\U0001F39E",
    "created": "\U0001F4C5",
    "country": "\U0001F30D",
    "title": "\U0001F4DA",
    "url": "\U0001F517",
    "duration": "\U0001F551",
    "subscribers": "\U0001F4E2",
    "views" : "\U0001F441"
}

emojis = SimpleNamespace(**default_emojis)