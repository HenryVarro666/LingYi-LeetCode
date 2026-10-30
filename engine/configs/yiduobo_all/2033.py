CONFIG = dict(
    num=2033, title='获取单值网格的最小操作数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='写成 ax+b · 中位数',
    tags=['灵神题单', '难度分 1672'],
    code='''
class Solution(object):
    def minOperations(self, grid, x):

        m = len(grid)
        n = len(grid[0])

        r = grid[0][0] % x
        num_list = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] % x != r:
                    return -1
                num_list.append(grid[i][j] // x)
        
        num_list = sorted(num_list)
        target = num_list[len(num_list) // 2]
        res = 0
        for num in num_list:
            res += abs(num - target)
        
        return res
''',
    call='Solution().minOperations([[2,4,10],[6,8,12]], 2)',
    expect=9,
    views=[
        dict(type='grid', var='grid', h=230, label='grid',
             cursors=[('i', 'j', 'yellow', '(i,j)')],
             color=lambda S, i, j, v: 'red' if 'r' in S and 'x' in S and v % S['x'] != S['r'] else None),
        dict(type='array', var='num_list', h=210, label='num_list（每个数写成 ax+b 里的 a）',
             color=lambda S, i, v: 'green' if 'target' in S and i == len(S['num_list']) // 2 else None,
             pointers={}),
        dict(type='text', h=60, size=28,
             fn=lambda S: f"`r = {S['r']}`：每个数 `% {S['x']}` 的余数都要是它" if 'r' in S and 'target' not in S else
             (f"`target = {S['target']}`，累计 `res = {S['res']}`" if 'target' in S else '')),
    ],
    watch=['x', 'r', ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('target', 'target', 'green'), ('res', 'res', 'yellow')],
    captions={
        'r = grid': '`r = {grid[0][0]} % {x} = {r}`：加减 `x` 不改变余数，先拿它当标准',
        'if grid[i][j] % x != r': '`grid[{i}][{j}] % {x} = {grid[i][j] % x}`，和 `r = {r}` {"一致" if grid[i][j] % x == r else "不一致 → 无法变成单值网格"}',
        'return -1': '余数不一致 → ==返回 -1==',
        'num_list.append': '写成 `ax+b`，`b` 都相同，只留 `a = {grid[i][j]} // {x} = {grid[i][j] // x}` → `{num_list}`',
        'sorted': '排序：`{num_list}`',
        'target =': '取中位数 `num_list[{len(num_list)} // 2] = {target}`：偶数长度时两个中间数任选一个都行',
        'res += abs': '`|{num} − {target}| = {abs(num - target)}`，`res` → {res}',
        'return res': '所有 `a` 都挪到 `{target}`，共 =={res}== 次操作',
    },
    cards=dict(
        one_liner='先查余数，再把每个数的 a 全拉到中位数',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['网格每次可以让任一元素 ==加 x 或减 x==，求全部相等的最少次数，不行返回 `-1`',
                 '示例：`[[2,4],[6,8]], x=2` → `4`',
                 '本视频：`[[2,4,10],[6,8,12]], x=2` → `9`'],
        quote='无论怎么操作，网格中的每个数对x的余数是不会变的，那么就需要先检测网格中每个数对x取模的余数是否一致，如果不一致，那么直接返回-1。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个数写成 `ax + b`，`b` 全相同 → 只要让各个 `a` 相等',
              '问题变成「数组每次加减 1，变成一致」，最优是==变成中位数==',
              '证明：两两配对，目标落在 `[mi, ma]` 之间时代价最小 `ma - mi`'],
        summary=['时间 `O(mn log(mn))`，快速选择找中位数可降到 `O(mn)`',
                 '偶数长度不必求平均，取中间两个数之一即可',
                 '原文为 Python 2 写法，`/` 整数除法已改为 `//`（共两处）',
                 '对比灵神：他直接对原数排序再除以 `x`；这里先除以 `x` 再比'],
    ),
)
