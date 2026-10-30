def _mask(x, m=2):
    return format(x, f'0{m}b')


def _fmt(v):
    return '∞' if v == float('inf') else str(v)


def _formula(S):
    if S.get('_line') in (21, 22, 23) and 'sub' in S and 'j' in S and S['sub']:
        j, sub, x, l = S['j'], S['sub'], S['x'], S['lcms'][S['sub']]
        c = (l - x % l) % l
        return (f"`x={x}` 改成 `lcms[{sub:02b}]={l}` 的倍数要 `{c}` 次；剩下 `{j ^ sub:02b}` 靠前面的数："
                f"`f[{j ^ sub:02b}]` = {_fmt(S['f'][j ^ sub])}")
    if S.get('_line') in (14, 15, 16, 17, 18, 19) and 'l' in S:
        return f"`lcm = {S['l']}`：候选下标 `{sorted(S['candidate_indices'])}`"
    return '`f[j]`：让 target 里集合 j 的数都有倍数，最少操作次数（二进制位 = target 下标）'


CONFIG = dict(
    num=3444, title='使数组包含目标值倍数的最少增量', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='子集状压 DP + 只留前 m 小候选',
    tags=['灵神题单·动态规划', '难度分 2337'],
    code='''
class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        lcms = [1] * (1 << m)
        for i, t in enumerate(target):
            bit = 1 << i
            for mask in range(bit):
                lcms[bit | mask] = lcm(t, lcms[mask])

        max_lcm = max(max(nums) * m, max(target))
        candidate_indices = set()
        for l in set(lcms[1:]):
            if l > max_lcm:
                continue
            lst = nsmallest(m, (((l - x % l) % l, i) for i, x in enumerate(nums)))
            for _, i in lst:
                candidate_indices.add(i)

        f = [inf] * (1 << m)
        f[0] = 0
        for i in candidate_indices:
            x = nums[i]
            for j in range((1 << m) - 1, 0, -1):
                sub = j
                while sub:
                    l = lcms[sub]
                    f[j] = min(f[j], f[j ^ sub] + (l - x % l) % l)
                    sub = (sub - 1) & j
        return f[-1]
''',
    setup='from math import lcm',
    call='Solution().minimumIncrements([7,2,9,5,3,13,1], [4,6])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（青色 = 入选候选）', h=170, cell=70,
             color=lambda S, i, v: 'cyan' if i in S.get('candidate_indices', ()) else ('yellow' if i == S.get('i') and 'x' in S else None)),
        dict(type='array', var='lcms', label='lcms[mask]：target 子集的最小公倍数（下标 = mask，位 i = target[i]）', h=170, cell=80,
             color=lambda S, i, v: 'yellow' if i == S.get('sub') and S.get('sub') else ('orange' if S.get('_line') in (7, 8, 9) and i == S.get('bit', 0) | S.get('mask', 0) else None)),
        dict(type='array', var='f', label='f[j]：满足集合 j 的最少操作次数', h=170, cell=80,
             color=lambda S, i, v: ('yellow' if i == S.get('j') else 'cyan' if i == (S.get('j', 0) ^ S.get('sub', 0)) and S.get('sub') else None)
             if 'j' in S else None),
        dict(type='text', size=28, fn=_formula, h=110),
    ],
    watch=[('x', 'x', 'pink'), ('j', "format(j, '02b')", 'yellow'), ('sub', "format(sub, '02b')", 'cyan'), ('l', 'l', 'purple')],
    captions={
        'm = len(target)': '`target` 只有 `{m}` 个数，用二进制表示它的子集，共 `{1 << m}` 种',
        'lcms = [1]': '`lcms[mask]` 用来存 target 子集的最小公倍数：要让一个数同时是它们的倍数，就得是 LCM 的倍数',
        'lcms[bit | mask] = ': '`lcms[{bit | mask:02b}] = lcm({t}, lcms[{mask:02b}])` = =={lcms[bit | mask]}==',
        'max_lcm =': '`max_lcm = {max_lcm}`：LCM 比它还大的子集，拆开改更划算，不必考虑',
        'candidate_indices = set()': '`candidate_indices` 存「值得修改」的 nums 下标：很少，远小于 n',
        'for l in set(lcms[1:])': lambda S, B, r: (f'所有 LCM 都处理完：候选下标 `{sorted(S.candidate_indices)}`，只有 `{len(S.candidate_indices)}` 个' if 'l' in B and B['l'] == S.l else f'对每个不同的 LCM `{S.l}`，找出把 nums 变成它的倍数最便宜的几个数'),
        'lst = nsmallest': 'LCM `{l}`：最便宜的前 `m = {m}` 个：`{lst}`（操作次数, 下标）。m 个目标最多占用 m 个数，所以只留前 m 小就够',
        'candidate_indices.add': '下标 `{i}`（`nums[{i}] = {nums[i]}`）入选 → `{sorted(candidate_indices)}`',
        'f = [inf]': '候选只剩 `{sorted(candidate_indices)}`。`f` 初始全是 ∞（不合法），只有空集 `f[0] = 0`',
        'f[0] = 0': '空集不需要任何倍数：`f[0] = 0`',
        'x = nums[i]': '轮到候选 `nums[{i}] = {x}`：像 0-1 背包，这个数改或不改',
        'sub = j': '`j = {j:02b}`（`j` 从大到小，`f[j ^ sub]` 还是上一个数之前的值）：枚举它的非空子集 `sub`，让 `x` 负责 `sub`',
        'l = lcms[sub]': '`x` 要改成 `lcms[{sub:02b}] = {l}` 的倍数',
        'f[j] = min': lambda S, B, r: f'`x = {S.x}` → `{S.l}` 的倍数要 `({S.l} − {S.x} % {S.l}) % {S.l} = {(S.l - S.x % S.l) % S.l}` 次，加上 `f[{S.j ^ S.sub:02b}] = {_fmt(S.f[S.j ^ S.sub])}`，取最小：`f[{S.j:02b}]` {_fmt(B.f[S.j])} → =={_fmt(S.f[S.j])}==',
        'return f[-1]': '`f[-1]` = 全集 `11`：每个目标都有了倍数，最少 =={ret}== 次',
    },
    skip=[5, 7, 6, 12, 11, 13, 16, 20, 21, 23, 24, 25, 26, 28],
    max_steps=110,
    cards=dict(
        one_liner='target 最多 4 个数，用二进制集合做状压 DP',
        complexity='时间 `O(n·2^m·log m + m·6^m)`，空间 `O(m·2^m)`',
        problem=['`nums` 每次可把一个数 `+1`，要让 `target` 每个数在 `nums` 里至少有一个倍数',
                 '求最少操作次数，`target` 长度 `m ≤ 4`',
                 '本视频：`nums=[7,2,9,5,3,13,1]`，`target=[4,6]` → `2`（7→8，5→6）'],
        quote='要修改的数一定在这 m 个 x 中。如果最小的被其他非空子集使用了，那么我们可以选次小的……由于 target 只有 m≤4 个数，所以只需要计算前 m 小的操作次数。',
        quote_src='—— 灵茶山艾府题解（时间优化）',
        idea=['先看最后一个数改或不改，改就是枚举 `j` 的子集 `sub`，变成 `lcms[sub]` 的倍数',
              '`f[j]` = 满足集合 `j` 的最少操作，倍数条件靠 LCM 合并',
              '优化：对每个 LCM 只留操作次数前 `m` 小的数当候选，DP 只跑这几个数'],
        summary=['朴素状压 `O(n·3^m)`，加候选优化后 DP 只跑 `O(m·2^m)` 个数',
                 '易错：LCM 最大约 `10^16`，Python 不会溢出，C++/Java 要用 64 位',
                 '`(l - x % l) % l` 同时处理已经是倍数的情况',
                 '`j` 从大到小枚举，就是 0-1 背包的滚动数组',
                 '题解前面还有记忆化、二维递推、一维空间优化三种写法，本视频演示最后的优化版'],
    ),
)
