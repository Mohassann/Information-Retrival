#!/usr/bin/env python

INDEX_DIR = "IndexFiles"
import re
import sys, os, lucene, threading, time
from datetime import datetime
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.store import MMapDirectory

"""
This class is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

# Ticker function provided by https://github.com/fnp/pylucene/blob/master/samples/IndexFiles.py
#  You can use tick when you work with times, and for converting between representations.
#  also tick is an iteration of some loop
class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush() # it collects some of the data "written" to standard out before it writes it to the terminal
            time.sleep(1.0)


# the IndexFiles class provided by:
# https://github.com/adham-elsabbagh/IR_Assignment
# https://github.com/fish2000/pylucene/blob/master/samples/IndexFiles.py
# https://stackoverflow.com/questions/42308801/python-lucene-function-add-field-contents-to-document-not-working

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        #  same for all the indexing procedures
        Storing = MMapDirectory(Paths.get(storeDir)) # As it is also mentioned by the apache that better to use MMapDirectory instead of the SimpleFSDirectory
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)  # Limiting the number of the Tokens while indexing
        Configure = IndexWriterConfig(analyzer)  # configurations that are used for creating the IndexWriter
        Configure.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        index_witer = IndexWriter(Storing, Configure)

        self.indexDocs(root, index_witer)
        ticker = Ticker()
        print ('commit index',)

        threading.Thread(target=ticker.run).start()
        index_witer.commit()
        index_witer.close()
        ticker.tick = False
        print('Done')


# the indexDocs function provided by both
# https://github.com/adham-elsabbagh/IR_Assignment
# https://github.com/fish2000/pylucene/blob/master/samples/IndexFiles.py

    def indexDocs(self, root, writer):

        x = FieldType()
        x.setStored(True)
        x.setTokenized(False)
        x.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        y = FieldType()
        y.setStored(True)
        y.setTokenized(True)
        y.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        #  Adding the cleaned data to the same file (overwriting)
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.xml'):
                    continue
                print ("adding", filename)

                try:
                    path = os.path.join(root, filename)
                    Doc = open(path)
                    Contents = Doc.read()

                    Doc.close()
                    doucments = Document()
                    doucments.add(Field("name", filename, x))
                    doucments.add(Field("path", root, x))

                    if len(Contents) > 0:
                        doucments.add(Field("contents", Contents, y))

                    else:
                        print ("Warning: no content in %s" % filename)
                    writer.addDocument(doucments)
                except Exception as e:
                    print ("Failed in indexDocs:", e)




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print (IndexFiles.__doc__)
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),StandardAnalyzer())
        end = datetime.now()
        print (end - start)
    except Exception as e:
        print ("Failed: ", e)
        raise e
