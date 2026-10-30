def _txt(S):
    if 'x' not in S:
        return ''
    return f'第一堆乘积 `x = {S["x"]}`，第二堆乘积 `y = {S["y"]}`，目标 `target = {S["target"]}`'


def _cap_leaf(S, B, ret):
    n = len(S.nums)
    if S.level == n:
        ok = S.x == S.target and S.y == S.target
        return (f'`level = {n}`：每个数都分完了，`x = {S.x}`、`y = {S.y}`，'
                + ('两堆都等于 `target` → ==找到了== `True`' if ok else '至少一堆不等于 `target` → `False`，回溯'))
    return f'`level = {S.level}` < {n}：还要分配 `nums[{S.level}] = {S.nums[S.level]}`'


CONFIG = dict(
    num=3566, title='等积子集的划分方案', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='dfs 枚举每个数放哪一堆',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1459'],
    code='''
class Solution(object):
    def checkEqualPartitions(self, nums, target):

        def find(level, x, y):
            if level == len(nums):
                return x == target and y == target

            return find(level + 1, x * nums[level], y) or find(level + 1, x, y * nums[level])

        return find(0, 1, 1)
''',
    call='Solution().checkEqualPartitions([2, 3, 4, 6], 12)',
    expect=True,
    views=[
        dict(type='text', h=70, fn=_txt, size=26),
        dict(type='array', var='nums', label='nums（蓝色箭头 = 当前要分配的数）', h=150, cell=80, pointers={'level': 'blue'},
             dim=lambda S, i, v: i < S.get('level', 0)),
        dict(type='calls', h=300),
    ],
    watch=[('level', 'level', 'blue'), ('x', 'x', 'cyan'), ('y', 'y', 'orange'), ('target', 'target', 'green')],
    captions={
        'return find(0, 1, 1)': '从 `find(0, 1, 1)` 开始：两堆的乘积都从 `1` 算起（空堆乘积为 1）',
        'if level == len(nums)': _cap_leaf,
        'return x == target': lambda S, B, r: f'判断 `x == target and y == target` → {r}',
        'return find(level + 1': lambda S, B, r: (
            f'`nums[{S.level - 1}] = {S.nums[S.level - 1]}` 乘进==第一堆==：`x = {S.x}`；回溯回来再试第二堆'
            if S.x != B.get('x') else
            f'`nums[{S.level - 1}] = {S.nums[S.level - 1]}` 乘进==第二堆==：`y = {S.y}`'),
    },
    max_steps=100,
    cards=dict(
        one_liner='n 很小：每个数要么进 x 堆要么进 y 堆，dfs 全试一遍',
        complexity='时间 `O(2^n)`，空间 `O(n)`',
        problem=['数组 `nums`（元素互不相同），整数 `target`',
                 '能否分成两个非空子集，乘积都等于 `target`',
                 '本视频：`[2,3,4,6]`, `12` → `True`（`2×6` 和 `3×4`）'],
        quote='由于nums中的元素个数较少，因此可以直接一趟dfs，找出所有的划分方案并判断是否合法即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`find(level, x, y)`：前 `level` 个数已分好，两堆乘积分别是 `x`、`y`',
              '第 `level` 个数二选一：乘到 `x` 上，或乘到 `y` 上',
              '全部分完时直接判断 `x == target and y == target`，用 `or` 找到一个就立刻返回'],
        summary=['时间 `O(2^n)`，空间 `O(n)`（递归栈）',
                 '不用判非空：`n >= 3` 且互不相同，空堆乘积是 1，另一堆一定 `> 1`',
                 '`or` 短路：找到一个合法划分就不再往下搜',
                 '对比灵神：灵神进一步折半枚举 + 最简分数，复杂度降到 `O(2^(n/2))`'],
    ),
)
