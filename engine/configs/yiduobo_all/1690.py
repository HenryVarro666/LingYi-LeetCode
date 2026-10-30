ST = [5, 3, 1, 4, 2]


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line') != 16:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i + 1, j), (i, j - 1)):
        return 'blue'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or j <= i or S.get('_line') != 16:
        return '`f[i][j]` = 石子 `i..j`（从 1 开始），==先手比后手多得的分=='
    s, f = S['s'], S['f']
    return (f'`max({s[j]} − {s[i]} − {f[i+1][j]}, {s[j-1]} − {s[i-1]} − {f[i][j-1]})` = =={f[i][j]}==')


CONFIG = dict(
    num=1690, title='石子游戏 VII', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间 DP · 按区间长度从短到长',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 1951'],
    code='''
class Solution(object):
    def stoneGameVII(self, stones):

        s = [0]
        for stone in stones:
            s.append(s[-1] + stone)

        n = len(stones)
        f = [[0] * (n + 1) for _ in range(n + 1)]
        for length in range(1, n + 1):
            for i in range(1, n - length + 2):
                j = i + length - 1
                if i == j:
                    f[i][j] = 0
                else:
                    f[i][j] = max(s[j] - s[i] - f[i + 1][j], s[j - 1] - s[i - 1] - f[i][j - 1])
        
        return f[1][n]
''',
    call=f'Solution().stoneGameVII({ST!r})',
    expect=6,
    skip=['for stone in stones', 's.append', 'j = i + length - 1', 'for i in range'],
    views=[
        dict(type='array', var='stones', label='stones（下标 0 起；DP 里石子编号从 1 起）', h=210, cell=84,
             pointers={'i-1': 'blue', 'j-1': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f', label='f[i][j]（行 i、列 j 均从 1 起；黄 = 正在算，蓝 = 依赖的两格）', h=360, cell=70,
             rows=lambda S: list(range(len(ST) + 1)), cols=lambda S: list(range(len(ST) + 1)), color=_cell),
    ],
    watch=[('length', 'length', 'orange'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s', 's', 'cyan')],
    captions={
        's = [0]': '前缀和 `s`，`s[0] = 0`：石子 `i+1..j` 的和 = `s[j] − s[i]`',
        'n = len': '`n = {n}`；`f` 开 `(n+1)×(n+1)`，石子编号用 1..n',
        'f = [[0]': '`f[i][j]`：石子 `i..j` 上先手比后手多得多少；先全部置 0',
        'for length in range': lambda S, B, r: (f'区间长度 `length = {S.length}`：==从短到长==，短区间先算好' if S.get('length') != B.get('length')
                                                else '所有长度都算完了'),
        'if i == j': lambda S, B, r: (f'`i = j = {S.i}`：区间只有一颗石子' if S.i == S.j else f'区间 `[{S.i},{S.j}]` 有 {S.j-S.i+1} 颗，要比较拿左还是拿右'),
        'f[i][j] = 0': '只剩一颗：移除后没有石子，得分差 `f[{i}][{j}] = 0`',
        'f[i][j] = max(': '拿第 `i` 颗：得 `s[{j}]−s[{i}]` = {s[j]-s[i]}，再减 `f[{i+1}][{j}]` = {f[i+1][j]}；拿第 `j` 颗：得 {s[j-1]-s[i-1]}，减 `f[{i}][{j-1}]` = {f[i][j-1]} → =={f[i][j]}==',
        'return f[1][n]': '整排的得分差 `f[1][{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='先枚举区间长度，用更短的区间推出更长的',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['石子排成一排，Alice 先手，每回合移除最左或最右一颗',
                 '得分是==剩余石子的和==；Alice 要扩大分差，Bob 要缩小',
                 '示例：`[5,3,1,4,2]` → `6`'],
        quote='对于这类区间从两侧向中间操作的问题，经典的做法就是动态规划。令f[i][j]表示区间i到j的某种最值，然后状态转移时就分别考虑操作i或者操作j。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：石子 `i..j`，先手比后手多得的分',
              '先手取第 `i` 颗：得其余的和，对手变先手，面对 `i+1..j`，扣掉 `f[i+1][j]`',
              '依赖更短的区间，所以 ==先枚举长度 `length`，再枚举左端点 `i`=='],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '石子和 DP 下标都从 1 起，`s[0] = 0`；区间和 `s[j] − s[i]` 正好是不含第 `i` 颗的和',
                 '易错：`i` 的上界是 `n - length + 1`（即 `range(1, n - length + 2)`）',
                 '原文文字写 `min`，但代码用的是 `max`，以代码为准',
                 '对比灵神：他用 `i` 倒序、`j` 正序；yiduobo 按区间长度枚举'],
    ),
)
