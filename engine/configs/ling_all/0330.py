CONFIG = dict(
    num=330, title='按要求补齐数组', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='归纳法 · 区间 [0,s-1] 倍增', tags=['灵神题单', '难度分 2952'],
    code='''
class Solution:
    def minPatches(self, nums: List[int], n: int) -> int:
        ans, s, i = 0, 1, 0
        while s <= n:
            if i < len(nums) and nums[i] <= s:
                s += nums[i]
                i += 1
            else:
                s *= 2  # 必须添加 s
                ans += 1
        return ans
''',
    call='Solution().minPatches([1,5,10], 20)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: f"已能凑出 ==[0, {S['s']-1}]== 的所有整数；目标 [1, {S['n']}]" if 's' in S else '', size=34),
        dict(type='array', var='nums', pointers={'i': 'blue'}, label='nums（已排序）', h=200,
             color=lambda S, i, v: ('green' if 'i' in S and i < S['i'] else None)),
        dict(type='text', fn=lambda S: f"已补充 {S['ans']} 个数" if 'ans' in S else '', size=30),
    ],
    watch=[('s', 's', 'cyan'), ('i', 'i', 'blue'), ('ans', 'ans', 'green'), 'n'],
    captions={
        'ans, s, i = 0, 1, 0': '`s = 1`：把 0 也算可得，当前能凑出 `[0, s-1] = [0, 0]`；`ans` 记补了几个数',
        'while s <= n': lambda S, B, r: (f'`s = {S.s} <= n = {S.n}`：[1, n] 还没凑满，继续' if S.s <= S.n
                                         else f'`s = {S.s} > n = {S.n}`：[0, {S.s-1}] 已覆盖 [1, n]，退出'),
        'if i < len(nums)': lambda S, B, r: (f'`nums[{S.i}] = {S.nums[S.i]} <= s = {S.s}`：能和 [0, s-1] 接上 → 成立' if S.i < len(S.nums) and S.nums[S.i] <= S.s
                                              else (f'`nums[{S.i}] = {S.nums[S.i]} > s = {S.s}`：中间缺一个 `s`，必须补' if S.i < len(S.nums)
                                                    else '`nums` 用完了，只能靠补数继续扩')),
        's += nums[i]': '区间平移 `[x, s+x-1]` 与 `[0, s-1]` 合并 → 能凑出 `[0, {s-1}]`',
        'i += 1': '`i` → {i}',
        's *= 2': '必须添加 `{B.s}`（再小凑不到更大，不够贪）→ 区间翻倍到 `[0, {s-1}]`',
        'ans += 1': '补了一个数，`ans` = {ans}',
        'return ans': '`s = {s} > n`，一共补了 `{ans}` 个数',
    },
    cards=dict(
        one_liner='区间 [0,s-1] 凑满了，要么并入 nums[i]，要么补 s 翻倍',
        complexity='时间 `O(m + log n)`，空间 `O(1)`',
        problem=['已排序正整数数组 `nums` 和正整数 `n`，往里补数使 `[1, n]` 内每个数都能由若干数之和表示',
                 '求最少补几个数',
                 '示例：`nums=[1,5,10], n=20` → `2`（补 2 和 4）'],
        quote='假设现在得到了区间 [0,s-1] 中的所有整数，如果此时遍历到整数 x=nums[i]，那么把 [0,s-1] 中的每个整数都增加 x，我们就得到了区间 [x,s+x-1] 中的所有整数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 0 也算可得，维护 `[0, s-1]` 全部可得',
              '`x <= s`：两个区间能拼上，`s += x`',
              '`x > s`：凑不出 `s`，必须补 `s`，区间翻倍成 `[0, 2s-1]`',
              '`s > n` 就停'],
        summary=['时间 `O(m + log n)`：`s` 至多翻倍 `log n` 次',
                 '补的数一定是当前的 `s`：补更小的数，扩得不够多',
                 '易错：`s` 初值是 1（表示 [0,0] 已有），条件是 `s <= n` 不是 `<`',
                 '同类题：1798 你能构造出连续值的最大数目'],
    ),
)
