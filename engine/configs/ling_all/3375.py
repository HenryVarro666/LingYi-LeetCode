CONFIG = dict(
    num=3375, title='使数组的值全部为 K 的最少操作次数', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='等价转化 · 不同元素个数',
    tags=['灵神题单', '难度分 1383'],
    code='''
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        mn = min(nums)
        if k > mn:
            return -1
        return len(set(nums)) - (k == mn)
''',
    call='Solution().minOperations([5,2,5,4,5,3], 2)',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', h=240,
             color=lambda S, i, v: 'green' if 'mn' in S and v == S['mn'] else ('orange' if v > S['k'] else None)),
        dict(type='set', var=lambda S: set(S['nums']), h=170, fmt=lambda x: str(x), label='set(nums)'),
        dict(type='text', fn=lambda S: (f"最小值 `{S['mn']}`，k = `{S['k']}`" + ('：k 比最小值大，永远变不成 → ==-1==' if S['k'] > S['mn'] else '：k ≤ 最小值，可以做到')) if 'mn' in S else f"目标 k = `{S['k']}`", size=30),
        dict(type='text', fn=lambda S: (f"不同元素 `{len(set(S['nums']))}` 个，每次操作消灭一个最大值" + ('；k == mn，少一次' if S['k'] == S['mn'] else '；k < mn，还要再降一次')) if 'mn' in S and S['k'] <= S['mn'] else '', size=28),
    ],
    watch=[('k', 'k', 'pink'), ('mn', 'mn', 'green'), ('不同元素', 'len(set(nums))', 'orange')],
    captions={
        'mn = min': '`mn = min(nums) = {mn}`：操作只会把数变小，所以最后只能变成 `<= mn` 的数',
        'if k > mn': lambda S, B, r: (f'`k = {S.k} > mn = {S.mn}`：最小的数不可能变大 → 无解' if S.k > S.mn else f'`k = {S.k} <= mn = {S.mn}`：k 不超过最小值，有解'),
        'return -1': '返回 `-1`：每次操作只能把大于 h 的数降下来，到不了更大的 k',
        'return len': '每次选 h 为次大值，把最大值降一档：`len(set(nums)) = {len(set(nums))}` 个不同值，降到最小值要 `{len(set(nums)) - 1}` 次；`k == mn` 为 `{k == mn}`，所以答案 =={ret}==',
    },
    cards=dict(
        one_liner='每次操作只能把最大值降到次大值，数不同值的个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选一个「合法」的 `h`（所有大于 `h` 的数都相等），把大于 `h` 的数都变成 `h`',
                 '求把全部数变成 `k` 的最少操作次数，做不到返回 `-1`',
                 '示例：`[5,2,5,4,5], k=2` → `2`；本视频：`[5,2,5,4,5,3], k=2` → `3`'],
        quote='所以操作只能改变大于次大值的数，也就是==最大值==。……每次选 `h` 为次大值是最优的。贪心地想，能一步到达次大值，没必要分好几步。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`h` 不能低于次大值，所以一次只能把「最大值」降到「次大值」',
              '数组里有 `m` 种不同的值，降到最小值要 `m-1` 次',
              '再分三种情况：`k > min` 无解；`k == min` 恰好 `m-1` 次；`k < min` 还要再降一次，共 `m` 次'],
        after=[dict(heading='分类讨论', lines=['`k > min(nums)`：最小的数永远不会变大 → `-1`',
                                               '`k == min(nums)`：答案 = 不同元素个数 − 1',
                                               '`k < min(nums)`：答案 = 不同元素个数',
                                               '合起来：`len(set(nums)) - (k == mn)`'])],
        summary=['时间 `O(n)`，空间 `O(n)`（`set`）',
                 '易错：先判 `k > mn` 返回 -1，再数不同元素',
                 '`k == mn` 是布尔值，减的是 1 或 0',
                 '同类思路：读懂操作到底改了什么（只改最大值），再数档位'],
    ),
)
