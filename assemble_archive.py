import sys
from pathlib import Path
from pprint import pprint

import MDL
import ValveUtils
from ValveUtils import GameInfoFile,KeyValueFile

if __name__ == '__main__':
    model = Path(sys.argv[1])
    dump_path = Path(sys.argv[2])
    mod_path = ValveUtils.get_mod_path(model)
    game_info_path = mod_path / 'gameinfo.txt'
    if not game_info_path.exists():
        raise FileNotFoundError("Failed to find gameinfo file")
    gi = GameInfoFile(game_info_path)
    # mod_paths = gi.get_search_paths_recursive()
    textures = []
    materials = []
    other_files =[]
    if model.exists() and dump_path.exists():
        other_files.append(model)
        mdl = MDL.SourceMdlFile49(filepath=str(model.with_name(model.stem)), read=False)
        mdl.read_skin_families()
        mdl.read_texture_paths()
        mdl.read_textures()
        print(mdl.file_data.textures)
        for texture in mdl.file_data.textures:
            for tex_path in mdl.file_data.texture_paths:
                mat = gi.find_material(Path(tex_path)/texture.path_file_name,use_recursive=True)
                if mat:
                    temp = ValveUtils.get_mod_path(mat).parent
                    materials.append((Path(mat),Path(mat).relative_to(temp)))
            ...

        for mat in materials:
            kv = KeyValueFile(mat[0])
            for v in list(kv.as_dict.values())[0].values():
                if '/' in v or '\\' in v:
                    tex = gi.find_texture(v,True)
                    if tex:
                        temp = ValveUtils.get_mod_path(tex).parent
                        textures.append((Path(tex),Path(tex).relative_to(temp)))
            # print(kv.as_dict)
    textures = list(set(textures))
    print('*'*10,'MATERIALS','*'*10)
    pprint(materials)
    print('*'*10,'TEXTURES','*'*10)
    pprint(textures)
