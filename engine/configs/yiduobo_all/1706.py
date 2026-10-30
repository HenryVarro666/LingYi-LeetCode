CONFIG = dict(
    num=1706, title='球会落何处', difficulty='Medium', category='网格图',
    author='yiduobo', technique='逐行推进所有球',
    tags=[],
    code='''
class Solution(object):
    def findBall(self, grid):

        n = len(grid[0])
        res = list(range(n))
        for line in grid:
            for index in range(n):
                if res[index] != -1:
                    p = res[index]
                    if line[p] == 1:
                        if p != n - 1 and line[p + 1] == 1:
                            res[index] = p + 1
                        else:
                            res[index] = - 1
                    else:
                        if p != 0 and line[p - 1] == -1:
                            res[index] = p - 1
                        else:
                            res[index] = -1
        
        return res
''',
    call='Solution().findBall([[1,1,1,-1],[-1,-1,1,1],[1,1,-1,-1]])',
    expect=[1, 2, -1, -1],
    views=[
        dict(type='grid', var='grid', h=330, cell=90,
             cursors=[('grid.index(line)', 'p', 'yellow', '球')],
             color=lambda S, i, j, v: ('blue' if v == 1 else 'pink')),
        dict(type='array', var='res', label='res[i]：第 i 颗球现在所在的列（-1 = 卡住）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: ('red' if v == -1 else None)),
        dict(type='text', size=26, fn=lambda S: (f"第 `{S['index']}` 颗球在第 `{S['p']}` 列，这一行的挡板是 `{S['line'][S['p']]}`" if 'p' in S and 'index' in S and S['_line'] >= 9 else '')),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'yellow'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}` 列，也就是 `{n}` 颗球',
        'res = list': '`res[i]`：第 `i` 颗球当前所在的列，开始就是自己那一列：`{res}`',
        'for line in grid': '一行一行往下推，所有球同时落到这一行',
        'for index in range': '处理第 `{index}` 颗球',
        'if res[index] != -1': lambda S, B, r: (f'`res[{S.index}] = {S.res[S.index]}`：球还在 → 计算它在这一行的去向' if S.res[S.index] != -1
                                                 else f'`res[{S.index}] = -1`：已经卡住，==不用再算=='),
        'p = res[index]': '球现在在第 `{p}` 列',
        'if line[p] == 1': lambda S, B, r: (f'`line[{S.p}] = 1`：右挡板，球要往右走，看右边格' if S.line[S.p] == 1
                                           else f'`line[{S.p}] = -1`：左挡板，球要往左走，看左边格'),
        'if p != n - 1': lambda S, B, r: (
            f'`p` 不在最右列，且 `line[{S.p + 1}] = 1` 也是右挡板 → ==顺畅通过==' if (S.p != S.n - 1 and S.line[S.p + 1] == 1)
            else '右边是墙，或者右边是左挡板（V 形）→ ==卡住=='),
        'if p != 0': lambda S, B, r: (
            f'`p` 不在最左列，且 `line[{S.p - 1}] = -1` 也是左挡板 → ==顺畅通过==' if (S.p != 0 and S.line[S.p - 1] == -1)
            else '左边是墙，或者左边是右挡板（V 形）→ ==卡住=='),
        'res[index] = p + 1': '球落到下一行的 `p + 1`：`res[{index}] = {res[index]}`',
        'res[index] = p - 1': '球落到下一行的 `p - 1`：`res[{index}] = {res[index]}`',
        'res[index] = - 1': '球卡住：`res[{index}] = -1`，以后不再计算',
        'res[index] = -1': '球卡住：`res[{index}] = -1`，以后不再计算',
        'return res': '全部行处理完：`{res}`，不是 `-1` 的就是掉出来的列号',
    },
    cards=dict(
        one_liner='逐行推进：只有「同向相邻」的格子球才过得去',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['`m x n` 的箱子，每格斜挡板：`1` 导向右，`-1` 导向左',
                 '每列顶部放一颗球，求每颗球从底部掉出的列，卡住记 `-1`',
                 '示例：`[[1,1,1,-1],[-1,-1,1,1],[1,1,-1,-1]]` → `[1,2,-1,-1]`'],
        quote='对于行中的某个位置p，只有两种可能可以让上一行到达p这个位置的球有机会落到下一行而不是被卡住。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p` 是右挡板：`p` 不能是最右格，且 `p + 1` 也是右挡板，球落到 `p + 1`',
              '`p` 是左挡板：`p` 不能是最左格，且 `p - 1` 也是左挡板，球落到 `p - 1`',
              '其他情况都卡住；按行推进所有球，卡住的球不再计算'],
        summary=['时间 `O(mn)`，空间 `O(n)`（`res` 数组）',
                 '先判边界再看邻格：`p != n - 1 and line[p + 1] == 1`',
                 '`res` 一旦为 `-1` 就保持不变，要跳过',
                 '原文为 Python 2 写法，`res = range(n)` 已改为 `res = list(range(n))`（Python 3 的 range 不能赋值）',
                 '对比灵神：灵神一颗球走到底，yiduobo 一行一行推所有球'],
    ),
)
