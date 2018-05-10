import sys

try:
    from .ByteIO import ByteIO
    from .VTX_DATA import *
except ImportError:
    from ByteIO import ByteIO
    from VTX_DATA import *


class SourceVtxFile49:
    def __init__(self, path=None, file=None):
        self.final = False
        if path:
            self.reader = ByteIO(path=path + ".dx90.vtx")
        elif file:
            self.reader = file
        # print('Reading VTX file')
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
                bopy_part_entry = self.reader.tell()
                body_part = SourceVtxBodyPart()
                body_part.model_count = self.reader.read_uint32()
                body_part.model_offset = self.reader.read_uint32()
                with self.reader.save_current_pos():
                    if body_part.model_count > 0 and body_part.model_offset != 0:
                        with self.reader.save_current_pos():
                            self.read_source_vtx_models(bopy_part_entry, body_part)
                    self.vtx.vtx_body_parts.append(body_part)
                # self.reader.seek(inputFileStreamPosition, 0)

    def read_source_vtx_models(self, body_part_entry, body_part: SourceVtxBodyPart):
        self.reader.seek(body_part_entry + body_part.model_offset, 0)
        for i in range(body_part.model_count):
            model_entry = self.reader.tell()
            model = SourceVtxModel()
            model.lodCount = self.reader.read_uint32()
            model.lodOffset = self.reader.read_uint32()
            if model.lodCount > 0 and model.lodOffset != 0:
                with self.reader.save_current_pos():
                    self.read_source_vtx_model_lods(model_entry, model)
            body_part.vtx_models.append(model)

    def read_source_vtx_model_lods(self, model_entry, model: SourceVtxModel):
        self.reader.seek(model_entry + model.lodOffset, 0)
        for i in range(model.lodCount):

            model_lod_entry = self.reader.tell()
            model_lod = SourceVtxModelLod()
            model_lod.lod = i
            model_lod.meshCount = self.reader.read_uint32()
            model_lod.meshOffset = self.reader.read_uint32()
            model_lod.switchPoint = self.reader.read_float()

            if model_lod.meshCount > 0 and model_lod.meshOffset != 0:
                with self.reader.save_current_pos():
                    self.read_source_vtx_meshes(model_lod_entry, model_lod)
            model.vtx_model_lods.append(model_lod)

    def read_source_vtx_meshes(self, model_lod_entry, model_lod: SourceVtxModelLod):
        self.reader.seek(model_lod_entry + model_lod.meshOffset, 0)
        for j in range(model_lod.meshCount):
            mesh_entry = self.reader.tell()
            mesh = SourceVtxMesh()
            mesh.strip_group_count = self.reader.read_uint32()
            mesh.strip_group_offset = self.reader.read_uint32()
            mesh.flags = self.reader.read_uint8()

            entry = self.reader.tell()
            if mesh.strip_group_count > 0 and mesh.strip_group_offset != 0:
                if self.first_strip_group_end == 0:
                    with self.reader.save_current_pos():
                        self.reader.seek(mesh_entry + mesh.strip_group_offset, 0)
                        for _ in range(mesh.strip_group_count):
                            SourceVtxStripGroup().read(self.reader, extra_8=self.StripGroupUsesExtra8Bytes)
                        self.first_strip_group_end = self.reader.tell()
                    self.reader.skip(entry - self.first_strip_group_end)
                elif self.second_strip_group_offset == 0:
                    self.second_strip_group_offset = mesh_entry
                    if self.first_strip_group_end == mesh_entry + mesh.strip_group_offset:
                        # Well, extra 8 bytes isn't required here
                        pass
                    else:
                        self.StripGroupUsesExtra8Bytes = not self.StripGroupUsesExtra8Bytes
                    print('Mesh', "require" if self.StripGroupUsesExtra8Bytes else "doesn't require",
                          "extra 8 bytes")
            self.reader.seek(entry)
            model_lod.vtx_meshes.append(mesh)

    def read_source_vtx_strip_groups(self, mesh_entry, mesh: SourceVtxMesh):
        self.reader.seek(mesh_entry + mesh.strip_group_offset, 0)

        for j in range(mesh.strip_group_count):

            strip_group_entry = self.reader.tell()

            strip_group = SourceVtxStripGroup()
            strip_group.vertex_count = self.reader.read_uint32()
            strip_group.vertex_offset = self.reader.read_uint32()
            strip_group.index_count = self.reader.read_uint32()
            strip_group.index_offset = self.reader.read_uint32()
            strip_group.strip_count = self.reader.read_uint32()
            strip_group.strip_offset = self.reader.read_uint32()
            strip_group.flags = self.reader.read_uint8()
            if self.StripGroupUsesExtra8Bytes:
                self.reader.read_uint32()
                self.reader.read_uint32()
            self.first_strip_group_end = self.reader.tell()

            strip_group_end = self.reader.tell()
            try:
                if strip_group.index_count > 0 and strip_group.index_offset != 0:
                    self.reader.seek(strip_group_entry + strip_group.index_offset)
                    for _ in range(strip_group.index_count):
                        strip_group.vtx_indexes.append(self.reader.read_uint16())

                if strip_group.strip_count > 0 and strip_group.strip_offset != 0:
                    self.reader.seek(strip_group_entry + strip_group.strip_offset)
                    for _ in range(strip_group.strip_count):
                        SourceVtxStrip().read(self.reader, strip_group)

                if strip_group.vertex_count > 0 and strip_group.vertex_offset != 0:
                    self.reader.seek(strip_group_entry + strip_group.vertex_offset)
                    for _ in range(strip_group.vertex_count):
                        SourceVtxVertex().read(self.reader, strip_group)

                self.reader.seek(strip_group_end, 0)
                mesh.vtx_strip_groups.append(strip_group)
            # we need to catch any exception
            except Exception:
                if self.final:
                    raise Exception('ERROR')
                self.retry += 1
                if self.retry > 3:
                    raise Exception('Can\'t read VTX file')
                self.StripGroupUsesExtra8Bytes = not self.StripGroupUsesExtra8Bytes
                print('Read failed \nRetrying')
                mesh.vtx_strip_groups.clear()
                self.read_source_vtx_strip_groups(mesh_entry, mesh)
            self.retry = 0
            print(strip_group)
            mesh.vtx_strip_groups.append(strip_group)


if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            a = SourceVtxFile49(r'test_data\Horse')
            # a = SourceVtxFile49(r'test_data\kali')
            # a = SourceVtxFile49(r'test_data\kali')
            print(a.vtx)
