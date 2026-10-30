def _cur(S):
    d = S['_inner']
    return d.get('j'), d.get('r')


def _color(S, rr, cc, v):
    j, r = _cur(S)
    if j is None or r is None or S.get('_line') != 12:
        return None
    if (rr, cc) == (j, r):
        return 'yellow'
    if (rr, cc) == (j - 1, (r - S['x']) % 3):
        return 'blue'
    return None


def _txt(S):
    d = S['_inner']
    j, r, x = d.get('j'), d.get('r'), S.get('x')
    if j is None or r is None or x is None or S.get('_line') != 12:
        return '`f[j][r]`：恰好选 `j` 个数、和模 3 为 `r` 时的最大和（`-inf` 表示不可能）'
    src = (r - x) % 3
    return f'`f[{j}][{r}] = max(f[{j}][{r}], f[{j - 1}][{src}] + {x})`，`({r} − {x}) % 3 = {src}`'


CONFIG = dict(
    num=3780, title='能被 3 整除的三元组最大和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='恰好装满型二维 0-1 背包（查表法）',
    tags=['灵神题单·动态规划'],
    code='''
max = lambda a, b: b if b > a else a

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        K = 3
        MOD = 3
        f = [[-inf] * MOD for _ in range(K + 1)]
        f[0][0] = 0
        for x in nums:
            for j in range(K, 0, -1):
                for r in range(MOD):
                    f[j][r] = max(f[j][r], f[j - 1][(r - x) % MOD] + x)
        return max(f[K][0], 0)
''',
    call='Solution().maximumSum([4, 2, 3])',
    expect=9,
    skip=['for r in range', 'for j in range'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前物品 x）', cell=80, h=150,
             color=lambda S, i, v: 'blue' if v == S.get('x') else None),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='table', var='f', label='f[j][r]（行 = 选了 j 个，列 = 和模 3 余 r；黄 = 正在更新，蓝 = 来源）', h=330, cell=96,
             rows=lambda S: [f'j={k}' for k in range(4)], cols=lambda S: [f'r={k}' for k in range(3)],
             color=_color, fmt=lambda v: '-∞' if v == -inf else str(v)),
    ],
    watch=[('x', "S.get('x')", 'blue'), ('j', "_inner.get('j')", 'pink'), ('r', "_inner.get('r')", 'yellow'), ('f[3][0]', 'f[3][0]', 'green')],
    captions={
        'K = 3': '要选恰好 `K = 3` 个数',
        'MOD = 3': '和要被 3 整除，只关心和模 `MOD = 3` 的余数',
        'f = [[-inf]': '`f[j][r]`：选了恰好 `j` 个数、和模 3 为 `r` 时的最大和；初始全是 ==-inf==（不可能）',
        'f[0][0] = 0': '一个数都没选：只有 `j = 0, r = 0` 合法，和为 0',
        'for x in nums': lambda S, B, r: (f'考虑物品 `x = {S.x}`：选或不选；下面 `j` ==倒序==枚举，`f[j-1]` 还是没选 x 的旧值，每个数只用一次' if S.get('x') != B.get('x') else '所有数都考虑完了'),
        'f[j][r] = max': lambda S, B, ret: (f'不选 `x`：保持 `f[{S.j}][{S.r}] = {B.f[S.j][S.r]}`；选 `x = {S.x}`：来自 `f[{S.j - 1}][{(S.r - S.x) % 3}] + {S.x}`'
                                            f' = {B.f[S.j - 1][(S.r - S.x) % 3]} + {S.x}'
                                            f'，取大 → =={S.f[S.j][S.r]}=='),
        'return max(f[K][0], 0)': '选 3 个数、和模 3 余 0 的最大和 `f[3][0]` = =={f[3][0]}==；若为负（无解）则返回 0',
    },
    cards=dict(
        one_liner='把每个数看成体积 (1, x) 的物品：恰好装 3 个、和模 3 为 0',
        complexity='时间 `O(nKM)`，空间 `O(KM)`',
        problem=['给你整数数组 `nums`，从中选==恰好三个==数，使它们的和能被 3 整除',
                 '返回这类三元组的最大和；没有就返回 `0`',
                 '示例：`[4,2,3,1]` → `9`（`4 + 2 + 3`）；本视频：`[4,2,3]`'],
        quote='把每个 x = nums[i] 看成一个体积为 (1, x)，价值为 x 的物品。……所以本题是一个「恰好装满型」二维 0-1 背包。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `f[j][r]`：选了恰好 `j` 个数、和模 3 为 `r` 的最大和',
              '转移：不选 `x` 是 `f[j][r]`，选 `x` 是 `f[j-1][(r-x) % 3] + x`，取最大',
              '第一维（前 i 个数）优化掉，`j` 要倒序；答案 `f[3][0]`，小于 0 就返回 0'],
        summary=['时间 `O(nKM)`，`K = M = 3`；空间 `O(KM)`',
                 '易错：初始值要用 `-inf` 表示不可能，只有 `f[0][0] = 0`；`(r - x) % MOD` 的减法取模',
                 '灵神还给了刷表法：用 `f[j][r]` 去更新 `f[j+1][(r+x) % 3]`，本质一样',
                 '类似题：474. 一和零、1262. 可被三整除的最大和'],
    ),
)
