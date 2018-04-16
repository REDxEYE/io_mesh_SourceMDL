from typing import List

try:
    from .ByteIO import ByteIO
    from .GLOBALS import SourceVertex
except:
    from ByteIO import ByteIO
    from GLOBALS import SourceVertex


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
        self.theVertexes = [] #type: List[SourceVertex]
        self.theFixups = []

    def read(self, reader: ByteIO):
        self.id = reader.read_fourcc()
        self.version = reader.read_uint32()
        self.checksum = reader.read_uint32()
        self.lodCount = reader.read_uint32()
        self.lodVertexCount = [reader.read_uint32() for _ in range(8)]
        self.fixupCount = reader.read_uint32()
        self.fixupTableOffset = reader.read_uint32()
        self.vertexDataOffset = reader.read_uint32()
        self.tangentDataOffset = reader.read_uint32()
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

    def read(self, reader: ByteIO):
        self.lodIndex = reader.read_uint32()
        self.vertexIndex = reader.read_uint32()
        self.vertexCount = reader.read_uint32()
        return self

    def __str__(self):
        return "<Fixup lod index:{} vertex index:{} vertex count:{}>".format(self.lodIndex, self.vertexIndex,
                                                                             self.vertexCount)

    def __repr__(self):
        return self.__str__()
