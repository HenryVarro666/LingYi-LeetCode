CONFIG = dict(
    num=1937, title='扣分后的最大得分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='滚动数组 · left_max / right_max 递推',
    tags=['动态规划', '难度分 2106'],
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
    call='Solution().maxPoints([[1,2,3],[1,5,1],[3,1,1]])',
    expect=9,
    skip=['m = len', 'n = len', 'g = []', 'for j in range(1, n)', 'for j in range(n - 2', 'for j in range(n):', 'f = g[:]'],
    max_steps=70,
    views=[
        dict(type='table', var='points', label='points', h=180, cell=60, cursors=[('i', 'j', 'yellow', '')]),
        dict(type='array', var='f', label='f：上一行每列选它的最大得分', h=150, cell=70, pointers={'j': 'blue'}),
        dict(type='array', var='g', label='g：本行的 max(left_max, right_max)', h=150, cell=70, pointers={'j': 'pink'}),
        dict(type='text', fn=lambda S: ('`now` = 一路带扣分传递的最大值：每走一格 `−1`，遇到更大的 `f[j]` 就换' if 'now' in S else ''), size=24, h=50),
    ],
    watch=['i', 'j', 'now', ('max(f)', 'max(f)', 'green')],
    captions={
        'f = points[0]': '第 0 行没有扣分，`f = {f}`',
        'for i in range': lambda S, B, r: (f'开始处理第 `{S.i}` 行：用 `f`（上一行）推出这一行' if S.i != B.get('i') else '所有行都处理完了'),
        'g.append(now)': '`g` 追加 `{now}`：这是只看左侧（含自己）的最优',
        'now = f[0]': '从左往右：`now` 从 `f[0]` = {now} 出发（第 0 列左边只有自己）',
        'now = max(now - 1': lambda S, B, r: (f'左→右：`max({B.now} − 1, f[{S.j}] = {S.f[S.j]})` = =={S.now}==，`g[{S.j}]` 记下左侧最优' if S.get('_line') == 14 else
                                             f'右→左：`max({B.now} − 1, f[{S.j}] = {S.f[S.j]})` = =={S.now}=='),
        'now = f[-1]': '从右往左：`now` 从最右 `f[-1]` = {now} 出发',
        'g[-1] = max': '最右格：`g[-1] = max(g[-1], {now})` = {g[-1]}',
        'g[j] = max(g[j], now)': '`g[{j}] = max(左侧最优, 右侧最优)` = =={g[j]}==',
        'g[j] += points[i][j]': '加上本格得分：`g[{j}] += {points[i][j]}` = =={g[j]}==',
        'return max(f)': '最后一行里最大的一个 = =={ret}==',
    },
    cards=dict(
        one_liner='left_max 和 right_max 都是“上一格减 1，或换成自己”',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['每行选一个格子得分，相邻行列差 `|c1−c2|` 会扣分',
                 '求最大总得分',
                 '示例：`[[1,2,3],[1,5,1],[3,1,1]]` → `9`'],
        quote='left_max[i][j] = max(left_max[i][j - 1] - 1, f[i - 1][j])，……这样一来，就可以正序一趟遍历，在均摊O(1)的时间复杂度内求出所有的left_max了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 要在上一行所有列里挑，扣 `|k−j|`，直接做是 `O(n²)`',
              '把 `k ≤ j` 的部分记成 `left_max`：从左到右，每走一格 `−1`，再和 `f[j]` 比',
              '`k ≥ j` 的部分记成 `right_max`：从右到左同理；两者取大，再加 `points[i][j]`'],
        summary=['时间 `O(mn)`，空间 `O(n)`（两个数组滚动）',
                 '易错：left 和 right 要分别扫一遍；右扫时最右格要单独初始化',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神拆成 `f+k` / `f−k` 两个前后缀最大；yiduobo 用“每格减 1”的递推'],
    ),
)
