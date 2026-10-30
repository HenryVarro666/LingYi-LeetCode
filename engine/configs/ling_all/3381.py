NUMS = [-5, 1, 2, -3, 4]
K = 2


def _pre(S):
    return list(accumulate(S['nums'], initial=0))


def _pj(S):
    return S['j'] + 1 if 'j' in S else None


def _mins(S):
    return ['∞' if v == inf else v for v in S['min_s']]


def _cap_ans(S, B, ret):
    m = B.min_s[S.i]
    if m == inf:
        return f'`i = j % k = {S.i}`，这个余数还没出现过，`min_s[{S.i}] = ∞` → 不能组成合法子数组，`ans` 不变'
    return (f'`s - min_s[{S.i}] = {S.s} − ({m}) = {S.s - m}`：下标同余 → 长度是 `k` 的倍数；'
            f'`ans` {B.ans if B.ans != -inf else "-∞"} → =={S.ans}==')


def _cap_min(S, B, ret):
    if S.min_s[S.i] < B.min_s[S.i]:
        return f'`s = {S.s}` 比 `min_s[{S.i}] = {B.min_s[S.i] if B.min_s[S.i] != inf else "∞"}` 更小 → 更新，以后同余的位置减它收益更大'
    return f'`s = {S.s}` 不比 `min_s[{S.i}] = {S.min_s[S.i]}` 小，不更新'


def _text(S):
    if 'i' not in S:
        return '前缀和差 `s[j] − s[i]` 的长度是 `j−i`，要它是 `k` 的倍数 ⇔ `i`、`j` ==模 k 同余=='
    return f'当前前缀和 `s` = =={S["s"]}==，余数 `i = j % k` = =={S["i"]}==，同余里最小的前缀和 `min_s[{S["i"]}]`'


CONFIG = dict(
    num=3381, title='长度可被 K 整除的子数组的最大元素和', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 模 k 同余最小值',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1943'],
    code='''
class Solution:
    def maxSubarraySum(self, nums: List[int], k: int) -> int:
        min_s = [inf] * k
        min_s[-1] = s = 0
        ans = -inf
        for j, x in enumerate(nums):
            s += x
            i = j % k
            ans = max(ans, s - min_s[i])
            min_s[i] = min(min_s[i], s)
        return ans
''',
    call=f'Solution().maxSubarraySum({NUMS}, {K})',
    expect=4,
    views=[
        dict(type='text', fn=_text, size=24, h=70),
        dict(type='array', var='nums', label='nums（蓝 = 当前 j）', cell=96, h=200,
             pointers={'j': 'blue'}, color=lambda S, i, v: 'blue' if S.get('j') == i else None),
        dict(type='array', var=_pre, label='前缀和 s（辅助观察，s[0]=0 即初始值）', cell=96, h=190,
             pointers={_pj: 'pink'}, pointer_labels={_pj: 's'},
             color=lambda S, i, v: 'pink' if S.get('j') is not None and i == S['j'] + 1 else None),
        dict(type='array', var=_mins, label='min_s[r]：余数 r 的最小前缀和', cell=96, h=200,
             pointers={'i': 'yellow'}, color=lambda S, i, v: 'yellow' if S.get('i') == i else None),
    ],
    watch=[('j', 'j', 'blue'), ('s', 's', 'pink'), ('i', 'i', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'min_s = [inf]': '`min_s[r]`：下标模 `k` 余 `r` 的前缀和里的最小值，初始 `∞`（还没见过）',
        'min_s[-1] = s = 0': '前缀和下标从 `-1` 起：`s[-1] = 0`，`-1` 与 `k-1` 同余 → `min_s[{k-1}] = 0`',
        'ans = -inf': '子数组必须非空且长度是 `k` 的倍数，先设 `-∞`',
        's += x': '前缀和 `s += {x}` → =={s}==',
        'i = j % k': '余数 `i = {j} % {k} = {i}`：和它同余的前缀和相减，长度才是 `k` 的倍数',
        'ans = max': _cap_ans,
        'min_s[i] = min': _cap_min,
        'return ans': '最大和 = =={ret}==',
    },
    cards=dict(
        one_liner='前缀和相减，长度是 k 的倍数 ⇔ 下标模 k 同余',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['求 `nums` 中==长度能被 k 整除==的非空子数组的最大和',
                 '示例：`nums=[-5,1,2,-3,4]`，`k=2` → `4`（子数组 `[1,2,-3,4]`）',
                 '`k = 1` 时就是 53 题最大子数组和'],
        quote='子数组 [i,j) 的元素和为 s[j]-s[i]，长度为 j-i。问题相当于：计算最大的 s[j]-s[i]，满足 i<j 且 j-i 是 k 的倍数。枚举 j，要使 s[j]-s[i] 尽量大，s[i] 要尽量小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举右端点 `j`，只需要和它==模 k 同余==的最小前缀和，不必枚举所有 `i`',
              '用长为 `k` 的数组 `min_s` 按余数分组，维护每组最小值',
              '先用 `s - min_s[i]` 更新答案，再用 `s` 更新 `min_s[i]`，保证 `i < j`'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '前缀和下标从 -1 开始：`min_s[-1] = 0`（就是 `min_s[k-1]`）',
                 '==先更新 ans，再更新 min_s==，否则会选到空子数组',
                 '题解另给「先算前缀和数组」的写法，以及把 k 个数绑成一个数的 DP 写法 `f[i+1] = max(f[i-k+1], 0) + S`'],
    ),
)
