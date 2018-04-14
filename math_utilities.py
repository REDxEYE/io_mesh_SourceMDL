import math

# Public Sub ConvertRotationMatrixToDegrees(m0, m1, m2, m3, m4, m5, m8, ByRef angleX As Double, ByRef angleY As Double, ByRef angleZ As Double)
# 		Dim c As Double
# 		Dim translateX As Double
# 		Dim translateY As Double
#
# 		angleY = -Math.Asin(Math.Round(m2, 6))
# 		c = Math.Cos(angleY)
# 		angleY = RadiansToDegrees(angleY)
# 		If Math.Abs(c) > 0.005 Then
# 			translateX = Math.Round(m8, 6) / c
# 			translateY = Math.Round(-m5, 6) / c
# 			angleX = RadiansToDegrees(Math.Atan2(translateY, translateX))
# 			translateX = Math.Round(m0, 6) / c
# 			translateY = Math.Round(-m1, 6) / c
# 			angleZ = RadiansToDegrees(Math.Atan2(translateY, translateX))
# 		Else
# 			angleX = 0
# 			translateX = Math.Round(m4, 6)
# 			translateY = Math.Round(m3, 6)
# 			angleZ = RadiansToDegrees(Math.Atan2(translateY, translateX))
# 		End If
# 	End Sub
def convert_rotation_matrix_to_degrees(m0, m1, m2, m3, m4, m5, m8):
    # print(m0, m1, m2, m3, m4, m5, m8)
    angleY = -math.asin(round(m2,6))
    c = math.cos(angleY)
    # angleY = math.radians(angleY)
    if abs(c) > 0.005:
        translateX = m8/c
        translateY = -m5/c
        angleX = (math.atan2(translateY,translateX))
        translateX = m0 / c
        translateY = -m1 / c
        angleZ = (math.atan2(translateY,translateX))
    else:
        angleX = 0
        translateX = m4
        translateY = m3
        angleZ = (math.atan2(translateY, translateX))
    # print(angleX,angleY,angleZ)
    return angleX,angleY,angleZ