from gurobipy import *

def GetVariables(round,varName,varSize,variable):
    res = []
    for i in range(varSize):
        res.append(varName + "_" + str(round) + "_" + str(i))
        variable.add(varName + "_" + str(round) + "_" + str(i))
    return res

##################################################differential part##################################################
def Constraint_initialize_D(offset, f, variable):
    f.write("c" + " = 1 " + "\n")

    res = []
    for i in range (STATE_LENGTH):
        res.append(GetVariables(offset,"X0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(offset,"X1",STATE_LENGTH,variable)[i])
        res.append(GetVariables(offset,"X2",STATE_LENGTH,variable)[i])
        res.append(GetVariables(offset,"X3",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(offset,"X0",STATE_LENGTH,variable)[i] + " - " + (str((0x0000000000000000100a000000000000>>(4*i))&0x1)) + " c = 0 \n")
        f.write(GetVariables(offset,"X1",STATE_LENGTH,variable)[i] + " - " + (str((0x0000000000000000100a000000000000>>(4*i+1))&0x1)) + " c = 0 \n")
        f.write(GetVariables(offset,"X2",STATE_LENGTH,variable)[i] + " - " + (str((0x0000000000000000100a000000000000>>(4*i+2))&0x1)) + " c = 0 \n")
        f.write(GetVariables(offset,"X3",STATE_LENGTH,variable)[i] + " - " + (str((0x0000000000000000100a000000000000>>(4*i+3))&0x1)) + " c = 0 \n")

    # for i in range (STATE_LENGTH):
    #     f.write(GetVariables(0,"Y0",STATE_LENGTH,variable)[i] + " - " + (str((0x001000000000a004000a224000800000>>(4*i))&0x1)) + " c = 0 \n")
    #     f.write(GetVariables(0,"Y1",STATE_LENGTH,variable)[i] + " - " + (str((0x001000000000a004000a224000800000>>(4*i+1))&0x1)) + " c = 0 \n")
    #     f.write(GetVariables(0,"Y2",STATE_LENGTH,variable)[i] + " - " + (str((0x001000000000a004000a224000800000>>(4*i+2))&0x1)) + " c = 0 \n")
    #     f.write(GetVariables(0,"Y3",STATE_LENGTH,variable)[i] + " - " + (str((0x001000000000a004000a224000800000>>(4*i+3))&0x1)) + " c = 0 \n")

    # for i in range (STATE_LENGTH):
    #     f.write(GetVariables(0,"X0",STATE_LENGTH,variable)[i] + " - " + (str((0x00C000000000A00C0004A3C000D00000>>(4*i))&0x1)) + " c = 0 \n")
    #     f.write(GetVariables(0,"X1",STATE_LENGTH,variable)[i] + " - " + (str((0x00C000000000A00C0004A3C000D00000>>(4*i+1))&0x1)) + " c = 0 \n")
    #     f.write(GetVariables(0,"X2",STATE_LENGTH,variable)[i] + " - " + (str((0x00C000000000A00C0004A3C000D00000>>(4*i+2))&0x1)) + " c = 0 \n")
    #     f.write(GetVariables(0,"X3",STATE_LENGTH,variable)[i] + " - " + (str((0x00C000000000A00C0004A3C000D00000>>(4*i+3))&0x1)) + " c = 0 \n")

    res = []
    for r in range (offset, offset + R_D):
        for i in range (STATE_LENGTH):
            res.append("2 " + GetVariables(r,"p_D0",STATE_LENGTH,variable)[i])
            res.append("1 " + GetVariables(r,"p_D1",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " = 7\n")

    res = []
    for r in range (0, offset + R_D):
        for i in range (STATE_LENGTH):
            res.append("2 " + GetVariables(r,"p_D0",STATE_LENGTH,variable)[i])
            res.append("1 " + GetVariables(r,"p_D1",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " = 26\n")

    # res = []
    # for r in range (0, offset + R_D):
    #     for i in range (STATE_LENGTH):
    #         res.append("1 " + GetVariables(r,"pp_D",STATE_LENGTH,variable)[i])
    # f.write(" + ".join(res) + " = 8\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(R_D + offset,"X0",STATE_LENGTH,variable)[i] + " - " + (str((0x00000000000000100008100002004400>>(4*i))&0x1)) + " c = 0 \n")
        f.write(GetVariables(R_D + offset,"X1",STATE_LENGTH,variable)[i] + " - " + (str((0x00000000000000100008100002004400>>(4*i+1))&0x1)) + " c = 0 \n")
        f.write(GetVariables(R_D + offset,"X2",STATE_LENGTH,variable)[i] + " - " + (str((0x00000000000000100008100002004400>>(4*i+2))&0x1)) + " c = 0 \n")
        f.write(GetVariables(R_D + offset,"X3",STATE_LENGTH,variable)[i] + " - " + (str((0x00000000000000100008100002004400>>(4*i+3))&0x1)) + " c = 0 \n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(0,"p_D0",STATE_LENGTH,variable)[i] + " - " + GetVariables(0,"pp_D",STATE_LENGTH,variable)[i] + " <= 0\n")
        f.write(GetVariables(0,"p_D1",STATE_LENGTH,variable)[i] + " - " + GetVariables(0,"pp_D",STATE_LENGTH,variable)[i] + " <= 0\n")

    # M0 = [[1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, -1, 0, 0, 0, -1, 0, -1], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, -1], [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, -1], [0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, -1], [0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, -1], [0, 0, -1, 0, 1, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, -1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -1, 0], [1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0], [-1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 1, -1, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, -1, -1, 0, 1, 0, 0, 0, -1], [0, 0, 0, 0, 1, 1, -1, 0, 0, 0, 0, 0], [0, 0, -1, 0, -1, 1, 0, 0, 1, 0, 0, -1], [0, 0, -1, 0, 0, -1, 1, 0, 1, 0, 1, -1], [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, -1], [0, 0, 0, 0, -1, -1, 0, 0, -1, 0, 0, -2], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0], [0, 0, -1, -1, 0, 0, -1, 0, 0, 0, 0, -2], [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, -1], [1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0], [1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    M0 = [[0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, -1], [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, -1], [1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, -1, 0, 0, 0, -1, 0, -1], [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, -1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, -1], [0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, -1], [0, -1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0], [0, -1, -1, 0, 1, 0, 0, 1, 1, 0, 0, -1], [0, 0, 0, 0, 1, -1, 0, -1, 0, 0, 0, -1], [0, 0, -1, 0, -1, 0, 0, -1, 0, 0, 0, -2], [0, 0, 1, 0, 0, 1, 0, -1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, 1, 1, -1, 0, 0, 0, 0, 0], [0, 0, 1, 0, -1, -1, -1, 0, 0, 0, 0, -2], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0], [1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, -1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, -1, -1, 0, 0, -1, 0, 0, -2], [0, 0, 0, 0, 0, 0, -1, 0, 0, 0, -1, -1], [0, -1, -1, 0, 0, 1, 0, 1, 1, 0, 0, -1], [0, -1, -1, -1, 0, -1, 0, 0, 1, 0, 1, -3], [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, -1], [1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0], [-1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]]
    for i in range (32):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(0,"p_D0",32,variable)[i])
            res.append(str(M0[t][1]) + " " + GetVariables(0,"p_D1",32,variable)[i])
            res.append(str(M0[t][2]) + " " + GetVariables(0,"Y3",32,variable)[i])
            res.append(str(M0[t][3]) + " " + GetVariables(0,"Y2",32,variable)[i])
            res.append(str(M0[t][4]) + " " + GetVariables(0,"Y1",32,variable)[i])
            res.append(str(M0[t][5]) + " " + GetVariables(0,"Y0",32,variable)[i])
            res.append(str(M0[t][6]) + " " + GetVariables(0,"M5",32,variable)[i])
            res.append(str(M0[t][7]) + " " + GetVariables(0,"M4",32,variable)[i])
            res.append(str(M0[t][8]) + " " + GetVariables(0,"M3",32,variable)[i])
            res.append(str(M0[t][9]) + " " + GetVariables(0,"M2",32,variable)[i])
            res.append(str(M0[t][10]) + " " + GetVariables(0,"M1",32,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[t][11]) + " c" + " >= 0 " + "\n")


def Constraint_sbox_D(r, f, variable):
    M0 = [[[1, -2, 0, 1, -2, -4, -4, -4, 14, -3, 0], [2, 6, 4, 2, 5, 4, 1, 1, -12, 8, 0], [-2, -6, -4, -2, 3, 1, -8, 7, 11, 11, 0], [1, 1, 0, 1, 2, 1, 3, 3, -3, -1, 0], [-2, -2, -5, 2, -3, -1, 5, -4, 10, 3, 0], [-4, -6, 2, -6, -4, -8, 5, 3, 20, -1, 0], [2, 0, 1, 2, 0, 0, -1, -1, 1, -1, 0], [2, -1, -3, -1, -2, 0, -2, 2, 5, 2, 0], [2, 1, 6, -5, -1, 1, 2, -3, 3, 4, 0], [-5, 0, 5, 2, -1, 1, -3, 2, 4, 3, 0], [-2, 1, -3, -2, -3, 1, -1, 1, 9, -1, 0], [-2, 0, -4, -2, 4, 0, -1, -1, 6, 3, 0], [-1, -1, 1, -1, 1, 0, -1, -1, 5, -2, 0], [1, 3, -2, 2, 4, -2, 2, 2, 0, -1, 0], [-3, -2, 0, 4, -1, -1, -2, -1, 6, 3, 0], [1, -1, 0, -1, 1, 1, 0, -1, 0, 0, -2], [0, -1, 0, 0, -1, -1, 1, 1, 0, 0, -2], [-3, -2, 0, -3, -2, 2, -1, -1, 10, -1, 0], [1, 2, -1, -2, -1, -1, 1, -2, 6, -1, 0], [1, 3, 2, 1, 0, 3, 2, 2, -5, 1, 0], [1, -1, 0, -1, 1, -1, -1, 0, 0, 0, -3], [-3, -2, 0, 3, 1, -1, -1, -2, 6, 1, 0], [1, 1, 2, 1, -2, -2, -1, -1, 4, -1, 0], [-1, 1, -1, 1, 0, -1, -1, 1, 0, 0, -3], [-1, -1, 0, 1, 1, 1, 0, 1, 0, 0, -1]],
    [[-2, -4, -4, -4, 1, -2, 1, 0, 14, -3, 0], [5, 4, 1, 1, 2, 6, 2, 4, -12, 8, 0], [3, 1, -8, 7, -2, -6, -2, -4, 11, 11, 0], [2, 1, 3, 3, 1, 1, 1, 0, -3, -1, 0], [-3, -1, 5, -4, 2, -2, -2, -5, 10, 3, 0], [-4, -8, 5, 3, -6, -6, -4, 2, 20, -1, 0], [0, 0, -1, -1, 2, 0, 2, 1, 1, -1, 0], [-2, 0, -2, 2, -1, -1, 2, -3, 5, 2, 0], [-2, 2, 4, -6, -7, -3, 1, 4, 11, 3, 0], [-1, 1, -3, 2, 2, 0, -5, 5, 4, 3, 0], [-3, 1, -1, 1, -2, 1, -2, -3, 9, -1, 0], [3, 0, -1, -1, -2, 0, -1, -3, 5, 2, 0], [1, 0, -1, -1, -1, -1, -1, 1, 5, -2, 0], [4, -2, 2, 2, 1, 3, 2, -2, 0, -1, 0], [1, -1, -3, -1, -4, -2, 4, 0, 7, 2, 0], [0, -1, -2, -1, 3, -1, -3, 0, 5, 2, 0], [-1, -1, 1, -2, -2, 2, 1, -1, 6, -1, 0], [0, 0, 1, 1, 1, -1, 1, 0, 0, 0, 0], [0, 4, 2, 2, 2, 4, 1, 3, -6, 1, 0], [-3, -3, -2, -2, 1, 1, 1, 3, 7, -1, 0], [-2, 2, -1, -1, -3, -2, -3, 0, 10, -1, 0], [1, 2, -1, 0, 1, -2, -3, -2, 5, 2, 0], [0, -1, -1, 1, 1, 1, -1, -1, 0, 0, -3], [1, 1, 1, 0, -1, -1, 1, 0, 0, 0, -1], [1, -1, 0, -1, 1, -1, -1, 0, 0, 0, -3]],
    [[-3, -3, -1, -7, -3, -3, -1, -2, 15, 5, 0], [5, 5, 2, 6, 1, -1, -1, 2, -3, -3, 0], [-1, -2, -1, 5, 3, 3, 4, 3, -5, 6, 0], [-3, 1, -4, 5, -2, 2, -2, -5, 11, -1, 0], [0, 2, 2, 0, 4, 1, 1, 2, -4, 1, 0], [2, -3, -2, -5, -6, 1, 1, -1, 9, 7, 0], [0, -2, 2, 2, 1, -1, -1, -2, 4, -1, 0], [0, -1, -1, -1, 2, 2, 2, 1, 1, -1, 0], [1, 2, -1, -5, 1, 1, -5, -2, 8, 3, 0], [0, 0, 0, 1, -1, -1, 1, 2, 0, 1, 0], [0, 1, -1, 0, -1, -2, 2, -2, 5, -1, 0], [1, -2, 2, -1, -2, 1, 1, -3, 6, -1, 0], [-4, 2, 1, -1, -2, -2, -2, 1, 7, 2, 0], [3, 4, 2, 1, 1, 4, 4, 2, -5, -1, 0], [3, -8, 2, -7, -3, -1, -3, 1, 14, 5, 0], [-2, 1, -2, -1, 1, -3, 2, -3, 8, 0, 0], [10, -3, -2, -6, 3, 2, -8, 1, 9, 7, 0], [0, 0, 0, 1, -1, 1, -1, 0, 0, -1, -2], [-1, 2, -2, -3, -1, 1, -2, 1, 6, 1, 0], [-1, -1, 1, -1, -1, 1, 0, 0, 0, 0, -3], [0, -2, -2, -1, 1, -1, -1, 2, 6, -1, 0], [0, 0, 1, 1, 0, 1, 1, -1, 0, 1, 0], [-1, -1, 0, -1, 1, 0, 1, 1, 0, 0, -2], [1, 1, 0, 0, 1, 0, 1, 1, 0, -1, 0]],
    [[1, -4, -2, -6, -5, -5, -1, -6, 25, -2, 0], [-3, 4, 2, -6, 0, 5, -1, 2, -1, 11, 0], [2, 3, 2, 4, 4, 3, 3, 2, -9, 2, 0], [-1, -4, -3, 5, -1, -6, 2, 0, 8, 7, 0], [-4, -1, 4, 3, -3, 8, -9, -5, 8, 10, 0], [3, 4, -1, 2, -3, -1, -3, 5, 7, -5, 0], [5, -3, 1, -7, 3, -6, -4, -2, 15, 2, 0], [2, -2, -2, 1, 4, 3, 6, 7, 0, -3, 0], [-3, -2, 3, -1, -3, -1, 2, -1, 11, -4, 0], [3, -1, -2, 1, -1, -1, 4, -4, 4, 3, 0], [-1, 2, 3, 1, 2, -3, 2, -2, 4, -2, 0], [-3, -2, -2, -1, 4, 4, -2, -4, 11, -1, 0], [1, 1, -3, -2, 5, -4, -6, 1, 9, 3, 0], [2, 1, 2, 3, -1, -2, -2, 0, 3, -1, 0], [2, 3, 4, -3, -5, 2, 1, 1, 0, 6, 0], [-2, -1, -2, 4, -1, 3, 3, 1, 4, -2, 0], [1, 0, 1, 1, 2, 3, 0, 1, -3, 1, 0], [2, 1, -1, -1, 3, 1, 3, 1, 1, -2, 0], [-2, -1, 1, -2, -1, -1, -1, 1, 7, -1, 0], [3, -1, -3, -2, -2, 1, -3, -2, 11, -1, 0], [-1, -1, -1, 1, 1, -1, -1, 0, 0, 0, -4], [-1, -1, -1, -1, 0, 0, 1, -1, 0, 0, -4], [0, 1, 0, 1, -1, -1, 0, -1, 0, -1, -3], [1, 1, 0, 1, 1, 1, 0, -1, 0, 0, 0], [1, -1, -1, -1, 0, 0, 1, 1, 0, -1, -3], [-1, 1, -1, -1, 0, 0, -1, -1, 0, 0, -4], [1, 0, 1, 1, 0, 1, 1, 0, 0, -1, 0], [-1, 1, -1, 0, 0, 1, 1, 1, 0, 0, -1]],
    [[-7, -5, -4, -3, 1, -2, -1, -8, 22, 3, 0], [4, 3, -2, 1, -3, 7, 3, 5, -8, 12, 0], [2, 0, 3, 2, 3, 1, 0, 4, -4, -1, 0], [7, 3, 1, 6, -4, -7, 2, -5, 4, 9, 0], [-2, 3, -2, -2, -1, -1, 0, 3, 4, 1, 0], [-1, -4, 4, -5, 0, 1, 2, -6, 8, 8, 0], [3, -4, -3, 1, -1, -4, -2, 2, 11, -1, 0], [3, 4, 3, 2, 2, 2, 2, 1, -7, 1, 0], [-1, -4, 4, 1, -1, 2, -4, 1, 8, -2, 0], [-3, 2, -3, 1, 5, 1, -5, -2, 7, 4, 0], [-3, 2, -3, 1, 5, 1, 5, 3, 2, -1, 0], [-4, 1, 2, -3, -4, 0, -1, 2, 8, 1, 0], [2, -3, -3, -2, 1, 1, 3, -2, 5, 2, 0], [1, 2, 2, -1, -2, -3, -3, -1, 9, -2, 0], [-2, 1, -2, -2, 1, 3, -1, -1, 7, -2, 0], [-1, -3, 2, 2, -2, 1, 7, -4, 2, 6, 0], [1, -4, 2, -2, 2, -2, -1, -1, 6, 2, 0], [1, -2, -2, 1, -3, 1, -3, -3, 11, -1, 0], [-3, 6, 2, 1, -2, -3, -2, -4, 8, 3, 0], [2, 1, -1, 0, 0, -1, 1, -1, 1, 1, 0], [0, 0, -1, -1, 1, -1, -1, 1, 0, -1, -4], [-1, 0, -1, 1, -1, -1, 0, 1, 0, 0, -3], [-1, -1, 2, -2, -2, -1, 1, 1, 6, -1, 0], [1, 1, 0, 1, 0, 1, 0, 1, 0, -1, 0], [-1, 1, -1, 0, -1, 1, 1, -1, 0, 0, -3], [0, 1, 1, 1, -1, -1, 1, 0, 0, -1, -2], [-1, -1, 1, 0, 1, 0, -1, -1, 0, 0, -3], [0, 1, 1, -1, 1, -1, 1, -1, 0, 0, -2]],
    [[-4, -5, -3, -7, -1, -2, 1, -8, 22, 3, 0], [-2, 3, 1, 4, 3, 7, -3, 5, -8, 12, 0], [3, 0, 2, 2, 0, 1, 3, 4, -4, -1, 0], [4, 0, -1, -1, 2, 1, 0, -2, 0, 4, 0], [-2, 3, -2, -2, 0, -1, -1, 3, 4, 1, 0], [1, 3, 6, 7, 2, -7, -4, -5, 4, 9, 0], [-3, -4, 1, 3, -2, -4, -1, 2, 11, -1, 0], [4, 5, 3, 5, 3, 2, 3, 1, -9, 1, 0], [4, -4, 1, -1, -4, 2, -1, 1, 8, -2, 0], [-3, 2, 1, -3, -7, 1, 7, -4, 9, 6, 0], [-2, 1, 3, -3, 5, -3, 2, 4, 4, -1, 0], [2, 1, -3, -4, -1, 0, -4, 2, 8, 1, 0], [-1, -1, -3, 3, 4, -2, 2, -3, 4, 3, 0], [-4, 2, -2, -4, 1, 4, 1, -1, 11, -4, 0], [2, 2, -1, 1, -3, -3, -2, -1, 9, -2, 0], [2, -1, 1, -2, 3, -1, -2, -2, 5, 1, 0], [-1, -2, -1, 0, -1, 2, -2, -2, 7, 0, 0], [0, 0, 1, -1, -1, -1, 0, -1, 0, -1, -4], [2, -4, -2, 1, -1, -2, 2, -1, 6, 2, 0], [-1, 1, -2, -2, -2, 3, 2, -1, 6, -1, 0], [1, 2, 3, 2, 4, 6, 4, 3, -9, 2, 0], [0, 1, 1, 1, -1, 1, -1, 0, 0, 0, -1], [-2, 1, -3, 2, -1, -3, -2, 1, 9, -1, 0], [1, -1, 1, 0, 1, 1, -1, -1, 0, 0, -2], [0, -1, 0, 1, 1, -1, -1, 1, 0, -1, -3], [-1, 0, -1, -1, 0, 0, 1, 1, 0, -1, -3], [-1, 0, 1, -1, 0, -1, -1, 1, 0, 0, -3], [1, 1, -1, 0, 1, -1, 1, -1, 0, 0, -2]],
    [[-4, -4, -2, -4, 0, 1, -2, 1, 14, -3, 0], [1, 4, 6, 1, 4, 2, 5, 2, -12, 8, 0], [7, 1, -6, -8, -4, -2, 3, -2, 11, 11, 0], [3, 1, 1, 3, 0, 1, 2, 1, -3, -1, 0], [-4, -1, -2, 5, -5, -2, -3, 2, 10, 3, 0], [3, -8, -6, 5, 2, -4, -4, -6, 20, -1, 0], [-1, 0, 0, -1, 1, 2, 0, 2, 1, -1, 0], [-1, 1, -3, -2, 0, 4, -1, -4, 6, 5, 0], [1, 1, 1, -1, -3, -2, -3, -2, 9, -1, 0], [2, 1, 0, -3, 5, -5, -1, 2, 4, 3, 0], [-1, 0, -1, -1, 1, -1, 1, -1, 5, -2, 0], [3, -1, 0, -3, -4, 1, -1, -2, 7, 2, 0], [-2, -1, 2, 3, -1, 1, 3, 1, -1, 3, 0], [-2, 0, -1, 2, 2, 1, -2, -3, 5, 1, 0], [1, 0, -1, 1, 0, 2, -1, 2, 1, -1, 0], [-2, -6, 1, -5, 3, -2, -6, 4, 16, -1, 0], [-3, 0, -2, -3, -2, -1, 2, -1, 10, -1, 0], [1, 2, 2, 1, 0, 1, -1, -1, 1, -1, 0], [0, 1, -1, 1, 0, 1, 1, -1, 0, 0, -1], [-2, 0, 0, 0, -1, -2, 1, 1, 3, 2, 0], [-1, 2, -2, -1, 0, -3, -2, -3, 10, -1, 0], [2, -1, 2, 2, -1, 1, 3, 1, -1, -1, 0], [-1, 0, 1, 1, -1, 0, -1, -1, 4, -1, 0], [0, -1, 1, -1, 1, 1, -1, 0, 0, -1, -3], [0, -1, -1, 1, 1, 0, 1, 1, 0, -1, -2], [0, 1, 1, 1, 1, 0, 0, 1, -1, 0, 0], [0, 1, -1, -1, 0, -1, 1, 1, 0, 0, -2], [0, -1, -1, -1, 1, 1, 1, 0, 0, 0, -2]],
    [[-6, -1, -5, -5, -6, -2, -4, 1, 25, -2, 0], [2, -1, 5, 0, -6, 2, 4, -3, -1, 11, 0], [2, 3, 3, 4, 4, 2, 3, 2, -9, 2, 0], [0, 2, -6, -1, 5, -3, -4, -1, 8, 7, 0], [-5, -9, 8, -3, 3, 4, -1, -4, 8, 10, 0], [2, -2, -1, -2, 1, 0, 2, 1, 4, -2, 0], [-2, -4, -6, 3, -7, 1, -3, 5, 15, 2, 0], [7, 6, 3, 4, 1, -2, -2, 2, 0, -3, 0], [-2, 2, -3, 2, 1, 3, 2, -1, 4, -2, 0], [-1, 1, 0, -3, -1, 2, -2, -3, 10, -3, 0], [-6, 6, -2, -2, 1, -3, -2, 4, 7, 5, 0], [-2, -3, 1, 1, -1, -2, 1, -4, 7, 3, 0], [4, -2, -4, 3, -3, -2, -2, -1, 11, -1, 0], [1, 2, 2, -1, 3, -1, -1, -1, 3, -2, 0], [1, 1, 2, -5, -3, 4, 3, 2, 0, 6, 0], [-1, -1, -1, 1, 2, 3, 1, 2, 2, -2, 0], [-2, 1, 2, 2, -2, -3, -3, -1, 9, -1, 0], [5, 3, 4, 5, 1, 2, 0, 2, -7, 1, 0], [-1, -3, 2, -4, -1, -3, -2, 3, 10, 1, 0], [-1, 0, -1, -1, 1, 0, 1, 0, 0, -1, -3], [0, 1, -2, -1, -1, -2, 1, 2, 5, -1, 0], [-1, -5, -1, 2, 3, -4, -2, -2, 9, 4, 0], [-1, 1, 2, 2, 1, -1, 2, 2, -2, 2, 0], [-1, -1, 1, 0, 0, 1, -1, -1, 0, 0, -3], [0, 1, -1, 0, -1, 1, 1, -1, 0, 0, -2], [0, 1, 1, -1, 1, 0, -1, 0, 0, -1, -2], [1, 1, 1, 0, 0, -1, 1, -1, 0, 0, -1]]]
    for i in range (STATE_LENGTH):
        for t in range (len(M0[r%8])):
            res = []
            res.append(str(M0[r%8][t][0]) + " " + GetVariables(r,"X3",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][1]) + " " + GetVariables(r,"X2",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][2]) + " " + GetVariables(r,"X1",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][3]) + " " + GetVariables(r,"X0",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][4]) + " " + GetVariables(r,"Y3",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][5]) + " " + GetVariables(r,"Y2",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][6]) + " " + GetVariables(r,"Y1",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][7]) + " " + GetVariables(r,"Y0",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][8]) + " " + GetVariables(r,"p_D0",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][9]) + " " + GetVariables(r,"p_D1",STATE_LENGTH,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[r%8][t][10]) + " c" + " >= 0 " + "\n")

def Constraint_rotation_D(r, f, variable, A, a, ra, B, b, rb):
    for i in range (STATE_LENGTH):
        f.write(GetVariables(rb,B,STATE_LENGTH,variable)[(i-b)%STATE_LENGTH] + " - " + GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH] + " = 0 " + "\n")

def Constraint_shift_D(r, f, variable, A, a, ra, B, b, rb):
    for i in range (b, STATE_LENGTH):
        f.write(GetVariables(rb,B,STATE_LENGTH,variable)[(i-b)%STATE_LENGTH] + " - " + GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH] + " = 0 " + "\n")
    for i in range (b):
        f.write(GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH] + " = 0 " + "\n")

def Constraint_three_xor_D(r, f, variable, A, a, ra, B, b, rb, C, c, rc, D, d, rd):
    M0 = [[-1, 1, 1, 1, 0], [1, -1, 1, 1, 0], [1, 1, -1, 1, 0], [-1, -1, -1, 1, -2], [1, 1, 1, -1, 0], [-1, -1, 1, -1, -2], [-1, 1, -1, -1, -2], [1, -1, -1, -1, -2]]

    for i in range (STATE_LENGTH):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH])
            res.append(str(M0[t][1]) + " " + GetVariables(rb,B,STATE_LENGTH,variable)[(i-b)%STATE_LENGTH])
            res.append(str(M0[t][2]) + " " + GetVariables(rc,C,STATE_LENGTH,variable)[(i-c)%STATE_LENGTH])
            res.append(str(M0[t][3]) + " " + GetVariables(rd,D,STATE_LENGTH,variable)[(i-d)%STATE_LENGTH])
            f.write(" + ".join(res) + " - " + str(M0[t][4]) + " c" + " >= 0 " + "\n")

def Constraint_D(f, variable):
    Constraint_initialize_D(offset, f, variable)
    for r in range (0, offset + R_D):
        Constraint_sbox_D(r, f, variable)
        # Constraint_rotation_D(r, f, variable, "A", 0, r, "Y0", 13, r)
        # Constraint_rotation_D(r, f, variable, "B", 0, r, "Y2", 3, r)
        # Constraint_three_xor_D(r, f, variable, "C", 0, r, "Y1", 0, r, "A", 0, r, "B", 0, r)
        # Constraint_shift_D(r, f, variable, "D", 0, r, "A", 3, r)
        # Constraint_three_xor_D(r, f, variable, "E", 0, r, "Y3", 0, r, "B", 0, r, "D", 0, r)
        # Constraint_rotation_D(r, f, variable, "X1", 0, r+1, "C", 1, r)
        # Constraint_rotation_D(r, f, variable, "X3", 0, r+1, "E", 7, r)
        # Constraint_three_xor_D(r, f, variable, "H", 0, r, "A", 0, r, "X1", 0, r+1, "X3", 0, r+1)
        # Constraint_shift_D(r, f, variable, "I", 0, r, "X1", 7, r+1)
        # Constraint_three_xor_D(r, f, variable, "J", 0, r, "B", 0, r, "X3", 0, r+1, "I", 0, r)
        # Constraint_rotation_D(r, f, variable, "X0", 0, r+1, "H", 5, r)
        # Constraint_rotation_D(r, f, variable, "X2", 0, r+1, "J", 22, r)

        # Constraint_rotation_D(r, f, variable, "A", 0, r, "Y0", 13, r)
        # Constraint_rotation_D(r, f, variable, "B", 0, r, "Y2", 3, r)
        Constraint_three_xor_D(r, f, variable, "X1", 32-1, r+1, "Y1", 0, r, "Y0", 13, r, "Y2", 3, r)
        Constraint_shift_D(r, f, variable, "D", 0, r, "Y0", 16, r)
        Constraint_three_xor_D(r, f, variable, "X3", 32-7, r+1, "Y3", 0, r, "Y2", 3, r, "D", 0, r)
        # Constraint_rotation_D(r, f, variable, "X1", 0, r+1, "C", 1, r)
        # Constraint_rotation_D(r, f, variable, "X3", 0, r+1, "E", 7, r)
        Constraint_three_xor_D(r, f, variable, "X0", 32-5, r+1, "Y0", 13, r, "X1", 0, r+1, "X3", 0, r+1)
        Constraint_shift_D(r, f, variable, "I", 0, r, "X1", 7, r+1)
        Constraint_three_xor_D(r, f, variable, "X2", 32-22, r+1, "Y2", 3, r, "X3", 0, r+1, "I", 0, r)
        # Constraint_rotation_D(r, f, variable, "X0", 0, r+1, "H", 5, r)
        # Constraint_rotation_D(r, f, variable, "X2", 0, r+1, "J", 22, r)    

def ObjectiveFunction_D(f, variable):
    res = []
    for r in range (0, 1):
        for i in range (32):
            res.append("12 " + GetVariables(0,"M5",32,variable)[i])
            res.append("10 " + GetVariables(0,"M4",32,variable)[i])
            res.append("8 " + GetVariables(0,"M3",32,variable)[i])
            res.append("6 " + GetVariables(0,"M2",32,variable)[i])
            res.append("4 " + GetVariables(0,"M1",32,variable)[i])
    f.write(" + ".join(res) + "\n")

def VariablesType(f):
    f.write("\n".join(variable) + "\n")

def CreateModel(lpFileName, variable):
    f = open(lpFileName, "w")
    f.write("Minimum\n")
    ObjectiveFunction_D(f, variable)
    f.write("Subject To\n")
    Constraint_D(f, variable)
    f.write("Binaries\n")
    VariablesType(f)
    f.write("End\n")
    f.close()

def SolveModel(lpFileName, solFileName):
    model = read(lpFileName)
    # model.setParam('OutputFlag', 0)
    # model.Params.PoolSearchMode = 2
    # model.Params.PoolSolutions = 200000000
    model.optimize()
    # model.computeIIS()
    # model.write("LELBC_dl.ilp")
    model.write(solFileName)
    # if model.status == GRB.OPTIMAL:
    #     print('Optimal objective:', model.objVal)
    #     print(model.status)

if __name__ == '__main__':
    STATE_LENGTH = 32

    offset = 1
    R_D = 2

    variable = set()
    lpFileName = "SERPENT_d.lp"
    solFileName = "SERPENT_d_%d.sol" % R_D
    CreateModel(lpFileName, variable)
    SolveModel(lpFileName, solFileName)