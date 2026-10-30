_I = lambda S: S['_inner'].get('i') if 'f0' in S['_inner'] else None


CONFIG = dict(
    num='LCR 090', title='打家劫舍 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='环形 → 两次线性 DP',
    tags=[],
    code='''
class Solution:
    def rob1(self, nums: List[int]) -> int:
        f0 = f1 = 0
        for i, x in enumerate(nums):
            f0, f1 = f1, max(f1, f0 + x)
        return f1

    def rob(self, nums: List[int]) -> int:
        return max(nums[0] + self.rob1(nums[2:-1]), self.rob1(nums[1:]))
''',
    call='Solution().rob([2,7,9,3,1])',
    expect=11,
    skip=['f0 = f1 = 0', 'for i, x in enumerate'],
    views=[
        dict(type='array', var=lambda S: S['_inner'].get('nums', []), label='当前处理的 nums（蓝 = 当前房子 x）', cell=84, h=230,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'},
             color=lambda S, k, v: 'blue' if 'x' in S['_inner'] and k == S['_inner'].get('i') else None),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"不偷：`f1 = {S['_inner']['f1']}`　偷：`f0 + x = {S['_inner']['f0']} + {S['_inner']['x']}` → 取大 ==`{max(S['_inner']['f1'], S['_inner']['f0'] + S['_inner']['x'])}`=="
                           if 'x' in S['_inner'] and S.get('_line') == 6 else "第一间和最后一间相邻：分「偷 nums[0]」和「不偷 nums[0]」两种情况")),
    ],
    watch=[('x', lambda S: S['_inner'].get('x', ''), 'blue'), ('f0', lambda S: S['_inner'].get('f0', ''), 'cyan'), ('f1', lambda S: S['_inner'].get('f1', ''), 'green')],
    captions={
        'f0, f1 = f1': lambda S, B, ret: (f'`f1 = max({B.f1}, {B.f0} + {B.x}) = {S.f1}`：'
                                           + ('偷这间更多' if B.f0 + B.x > B.f1 else '不偷更多（或一样）')),
        'return f1': '这一段非环形房子的最大金额 = =={ret}==',
        'return max(': '两种方案取大：偷 `nums[0]` → `{B.nums[0]} + rob1(nums[2:-1])`，其中 `nums[2:-1] = {B.nums[2:-1]}`（`nums[1]`、`nums[n-1]` 都不能偷）；不偷 → `rob1(nums[1:])`，`nums[1:] = {B.nums[1:]}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='环形拆成两个线性问题：偷不偷第一间',
        complexity='时间 `O(n)`，空间 `O(1)`（忽略切片开销）',
        problem=['房屋围成一圈，第一间和最后一间也相邻，相邻不能同时偷',
                 '求不触发警报时能偷到的最高金额',
                 '示例：`[2,3,2]` → `3`；本视频：`[2,7,9,3,1]` → `11`'],
        quote='如果偷 nums[0]，那么 nums[1] 和 nums[n-1] 不能偷，问题变成从 nums[2] 到 nums[n-2] 的非环形版本；如果不偷 nums[0]，那么问题变成从 nums[1] 到 nums[n-1] 的非环形版本。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分类讨论：是否偷 `nums[0]`',
              '偷：去掉两个邻居，剩 `nums[2:-1]`，再加上 `nums[0]`',
              '不偷：剩 `nums[1:]`；两个子问题都直接复用 198 题的 `rob1`',
              '两种方案取最大值'],
        result='两种方案取大，答案 11',
        summary=['时间 `O(n)`，空间 `O(1)`（Python 忽略切片开销）',
                 '易错：偷 `nums[0]` 时区间是 `nums[2:-1]`（去掉 1 和 n-1），不是 `nums[2:]`',
                 '`n = 1` 时 `nums[2:-1]` 为空，`rob1` 返回 0，所以结果正好是 `nums[0]`',
                 '前置题：LCR 089 / 198 打家劫舍'],
    ),
)
