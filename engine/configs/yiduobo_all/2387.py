GRID = [[1, 3, 5], [2, 6, 9], [3, 6, 9]]


def _cnt_color(S, i, j, v):
    I = S.get('_inner', {})
    if 'v' in I:
        return 'green' if v <= I['v'] else None
    return None


CONFIG = dict(
    num=2387, title='行排序矩阵的中位数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 + 行内二分计数',
    tags=['二分算法'],
    code='''
class Solution(object):
    def matrixMedian(self, grid):

        m = len(grid)
        n = len(grid[0])

        def check(v):
            cnt = 0
            for i in range(m):
                if v < grid[i][0]:
                    continue
                left = 0
                right = n - 1
                while left < right:
                    mid = (left + right + 1) // 2
                    if grid[i][mid] <= v:
                        left = mid
                    else:
                        right = mid - 1

                cnt += left + 1

            return cnt > m * n // 2

        left = 1
        right = 10 ** 6
        while left < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid + 1

        return left
''',
    call=f'Solution().matrixMedian({GRID!r})',
    expect=5,
    skip=[9, 12, 13, 14, 15, 16, 17, 19],
    max_steps=46,
    views=[
        dict(type='grid', var='grid', label='grid（每行单调不减；绿 = 当前检查的 v 以内的数）', cell=96, h=330,
             color=_cnt_color, cursors=[('i', 'left', 'yellow', '行内二分')]),
        dict(type='text', size=26, h=130,
             fn=lambda S: (f"答案区间 [{S['left']}, {S['right']}]，试探 mid = {S['mid']}" if S.get('_inner', {}).get('v') is None and 'mid' in S and 'right' in S
                           else (f"check(v={S['_inner']['v']})：已累计 {S['_inner'].get('cnt', 0)} 个 <= v，一半是 {len(S['grid'])*len(S['grid'][0])//2}" if 'v' in S.get('_inner', {}) else ''))),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'mid', ('cnt', lambda S: S.get('_inner', {}).get('cnt', S.get('cnt')), 'green')],
    captions={
        'm = len(grid)': '`m = {m}` 行',
        'n = len(grid[0])': '`n = {n}` 列，共 `m × n = {m * n}` 个数',
        'if v < grid[i][0]': lambda S, B, r: (f'第 `{S.i}` 行最小值 `{S.grid[S.i][0]}` > v = `{S.v}`：这一行没有数 <= v，跳过'
                                              if S.v < S.grid[S.i][0] else f'第 `{S.i}` 行最小值 `{S.grid[S.i][0]}` <= v = `{S.v}`：这一行至少有 1 个，二分找有几个'),
        'continue': '这一行贡献 0 个',
        'cnt += left + 1': '第 `{i}` 行有 `left + 1 = {left + 1}` 个数 <= v → `cnt = {cnt}`',
        'return cnt > m * n // 2': lambda S, B, r: f'`cnt = {S.cnt}` {"大于" if S.cnt > S.m * S.n // 2 else "不大于"} `{S.m * S.n // 2}`：==v {"够大" if S.cnt > S.m * S.n // 2 else "太小"}=={"，中位数 <= v" if S.cnt > S.m * S.n // 2 else "，中位数 > v"}',
        'left = 1': '答案至少是 1（二分答案，不是二分下标）：`left = 1`',
        'right = 10 ** 6': '题目给的值域上界：`right = 10 ** 6`',
        'while left < right': lambda S, B, r: (f'答案区间 `[{S.left}, {S.right}]` 还没缩成一个数 → 继续' if S.left < S.right else f'区间只剩 `{S.left}` → 结束'),
        'mid = (left + right) // 2': '试探答案 `mid = {mid}`',
        'if check(mid)': '假设中位数 `<= {mid}`：进 `check`，数一数矩阵里有多少个数 `<= {mid}`',
        30: '`mid` 够大，答案可能就是它：`right = {right}`',
        32: '`mid` 太小：`left = {left}`',
        'return left': '区间收敛到 `{left}`：这就是中位数',
    },
    cards=dict(
        one_liner='二分答案：看 <= mid 的数是否超过一半',
        complexity='时间 `O(m log n log C)`，空间 `O(1)`',
        problem=['`m` 行 `n` 列矩阵，每行单调不减，`m × n` 为奇数',
                 '求所有数的中位数',
                 '本视频：`[[1,3,5],[2,6,9],[3,6,9]]` → `5`'],
        quote='首先二分答案res，接下来遍历每一行，在当前行中通过二分找出当前行中有多少个数小于等于res。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层二分答案 `v`：`<= v` 的数超过一半时，中位数 `<= v`',
              '内层每行有序，再二分找出这一行有几个 `<= v`',
              '作者说明题目想要 `O(m log n)`，他没想到，用的是这个较慢的写法'],
        summary=['外层 `log C`（C = 10^6，约 20 轮），每轮 `m` 行，每行二分 `log n`',
                 '行内二分找「最后一个 <= v」，所以 `mid` 要向上取整 `+ 1`',
                 '判断是 `cnt > m * n // 2`：奇数个数时刚好对应中位数',
                 '原文为 Python 2 写法，三处整数除法 `/` 已改为 `//`',
                 '视频只展开前几轮，其余折叠为快进'],
    ),
)
