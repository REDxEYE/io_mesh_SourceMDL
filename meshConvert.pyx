import MDL_DATA
import VTX_DATA
import VVD_DATA
import GLOBALS

cpdef int getPoly( StripGroup:VTX_DATA.SourceVtxStripGroup, int VtxIndexIndex,int lodIndex,int meshVertexIndexStart,
            bodyPartVertexIndexStart: int, VVD:VVD_DATA.SourceVvdFileData):
    cdef int ind
    cdef list poly_indexes = []
    cdef int VtxVertexIndex
    #print('VtxIndexIndex',VtxIndexIndex)
    VtxVertexIndex = StripGroup.theVtxIndexes[VtxIndexIndex]  # type: int
    VtxVertex = StripGroup.theVtxVertexes[VtxVertexIndex]  # type: VTX_DATA.SourceVtxVertex
    vertexIndex = VtxVertex.originalMeshVertexIndex + bodyPartVertexIndexStart + meshVertexIndexStart
    #if VVD.theVvdFileData.fixupCount == 0:
    #    Vertex = VVD.theVvdFileData.theVertexes[vertexIndex - 1]  # type: GLOBALS.SourceVertex
    #else:
    #    Vertex = VVD.theVvdFileData.theFixedVertexesByLod[0][vertexIndex - 1]  # type: GLOBALS.SourceVertex
    #print('poly_indexes',len(poly_indexes))
    return vertexIndex
cpdef tuple WriteMesh( VtxModel :VTX_DATA.SourceVtxModel, int lodIndex,  Model:MDL_DATA.SourceMdlModel,
              bodyPartVertexIndexStart,mat_indexes,VVD):
    VtxLod = VtxModel.theVtxModelLods[lodIndex]  # type: VTX_DATA.SourceVtxModelLod
    cdef list indexes = []
    cdef list vertex_idexes = []
    cdef int groupIndex,vtxIndexIndex,ind,meshIndex
    cdef list poly = []
    for meshIndex, VtxMesh in enumerate(VtxLod.theVtxMeshes):  # type: VTX_DATA.SourceVtxMesh
        print('meshIndex',meshIndex)

        materialIndex = Model.theMeshes[meshIndex].materialIndex
        meshVertexIndexStart = Model.theMeshes[meshIndex].vertexIndexStart
        print('stripGroupCount',VtxMesh.stripGroupCount)
        if VtxMesh.stripGroupCount > 0:
            for groupIndex, StripGroup in enumerate(
                    VtxMesh.theVtxStripGroups):  # type: VTX_DATA.SourceVtxStripGroup
                print('groupIndex',groupIndex)
                if StripGroup.stripCount > 0 and StripGroup.indexCount > 0 and StripGroup.vertexCount > 0:
                    print(StripGroup.theVtxIndexes.__len__())
                    for vtxIndexIndex in range(0, StripGroup.theVtxIndexes.__len__(), 3):
                        if vtxIndexIndex%1000==0:
                            print('vtxIndexIndex_progress',vtxIndexIndex)
                        mat_indexes.append(materialIndex)
                        poly = []
                        for ind in range(3):
                            #print('ind',ind)
                            if vtxIndexIndex+ind not in vertex_idexes:
                                vertex_idexes.append(vtxIndexIndex+ind)
                            poly.append(getPoly(StripGroup, int(vtxIndexIndex+ind), lodIndex, meshVertexIndexStart,
                                    bodyPartVertexIndexStart,VVD))
                        indexes.append(tuple(poly))
        print('INDEXES',len(indexes))
    return (indexes,mat_indexes,vertex_idexes)


