from math import comb

memo: dict[tuple[int, int], float] = dict()
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
p = 0.46
ps = [0] + [p ** (4 - i) * (1 - p) ** i * comb(4, i) for i in range(1, 5)] + [p**4]
ps = [round(x, 8) for x in ps]


def recur_bef(first: int, second: int) -> float:
    if first == 30:
        memo[(first, second)] = 1.0
        return 1.0
    if second == 30:
        memo[(first, second)] = 0.0
        return 0.0
    if (first, second) in memo:
        return memo[(first, second)]

    res = 0.0
    for sq in range(1, 6):
        res += recur_aft(first, second, sq) * ps[sq]
    memo[(first, second)] = res
    return res


def recur_aft(first: int, second: int, sq: int) -> float:
    if move[first][sq] == second:
        return recur_bef(second, 0)
    if sq >= 4:
        return recur_bef(move[first][sq], second)
    return 1.0 - recur_bef(second, move[first][sq])


recur_bef(0, 0)
arr = [[0.0] * 31 for _ in range(31)]
for x, y in memo:
    arr[x][y] = memo[(x, y)]
print(arr)

f = open("NNUE2/table.txt", "w")
f.write(str(arr))
