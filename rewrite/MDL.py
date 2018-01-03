import sys

from ByteReader import ByteReader
from rewrite.MDL_DATA import *
class SourceMdlFile49:

    def __init__(self, filepath):
        self.reader = ByteReader(filepath+'.mdl')
        self.mdl = SourceMdlFileData()
        self.mdl.read(self.reader)

        self.readBones()
        self.readBoneControllers()

        self.readFlexDescs()
        self.readFlexControllers()
        self.readFlexRules()

        self.readAttachments()
        self.readBoneTableByName()

        self.readBodyParts()
        self.readTextures()
        self.readTexturePaths()

        print(self.mdl)

    def readBones(self):
        if self.mdl.boneCount>0:
            self.reader.seek(self.mdl.boneOffset, 0)
            for i in range(self.mdl.boneCount):
                SourceMdlBone().read(self.reader, self.mdl)

    def readBoneControllers(self):
        if self.mdl.boneControllerCount>0:
            for _ in range(self.mdl.boneControllerCount):
                SourceMdlBoneController().read(self.reader, self.mdl)

    def readFlexDescs(self):
        if self.mdl.flexDescCount > 0:
            self.reader.seek(self.mdl.flexDescOffset, 0)
            for _ in range(self.mdl.flexDescCount):
                FlexDesc = SourceMdlFlexDesc()
                FlexDesc.read(self.reader)
                self.mdl.theFlexDescs.append(FlexDesc)

    def readFlexControllers(self):
        if self.mdl.flexControllerCount > 0:
            self.reader.seek(self.mdl.flexControllerOffset, 0)
            for i in range(self.mdl.flexControllerCount):
                SourceMdlFlexController().read(self.reader, self.mdl)

    def readFlexRules(self):
        self.reader.seek(self.mdl.flexRuleOffset, 0)
        for i in range(self.mdl.flexRuleCount):
            SourceMdlFlexRule().read(self.reader, self.mdl)

    def readAttachments(self):
        if self.mdl.localAttachmentCount>0:
            self.reader.seek(self.mdl.localAttachmentOffset, 0)
            for _ in range(self.mdl.localAttachmentCount):
                SourceMdlAttachment().read(self.reader, self.mdl)

    def readBoneTableByName(self):
        self.reader.seek(self.mdl.boneTableByNameOffset)
        if self.mdl.boneTableByNameOffset != 0:
            for i in range(self.mdl.boneCount):
                index = self.reader.readByte()
                self.mdl.theBoneTableByName.append(index)

    def readBodyParts(self):
        if self.mdl.bodyPartCount>0:
            self.reader.seek(self.mdl.bodyPartOffset)
            for _ in range(self.mdl.bodyPartCount):
                SourceMdlBodyPart().read(self.reader,self.mdl)

    def readTextures(self):
        if self.mdl.textureCount<1:
            return
        self.reader.seek(self.mdl.textureOffset)
        for _ in range(self.mdl.textureCount):
            SourceMdlTexture().read(self.reader,self.mdl)

    def readTexturePaths(self):
        if self.mdl.texturePathCount>0:
            self.reader.seek(self.mdl.texturePathOffset)
            for _ in range(self.mdl.texturePathCount):
                texturePathOffset = self.reader.readInt32()
                entry = self.reader.tell()
                if texturePathOffset!=0:
                    self.mdl.theTexturePaths.append(self.reader.get_name_from_offset(texturePathOffset,0))
                else:
                    self.mdl.theTexturePaths.append("")
                self.reader.seek(entry)


if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            SourceMdlFile49(r'..\test_data\nick_hwm')
