import re


def get_tweets_number(text):
    splitted = text.split(' ')
    pattern = re.compile("(\d*[,.]\d*)[a-zA-Z]*")

    return_data = {"stats": False, "data": text}
    if pattern.match(splitted[0]):
        return_data["stats"] = True
        return_data["data"] = splitted[0]

    return return_data


def add_dot_at_the_end(text):
    last_character = text[-1:]
    if last_character == ".":
        return text + "."

    return text
