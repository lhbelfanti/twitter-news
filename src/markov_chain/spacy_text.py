import markovify
import spacy
from logger import Logger


class SpacyText(markovify.Text):

    dict_loaded = False
    nlp = None

    @staticmethod
    def load_dict():
        if not SpacyText.dict_loaded:
            Logger.info("----------------------------------------")
            Logger.info("Loading NLP module...")
            SpacyText.nlp = spacy.load("es")
            SpacyText.dict_loaded = True
            Logger.info("NLP module loaded")
            Logger.info("----------------------------------------")

    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in SpacyText.nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
