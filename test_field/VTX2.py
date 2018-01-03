import os
import re
import traceback
from pprint import pprint
import sys
import struct
DEBUG = False
try:
    from .VTX_DATA import *
except:
    from VTX_DATA import *


class SourceVtxFile49:
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

    @staticmethod
    def GetNameFromOffset(offset, index, data):
        data_ = data[offset + index:]
        name = ""
        for C in data_:
            if C == 0:
                break
            name += chr(C)
        return name

    def __init__(self, filepath):
        if isinstance(filepath, str):
            fp = open(filepath, "rb")
        else:
            fp = filepath
        self.data = fp
        self.retry = 0
        self.theFirstMeshWithStripGroups = None
        self.theFirstMeshWithStripGroupsInputFileStreamPosition = -1
        self.theSecondMeshWithStripGroups = None
        self.theExpectedStartOfSecondStripGroupList = -1
        self.theStripGroupUsesExtra8Bytes = False
        self.theVtxFileData = SourceVtxFileData()
        self.ReadSourceVtxHeader()
        self.ReadSourceVtxBodyParts()
        try:
            fp.close()
        except:
            pass
    def ReadSourceVtxHeader(self):
        self.theVtxFileData.version = self.readInt32()
        self.theVtxFileData.vertexCacheSize = self.readInt32()
        self.theVtxFileData.maxBonesPerStrip = self.readUInt16()
        self.theVtxFileData.maxBonesPerTri = self.readUInt16()
        self.theVtxFileData.maxBonesPerVertex = self.readInt32()
        self.theVtxFileData.checksum = self.readInt32()
        self.theVtxFileData.lodCount = self.readInt32()
        self.theVtxFileData.materialReplacementListOffset = self.readInt32()
        self.theVtxFileData.bodyPartCount = self.readInt32()
        self.theVtxFileData.bodyPartOffset = self.readInt32()
        if DEBUG:
            pprint(self.theVtxFileData.__dict__)

    def ReadSourceVtxBodyParts(self):
        if self.theVtxFileData.bodyPartCount > 0:
            self.data.seek(self.theVtxFileData.bodyPartOffset, 0)
            for i in range(self.theVtxFileData.bodyPartCount):
                #print('BodyPart N{}'.format(i))
                bodyPartInputFileStreamPosition = self.data.tell()
                aBodyPart = SourceVtxBodyPart()
                aBodyPart.modelCount = self.readInt32()
                aBodyPart.modelOffset = self.readInt32()
                inputFileStreamPosition = self.data.tell()
                if aBodyPart.modelCount > 0 and aBodyPart.modelOffset != 0:
                    self.ReadSourceVtxModels(bodyPartInputFileStreamPosition, aBodyPart)
                if DEBUG:
                    pass
                    pprint(aBodyPart.__dict__)
                self.theVtxFileData.theVtxBodyParts.append(aBodyPart)
                self.data.seek(inputFileStreamPosition, 0)

    def ReadSourceVtxModels(self, bodyPartInputFileStreamPosition, aBodyPart: SourceVtxBodyPart):
        self.data.seek(bodyPartInputFileStreamPosition + aBodyPart.modelOffset, 0)
        for i in range(aBodyPart.modelCount):

            modelInputFileStreamPosition = self.data.tell()
            aModel = SourceVtxModel()
            aModel.lodCount = self.readInt32()
            aModel.lodOffset = self.readInt32()

            inputFileStreamPosition = self.data.tell()
            if DEBUG:
                pprint(aModel.__dict__)
            if aModel.lodCount > 0 and aModel.lodOffset != 0:
                self.ReadSourceVtxModelLods(modelInputFileStreamPosition, aModel)
            aBodyPart.theVtxModels.append(aModel)
            self.data.seek(inputFileStreamPosition, 0)

    def ReadSourceVtxModelLods(self, modelInputFileStreamPosition, aModel: SourceVtxModel):
        self.data.seek(modelInputFileStreamPosition + aModel.lodOffset, 0)
        for i in range(aModel.lodCount):

            modelLodInputFileStreamPosition = self.data.tell()
            aModelLod = SourceVtxModelLod()
            aModelLod.lod = i
            aModelLod.meshCount = self.readInt32()
            aModelLod.meshOffset = self.readInt32()
            aModelLod.switchPoint = self.readFloat()


            inputFileStreamPosition = self.data.tell()
            if aModelLod.meshCount > 0 and aModelLod.meshOffset != 0:
                self.ReadSourceVtxMeshes(modelLodInputFileStreamPosition, aModelLod)
            self.data.seek(inputFileStreamPosition, 0)
            aModel.theVtxModelLods.append(aModelLod)
            if DEBUG:
                pprint(aModelLod.__dict__)
    def ReadSourceVtxMeshes(self, modelLodInputFileStreamPosition, aModelLod: SourceVtxModelLod):
        self.data.seek(modelLodInputFileStreamPosition + aModelLod.meshOffset, 0)
        for j in range(aModelLod.meshCount):

            meshInputFileStreamPosition = self.data.tell()
            aMesh = SourceVtxMesh()
            aMesh.stripGroupCount = self.readInt32()
            aMesh.stripGroupOffset = self.readInt32()
            aMesh.flags = self.readUByte()

            inputFileStreamPosition = self.data.tell()
            # if DEBUG:
            #     pprint(aMesh.__dict__)
            if aMesh.stripGroupCount > 0 and aMesh.stripGroupOffset != 0:
                if self.theFirstMeshWithStripGroups == None:
                    self.theFirstMeshWithStripGroups = aMesh
                    self.theFirstMeshWithStripGroupsInputFileStreamPosition = meshInputFileStreamPosition
                    self.AnalyzeVtxStripGroups(meshInputFileStreamPosition, aMesh)
                    self.ReadSourceVtxStripGroups(meshInputFileStreamPosition, aMesh)
                elif self.theSecondMeshWithStripGroups == None:
                    self.theSecondMeshWithStripGroups = aMesh
                    if self.theExpectedStartOfSecondStripGroupList != meshInputFileStreamPosition + aMesh.stripGroupOffset:
                        self.theStripGroupUsesExtra8Bytes = True
                        if len(aMesh.theVtxStripGroups) > 0:
                            aMesh.theVtxStripGroups.clear()
                        self.ReadSourceVtxStripGroups(meshInputFileStreamPosition, aMesh)
                    self.ReadSourceVtxStripGroups(meshInputFileStreamPosition, aMesh)
                else:
                    self.ReadSourceVtxStripGroups(meshInputFileStreamPosition, aMesh)
            self.data.seek(inputFileStreamPosition, 0)
            aModelLod.theVtxMeshes.append(aMesh)

    def AnalyzeVtxStripGroups(self, meshInputFileStreamPosition, aMesh: SourceVtxMesh):
        self.data.seek(meshInputFileStreamPosition + aMesh.stripGroupOffset, 0)
        for j in range(aMesh.stripGroupCount):
            aStripGroup = SourceVtxStripGroup()
            aStripGroup.vertexCount = self.readInt32()
            aStripGroup.vertexOffset = self.readInt32()
            aStripGroup.indexCount = self.readInt32()
            aStripGroup.indexOffset = self.readInt32()
            aStripGroup.stripCount = self.readInt32()
            aStripGroup.stripOffset = self.readInt32()
            aStripGroup.flags = self.readUByte()
        self.theExpectedStartOfSecondStripGroupList = self.data.tell()

    def ReadSourceVtxStripGroups(self, meshInputFileStreamPosition, aMesh: SourceVtxMesh):
        self.data.seek(meshInputFileStreamPosition + aMesh.stripGroupOffset, 0)
        for j in range(aMesh.stripGroupCount):

            stripGroupInputFileStreamPosition = self.data.tell()
            aStripGroup = SourceVtxStripGroup()
            aStripGroup.vertexCount = self.readInt32()
            aStripGroup.vertexOffset = self.readInt32()
            aStripGroup.indexCount = self.readInt32()
            aStripGroup.indexOffset = self.readInt32()
            aStripGroup.stripCount = self.readInt32()
            aStripGroup.stripOffset = self.readInt32()
            aStripGroup.flags = self.readUByte()
            if self.theStripGroupUsesExtra8Bytes:
                self.readUInt32()
                self.readUInt32()
            # if DEBUG:
            #     pprint(['aStripGroup', aStripGroup.__dict__])
            inputFileStreamPosition = self.data.tell()
            try:
                if aStripGroup.indexCount > 0 and aStripGroup.indexOffset != 0:
                    self.ReadSourceVtxIndexes(stripGroupInputFileStreamPosition, aStripGroup)

                if aStripGroup.stripCount > 0 and aStripGroup.stripOffset != 0:
                    self.ReadSourceVtxStrips(stripGroupInputFileStreamPosition, aStripGroup)

                if aStripGroup.vertexCount > 0 and aStripGroup.vertexOffset != 0:
                    self.ReadSourceVtxVertexes(stripGroupInputFileStreamPosition, aStripGroup)

                self.data.seek(inputFileStreamPosition, 0)
                aMesh.theVtxStripGroups.append(aStripGroup)
            except Exception:
                self.retry += 1
                print('FAIL N{}'.format(self.retry))
                if self.retry > 3:
                    raise Exception('Can\'t read VTX file')
                    return
                self.theStripGroupUsesExtra8Bytes = not self.theStripGroupUsesExtra8Bytes
                self.data.seek(meshInputFileStreamPosition + aMesh.stripGroupOffset, 0)
                self.ReadSourceVtxStripGroups(meshInputFileStreamPosition, aMesh)

    def ReadSourceVtxVertexes(self, stripGroupInputFileStreamPosition, aStripGroup: SourceVtxStripGroup):
        self.data.seek(stripGroupInputFileStreamPosition + aStripGroup.vertexOffset, 0)
        for i in range(aStripGroup.vertexCount):
            aVertex = SourceVtxVertex()
            aVertex.boneWeightIndex = [self.readUByte() for k in range(self.theVtxFileData.maxBonesPerVertex)]
            aVertex.boneCount = self.readUByte()
            aVertex.originalMeshVertexIndex = self.readUInt16()
            aVertex.boneId = [self.readUByte() for k in range(self.theVtxFileData.maxBonesPerVertex)]

            aStripGroup.theVtxVertexes.append(aVertex)

    def ReadSourceVtxIndexes(self, stripGroupInputFileStreamPosition, aStripGroup: SourceVtxStripGroup):
        self.data.seek(stripGroupInputFileStreamPosition + aStripGroup.indexOffset, 0)
        for j in range(aStripGroup.indexCount):
            d = self.readUInt16()
            aStripGroup.theVtxIndexes.append(d)

    def ReadSourceVtxStrips(self, stripGroupInputFileStreamPosition, aStripGroup: SourceVtxStripGroup):
        self.data.seek(stripGroupInputFileStreamPosition + aStripGroup.stripOffset, 0)
        for j in range(aStripGroup.stripCount):
            aStrip = SourceVtxStrip()
            aStrip.indexCount = self.readInt32()
            aStrip.indexMeshIndex = self.readInt32()
            aStrip.vertexCount = self.readInt32()
            aStrip.vertexMeshIndex = self.readInt32()
            aStrip.boneCount = self.readInt16()
            aStrip.flags = self.readUByte()
            aStrip.boneStateChangeCount = self.readInt32()
            aStrip.boneStateChangeOffset = self.readInt32()

            # pprint(aStrip.__dict__)
            aStripGroup.theVtxStrips.append(aStrip)


if __name__ == "__main__":
    DEBUG = True
    A = SourceVtxFile49(r'test_data\medic.dx90.vtx')
    # print(A.theVtxFileData.theVtxBodyParts)

