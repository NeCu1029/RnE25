import random
import ctypes
from math import comb

move = [
    [0, 1, 2, 3, 4, 5],
    [0, 2, 3, 4, 5, 6],
    [0, 3, 4, 5, 6, 7],
    [0, 4, 5, 6, 7, 8],
    [0, 5, 6, 7, 8, 9],
    [0, 21, 22, 23, 24, 25],
    [0, 7, 8, 9, 10, 11],
    [0, 8, 9, 10, 11, 12],
    [0, 9, 10, 11, 12, 13],
    [0, 10, 11, 12, 13, 14],
    [0, 26, 27, 23, 28, 29],
    [0, 12, 13, 14, 15, 16],
    [0, 13, 14, 15, 16, 17],
    [0, 14, 15, 16, 17, 18],
    [0, 15, 16, 17, 18, 19],
    [0, 16, 17, 18, 19, 20],
    [0, 17, 18, 19, 20, 30],
    [0, 18, 19, 20, 30, 30],
    [0, 19, 20, 30, 30, 30],
    [0, 20, 30, 30, 30, 30],
    [0, 30, 30, 30, 30, 30],
    [0, 22, 23, 24, 25, 15],
    [0, 23, 24, 25, 15, 16],
    [0, 28, 29, 20, 30, 30],
    [0, 25, 15, 16, 17, 18],
    [0, 15, 16, 17, 18, 19],
    [0, 27, 23, 28, 29, 20],
    [0, 23, 28, 29, 20, 30],
    [0, 29, 20, 30, 30, 30],
    [0, 20, 30, 30, 30, 30],
    [0, 30, 30, 30, 30, 30],
]
p = 0.46  # 둥근 면 확률
ps = (
    [0] + [p ** (4 - i) * (1 - p) ** i * comb(4, i) for i in range(1, 5)] + [p**4]
)  # 도개걸윷모 확률
c1 = ctypes.WinDLL("./minimax.so")
c2 = ctypes.WinDLL("./mm_nnue.so")
bef1 = c1.bef
bef1.argtypes = [ctypes.c_int] * 10 + [ctypes.c_double] * 2
bef1.restype = ctypes.c_double
alloc = c2.alloc
dealloc = c2.dealloc
bef2 = c2.bef
bef2.argtypes = [ctypes.c_int] * 10 + [ctypes.c_double] * 2 + [ctypes.c_int]
bef2.restype = ctypes.c_double


def rand_float(a, b):
    return random.random() * (b - a) + a


def ev(
    w1: int,
    w2: int,
    w3: int,
    w4: int,
    b1: int,
    b2: int,
    b3: int,
    b4: int,
    turn: int,
    no: int,
) -> float:
    if no == -1:
        return bef1(w1, w2, w3, w4, b1, b2, b3, b4, turn, 4, -100000.0, 100000.0)
    return bef2(w1, w2, w3, w4, b1, b2, b3, b4, turn, 4, -100000.0, 100000.0, no)


def fight(no1: int, no2: int):  # 시뮬레이션 1회 시행 (백 승 -> 0, 흑 승 -> 1)
    wh = [0, 0, 0, 0]
    bl = [0, 0, 0, 0]
    turn = 0

    while True:
        rd = random.random()
        sq = 0
        for i in range(1, 6):
            if rd <= ps[i]:
                sq = i
                break
            else:
                rd -= ps[i]
        ww, bb = wh[:], bl[:]

        if turn:  # 흑 차례
            move_mal, res, tu = 0, 1 << 30, 0
            for i in range(4):
                wh, bl = ww[:], bb[:]
                ori = bl[i]
                catch = False
                if ori == 30:
                    continue
                for j in range(4):
                    if bl[j] == ori and (ori > 0 or i == j):
                        bl[j] = move[ori][sq]  # 업기
                    if wh[j] == move[ori][sq] and wh[j] < 30:
                        wh[j] = 0  # 잡기
                        catch = True

                cur = ev(
                    wh[0],
                    wh[1],
                    wh[2],
                    wh[3],
                    bl[0],
                    bl[1],
                    bl[2],
                    bl[3],
                    int(sq in (4, 5) or catch),
                    no2,
                )
                if cur < res:
                    move_mal, res, tu = i, cur, int(sq in (4, 5) or catch)

            wh, bl = ww[:], bb[:]
            ori = bb[move_mal]
            for j in range(4):
                if bl[j] == ori and (ori > 0 or move_mal == j):
                    bl[j] = move[ori][sq]  # 업기
                if wh[j] == move[ori][sq] and wh[j] < 30:
                    wh[j] = 0  # 잡기
            turn = tu

        else:  # 백 차례
            move_mal, res, tu = 0, -(1 << 30), 0
            for i in range(4):
                wh, bl = ww[:], bb[:]
                ori = wh[i]
                catch = False
                if ori == 30:
                    continue
                for j in range(4):
                    if wh[j] == ori and (ori > 0 or i == j):
                        wh[j] = move[ori][sq]  # 업기
                    if bl[j] == move[ori][sq] and bl[j] < 30:
                        bl[j] = 0  # 잡기
                        catch = True

                cur = ev(
                    wh[0],
                    wh[1],
                    wh[2],
                    wh[3],
                    bl[0],
                    bl[1],
                    bl[2],
                    bl[3],
                    1 - int(sq in (4, 5) or catch),
                    no1,
                )
                if cur > res:
                    move_mal, res, tu = i, cur, 1 - int(sq in (4, 5) or catch)

            wh, bb = ww[:], bb[:]
            ori = ww[move_mal]
            for j in range(4):
                if wh[j] == ori and (ori > 0 or move_mal == j):
                    wh[j] = move[ori][sq]  # 업기
                if bl[j] == move[ori][sq] and bl[j] < 30:
                    bl[j] = 0  # 잡기
            turn = tu

        if wh == [30] * 4:
            return 0
        elif bl == [30] * 4:
            return 1
        print(wh, bl, res)


alloc()
fight(19, -1)
dealloc()
