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
        self.theFixups =[]
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
class SourceVvdFixup:
    def __init__(self):
        self.lodIndex = 0
        self.vertexIndex = 0
        self.vertexCount = 0
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)