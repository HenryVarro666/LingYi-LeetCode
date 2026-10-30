def _color(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or i >= len(S['f']):
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if r == i - 1 and c in (j, j - 1) and c >= 0:
        return 'blue'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    p = S['prob']
    if i is None or j is None:
        return '`f[i][j]` = 抛 i 次硬币、恰好 j 次正面朝上的概率'
    if j == 0:
        return f'`f[{i}][0] = f[{i-1}][0] × (1 − {p[i-1]})`'
    return f'`f[{i}][{j}] = f[{i-1}][{j-1}] × {p[i-1]} + f[{i-1}][{j}] × (1 − {p[i-1]})`'


CONFIG = dict(
    num=1230, title='抛掷硬币', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='二维 DP · 抛 i 次恰好 j 次正面',
    tags=[],
    code='''
class Solution(object):
    def probabilityOfHeads(self, prob, target):

        n = len(prob)
        f = [[0.0] * (n + 1) for _ in range(n + 1)]
        f[0][0] = 1.0
        for i in range(1, n + 1):
            for j in range(0, i + 1):
                if j == 0:
                    f[i][j] = f[i - 1][j] * (1 - prob[i - 1])
                else:
                    f[i][j] = f[i - 1][j - 1] * prob[i - 1] + f[i - 1][j] * (1 - prob[i - 1])
        
        return f[n][target]
''',
    call='Solution().probabilityOfHeads([0.5, 0.25, 0.5], 1)',
    expect=0.4375,
    skip=['for j in range'],
    views=[
        dict(type='array', var='prob', label='prob[i]：第 i+1 枚硬币正面朝上的概率', h=150, cell=90,
             color=lambda S, k, v: 'blue' if S.get('i') is not None and k == S['i'] - 1 else None),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 它依赖的上一行格子）', h=330, cell=96,
             rows=lambda S: [f'抛{k}次' for k in range(len(S['f']))] if 'f' in S else [],
             cols=lambda S: [f'{k}正' for k in range(len(S['f']))] if 'f' in S else [], color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('target', 'target', 'green')],
    captions={
        'n = len(prob)': '`n = {n}` 枚硬币',
        'f = [[0.0]': '`f[i][j]`：抛 `i` 次、恰好 `j` 次正面朝上的概率；先全部填 0',
        'f[0][0] = 1.0': '一次都没抛，0 次正面的概率是 ==1==：这是递推的起点',
        'for i in range': lambda S, B, r: (f'第 `{S.i}` 行：考虑第 `{S.i}` 枚硬币（概率 `prob[{S.i-1}] = {S.prob[S.i-1]}`）' if S.get('i') != B.get('i') else '所有硬币都考虑完了'),
        'if j == 0': lambda S, B, r: ('`j = 0`：一次正面都没有，最后这枚只能是背面' if S.j == 0 else f'`j = {S.j} > 0`：最后这枚可能是正面，也可能是背面'),
        'f[i][j] = f[i - 1][j] *': '`f[{i}][0] = f[{i-1}][0] × (1 − {prob[i-1]})` = =={f[i][j]}==',
        'f[i][j] = f[i - 1][j - 1]': '最后正面：`f[{i-1}][{j-1}] × {prob[i-1]}`；最后背面：`f[{i-1}][{j}] × (1 − {prob[i-1]})`；相加 = =={f[i][j]}==',
        'return f[n][target]': '抛完 `{n}` 次、恰好 `{target}` 次正面 = `f[{n}][{target}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j]：前 i 枚里恰好 j 枚正面，按最后一枚分两类',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['有 `n` 枚不均匀硬币，第 `i` 枚正面朝上的概率是 `prob[i]`',
                 '每枚抛一次，求==恰好 `target` 枚正面朝上==的概率',
                 '示例：`prob = [0.5, 0.25, 0.5]`，`target = 1` → `0.4375`'],
        quote='令f[i][j]表示抛i次硬币，有j次正面向上的概率。首先初始化f[0][0] = 1',
        quote_src='—— yiduobo 题解原文',
        idea=['`j = 0`：最后一次必然是背面，`f[i][0] = f[i-1][0] × (1 − prob[i-1])`',
              '`j > 0`：最后一次正面（从 `j-1` 来）或背面（从 `j` 来），两项相加',
              '答案是 `f[n][target]`'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`，可以滚动数组降到 `O(n)`',
                 '易错：`prob` 下标比 `i` 小 1，用 `prob[i - 1]`',
                 '`j` 最多到 `i`，不可能的格子保持 0',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
