A, B, X = '1001', '0000', 2
N = len(A)


def _tbl(S):
    f = S.get('f')
    if f is None:
        return [[0] * (2 * (N // 2 + 1)) for _ in range(N)]
    return [[('-' if f[i][r][fr] is None else f[i][r][fr]) for r in (0, 1) for fr in range(N // 2 + 1)] for i in range(N)]


def _cc(S, i, j, v):
    idx = S.get('index')
    if idx is None:
        return None
    if i == idx and v != '-' and S.get('_line', 0) >= 14:
        return 'yellow'
    if i == idx - 1 and v != '-' and S.get('_line', 0) >= 14:
        return 'blue'
    return None


def _sc(S, k, v):
    idx = S.get('index')
    if idx is None:
        return ('orange' if A[k] != B[k] else None)
    if k == idx:
        return 'blue'
    return 'orange' if A[k] != B[k] else None


def _fx(S):
    ln = S.get('_line', 0)
    idx = S.get('index')
    if idx is None or ln < 14:
        return '`f[index][reversed][free]`：前 `index+1` 位已配好，`reversed` = 是否翻转了 `s1[index]` 和 `s1[index+1]`，`free` = 剩余免费消除次数'
    return f'第 {idx} 位：`s1[{idx}] = {A[idx]}`，`s2[{idx}] = {B[idx]}`，' + ('==相同==' if A[idx] == B[idx] else '==不同==')


CONFIG = dict(
    num=2896, title='执行操作使两个字符串相等', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='三维 DP · 免费消除次数',
    tags=['其他线性 DP', '多维 DP', '难度分 2172'],
    code='''
class Solution(object):
    def minOperations(self, s1, s2, x):

        n = len(s1)

        f = [[[None] * (n // 2 + 1) for _ in range(2)] for _ in range(n)]
        if s1[0] == s2[0]:
            f[0][0][0] = 0
        else:
            f[0][1][0] = 1
            if n >= 2:
                f[0][0][1] = x
        
        for index in range(1, n):
            if s1[index] == s2[index]:
                for free in range(n // 2 + 1):
                    if f[index - 1][0][free] is not None:
                        f[index][0][free] = f[index - 1][0][free]
                    if f[index - 1][1][free] is not None:
                        f[index][1][free] = f[index - 1][1][free] + 1
            
            else:
                for free in range(n // 2 + 1):
                    if f[index - 1][0][free] is not None:
                        if free > 0 and (f[index][0][free - 1] is None or f[index][0][free - 1] > f[index - 1][0][free]):
                            f[index][0][free - 1] = f[index - 1][0][free]
                        if free < n // 2 and (f[index][0][free + 1] is None or f[index][0][free + 1] > f[index - 1][0][free] + x):
                            f[index][0][free + 1] = f[index - 1][0][free] + x
                        if f[index][1][free] is None or f[index][1][free] > f[index - 1][0][free]:
                            f[index][1][free] = f[index - 1][0][free] + 1
                    
                    if f[index - 1][1][free] is not None and (f[index][0][free] is None or f[index][0][free] > f[index - 1][1][free]):
                        f[index][0][free] = f[index - 1][1][free]
        
        if f[-1][0][0] is None:
            return -1
        return f[-1][0][0]
''',
    call=f'Solution().minOperations({A!r}, {B!r}, {X})',
    expect=2,
    skip=['for free in range', 'for _ in range', 'if f[index - 1][0][free] is not None', 'if f[index - 1][1][free] is not None', 'if free > 0 and', 'if free < n // 2 and', 'if f[index][1][free] is None'],
    max_steps=90,
    views=[
        dict(type='string', var=lambda S: A, label='s1（橙 = 与 s2 不同）', h=120, cell=70, color=_sc),
        dict(type='string', var=lambda S: B, label='s2', h=120, cell=70, color=_sc),
        dict(type='text', fn=_fx, size=24, h=70),
        dict(type='table', var=_tbl, label='f[index]（列 = reversed·free；黄 = 当前行，蓝 = 上一行）', h=330, cell=64,
             rows=lambda S: [f'i={k}' for k in range(N)], cols=lambda S: [f'{r}·{k}' for r in (0, 1) for k in range(N // 2 + 1)],
             color=_cc),
    ],
    watch=[('index', 'index', 'blue'), ('free', 'free', 'pink'), ('x', 'x', 'orange')],
    captions={
        'n = len(s1)': '`n = {n}`；免费消除次数最多 `n // 2`',
        'f = [[[None]': '`f[index][reversed][free]` 全是 ==None==：表示这个状态还没有到达',
        'if s1[0] == s2[0]': lambda S, B, r: ('第 0 位已经相同' if S.s1[0] == S.s2[0] else '第 0 位不同：有两种办法，分别记状态'),
        'f[0][0][0] = 0': '第 0 位相同，什么都不用做：`f[0][0][0] = 0`',
        'f[0][1][0] = 1': '第 0 位不同，翻转 `s1[0]` 和 `s1[1]`，代价 1：`f[0][1][0] = 1`',
        'if n >= 2': '只有 `n ≥ 2` 才能留免费机会',
        'f[0][0][1] = x': '或者用代价 `x` 的操作：这一位消除，并给后面留 ==1 次免费消除==：`f[0][0][1] = {x}`',
        'for index in range(1, n)': '`index = {index}`：由 `f[{index - 1}]` 推出 `f[{index}]`',
        'if s1[index] == s2[index]': lambda S, B, r: (f'`s1[{S.index}] = s2[{S.index}]`：这位本来就一样，只需顺延' if S.s1[S.index] == S.s2[S.index]
                                                      else f'`s1[{S.index}] ≠ s2[{S.index}]`：这位要修，有 4 种来源'),
        'f[index][0][free] = f[index - 1][0][free]': '相同位、没翻转：直接继承 `f[{index - 1}][0][{free}]` = =={f[index][0][free]}==',
        'f[index][1][free] = f[index - 1][1][free] + 1': '上一位翻了 `s1[index]`，这里再翻一次抵消，代价 +1 → =={f[index][1][free]}==',
        'f[index][0][free - 1] = f[index - 1][0][free]': '==用掉一次免费消除==：`free` {free} → {free - 1}，代价不变 = =={f[index][0][free - 1]}==',
        'f[index][0][free + 1] = f[index - 1][0][free] + x': '用代价 `x` 的操作消除这位，==留一次免费给后面==：`free` {free} → {free + 1}，代价 +{x} = =={f[index][0][free + 1]}==',
        'f[index][1][free] = f[index - 1][0][free] + 1': '翻转 `s1[index]` 和 `s1[index+1]`，代价 +1，标记 `reversed = 1` = =={f[index][1][free]}==',
        'f[index][0][free] = f[index - 1][1][free]': '上一位已经把这位一起翻好了：无需操作，`reversed` 回到 0 = =={f[index][0][free]}==',
        'if f[-1][0][0] is None': lambda S, B, r: ('终点状态为 None → 无解' if S.f[-1][0][0] is None else '终点 `f[-1][0][0]` 有值：免费机会刚好用完且没有悬着的翻转'),
        'return -1': '无解，返回 -1',
        'return f[-1][0][0]': '最小代价 =={ret}==',
    },
    cards=dict(
        one_liner='把「任意两位花 x」看成：消除这位，再留一次免费消除给后面',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`s1`、`s2` 是等长二进制串，目标把 `s1` 变成 `s2`',
                 '操作一：任选两位翻转，代价 `x`；操作二：翻转相邻两位，代价 `1`',
                 '本视频：`"1001"` → `"0000"`，`x = 2`，答案 `2`'],
        quote='可以将其视为一种无差别消除的机会。也就是说，对于某个不匹配的 s1[index] 和 s2[index]，可以使用 x 的代价，将二者变为匹配，同时还有一次免费强制匹配的机会留给后续的字符串使用。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心「就近配对」在有 `x` 操作时不成立，改用 DP',
              '状态 `f[index][reversed][free]`：当前是否翻了 `s1[index]` 与 `s1[index+1]`，还剩几次免费消除',
              '不匹配的位有 4 种转移：免费消除、花 `x` 留免费、相邻翻转、被上一位翻掉'],
        summary=['时间 `O(n²)`，空间 `O(n²)`（`free` 最多 `n // 2`）',
                 '终点必须 `f[-1][0][0]`：没有悬着的翻转，也没有剩余免费次数',
                 '`None` 表示状态不可达，每次转移前都要先判空',
                 '原文为 Python 2 写法，`n / 2` 都已改为 `n // 2`',
                 '对比灵神：灵神从后往前做记忆化搜索，再给出只看差异位置的 `O(n)` 解法'],
    ),
)
