A0 = [2, 5, 1, 2]
B0 = [5, 2, 1, 2]


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 8:
        return None
    if (r, c) == (i + 1, j + 1):
        return 'yellow'
    if S['A'][i] == S['B'][j]:
        return 'green' if (r, c) == (i, j) else None
    return 'blue' if (r, c) in ((i + 1, j), (i, j + 1)) else None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f[i][j]` = `A` 的前 `i` 个数与 `B` 的前 `j` 个数最多能匹配几个'
    if S['A'][i] == S['B'][j]:
        return f'`A[{i}] = B[{j}] = {S["A"][i]}` → `f[{i + 1}][{j + 1}] = f[{i}][{j}] + 1`'
    return f'`A[{i}] = {S["A"][i]}` ≠ `B[{j}] = {S["B"][j]}` → `max(f[{i + 1}][{j}], f[{i}][{j + 1}])`'


CONFIG = dict(
    num=1035, title='不相交的线', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='二维 DP · 最长公共子序列',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1806'],
    code='''
class Solution(object):
    def maxUncrossedLines(self, A, B):
        m = len(A)
        n = len(B)
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if A[i] == B[j]:
                    f[i + 1][j + 1] = f[i][j] + 1
                else:
                    f[i + 1][j + 1] = max(f[i + 1][j], f[i][j + 1])
        return f[m][n]
''',
    call=f'Solution().maxUncrossedLines({A0}, {B0})',
    expect=3,
    skip=['for j in range'],
    max_steps=80,
    views=[
        dict(type='array', var='A', label='A（蓝 = 当前 A[i]）', h=160, cell=60,
             pointers={'i': 'blue'}),
        dict(type='array', var='B', label='B（粉 = 当前 B[j]）', h=160, cell=60,
             pointers={'j': 'pink'}),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，绿/蓝 = 它依赖的格子）', h=300, cell=56,
             rows=lambda S: ['∅'] + [f'{k}:{c}' for k, c in enumerate(A0)],
             cols=lambda S: ['∅'] + [f'{k}:{c}' for k, c in enumerate(B0)],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('A[i]', 'A[i]', 'blue'), ('B[j]', 'B[j]', 'pink')],
    captions={
        'm = len': '`m = {m}`，`A` 有 {m} 个数',
        'n = len': '`n = {n}`，`B` 有 {n} 个数',
        'f = [[0]': '`f[i][j]`：`A` 的前 `i` 个数、`B` 的前 `j` 个数最多匹配几个；多留一行一列表示「空」，初始全 0',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：看 `A[{S.i}] = {S.A[S.i]}`，一行一行往下填' if S.i != B.get('i') else '所有行都填完了'),
        'if A[i] == B[j]': lambda S, B, r: (f'`A[{S.i}] = {S.A[S.i]}`，`B[{S.j}] = {S.B[S.j]}` → '
                                            + ('相等，可以连线' if S.A[S.i] == S.B[S.j] else '不相等，这两个数连不了')),
        'f[i + 1][j + 1] = f[i][j] + 1': '相等就接在左上角后面：`f[{i + 1}][{j + 1}] = f[{i}][{j}] + 1` = =={f[i + 1][j + 1]}==',
        'f[i + 1][j + 1] = max': '不相等：取「少看 A 一个」或「少看 B 一个」较大者：`max({f[i + 1][j]}, {f[i][j + 1]})` = =={f[i + 1][j + 1]}==',
        'return f[m][n]': '右下角 `f[{m}][{n}]` 就是 `A`、`B` 全部考虑后的最大连线数 = =={ret}==',
    },
    cards=dict(
        one_liner='描述花里胡哨，其实就是最长公共子序列',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['两行数字 `A`、`B`，相等的数字可以连线，连线==不能相交==（端点也不行）',
                 '求最多能画几条线',
                 '示例：`[1,4,2]` 与 `[1,2,4]` → `2`；本视频用 `[2,5,1,2]` 与 `[5,2,1,2]` → `3`'],
        quote='虽然题目描述花里胡哨的，但是仔细分析可以发现这就是个最长公共子序列问题，那么使用经典的二维动态规划，令f[i][j]表示A的前i个数字与B的前j个数字最多能匹配上多少',
        quote_src='—— yiduobo 题解',
        idea=['连线不相交 ⇔ 两边下标同时递增 ⇔ 公共子序列',
              '`A[i] == B[j]`：多一条线，`f[i][j] + 1`',
              '不相等：`A[i]` 与 `B[j]` 至少有一个用不上，取 `f[i+1][j]`、`f[i][j+1]` 较大者'],
        summary=['时间、空间都是 `O(mn)`，二维表直接按行填',
                 '`f` 多开一行一列，表示其中一边为空，不用单独处理边界',
                 '原文为经典 LCS 模板；类似题 1143. 最长公共子序列',
                 '对比灵神：灵神进一步把二维压成一维，用 `pre` 保存左上角'],
    ),
)
