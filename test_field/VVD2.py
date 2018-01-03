import io
import re
import struct
import traceback

import sys
from pprint import pprint
try:
    from .VVD_DATA import *
    from .GLOBALS import *
except:
    from test_field.VVD_DATA import *
    from test_field.GLOBALS import *


class SourceVvdFile49:
    def readASCII(self, len_):
        return ''.join([self.readACSIIChar() for _ in range(len_)])

    def readByte(self):
        type_ = 'b'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readBytes(self, len_):
        type_ = 'b'
        return [struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0] for _ in range(len_)]

    def readUByte(self):
        type_ = 'B'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readInt32(self):
        type_ = 'i'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readUInt32(self):
        type_ = 'I'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readInt16(self):
        type_ = 'h'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readUInt16(self):
        type_ = 'H'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readFloat(self):
        type_ = 'f'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readACSIIChar(self):
        a = self.readUByte()
        return chr(a)
    def __init__(self,filepath):
        if isinstance(filepath,str):
            fp = open(filepath, "rb")
        else:
            fp = filepath
        self.MAX_NUM_BONES_PER_VERT = 3
        self.data = fp
        self.theVvdFileData = SourceVvdFileData()
        self.ReadSourceVvdHeader()
        self.ReadVertexes()
        self.ReadFixups()
        try:
            fp.close()
        except:
            pass
    def ReadSourceVvdHeader(self):
        self.theVvdFileData.id = self.readASCII(4)
        self.theVvdFileData.version = self.readInt32()
        self.theVvdFileData.checksum = self.readInt32()
        self.theVvdFileData.lodCount = self.readInt32()
        self.theVvdFileData.theFixedVertexesByLod = [[]] * self.theVvdFileData.lodCount
        self.theVvdFileData.lodVertexCount = []
        for i in range(8):
            self.theVvdFileData.lodVertexCount.append(self.readInt32())
        self.theVvdFileData.fixupCount = self.readInt32()
        self.theVvdFileData.fixupTableOffset = self.readInt32()
        self.theVvdFileData.vertexDataOffset = self.readInt32()
        self.theVvdFileData.tangentDataOffset = self.readInt32()

    def ReadVertexes(self):
        if self.theVvdFileData.lodCount<=0:
            return
        self.data.seek(self.theVvdFileData.vertexDataOffset,0)

        vertexCount = self.theVvdFileData.lodVertexCount[0]

        for j in range(vertexCount):
            aStudioVertex = SourceVertex()
            aStudioVertex.boneWeight.weight = []
            for x in range(3):
                aStudioVertex.boneWeight.weight.append(self.readFloat())
            aStudioVertex.boneWeight.bone = []
            for x in range(3):
                aStudioVertex.boneWeight.bone.append(self.readUByte())
            aStudioVertex.boneWeight.boneCount = self.readUByte()
            aStudioVertex.positionX = self.readFloat()
            aStudioVertex.positionY = self.readFloat()
            aStudioVertex.positionZ = self.readFloat()
            aStudioVertex.normalX = self.readFloat()
            aStudioVertex.normalY = self.readFloat()
            aStudioVertex.normalZ = self.readFloat()
            aStudioVertex.texCoordX = self.readFloat()
            aStudioVertex.texCoordY = self.readFloat()
            self.theVvdFileData.theVertexes.append(aStudioVertex)

    def ReadFixups(self):
        if self.theVvdFileData.fixupCount>0:
            self.theVvdFileData.theFixups = [None]*self.theVvdFileData.fixupCount
            # self.theVvdFileData.theFixedVertexesByLod = [None]*self.theVvdFileData.
            print('Found fixups',self.theVvdFileData.fixupCount)
            self.data.seek(self.theVvdFileData.fixupTableOffset,0)
            for i in range(self.theVvdFileData.fixupCount):
                aFixup = SourceVvdFixup()
                aFixup.lodIndex = self.readInt32()
                aFixup.vertexIndex = self.readInt32()
                aFixup.vertexCount = self.readInt32()
                self.theVvdFileData.theFixups[i] = aFixup
            if self.theVvdFileData.lodCount >0:
                self.data.seek(self.theVvdFileData.vertexDataOffset,0)
                for lodIndex in range(self.theVvdFileData.lodCount):
                    self.SetupFixedVertexes(lodIndex)
    def SetupFixedVertexes(self,lodIndex:int):
        for fixupIndex in range(len(self.theVvdFileData.theFixups)):
            aFixup = self.theVvdFileData.theFixups[fixupIndex]
            #print(aFixup)
            if aFixup.lodIndex >= lodIndex:
                for j in range(aFixup.vertexCount):
                    aStudioVertex = self.theVvdFileData.theVertexes[aFixup.vertexIndex+j]
                    self.theVvdFileData.theFixedVertexesByLod[lodIndex].append(aStudioVertex)
if __name__ == "__main__":
    with open('log.log', "w") as f:
        with f as sys.stdout:
            A = SourceVvdFile49(r'test_data\medic.vvd')
            pprint(A.theVvdFileData.lodVertexCount)
            print(A.theVvdFileData.theFixedVertexesByLod[0])
