G = [[4, 2, 4, 1], [2, 4, 4, 2], [3, 2, 2, 4]]


def _c(S, i, j, v):
    if not S.get('now') or 'i' not in S or 'j' not in S:
        return None
    if S['_line'] < LV:
        # 水平分割：前 i 行 + 第 i 行前 j+1 个
        return 'green' if (i < S['i'] or (i == S['i'] and j <= S['j'])) else None
    return 'green' if (j < S['j'] or (j == S['j'] and i <= S['i'])) else None


LV = 21
CONFIG = dict(
    num=3546, title='等和矩阵分割 I', difficulty='Medium', category='模拟',
    author='yiduobo', technique='行 / 列累加 · 提前 break',
    code='''
class Solution(object):
    def canPartitionGrid(self, grid):
        
        m = len(grid)
        n = len(grid[0])
        s = 0

        for i in range(m):
            for j in range(n):
                s += grid[i][j]
        
        now = 0
        for i in range(m - 1):
            for j in range(n):
                now += grid[i][j]
            
            if now + now == s:
                return True
            elif now + now > s:
                break
        
        now = 0
        for j in range(n - 1):
            for i in range(m):
                now += grid[i][j]
            
            if now + now == s:
                return True
            elif now + now > s:
                break
        
        return False
''',
    call=f'Solution().canPartitionGrid({G})',
    expect=True,
    skip=['m = len', 'n = len', 's = 0', 'for i in range(m)', 'for j in range(n)', 'for i in range(m - 1)', 'for j in range(n - 1)'],
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已累加进 now 的格子；黄框 = 当前格）', cell=84, h=360,
             color=_c, cursors=[('i', 'j', 'yellow')]),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"`now = {S['now']}`，`now + now = {S['now'] * 2}`，总和 `s = {S['s']}`" if 'now' in S else (f"总和累加中：`s = {S['s']}`" if 's' in S else ''))),
    ],
    watch=['s', 'now', 'i', 'j'],
    captions={
        's += grid[i][j]': '累加总和：`s = {s}`',
        'now = 0': lambda S, B, r: ('开始水平划分：`now` 记录前几行的和' if S._line < 21 else '水平划分不行，改试竖直划分：`now` 记录前几列的和'),
        'now += grid[i][j]': '`now += grid[{i}][{j}]` → `now = {now}`',
        'if now + now == s': lambda S, B, r: (f'`{S.now} + {S.now} = {2 * S.now}` ' + ('==等于== ' if 2 * S.now == S.s else '不等于 ') + f'总和 `{S.s}`'
                                              + ('：前面这部分恰好是一半' if 2 * S.now == S.s else '')),
        'return True': '找到恰好一半的划分 → 返回 `True`',
        'elif now + now > s': lambda S, B, r: (f'`{2 * S.now} > {S.s}`：已经超过一半，==数都是正数，再累加只会更大== → `break`' if 2 * S.now > S.s
                                                else f'`{2 * S.now} < {S.s}`：还不到一半，继续累加下一行/列'),
        'break': '提前结束这个方向',
        'return False': '水平、竖直都不行 → `False`',
    },
    cards=dict(
        one_liner='先算总和，再逐行、逐列累加，等于一半就能划分',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m × n` 的正整数矩阵，找一条水平或竖直分割线',
                 '分成的两个非空部分元素和相同',
                 '本视频：3×4 矩阵，总和 34，横切不行，竖切在第 2 列后分开'],
        quote='若某个f[index] * 2恰好等于s，说明可以水平划分。……由于f和g中每个元素之和上一个元素有关，同时也只是用了一次，因此可以使用变量迭代优化掉数组的空间。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]` 表示前 index+1 行的和，在上一个基础上累加新一行',
              '`f * 2 == s` 就能水平划分；列方向同理',
              '实现上用变量 `now` 代替数组 `f` / `g`，空间降到 `O(1)`'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：只枚举到 `m - 1` 行、`n - 1` 列，保证两部分非空',
                 '因为元素都是正数，`now` 超过一半就 `break`',
                 '切换方向前别忘记把 `now` 重置为 0',
                 '原文 `now + now` 判断，等价于 `now * 2`；代码未改，只删去类型说明'],
    ),
)
