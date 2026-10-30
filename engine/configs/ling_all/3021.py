def _grid(S):
    n, m = S['n'], S['m']
    return [['A' if (x + y) % 2 else '' for y in range(1, m + 1)] for x in range(1, n + 1)]


CONFIG = dict(
    num=3021, title='Alice 和 Bob 玩鲜花游戏', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='奇偶性 · 化简为 n·m/2',
    code='''
class Solution:
    def flowerGame(self, n: int, m: int) -> int:
        return n * m // 2
''',
    call='Solution().flowerGame(4, 5)',
    expect=10,
    views=[
        dict(type='table', var=_grid, label='行 x=1..n，列 y=1..m；A = x+y 为奇数，Alice 赢', rows=lambda S: list(range(1, S['n'] + 1)),
             cols=lambda S: list(range(1, S['m'] + 1)), cell=96, h=330,
             color=lambda S, i, j, v: 'green' if v else None),
        dict(type='text', h=110, size=30, fn=lambda S: f"`n·m = {S['n']*S['m']}`，其中一半的格子奇偶和为奇" ),
    ],
    watch=['n', 'm'],
    captions={
        'return': '每回合摘一朵，摘最后一朵的赢 → `x+y` 为奇数 Alice 赢。奇偶各占一半：`{n} × {m} // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='谁摘最后一朵谁赢，所以只看 x+y 是不是奇数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两排花 `x`、`y` 朵，Alice 先手，每次在一排摘一朵，摘完最后一朵的人赢',
                 '数 `x∈[1,n]`、`y∈[1,m]` 中 Alice 必赢的对数',
                 '示例：`n=3, m=2` → `3`；本视频：`n=4, m=5` → `10`'],
        quote='每回合摘一朵花，摘到最后一朵花的人获胜。所以当且仅当鲜花个数 x+y 是奇数时，Alice 摘到最后一朵花。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 偶 `y` 奇，或 `x` 奇 `y` 偶：偶数 `floor(n/2)` 个，奇数 `ceil(n/2)` 个，乘起来相加',
              '分 `n` 偶、`m` 偶、都奇三种情况化简，都等于 `floor(nm/2)`',
              '也可以看成棋盘：奇偶格子各占一半'],
        summary=['时间、空间都是 `O(1)`',
                 '易错：`n*m` 可能很大，用整除 `//`，Python 不会溢出',
                 '答案是 `n*m // 2`，不需要枚举数对',
                 '同类：只看总数奇偶的博弈题'],
        after=[dict(heading='三种情况化简', lines=['`n` 偶：`n/2 × (ceil(m/2) + floor(m/2)) = nm/2`',
                                                  '`m` 偶：同理，`nm/2`',
                                                  '都奇：`(n−1)(m+1)/4 + (n+1)(m−1)/4 = (nm−1)/2`，即 `floor(nm/2)`'])],
    ),
)
