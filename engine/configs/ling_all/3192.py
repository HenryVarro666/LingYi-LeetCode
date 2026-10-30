def _eff(S):
    nums, k = S['nums'], S['k']
    return [x ^ (k % 2) for x in nums]


CONFIG = dict(
    num=3192, title='使二进制数组全部等于 1 的最少操作次数 II', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='从左到右 · 记录操作次数奇偶',
    tags=['灵神题单', '难度分 1433'],
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        k = 0
        for x in nums:
            if x == k % 2:  # 必须操作
                k += 1
        return k
''',
    call='Solution().minOperations([0,1,1,0,1])',
    expect=4,
    views=[
        dict(type='text', size=34, fn=lambda S: (f"之前操作了 `{S['k']}` 次（{'奇' if S['k'] % 2 else '偶'}数）" + (f"，当前 `x = {S['x']}` 被反转成 =={S['x'] ^ (S['k'] % 2)}==" if 'x' in S else '')) if 'k' in S else ''),
        dict(type='array', var='nums', h=240, label='nums（原始值）',
             color=lambda S, i, v: None),
    ],
    watch=[('k', 'k', 'green'), ('k % 2', 'k % 2', 'blue'), 'x'],
    captions={
        'k = 0': '`k` 是之前的操作次数，只关心它的==奇偶性==',
        'for x in nums': '遍历到 `x = {x}`：前面的 `{k}` 次操作都会反转它，所以它现在是 `{x ^ (k % 2)}`',
        'if x == k % 2': lambda S, B, r: (f'`x = {S.x}`，`k % 2 = {S.k % 2}`：相等 → 反转后是 0，==必须操作==' if S.x == S.k % 2 else f'`x = {S.x}`，`k % 2 = {S.k % 2}`：不等 → 反转后已是 1，不用操作'),
        'k += 1': '从这里操作一次（一定要、且至多一次）：`k` → {k}，后面的元素奇偶翻转',
        'return k': '操作次数 `{k}`',
    },
    cards=dict(
        one_liner='从左到右，遇到（被反转后的）0 就必须操作',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可选下标 `i`，把 `i` 到末尾的所有元素 0/1 反转',
                 '求把 `nums` 全变成 1 的最少操作次数',
                 '示例：`[0,1,1,0,1]` → `4`'],
        quote='反转偶数次等于没反转，所以只需考虑操作次数的奇偶性。……从左到右的操作方式有且仅有一种。',
        quote_src='—— 灵茶山艾府题解',
        idea=['操作顺序不影响结果，同一下标最多一次 → 可以从左到右处理',
              '`nums[i]` 只受左边操作影响：设之前操作了 `k` 次',
              '`x == k % 2` 说明现在是 0，==必须操作==；否则已是 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '题解还给了方法二：`(nums[0]^1) + sum(x^y for x,y in pairwise(nums))`，数相邻不同的位置',
                 '易错：`x == k % 2` 才操作，别写反',
                 '相似思路：翻转后缀、灯泡开关类题'],
        before=[],
    ),
)
