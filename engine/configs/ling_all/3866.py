CONFIG = dict(
    num=3866, title='找到第一个唯一偶数', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数 · 再扫一遍',
    code='''
class Solution:
    def firstUniqueEven(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        for x in nums:
            if x % 2 == 0 and cnt[x] == 1:
                return x
        return -1
''',
    call='Solution().firstUniqueEven([3,4,2,5,4,6])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=220, label='nums', color=lambda S, k, v: 'blue' if v == S.get('x') else None),
        dict(type='map', var='cnt', h=300, fmt=lambda k, v: f'{k} : {v}'),
    ],
    watch=[('x', 'x', 'blue')],
    captions={
        'cnt = Counter': '统计每个数出现次数：`cnt = {cnt}`',
        'if x % 2 == 0 and cnt[x] == 1': lambda S, B, r: (
            f'`{S.x}` 是奇数 → 跳过' if S.x % 2 else
            (f'`{S.x}` 是偶数，但出现 `{S.cnt[S.x]}` 次，不是恰好一次 → 跳过' if S.cnt[S.x] != 1
             else f'`{S.x}` 是偶数，且恰好出现 1 次 → ==成立==')),
        'return x': '第一个满足条件的就是答案 =={x}==（按数组顺序，最早的先到）',
        'return -1': '没有出现恰好一次的偶数 → 返回 -1',
    },
    cards=dict(
        one_liner='先数一遍次数，再按顺序找第一个出现一次的偶数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums`，返回恰好出现一次的第一个偶数（以下标最早为准）',
                 '不存在就返回 `-1`',
                 '示例：`[3,4,2,5,4,6]` → `2`'],
        quote='遍历 nums，同时用哈希表（或者数组）统计每个数的出现次数。然后再次遍历 nums，如果 nums[i] 是偶数且只出现一次，返回 nums[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一遍：`Counter` 得到每个数的出现次数',
              '第二遍：仍按原数组顺序扫，保证返回的是下标最早的',
              '偶数 `x % 2 == 0` 且 `cnt[x] == 1` 就直接返回'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：第二遍要遍历 `nums` 而不是遍历 `cnt`，才能保证顺序',
                 '值域只有 100，也可以用长为 101 的数组代替哈希表'],
    ),
)
