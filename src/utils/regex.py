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


def get_cashtags(text):
    cashtags = []
    if not text or text.find('$') == -1:
        return cashtags

    cashtag_string = r'(?:\$[a-zA-Z]{1,6}([._][a-zA-Z]{1,2})?)'
    cashtag_re = re.compile(cashtag_string, re.VERBOSE | re.I | re.UNICODE)
    iterator = cashtag_re.finditer(text)

    for match in iterator:
        cashtags.append(match.group())

    return cashtags
