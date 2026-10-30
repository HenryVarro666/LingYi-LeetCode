def _txt(S):
    if 'median' in S:
        a, m, x = S['a'], S['median'], S['x']
        t = ' + '.join(f'|{v}−{m}|' for v in a)
        return f'`({t}) ÷ {x}` = =={sum(abs(v - m) for v in a) // x}=='
    if 'target' in S:
        return f'每个数 `% {S["x"]}` 都必须等于 ==`{S["target"]}`==，否则返回 -1'
    return ''


CONFIG = dict(
    num=2033, title='获取单值网格的最小操作数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='模 x 判无解 + 中位数贪心',
    tags=['贪心与思维', '难度分 1672'],
    code='''
class Solution:
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        a = []
        target = grid[0][0] % x

        # 1. 判断是否无解
        for row in grid:
            for v in row:
                if v % x != target:  # 每个数模 x 都必须相等
                    return -1
            a += row

        # 2. 计算 grid 的中位数 median
        a.sort()
        median = a[len(a) // 2]

        # 3. 计算操作次数
        return sum(abs(v - median) for v in a) // x
''',
    call='Solution().minOperations([[2,10],[4,6],[8,14]], 2)',
    expect=10,
    views=[
        dict(type='text', fn=_txt, size=30, h=70),
        dict(type='grid', var='grid', h=260, label='grid',
             color=lambda S, i, j, v: 'red' if 'target' in S and 'x' in S and v % S['x'] != S['target'] else None),
        dict(type='array', var='a', h=200, label='a（拍平 grid，之后排序）',
             color=lambda S, i, v: 'green' if 'median' in S and i == len(S['a']) // 2 else None),
    ],
    watch=['x', 'target', ('v', 'v', 'yellow'), ('median', 'median', 'green')],
    captions={
        'target = grid': '`target = {grid[0][0]} % {x} = {target}`：操作不改变模 `x` 的余数，所有数的余数必须和它一样',
        'if v % x != target': '`{v} % {x} = {v % x}`，和 `target = {target}` {"相等 → 这个数可以参与" if v % x == target else "不等 → 永远凑不成同一个数"}',
        'return -1': '余数不同，无解 → 返回 ==-1==',
        'a += row': '这一行都合法，拍平加入 `a` → `{a}`',
        'a.sort()': '排序后 `a = {a}`，中位数就在中间',
        'median =': '`median = a[{len(a)} // 2] = a[{len(a)//2}] = {median}`：往中间聚拢，总移动距离最小',
        'return sum': '总距离 `{ret * x}` ÷ `{x}` = =={ret}== 次操作',
    },
    cards=dict(
        one_liner='先看余数能否一致，再把所有数拉到中位数',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['每次可以让 `grid` 中任一元素 ==加 x 或减 x==，求变成全相等的最少操作数，不可能则 `-1`',
                 '示例：`[[2,4],[6,8]], x=2` → `4`',
                 '本视频：`[[2,10],[4,6],[8,14]], x=2` → `10`'],
        quote='想象操场上有一些人，把这些人聚在一起，怎么移动最迅速？往「中间」移动是最迅速的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`(v + kx) % x` 不变：所有数模 `x` 的结果必须一样，否则无解',
              '把所有数变成==中位数==最优，总移动距离除以 `x` 就是操作次数'],
        summary=['时间 `O(mn log(mn))`，瓶颈是排序；快速选择可到 `O(mn)`',
                 '先判无解再排序；中位数取 `a[len(a)//2]`，偶数长度取哪个中间数都行',
                 '如果有负数，模的结果有正有负，改判 `(v - grid[0][0]) % x != 0`',
                 '模板题：中位数贪心（如 462、2448）'],
    ),
)
