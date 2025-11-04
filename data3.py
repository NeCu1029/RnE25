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
    [0]
    + [P ** (4 - pos) * (1 - P) ** pos * comb(4, pos) for pos in range(1, 5)]
    + [P**4]
)  # 도개걸윷모 확률
DEPTH = 8


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


res = set()
eq_w, eq_b = 0, 0
neq_w, neq_b = 0, 0
while eq_w < 3000 or eq_b < 3000 or neq_w < 6000 or neq_b < 6000:
    k = random.randint(2, 4)
    merged = [random.randint(1, 29)] * k + [random.randint(0, 30) for _ in range(4 - k)]
    nonmerged = [random.randint(0, 30) for _ in range(4)]
    if (set(merged) & set(nonmerged)) - {0, 30}:
        continue

    pos = merged + nonmerged if random.random() < 0.05 else nonmerged + merged
    pos = tuple(pos)
    ev = static(*pos)
    mm = minimax(*pos)
    if abs(ev - mm) >= 8.0:
        continue
    if mm <= 1.0 or mm >= 99.0:
        continue

    catchable = [0] * 6
    wh, bl = pos[:4], pos[4:]
    for j in wh:
        for k in range(1, 6):
            if MOVES[j][k] in wh or MOVES[j][k] in bl:
                catchable[k] = 1
    catch_p = sum([catchable[x] * PS[x] for x in range(1, 6)])
    if catch_p >= 0.5:
        continue

    if 40.0 <= mm <= 60.0:
        if eq_w < 3000 and pos not in res and mm >= 50.0:
            eq_w += 1
            res.add(pos)
        if eq_b < 3000 and pos not in res and mm < 50.0:
            eq_b += 1
            res.add(pos)
    else:
        if neq_w < 6000 and pos not in res and mm >= 50.0:
            neq_w += 1
            res.add(pos)
        if neq_b < 6000 and pos not in res and mm < 50.0:
            neq_b += 1
            res.add(pos)
    print(eq_w, eq_b, neq_w, neq_b)

data = []
label = []
for pos in res:
    data.append(pos)
    label.append(minimax(*pos))
print(label[:10])
with open("data3.pickle", "wb") as f:
    pickle.dump((data, label), f)
