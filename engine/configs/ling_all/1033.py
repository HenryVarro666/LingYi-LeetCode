CONFIG = dict(
    num=1033, title='移动石子直到连续', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 分类讨论', tags=['灵神题单', '难度分 1421'],
    code='''
class Solution:
    def numMovesStones(self, a: int, b: int, c: int) -> List[int]:
        a, b, c = sorted((a, b, c))
        return [0 if c - a == 2 else
                1 if b - a <= 2 or c - b <= 2 else
                2,
                c - a - 2]
''',
    call='Solution().numMovesStones(5, 1, 2)',
    expect=[1, 2],
    views=[
        dict(type='text', fn=lambda S: f"排序后 `a={S['a']}, b={S['b']}, c={S['c']}`：`b-a={S['b']-S['a']}`，`c-b={S['c']-S['b']}`，`c-a={S['c']-S['a']}`" if S['a'] < S['b'] < S['c'] else '三枚石子 a、b、c，先排序'),
        dict(type='array', var=lambda S: [S['a'], S['b'], S['c']], label='石子位置（从小到大）', h=260, cell=120,
             color=lambda S, i, v: ['blue', 'yellow', 'pink'][i] if S['a'] < S['b'] < S['c'] else None),
    ],
    skip=['1 if b - a', 'c - a - 2]'],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'yellow'), ('c', 'c', 'pink')],
    captions={
        'a, b, c = sorted': '先排序，保证 `a < b < c`：现在 `a={a}, b={b}, c={c}`',
        'return [': lambda S, B, ret: '返回一个二元列表：[最小次数, 最大次数]，先逐个分支求值' if ret is None else f"最小 `{ret[0]}`：c-a={S['c']-S['a']}，b-a={S['b']-S['a']}，c-b={S['c']-S['b']}，只要有间距 ≤ 2 就一步到位；最大 `c-a-2 = {ret[1]}`：每步只挪一格。返回 =={ret}==",
    },
    cards=dict(
        one_liner='排序后只看三个间距，直接分类讨论',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['数轴上三枚石子，每回合把最左或最右的石子，放到两端之间的空位（不能和中间重合）',
                 '求让三枚石子连续所需的最小、最大移动次数',
                 '示例：`a=1, b=2, c=5` → `[1, 2]`'],
        quote='最大移动次数：a 和 c 向 b 靠拢，每次只移动一个单位长度，答案就是 c-a-2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最大：每次只让两端靠近一格，共 `c-a-2` 步（扣掉三个石子占的位置）',
              '最小：`c-a=2` 已连续，为 0；有间距 ≤ 2 就一步搞定，否则两端各挪一次共 2 步'],
        summary=['先 `sorted`，之后所有判断都基于 a<b<c',
                 '`b-a<=2 or c-b<=2` 同时覆盖：已有两颗相邻、或中间只隔一个空位',
                 '最小值的三种取值 0/1/2，要按顺序判断',
                 '进阶：1040 题是一万颗石子的版本'],
    ),
)
