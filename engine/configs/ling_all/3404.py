from fractions import Fraction

NUMS = [1, 2, 1, 2, 2, 4, 1, 2, 2]


def _fr(k, v):
    f = Fraction(k).limit_denominator(1000)
    return f'{f.numerator}/{f.denominator}: {v}'


def _region(S, i, v):
    if 'i' not in S:
        return None
    c = S['i']
    if i == c - 2:
        return 'blue'
    if i == c:
        return 'pink'
    if i < c - 3:
        return 'cyan'
    if i >= c + 2:
        return 'orange'
    return None


def _txt(S):
    if 'i' not in S:
        return '把 `a*c = b*d` 变成 `a/b = d/c`：左边的 a、b 都在 c、d 的左侧'
    i = S['i']
    nums = S['nums']
    head = f"b = `nums[{i - 2}]` = {nums[i - 2]}，c = `nums[{i}]` = {nums[i]}"
    if S.get('_line') in (16, 17) and 'd' in S:
        return head + f"；查 `d/c = {S['d']}/{nums[i]}` 的个数"
    if 'a' in S and S.get('_line') in (11, 12):
        return head + f"；放入 `a/b = {S['a']}/{nums[i - 2]}`"
    return head


CONFIG = dict(
    num=3404, title='统计特殊子序列的数目', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右、维护左 · 哈希表记 a/b',
    tags=['动态规划', '难度分 2445'],
    code='''
class Solution:
    def numberOfSubsequences(self, nums: List[int]) -> int:
        ans = 0
        cnt = defaultdict(int)
        # 枚举 b 和 c
        for i in range(4, len(nums) - 2):
            # 增量式更新，本轮循环只需枚举 b=nums[i-2] 这一个数
            # 至于更前面的 b，已经在前面的循环中添加到 cnt 中了，不能重复添加
            b = nums[i - 2]
            # 枚举 a
            for a in nums[:i - 3]:
                cnt[a / b] += 1

            c = nums[i]
            # 枚举 d
            for d in nums[i + 2:]:
                ans += cnt[d / c]
        return ans
''',
    call=f'Solution().numberOfSubsequences({NUMS})',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（青 = a 的范围，蓝 = b，粉 = c，橙 = d 的范围）', h=230, cell=84,
             color=_region, dim=lambda S, i, v: 'i' in S and S['i'] - 2 < i < S['i'] and i != S['i'] - 2),
        dict(type='map', var='cnt', label='cnt：左边每种 a/b 出现了几次', fmt=_fr, h=260, font=30),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'pink'), 'b', 'c', 'a', 'd', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans`：特殊子序列个数',
        'cnt = defaultdict': '`cnt[a/b]`：左边（间隔够远）的 `a/b` 各出现几次',
        'for i in range': lambda S, B, ret: (f'枚举 c 的下标 `i = {S.i}`（c = {S.nums[S.i]}）' if 'i' not in B or S.i != B.i else '枚举完了，结束'),
        'b = nums[i - 2]': '`b = nums[{i-2}] = {b}`：`b` 与 `c` 隔一个数，本轮新增的 b 只有它',
        'for a in nums[:i - 3]': '`a` 要和 `b` 隔一个数 → 在 `nums[:{i-3}]` 里取，一个个来；取完这一圈结束',
        'cnt[a / b] += 1': '`a / b = {a}/{b} = {a / b}`，记入 `cnt` → ==这个比值出现 {cnt[a / b]} 次==',
        'c = nums[i]': '`c = nums[{i}] = {c}`',
        'for d in nums[i + 2:]': '`d` 要和 `c` 隔一个数 → 在 `nums[{i+2}:]` 里取，一个个来；取完换下一个 `c`',
        'ans += cnt[d / c]': '`d / c = {d}/{c} = {d / c}`：左边有 `{cnt[d / c]}` 个相同的 `a/b` → `ans` = =={ans}==',
        'return ans': '一共 `{ans}` 个特殊子序列',
    },
    max_steps=90,
    cards=dict(
        one_liner='a*c = b*d 变成 a/b = d/c：枚举右边，哈希表记左边的比值',
        complexity='时间 `O(n^2)`，空间 `O(min(n^2, U^2))`',
        problem=['找下标 `p<q<r<s` 且相邻间隔至少一个数的子序列，满足 `nums[p]*nums[r] == nums[q]*nums[s]`',
                 '答案是这样的子序列个数',
                 '本视频：`[1,2,1,2,2,4,1,2,2]` → `4`'],
        quote='在枚举右边的 c 和 d 的同时，用哈希表维护左边的 a/b 的个数。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['令 a,b,c,d 为四个数，式子变形为 `a/b = d/c`，a、b 在左，c、d 在右',
              '枚举 c：把新的 b = `nums[i-2]` 和它左边所有 a 的 `a/b` 加入哈希表（增量更新，不重复加）',
              '再枚举 d，`cnt[d/c]` 就是左边与之相等的 `a/b` 的个数'],
        summary=['时间 `O(n^2)`，空间 `O(min(n^2, U^2))`',
                 '数值只到 1000，浮点除法不会误判相等；用最简分数（方法一）更保险',
                 '间隔限制：`b` 取 `i-2`，`a` 取 `nums[:i-3]`，`d` 从 `i+2` 起',
                 '方法一：前后缀分解，用 gcd 约成最简分数',
                 '相似：1512 好数对（两个数的版本）'],
    ),
)
