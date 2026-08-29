from gurobipy import *

def GetVariables(round,varName,varSize,variable):
    res = []
    for i in range(varSize):
        res.append(varName + "_" + str(round) + "_" + str(i))
        variable.add(varName + "_" + str(round) + "_" + str(i))
    return res

##################################################linear_part##################################################
def Constraint_initialize_L(offset, f, variable):
    f.write("c" + " = 1 " + "\n")

    res = []
    for i in range (STATE_LENGTH):
        res.append(GetVariables(offset,"X0",STATE_LENGTH,variable)[i])
        res.append(GetVariables(offset,"X1",STATE_LENGTH,variable)[i])
        res.append(GetVariables(offset,"X2",STATE_LENGTH,variable)[i])
        res.append(GetVariables(offset,"X3",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " >= 1 " + "\n")

    for i in range (STATE_LENGTH):
        f.write(GetVariables(offset,"X0",STATE_LENGTH,variable)[i] + " - " + (str((0x00000000000000000000000800000000>>(4*i+0))&0x1)) + " c = 0 \n")
        f.write(GetVariables(offset,"X1",STATE_LENGTH,variable)[i] + " - " + (str((0x00000000000000000000000800000000>>(4*i+1))&0x1)) + " c = 0 \n")
        f.write(GetVariables(offset,"X2",STATE_LENGTH,variable)[i] + " - " + (str((0x00000000000000000000000800000000>>(4*i+2))&0x1)) + " c = 0 \n")
        f.write(GetVariables(offset,"X3",STATE_LENGTH,variable)[i] + " - " + (str((0x00000000000000000000000800000000>>(4*i+3))&0x1)) + " c = 0 \n")

    # for i in range (STATE_LENGTH):
        f.write(GetVariables(R_L + offset,"X0",STATE_LENGTH,variable)[i] + " - " + (str((0x2a00308043090ab2e02a240400801089>>(4*i+0))&0x1)) + " c = 0 \n")
        f.write(GetVariables(R_L + offset,"X1",STATE_LENGTH,variable)[i] + " - " + (str((0x2a00308043090ab2e02a240400801089>>(4*i+1))&0x1)) + " c = 0 \n")
        f.write(GetVariables(R_L + offset,"X2",STATE_LENGTH,variable)[i] + " - " + (str((0x2a00308043090ab2e02a240400801089>>(4*i+2))&0x1)) + " c = 0 \n")
        f.write(GetVariables(R_L + offset,"X3",STATE_LENGTH,variable)[i] + " - " + (str((0x2a00308043090ab2e02a240400801089>>(4*i+3))&0x1)) + " c = 0 \n")

    res = []
    for r in range (offset, offset + R_L):
        for i in range (STATE_LENGTH):
            res.append("2 " + GetVariables(r,"p_L0",STATE_LENGTH,variable)[i])
            res.append("1 " + GetVariables(r,"p_L1",STATE_LENGTH,variable)[i])
    f.write(" + ".join(res) + " = 15\n")

    # for i in range (32):
    #     f.write(GetVariables(R_L + offset,"X0",STATE_LENGTH,variable)[i] + " - " + GetVariables(offset + R_L-1,"p_L",STATE_LENGTH,variable)[i] + " <= 0\n")
    #     f.write(GetVariables(R_L + offset,"X1",STATE_LENGTH,variable)[i] + " - " + GetVariables(offset + R_L-1,"p_L",STATE_LENGTH,variable)[i] + " <= 0\n")
    #     f.write(GetVariables(R_L + offset,"X2",STATE_LENGTH,variable)[i] + " - " + GetVariables(offset + R_L-1,"p_L",STATE_LENGTH,variable)[i] + " <= 0\n")
    #     f.write(GetVariables(R_L + offset,"X3",STATE_LENGTH,variable)[i] + " - " + GetVariables(offset + R_L-1,"p_L",STATE_LENGTH,variable)[i] + " <= 0\n")
    #     f.write(GetVariables(R_L + offset,"X0",STATE_LENGTH,variable)[i] + " + " + GetVariables(R_L + offset,"X2",STATE_LENGTH,variable)[i] + " + " + \
    #             GetVariables(R_L + offset,"X3",STATE_LENGTH,variable)[i] + " + " + GetVariables(R_L + offset,"X3",STATE_LENGTH,variable)[i] + " - " + \
    #             GetVariables(offset + R_L-1,"p_L",STATE_LENGTH,variable)[i] + " >= 0\n")

    # res = []
    # DLD1 = []
    # # DLD1 = [1,6,8,11,12,15,16,17,18,20,22]
    # # DLD2 = [2,3,7,10,21,23,25,26,28,30]
    # # DLD3 = [0,5,13,27]
    # for r in range (1):
    #     for i in range (32):
    #         if (i not in DLD1):
    #             res.append(GetVariables(offset + R_L-1,"p_L",32,variable)[i])
    # # f.write(" + ".join(res) + " >= 10\n")
    # f.write(" + ".join(res) + " = 11\n")

def Constraint_sbox_L(r, f, variable):
    M0 = [[[-4, -3, -7, -2, -2, -5, 4, -10, 33, 21, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [5, 6, 8, 5, 6, 3, 2, 2, -7, -15, 0], [1, 0, -7, -2, -3, -4, -3, 2, 19, 12, 0], [-1, 0, 1, -1, 0, 0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, 1, -1, -1, 0, 1, -1], [0, 0, 0, 0, 0, 1, 1, 1, -1, 0, 0], [1, 0, 1, 1, 0, 0, 0, 0, -1, 0, 0], [-3, 5, 1, -4, 1, 6, 3, 2, 4, 0, 0], [2, -4, 1, -4, 0, -2, -1, 3, 10, 7, 0], [-1, -5, -1, 2, -6, 4, -3, -3, 15, 13, 0], [0, -1, -1, 2, 4, 2, 1, 3, 1, -2, 0], [1, 0, -1, -1, 0, 1, 0, 0, 0, 1, -1], [0, 0, 1, 0, 0, -1, 1, -1, 0, 1, -1], [-4, -1, 1, 2, -4, -2, -1, 2, 11, 8, 0], [-1, 0, -1, 1, 0, 1, 0, 0, 0, 1, -1], [-1, 0, 0, -1, 2, -1, -2, -2, 6, 5, 0], [0, 0, 1, 0, 0, -1, -1, 1, 0, 1, -1], [1, 0, 0, 1, 0, 0, 1, 1, -1, 0, 0], [-1, 0, 0, -1, 0, 0, 1, 1, 0, 1, -1], [1, 0, 0, 1, 0, 0, -1, -1, 0, 1, -1], [2, 1, -1, -3, 0, -2, -1, -2, 9, 6, 0], [2, -1, 0, 1, 1, 2, 2, -2, 3, 0, 0], [-1, 0, 0, -1, 0, 0, -1, -1, 0, 1, -3], [-1, 1, -1, 1, 0, 0, -1, -1, 0, -1, -4]],
    [[-2, -5, 4, -10, -2, -3, -4, -7, 33, 21, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [6, 3, 2, 2, 5, 6, 5, 8, -7, -15, 0], [-3, -4, -3, 2, -2, 0, 1, -7, 19, 12, 0], [0, 0, 0, 0, -1, 0, -1, 1, 0, 1, -1], [0, 1, -1, -1, 0, 0, 0, 0, 0, 1, -1], [0, 1, 1, 1, 0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 1, 0, 1, 1, -1, 0, 0], [1, 6, 3, 2, -4, 5, -3, 1, 4, 0, 0], [0, -2, -1, 3, -4, -4, 2, 1, 10, 7, 0], [-6, 4, -3, -3, 2, -5, -1, -1, 15, 13, 0], [5, 1, 2, 2, 3, -2, 1, -1, 1, -2, 0], [0, 1, 0, 0, -1, 0, 1, -1, 0, 1, -1], [0, -1, 1, -1, 0, 0, 0, 1, 0, 1, -1], [-2, -1, -1, 1, 1, 0, -2, 1, 5, 4, 0], [0, 1, 0, 0, 1, 0, -1, -1, 0, 1, -1], [2, -1, -2, -2, -3, -1, -3, -1, 11, 9, 0], [0, 0, -1, -1, 1, 0, 1, 0, 0, 1, -1], [0, 0, 1, 1, -1, 0, -1, 0, 0, 1, -1], [0, -1, -1, 1, 0, 0, 0, 1, 0, 1, -1], [3, 5, 6, 3, 1, 5, 4, 6, -4, -13, 0], [0, 0, 1, 1, 1, 0, 1, -1, 0, 1, 0], [1, -3, -2, -1, 2, 2, -5, -2, 13, 8, 0], [0, 0, -1, -1, -1, 0, -1, 0, 0, 1, -3], [1, -1, -1, -1, -2, 1, 1, 0, 5, 3, 0]],
    [[-1, -1, -7, -4, -2, -3, -3, -7, 26, 20, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [3, 1, 1, 4, 0, 2, 2, 1, -3, -5, 0], [1, 0, 0, 0, 1, 2, 2, 0, -2, -1, 0], [-7, -1, 1, 4, 5, -3, -2, 1, 13, 6, 0], [1, 0, 0, 0, 0, -1, -1, 0, 0, 1, -1], [-7, -1, 1, -4, -5, 3, 2, 1, 17, 10, 0], [0, -1, -1, 0, -2, -1, -2, 0, 5, 6, 0], [4, 3, 1, 0, 2, 1, 1, 4, -2, -5, 0], [1, -1, -1, 0, 0, 0, 0, 0, 0, 1, -1], [1, 2, 2, 0, -2, -1, -2, 1, 2, 3, 0], [-1, 1, -1, 0, -1, -1, 2, 0, 3, 2, 0], [-2, 4, -2, -1, 2, 3, -6, -1, 10, 6, 0], [3, -8, 4, -4, 5, -2, 3, -1, 15, 7, 0], [0, 1, 1, 0, 2, 1, 2, 0, -2, -1, 0], [1, -1, 1, 0, -1, 1, -2, 1, 4, 2, 0], [-1, -1, 1, 0, -1, -1, 0, 0, 0, 1, -3], [0, -1, -1, 0, 1, 0, 1, 0, 0, 1, -1], [-1, -1, 1, 0, 1, 1, 0, 0, 0, 1, -1], [1, 1, 1, 0, 0, 0, 0, 0, -1, 0, 0], [-1, 1, -1, 2, 3, 1, 0, 4, 1, -2, 0], [-2, 1, 1, 0, -1, 2, -1, -2, 5, 4, 0], [-1, -1, 1, -3, -1, -1, 2, -1, 7, 5, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, -1, 0]],
    [[-7, -8, -2, -1, -6, -4, -1, -4, 32, 23, 0], [2, 2, 3, 3, 4, 4, 4, 5, -6, -11, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [3, 5, 2, 2, -1, 1, 1, -1, 0, -3, 0], [-3, 4, -2, -2, 1, -1, -3, -2, 12, 8, 0], [0, -1, -1, -1, -3, -3, -2, 2, 8, 9, 0], [4, -3, 5, -2, 9, 2, -1, -4, 9, 1, 0], [-2, -2, -2, -1, 0, 1, 0, 1, 5, 6, 0], [4, 6, 3, 1, -2, -1, 8, 2, 0, -6, 0], [2, -1, -5, 3, -2, 2, 1, -3, 9, 6, 0], [3, 1, 3, 0, 2, 4, 4, 5, -5, -8, 0], [2, 0, 2, 1, 0, -2, -2, 1, 2, 3, 0], [2, 1, -2, 0, 2, -1, 1, 2, 2, 0, 0], [5, 3, 2, 2, -1, 6, -1, 4, -1, -6, 0], [-4, -3, -2, 5, 1, -4, 1, 3, 10, 8, 0], [0, 2, 2, 1, -2, -2, 0, 1, 2, 3, 0], [-1, -3, -5, -5, -4, -4, -2, -5, 24, 21, 0], [1, 2, 0, 2, 2, 1, -2, -2, 2, 3, 0], [-1, 1, -2, -2, 1, 2, 2, 0, 3, 4, 0], [-2, -1, 4, -3, 2, -1, -4, -2, 11, 8, 0], [-1, -1, 1, 1, -1, 0, -1, 0, 0, 1, -3], [0, -1, -1, -1, 1, 1, 0, 0, 0, 1, -2], [-4, 2, -3, 2, 5, -1, 1, -1, 8, 4, 0], [0, 0, 1, 1, 2, 2, 2, 1, -2, -3, 0], [-3, 0, 4, -1, -2, 2, 1, -3, 8, 5, 0], [1, 1, -1, -1, -1, 0, -1, 0, 0, 1, -3], [1, -1, 1, -1, 0, -1, 1, -1, 0, 1, -3], [1, -1, -1, 1, 1, -1, 0, -1, 0, 1, -3], [0, 1, 1, 0, 1, 1, 0, 1, -1, 0, 0], [-1, 0, -1, 0, 0, -1, -1, 1, 0, 1, -3], [2, 3, 2, 3, -1, -1, 2, -1, 0, -1, 0], [-1, -2, -1, -2, -1, -1, 1, -1, 7, 7, 0], [-2, -2, 1, 1, 2, 0, 2, 1, 2, 3, 0], [-1, 1, 1, -1, 1, -1, 0, -1, 0, 1, -3], [-1, 1, -1, 1, 0, -1, 1, -1, 0, 1, -3], [1, 1, -1, -1, 1, 0, 1, 0, 0, 1, -1], [1, -1, 1, -1, 0, 1, -1, -1, 0, 1, -3], [-1, 0, -1, 0, 0, 1, 1, 1, 0, 1, -1], [1, 0, 1, 1, 0, 1, 1, 0, -1, 0, 0], [0, -1, -1, 0, 1, 1, 0, 1, 0, 1, -1], [-1, -1, 0, 0, -1, 0, -1, 1, 0, 1, -3], [0, -1, -1, 0, -1, -1, 0, 1, 0, 1, -3], [-1, 1, -1, 1, 0, 1, -1, -1, 0, 0, -3], [-1, 1, 1, -1, -1, 1, 0, -1, 0, 0, -3]],
    [[-1, -3, -9, -5, -4, -4, -3, -2, 30, 21, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [4, 7, 3, 4, 2, 5, 6, 0, -9, -10, 0], [4, 3, 4, 2, 4, 2, 1, 5, -3, -10, 0], [0, 1, 0, 0, 1, 2, 2, 0, -2, -1, 0], [-1, -4, 5, -1, -2, 4, -2, 1, 9, 4, 0], [-1, 2, 2, 1, 0, -2, 1, 0, 3, 0, 0], [-2, 2, -2, -1, 0, -1, -1, 0, 5, 6, 0], [-2, -2, 4, 1, 2, -4, -1, -5, 12, 9, 0], [1, -1, -2, 2, 1, -1, -1, 1, 4, 2, 0], [-2, 1, -3, 4, -1, 2, 1, -2, 7, 4, 0], [1, 1, 1, 0, 0, -1, -1, 0, 0, 1, -1], [-2, 1, 0, -2, -1, -1, 2, 0, 4, 5, 0], [-1, -1, 0, 2, 1, 0, 3, 3, 1, -1, 0], [-1, -1, 2, 2, 2, 1, -1, 0, 1, 2, 0], [0, 0, -1, -1, 1, 1, 0, 0, 0, 1, -1], [1, 0, 0, 1, -1, -1, 1, 0, 0, 1, -1], [-2, -1, -2, 1, -2, -1, -2, 0, 8, 9, 0], [1, -1, 0, -1, 1, 0, 1, 0, 0, 1, -1], [1, 0, 1, 0, -1, -1, -1, 0, 0, 1, -2], [0, -1, 1, -1, -1, 2, -1, 0, 3, 2, 0], [2, -1, -2, -2, -1, 0, 1, -2, 8, 5, 0], [-1, 1, 0, -1, 1, 1, 0, 0, 0, -1, -2], [1, -1, -1, 0, 1, -1, -1, 0, 0, 0, -3], [0, -1, -1, 1, -1, 1, -1, 0, 0, 1, -3], [0, 1, -1, -1, 0, 1, 0, 0, 0, 1, -1], [0, 1, 1, 1, 0, 1, -1, 0, 0, 1, 0], [-1, -1, 0, 1, 1, 0, 1, 0, 0, 1, -1], [-1, -1, 1, 0, 1, -1, -1, 0, 0, 1, -3], [1, 0, 0, -1, -1, 0, 1, 0, 1, 0, -1]],
    [[-9, -3, -5, -1, -3, -4, -4, -2, 30, 21, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [3, 7, 4, 4, 6, 5, 2, 0, -9, -10, 0], [4, 3, 2, 4, 1, 2, 4, 5, -3, -10, 0], [0, 1, 0, 0, 2, 2, 1, 0, -2, -1, 0], [5, -4, -1, -1, -2, 4, -2, 1, 9, 4, 0], [2, 2, 1, -1, 1, -2, 0, 0, 3, 0, 0], [-2, 2, -1, -2, -1, -1, 0, 0, 5, 6, 0], [-2, -3, 1, 2, -3, -3, 2, -1, 10, 7, 0], [2, -3, 4, 1, 5, 3, 1, 8, 2, -6, 0], [4, -2, 1, -2, -1, -4, 2, -5, 12, 9, 0], [1, 1, 0, 1, -1, -1, 0, 0, 0, 1, -1], [-3, 1, 4, -2, 1, 2, -1, -2, 7, 4, 0], [0, 1, -2, -2, 2, -1, -1, 0, 4, 5, 0], [2, -1, 2, -1, -1, 1, 2, 0, 1, 2, 0], [-1, 0, -1, 0, 0, 1, 1, 0, 0, 1, -1], [0, 0, 1, 1, 1, -1, -1, 0, 0, 1, -1], [-2, -1, 1, -2, -2, -1, -2, 0, 8, 9, 0], [0, -1, -1, 1, 1, 0, 1, 0, 0, 1, -1], [1, 0, 0, 1, -1, -1, -1, 0, 0, 1, -2], [1, -1, -1, 0, -1, 2, -1, 0, 3, 2, 0], [-1, 3, -1, -2, -2, 1, 1, 1, 5, 3, 0], [0, -1, 1, -1, 1, 0, 1, 0, 0, 1, -1], [-1, 0, -2, 2, 1, 0, -1, -1, 5, 3, 0], [1, 1, 1, 0, 0, 1, 0, 0, -1, 0, 0], [-1, 1, -1, 0, 0, 1, 0, 0, 0, 1, -1], [-1, -1, 1, 0, -1, 1, -1, 0, 0, 1, -3], [-2, -1, 0, 1, -3, -3, 1, 1, 8, 6, 0], [1, -1, 0, -1, -1, -1, 1, 0, 0, 1, -3]],
    [[4, -5, -3, -10, -7, -2, -2, -4, 33, 21, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [1, 3, 3, 1, 4, 4, 3, 4, -5, -9, 0], [-3, -4, 0, 2, -7, -2, -3, 1, 19, 12, 0], [0, 0, 0, 0, 1, -1, 0, -1, 0, 1, -1], [-1, 1, 0, -1, 0, 0, 0, 0, 0, 1, -1], [3, 5, 2, 3, 5, 1, 0, 1, -4, -7, 0], [3, 2, -1, 3, 1, 2, 6, 2, -3, -6, 0], [0, 0, 0, 0, 1, 1, 0, 1, -1, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0, -1, 0, 0], [-1, -4, -3, 1, 2, -3, -1, -1, 11, 9, 0], [-2, 1, 2, -2, 0, -1, 3, -1, 4, 3, 0], [-3, 4, -5, -3, -1, 2, -6, -1, 15, 13, 0], [0, 1, 0, 0, -1, -1, 0, 1, 0, 1, -1], [1, -1, 0, -1, 1, 0, 0, 0, 0, 1, -1], [-1, -1, 0, 1, 1, 0, 0, 0, 0, 1, -1], [0, 1, 0, 0, -1, 1, 0, -1, 0, 1, -1], [-1, 0, 0, -1, 0, 1, 0, 1, 0, 1, -1], [1, 0, 0, 1, 0, -1, 0, -1, 0, 1, -1], [-2, -5, -2, -1, -4, 2, -3, -5, 22, 14, 0], [2, 5, 5, 1, 2, -3, 1, -2, 2, -1, 0], [1, 0, 0, 1, 0, 1, 0, 1, -1, 0, 0], [-1, 0, 0, -1, 0, -1, 0, -1, 0, 1, -3], [-1, -2, 0, -2, -1, -2, -1, 2, 9, 6, 0], [0, 1, 0, 1, 0, 2, 2, 1, 0, -2, 0], [-1, 0, -1, 1, -1, 0, 0, 0, 0, -1, -3]],
    [[-4, -1, -4, -6, -1, -2, -8, -7, 32, 23, 0], [5, 4, 4, 4, 3, 3, 2, 2, -6, -11, 0], [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1], [2, 8, -1, -2, 1, 3, 6, 4, 0, -6, 0], [-2, -3, -1, 1, -2, -2, 4, -3, 12, 8, 0], [2, -2, -3, -3, -1, -1, -1, 0, 8, 9, 0], [1, -3, 4, 1, 3, 2, 2, 6, 1, -4, 0], [1, 0, 1, 0, -1, -2, -2, -2, 5, 6, 0], [-2, 1, -1, 5, -3, 1, -3, 3, 8, 4, 0], [1, -2, -2, 0, 1, 2, 0, 2, 2, 3, 0], [-3, -2, 2, -2, 3, -2, -1, -1, 11, 6, 0], [5, 4, 4, 2, 0, 3, 1, 3, -5, -8, 0], [1, -1, -3, 3, 3, -1, 0, -2, 6, 4, 0], [-2, -4, -1, 2, -3, 4, -1, -2, 11, 8, 0], [-2, 2, -1, -2, 4, 2, 4, 3, 1, 0, 0], [-5, -2, -4, -4, -5, -5, -3, -1, 24, 21, 0], [2, -4, -3, -4, 2, 2, -1, -1, 9, 10, 0], [2, -1, 2, -1, 0, 0, 1, 1, 1, 0, 0], [0, 2, 2, 1, -2, -2, 1, -1, 3, 4, 0], [1, 2, 0, 2, 1, 1, -2, -2, 2, 3, 0], [-2, -2, 1, 2, 2, 0, 2, 1, 2, 3, 0], [2, 1, -1, 2, 0, -2, 1, 2, 2, 0, 0], [0, 0, 1, 1, -1, -1, -1, 0, 2, 3, 0], [-2, 1, 2, -1, -1, 3, 0, -2, 5, 3, 0], [-1, 0, -1, 1, 1, -1, -1, 1, 0, 1, -3], [-1, 1, -1, 0, 1, -1, 1, -1, 0, 1, -3], [-1, -1, 1, 0, -1, 1, -1, 1, 0, 1, -3], [0, 1, 1, 1, 1, 1, 0, 0, -1, 0, 0], [1, 0, 1, 1, 0, 1, 1, 0, -1, 0, 0], [1, 0, -1, -1, 0, 1, 1, 0, 0, 1, -1], [1, 0, -1, -1, 0, -1, -1, 0, 0, 1, -3], [-1, 1, 1, -1, 1, 0, 0, 1, 0, 1, -1], [-1, 1, -2, -2, -2, -1, -2, 0, 8, 9, 0], [-4, -3, 1, -1, -4, 2, 2, -3, 14, 10, 0], [-1, 0, -1, 1, -1, 1, 1, -1, 0, 1, -3], [1, -1, -1, 0, 0, -1, 0, -1, 0, 1, -3], [1, 1, 1, 0, 0, -1, 0, -1, 0, 1, -1], [0, -1, 0, -1, -1, -1, 1, 1, 0, 1, -3], [0, 1, 0, 1, -1, -1, 1, 1, 0, 1, -1], [1, -1, 0, -1, 0, 0, -1, -1, 0, 1, -3], [-1, -1, 0, -1, 1, 1, -1, -1, 0, 0, -4], [0, 0, 0, 0, -1, -1, -1, -1, 0, 1, -3], [1, 0, 1, 1, 0, -1, -1, 0, 0, 1, -1], [-1, 0, 1, -1, 1, -1, -1, 1, 0, 0, -3], [-1, -1, 1, 0, 1, -1, 1, -1, 0, 0, -3]]]
    
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
            res.append(str(M0[r%8][t][8]) + " " + GetVariables(r,"p_L0",STATE_LENGTH,variable)[i])
            res.append(str(M0[r%8][t][9]) + " " + GetVariables(r,"p_L1",STATE_LENGTH,variable)[i])
            f.write(" + ".join(res) + " - " + str(M0[r%8][t][10]) + " c" + " >= 0 " + "\n")

def Constraint_rotation_L(r, f, variable, A, a, ra, B, b, rb):
    for i in range (STATE_LENGTH):
        f.write(GetVariables(rb,B,STATE_LENGTH,variable)[(i-b)%STATE_LENGTH] + " - " + GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH] + " = 0 " + "\n")

def Constraint_shift_L(r, f, variable, A, a, ra, B, b, rb):
    for i in range (b, STATE_LENGTH):
        f.write(GetVariables(rb,B,STATE_LENGTH-b,variable)[(i-b)%STATE_LENGTH] + " - " + GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH] + " = 0 " + "\n")
    # for i in range (b):
    #     f.write(GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH] + " = 0 " + "\n")

def Constraint_two_L(r, f, variable, A, a, ra, B, b, rb, C, c, rc, d):
    M0 = [[-1, 1, 1, 0], [1, -1, 1, 0], [1, 1, -1, 0], [-1, -1, -1, -2]]
    for i in range (STATE_LENGTH-d):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH])
            res.append(str(M0[t][1]) + " " + GetVariables(rb,B,STATE_LENGTH,variable)[(i-b)%STATE_LENGTH])
            res.append(str(M0[t][2]) + " " + GetVariables(rc,C,STATE_LENGTH-d,variable)[(i-c)%STATE_LENGTH])
            f.write(" + ".join(res) + " - " + str(M0[t][3]) + " c" + " >= 0 " + "\n")
    for i in range (STATE_LENGTH-d, STATE_LENGTH):
        f.write(GetVariables(rb,B,STATE_LENGTH,variable)[(i-b)%STATE_LENGTH] + " - " + GetVariables(ra,A,STATE_LENGTH,variable)[(i-a)%STATE_LENGTH] + " = 0 " + "\n")

def Constraint_three_L(r, f, variable, A, a, ra, B, b, rb, C, c, rc, D, d, rd, e):
    M0 = [[-1, 1, 1, 1, 0], [1, -1, 1, 1, 0], [1, 1, -1, 1, 0], [-1, -1, -1, 1, -2], [1, 1, 1, -1, 0], [-1, -1, 1, -1, -2], [-1, 1, -1, -1, -2], [1, -1, -1, -1, -2]]
    M1 = [[-1, 1, 1, 0], [1, -1, 1, 0], [1, 1, -1, 0], [-1, -1, -1, -2]]
    for i in range (STATE_LENGTH-d):
        for t in range (len(M0)):
            res = []
            res.append(str(M0[t][0]) + " " + GetVariables(ra,A,STATE_LENGTH-a,variable)[(i-a)%STATE_LENGTH])
            res.append(str(M0[t][1]) + " " + GetVariables(rb,B,STATE_LENGTH-b,variable)[(i-b)%STATE_LENGTH])
            res.append(str(M0[t][2]) + " " + GetVariables(rc,C,STATE_LENGTH-c,variable)[(i-c)%STATE_LENGTH])
            res.append(str(M0[t][3]) + " " + GetVariables(rd,D,STATE_LENGTH-d,variable)[(i-d)%STATE_LENGTH])
            f.write(" + ".join(res) + " - " + str(M0[t][4]) + " c" + " >= 0 " + "\n")
    for i in range (STATE_LENGTH-d, STATE_LENGTH):
        for t in range (len(M1)):
            res = []
            res.append(str(M1[t][0]) + " " + GetVariables(ra,A,STATE_LENGTH-a,variable)[(i-a)%STATE_LENGTH])
            res.append(str(M1[t][1]) + " " + GetVariables(rb,B,STATE_LENGTH-b,variable)[(i-b)%STATE_LENGTH])
            res.append(str(M1[t][2]) + " " + GetVariables(rc,C,STATE_LENGTH-c,variable)[(i-c)%STATE_LENGTH])
            f.write(" + ".join(res) + " - " + str(M1[t][3]) + " c" + " >= 0 " + "\n")

def Constraint_L(f, variable):
    Constraint_initialize_L(offset, f, variable)
    for r in range (offset, offset + R_L):
        Constraint_sbox_L(r, f, variable)

        Constraint_rotation_L(r, f, variable, "A", 0, r, "Y0", 13, r)
        Constraint_two_L(r, f, variable, "A", 0, r, "Y1", 0, r, "B", 0, r, 0)
        Constraint_two_L(r, f, variable, "B", 0, r, "F", 0, r, "E", 0, r, 3)
        Constraint_shift_L(r, f, variable, "Y3", 0, r, "E", 3, r)
        Constraint_rotation_L(r, f, variable, "X0", 0, r+1, "F", 5, r)
        Constraint_rotation_L(r, f, variable, "C", 0, r, "Y2", 3, r)
        Constraint_three_L(r, f, variable, "C", 0, r, "Y1", 0, r, "Y3", 0, r, "G", 0, r, 0)
        Constraint_rotation_L(r, f, variable, "X2", 0, r+1, "G", 22, r)
        Constraint_rotation_L(r, f, variable, "H", 0, r, "Y1", 1, r)
        Constraint_two_L(r, f, variable, "H", 0, r, "F", 0, r, "I", 0, r, 0)
        Constraint_two_L(r, f, variable, "I", 0, r, "X1", 0, r+1, "J", 0, r, 7)
        Constraint_shift_L(r, f, variable, "G", 0, r, "J", 7, r)
        Constraint_rotation_L(r, f, variable, "K", 0, r, "Y3", 7, r)
        Constraint_three_L(r, f, variable, "K", 0, r, "F", 0, r, "G", 0, r, "X3", 0, r+1, 0)

        # # Constraint_rotation_L(r, f, variable, "A", 0, r, "Y0", 13, r)
        # Constraint_three_L(r, f, variable, "Y0", 13, r, "Y1", 0, r, "X0", 32-5, r+1, "E", 0, r, 3)
        # Constraint_shift_L(r, f, variable, "Y3", 0, r, "E", 3, r)
        # # Constraint_rotation_L(r, f, variable, "X0", 0, r+1, "F", 5, r)
        # # Constraint_rotation_L(r, f, variable, "C", 0, r, "Y2", 3, r)
        # Constraint_three_L(r, f, variable, "Y2", 3, r, "Y1", 0, r, "Y3", 0, r, "G", 0, r, 0)
        # Constraint_rotation_L(r, f, variable, "X2", 0, r+1, "G", 22, r)
        # Constraint_rotation_L(r, f, variable, "H", 0, r, "Y1", 1, r)
        # Constraint_three_L(r, f, variable, "H", 0, r, "X0", 32-5, r+1, "X1", 0, r+1, "J", 0, r, 7)
        # Constraint_shift_L(r, f, variable, "G", 0, r, "J", 7, r)
        # Constraint_rotation_L(r, f, variable, "K", 0, r, "Y3", 7, r)
        # Constraint_three_L(r, f, variable, "K", 0, r, "X0", 32-5, r+1, "G", 0, r, "X3", 0, r+1, 0)

def ObjectiveFunction_L(f, variable):
    pass
    # res = []
    # DLD1 = []
    # # DLD1 = [1,6,8,11,12,15,16,17,18,20,22]
    # # DLD2 = [2,3,7,10,21,23,25,26,28,30]
    # # DLD3 = [0,5,13,27]
    # for r in range (1):
    #     for i in range (32):
    #         if (i not in DLD1):
    #             res.append(GetVariables(offset + R_L-1,"p_L",32,variable)[i])
    # f.write(" + ".join(res) + "\n")

    # res = []
    # for r in range (offset, offset + R_L):
    #     for i in range (STATE_LENGTH):
    #         res.append("2 " + GetVariables(r,"p_L0",STATE_LENGTH,variable)[i])
    #         res.append("1 " + GetVariables(r,"p_L1",STATE_LENGTH,variable)[i])
    # f.write(" + ".join(res) + " \n")

def VariablesType(f):
    f.write("\n".join(variable) + "\n")

def CreateModel(lpFileName, variable):
    f = open(lpFileName, "w")
    f.write("Maximum\n")
    ObjectiveFunction_L(f, variable)
    f.write("Subject To\n")
    Constraint_L(f, variable)
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
    # model.write("SERPENT_l.ilp")
    model.write(solFileName)
    # if model.status == GRB.OPTIMAL:
    #     print('Optimal objective:', model.objVal)
    #     print(model.status)

if __name__ == '__main__':
    STATE_LENGTH = 32

    offset = 6
    R_L = 4

    variable = set()
    lpFileName = "SERPENT_l.lp"
    solFileName = "SERPENT_l_%d.sol" % R_L
    CreateModel(lpFileName, variable)
    SolveModel(lpFileName, solFileName)