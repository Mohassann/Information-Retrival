INDEX_DIR = "IndexFiles"
FIELD_CONTENTS = "contents"

import sys, os, lucene
from spellchecker import SpellChecker
from org.apache.lucene.store import MMapDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.pylucene.search.similarities import PythonClassicSimilarity
from org.apache.lucene.search import \
    BooleanClause, BooleanQuery, Explanation, PhraseQuery, TermQuery
from org.apache.pylucene.search import PythonSimpleCollector
from org.apache.lucene.search.similarities import BM25Similarity, ClassicSimilarity
from org.apache.lucene.util import BytesRef, BytesRefIterator
import os, lucene

import inquirer
import re
import lucene
from os import path, listdir
import numpy
import math
from lucene import *
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.search.highlight import SimpleSpanFragmenter
from org.apache.lucene.search.highlight import QueryScorer
from org.apache.lucene.search.highlight import Highlighter
from java.io import StringReader

"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


# some of the code of the run function is provided by https://github.com/fnp/pylucene/blob/master/samples/SearchFiles.py
# we added spell checking manually using spellchecker library
# user can Enter any query - but if one of the words in the query string is misspelled,
# the user will get warning with a list of candidate words, which the user can choose from it.


def run(searcher, analyzer):
    while True:

        spell = SpellChecker()  # loads default word frequency list
        print("------- Press Enter to quit OR -------")
        print ("")
        input_query = raw_input("Enter Document Title: ")
        wordlist = input_query.split()

        #  same as Case Folding Makes the Query case insensitive
        wordlistt = [x.lower() for x in wordlist]
        # print wordlistt
        Processed_query = ' '.join(wordlistt[:])

        # checking the misspelled words and suggesting the correct word
        # find those words that may be misspelled
        misspelled = list(spell.unknown(wordlist))
        print("Misspelled words in your Query : ", misspelled)
        for word in misspelled:
            candidates = spell.candidates(word)
            print (" Candidate word:  ", candidates)

        # searching for the query and finding the documents that contain the query
        if Processed_query:
            print("Searching for documents that contains the query:", Processed_query)
            relevant_query = QueryParser("contents", analyzer).parse(Processed_query)
            scoreDocs = searcher.search(relevant_query, 1500).scoreDocs
            Inputquery_scoreDocs = []

            # getting the name of the document that contain the matching query
            for scoreDoc in scoreDocs:
                documents = searcher.doc(scoreDoc.doc)
                Inputquery_scoreDocs.append(documents.get("name"))
                score = scoreDoc.score  # score is the the closeness of each hit to our query
                document_id = scoreDoc.doc

                HighlightFormatter = SimpleHTMLFormatter()
                query_score = QueryScorer(relevant_query)
                highlighter = Highlighter(HighlightFormatter, query_score)
                # Set the fragment size. We break text in to fragment of 64 characters
                fragmenter = SimpleSpanFragmenter(query_score, 64)
                highlighter.setTextFragmenter(fragmenter)
                text = documents.get(FIELD_CONTENTS)
                # ts = analyzer.tokenStream(FIELD_CONTENTS, StringReader(text))
                print('path:', documents.get("path"), 'name:', documents.get("name"), 'score: ', score, 'Doc ID :',
                        document_id)
            list_relevant = '\n'.join(Inputquery_scoreDocs)

            # adding the retrieved document names and the query in to two different file
            with open('Name of the Retrieved Documents.txt', 'w') as ouput:
                ouput.write(list_relevant)
            # with open('Retrieved Document content.txt', 'w') as ouput:
            #     ouput.write(text)

            print ("")
            print("%s Total number of retrieved documents." % len(scoreDocs))
            print ("")

        #  shows a warning if the user entered a misspelled word
        if len(misspelled) == 0:
            print ("--- The Spelling of all the Words are in the input query is correct---")
        else:
            print (' --- Correct the misspelled Word/Words --- ', misspelled)
            print ('Do you meant', misspelled, 'if not you can choose from the suggested words above')

        if input_query == '':  # not sure, but need a way to kill the program...
            return


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = MMapDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    searcher.setSimilarity(BM25Similarity())
    analyzer = StandardAnalyzer()

    run(searcher, analyzer)
    del searcher
