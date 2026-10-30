P = [[1, 5, 2, 1], [2, 3, 4, 1], [4, 2, 1, 5]]


def _row(S):
    i = S.get('i')
    return S['points'][i] if i is not None else None


def _txt(S):
    L = S.get('_line')
    if 'i' not in S:
        return '`f[j]` = 当前行选第 `j` 列时的最大得分；列距离 1 扣 1 分'
    if L in (11, 12, 13, 14, 15):
        return '左→右：`left_max[j] = max(left_max[j−1] − 1, f[j])`（左边来的，每走一格多扣 1）'
    if L in (17, 18, 19, 20, 21):
        return '右→左：`right_max[j] = max(right_max[j+1] − 1, f[j])`，与左边结果取较大者'
    if L in (23, 24):
        return '上一行的最优扣分后，再加上本行 `points[i][j]`'
    return ''


CONFIG = dict(
    num=1937, title='扣分后的最大得分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='滚动 DP + 左右各扫一遍（left_max / right_max）',
    tags=['二、网格图 DP', '十一、优化 DP', '难度分 2106'],
    code='''
class Solution(object):
    def maxPoints(self, points):

        m = len(points)
        n = len(points[0])

        f = points[0][:]
        for i in range(1, m):
            g = []

            now = f[0]
            g.append(now)
            for j in range(1, n):
                now = max(now - 1, f[j])
                g.append(now)
            
            now = f[-1]
            g[-1] = max(g[-1], now)
            for j in range(n - 2, -1, -1):
                now = max(now - 1, f[j])
                g[j] = max(g[j], now)
            
            for j in range(n):
                g[j] += points[i][j]
            
            f = g[:]
        
        return max(f)
''',
    call=f'Solution().maxPoints({P})',
    expect=12,
    skip=['m = len', 'n = len', 'now = f[0]', 'now = f[-1]', 'for j in range(1, n)', 'for j in range(n - 2', 'for j in range(n):', 'f = g[:]'],
    views=[
        dict(type='array', var=_row, label='points[i]（本行得分）', cell=84, h=150),
        dict(type='array', var='f', label='f（上一行：选第 j 列的最大得分）', cell=84, h=190, pointers={'j': 'pink'}),
        dict(type='array', var='g', label='g（本行：先放「从上一行扣分后」的最优，最后再加 points[i][j]）', cell=84, h=190,
             pointers={'j': 'pink'}, color=lambda S, k, v: 'green' if S.get('_line') in (23, 24) and k <= S.get('j', -1) else None),
        dict(type='text', fn=_txt, size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('now', 'now', 'cyan')],
    captions={
        'f = points[0][:]': '第 0 行没有上一行，`f` 就是 `points[0]`',
        'for i in range': lambda S, B, r: (f'开始处理第 `{S.i}` 行：用 `f`（第 {S.i-1} 行）算出新的 `g`' if S.i != B.get('i') or 'i' not in B else '所有行处理完'),
        'g = []': '`g` 保存第 `i` 行的 `max(上一行 − 距离)`',
        'g.append(now)': '`g` 加入 `now = {now}`',
        'now = max(now - 1, f[j])': lambda S, B, r: (
            f'从左边来要多扣 1：`max(now − 1, f[{S.j}])` = `max({B.now - 1}, {S.f[S.j]})` → `now` 变为=={S.now}==' if S._line == 14 else
            f'从右边来也要多扣 1：`max(now − 1, f[{S.j}])` = `max({B.now - 1}, {S.f[S.j]})` → `now` 变为=={S.now}=='),
        'g[-1] = max(g[-1], now)': '右端的 `now` 从 `f[-1] = {f[-1]}` 起步，与左扫结果取较大者 → `g[{n-1}]` = {g[-1]}',
        'g[j] = max(g[j], now)': '`g[{j}] = max(左扫值, now={now})` = =={g[j]}==：左右两边来的取较大者',
        'g[j] += points[i][j]': '`g[{j}]` 加上本行得分 `points[{i}][{j}] = {points[i][j]}` → =={g[j]}==',
        'return max(f)': '最后一行里选最大的 → =={ret}==',
    },
    cards=dict(
        one_liner='距离扣分是线性的：左右各扫一遍，每走一格减 1',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['每行选一个格子得分，相邻两行选的列相差 `d` 要扣 `d` 分',
                 '求最大总得分',
                 '本视频：`[[1,5,2,1],[2,3,4,1],[4,2,1,5]]`'],
        quote='left_max[i][j] = max(left_max[i][j - 1] - 1, f[i - 1][j])……这样一来，就可以正序一趟遍历，在均摊O(1)的时间复杂度内求出所有的left_max了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` = 上一行任选 `k` 的 `f[i-1][k] − |k−j|`，再加 `points[i][j]`，直接枚举是 `O(n)`',
              '左边来的部分：`left_max[j] = max(left_max[j−1] − 1, f[j])`，正序一遍',
              '右边来的部分同理，倒序一遍；取较大者，再加本行得分'],
        summary=['时间 `O(mn)`，用 `f`、`g` 两个数组滚动，空间 `O(n)`',
                 '易错：左扫和右扫==都要包含 `f[j]` 本身（距离 0）==',
                 '右扫的起点 `now = f[-1]` 要先和 `g[-1]` 取最大',
                 '原文是 Python 3 兼容写法，代码未改',
                 '灵神题解思路相近：拆绝对值，维护 `f−k` 与 `f+k` 的前后缀最大'],
    ),
)
