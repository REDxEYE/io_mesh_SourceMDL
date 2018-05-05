import sys

try:
    from .ByteIO import ByteIO
    from .VVD_DATA import SourceVvdFileData
except ImportError:
    from ByteIO import ByteIO
    from VVD_DATA import SourceVvdFileData


class SourceVvdFile49:
    def __init__(self, path=None, file=None):
        if path:
            self.reader = ByteIO(path=path + ".vvd")
        elif file:
            self.reader = file
        self.file_data = SourceVvdFileData()
        self.file_data.read(self.reader)

    def test(self):
        print(len(self.file_data.vertexes))


if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            # model = r'.\test_data\xenomorph'
            model = r'.\test_data\hard_suit'
            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            SourceVvdFile49(model).test()
