# Copyright (C) 2001-2020 NLTK Project
# Author: Steven Bird <stevenbird1@gmail.com>
#         Edward Loper <edloper@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

from nltk.corpus.reader.wordnet import NOUN
from nltk.corpus import wordnet

#  The WordNetLemmatizer Class is also provided by https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
#  https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
#  More info on the WordNet can be found on https://www.nltk.org/howto/wordnet.html


class WordNetLemmatizer(object):
    """
    WordNet Lemmatizer

    Lemmatize using WordNet's built-in morphy function.
    Returns the input word unchanged if it cannot be found in WordNet.

        >>> from nltk.stem import WordNetLemmatizer
        >>> wnl = WordNetLemmatizer()
        >>> print(wnl.lemmatize('dogs'))
        dog
        >>> print(wnl.lemmatize('churches'))
        church
        >>> print(wnl.lemmatize('aardwolves'))
        aardwolf
        >>> print(wnl.lemmatize('abaci'))
        abacus
        >>> print(wnl.lemmatize('hardrock'))
        hardrock
    """

    def __init__(self):
        pass
    # morphy checks for suffix and ending of the given query, in an intelligent manner to translate the given query to the base words mentioned in the wordNet.
    def lemmatize(self, word, pos):
        lemmas = wordnet._morphy(word, pos)
        return min(lemmas, key=len) if lemmas else word

    def __repr__(self):
        return "<WordNetLemmatizer>"



# unload wordnet
def teardown_module(module=None):
    from nltk.corpus import wordnet

    wordnet._unload()
