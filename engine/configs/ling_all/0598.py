CONFIG = dict(
    num=598, title='区间加法 II', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='求矩形交集',
    tags=['灵神题单', '难度分 1400'],
    code='''
class Solution:
    def maxCount(self, m: int, n: int, ops: List[List[int]]) -> int:
        min_a = min((op[0] for op in ops), default=m)
        min_b = min((op[1] for op in ops), default=n)
        return min_a * min_b
''',
    call='Solution().maxCount(3, 4, [[2,3],[3,2],[3,4]])',
    expect=4,
    setup='',
    views=[
        dict(type='grid', h=330, var=lambda S: [[sum(1 for a, b in S['ops'] if x < a and y < b) for y in range(S['n'])] for x in range(S['m'])],
             color=lambda S, i, j, v: 'green' if v == len(S['ops']) else None, label='矩阵 M 最终的值（绿 = 被所有操作覆盖）'),
        dict(type='text', fn=lambda S: ('交集：左上角 (0,0)，大小 `' + (f"{S['min_a']} × {S['min_b']}" if 'min_b' in S else (f"{S['min_a']} × ?" if 'min_a' in S else '? × ?')) + '`')),
    ],
    watch=['m', 'n', 'min_a', 'min_b'],
    captions={
        'min_a = ': '所有 `ops[i][0]` 的最小值 = =={min_a}==：交集的行数（空 ops 时取 m）',
        'min_b = ': '所有 `ops[i][1]` 的最小值 = =={min_b}==：交集的列数（空 ops 时取 n）',
        'return': '交集是左上角在 (0,0) 的 `{min_a} × {min_b}` 矩形，里面的数被加得最多 → =={ret}==',
    },
    cards=dict(
        one_liner='每次加一的矩形都从左上角出发，交集就是最大值区域',
        complexity='时间 `O(k)`，空间 `O(1)`，k 为 ops 长度',
        problem=['`m × n` 矩阵初始全 0，`ops[i] = [a, b]` 表示左上 `a × b` 区域每个数加 1',
                 '执行完所有操作，求矩阵里最大整数的个数',
                 '示例：`m=3, n=3, ops=[[2,2],[3,3]]` → `4`'],
        quote='这些子矩形的交集中的数，被加一的次数最多，是最终矩阵中的最大整数。由于子矩形的左上角都是 (0,0)，所以交集矩形的左上角也是 (0,0)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['被所有操作都覆盖的格子加一次数最多',
              '左上角都是 (0,0) → 交集大小 = 最小 a × 最小 b',
              'ops 为空时交集就是整个矩阵，用 `default=m / n` 处理'],
        summary=['时间 `O(k)`，空间 `O(1)`',
                 '易错：ops 为空，答案是 `m * n`，靠 `min(..., default=)` 解决',
                 '不要真的构造矩阵，m、n 可达 4×10^4'],
    ),
)
