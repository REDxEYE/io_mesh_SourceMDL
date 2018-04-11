import sys
from pprint import pprint
try:
    from .ByteIO import ByteIO
    from .VTX_DATA import *
except:
    from ByteIO import ByteIO
    from VTX_DATA import *


class SourceVtxFile49:
    def __init__(self, path = None, file = None):
        if path:
            self.reader = ByteIO(path = path + ".dx90.vtx")
        elif file:
            self.reader = file
        self.retry = 0
        self.first_strip_group_end = 0
        self.second_strip_group_offset = 0
        self.StripGroupUsesExtra8Bytes = True
        self.vtx = SourceVtxFileData()
        self.read_source_vtx_header()
        # self.read_source_vtx_body_parts()

    def read_source_vtx_header(self):
        self.vtx.read(self.reader)

    # Deprecated stuff, left for debug

    def read_source_vtx_body_parts(self):
        if self.vtx.bodyPartCount > 0:
            self.reader.seek(self.vtx.bodyPartOffset, 0)
            for i in range(self.vtx.bodyPartCount):
                bodyPartInputFileStreamPosition = self.reader.tell()
                aBodyPart = SourceVtxBodyPart()
                aBodyPart.modelCount = self.reader.read_uint32()
                aBodyPart.modelOffset = self.reader.read_uint32()
                inputFileStreamPosition = self.reader.tell()
                if aBodyPart.modelCount > 0 and aBodyPart.modelOffset != 0:
                    with self.reader.save_current_pos():
                        self.read_source_vtx_models(bodyPartInputFileStreamPosition, aBodyPart)
                self.vtx.theVtxBodyParts.append(aBodyPart)
                self.reader.seek(inputFileStreamPosition, 0)

    def read_source_vtx_models(self, bodyPartInputFileStreamPosition, aBodyPart: SourceVtxBodyPart):
        self.reader.seek(bodyPartInputFileStreamPosition + aBodyPart.modelOffset, 0)
        for i in range(aBodyPart.modelCount):

            model_entry = self.reader.tell()
            aModel = SourceVtxModel()
            aModel.lodCount = self.reader.read_uint32()
            aModel.lodOffset = self.reader.read_uint32()

            model_end = self.reader.tell()
            if aModel.lodCount > 0 and aModel.lodOffset != 0:
                with self.reader.save_current_pos():
                    self.read_source_vtx_model_lods(model_entry, aModel)
            aBodyPart.theVtxModels.append(aModel)

    def read_source_vtx_model_lods(self, model_entry, aModel: SourceVtxModel):
        self.reader.seek(model_entry + aModel.lodOffset, 0)
        for i in range(aModel.lodCount):

            model_lod_entry = self.reader.tell()
            aModelLod = SourceVtxModelLod()
            aModelLod.lod = i
            aModelLod.meshCount = self.reader.read_uint32()
            aModelLod.meshOffset = self.reader.read_uint32()
            aModelLod.switchPoint = self.reader.read_float()

            if aModelLod.meshCount > 0 and aModelLod.meshOffset != 0:
                with self.reader.save_current_pos():
                    self.read_source_vtx_meshes(model_lod_entry, aModelLod)
            aModel.theVtxModelLods.append(aModelLod)

    def read_source_vtx_meshes(self, model_lod_entry, aModelLod: SourceVtxModelLod):
        self.reader.seek(model_lod_entry + aModelLod.meshOffset, 0)
        for j in range(aModelLod.meshCount):
            mesh_entry = self.reader.tell()
            aMesh = SourceVtxMesh()
            aMesh.stripGroupCount = self.reader.read_uint32()
            aMesh.stripGroupOffset = self.reader.read_uint32()
            aMesh.flags = self.reader.read_uint8()

            inputFileStreamPosition = self.reader.tell()
            if aMesh.stripGroupCount > 0 and aMesh.stripGroupOffset != 0:
                if self.first_strip_group_end == 0:
                    with self.reader.save_current_pos():
                        self.reader.seek(mesh_entry + aMesh.stripGroupOffset, 0)
                        for j in range(aMesh.stripGroupCount):
                            SourceVtxStripGroup().read(self.reader,extra_8 = self.StripGroupUsesExtra8Bytes)
                        self.first_strip_group_end = self.reader.tell()
                    self.reader.skip(inputFileStreamPosition-self.first_strip_group_end)
                elif self.second_strip_group_offset == 0:
                    self.second_strip_group_offset = mesh_entry
                    if self.first_strip_group_end == mesh_entry+aMesh.stripGroupOffset:
                        # Well, extra 8 bytes isn't required here
                        pass
                    else:
                        self.StripGroupUsesExtra8Bytes = not self.StripGroupUsesExtra8Bytes
                    print('Mesh', "require" if self.StripGroupUsesExtra8Bytes else "doesn't require",
                          "extra 8 bytes")
            self.reader.seek(inputFileStreamPosition)
            aModelLod.theVtxMeshes.append(aMesh)



    def read_source_vtx_strip_groups(self, mesh_entry, aMesh: SourceVtxMesh):
        self.reader.seek(mesh_entry + aMesh.stripGroupOffset, 0)
        entry = self.reader.tell()

        for j in range(aMesh.stripGroupCount):

            strip_group_entry = self.reader.tell()

            aStripGroup = SourceVtxStripGroup()
            aStripGroup.vertexCount = self.reader.read_uint32()
            aStripGroup.vertexOffset = self.reader.read_uint32()
            aStripGroup.indexCount = self.reader.read_uint32()
            aStripGroup.indexOffset = self.reader.read_uint32()
            aStripGroup.stripCount = self.reader.read_uint32()
            aStripGroup.stripOffset = self.reader.read_uint32()
            aStripGroup.flags = self.reader.read_uint8()
            if self.StripGroupUsesExtra8Bytes:
                self.reader.read_uint32()
                self.reader.read_uint32()
            self.first_strip_group_end = self.reader.tell()

            strip_group_end = self.reader.tell()
            try:
                if aStripGroup.indexCount > 0 and aStripGroup.indexOffset != 0:
                    self.reader.seek(strip_group_entry+aStripGroup.indexOffset)
                    for _ in range(aStripGroup.indexCount):
                        aStripGroup.theVtxIndexes.append(self.reader.read_uint16())

                if aStripGroup.stripCount > 0 and aStripGroup.stripOffset != 0:
                    self.reader.seek(strip_group_entry + aStripGroup.stripOffset)
                    for _ in range(aStripGroup.stripCount):
                        SourceVtxStrip().read(self.reader,aStripGroup)

                if aStripGroup.vertexCount > 0 and aStripGroup.vertexOffset != 0:
                    self.reader.seek(strip_group_entry + aStripGroup.vertexOffset)
                    for _ in range(aStripGroup.vertexCount):
                        SourceVtxVertex().read(self.reader, aStripGroup)

                self.reader.seek(strip_group_end, 0)
                aMesh.theVtxStripGroups.append(aStripGroup)
            except Exception:
                if self.final:
                    raise Exception('ERROR')
                self.retry += 1
                if self.retry > 3:
                    raise Exception('Can\'t read VTX file')
                self.StripGroupUsesExtra8Bytes = not self.StripGroupUsesExtra8Bytes
                print('Read failed \nRetrying')
                aMesh.theVtxStripGroups.clear()
                self.read_source_vtx_strip_groups(mesh_entry, aMesh)
            self.retry = 0
            print(aStripGroup)
            aMesh.theVtxStripGroups.append(aStripGroup)

if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:

            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            a = SourceVtxFile49(r'test_data\kali')
            print(a.vtx)
