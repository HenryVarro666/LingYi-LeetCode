CONFIG = dict(
    num=2856, title='删除数对后的最小数组长度', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='哈希统计最大频次',
    tags=['灵神题单', '难度分 1750'],
    code='''
class Solution(object):
    def minLengthAfterRemovals(self, nums):

        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        max_freq = max(freq.values())
        if len(nums) - max_freq >= max_freq:
            return len(nums) % 2
        else:
            return max_freq * 2 - len(nums)
''',
    call='Solution().minLengthAfterRemovals([1,2,2,2,2,3])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', h=220,
             color=lambda S, i, v: 'orange' if 'v' in S and i < len(S['nums']) and v == S['v'] else None),
        dict(type='map', var='freq', label='freq：每个数出现几次', h=300),
        dict(type='text', size=30, fn=lambda S: (
            f"`max_freq = {S['max_freq']}`，其余元素共 `{len(S['nums'])-S['max_freq']}` 个" if 'max_freq' in S else '')),
    ],
    watch=['v', ('max_freq', 'max_freq', 'orange')],
    captions={
        'freq = {}': '用字典 `freq` 统计每个数的出现次数',
        'for v in nums': '取出 `v = {v}`',
        'freq[v] =': '`freq[{v}]` 变成 `{freq[v]}`',
        'max_freq = max': '最大频次 `max_freq = {max_freq}`：这个数能配的对象只有其他 `{len(nums) - max_freq}` 个',
        'if len(nums)': lambda S, B, r: (f'其余 `{len(S.nums)-S.max_freq}` >= `max_freq {S.max_freq}`？成立：任何数都能找到不同的搭档'
                                         if len(S.nums) - S.max_freq >= S.max_freq else
                                         f'其余 `{len(S.nums)-S.max_freq}` >= `max_freq {S.max_freq}`？不成立：最大频次的数配不完'),
        'return len(nums) % 2': '能配完：长度偶数剩 0，奇数剩 1 → =={ret}==',
        'return max_freq': '配不完：`{max_freq} * 2 - {len(nums)}` = =={ret}==，这些都是同一个数，无法再删',
    },
    cards=dict(
        one_liner='最多的那个数配不完，就剩下配不掉的；否则看奇偶',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['非递减数组，每次选两个 `nums[i] < nums[j]` 的数一起删掉',
                 '求任意次操作后数组最短长度',
                 '本视频：`[1,2,2,2,2,3]` → `2`'],
        quote='只要数组中各元素出现次数的最大值max_freq不超过数组长度的一半，那么必然有办法将数组删完或者删到只剩下一个元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['任何数 x 都能和任何不同的 y 配成一对',
              '`max_freq` 不超过一半：删完或剩 1 个，看长度奇偶',
              '否则最多形成 `n - max_freq` 对，剩 `max_freq*2 - n` 个'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '这份写法不用到数组有序，用字典统计频次',
                 '易错点：不过半时别写成 0，要看奇偶',
                 '对比灵神：灵神利用有序性只用二分，`O(log n)`'],
    ),
)
