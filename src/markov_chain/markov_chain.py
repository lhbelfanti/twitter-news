import markovify
from config import Configuration
from markov_chain import SpacyText


class MarkovChain:

    def execute(self, text):
        # Build the model.
        if Configuration.config["activate_nlp"]:
            SpacyText.load_dict()
            text_model = SpacyText(text)
        else:
            text_model = markovify.Text(text)

        body = ""
        sentences = []
        # Create randomly-generated sentences
        for i in range(Configuration.config["sentences_to_generate"]):
            sentence = text_model.make_sentence()
            if sentence is not None and sentence not in sentences:
                body += sentence
                sentences.append(sentence)

        return body
