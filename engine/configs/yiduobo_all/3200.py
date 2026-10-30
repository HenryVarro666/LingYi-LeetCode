CONFIG = dict(
    num=3200, title='三角形的最大高度', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='从大到小枚举行数 · 少球配小行', tags=[],
    code='''
class Solution(object):
    def maxHeightOfTriangle(self, red, blue):

        if red > blue:
            red, blue = blue, red
        
        for res in range(20, 0, -1):
            even = res // 2
            odd = res - even

            even_balls = (1 + even) * even
            odd_balls = odd ** 2

            if min(odd_balls, even_balls) <= red and max(odd_balls, even_balls) <= blue:
                return res
''',
    call='Solution().maxHeightOfTriangle(80, 60)',
    expect=15,
    views=[
        dict(type='text', fn=lambda S: f"少的颜色 red = {S['red']}，多的颜色 blue = {S['blue']}", size=30, h=60),
        dict(type='text', fn=lambda S: (f"试 `{S['res']}` 行：偶数行 {S['even']} 行，奇数行 {S['odd']} 行" if 'odd' in S else (f"试 `{S['res']}` 行" if 'res' in S else '')), size=30, h=60),
        dict(type='text', fn=lambda S: (f"偶数行共 =={S['even_balls']}== 球　奇数行共 =={S['odd_balls']}== 球" if 'even_balls' in S and 'odd_balls' in S and S.get('even') is not None and S['even_balls'] == (1 + S['even']) * S['even'] else ''), size=30, h=60),
        dict(type='text', fn=lambda S: (f"少的一类 `{min(S['odd_balls'], S['even_balls'])}` 用 red（{S['red']}），多的一类 `{max(S['odd_balls'], S['even_balls'])}` 用 blue（{S['blue']}）" if 'even_balls' in S and 'odd_balls' in S else ''), size=28, h=60),
    ],
    watch=['red', 'blue', ('res', 'res', 'green'), 'even', 'odd'],
    skip=['even = res', 'odd = res'],
        captions={
        'if red > blue': '默认 red <= blue：红蓝没有本质区别，不满足就交换',
        'red, blue = blue, red': '交换后 `red = {red}`，`blue = {blue}`',
        'for res in range': '球总数不超过 100，行数不可能超过 20 → 从 `{res}` 行往下试，==第一个成功的就是最大==',
        'even_balls = ': '`res = {res}` 行：偶数行 `{even}` 行、奇数行 `{odd}` 行。偶数行球数 `(1+{even})×{even}` = =={even_balls}==',
        'odd_balls = ': '奇数行球数 `{odd}^2` = =={odd_balls}==',
        'if min(odd_balls': lambda S, B, r: (
            f"少的 `{min(S.odd_balls, S.even_balls)}` 用 red（{S.red}），多的 `{max(S.odd_balls, S.even_balls)}` 用 blue（{S.blue}）→ "
            + ('==都放得下，就是这个高度==' if min(S.odd_balls, S.even_balls) <= S.red and max(S.odd_balls, S.even_balls) <= S.blue else '放不下，行数减一再试')),
        'return res': '`{res}` 行可以摆出来 → 最大高度 =={res}==',
    },
    cards=dict(
        one_liner='球少的颜色去填球数小的那类行，从大到小试行数',
        complexity='时间 `O(1)`（最多试 20 行），空间 `O(1)`',
        problem=['红球 `red` 个、蓝球 `blue` 个，摆第 `k` 行恰好 `k` 个同色球的三角形',
                 '相邻两行不同色，求最大高度',
                 '本视频：`red = 80, blue = 60` → `15`'],
        quote='奇数行上球的总数为1 + 3 + 5 + ... + (odd * 2 - 1)，求和的结果恰好就是odd^2。另一方面，偶数行上球的总数为2 + 4 + 6 + ... + even * 2，求和得结果为(even + 1) * even。',
        quote_src='—— yiduobo 题解原文',
        idea=['红蓝对称：先让 `red <= blue`，就不用讨论两种颜色分配',
              'n 行里偶数行 `n//2` 行，奇数行是剩下的',
              '两类行球数较小的给 red，较大的给 blue，都够就成功'],
        summary=['球数不超过 100，行数最多 20 行，直接暴力枚举',
                 '易错：偶数行球数是 `(1+even)*even`，不是 `even^2`',
                 '原文本身已是 Python 3 可运行（整除本就写成 `//`），未做改动',
                 '作者也提到可以二分答案'],
    ),
)
