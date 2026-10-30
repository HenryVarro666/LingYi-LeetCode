def _lp(names, txt, end):
    def f(S, B, r):
        if all(n in B and B[n] == S[n] for n in names):
            return end
        return txt(S)
    return f


def _in(S, r, c):
    i, j, k = S.get('i'), S.get('j'), S['k']
    if i is None or j is None:
        return False
    return i <= r < i + k and j <= c < j + k


def _pair(S):
    if 'x' in S and 'y' in S and S.get('_line') in (14, 15, 16):
        if S['x'] < S['y']:
            return f"相邻两数 `{S['x']}` 和 `{S['y']}`：不同，差 `{S['y'] - S['x']}`，当前最小 `res = {S['res']}`"
        return f"相邻两数 `{S['x']}` 和 `{S['y']}`：相同，不能算，当前最小 `res = {S['res']}`"
    return '子矩阵展开成 `a` 排序后，最小差只可能出现在相邻元素之间'


CONFIG = dict(
    num=3567, title='子矩阵的最小绝对差', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='暴力枚举子矩阵 · 排序后看相邻差',
    tags=[],
    code='''
class Solution:
    def minAbsDiff(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m, n = len(grid), len(grid[0])
        ans = [[0] * (n - k + 1) for _ in range(m - k + 1)]
        for i in range(m - k + 1):
            sub_grid = grid[i: i + k]
            for j in range(n - k + 1):
                a = []
                for row in sub_grid:
                    a += row[j: j + k]
                a.sort()

                res = inf
                for x, y in pairwise(a):
                    if x < y:  # 题目要求相减的两个数必须不同
                        res = min(res, y - x)
                if res < inf:
                    ans[i][j] = res
        return ans
''',
    call='Solution().minAbsDiff([[1,-2,3],[2,3,5]], 2)',
    expect=[[1, 2]],
    skip=['m, n = len', 'sub_grid = grid'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（蓝框 = 当前 k×k 子矩阵）', h=230, cell=90,
             color=lambda S, r, c, v: 'blue' if _in(S, r, c) else None,
             cursors=[('i', 'j', 'yellow', '(i,j)')]),
        dict(type='array', var='a', label='a（子矩阵展开并排序）', h=170, cell=80),
        dict(type='text', h=90, size=28, fn=_pair),
        dict(type='grid', var='ans', label='ans', h=150, cell=90,
             color=lambda S, r, c, v: 'green' if (r, c) == (S.get('i'), S.get('j')) and S.get('_line') == 18 else None),
    ],
    watch=['i', 'j', ('res', 'res', 'yellow')],
    captions={
        'ans = [[0]': '`ans` 有 `(m-k+1) × (n-k+1)` 格，先全填 `0`（全相同时答案就是 0）',
        'for i in range': _lp(['i'], lambda S: f'枚举子矩阵左上角的行 `i = {S.i}`', '所有行都枚举完了，循环结束'),
        'for j in range': _lp(['j'], lambda S: f'枚举左上角的列 `j = {S.j}`，子矩阵是 `({S.i},{S.j})` 开始的 `{S.k}×{S.k}`', '这一行的列都枚举完了，回到外层'),
        'a = []': '准备一个空数组 `a`，装子矩阵的所有元素',
        'for row in sub_grid': _lp(['row'], lambda S: '取子矩阵的一行', '`k` 行都并进来了，`a` 收集完毕'),
        'a += row': '把这一行的 `{k}` 个数并入 `a`：`a = {a}`',
        'a.sort()': '排序后，差最小的两个不同数一定相邻：`a = {a}`',
        'res = inf': '`res` 记录最小差，初始为无穷大',
        'for x, y in pairwise': _lp(['x','y'], lambda S: f'看相邻两数 `{S.x}`、`{S.y}`', '相邻两数都看完了，`res` 定下来'),
        'if x < y': lambda S, B, r: (f'`{S.x} < {S.y}`：两数不同，可以算差' if S.x < S.y else f'`{S.x} = {S.y}`：相同，题目要求不同值，跳过'),
        'res = min': '`res = min({B.res}, {y} - {x})` = =={res}==',
        'if res < inf': lambda S, B, r: ('`res` 被更新过：存入 `ans[i][j]`' if S.res < inf else '`res` 仍是无穷大：全部相同，保持 `0`'),
        'ans[i][j] = res': '`ans[{i}][{j}] = {res}`',
        'return ans': '所有子矩阵都算完：返回 `{ans}`',
    },
    cards=dict(
        one_liner='把子矩阵展开排序，最小差只会在相邻两数之间',
        complexity='时间 `O((m-k)(n-k)k²logk)`，空间 `O(k²)`',
        problem=['`m×n` 矩阵，对每个 `k×k` 子矩阵，求任意两个不同值之差的最小绝对值',
                 '子矩阵所有数都相同则为 `0`',
                 '示例：`[[1,-2,3],[2,3,5]], k=2` → `[[1,2]]`'],
        quote='把子矩形中的所有元素添加到一个数组 a 中，然后把 a 排序。排序后，不同元素之差的最小值一定来自 a 的相邻元素。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数据范围只有 `30×30`，直接暴力枚举每个子矩阵',
              '展开成 `a` 并排序，用 `pairwise` 看相邻两数',
              '`x < y` 才算（要求不同的数），全相同则保持 `0`'],
        summary=['时间 `O((m-k)(n-k)k²logk)`，空间 `O(k²)`',
                 '易错点：相同的数不能算差，必须判 `x < y`',
                 '`res` 一直是 `inf` 说明子矩阵元素全相同，答案是 `0`',
                 '进阶做法：定长滑动窗口 + 有序集合 + 懒删除堆，`O((m-k)nk log k)`，常数大'],
    ),
)
