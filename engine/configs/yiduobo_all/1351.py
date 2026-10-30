CONFIG = dict(
    num=1351, title='统计有序矩阵中的负数', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='逐行扫描 · 非负边界单调左移',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def countNegatives(self, grid):

        m = len(grid)
        n = len(grid[0])
        res = m * n
        now = n - 1
        for index in range(m):
            while now >= 0 and grid[index][now] < 0:
                now -= 1

            if now == -1:
                break

            res = res - now - 1

        return res
''',
    call='Solution().countNegatives([[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]])',
    expect=8,
    views=[
        dict(type='text', fn=lambda S: (f"总数 `{S['m']}×{S['n']}` 先全算作非负，每行扣掉 `now + 1` 个：`res` = =={S['res']}==" if 'res' in S else '')),
        dict(type='grid', var='grid', cursors=[('index', 'now', 'yellow', '(行,now)')], h=420, cell=96,
             color=lambda S, i, j, v: ('pink' if v < 0 else None) if 'res' in S else None,
             dim=lambda S, i, j, v: ('now' in S and 'index' in S and (i < S['index'] and j > S['now']) )),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = m * n': '先假设全是非负数：`res = {m} × {n} = {res}`，之后逐行扣掉非负数的个数',
        'now = n - 1': '`now`：当前行最右边的非负数下标，初始在最后一列 `{now}`',
        'while now >= 0': lambda S, B, r: (f'`grid[{S.index}][{S.now}] = {S.grid[S.index][S.now]} < 0`：还是负数 → `now` 继续左移' if (S.now >= 0 and S.grid[S.index][S.now] < 0) else f'`now = {S.now}` 处是非负数（或已越界）→ 本行边界找到'),
        'now -= 1': '`now` → {now}。行与行也有序：下一行的边界不会比它更靠右',
        'if now == -1': lambda S, B, r: ('`now = -1`：本行及以下全是负数 → 结束' if S.now == -1 else f'`now = {S.now}`，本行还有非负数，继续'),
        'res = res - now - 1': '本行第 0 到 `{B.now}` 列共 `{now + 1}` 个非负数，从 `res` 里扣掉：`res` → =={res}==',
        'return res': '剩下的就是负数个数 `{res}`',
    },
    cards=dict(
        one_liner='反过来数非负数，边界 now 只左移不回头，总共 O(m+n)',
        complexity='时间 `O(m + n)`，空间 `O(1)`',
        problem=['`m*n` 矩阵，每行每列都非严格递减，统计负数个数',
                 '本视频：4×4 示例 → `8`'],
        quote='题目要求矩阵中负数的数目，那么我们可以反过来求矩阵中非负数的数目，再用总数减去这个数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['每行里非负数都在前面：只要找到最后一个非负数下标 `now`，就有 `now + 1` 个',
              '行之间也单调：上一行 `now + 1` 处是负数，下一行同一位置更小，也是负数',
              '所以下一行直接从上一行的 `now` 往前找，`now` 不会回头'],
        summary=['时间 `O(m + n)`，空间 `O(1)`',
                 '`now == -1` 时后面的行全是负数，直接 `break`',
                 '先用 `m*n` 当总数，每行扣掉非负数个数',
                 '对比灵神：灵神从右上角数负数，yiduobo 逐行数非负数'],
    ),
)
