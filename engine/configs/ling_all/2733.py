CONFIG = dict(
    num=2733, title='既不是最小值也不是最大值', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='前三个数取中间值', tags=['灵神题单', '难度分 1148'],
    code='''
class Solution:
    def findNonMinOrMax(self, nums: List[int]) -> int:
        return sorted(nums[:3])[1] if len(nums) > 2 else -1
''',
    call='Solution().findNonMinOrMax([3,2,1,4])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: '前三个数 ' + str(S['nums'][:3]) + '：排序后取中间那个，它严格夹在另外两个之间' if len(S['nums']) > 2 else ''),
        dict(type='array', var='nums', label='nums', h=300,
             color=lambda S, i, v: 'yellow' if i < 3 else None,
             dim=lambda S, i, v: i >= 3),
        dict(type='text', fn=lambda S: '黄色 = 前三个数；后面的数不用看', size=30),
    ],
    watch=[('n', 'len(nums)'), ('前三个', 'sorted(nums[:3])')],
    captions={
        'return sorted': '`len(nums) = {len(nums)}`：多于 2 个 → 前三个排序得 `{sorted(nums[:3])}`，取下标 1 的 =={ret}==；它比前三个里的最小、最大都不同，所以必然既非最小也非最大',
    },
    cards=dict(
        one_liner='数互不相同：前三个数里取中间值就是答案',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['数组 `nums` 由不同正整数组成，返回任一个既不是最小值也不是最大值的数',
                 '不存在就返回 `-1`',
                 '示例：`[3,2,1,4]` → `2`（`3` 也可以）'],
        quote='由于数组元素各不相同，所以答案一定在前三个数中，不妨取前三个数的中间值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长度不超过 2：每个数不是最小就是最大 → `-1`',
              '长度至少 3：前三个数互不相同，中间值 ==比其中一个大、比另一个小==',
              '整个数组的最小/最大也许在后面，但那只会让这个中间值仍然夹在中间'],
        before=[dict(heading='先想边界', lines=['只有 1 个数：它既是最小也是最大 → `-1`',
                '只有 2 个数：一个最小、一个最大 → `-1`',
                '3 个及以上：互不相同，一定能找到答案'])],
        after=[dict(heading='为什么前三个就够', lines=['前三个数互不相同，设排序后为 `a < b < c`',
                '`b` 比 `a` 大，所以 `b` 不是整个数组的最小值',
                '`b` 比 `c` 小，所以 `b` 也不是整个数组的最大值',
                '更大的、更小的数出现在后面也不影响这个结论'])],
        summary=['时间 `O(1)`，空间 `O(1)`（排序只排 3 个数）',
                 '易错点：长度 ≤ 2 要返回 `-1`，否则 `sorted(...)[1]` 会越界',
                 '「互不相同」是前提：有重复值时这个结论不成立'],
    ),
)
