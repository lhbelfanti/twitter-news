import constants
import markovify
from markov_chain import SpacyText


class MarkovChain:

    def execute(self, text):
        # Build the model.
        text_model = SpacyText(text)  # markovify.Text(text)

        body = ""
        sentences = []
        # Create randomly-generated sentences
        for i in range(constants.SENTENCES_TO_GENERATE):
            sentence = text_model.make_sentence()
            if sentence is not None and sentence not in sentences:
                body += sentence
                sentences.append(sentence)

        return body
