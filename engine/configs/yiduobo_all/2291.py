def _txt(S):
    if 'pre' not in S:
        return '`f[j]`：预算为 j 时的最大收益'
    pre, fu = S['pre'], S['fu']
    if pre > fu or pre > S['budget']:
        return f'这支股票：买入 `{pre}`，未来 `{fu}` → 不赚钱或买不起，跳过'
    return f'这支股票：买入 `{pre}`，未来 `{fu}`，利润 `{fu - pre}`'


CONFIG = dict(
    num=2291, title='最大股票收益', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='0-1 背包 · 最大价值',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def maximumProfit(self, present, future, budget):

        f = [0] * (budget + 1)
        for pre, fu in zip(present, future):
            if pre > fu or pre > budget:
                continue

            for index in range(budget, pre - 1, -1):
                f[index] = max(f[index], f[index - pre] + fu - pre)

        return f[-1]
''',
    call='Solution().maximumProfit([5,4,6,2,3], [8,5,4,3,5], 10)',
    expect=6,
    max_steps=60,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='f', label='f[j]（预算 j 能赚的最多钱；蓝箭头 = index）', h=260, cell=80,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('pre', 'pre', 'pink'), ('fu', 'fu', 'cyan'), ('index', 'index', 'blue'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f = [0] * (budget + 1)': '`f[j]`：预算 `j` 时的最大收益；一支都不买就是 0',
        'for pre, fu in zip': lambda S, B, r: f'取下一支股票：现价 `{S.pre}`，未来价 `{S.fu}`',
        'if pre > fu': lambda S, B, r: ('`pre > fu`（会亏）或 `pre > budget`（买不起）→ ==不可能选它==，换下一支'
                                       if (S.pre > S.fu or S.pre > S.budget) else
                                       f'`{S.pre} ≤ {S.fu}` 且买得起 → 值得考虑'),
        'for index in range': '`index` 从大到小：倒序保证每支股票只买一次',
        'f[index] = max': '`max(不买 {B.f[index]}, 买：f[{index} − {pre}] + {fu} − {pre} = {B.f[index - pre]} + {fu - pre})` → =={f[index]}==',
        'return f[-1]': '预算 `budget` 下最大收益 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='每支股票买或不买：现价当重量，利润当价值',
        complexity='时间 `O(n·budget)`，空间 `O(budget)`',
        problem=['`present[i]` 是第 `i` 支股票现价，`future[i]` 是一年后的价格，初始预算 `budget`',
                 '每支股票最多买一次，卖出后拿回本金，求最大净收益',
                 '示例：`[5,4,6,2,3], [8,5,4,3,5], 10` → `6`'],
        quote='经典的背包问题，可以使用动态规划求解。令f[i][j]表示前i支股票，在初始预算为j时可以得到的最大收益',
        quote_src='—— yiduobo 题解原文',
        idea=['现价 `pre` 是占用的预算，利润 `fu − pre` 是价值，就是标准 0-1 背包',
              '`pre > fu` 的股票只会亏，直接跳过',
              '每轮只依赖上一轮 → 滚动数组，`index` 倒序'],
        summary=['时间 `O(n·budget)`，空间 `O(budget)`',
                 '`f[budget]` 即答案，因为 `f` 随预算单调不减，`f[-1]` 就是它',
                 '必须倒序遍历预算，否则一支股票会被买多次',
                 '原文为 Python 2 风格，代码未改（原文无需改动）'],
    ),
)
