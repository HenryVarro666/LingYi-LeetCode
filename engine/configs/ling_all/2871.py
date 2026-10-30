def _seg(S):
    if 'a' not in S:
        return ''
    a = S['a']
    return f"当前段的 AND：`a = {'全 1（空）' if a == -1 else a}`　已分割 `ans = {S['ans']}` 段"


CONFIG = dict(
    num=2871, title='将数组分割成最多数目的子数组', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='AND 性质 · 贪心立刻分割',
    tags=['灵神题单·位运算', '难度分 1750'],
    code='''
class Solution:
    def maxSubarrays(self, nums: List[int]) -> int:
        ans = 0
        a = -1  # -1 就是 111...1，和任何数 AND 都等于那个数
        for x in nums:
            a &= x
            if a == 0:
                ans += 1  # 分割
                a = -1
        return max(ans, 1)  # 如果 ans=0 说明所有数的 and>0，答案为 1
''',
    call='Solution().maxSubarrays([3,1,2,4,0,6,5,0,3])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（绿色 = 已经分割出去的数）'),
        dict(type='text', fn=_seg, size=38),
    ],
    watch=[('x', 'x', 'blue'), ('a', 'a', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计分割出的、AND 等于 0 的子数组个数',
        'a = -1': '`a` 是当前段的 AND。==-1 是全 1==，和任何数 AND 都等于那个数，当作「空段」',
        'for x in nums': '取下一个数 `x = {x}`',
        'a &= x': '当前段 AND 上 `x = {x}`：`a` → {a}（AND 的数越多结果越小）',
        'if a == 0': lambda S, B, r: ('`a = 0`：这一段 AND 已经是 0，==立刻分割==，别多吃后面的数' if S.a == 0 else f'`a = {S.a}` 还大于 0，继续往这一段里加数'),
        'ans += 1': '分割出一段 AND 为 0 的子数组：`ans` → {ans}',
        'a = -1': lambda S, B, r: ('`a` 重置为 -1，下一段重新开始。' if S['_line'] != 4 else '`a` 是当前段的 AND。==-1 是全 1==，和任何数 AND 都等于那个数，当作「空段」'),
        'return max(ans, 1)': '`ans = {ans}`：末尾剩下的 AND 大于 0 的数并到最后一段；若 `ans = 0` 则整个数组只能一段 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='整体 AND 为 0 才能多分：每当 AND 变 0 就立刻切一刀',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组分成若干连续子数组，每段的分数是该段所有数的 AND',
                 '先让分数之和最小，再让子数组个数最多，求最多几段',
                 '示例：`[1,0,2,0,1,2]` → `3`'],
        quote='如果 nums 数组的 AND 是大于 0 的，那么只能分割出一个数组……如果等于 0，那么可以分割出尽量多的 AND 等于 0 的子数组。怎么分？从左到右遍历数组，==只要发现 AND 等于 0 就立刻分割==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子数组 AND 不会低于整个数组的 AND，设整体 AND 为 `a`',
              '`a > 0`：多分一段总分至少 `2a`，更差，只能 1 段',
              '`a = 0`：要尽量多的 AND 为 0 的段，==遇 0 就切==，把后面的数留给下一段'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`a = -1` 即二进制全 1，是 AND 的单位元，不能写成 0',
                 '末尾剩下 AND 大于 0 的数，合并进前一段，不影响答案',
                 '`ans = 0` 时答案是 1，所以 `max(ans, 1)`'],
    ),
)
