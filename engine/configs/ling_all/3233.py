from math import isqrt

L, R = 4, 16


def _pi():
    pi = [0] * 9
    for i in range(2, 9):
        pi[i] = pi[i - 1] + (1 if all(i % d for d in range(2, i)) else 0)
    return pi


def _arr(S):
    return _pi()


def _txt(S):
    if 'l' not in S:
        return f'`[l, r] = [{L}, {R}]`：特殊数字 = 质数的平方 `p²`；先看 `pi` 前缀和表'
    a, b = int(S['r'] ** 0.5), int((S['l'] - 1) ** 0.5)
    pi = _pi()
    return (f'`isqrt(r) = {a}`，`isqrt(l-1) = {b}` → 特殊数字 `pi[{a}] − pi[{b}] = {pi[a]} − {pi[b]} = {pi[a]-pi[b]}` 个'
            f'（即 {", ".join(str(p*p) for p in range(b+1, a+1) if pi[p]>pi[p-1]) or "无"}）')


def _rng(S):
    return list(range(0, R + 1))


def _col(S, i, v):
    if any(v == p * p for p in range(2, 5) if p in (2, 3)):
        return 'yellow' if L <= v <= R else None
    return None


CONFIG = dict(
    num=3233, title='统计不是特殊数字的数字数量', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='正难则反 · 质数前缀和 π(√x)',
    tags=['灵神题单·数学算法', '难度分 1509'],
    code='''
MX = 31622
pi = [0] * (MX + 1)
for i in range(2, MX + 1):
    if pi[i] == 0:  # i 是质数
        pi[i] = pi[i - 1] + 1
        for j in range(i * i, MX + 1, i):
            pi[j] = -1  # 标记 i 的倍数为合数
    else:
        pi[i] = pi[i - 1]

class Solution:
    def nonSpecialCount(self, l: int, r: int) -> int:
        return r - l + 1 - (pi[isqrt(r)] - pi[isqrt(l - 1)])
''',
    call=f'Solution().nonSpecialCount({L}, {R})',
    expect=11,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='array', var=_arr, pointers={'int(r ** 0.5)': 'blue', 'int((l - 1) ** 0.5)': 'pink'}, h=260,
             label='pi[0..8]：[0, i] 里的质数个数（蓝 = isqrt(r)，粉 = isqrt(l-1)）'),
        dict(type='array', var=_rng, color=_col, cell=50, h=200, label=f'区间 0..{R}（黄 = 区间里的特殊数字 4 和 9）'),
    ],
    watch=['l', 'r'],
    captions={
        'return r - l + 1': lambda S, B, ret: (
            f'区间共 `{S.r} − {S.l} + 1 = {S.r - S.l + 1}` 个数，减去特殊数字个数 '
            f'`pi[{isqrt(S.r)}] − pi[{isqrt(S.l - 1)}]` = `{_pi()[isqrt(S.r)]} − {_pi()[isqrt(S.l - 1)]}` '
            f'= =={_pi()[isqrt(S.r)] - _pi()[isqrt(S.l - 1)]}== → 答案 ==`{ret}`=='),
    },
    cards=dict(
        one_liner='特殊数字 = 质数的平方，正难则反',
        complexity='时间 `O(1)`，空间 `O(1)`（不计预处理）',
        problem=['真因数 = 除自身外的正因数；恰有 ==两个真因数== 的数叫特殊数字',
                 '求 `[l, r]` 里 ==不是== 特殊数字的个数',
                 f'本视频：`l = {L}`，`r = {R}` → `11`（特殊数字是 4 和 9）'],
        quote='根据题意，只有质数的平方 p² 才是特殊数字，因为 p² 恰好有两个真因数 1 和 p。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`1` 没有真因数，质数只有 1 个，其他数不是质数平方就至少 3 个',
              '所以 `[0, i]` 里的特殊数字个数 = `[0, isqrt(i)]` 里的质数个数 `π(isqrt(i))`',
              '前缀和 `pi` 预处理到 `√1e9 ≈ 31622`，再相减：`π(√r) − π(√(l−1))`'],
        after=[dict(heading='预处理 pi 表', lines=[
            '外层 `i` 从 2 扫描：`pi[i] == 0` 说明没被划掉 → ==质数==',
            '质数 `i`：`pi[i] = pi[i-1] + 1`，并把 `i*i` 起的倍数标成 `-1`',
            '合数：`pi[i] = pi[i-1]`，继承前缀和',
            '这就是埃氏筛和前缀和合并成一次循环'])],
        summary=['答案 = 区间整数个数 − 特殊数字个数 = `r−l+1 − (π(√r) − π(√(l−1)))`',
                 '易错：用 `isqrt(l - 1)`，而不是 `isqrt(l)`，否则会漏掉 `l` 本身恰好是质数平方的情况',
                 '预处理 `O(√U log log √U)`，之后每次询问 `O(1)`',
                 '本题 `l` 最小是 1，`isqrt(0) = 0`，`pi[0] = 0`，不会越界'],
    ),
)
