def _ix(S):
    return S['nums'].index(S['x']) if 'x' in S and 'nums' in S else None


CONFIG = dict(
    num=2488, title='统计中位数为 K 的子数组', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 哈希表（±1 转化）',
    tags=['灵神题单·常用数据结构', '难度分 1999'],
    code='''
class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)  # k 左边的前缀和的出现次数
        cnt[0] = 1
        ans = s = 0
        found_k = False
        for x in nums:
            if x == k:
                found_k = True
            elif x < k:
                s -= 1
            else:
                s += 1
            if not found_k:
                cnt[s] += 1  # 统计 k 左边的前缀和的出现次数
            else:
                ans += cnt[s] + cnt[s - 1]
        return ans
''',
    call='Solution().countSubarrays([3,2,1,4,5], 4)',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（绿 = k，粉 = 小于 k 记 −1，青 = 大于 k 记 +1）', h=200,
             pointers={_ix: 'blue'}, pointer_labels={_ix: 'x'},
             color=lambda S, i, v: 'green' if v == S['k'] else ('pink' if v < S['k'] else 'cyan')),
        dict(type='map', var='cnt', label='cnt：k 左边的前缀和 → 出现次数', fmt=lambda kk, v: f'{kk}: {v}', h=210, font=32),
        dict(type='text', h=90, size=30,
             fn=lambda S: ('`s` = 大于 k 的个数 − 小于 k 的个数（前缀和）' if 'found_k' not in S else
                           (f"已经过了 k：查 `cnt[{S['s']}] + cnt[{S['s']-1}]` = {S['cnt'].get(S['s'], 0)} + {S['cnt'].get(S['s']-1, 0)}"
                            if S['found_k'] else f"还没遇到 k：把前缀和 `s = {S['s']}` 记入哈希表"))),
    ],
    watch=['x', ('s', 's', 'blue'), ('found_k', 'found_k', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'cnt[0] = 1': '空前缀的和是 0，出现 1 次',
        'found_k = True': '遇到 `k = {k}`：它记为 0，从这里开始右边的前缀和才是“包含 k”的子数组',
        's -= 1': '`{x}` 比 `k = {k}` 小，记为 −1 → `s = {s}`',
        's += 1': '`{x}` 比 `k = {k}` 大，记为 +1 → `s = {s}`',
        'cnt[s] += 1': 'k 还没出现：只统计左边的前缀和，`cnt[{s}]` = {cnt[s]}',
        'ans += ': '当前前缀和 `s = {s}`：差 0 的有 `cnt[{s}] = {cnt[s]}` 个（奇数长度），差 1 的有 `cnt[{s-1}] = {cnt[s-1]}` 个（偶数长度）→ `ans = {ans}`',
        'return ans': '共 =={ans}== 个中位数为 `{k}` 的子数组',
    },
    cards=dict(
        one_liner='大于 k 记 +1，小于 k 记 −1，再数前缀和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 是 1 到 n 的排列，求中位数恰好为 `k` 的子数组个数',
                 '偶数长度取中间偏左的那个数',
                 '示例：`[3,2,1,4,5]`，`k=4` → 3（`[4]`、`[4,5]`、`[1,4,5]`）'],
        quote='如果子数组中「大于 k 的元素个数」等于「小于 k 的元素个数」，或者多一个，那么 k 就是中位数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['大于 k 记 1，小于 k 记 −1，k 记 0；问题变成：含 0 且和为 0 或 1 的子数组个数',
              '用 560 的前缀和 + 哈希表：先统计 k 左边的前缀和次数',
              '到了 k 及右边，用 `cnt[s]`（和为 0）+ `cnt[s−1]`（和为 1）累加答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`cnt[0] = 1` 表示空前缀，否则漏掉从头开始的子数组',
                 '易错点：k 本身的位置要入哈希表还是查询——遇到 k 后就只查不存',
                 '另一种写法：用数组代替哈希表，`s` 初始化为 n 避免负下标',
                 '前置题：560 和为 K 的子数组'],
    ),
)
