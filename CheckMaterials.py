import sys
from ctypes import windll
from pathlib import Path

k32 = windll.LoadLibrary('kernel32.dll')
setConsoleModeProc = k32.SetConsoleMode
setConsoleModeProc(k32.GetStdHandle(-11), 0x0001 | 0x0002 | 0x0004)
# import winreg
#
# winreg.SetValueEx(winreg.HKEY_CURRENT_USER,r'HKEY_CURRENT_USER\Console\VirtualTerminalLevel',0,winreg.REG_DWORD,1)
sandwich = r'''                   _.---._
                _.-~       ~-._
            _.-~               ~-._
        _.-~                       ~---._
    _.-~                                 ~\
 .-~                                    _.;
 :-._                               _.-~ ./
 `-._~-._                   _..__.-~ _.-~
  /  ~-._~-._              / .__..--~----._
 \_____(_;-._\.        _.-~_/       ~).. . \
    /(_____  \`--...--~_.-~______..-+_______)
  .(_________/`--...--~/    _/nad        /\
 /-._     \_     (___./_..-~__.....__..-~./
 `-._~-._   ~\--------~  .-~_..__.-~ _.-~
     ~-._~-._ ~---------'  / .__..--~
         ~-._\.        _.-~_/
             \`--...--~_.-~
              `--...--~'''


import MDL
import ValveUtils
from ValveUtils import GameInfoFile, KeyValueFile

if __name__ == '__main__':
    if sys.argv[1] == 'make':
        temp = ' '.join(sys.argv[1:])
        if 'me' in temp and 'sandwich' in temp:
            print('Here is your sandwich')
            print(sandwich)
            exit()
    # model = Path(r"G:\SteamLibrary\SteamApps\common\half-life 2\hl2\models\shadertest\envballs.mdl")
    model = Path(sys.argv[1])
    # if len(sys.argv) > 2:
    #     dump_path = Path(sys.argv[2])
    # else:
    #     dump_path = None
    if not model.exists():
        print('\033[91mMODEL NOT FOUND\033[0m')
        exit()
    print('\033[94mReading \033[95m{}\033[0m'.format(model))
    mod_path = ValveUtils.get_mod_path(model)
    game_info_path = mod_path / 'gameinfo.txt'
    if not game_info_path.exists():
        raise FileNotFoundError("Failed to find gameinfo file")
    gi = GameInfoFile(game_info_path)
    # mod_paths = gi.get_search_paths_recursive()
    textures = []
    used_textures = []
    materials = []
    other_files = []
    print('Trying to find used textures and materials')
    print('Searching in:')
    for path in gi.get_search_paths_recursive():
        print('\t\x1b[95m{}\x1b[0m'.format(path))
    if model.exists():
        other_files.append(model)
        mdl = MDL.SourceMdlFile49(filepath=str(model.with_name(model.stem)), read=False)
        mdl.read_skin_families()
        mdl.read_texture_paths()
        mdl.read_textures()
        # print(mdl.file_data.textures)
        for texture in mdl.file_data.textures:
            for tex_path in mdl.file_data.texture_paths:
                mat = gi.find_material(Path(tex_path) / texture.path_file_name, use_recursive=True)
                if mat:
                    temp = ValveUtils.get_mod_path(mat).parent
                    materials.append((Path(mat), Path(mat).relative_to(temp)))
            ...

        for mat in materials:
            kv = KeyValueFile(mat[0])
            for v in list(kv.as_dict.values())[0].values():
                if '/' in v or '\\' in v:
                    used_textures.append(Path(v))
                    tex = gi.find_texture(v, True)
                    if tex:
                        temp = ValveUtils.get_mod_path(tex).parent
                        textures.append((Path(tex), Path(tex).relative_to(temp)))
            # print(kv.as_dict)
        print('\033[94m', '*' * 10, 'MATERIALS', '*' * 10, '\033[0m')
        for texture in mdl.file_data.textures:
            exist = False
            found_path = None
            for mat in materials:
                if mat[1].stem == texture.path_file_name:
                    exist = True
                    found_path = mat[0]
                    break
            if exist:
                print('>>>\033[94m', texture.path_file_name, '-> \033[92mFound here \033[0m>', '\033[95m', found_path,
                      '\033[0m')
            else:
                print('>>>\033[94m', texture.path_file_name, '-> \033[91mNot found!', '\033[0m')
            # print()

        print('\033[94m', '*' * 10, 'TEXTURES', '*' * 10, '\033[0m')
        for used_texture in used_textures:
            exist = False
            found_path = None
            for tex in textures:
                if tex[1].stem == used_texture.stem:
                    exist = True
                    found_path = tex[0]
                    break
            if exist:
                print('>>>\033[94m', used_texture, '-> \033[92mFound here \033[0m>', '\033[95m', found_path,
                      '\033[0m')
            else:
                print('>>>\033[94m', used_texture, '-> \033[91mNot found!', '\033[0m')
            # print()
    textures = list(set(textures))
    input('Press Enter to exit')
    # print('*'*10,'MATERIALS','*'*10)
    # pprint(materials)
    # print('*'*10,'TEXTURES','*'*10)
    # pprint(textures)


