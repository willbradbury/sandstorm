"""
Utility class to help with downloading and preprocessing training and testing data.
"""

import MySQLdb
import numpy as np
import nltk.data
import os
import re

class Downloader():
    def __init__ (self):
        self.db = MySQLdb.connect(host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            passwd=os.environ['DB_PASSWORD'],
            db=os.environ['DB_NAME'])

        self.cur = self.db.cursor()

        self.comments = []
        self.sentences = []

    def download(self):
        self.cur.execute('SELECT `text` FROM `comments` WHERE `message_type`=2')

        for row in self.cur.fetchall():
            s = re.sub(r'\s+',' ',row[0])
            self.comments.append(unicode(s,'utf8'))

    def preprocess(self):
        tok = nltk.data.load('tokenizers/punkt/english.pickle')

        for comment in self.comments:
            for sent in tok.tokenize(comment):
                self.sentences.append(sent)

    def write_out(self, train, test):
        with open(train,'w') as tr:
            for sent in self.sentences[:int(len(self.sentences)*0.7)]:
                tr.write(sent.encode("UTF-8"))
                tr.write('\n')
        with open(test,'w') as te:
            for sent in self.sentences[int(len(self.sentences)*0.7):]:
                te.write(sent.encode("UTF-8"))
                te.write("\n")
