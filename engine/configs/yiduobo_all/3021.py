def _grid(S):
    n, m = S['n'], S['m']
    return [['A' if (x + y) % 2 else '' for y in range(1, m + 1)] for x in range(1, n + 1)]


CONFIG = dict(
    num=3021, title='Alice 和 Bob 玩鲜花游戏', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='奇偶计数 · 乘法原理',
    code='''
class Solution(object):
    def flowerGame(self, n, m):

        even_n = n // 2
        odd_n = n - even_n

        even_m = m // 2
        odd_m = m - even_m

        return even_n * odd_m + odd_n * even_m
''',
    call='Solution().flowerGame(4, 5)',
    expect=10,
    views=[
        dict(type='table', var=_grid, label='行 x=1..n，列 y=1..m；A = 总数为奇数，Alice 赢',
             rows=lambda S: list(range(1, S['n'] + 1)), cols=lambda S: list(range(1, S['m'] + 1)),
             cell=96, h=300, color=lambda S, i, j, v: 'green' if v else None),
        dict(type='text', h=130, size=28, fn=lambda S: (
            f"n 的 偶数 `{S['even_n']}` 个，奇数 `{S['odd_n']}` 个" if 'odd_n' in S and 'odd_m' not in S else
            f"m 的 偶数 `{S['even_m']}` 个，奇数 `{S['odd_m']}` 个" if 'odd_m' in S else '')),
    ],
    watch=['n', 'm', 'even_n', 'odd_n', 'even_m', 'odd_m'],
    captions={
        'even_n =': '`[1, {n}]` 里偶数有 `n // 2` = =={even_n}== 个',
        'odd_n =': '其余是奇数：`{n} − {even_n}` = =={odd_n}== 个',
        'even_m =': '`[1, {m}]` 里偶数有 `m // 2` = =={even_m}== 个',
        'odd_m =': '其余是奇数：`{m} − {even_m}` = =={odd_m}== 个',
        'return': '总数为奇数：偶×奇 + 奇×偶 = `{even_n}×{odd_m} + {odd_n}×{even_m}` = =={ret}==',
    },
    cards=dict(
        one_liner='方向无关紧要，总花数是奇数 Alice 才赢',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['两排花 `x`、`y` 朵，Alice 先手，每次摘一朵，摘完最后一朵的人赢',
                 '数 `x∈[1,n]`、`y∈[1,m]` 中 Alice 必赢的对数',
                 '本视频：`n=4, m=5` → `10`'],
        quote='每次行动虽然可以选择方向，但是要求把所有鲜花都摘完，因此方向在这里无关紧要。如果鲜花的数量为奇数，那么Alice获胜。',
        quote_src='—— yiduobo 题解原文',
        idea=['总数 `x+y` 是奇数 → Alice 赢',
              '要奇数：Alice 那排奇数、Bob 那排偶数，或相反',
              '先算偶数个数 `n // 2`，奇数是 `n` 减去它，再用乘法原理'],
        summary=['时间、空间都是 `O(1)`',
                 '易错：奇数个数是 `n − n//2`，不是 `n//2`',
                 '两种组合要相加：偶×奇 + 奇×偶',
                 '原文已是 `//` 写法，代码无需改动',
                 '对比灵神：灵神进一步化简成 `n*m//2`；yiduobo 停在奇偶计数'],
        after=[dict(heading='验算本例', lines=['`n=4`：偶 2、奇 2；`m=5`：偶 2、奇 3',
                                              '偶×奇 = `2×3 = 6`，奇×偶 = `2×2 = 4`',
                                              '合计 `6 + 4 = 10`，与代码一致'])],
    ),
)
