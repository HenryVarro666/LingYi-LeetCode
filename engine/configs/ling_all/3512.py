CONFIG = dict(
    num=3512, title='使数组和能被 K 整除的最少操作次数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='总和取模',
    tags=[],
    code='''
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        return sum(nums) % k
''',
    call='Solution().minOperations([3,9,7], 5)',
    expect=4,
    views=[
        dict(type='array', var='nums', h=240, label='nums'),
        dict(type='text', size=34, fn=lambda S: f"`s = sum(nums) = {sum(S['nums'])}`，`k = {S['k']}`" if 'nums' in S else ''),
        dict(type='text', size=34, fn=lambda S: f"至少要减 `s mod k` = `{sum(S['nums'])} mod {S['k']}` = =={sum(S['nums']) % S['k']}==" if 'nums' in S else ''),
    ],
    watch=['k', ('sum(nums)', 'sum(nums)', 'cyan'), ('答案', 'sum(nums) % k', 'green')],
    captions={
        'return sum': '总和 `{sum(nums)}`，每次操作只能让总和减 1：减到不超过它的最大的 `{k}` 的倍数，需要 `{sum(nums)} % {k}` = =={ret}== 次',
    },
    cards=dict(
        one_liner='每次操作让总和减 1，所以答案就是总和模 k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作可把某个 `nums[i]` 减 1，求让元素和被 `k` 整除的最少操作次数',
                 '示例：`nums=[3,9,7], k=5` → `4`'],
        quote='每次操作可以把 s 减少 1。目标是把 s 变成一个 k 的倍数，且操作次数越小越好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只关心总和 `s`，减哪个元素都一样',
              '比如 `s=8, k=3`：减 2 次变成 6',
              '一般地，至少操作 `s % k` 次就到了 k 的倍数'],
        before=[dict(heading='先看一个小例子', lines=['`s = 8, k = 3`：8 不是 3 的倍数', '最近的更小倍数是 `6`，要减 `8 − 6 = 2` 次', '而 `8 % 3 = 2`，正好相等'])],
        after=[dict(heading='三个示例对照', lines=['`[3,9,7], k=5`：和 19，`19 % 5 = 4`', '`[4,1,3], k=4`：和 8，`8 % 4 = 0`，不用操作', '`[3,2], k=6`：和 5，`5 % 6 = 5`，全减成 0'])],
        summary=['时间 `O(n)`（求和），空间 `O(1)`',
                 '易错：不用管具体减哪个数；题目保证 nums[i] 够减，直接取模即可',
                 '本质：求余数 = 到下一个更小倍数的距离'],
    ),
)
