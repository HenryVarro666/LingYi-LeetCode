G = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

CONFIG = dict(
    num=3417, title='跳过交替单元格的之字形遍历', difficulty='Easy', category='网格图',
    author='yiduobo', technique='之字形 + 下标和为偶数',
    code='''
class Solution(object):
    def zigzagTraversal(self, grid):
        
        m = len(grid)
        n = len(grid[0])
        
        res = []
        for i in range(m):
            if i % 2 == 0:
                start, end, step = 0, n, 1
            else:
                start, end, step = n - 1, -1, -1
            
            for j in range(start, end, step):
                if (i + j) % 2 == 0:
                    res.append(grid[i][j])
        
        return res
''',
    call=f'Solution().zigzagTraversal({G})',
    expect=[1, 3, 8, 6, 9, 11],
    skip=['m = len', 'n = len', 'res = []'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前格，绿 = 已加入答案）', cell=84, h=330,
             cursors=[('i', 'j', 'blue')],
             color=lambda S, i, j, v: 'green' if 'res' in S and v in S['res'] else None),
        dict(type='array', var='res', label='res', cell=70, h=170, color=lambda S, k, v: 'green'),
        dict(type='text', fn=lambda S: (f"`i + j = {S['i']} + {S['j']} = {S['i'] + S['j']}`，" + ('==偶数 → 取==' if (S['i'] + S['j']) % 2 == 0 else '奇数 → 跳过')) if 'j' in S and 'i' in S and S['_line'] in (14, 15, 16) else '', size=28),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'start', 'end', 'step', ('res', 'res', 'green')],
    captions={
        'if i % 2 == 0': lambda S, B, r: (f'`i = {S.i}` 是偶数行 → 从左往右' if S.i % 2 == 0 else f'`i = {S.i}` 是奇数行 → 从右往左'),
        'start, end, step = 0': '偶数行：`j` 从 `0` 走到 `{n-1}`，步长 `1`',
        'start, end, step = n - 1': '奇数行：`j` 从 `{n-1}` 走到 `0`，步长 `-1`（`end = -1` 是开区间）',
        'for j in range': lambda S, B, r: (f'走到格子 `({S.i},{S.j})`，值 `{S.grid[S.i][S.j]}`' if not (S.get('j') == B.get('j') and S.j == S.end - S.step) else '这一行走完了'),
        'if (i + j) % 2 == 0': lambda S, B, r: (f'`({S.i} + {S.j}) % 2 = {(S.i + S.j) % 2}` → ==下标和为偶数，要取==' if (S.i + S.j) % 2 == 0 else f'`({S.i} + {S.j}) % 2 = 1` → 下标和为奇数，跳过'),
        'res.append': '取 `grid[{i}][{j}] = {grid[i][j]}`：`res = {res}`',
        'for i in range': lambda S, B, r: (f'开始第 `{S.i}` 行' if S.get('i') != B.get('i') or 'i' not in B else '所有行都走完了'),
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='之字形里被取到的格子，下标和 i+j 都是偶数',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计）',
        problem=['`m x n` 的正整数网格，按之字形遍历：偶数行向右，奇数行向左',
                 '遍历时==跳过每个交替的单元格==，按顺序记录访问到的值',
                 '示例：`[[1,2],[3,4]]` → `[1,4]`',
                 '本视频：`3x4` 的 `1..12` → `[1,3,8,6,9,11]`'],
        quote='观察题目给出的样例可以发现，所有被遍历到的单元格的奇偶下标之和都是偶数',
        quote_src='—— yiduobo 题解原文',
        idea=['偶数行 `start, end, step = 0, n, 1`；奇数行 `n - 1, -1, -1`',
              '不用单独维护“选/跳”的开关，直接判断 `(i + j) % 2 == 0`',
              '偶数行取 `j` 为偶数的列，奇数行取 `j` 为奇数的列，恰好交替'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：奇数行 `end = -1`，`range` 才包含下标 `0`',
                 '本例 `n = 4`：第 0 行取 1、3，第 1 行从右往左取 8、6，换行后依然交替',
                 '原文为 Python 2 风格，代码无需修改，Python 3 直接可运行',
                 '对比灵神：灵神用取反标记 + 反转奇数行；这里靠下标奇偶性直接判断'],
    ),
)
