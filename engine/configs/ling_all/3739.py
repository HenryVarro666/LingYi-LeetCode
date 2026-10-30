def _t(S):
    if 's' not in S or 'n' not in S:
        return ''
    return f"前缀和 `s = {S['s'] - S['n']}`（数组下标 `{S['s']}` = s + n）；`f` = 左边比 s 小的前缀个数 = =={S['f']}=="


CONFIG = dict(
    num=3739, title='统计主要元素子数组数目 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='±1 前缀和 · 增量维护 f，O(n)',
    tags=['前缀和与哈希表', '难度分 2090'],
    code='''
class Solution:
    def countMajoritySubarrays(self, nums: List[int], target: int) -> int:
        s = n = len(nums)
        cnt = [0] * (n * 2 + 1)
        cnt[s] = 1
        ans = f = 0
        for x in nums:
            if x == target:
                f += cnt[s]
                s += 1
            else:
                s -= 1
                f -= cnt[s]
            ans += f
            cnt[s] += 1
        return ans
''',
    call='Solution().countMajoritySubarrays([1,2,2,3,2], 2)',
    expect=9,
    views=[
        dict(type='array', var='nums', label='nums（绿 = target，记 +1；其余 −1）', h=170, cell=100,
             color=lambda S, i, v: 'green' if v == S['target'] else None),
        dict(type='array', var='cnt', label='cnt[下标]：该前缀和出现次数（下标 = s + n）', h=230, cell=84, pointers={'s': 'blue'}),
        dict(type='text', h=110, size=28, fn=_t),
    ],
    watch=[('x', 'x', 'blue'), ('s', 's', 'cyan'), ('f', 'f', 'orange'), ('ans', 'ans', 'green')],
    captions={
        's = n = len': '`s` 初始为 `n = {n}`：偏移 n，避免负下标（真实前缀和 = s − n = 0）',
        'cnt = [0]': '`cnt` 长 `2n+1 = {len(cnt)}`，前缀和范围 `[−n, n]`',
        'cnt[s] = 1': '空前缀（和 0）出现 1 次',
        'ans = f = 0': '`f`：左边比当前前缀和小的个数；`ans` 是 f 的总和',
        'for x in nums': lambda S, B, r: (f'枚举 `x = {S.x}`' if sum(S.cnt) <= len(S.nums) else '遍历结束'),
        'if x == target': lambda S, B, r: (f'`{S.x} == {S.target}`：这个数记 +1，前缀和变大' if S.x == S.target
                                           else f'`{S.x} ≠ {S.target}`：这个数记 −1，前缀和变小'),
        'f += cnt[s]': '`s` 要变大 1：新增的“比我小”的，正是等于旧 s 的那 `{cnt[B.s]}` 个 → `f = {f}`',
        'f -= cnt[s]': '`s` 变小 1 后，原来比我小的里等于新 s 的 `{cnt[s]}` 个不再“小于”了 → `f = {f}`',
        's += 1': '前缀和 +1：`s = {s}`',
        's -= 1': '前缀和 −1：`s = {s}`',
        'ans += f': '以当前位置为右端点，主要元素子数组有 `f = {f}` 个 → `ans = {ans}`',
        'cnt[s] += 1': '把当前前缀和计入：`cnt[{s}] = {cnt[s]}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='target 记 +1、其余 −1：前缀和只会 ±1，f 随之增减',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['主要元素：在子数组中出现次数 ==严格大于== 长度的一半',
                 '求以 `target` 为主要元素的子数组个数',
                 '示例：`[1,2,2,3,2], target = 2`'],
        quote='把 nums 中的 target 视作 1，其余元素视作 −1……问题变成：计算 a 中元素和严格大于 0 的子数组个数。',
        quote_src='—— 灵茶山艾府题解 · 转化',
        idea=['和 > 0 ⇔ `s[j] − s[i] > 0`，即统计左边有多少个前缀和 < `s[j]`',
              '方法一用有序集合 `O(n log n)`；这里利用 ==s 每次只变 1==',
              '`s` 加 1：`f` 加上 `cnt[旧 s]`；`s` 减 1：`f` 减去 `cnt[新 s]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`s` 初始成 `n`（偏移），数组才不会越界',
                 '`f += cnt[s]` 在 s 变化之前，`f -= cnt[s]` 在变化之后',
                 '`cnt[s] += 1` 放在 `ans += f` 之后，保证 i < j',
                 '方法一：`SortedList` + `bisect_left`；优化前用 `defaultdict`，思路相同'],
    ),
)
