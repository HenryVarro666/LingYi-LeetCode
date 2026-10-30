CONFIG = dict(
    num=2731, title='移动机器人', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='碰撞等价穿过 + 排序后算两两距离和',
    tags=['灵神题单', '难度分 1923'],
    code='''
class Solution:
    def sumDistance(self, nums: List[int], s: str, d: int) -> int:
        for i, c in enumerate(s):
            nums[i] += d if c == 'R' else -d
        nums.sort()

        ans = s = 0
        for i, x in enumerate(nums):
            ans += i * x - s
            s += x
        return ans % (10 ** 9 + 7)
''',
    call='Solution().sumDistance([0,2,5], "RLR", 1)',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums（机器人位置，d 秒后）', h=300, pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if S['_line'] >= 9 and i < S.get('i', 0) else None),
        dict(type='text', size=34, fn=lambda S: (f"`ans += {S['i']} × {S['x']} − {S['s']}` → ans = =={S['ans']}==" if S['_line'] in (10, 11) and 'x' in S and S['i'] is not None else '')),
    ],
    watch=['i', 'x', ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'for i, c in enumerate(s)': lambda S, B, r: ('所有机器人都处理完了' if B.get('i') == S.i else f'第 {S.i} 个机器人，方向 `{S.c}`'),
        'nums[i] +=': '碰撞等于互相穿过，各走各的：`nums[{i}]` 直接加减 `d`，变成 `{nums[i]}`',
        'nums.sort()': '机器人无法区分，交换位置不影响距离和：==排序==后 `{nums}`',
        'ans = s = 0': '`ans` 是距离和，`s` 是左边已遍历数的前缀和',
        'for i, x in enumerate(nums)': lambda S, B, r: ('所有数都枚举完了' if B.get('i') == S.i else f'枚举第 `{S.i}` 小的数 `x = {S.x}`，它左边有 `{S.i}` 个数'),
        'ans += i * x - s': '`x` 与左边 {i} 个数的距离和 = `{i}×{x} − {s}` = {i * x - s}，`ans` = {ans}',
        's += x': '`x` 加进前缀和：`s = {s}`',
        'return ans': '对 `10^9+7` 取模，答案 `{ret}`',
    },
    cards=dict(
        one_liner='碰撞等于穿过：各走各的，排序后算两两距离和',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数轴上有机器人，`s[i]` 指定方向，每秒走一格，相撞立刻掉头',
                 '求 `d` 秒后所有机器人两两距离之和，对 `10^9+7` 取模',
                 '示例：`nums=[0,2,5]`，`s="RLR"`，`d=1` → `10`'],
        quote='相撞等价于机器人互相穿过对方，因为我们无法区分机器人。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最后只问距离和：位置数组任意交换都不影响，机器人==不可区分==',
              '所以可以无视碰撞，每个机器人独立走 `d` 步',
              '排序后第 `i` 小的数 `a[i]` 与左边的距离和是 `i·a[i] − 前缀和`，边遍历边累加'],
        summary=['时间 `O(n log n)`，瓶颈是排序；空间可原地 `O(1)`',
                 '==不能在排序前取模==：取模会打乱大小关系，`i` 就对不上了',
                 '代码里 `s` 先是方向字符串，后面被复用成前缀和',
                 '类似思路：1503 所有蚂蚁掉下来前的最后一刻'],
    ),
)
