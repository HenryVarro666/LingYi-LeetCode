CONFIG = dict(
    num=2784, title='检查数组是否是好的', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='集合去重 · 逐个检查',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def isGood(self, nums):

        if len(nums) == 1:
            return False

        vis = set()
        max_v = len(nums) - 1
        for v in nums:
            if v < 1 or v > max_v:
                return False
            if v in vis and v != max_v:
                return False
            vis.add(v)

        return len(vis) == max_v
''',
    call='Solution().isGood([3,1,4,2,4,3])',
    expect=False,
    views=[
        dict(type='array', var='nums', pointers={'v': 'blue'}, label='nums', h=220,
             color=lambda S, i, v: 'pink' if 'max_v' in S and v == S['max_v'] else None),
        dict(type='set', var='vis', label='vis（已见过的数）', h=200),
    ],
    watch=[('max_v', 'max_v', 'pink'), ('v', 'v', 'blue')],
    captions={
        'len(nums) == 1': lambda S, B, r: f'长度 `{len(S.nums)}`，不是 1，继续（长度 1 时 base 至少有 2 个元素，必为假）',
        'vis = set': '`vis` 集合记录出现过的数',
        'max_v = len': '`max_v = len(nums) - 1 = {max_v}`：好数组里最大的数只可能是它',
        'v < 1 or v > max_v': lambda S, B, r: f'`v = {S.v}`，范围 `[1, {S.max_v}]`：' + ('超出范围 → False' if (S.v < 1 or S.v > S.max_v) else '在范围内，继续'),
        'v in vis and v != max_v': lambda S, B, r: (f'`{S.v}` 已出现过，而且不是 `max_v` → ==重复了== → False' if (S.v in S.vis and S.v != S.max_v)
            else (f'`{S.v}` 已出现过，但它是 `max_v`，允许出现两次' if S.v in S.vis else f'`{S.v}` 第一次出现')),
        'vis.add(v)': '`{v}` 加入集合，`vis` 现在 {len(vis)} 个数',
        'return len(vis)': '集合大小要等于 `max_v`',
    },
    cards=dict(
        one_liner='用集合去重：只有最大的数可以重复，其余必须各出现一次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`base[n] = [1,...,n-1,n,n]`，判断 `nums` 是否是它的排列',
                 '示例：`[1,3,3,2]` → `true`',
                 '本视频：`[3,1,4,2,4,3]` → `false`'],
        quote='使用集合为数组去重，同时记录下数组中的最小值和最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['最大值只能是 `长度 - 1`，不在 `[1, max_v]` 就不是',
              '重复的数只允许是 `max_v`；别的数再次出现就返回 False',
              '最后集合里的不同数必须正好是 `max_v` 个'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '开头长度为 1 要单独返回 False（`[x]` 不可能是 base）',
                 '重复出现 `max_v` 多于两次时，集合元素数不够，由最后一句兜底',
                 '对比灵神：灵神把 nums 本身当标记数组，空间 `O(1)`'],
    ),
)
