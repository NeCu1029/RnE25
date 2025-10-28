import ctypes
import random
import pickle
from math import comb

PATH = "C:/Users/ljw10/Desktop/LeeJunWoo/gshs/research/grade1/codes_final/minimax.so"
c = ctypes.cdll.LoadLibrary(PATH)
c.ev.restype = ctypes.c_double
c.bef.restype = ctypes.c_double

MOVES = [
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
P = 0.46  # 둥근 면 확률
PS = (
    [0] + [P ** (4 - i) * (1 - P) ** i * comb(4, i) for i in range(1, 5)] + [P**4]
)  # 도개걸윷모 확률
DEPTH = 8
EQ_NEED = 10000
NEQ_NEED = 15000


def static(
    w1: int, w2: int, w3: int, w4: int, b1: int, b2: int, b3: int, b4: int
) -> float:
    """winning rate using static evaluation function"""
    return c.ev(w1, w2, w3, w4, b1, b2, b3, b4, 0)


def minimax(
    w1: int, w2: int, w3: int, w4: int, b1: int, b2: int, b3: int, b4: int
) -> float:
    """winning rate using minimax search"""
    return c.bef(w1, w2, w3, w4, b1, b2, b3, b4, 0, DEPTH, -100000, 100000)


def collect(n: int) -> set[tuple[int, ...]]:
    """collecting positions by n games"""
    res = set()

    for _ in range(n):
        wh = [0, 0, 0, 0]
        bl = [0, 0, 0, 0]
        turn = 0

        while True:
            rd = random.random()
            sq = 0
            for i in range(1, 6):
                if rd <= PS[i]:
                    sq = i
                    break
                else:
                    rd -= PS[i]

            if turn:
                res.add(tuple(bl) + tuple(wh))
                mal = random.randint(0, 3)
                catch = False
                ori = bl[mal]
                for j in range(4):
                    if bl[j] == ori and (ori > 0 or mal == j):
                        bl[j] = MOVES[ori][sq]
                    if wh[j] == MOVES[ori][sq] and wh[j] < 30:
                        wh[j] = 0
                        catch = True
                turn = int(sq in (4, 5) or catch)
            else:
                res.add(tuple(wh) + tuple(bl))
                mal = random.randint(0, 3)
                catch = False
                ori = wh[mal]
                for j in range(4):
                    if wh[j] == ori and (ori > 0 or mal == j):
                        wh[j] = MOVES[ori][sq]
                    if bl[j] == MOVES[ori][sq] and bl[j] < 30:
                        bl[j] = 0
                        catch = True
                turn = 1 - int(sq in (4, 5) or catch)

            if sum(wh) == 120 or sum(bl) == 120:
                break

    return res


res = set()
eq_w, eq_b = 0, 0
neq_w, neq_b = 0, 0
while eq_w + eq_b < EQ_NEED or neq_b + neq_b < NEQ_NEED:
    positions = collect(100)
    for i in positions:
        ev = static(*i)
        mm = minimax(*i)
        if abs(ev - mm) >= 6.0:
            continue
        if mm <= 1.0 or mm >= 99.0:
            continue

        catchable = [0] * 6
        wh, bl = i[:4], i[4:]
        for j in wh:
            for k in range(1, 6):
                if MOVES[j][k] in wh or MOVES[j][k] in bl:
                    catchable[k] = 1
        catch_p = sum([catchable[x] * PS[x] for x in range(1, 6)])
        if catch_p >= 0.5:
            continue

        if 40.0 <= mm <= 60.0:
            if eq_w < EQ_NEED // 2 and i not in res and mm >= 50.0:
                eq_w += 1
                res.add(i)
            if eq_b < EQ_NEED // 2 and i not in res and mm < 50.0:
                eq_b += 1
                res.add(i)
        else:
            if neq_w < NEQ_NEED // 2 and i not in res and mm >= 50.0:
                neq_w += 1
                res.add(i)
            if neq_b < NEQ_NEED // 2 and i not in res and mm < 50.0:
                neq_b += 1
                res.add(i)
    print(eq_w, eq_b, neq_w, neq_b)

data = []
label = []
for i in res:
    data.append(i)
    label.append(minimax(*i))
print(label[:10])
f = open("initial_data.pickle", "wb")
pickle.dump((data, label), f)
