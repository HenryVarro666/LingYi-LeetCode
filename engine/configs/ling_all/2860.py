def _info(S):
    if 'i' not in S:
        n = len(S['nums'])
        return f'选 `k` 个学生时方案==唯一==：排序后，前 `k` 个选、其余不选，共 `{n}` 个学生'
    i, x, y = S['i'], S['x'], S['y']
    ok = x < i < y
    return (f'选前 `{i}` 个学生：要求 `nums[{i-1}] < {i} < nums[{i}]` 即 `{x} < {i} < {y}` → '
            + ('==成立，多一种方案==' if ok else '不成立'))


CONFIG = dict(
    num=2860, title='让所有学生保持开心的分组方法数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 · 枚举分界线',
    tags=['灵神题单', '难度分 1626'],
    code='''
class Solution:
    def countWays(self, nums: List[int]) -> int:
        nums.sort()
        ans = nums[0] > 0  # 一个学生都不选
        for i, (x, y) in enumerate(pairwise(nums), 1):
            if x < i < y:
                ans += 1
        return ans + 1  # 一定可以都选
''',
    call='Solution().countWays([6, 0, 3, 3, 6, 7, 2, 7])',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=80),
        dict(type='array', var='nums', label='nums（排序后；绿 = 选中的前 i 个，蓝箭头 = 分界线右侧第一个 nums[i]）',
             pointers={'i': 'blue'}, cell=96, h=280,
             color=lambda S, k, v: 'green' if ('i' in S and k < S['i']) else None,
             dim=lambda S, k, v: 'i' in S and k > S['i']),
    ],
    watch=[('i', lambda S: S.get('i'), 'blue'), ('x', lambda S: S.get('x')), ('y', lambda S: S.get('y')), ('ans', lambda S: int(S['ans']) if 'ans' in S else None, 'green')],
    captions={
        'nums.sort()': '排序后：选 `k` 人就是选==前 `k` 小==，其余不选 → 每个 `k` 只有唯一方案',
        'ans = nums[0] > 0': '一个都不选：要让没选的人都开心，需要 `0 < nums[0]` → `{nums[0]} > 0` 为 `{ans}`',
        'for i, (x, y)': '分界线在 `nums[{i-1}]` 和 `nums[{i}]` 之间：选前 `i = {i}` 个，`x = {x}`，`y = {y}`',
        'if x < i < y': lambda S, B, r: (f'选的 `{S.i}` 人都要 `x = {S.x} < {S.i}`，没选的都要 `{S.i} < y = {S.y}` → '
                                          + ('==两边都满足==' if S.x < S.i < S.y else '不满足，这个分界线不行')),
        'ans += 1': '选前 `{i}` 个学生是一种合法方案，`ans` = {int(ans)}',
        'return ans + 1': '全选一定合法（`nums[i] < n`）：`{int(ans)} + 1` = =={ret}==',
    },
    cards=dict(
        one_liner='选 k 人的方案唯一：排序后枚举分界线',
        complexity='时间 `O(n log n)`，空间 `O(1)`（忽略排序栈）',
        problem=['`nums[i]` 是第 `i` 个学生的要求：选中则人数要 ==严格大于== 它，没选则人数要 ==严格小于== 它',
                 '返回让所有学生都开心的选人方案数',
                 '本视频：`[6,0,3,3,6,7,2,7]` → `3`'],
        quote='在选择学生人数固定的时候，选择方案是唯一的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['恰好选 `k` 人：`nums[i] < k` 的必须选，`nums[i] > k` 的不能选，`nums[i] = k` 的不能出现',
              '排序后以分界线切开：选 `i` 个 ⇔ `nums[i-1] < i < nums[i]`',
              '枚举 `i = 1..n-1`；再单独处理 选 0 个（`nums[0] > 0`）和选 `n` 个（一定可以）'],
        result='运行结束，返回 `3`：选 1 个、4 个、全选',
        summary=['时间 `O(n log n)`，瓶颈在排序；用计数排序可做到 `O(n)`',
                 '易错：别漏掉选 0 个和选 n 个两种特殊情况',
                 '`ans = nums[0] > 0` 是布尔值，之后 `ans += 1` 会当作整数用',
                 '`pairwise(nums)` 每次给出相邻两个数 `(x, y)`，`enumerate` 从 1 开始，`i` 正好是分界线左边的人数'],
    ),
)
