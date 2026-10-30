G = [[3, 2], [1, 3], [3, 4], [0, 1]]

CONFIG = dict(
    num=3402, title='使每一列严格递增的最少操作次数', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='逐列从上往下贪心',
    tags=['贪心与思维', '难度分 1246'],
    code='''
class Solution:
    def minimumOperations(self, grid: List[List[int]]) -> int:
        ans = 0
        for col in zip(*grid):
            pre = -inf
            for x in col:
                ans += max(pre + 1 - x, 0)
                pre = max(pre + 1, x)
        return ans
''',
    call=f'Solution().minimumOperations({G})',
    expect=15,
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 正在扫描的那一列）', cell=90, h=380,
             color=lambda S, i, j, v: 'blue' if 'col' in S and tuple(S['grid'][r][j] for r in range(len(S['grid']))) == S['col'] else None),
        dict(type='text', fn=lambda S: (f"这一列 `col = {list(S['col'])}`，当前 `x = {S['x']}`" if 'col' in S and 'x' in S else ''), size=30),
        dict(type='text', fn=lambda S: (f"目标：`x` 至少要 ==大于前一个数== `{S['pre']}`，即 `≥ {S['pre'] + 1}`" if 'pre' in S and S['pre'] != float('-inf') else '第一个数不用变'), size=30),
    ],
    watch=[('pre', 'pre', 'blue'), ('x', 'x', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'for col in zip': '`zip(*grid)` 把每一列取出来：列与列互不影响，==各列独立处理==',
        'pre = -inf': '每列重新开始：前一个数设为 `-inf`，所以第一个数不需要操作',
        'ans += max': lambda S, B, r: (f'`x = {B.x}` 比 `pre + 1 = {B.pre + 1}` 小 → 至少增大到 `{B.pre + 1}`，操作 `{B.pre + 1 - B.x}` 次，累计 =={S.ans}=='
                                       if B.pre + 1 > B.x else f'`x = {B.x}` 已经大于 `pre = {B.pre}` → 不用操作'),
        'pre = max': lambda S, B, r: f'操作后的数是 `max(pre + 1, x) = {S.pre}`：==恰好增大到 pre+1 最优==，否则后面的数要增得更多',
        'return ans': '所有列处理完，返回总操作次数 `{ans}`',
    },
    cards=dict(
        one_liner='只能变大：每个数恰好增大到「前一个数 + 1」',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m×n` 非负矩阵，一次操作可把任一元素 `+1`',
                 '求让==每一列严格递增==的最少操作次数',
                 '示例：`[[3,2],[1,3],[3,4],[0,1]]` → `15`'],
        quote='增大到恰好等于 `pre+1` 是最优的（不然后面的数需要变得更大），操作 `pre+1-x` 次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只能变大，所以每列第一个数肯定不用变',
              '后面的 `x` 比 `pre` 大就不变，否则增大到 `pre+1`',
              '`pre` 记录的是「操作后」的前一个数，不是原值'],
        summary=['时间 `O(mn)`，空间 `O(1)`（`zip` 的迭代不额外存整列）',
                 '易错：`pre` 要更新为操作后的值 `max(pre+1, x)`，而不是 `x`',
                 '变形：严格递减、操作改成减 1、每次恰好加 k'],
    ),
)
