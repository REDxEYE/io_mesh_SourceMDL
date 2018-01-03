from ByteReader import ByteReader
from rewrite.GLOBALS import SourceVertex


class SourceVvdFileData:
    def __init__(self):
        self.id = ""
        self.version = 0
        self.checksum = 0
        self.lodCount = 0
        self.lodVertexCount = []
        self.fixupCount = 0
        self.fixupTableOffset = 0
        self.vertexDataOffset = 0
        self.tangentDataOffset = 0
        self.theVertexesByLod = {}
        self.theFixedVertexesByLod = []
        self.theVertexes = []
        self.theFixups = []

    def read(self, reader: ByteReader):
        self.id = reader.readASCII(4)
        self.version = reader.readInt32()
        self.checksum = reader.readInt32()
        self.lodCount = reader.readInt32()
        self.lodVertexCount = [reader.readInt32() for _ in range(8)]
        self.fixupCount = reader.readInt32()
        self.fixupTableOffset = reader.readInt32()
        self.vertexDataOffset = reader.readInt32()
        self.tangentDataOffset = reader.readInt32()
        self.theFixedVertexesByLod = [[]] * self.lodCount
        if self.lodCount <= 0:
            return

        reader.seek(self.vertexDataOffset)
        for _ in range(self.lodVertexCount[0]):
            self.theVertexes.append(SourceVertex().read(reader))

        reader.seek(self.fixupTableOffset)
        if self.fixupCount > 0:
            for _ in range(self.fixupCount):
                self.theFixups.append(SourceVvdFixup().read(reader))
        if self.lodCount > 0:
            for lodIndex in range(self.lodCount):
                for fixupIndex in range(len(self.theFixups)):
                    fixUp = self.theFixups[fixupIndex]
                    if fixUp.lodIndex >= lodIndex:
                        for j in range(fixUp.vertexCount):
                            vertex = self.theVertexes[fixUp.vertexIndex + j]
                            self.theFixedVertexesByLod[lodIndex].append(vertex)

    def __str__(self):
        return "<FileData id:{} version:{} lod count:{} fixup count:{}>".format(self.id,self.version,self.lodCount,self.fixupCount)

    def __repr__(self):
        return self.__str__()


class SourceVvdFixup:
    def __init__(self):
        self.lodIndex = 0
        self.vertexIndex = 0
        self.vertexCount = 0

    def read(self, reader: ByteReader):
        self.lodIndex = reader.readInt32()
        self.vertexIndex = reader.readInt32()
        self.vertexCount = reader.readInt32()
        return self

    def __str__(self):
        return "<Fixup lod index:{} vertex index:{} vertex count:{}>".format(self.lodIndex, self.vertexIndex,
                                                                             self.vertexCount)

    def __repr__(self):
        return self.__str__()
