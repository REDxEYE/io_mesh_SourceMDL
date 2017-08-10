import io, struct
from io import BytesIO


class ByteReaderException(Exception):
    pass


class ByteReader:
    settings = {}
    @staticmethod
    def strip(data):
        buffer = ''
        for a in data:
            if a == 0:
                break
            buffer += chr(a)
        return buffer
    def __init__(self, file_handler):

        if file_handler.__class__ is bytes:
            self.data = BytesIO(file_handler)
        elif file_handler.__class__ is io.FileIO or file_handler.__class__ is io.TextIOWrapper or file_handler.__class__ is io.BufferedReader:

            file_handler = file_handler  # type: io.FileIO
            if 'b' not in file_handler.mode:
                raise ByteReaderException('File not in read-bytes mode')
            self.data = BytesIO(file_handler.read())
        elif file_handler.__class__ is str:
            self.data = open(file_handler, 'rb')
        try:
            self.data.__repr__ = self.__repr__
        except:
            pass
    def readASCII(self, len_):
        return ''.join([self.readACSIIChar() for _ in range(len_)])

    def readByte(self):
        type_ = 'b'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readBytes(self, len_):
        type_ = 'b'
        return [struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0] for _ in range(len_)]
    def readUBytes(self, len_):
        type_ = 'B'
        return [struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0] for _ in range(len_)]

    def readUBytesRaw(self, len_):
        type_ = 'B'
        return bytes([struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0] for _ in range(len_)])

    def readUByte(self):
        type_ = 'B'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readInt32(self):
        type_ = 'i'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readUInt32(self):
        type_ = 'I'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readInt16(self):
        type_ = 'h'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]
    def readShort(self,unsinged = False):
        if unsinged:
            return self.readUInt16()
        else:
            return self.readInt16()
    def readUShort(self):
        return self.readUInt16()
    def readUInt16(self):
        type_ = 'H'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readFloat(self):
        type_ = 'f'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readUString(self,maxlen):

        return self.strip(struct.unpack('H'*maxlen,self.data.read(maxlen*2)))

    def readACSIIChar(self):
        a = self.readUByte()
        return chr(a)
    def readASCIIString(self):
        byte = self.readUByte()

        acc = ''
        while byte!=0:
            acc+=chr(byte)
            byte = self.readUByte()
        return acc
    def readUnicodeString(self):
        byte = self.readUShort()

        acc = ''
        while byte!=0:
            acc+=chr(byte)
            byte = self.readUShort()
        return acc

    def readInt(self,Unsinged = False):
        if Unsinged:
            return self.readUInt32()
        else:
            return self.readInt32()

    def skip(self,num):
        self.read(num)


    def find(self,sub,start):
        start_ = self.tell()
        self.seek(0)
        buff = bytes(self.read())
        a = buff.find(sub,start)
        self.seek(start_)
        return a
    def rewind(self,num):
        self.data.seek(-num,1)
    def read(self,num = -1):
        return self.data.read(num)

    def tell(self):
        return self.data.tell()

    def seek(self,*args,**kwargs):
        self.data.seek(*args,**kwargs)

    def get_string_at_offset(self,start,offset) -> str:
        pos = self.tell()
        self.seek(offset+start,0)
        st = self.readASCIIString()
        self.seek(pos)
        return st

    def __len__(self):
        pos = self.tell()
        self.seek(0,2)
        end = self.tell()
        self.seek(pos)
        return end


    def __repr__(self):
        return '<Bytereader Size:{}>'.format(self.__len__())

if __name__ == '__main__':
    file = r'test_data\nick_hwm.mdl'
    a = ByteReader(open(file, 'rb').read())

