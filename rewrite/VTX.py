import sys
from pprint import pprint

from ByteReader import ByteReader
from rewrite.VTX_DATA import *


class SourceVtxFile49:
    def __init__(self, file):
        self.reader = ByteReader(file+".dx90.vtx")
        self.vtx = SourceVtxFileData()
        self.readSourceVtxHeader()
        self.readSourceVtxBodyParts()
        pprint(self.vtx)
    def readSourceVtxHeader(self):
        self.vtx.read(self.reader)

    def readSourceVtxBodyParts(self):
        if self.vtx.bodyPartCount>0:
            self.reader.seek(self.vtx.bodyPartOffset)
            for _ in range(self.vtx.bodyPartCount):
                SourceVtxBodyPart().read(self.reader,self.vtx)


with open('log.log', "w") as f:  # replace filepath & filename
    with f as sys.stdout:
        # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
        SourceVtxFile49(r'..\test_data\medic')