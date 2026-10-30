NUMS = [1, 2, 5, 4]


def _txt(S):
    if 'bit' not in S or 's' not in S or 'f' not in S or 'w' not in S or S.get('_line', 0) < 13:
        return '`f[S]`：集合 S 的所有子集（对应的二进制数）中的最大值。先逐个枚举比特 `i`，再枚举 `s`'
    s, bit, w = S['s'], S['bit'], S['w']
    i = bit.bit_length() - 1
    if not s & bit:
        return f'比特 `i={i}`：`s={s:0{w}b}` 的第 {i} 位是 0，跳过'
    return f'比特 `i={i}`：`s={s:0{w}b}` 含第 {i} 位 → 看去掉它的 `s^bit={s ^ bit:0{w}b}`，`f` 取两者较大'


def _col(S, i, v):
    s, bit = S.get('s'), S.get('bit')
    if s is None or bit is None or S.get('_line', 0) < 13:
        return None
    if i == s:
        return 'blue'
    if i == s ^ bit:
        return 'pink'
    return None


CONFIG = dict(
    num=3670, title='没有公共位的整数最大乘积', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='SOS DP（高维前缀和 · 子集最大值）',
    tags=['灵神题单·动态规划', '难度分 2234'],
    code='''
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        w = max(nums).bit_length()
        u = 1 << w
        f = [0] * u
        for x in nums:
            f[x] = x

        for i in range(w):
            bit = 1 << i  # 避免在循环中反复计算 1 << i
            s = 0
            while s < u:
                s |= bit  # 快速跳到第 i 位是 1 的 s
                v = f[s ^ bit]
                if v > f[s]:
                    f[s] = v
                s += 1

        return max(x * f[(u - 1) ^ x] for x in nums)
''',
    call=f'Solution().maxProduct({NUMS})',
    expect=10,
    skip=['while s < u', 's += 1', 'for x in nums:', 'u = 1 << w'],
    max_steps=60,
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=90),
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var='f', label='f[S]：S 的所有子集中最大的数（下标 = 二进制集合，蓝 = s，粉 = s^bit）', h=300, cell=80,
             color=_col, pointers={'s': 'blue'}),
    ],
    watch=[('i', 'i', 'cyan'), ('bit', 'bit', 'orange'), ('s', 's', 'blue'), ('v', 'v', 'pink')],
    captions={
        'w = max': '最大数 `{max(nums)}` 的二进制长 `w = {w}` 位，全集 `U` 有 `w` 个元素',
        'f = [0] * u': '`f` 有 `2^w = {u}` 项：每个下标是一个集合',
        'f[x] = x': '初始值：`f[{x}] = {x}`，集合 `{x:b}` 自己就是 nums 里的数',
        'bit = 1 << i': lambda S, B, r: f'处理第 `{S.i}` 位（`bit = {S.bit}`）：让每个含这一位的 `s` 吸收「去掉这一位」的子集',
        's = 0': '`s` 从 0 开始',
        's |= bit': lambda S, B, r: f'`s |= bit` → `{S.s}`（二进制 `{S.s:0{S.w}b}`）：直接跳到第 `{S.i}` 位是 1 的集合',
        'v = f[s ^ bit]': lambda S, B, r: f'去掉第 `{S.i}` 位：`s ^ bit = {S.s ^ S.bit}`，`v = f[{S.s ^ S.bit}]` = =={S.v}==',
        'if v > f[s]': lambda S, B, r: (f'`v = {S.v} > f[{S.s}] = {S.f[S.s]}`：子集里有更大的数 → ==更新=='
                                        if S.v > S.f[S.s] else f'`v = {S.v} <= f[{S.s}] = {S.f[S.s]}`：不更新'),
        'f[s] = v': '`f[{s}] = {v}`：集合 `{s:0{w}b}` 的子集最大值 = =={v}==',
        'return max': lambda S, B, r: ('枚举每个 `x`，在 `x` 的补集里找最大的数 `f[(u-1)^x]`，乘积取最大：'
                                       + '、'.join(f'`{x}×f[{(S.u - 1) ^ x}]={x * S.f[(S.u - 1) ^ x]}`' for x in S.nums) + f' → =={r}=='),
    },
    cards=dict(
        one_liner='和 x 无公共位 = 在 x 的补集里选子集，用 SOS DP 求子集最大值',
        complexity='时间 `O(n + U log U)`，空间 `O(U)`',
        problem=['给整数数组 `nums`，找两个不同下标，二进制==没有公共置位==，使乘积最大',
                 '没有这样的数对返回 `0`',
                 '示例：`[1,2,3,4,5,6,7]` → `12`；本视频：`[1,2,5,4]` → `10`'],
        quote='两个数的按位与等于 0，等价于两个集合 A 和 B 的交集为空，这又等价于 B 是 A 关于全集 U 的补集的子集。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把每个数看成集合：`nums[j]` 必须是 `~nums[i]` 的==子集==',
              '定义 `f[S]` = S 的所有子集中最大的数；初始 `f[x] = x`',
              '先枚举比特 `i`，再枚举 `s`：`f[s] = max(f[s], f[s ^ bit])`，这样子集不会重复',
              '答案 = `max(x * f[全集 ^ x])`'],
        summary=['时间 `O(n + U log U)`，`U` 是最大值；空间 `O(U)`',
                 '==外层枚举比特、内层枚举 s==，顺序反了就变成方法一（普通状压 DP）；求最大值两种都对，求和只有这种才对',
                 '`s |= bit` 直接跳到含该位的 `s`，省掉一半无效枚举',
                 '灵神另给：写法一（`if s & bit`）、方法一（先枚举 s 再枚举 i）、`n²` 暴力与 DP 二选一的平衡写法'],
    ),
)
