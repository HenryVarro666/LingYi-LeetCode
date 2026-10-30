def _t(S):
    if 's' not in S:
        return ''
    m, k = S['modulo'], S['k']
    if S['s'] >= k:
        t = (S['s'] - k) % m
        return f"前缀和 `s = {S['s']}`：左边要找 `s[l] % {m} = ({S['s']} − {k}) % {m}` = =={t}==，已有 `{S['cnt'][t]}` 个"
    return f"前缀和 `s = {S['s']} < k = {k}`：没有 s[l] 能满足，跳过"


CONFIG = dict(
    num=2845, title='统计趣味子数组的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 计数数组 · 枚举右维护左',
    tags=['前缀和与哈希表', '难度分 2073'],
    code='''
class Solution:
    def countInterestingSubarrays(self, nums: List[int], modulo: int, k: int) -> int:
        cnt = [0] * min(len(nums) + 1, modulo)
        cnt[0] = 1  # 单独统计 s[0]=0
        ans = s = 0
        for x in nums:
            if x % modulo == k:
                s += 1
            if s >= k:
                ans += cnt[(s - k) % modulo]
            cnt[s % modulo] += 1
        return ans
''',
    call='Solution().countInterestingSubarrays([3,1,9,6], 3, 0)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（x % modulo == k 记 1）', h=190, cell=110,
             color=lambda S, i, v: 'green' if v % S['modulo'] == S['k'] else None),
        dict(type='array', var='cnt', label='cnt[r]：前缀和 % modulo = r 的个数（粉 = 要找的余数）', cell=110, h=210,
             pointers={'s % modulo': 'blue'},
             color=lambda S, i, v: 'pink' if S['s'] >= S['k'] and i == (S['s'] - S['k']) % S['modulo'] else None),
        dict(type='text', h=110, size=28, fn=_t),
    ],
    watch=[('x', 'x', 'blue'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'cnt = [0]': '`cnt` 只需 `min(n+1, modulo)` 格：`s % modulo` 不会更大 → `{cnt}`',
        'cnt[0] = 1': '空前缀 `s[0] = 0` 先算一个：`cnt[0] = 1`',
        'ans = s = 0': '`s` 是 1 的个数（前缀和），`ans` 是答案',
        'for x in nums': lambda S, B, r: (f'枚举右端点，当前元素 `x = {S.x}`' if sum(S.cnt) <= len(S.nums) else '遍历结束'),
        'if x % modulo == k': lambda S, B, r: (f'`{S.x} % {S.modulo} = {S.x % S.modulo}`，等于 k → 记 1' if S.x % S.modulo == S.k
                                               else f'`{S.x} % {S.modulo} = {S.x % S.modulo}` ≠ k = {S.k} → 记 0'),
        's += 1': '前缀和加一：`s = {s}`',
        'if s >= k': lambda S, B, r: (f'`s = {S.s} ≥ k = {S.k}`：可以向左找 s[l]' if S.s >= S.k
                                      else f'`s = {S.s} < k = {S.k}`：`s−k+modulo > s`，左边不可能有，跳过'),
        'ans += cnt': '需要左边余数为 `({s} − {k}) % {modulo} = {(s - k) % modulo}`，有 `{cnt[(s - k) % modulo]}` 个 → `ans = {ans}`',
        'cnt[s % modulo] += 1': '==先查后加==：当前前缀和余数 `{s % modulo}` 入 cnt，`cnt = {cnt}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='把满足条件的元素记 1：变成「和模 m 等于 k」的子数组计数',
        complexity='时间 `O(n)`，空间 `O(min(n, modulo))`',
        problem=['子数组里满足 `nums[i] % modulo == k` 的个数记为 `cnt`',
                 '若 `cnt % modulo == k`，该子数组就是趣味子数组，求个数',
                 '示例：`[3,1,9,6], modulo = 3, k = 0` → `2`'],
        quote='枚举右，维护左。……我们需要知道在 r 左侧有多少个 s[l] mod modulo 也等于 6，这可以在遍历 s 的过程中，用哈希表（其实只需要数组）统计。',
        quote_src='—— 灵茶山艾府题解 · 思路',
        idea=['满足条件的元素视作 1，其余 0 → 子数组 1 的个数 = 区间和',
              '`(s[r] − s[l]) % modulo = k` 移项：`s[l] % modulo = (s[r] − k) % modulo`',
              '`s ≤ n`，所以哈希表可以换成长 `min(n+1, modulo)` 的数组'],
        summary=['时间 `O(n)`，空间 `O(min(n, modulo))`',
                 '易错：`cnt[0] = 1` 代表空前缀，不能漏',
                 '`s < k` 时跳过，避免 `(s − k) % modulo` 回绕到不该用的格子',
                 '先用 `s` 查 `cnt`，再把 `s` 加进 `cnt`',
                 '写法一用 `accumulate` 先造前缀和数组，思路相同'],
    ),
)
