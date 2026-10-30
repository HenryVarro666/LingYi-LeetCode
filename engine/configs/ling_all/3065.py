CONFIG = dict(
    num=3065, title='超过阈值的最少操作数 I', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='统计小于 k 的个数', tags=[],
    code='''
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        return sum(x < k for x in nums)
''',
    call='Solution().minOperations([2,11,10,1,3,9,12], 10)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: f"阈值 `k = {S['k']}`：小于 k 的数必须被删，共 ==" + str(sum(v < S['k'] for v in S['nums'])) + "== 个"),
        dict(type='array', var='nums', h=300, label='nums（红 = 小于 k，要删）',
             color=lambda S, i, v: 'red' if v < S['k'] else 'green'),
    ],
    watch=['k', ('x', 'x', 'yellow')],
    captions={
        'return sum': lambda S, B, ret: f'每次只能删最小值 → ==所有小于 k 的数都得删，其余一个不用删==。数一数：`2, 1, 3, 9` 共 `{ret}` 个，返回 `{ret}`',
    },
    cards=dict(
        after=[dict(heading='逐个看一遍', lines=['`2 < 10` 要删，`11` 不用，`10` 不用（等于 k 不删）',
                                                '`1 < 10` 要删，`3 < 10` 要删，`9 < 10` 要删，`12` 不用',
                                                '一共 `4` 个小于 k，每次删当前最小值，删 4 次就够了',
                                                '`sum(x < k for x in nums)` 把 True 当 1 累加，就是这个计数'])],
        one_liner='小于 k 的数一定要删，其余不用动：数个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作可以删掉 `nums` 中的最小元素',
                 '求让所有元素都 `>= k` 的最少操作次数',
                 '示例：`[2,11,10,1,3]`，`k = 10` → `3`；本视频：`[2,11,10,1,3,9,12]` → `4`'],
        quote='由于所有小于 k 的数都要被删除，所以统计 nums 中的小于 k 的元素个数即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删最小值，等价于从小到大依次删掉所有 `< k` 的数',
              '一个 `>= k` 的数都不用删，所以答案就是 `< k` 的个数',
              '`x < k` 是布尔值，`sum` 把 True 当 1 相加，一行搞定'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '不需要排序，也不需要真的删除元素',
                 '易错：是 `x < k` 要删，等于 k 的不删',
                 'Python 技巧：`sum(布尔表达式 for ...)` 统计满足条件的个数'],
    ),
)
