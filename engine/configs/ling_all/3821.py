from math import comb as _comb


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W = 50
    ans = S.get('ans', 0)
    i = S.get('i')
    done = S.get('_line') == 11
    cv.text((x0 + 18, y0 + 4), 'ans 的二进制（50 位，从最高位 49 往下一位一位试填；绿 = 填了 1）', 22, T['muted'], bold=True)
    cell = (x1 - x0 - 40) / W
    sx = x0 + 20
    ys = y0 + 90
    ch = 46
    for b in range(W):
        pos = W - 1 - b          # 第 pos 位，最高位在最左
        X = sx + b * cell
        bit = (ans >> pos) & 1
        passed = i is not None and pos > i
        cur = i is not None and pos == i and not done
        fill = T['green'] if bit else ((52, 60, 72) if passed else T['panel2'])
        cv.rect((X + 1, ys, X + cell - 1, ys + ch), fill=fill, r=4, outline=T['yellow'] if cur else T['border'], width=3 if cur else 1)
        cv.text((X + cell / 2, ys + ch / 2), bit, 15, T['bg'] if bit else T['muted'], anchor='mm', bold=True, mono=True)
        if pos % 5 == 0 or cur:
            cv.text((X + cell / 2, ys + ch + 6), pos, 13, T['yellow'] if cur else T['dim'], anchor='mt', mono=True)
    if i is not None and not done:
        X = sx + (W - 1 - i) * cell + cell / 2
        cv.tri_up(X, ys - 4, 9, T['yellow'])
        cv.text((X, ys - 34), f'i = {i}', 22, T['yellow'], anchor='mb', bold=True)
    cv.text((x0 + 20, ys + ch + 70), f'ans = {ans}（十进制）', 28, T['text'], bold=True)


def _txt(S):
    i = S.get('i')
    if i is None:
        return '用组合数「试填」：从最高位开始，决定每一位填 0 还是 1'
    line = S.get('_line')
    if line == 6 and 'c' in S:
        c, n, k = S['c'], S['n'], S['k']
        return f'第 `{i}` 位填 0 的方案数 `C({i}, {k})` = =={c}==；`n` = {n} {">" if n > c else "≤"} {c} → 填 =={1 if n > c else 0}=='
    return f'`n = {S["n"]}`，还要填 `k = {S["k"]}` 个 1'


CONFIG = dict(
    num=3821, title='二进制中恰好K个1的第N小整数', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='试填法 · 逐位用组合数定位',
    tags=['组合计数', '试填法', '难度分 2069'],
    setup='''
from math import comb
''',
    code='''
class Solution:
    def nthSmallest(self, n: int, k: int) -> int:
        ans = 0
        for i in range(49, -1, -1):
            c = comb(i, k)  # 第 i 位填 0 的方案数
            if n > c:  # n 比较大，第 i 位必须填 1
                n -= c
                ans |= 1 << i
                k -= 1  # 维护剩余的 1 的个数
                if k == 0:  # 填完了 1，ans 剩余低位都是 0
                    return ans
''',
    call='Solution().nthSmallest(4, 2)',
    expect=9,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=[('i', 'i', 'yellow'), ('c', 'c', 'blue'), ('n', 'n', 'pink'), ('k', 'k', 'cyan'), ('ans', 'ans', 'green')],
    skip=['for i in range', 'c = comb', 'n -= c', 'k -= 1', 'if k == 0'],
    max_steps=28,
    captions={
        'ans = 0': '`ans` 从 0 开始，从高位到低位一位一位决定；题目保证答案 `< 2^50`，所以从第 49 位开始',
        'if n > c': lambda S, B, r: (f'第 `{S.i}` 位填 0 的方案数 `C({S.i}, {S.k})` = =={S.c}==；`n = {S.n} > {S.c}` → 前 `{S.c}` 小都填 0，第 `{S.n}` 小必须填 1' if S.n > S.c else f'第 `{S.i}` 位填 0 的方案数 `C({S.i}, {S.k})` = =={S.c}==；`n = {S.n} ≤ {S.c}` → 答案在填 0 的这堆里，这一位填 0'),
        'ans |= 1': lambda S, B, r: f'这一位填 1：`n -= c` → `n = {S.n}`（排除填 0 的那堆），`ans |= 1 << {S.i}` → ans = =={S.ans}==；还剩 `k − 1 = {S.k - 1}` 个 1 要放' + ('，==放完了，低位全是 0，返回==' if S.k == 1 else ''),
        'return ans': '1 全放完了，`ans` 剩下的低位都是 0 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='从高位到低位试填：n 大于「这一位填 0 的方案数」就必须填 1',
        complexity='时间 `O(W)`（W = 50），空间 `O(1)`',
        problem=['求二进制恰好有 `k` 个 `1` 的第 `n` 小的正整数，答案 `< 2^50`',
                 '示例：`n=4, k=2` → `9`（`3, 5, 6, 9` 里的第 4 个）',
                 '`3 = 11`，`5 = 101`，`6 = 110`，`9 = 1001`'],
        quote='枚举 i=49,48,…,0，计算在 i 个位置上填 k 个 1 的方案数 c = C(i,k)……如果 n ≤ c，那么答案二进制的 i 位填 0。如果 n > c，说明 n 比较大，答案二进制的 i 位填 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案第 `i` 位填 `0`：低 `i` 位放 `k` 个 1，共 `C(i, k)` 种，它们都比填 `1` 的小',
              '`n ≤ C(i, k)` → 答案在这堆里，填 `0`',
              '`n > C(i, k)` → 前面这堆都不是，`n -= C(i, k)`，填 `1`，`k -= 1`',
              '`k` 变成 `0` 就提前返回：剩下的低位全是 `0`'],
        after=[dict(heading='实现细节', lines=[
            '本视频用 `math.comb(i, k)` 现算组合数',
            '原文还给了「Python3 预处理」：先用杨辉三角预处理 `comb[i][j]`，`i < 50`',
            '`comb(i, k)` 在 `i < k` 时是 `0`，所以高位自然都填 `0`'])],
        summary=['时间 `O(W)`，`W = 50`；空间 `O(1)`',
                 '从第 `49` 位开始：题目保证答案 `< 2^50`',
                 '`n > c` 才填 `1`；`n == c` 时填 `0`（`c` 种里的最后一个）',
                 '`n -= c` 和 `k -= 1` 要一起做；`k == 0` 就提前返回',
                 '视频里 `for`、`c = comb(i, k)`、`n -= c`、`k -= 1`、`if k == 0` 不单独成步，信息合并进相邻字幕；中间重复的高位步骤快进'],
    ),
)
