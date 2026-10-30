def _pre(S):
    return 'target' in S and 'i' in S


def _need(S, i, v):
    return S.get('target') is not None and ((v - i) & 1) != S['target']


def _info(S):
    if 'target' not in S:
        return f"全局最小 `g_min = {S.get('g_min', '?')}`，全局最大 `g_max = {S.get('g_max', '?')}`" if 'g_min' in S else ''
    x = S.get('x')
    t = S['target']
    s = f"目标：偶数下标放 =={'偶' if t == 0 else '奇'}== 数    已操作 `op = {S.get('op')}`"
    if 'mn' in S and x is not None:
        s += f"    当前最小 `{S['mn']}`  最大 `{S['mx']}`"
    return s


CONFIG = dict(
    num=3854, title='使数组奇偶交替的最少操作', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='枚举两种奇偶模式 + 最值分类讨论',
    tags=['贪心算法', '思维题', '难度分 2095'],
    code='''
class Solution:
    def makeParityAlternating(self, nums: List[int]) -> List[int]:
        if len(nums) == 1:
            return [0, 0]

        g_min = min(nums)
        g_max = max(nums)

        def calc(target: int) -> List[int]:
            op = 0
            mn, mx = inf, -inf
            for i, x in enumerate(nums):
                # 如果 target = 0，那么操作后，nums 每个数的奇偶性必须分别等于 0,1,0,1,... 即 target ^ (i%2)
                if (x - i) & 1 != target:  # 等价于 x&1 != target ^ (i%2)
                    op += 1
                    if x == g_min:
                        x += 1
                    elif x == g_max:
                        x -= 1
                mn = min(mn, x)
                mx = max(mx, x)
            return [op, max(mx - mn, 1)]  # 在 n >= 2 的情况下，极差至少是 1

        return min(calc(0), calc(1))
''',
    call='Solution().makeParityAlternating([-2,-3,1,4,6])',
    expect=[2, 9],
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=260, label='nums（红框 = 奇偶性不符，需要操作一次）',
             color=lambda S, i, v: ('red' if _need(S, i, v) else None) if 'target' in S else None,
             dim=lambda S, i, v: 'i' in S and 'target' in S and i < S['i']),
        dict(type='text', fn=lambda S: (f"这一格 `x = {S['x']}`" + ('，奇偶不符：' + ('等于最小值 → ==+1==' if S['x'] == S.get('g_min') else '等于最大值 → ==−1==' if S['x'] == S.get('g_max') else '夹在中间 → 改成 ±1 都不影响极差') if _need(S, S['i'], S['x']) and S['_line'] >= 14 else '')) if 'x' in S and 'i' in S and 'target' in S else '', size=24),
    ],
    watch=['g_min', 'g_max', 'target', 'op', 'mn', 'mx', 'x'],
    captions={
        'if len(nums) == 1': '只有一个数本来就奇偶交替，直接返回 `[0, 0]`；`n = {len(nums)}`',
        'g_min = min': '`g_min = {g_min}`：全局最小值',
        'g_max = max': '`g_max = {g_max}`：全局最大值',
        'op = 0': '枚举目标 `target = {target}`：偶数下标放{"偶" if target == 0 else "奇"}数；`op` 记操作次数',
        'mn, mx = inf': '`mn, mx` 记操作后的最小、最大值',
        'if (x - i) & 1 != target': lambda S, B, r: (f"`x = {S.x}, i = {S.i}`：`(x-i)&1 = {(S.x - S.i) & 1}` " + ('≠' if (S.x - S.i) & 1 != S.target else '=') + f" `target = {S.target}` → " + ('==奇偶不符，必须操作一次==（只会 ±1，每个数至多操作一次）' if (S.x - S.i) & 1 != S.target else '奇偶已符合，不用动')),
        'op += 1': '操作次数 `op = {op}`',
        'if x == g_min': lambda S, B, r: (f"`x = {S.x}` {'==' if S.x == S.g_min else '≠'} `g_min = {S.g_min}`" + (' → ==最小值只能往上加 1==，不会拉低最小值' if S.x == S.g_min else ' → 看是不是最大值')),
        'x += 1': '最小值 `+1` → `x = {x}`，最小值被抬高',
        'elif x == g_max': lambda S, B, r: (f"`x = {S.x}` {'==' if S.x == S.g_max else '≠'} `g_max = {S.g_max}`" + (' → ==最大值只能往下减 1==' if S.x == S.g_max else ' → 夹在中间，改成 ±1 都能落在新的最值之间，极差不变，不用改')),
        'x -= 1': '最大值 `-1` → `x = {x}`，最大值被压低',
        'mn = min': '`mn = min({B.mn}, {x}) = {mn}`',
        'mx = max': '`mx = max({B.mx}, {x}) = {mx}`',
        'return [op, max': '`target = {target}`：操作 `{op}` 次，极差 `max({mx} - {mn}, 1) = {max(mx - mn, 1)}`（`n ≥ 2` 极差至少 1）',
        'return min(calc(0), calc(1))': lambda S, B, ret: ('两种模式各算一遍 `[操作数, 极差]`，再取较小的：先比操作数，再比极差' if ret is None else f'两种模式取较小 → `{ret}`'),
    },
    cards=dict(
        one_liner='枚举两种奇偶模式；改动时最小值 +1、最大值 −1，极差最小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 每次可把某个数 `+1` 或 `-1`，要变成相邻奇偶性都不同的数组',
                 '返回 `[最少操作数, 恰好这么多次操作后 max-min 的最小值]`',
                 '示例：`[-2,-3,1,4]` → `[2,6]`'],
        quote='对于要修改的数，如果其等于 gMin，那么加一；否则如果其等于 gMax，那么减一；其他情况不修改。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只有两种目标：偶奇偶奇… 或 奇偶奇偶…，分别枚举',
              '不符的数操作一次奇偶性就变，所以每个数==至多操作一次==',
              '改最小值 ==+1==、改最大值 ==−1==，其余数改成什么都不影响极差'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`n = 1` 要单独返回 `[0, 0]`；`n ≥ 2` 极差至少是 1，所以 `max(mx - mn, 1)`',
                 '`g_min == g_max` 时统一 `+1`（`if` 先命中），极差为 1，不会变成 2',
                 '灵神还提到通用做法：每个数看成列表 `[x]` 或 `[x-1, x+1]`，转化成第 632 题最小区间'],
    ),
)
