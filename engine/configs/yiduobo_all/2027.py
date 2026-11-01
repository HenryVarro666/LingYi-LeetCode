CONFIG = dict(
    num=2027, title='转换字符串的最少操作次数', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='最左 X 必须操作 · 一趟遍历',
    tags=['贪心与思维', '从最左开始贪心', '难度分 1346'],
    code='''
class Solution(object):
    def minimumMoves(self, s):

        p = 0
        res = 0
        while p < len(s):
            if s[p] == 'X':
                res += 1
                p += 3
            else:
                p += 1
        
        return res
''',
    call='Solution().minimumMoves("XXOXOXOOXX")',
    expect=3,
    views=[
        dict(type='string', var='s', pointers={'p': 'blue'}, label='s', h=200,
             color=lambda S, i, v: 'orange' if v == 'X' else None,
             dim=lambda S, i, v: 'p' in S and i < S['p']),
        dict(type='text', h=70, fn=lambda S: f"已操作 ==`{S['res']}`== 次" if 'res' in S else ''),
    ],
    watch=[('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'p = 0': '从最左边开始扫：`p = 0`',
        'if s[p]': lambda S, B, r: (f'`s[{S.p}] = X`：最左边的 X 必须被某次操作覆盖' if S.s[S.p] == 'X' else f'`s[{S.p}] = O`：不用管，往右一位'),
        'res += 1': '以这个 X 为起点操作一次，覆盖 `{p}..{p+2}`：`res` → =={res}==',
        'p += 3': '这三位都变成 O 了，直接跳到 `p = {p}`',
        'p += 1': '`p` → {p}',
        'return res': '最少操作 `{ret}` 次',
    },
    cards=dict(
        one_liner='最左边的 X 必须处理，把三格都用来向右盖',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作选三个连续字符，全变成 `O`',
                 '求把 `s` 全变成 `O` 的最少操作次数',
                 '示例：`XXOX` → `2`；本视频：`XXOXOXOOXX` → `3`'],
        quote='对于当前字符串中最左侧的X，必须执行一次操作。为了使得这次操作尽可能惠及到后面的位置，那么现在应该将从该位置开始的三个字符变为O。',
        quote_src='—— yiduobo 题解原文',
        idea=['最左的 X 一定要有一次操作盖住它',
              '让它做三格的最左端，能多盖住右边两格，不会更差',
              '遇到 X 就 `p += 3`，遇到 O 就 `p += 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：X 之后跳 3 位而不是 1 位；越界时 `p` 超过长度，`while` 自然结束',
                 '原文为 Python 2 风格，除 `class Solution(object)` 外无需改动，代码一字未改',
                 '对比灵神：灵神写成 `for` 里 `i += 2`，yiduobo 用 `while` 直接 `+= 3`'],
    ),
)
