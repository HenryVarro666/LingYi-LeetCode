CONFIG = dict(
    num=1911, title='最大交替子序列和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP · 滚动数组（Go 原文转写）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1786'],
    code='''
class Solution:
    def maxAlternatingSum(self, nums: List[int]) -> int:
        f = [0, -inf]  # 原文 MinInt/2 防溢出，Python 用 -inf
        for v in nums:
            f = [max(f[0], f[1] - v), max(f[1], f[0] + v)]
        return f[1]
''',
    call='Solution().maxAlternatingSum([6, 2, 1, 4, 5, 3])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在决定选不选的数）', h=190, cell=80,
             color=lambda S, i, x: 'blue' if 'v' in S and x == S['v'] else None),
        dict(type='array', var='f', label='f = [偶数长度的最大交替和, 奇数长度的最大交替和]', h=190, cell=150, index=False),
        dict(type='text', h=70, size=26,
             fn=lambda S: (f"选 `{S['v']}`：偶数长 `max({S['f'][0]}, 奇数长 − v)`；奇数长 `max({S['f'][1]}, 偶数长 + v)`" if 'v' in S else '`f[0]` 偶数长，`f[1]` 奇数长；奇数长的最后一个数取正号')),
    ],
    watch=[('v', 'v', 'blue'), ('f[0] 偶数长', 'f[0]', 'cyan'), ('f[1] 奇数长', 'f[1]', 'green')],
    captions={
        'f = [0, -inf]': '`f[0] = 0`：空序列，和为 0；`f[1] = -inf`：奇数长的序列还不存在',
        'for v in nums': lambda S, B, r: (f'依次考虑每个数 `v = {S.v}`：选，或者不选' if S._line == 4 and S.f != B.get('f') or B.get('v') != S.v else '数都考虑完了'),
        'f = [max(': '`f[0] = max({B.f[0]}, {B.f[1]} − {v}) = {f[0]}`（不选 / 作为偶数位被减）；`f[1] = max({B.f[1]}, {B.f[0]} + {v}) = {f[1]}`（不选 / 作为奇数位被加）',
        'return f[1]': '数全为正，长为偶数的序列最后一个数要减掉，不如不要 → 答案取 `f[1]` = =={ret}==',
    },
    cards=dict(
        one_liner='选或不选：偶数长、奇数长两个状态滚动转移',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['交替和 = 偶数下标之和 − 奇数下标之和，如 `[4,2,5,3]` → `(4+5)−(2+3)=4`',
                 '求 `nums` 任意子序列的==最大交替和==',
                 '示例：`[4,2,5,3]` → `7`（子序列 `[4,2,5]`）'],
        quote='定义 f[i][0] 表示前 i 个数中长为偶数的子序列的最大交替和，f[i][1] 表示前 i 个数中长为奇数的子序列的最大交替和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['对第 `i` 个数有选或不选两种决策，所以每个状态从两处转移取最大',
              '选它：偶数长时它排在奇数位要减 `v`，奇数长时排在偶数位要加 `v`',
              '代码用滚动数组，只留 `f[i]` 这一层，`f = [偶, 奇]`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`math.MinInt / 2` 在 Python 里不会溢出，直接用 `-inf`）',
                 '时间 `O(n)`，空间 `O(1)`',
                 '元素全为正，`f[n][1] > f[n][0]` 必然成立，直接返回 `f[1]`',
                 '易错：初值是 `f[0]=0` 与 `f[1]=-inf`，不是都 0；两个新值要同时用旧值算（所以用列表一起赋值）'],
    ),
)
