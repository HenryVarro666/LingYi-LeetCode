CONFIG = dict(
    num=2592, title='最大化数组的伟大值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='田忌赛马 · 排序 + 单调指针',
    tags=['灵神题单', '贪心与思维', '难度分 1569'],
    code='''
class Solution(object):
    def maximizeGreatness(self, nums):

        nums.sort()
        p = 0
        for index, v in enumerate(nums):
            while p < len(nums) and nums[p] <= v:
                p += 1
            
            if p == len(nums):
                break
            
            p += 1
        
        return index
''',
    call='Solution().maximizeGreatness([1,3,5,2,1,3,1])',
    expect=4,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"`nums[{S['index']}] = {S['v']}` 找配对：第一个比它大的是 `nums[{S['p']}]`" if 'v' in S and 'p' in S and S['p'] < len(S['nums']) else '先排序，再让每个数找「刚好比它大」的对手')),
        dict(type='array', var='nums', pointers={'index': 'blue', 'p': 'pink'}, h=300, label='nums（排序后）',
             color=lambda S, i, v: 'green' if 'index' in S and i < S['index'] else None),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'cyan'), ('p', 'p', 'pink')],
    captions={
        'nums.sort()': '排序：弱的数先找对手 → `{nums}`',
        'p = 0': '`p` 是当前配对对手的下标，只会往右走',
        'for index, v in enumerate': '轮到 `nums[{index}] = {v}`：它要找一个刚好比它大的对手',
        'while p < len(nums)': lambda S, B, r: (f"`nums[{S.p}] = {S.nums[S.p]}` ≤ `{S.v}` → 打不过，`p` 右移" if S.p < len(S.nums) and S.nums[S.p] <= S.v
                                              else (f"`p = {S.p}` 到末尾了，没有对手可选" if S.p >= len(S.nums) else f"`nums[{S.p}] = {S.nums[S.p]}` > `{S.v}` → 找到刚好赢的对手，停")),
        'p += 1': lambda S, B, r: (f'`nums[{S.p - 1}] <= v`，打不过 → `p` 右移到 {S.p}' if S._line == 8 else f'`nums[{S.p - 1}]` 配给 `v = {S.v}`，这个对手用掉了，`p` → {S.p}'),
        'if p == len(nums)': lambda S, B, r: ('`p == len(nums)` → ==成立==：没有更大的数了，后面的数需求只会更高，配对到此为止' if S.p == len(S.nums)
                                              else f'`p = {S.p}` < `{len(S.nums)}` → 还有对手，这个数配对成功'),
        'break': '结束遍历：此时 `index = {index}` 正好是前面成功配对的数量',
        'return index': '返回 `index` = =={index}==',
    },
    cards=dict(
        one_liner='牺牲最小值，每个数都挑刚好能赢的对手',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['重排 `nums` 为 `perm`，数 `perm[i] > nums[i]` 的个数，求最大值',
                 '示例：`[1,3,5,2,1,3,1]` → `4`',
                 '数组里可能有相同值，需要一点调整'],
        quote='1、尽量挑弱的对手打形成配对  2、每次配对时，都选择能刚好赢的数',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后遍历：当前数 `v` 的对手下标 `p`，因为 `v` 单调不减，`p` 只会右移',
              '`while nums[p] <= v` 跳过打不过的，停下就是刚好赢的',
              '`p` 走到末尾：后面的数更大，也找不到对手，直接返回已配对数 `index`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`p` 单调右移，整个 while 均摊 `O(n)`',
                 '`index` 恰好等于 break 时已配对的个数（前面每个数各配一个）',
                 '原文为 Python 2 风格，本视频无需修改，直接运行'],
    ),
)
