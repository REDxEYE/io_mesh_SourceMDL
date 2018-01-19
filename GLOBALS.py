import random
import struct
try:
    from .ByteIO import ByteIO
except:
    from ByteIO import ByteIO


class SourceVector:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def read(self, reader:ByteIO):
        self.x = reader.read_float()
        self.y = reader.read_float()
        self.z = reader.read_float()
        return self
    @property
    def asList(self):
        return [self.x, self.y, self.z]

    @property
    def as_string_smd(self):
        return "{:.6f} {:.6f} {:.6f}".format(self.x,self.y,self.z)

    @property
    def as_string(self):
        return " X:{} Y:{} Z:{}".format(self.x,self.y,self.z)

    def __str__(self):
        return "<Vector 3D X:{} Y:{} Z:{}".format(self.x,self.y,self.z)

    def __repr__(self):
        return "<Vector 3D X:{} Y:{} Z:{}".format(self.x,self.y,self.z)

class SourceQuaternion:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.w = 0.0

    def read(self, reader:ByteIO):
        self.x = reader.read_float()
        self.y = reader.read_float()
        self.z = reader.read_float()
        self.w = reader.read_float()
        return self

    def __str__(self):
        return "<Quaternion X:{} Y:{} Z:{} W:{}".format(self.x,self.y,self.z,self.w)

    def __repr__(self):
        return "<Quaternion X:{} Y:{} Z:{} W:{}".format(self.x,self.y,self.z,self.w)

class SourceFloat16bits:
    float32bias = 127
    float16bias = 15
    maxfloat16bits = 65504.0
    half_denorm = (1.0 / 16384.0)

    def __init__(self):
        self.the16BitValue = 0

    def read(self,reader:ByteIO):
        self.the16BitValue = reader.read_uint16()
        return self

    @property
    def TheFloatValue(self):
        result = 0
        sign = 0
        floatSign = 0
        sign = self.GetSign(self.the16BitValue)
        if sign == 1:
            floatSign = -1
        else:
            floatSign = 0
        if self.IsInfinity(self.the16BitValue):
            return self.maxfloat16bits * floatSign
        if self.IsNaN(self.the16BitValue):
            return 0
        mantissa = 0
        biased_exponent = 0
        mantissa = self.GetMantissa(self.the16BitValue)
        biased_exponent = self.GetBiasedExponent(self.the16BitValue)
        if biased_exponent == 0 and mantissa != 0:
            floatMantissa = 0
            floatMantissa = mantissa / 1024.0
            result = floatSign * floatMantissa * self.half_denorm
        else:
            result = self.GetSingle(self.the16BitValue)
        return result

    def GetMantissa(self, value):
        return (value & 0x3FF)

    def GetBiasedExponent(self, value):
        return (value & 0x7C00) >> 10

    def GetSign(self,value):
        return (value & 0x8000) >> 15

    def GetSingle(self,value):
        bitsResult = IntegerAndSingleUnion()
        mantissa = None
        biased_exponent = None
        sign = None
        resultMantissa = None
        resultBiasedExponent = None
        resultSign = None
        bitsResult.i = 0
        mantissa = self.GetMantissa(self.the16BitValue)
        biased_exponent = self.GetBiasedExponent(self.the16BitValue)
        sign = self.GetSign(self.the16BitValue)
        resultMantissa = mantissa << (23 - 10)
        if biased_exponent == 0:
            resultBiasedExponent = 0
        else:
            resultBiasedExponent = (biased_exponent - self.float16bias + self.float32bias) << 23
        resultSign = sign << 31

        bitsResult.i = resultSign | resultBiasedExponent | resultMantissa

        return bitsResult.s
    def IsInfinity(self,value):
        mantissa = None
        biased_exponent = None
        mantissa = self.GetMantissa(value)
        biased_exponent = self.GetBiasedExponent(value)
        return (biased_exponent == 31) and (mantissa == 0)
    def IsNaN(self,value):
        mantissa = None
        biased_exponent = None
        mantissa = self.GetMantissa(value)
        biased_exponent = self.GetBiasedExponent(value)
        return (biased_exponent == 31) and (mantissa != 0)
    def __str__(self):
        return self.TheFloatValue
    def __repr__(self):
        return self.TheFloatValue

class IntegerAndSingleUnion:
    def __init__(self):
        self.i = 0
    @property
    def s(self):
        a = struct.pack('!I', self.i)
        return struct.unpack('!f', a)[0]


class SourceVertex:
    def __init__(self):
        self.boneWeight = SourceBoneWeight()
        self.position = SourceVector()

        self.normal = SourceVector()
        self.texCoordX = 0
        self.texCoordY = 0

    def read(self,reader:ByteIO):

        self.boneWeight.read(reader)
        self.position.read(reader)
        self.normal.read(reader)
        self.texCoordX = reader.read_float()
        self.texCoordY = reader.read_float()
        return self

    def __str__(self):
        return "<Vertex pos:{} bone weight:{}>".format(self.position.as_string,self.boneWeight)

    def __repr__(self):
        return self.__str__()

class SourceMdlTexture:
    def __init__(self):
        self.nameOffset = 0
        self.flags = 0
        self.used = 0
        self.unused1 = 0
        self.materialP = 0
        self.clientMaterialP = 0
        self.unused = []  # len 10
        self.thePathFileName = 'texture' + str(random.randint(0, 256))
    def read(self,reader:ByteIO):
        entry = reader.tell()
        self.nameOffset = reader.read_uint32()
        self.thePathFileName = reader.read_from_offset(entry+self.nameOffset,reader.read_ascii_string)
        self.flags = reader.read_uint32()
        self.used = reader.read_uint32()
        self.unused1 = reader.read_uint32()
        self.materialP = reader.read_uint32()
        self.clientMaterialP = reader.read_uint32()
        self.unused = [reader.read_uint32() for _ in range(5)]



    def __repr__(self):
        return "<MDL texture name:{}>".format(self.thePathFileName)


class SourceBoneWeight:
    def __init__(self):
        self.weight = []
        self.bone = []
        self.boneCount = b"\x00"

    def read(self,reader:ByteIO):
        self.weight = [reader.read_float() for _ in range(3)]
        self.bone = [reader.read_uint8() for _ in range(3)]
        self.boneCount = reader.read_uint8()
        return self

    def __str__(self):
        return '<BoneWeight Weight: {} Bone: {} BoneCount: {}>'.format(self.weight,self.bone,self.boneCount)
    def __repr__(self):
        return self.__str__()