import markovify

from markov_chain import SpacyText


class MarkovChain:
    def __init__(self, config):
        self.config = config

    def execute(self, text):
        # Build the model.
        activate_nlp = self.config.get("activate_nlp")
        if activate_nlp:
            SpacyText.load_dict()
            text_model = SpacyText(text)
        else:
            text_model = markovify.Text(text)

        body = ""
        sentences = []
        # Create randomly-generated sentences
        sentences_to_generate = self.config.get("sentences_to_generate")
        for i in range(sentences_to_generate):
            sentence = text_model.make_sentence()
            if sentence is not None and sentence not in sentences:
                body += sentence
                sentences.append(sentence)

        return body
