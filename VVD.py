import sys
from pprint import pprint
try:
    from .ByteIO import ByteIO
    from .VVD_DATA import SourceVvdFileData
except:
    from ByteIO import ByteIO
    from VVD_DATA import SourceVvdFileData


class SourceVvdFile49:
    def __init__(self, filepath):
        self.reader = ByteIO(path = filepath + '.vvd')
        self.vvd = SourceVvdFileData()
        self.vvd.read(self.reader)

if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            SourceVvdFile49(r'..\test_data\cuz')