def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') not in (9, 10):
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) == (i - 1, j):
        return 'blue'
    if (r, c) == (i - 1, j - 1):
        return 'green'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'f' not in S or i < 1 or S.get('_line') not in (9, 10):
        return '`f[i][j]` = 把 `i` 个不同的球放进 `j` 个相同的盒子（盒子非空）的方案数'
    f = S['f']
    return f'`f[{i}][{j}] = f[{i-1}][{j}] × {j} + f[{i-1}][{j-1}]` = {f[i-1][j]}×{j} + {f[i-1][j-1]}'


CONFIG = dict(
    num=1692, title='计算分配糖果的不同方式', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='第二类斯特林数 · 看最后一个球',
    tags=[],
    code='''
class Solution(object):
    def waysToDistribute(self, n, k):

        f = [[0] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 1
        mod = 10 ** 9 + 7
        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                f[i][j] = f[i - 1][j] * j + f[i - 1][j - 1]
                f[i][j] %= mod

        return f[-1][-1]
''',
    call='Solution().waysToDistribute(5, 3)',
    expect=25,
    skip=['for j in range', 'f[i][j] %= mod'],
    views=[
        dict(type='text', fn=_formula, size=26, h=70),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 放进已有盒子，绿 = 放进新盒子）', h=420, cell=84,
             rows=lambda S: [f'{k}球' for k in range(len(S['f']))] if 'f' in S else [],
             cols=lambda S: [f'{k}盒' for k in range(len(S['f'][0]))] if 'f' in S else [],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('n', 'n'), ('k', 'k')],
    captions={
        'f = [[0] * (k + 1)': '建表 `f`：`{n + 1}` 行（球数 0..{n}）× `{k + 1}` 列（盒数 0..{k}）',
        'f[0][0] = 1': '0 个球放 0 个盒子：什么都不做算 ==1 种==，这是所有转移的起点',
        'mod = ': '答案可能很大，取模 `{mod}`',
        'for i in range': '`i = {i}`：现在考虑第 `{i}` 个球。算 `f[i]` 只依赖 `f[i-1]`',
        'f[i][j] = f[i - 1][j] * j': '第 `{i}` 个球：放进 `{j}` 个旧盒子之一 `{B.f[i-1][j]}×{j}`，或开新盒子 `{B.f[i-1][j-1]}` → `f[{i}][{j}]` = =={f[i][j]}==',
        'return': '`f[n][k]` 就是答案：`{n}` 个不同的球放进 `{k}` 个相同盒子 = =={ret}== 种',
    },
    cards=dict(
        one_liner='考虑最后一个球：放进旧盒子，或自己开新盒子',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['把 `n` 颗==不同的==糖果分给 `k` 个==相同的==袋子，每个袋子至少一颗，求方案数（对 `10^9+7` 取模）',
                 '袋子之间无顺序，袋内糖果也无顺序',
                 '示例：`n = 3, k = 2` → `3`；本视频演示 `n = 5, k = 3` → `25`'],
        quote='题目实际上就是要求将n个不同的球放入m个相同的盒子里……非常经典的组合数学问题，比较官方的名称是第二类斯特林数。',
        quote_src='—— yiduobo 题解',
        idea=['令 `f[i][j]` = `i` 个不同的球放进 `j` 个相同盒子的方案数，只看最后一个球',
              '放进已有盒子：`f[i-1][j] × j`；自己放新盒子：`f[i-1][j-1]`',
              '盒子无序，按「盒内最小编号」排好序，就不会重复计数'],
        summary=['时间 `O(nk)`；`j` 只需枚举到 `min(i, k)`，因为盒子不能空',
                 '易错：已有盒子要乘 `j`（有 `j` 个盒子可选），新盒子不乘',
                 '边界 `f[0][0] = 1`，其余初始为 0',
                 '同类：第二类斯特林数；1866 是第一类斯特林数'],
    ),
)
