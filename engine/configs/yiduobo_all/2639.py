G = [[-15, 1, 3], [5, 0, 12]]

CONFIG = dict(
    num=2639, title='查询网格图中每一列的宽度', difficulty='Easy', category='网格图',
    author='yiduobo', technique='逐格数位数',
    tags=[],
    code='''
class Solution(object):
    def findColumnWidth(self, grid):
        m = len(grid)
        n = len(grid[0])
        res = [0] * n
        for i in range(m):
            for j in range(n):
                v = grid[i][j]
                length = 0
                if v < 0:
                    length += 1
                    v = -v

                if v == 0:
                    length += 1
                else:
                    while v > 0:
                        length += 1
                        v //= 10

                res[j] = max(res[j], length)

        return res
''',
    call=f'Solution().findColumnWidth({G})',
    expect=[3, 1, 2],
    views=[
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '(i,j)')], h=260,
             color=lambda S, i, j, v: 'blue' if 'j' in S and j == S['j'] and i != S.get('i') else None),
        dict(type='array', var='res', label='res（每列当前最大宽度）', pointers={'j': 'blue'}, h=220),
        dict(type='text', fn=lambda S: f"当前数字 `v = {S['v']}`，已数长度 `length = {S['length']}`" if 'length' in S else '', size=28, h=60),
    ],
    watch=['i', 'j', 'v', 'length', ('res', 'res', 'green')],
    skip=['m = len', 'n = len', 'res = [0]', 'v = grid[i][j]', 'length = 0', 'v = -v'],
    captions={
        'for i in range': lambda S, B, r: (f'逐行扫描：`i = {S.i}`' if B.get('i') != S.i else '所有行都扫完了，退出循环'),
        'for j in range': lambda S, B, r: (f'取格子 `grid[{S.i}][{S.j}]` = =={S.grid[S.i][S.j]}==，从 `length = 0` 开始数' if B.get('j') != S.j else f'第 {S.i} 行的 {len(S.grid[0])} 个格子都处理完了'),
        'if v < 0': lambda S, B, r: (f'`v = {S.v} < 0`：是负数 → 先把负号算进长度，再取绝对值' if S.v < 0
                                     else f'`v = {S.v}` 不是负数，没有负号'),
        'length += 1': '`length` 加 1 → =={length}==',
        'if v == 0': lambda S, B, r: ('`v = 0`：0 也占一位' if S.v == 0 else f'`v = {S.v}` 不为 0，要一位一位数'),
        'while v > 0': lambda S, B, r: (f'`v = {S.v} > 0`，还有数位没数' if S.v > 0 else '`v = 0`，数位数完了'),
        'v //= 10': '去掉个位：`v` → {v}',
        'res[j] = max': '`res[{j}] = max({B.res[j]}, {length})` = =={res[j]}==',
        'return res': '每列宽度：`{res}`',
    },
    cards=dict(
        one_liner='逐个格子数位数，用最大值更新这一列的答案',
        complexity='时间 `O(mn·logU)`，空间 `O(1)`',
        problem=['矩阵一列的宽度 = 该列数字字符串长度的最大值，负号也算一位',
                 '返回每一列的宽度',
                 '本视频：`[[-15,1,3],[5,0,12]]` → `[3,1,2]`'],
        quote='直接遍历网格中的每个位置，对于grid[i][j]，若其为负数，则需要先将其变为正数，同时将其对应的长度加上1，也就是负号的长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['负数：先给长度加 1（负号），再取相反数',
              '`0` 单独处理：`while v > 0` 进不去，所以要手动记 1 位',
              '不断除 10 数位数，再用 `max` 更新 `res[j]`'],
        summary=['时间 `O(mn·logU)`，空间 `O(1)`（返回值不计）',
                 '易错：`0` 的长度是 1；负号要加 1',
                 '原文为 Python 2 风格，只删去了空行与类型说明（代码本身无需改动）',
                 '对比灵神：灵神只对列最大/最小值数位，yiduobo 对每个格子都数'],
    ),
)
