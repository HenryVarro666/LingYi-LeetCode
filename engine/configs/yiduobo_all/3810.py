CONFIG = dict(
    num=3810, title='变成目标数组的最少操作次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='集合去重 · 记录需要修改的值',
    tags=['贪心算法', '思维题', '难度分 1492'],
    code='''
class Solution(object):
    def minOperations(self, nums, target):
        
        m = set()
        for x, y in zip(nums, target):
            if x != y:
                m.add(x)
        
        return len(m)
''',
    call='Solution().minOperations([1,2,1,2,7,3], [3,4,5,6,7,3])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=210, label='nums',
             color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] else None),
        dict(type='array', var='target', h=210, label='target',
             color=lambda S, i, v: 'green' if S['nums'][i] == v else None),
        dict(type='set', var='m', h=150, fmt=lambda x: str(x), label='m（需要操作的 x）'),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        'm = set()': '`m` 集合：存==需要操作的数值==，重复的只留一个',
        'for x, y in zip': '同时取 `nums` 的 `x = {x}` 和 `target` 的 `y = {y}`',
        'if x != y': lambda S, B, r: (f'`x = {S.x}` ≠ `y = {S.y}` → 这个位置要改，`{S.x}` 必须被选中操作一次' if S.x != S.y else f'`x = {S.x}` == `y = {S.y}` → 已经对了，不用管'),
        'm.add(x)': '`{x}` 加入集合 `m` = {sorted(m)}（已有则不变）',
        'return len': '集合大小 `len(m)` = =={ret}==：每个数值只要操作一次',
    },
    cards=dict(
        one_liner='一次操作能把 nums 里同一个值全部调好，数一数有几个不同的值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选整数 `x`，找出 `nums` 中全部等于 `x` 的极大连续段，把它们改成对应的 `target`',
                 '求把 `nums` 变成 `target` 的最少操作次数',
                 '本视频：`[1,2,1,2,7,3]` → `[3,4,5,6,7,3]` 答案 `2`'],
        quote='每次操作，都选择一个整数x，然后将nums中所有等于x的都变为与对应的target相等。',
        quote_src='—— yiduobo 题解原文',
        idea=['描述绕，其实是每次选一个值 `x`，把 `nums` 里所有 `x` 一次性调成目标值',
              '一趟遍历：`nums[index] != target[index]` 就把这个值放进集合',
              '集合里有几个值，就需要几次操作'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '放进集合的是 `nums` 的值 `x`，不是 `target` 的值，也不是下标',
                 '`x == y` 的位置不用管，即使 `x` 在别处出现也不影响',
                 '对比灵神：灵神先论证“下界能达到”，yiduobo 直接按操作含义计数',
                 '原文为 Python 2 风格，除类型说明外代码无需改动'],
    ),
)
