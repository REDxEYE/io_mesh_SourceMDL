import random
from pprint import pformat

import sys,struct

debug_write = lambda *text: sys.stderr.write(' '.join([pformat(t) for t in text])+'\n')
class SourceBoneWeight:
    def __init__(self):
        self.weight = []
        self.bone = []
        self.boneCount = b"\x00"
    def __str__(self):
        return 'Weight: {} Bone: {} BoneCount: {}'.format(self.weight,self.bone,self.boneCount)
    def __repr__(self):
        return self.__str__()


class SourceVertex:
    def __init__(self):
        self.boneWeight = SourceBoneWeight()
        self.positionX = 0
        self.positionY = 0
        self.positionZ = 0
        self.normalX = 0
        self.normalY = 0
        self.normalZ = 0
        self.texCoordX = 0
        self.texCoordY = 0

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)


class SourceVector:
    def __init__(self,data = None):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        if data:
            self.x = struct.unpack('f', data.read(4))[0]
            self.y = struct.unpack('f', data.read(4))[0]
            self.z = struct.unpack('f', data.read(4))[0]
    @staticmethod
    def gen(data):
        a = SourceVector()
        a.x = struct.unpack('f', data.read(4))[0]
        a.y = struct.unpack('f', data.read(4))[0]
        a.z = struct.unpack('f', data.read(4))[0]
        return a

    def __getattr__(self, item):
        if item == 'x':
            return self.x
        elif item == 'y':
            return self.y
        elif item == 'z':
            return self.z
        else:
            return self.__dict__[item]

    @property
    def asList(self):
        return [self.x, self.y, self.z]
    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceQuaternion:
    def __init__(self, data):
        self.x = struct.unpack('f', data.read(4))[0]
        self.y = struct.unpack('f', data.read(4))[0]
        self.z = struct.unpack('f', data.read(4))[0]
        self.w = struct.unpack('f', data.read(4))[0]

    def __getattr__(self, item):
        if item == 'x':
            return self.x
        elif item == 'y':
            return self.y
        elif item == 'z':
            return self.z
        elif item == 'w':
            return self.w
        else:
            return self.__dict__[item]

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlTexture:
    def __init__(self):
        self.nameOffset = 0
        self.flags = 0
        self.used = 0
        self.unused1 = 0
        self.materialP = 0
        self.clientMaterialP = 0
        self.unused = []  # len 10
        self.thePathFileName = 'texture' + pformat(random.randint(0, 256))

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

class SourceMdlAnimationDescBase:
    def __init__(self):
        self.theName = ''


class SourceFloat16bits:
    float32bias = 127
    float16bias = 15
    maxfloat16bits = 65504.0
    half_denorm = (1.0 / 16384.0)

    def __init__(self):
        self.the16BitValue = 0

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
        return pformat(self.TheFloatValue)
    def __repr__(self):
        return self.__str__()
class IntegerAndSingleUnion:
    def __init__(self):
        self.i = 0
    @property
    def s(self):
        a = struct.pack('!I', self.i)
        return struct.unpack('!f', a)[0]


if __name__ == '__main__':
    a = SourceFloat16bits()
    a.the16BitValue = 32769
    print(a.TheFloatValue)
