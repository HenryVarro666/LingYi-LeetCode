CONFIG = dict(
    num=2731, title='移动机器人', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='碰撞等价互换 + 逐个统计被减次数',
    tags=['灵神题单', '难度分 1923'],
    code='''
class Solution(object):
    def sumDistance(self, nums, s, d):

        for index, char in enumerate(s):
            if char == 'R':
                nums[index] += d
            else:
                nums[index] -= d
        
        nums.sort()
        res = 0
        mod = 10 ** 9 + 7
        for index in range(1, len(nums)):
            res = (res + nums[index] * index) % mod
            res = (res - nums[-index - 1] * index % mod + mod) % mod
        
        return res
''',
    call='Solution().sumDistance([0,2,5], "RLR", 1)',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums（机器人位置，d 秒后）', h=300, pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if S['_line'] == 13 and i == S['index'] else 'pink' if S['_line'] == 14 and i == len(S['nums']) - S['index'] - 1 else None)),
        dict(type='text', size=32, fn=lambda S: (f"`nums[{S['index']}]` 当被减数 {S['index']} 次；`nums[{len(S['nums'])-S['index']-1}]` 当减数 {S['index']} 次" if S['_line'] in (13, 14) else '')),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'for index, char in enumerate(s)': lambda S, B, r: ('所有机器人都处理完了' if B.get('index') == S.index else f'第 {S.index} 个机器人，方向 `{S.char}`'),
        "char == 'R'": lambda S, B, r: ('向右走 → 位置加 `d`' if S.char == 'R' else '向左走 → 位置减 `d`'),
        'nums[index] += d': '碰撞等于互换后折返，当作各走各的：`nums[{index}] = {nums[index]}`',
        'nums[index] -= d': '碰撞等于互换后折返，当作各走各的：`nums[{index}] = {nums[index]}`',
        'nums.sort()': '按最终坐标排序：`{nums}`',
        'res = 0': '`res` 累计距离和',
        'mod = ': '答案要取模：`mod = 10^9+7`',
        'for index in range(1, len(nums))': lambda S, B, r: ('枚举完了' if B.get('index') == S.index else f'枚举 `k = {S.index}`：左边有 k 个的机器人当被减数，右边有 k 个的当减数'),
        'res = (res + nums[index]': '`nums[{index}]` 左边有 {index} 个，当被减数 {index} 次：`res += {nums[index]}×{index}` → {res}',
        'res = (res - nums[-index - 1]': '`nums[{-index-1}]` 右边有 {index} 个，当减数 {index} 次：`res −= {nums[-index-1]}×{index}` → {res}',
        'return res': '距离和 `{res}`',
    },
    cards=dict(
        one_liner='相遇互换等于没发生：各走各的，再数每个坐标出现几次',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数轴上的机器人按 `s` 给的方向走 `d` 秒，相撞则掉头',
                 '求所有机器人两两距离之和，对 `10^9+7` 取模',
                 '示例：`nums=[0,2,5]`，`s="RLR"`，`d=1` → `10`'],
        quote='当两个机器人相遇时，完全可以将二者互换后再折返，这样一来就相当于什么都没有发生。',
        quote_src='—— yiduobo 题解原文',
        idea=['机器人没有差异，相遇互换再折返等于各走各的，一趟遍历算出最终坐标',
              '排序后下标 k 的机器人左边有 k 个，作被减数 k 次',
              '下标 n−k−1 的机器人右边有 k 个，作减数 k 次，所以枚举 k 同时加一项减一项'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '减法要写成 `(… + mod) % mod`，避免取模后出现负数',
                 '排序必须在取模之前，大小关系才不会被打乱',
                 '对比灵神：灵神用前缀和 `i·a[i] − s`，本文按「被减/做减次数」两头配对'],
    ),
)
