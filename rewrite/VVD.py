import sys
from pprint import pprint

from ByteReader import ByteReader
from rewrite.VVD_DATA import SourceVvdFileData


class SourceVvdFile49:
    def __init__(self, filepath):
        self.reader = ByteReader(filepath + '.vvd')
        self.vvd = SourceVvdFileData()
        self.vvd.read(self.reader)
        pprint(self.vvd.__dict__)

if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            SourceVvdFile49(r'..\test_data\cuz')