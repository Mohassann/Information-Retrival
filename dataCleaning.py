# coding=utf-8
import os,re,sys


#  the cleaning data also Provided by https://github.com/adham-elsabbagh/IR_Assignment/blob/master/parser.py
# we add some of the codes to our Parser file based on our given dataset

def cleaning_data():
    x=[]
    for filename in os.listdir(dir):
        #  Checking for the .xml files inside the given documents
        if filename.endswith('.xml'):
            if not filename.endswith('.xml'):
                continue
            print("Cleaning", filename)

            with open(os.path.join(dir, filename),'r') as f:

                # this regex for cleaning the files from XML entities that resulted from encoding the file  and XML tags
                # clean file =re.sub('<Title>(.*?)</Title>|<[^>]+>|(lt;)|(gt;)|/p[^>]|p[^>]|/code[^>]|^[ \t]+|&(#[xX][0-9a-fA-F]+|#\d+|[lg]t|amp|apos|quot);', "", f.read())
                cleanfile=re.sub('(lt;)|(gt;)|/p[^>]|p[^>]|/code[^>]|^[ \t]+|&(#[xX][0-9a-fA-F]+|#\d+|[lg]t|amp|apos|quot);', "", f.read())


                with open(os.path.join(dir, filename),'w') as r:
                    r.write(cleanfile)

                #  provided also by https://docs.python.org/2/library/re.html
                #  Regular Expression(RE) the functions in this module let you check if a particular string matches a given regular expression
                #  (or if a given regular expression matches a particular string, which comes down to the same thing).

                # findall() module is used to search for “all” occurrences that match a given pattern
                # findall()  read all the lines of the file and will return all non-overlapping matches of pattern in a single step.
                # Provided also by https://www.guru99.com/python-regular-expressions-complete-tutorial.html
                titles = re.findall("<Title>(.*?)</Title>", cleanfile)
                x.append(titles)

                flatList = [item for elem in x for item in elem]
                fulxlStr = '\n'.join(flatList)

                #  add selected titles of the documents that are cleaned to another file
                with open('Titles of a questions in Stackoverflow.txt', 'w') as t:
                    t.write(fulxlStr)


                # read all the line in the cleaned list and add it to a new Titles of a questions in Stackoverflow.txt file
                with open('Titles of a questions in Stackoverflow.txt','r') as t ,open('query.txt','w')as n:
                    Read_line = t.readline()
                    Loop = 1
                    while Read_line:
                        n.write( str(str(Loop) + '\t' + Read_line))
                        Read_line = t.readline()
                        Loop+=1

                # The re module provides functions and support for regular expressions. re.sub() is used to replace substrings in strings.
                # provided also by https://www.kite.com/python/answers/how-to-use-re.sub()-in-python
                cleanfile2=re.sub("<Title>(.*?)</Title>|<[^>]+>|^a-zA-Z.\d\s","",cleanfile)
                with open(os.path.join(dir, filename),'w') as r:
                    r.write(cleanfile2)


        else:print('sorry this directory does not have any xml files')
    print('done...')



if __name__ == '__main__':
    dir = sys.argv[1]
    if len(sys.argv) < 2:
        print(dir.__doc__)
        sys.exit(1)
    print('cleaning data...')
    cleaning_data()



