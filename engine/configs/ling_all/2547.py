def _state(S):
    return list(S['state']) if 'state' in S else []


CONFIG = dict(
    num=2547, title='拆分数组的最小代价', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP · 倒序枚举 + 唯一元素计数',
    tags=['常用数据结构'],
    code='''
class Solution:
    def minCost(self, nums: List[int], k: int) -> int:
        n = len(nums)
        f = [0] * (n + 1)
        for i in range(n):
            state, unique, mn = [0] * n, 0, inf
            for j in range(i, -1, -1):
                x = nums[j]
                if state[x] == 0:  # 首次出现
                    state[x] = 1
                    unique += 1
                elif state[x] == 1:  # 不再唯一
                    state[x] = 2
                    unique -= 1
                mn = min(mn, f[j] - unique)
                # if f[j]-unique < mn: mn = f[j]-unique  # 手写 min 会快很多
            f[i + 1] = k + mn
        return f[n] + n
''',
    call='Solution().minCost([1,2,1,1], 2)',
    expect=5,
    skip=['x = nums[j]', 'state[x] = 1', 'state[x] = 2'],
    max_steps=80,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 最后一段 nums[j..i]）', window=('j', 'i'), pointers={'j': 'blue', 'i': 'pink'}, h=210),
        dict(type='array', var=_state, label='state[x]：0 未出现，1 出现一次，2 出现多次（每个 i 重新清零）', h=190),
        dict(type='array', var=lambda S: ['∞' if v == float('inf') else v for v in S['f']], label="f'[t] = f[t] − t（最后答案 f'[n] + n）", pointers={'j': 'blue'}, h=200),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), ('unique', 'unique', 'cyan'), ('mn', 'mn', 'orange')],
    captions={
        'f = [0]': '`f[t]` 是前 `t` 个数的最小代价（已减去 `t`，即 `f[t] - t`），初始 `f[0] = 0`',
        'for i in range': lambda S, B, r: (f'计算 `f[{S.i+1}]`：划分 `nums[0..{S.i}]`，枚举最后一段的起点 `j`' if 'i' in S and S.get('_line') == 5 and S.f[S.i+1] == 0 else '所有 `i` 都算完了'),
        'state, unique, mn': '新的一轮：`state` 清零，`unique` = 只出现一次的数的个数，`mn` 记录最小值',
        'if state[x] == 0': lambda S, B, r: (f'`nums[{S.j}] = {S.nums[S.j]}` 首次出现 → 暂时唯一，`unique` +1' if S.state[S.nums[S.j]] == 0 else f'`nums[{S.j}] = {S.nums[S.j]}` 已出现过'),
        'unique += 1': '`state[{nums[j]}] = 1`：只出现一次 → `unique = {unique}`',
        'elif state[x] == 1': lambda S, B, r: (f'`{S.nums[S.j]}` 之前只出现一次，现在第二次 → ==不再唯一==' if S.state[S.nums[S.j]] == 1 else '已经出现过多次，`unique` 不变'),
        'unique -= 1': '`state[{nums[j]}] = 2`：它不再唯一 → `unique = {unique}`',
        'mn = min': '重要性 = 段长 − unique + k；去掉公共的 `i-j`：取 `min(f[j] − unique)` → `mn = min({B.mn}, {f[j]} − {unique}) = =={mn}==',
        'f[i + 1] = k': "`f'[{i+1}] = k + mn = {k} + ({mn})` = =={f[i+1]}==",
        'return f[n] + n': "答案 = `f'[n] + n` = `{f[n]} + {n}` = =={ret}==",
    },
    cards=dict(
        one_liner='划分型 DP：倒着枚举最后一段，边加数边维护只出现一次的个数',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['把数组拆成若干子数组，代价 = 每段的 `k + trimmed长度`',
                 '`trimmed` 去掉子数组里只出现一次的数，剩下元素个数就是重要性的主体',
                 '本视频：`nums = [1,2,1,1]`，`k = 2` → `5`'],
        quote='重要性为子数组的长度减去只出现一次的元素个数加 k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`state[x]`：0/1/2 表示出现 0/1/多次，`unique` 随之增减',
              '重要性 `= i−j+1 − unique + k`，把 `i−j+1` 拆开，定义 `f\'[t] = f[t] − t`',
              '`f\'[i+1] = k + min(f\'[j] − unique)`，最后答案 `f\'[n] + n`'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '`f` 存的是 `f[t]-t`，返回时要 `+ n`',
                 '`state` 每个 `i` 都要重新清零',
                 '灵神还给出线段树优化的 `O(n log n)` 写法，本视频演示 `O(n^2)` 版本'],
    ),
)
