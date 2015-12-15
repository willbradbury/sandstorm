"""
Main driver file for training and testing sandstorm.
"""

import sys
from download import Downloader
from tag import Tagger
from model import Model

def print_help():
    print("""sandstorm | Linc | letslinc.com

python main.py [download] [tag] [train] [test]

download -- Download latest comment data from production db
tag -- Tool to manually tag test data
train -- Construct model from training data and report stats
test -- Test model on testing data and report stats

Submodules can be combined to perform multiple tasks in one call
""")

def main():
    args = [i.lower() for i in sys.argv]

    if 'help' in args or len(args) is 1:
        print_help()

    if 'download' in args:
        down = Downloader()
        down.download()
        down.preprocess()
        down.write_out(train="train.dat",test="test.dat")
    if 'tag' in args:
        t = Tagger()
        t.tag("test.dat")
        t.write_out("test_tagged.dat")
    if 'train' in args:
        m = Model()
        m.train("train.dat")
        m.write_out()
    if 'test' in args:
        m = Model("model.mdl")
        m.test("test_tagged.dat")

if __name__ == "__main__" : main()
