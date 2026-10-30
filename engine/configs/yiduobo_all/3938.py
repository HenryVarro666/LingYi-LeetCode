G = [[4, -2, -3], [-1, -3, -1], [-4, 2, -1]]


def _gcolor(S, i, j, v):
    g, nums = S['grid'], S.get('nums')
    m, n = len(g), len(g[0])
    if nums is None:
        if S['_line'] in (9, 10, 11, 12) and 0 < i < m - 1 and 0 < j < n - 1:
            return 'yellow'
        return None
    for r in range(m):
        if g[r] is nums:
            return 'blue' if i == r else None
    for c in range(n):
        if [row[c] for row in g] == nums:
            return 'blue' if j == c else None
    return None


def _txt(S):
    if 'now' not in S or 'nums' not in S:
        return '边界上的共享段长度必须 >= 2；内部格子可以单独成段'
    return f"`now = {S['now']}`（以当前位置结尾的和），`ma = {S['ma']}`（长度 >= 2 的最大和）"


CONFIG = dict(
    num=3938, title='矩阵中最大共享路径和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='行列最大子段和 + 内部单格（图论度数分析）',
    tags=['一、入门 DP', '难度分 2252'],
    code='''
class Solution(object):
    def maxScore(self, grid):
        
        m = len(grid)
        n = len(grid[0])

        res = None
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if res is None or res < grid[i][j]:
                    res = grid[i][j]
        
        def calc(nums):
            ma = None
            now = nums[0]
            for v in nums[1:]:
                now += v
                if ma is None or ma < now:
                    ma = now
                if now < v:
                    now = v
            
            return ma

        for i in range(m):
            ma = calc(grid[i])
            if res is None or res < ma:
                res = ma
        
        for j in range(n):
            nums = [grid[i][j] for i in range(m)]
            ma = calc(nums)
            if res is None or res < ma:
                res = ma
        
        return res
''',
    call=f'Solution().maxScore({G})',
    expect=3,
    max_steps=58,
    skip=['m = len', 'n = len', 'res = None', 'ma = None', 'for j in range(1, n - 1)', 'for i in range(1, m - 1)',
          'for i in range(m):', 'for j in range(n):', 'now = nums[0]', 'nums = [grid', 'ma = now'],
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 内部单格；蓝 = 正在算的行/列）', cell=100, h=330, color=_gcolor),
        dict(type='array', var='nums', label='nums（当前这一行/列）', cell=84, h=150),
        dict(type='text', fn=_txt, size=26, h=60),
    ],
    watch=[('v', 'v', 'blue'), ('now', 'now', 'cyan'), ('ma', 'ma', 'pink'), ('res', 'res', 'green')],
    captions={
        'if res is None or res < grid[i][j]': '内部格子 `grid[{i}][{j}] = {grid[i][j]}`：度数为 4，能单独成共享段 → 候选答案（当前 `res` = {B.res}）',
        'res = grid[i][j]': '`res` 更新为内部格子的值 {res}',
        'now += v': '`now += {v}` → `now` 变为 =={now}==：这是以 `v` 结尾、至少两个数的和（因为 now 起始就是 nums[0] 或更长）',
        'ma < now': lambda S, B, r: (f'`now = {S.now}` 比 `ma` 大 → 更新 `ma = {S.now}`' if B.ma is None or B.ma < S.now
                                     else f'`now = {S.now}` 不比 `ma = {S.ma}` 大 → 不更新'),
        'ma = now': '`ma` = {ma}',
        'if now < v': lambda S, B, r: (f'`now = {S.now} < v = {S.v}`：前面的和拖后腿 → 下次从 `v` 重新开始' if S.now < S.v
                                       else f'`now = {S.now} ≥ v = {S.v}`：前面的和有帮助，继续累加'),
        'now = v': '`now = v = {now}`：丢掉前面，只保留当前这个数作为段首',
        'return ma': '这一行/列长度 >= 2 的最大子段和 = `{ma}`',
        'ma = calc(grid[i])': '对第 {i} 行调用 `calc`：求这一行里长度 >= 2 的最大子段和',
        'ma = calc(nums)': '对第 {j} 列调用 `calc`：求这一列里长度 >= 2 的最大子段和',
        'if res is None or res < ma': '`res = max(res, ma)`：当前 `res = {res}`，`ma = {ma}`',
        'res = ma': '`res` 更新为 `ma` = {res}',
        'return res': '所有行、列、内部格子里取最大，答案 `{ret}`',
    },
    cards=dict(
        one_liner='两条路径至多重叠一段 → 每行每列求最大子段和，边界段长度要 >= 2',
        complexity='时间 `O(mn)`，空间 `O(m)`',
        problem=['玩家 1 从左上走到右下（右/下），玩家 2 从左下走到右上（右/上）',
                 '两条路径重叠的格子叫共享格，求共享格的值之和的最大值',
                 '本视频：`[[4,-2,-3],[-1,-3,-1],[-4,2,-1]]` → `3`'],
        quote='两个玩家的行进路径是两条交叉的折线，这也就意味着至多只会有一段路径重叠在一起。',
        quote_src='—— yiduobo 题解原文',
        idea=['重叠只会是一行或一列里的一段 → 求每行每列的最大子段和',
              '图论角度：四边上的格子度数为 3，角上为 2，两条路径一进一出必共享相邻格 → 子段长度 >= 2',
              '内部格子度数为 4，进出可以不共享邻居 → 可以单独成段'],
        summary=['时间 `O(mn)`，每行每列各扫一遍',
                 '`calc` 里 `now` 先加上 `v` 再更新 `ma`，所以 `ma` 至少包含两个数',
                 '内部单格要单独遍历（`1..m-2`、`1..n-2`），不能漏',
                 '原文是 Python 3 兼容写法，代码未改',
                 '对比灵神：灵神用 `f + x` 先更新答案，yiduobo 用 `now` 加完再更新'],
    ),
)
