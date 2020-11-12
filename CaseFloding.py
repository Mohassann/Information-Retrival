
"""
Provided by analyzers-icu API
https://lucene.apache.org/core/4_1_0/analyzers-icu/overview-summary.html

Text Segmentation: Tokenizes text based on properties and rules defined in Unicode.
Collation: Compare strings according to the conventions and standards of a particular language, region or country.
Normalization: Converts text to a unique, equivalent form.
Case Folding: Removes case distinctions with Unicode's Default Caseless Matching algorithm.
Search Term Folding: Removes distinctions (such as accent marks) between similar characters for a loose or fuzzy search.
Text Transformation: Transforms Unicode text in a context-sensitive fashion: e.g. mapping Traditional to Simplified Chinese
"""


#  Accent removal
#  Case folding
#  Canonical duplicates folding
#  Dashes folding
#  Diacritic removal (including stroke, hook, descender)
#  Greek letterforms folding
#  Han Radical folding
#  Hebrew Alternates folding
#  Jamo folding
#  Letterforms folding
#  Math symbol folding
#  Multigraph Expansions: All
#  Native digit folding
#  No-break folding
#  Overline folding
#  Positional forms folding
#  Small forms folding
#  Space folding
#  Spacing Accents folding
#  Subscript folding
#  Superscript folding
#  Suzhou Numeral folding
#  Symbol folding
#  Underline folding
#  Vertical forms folding
#  Width folding

# the ICUFolding provided by
# https://github.com/fish2000/pylucene/blob/master/python/ICUFoldingFilter.py

import os, lucene,sys


from org.apache.lucene.analysis.icu  import ICUNormalizer2Filter
from org.apache.lucene.analysis.icu import ResourceBundle, Normalizer2, UNormalizationMode2

utr30 = os.path.join(lucene.__dir__, 'resources', 'org', 'apache', 'lucene', 'analysis', 'icu', 'utr30.dat')
ResourceBundle.setAppData("utr30", utr30)


class ICUFoldingFilter(ICUNormalizer2Filter):

    def __init__(self, input):

        normalizer = Normalizer2.getInstance("utr30", "utr30", UNormalizationMode2.COMPOSE)
        super(ICUFoldingFilter, self).__init__(input, normalizer)
