NUMS = [3, 2, 4, 4, 1]


def _col(S, i, v):
    if 'index' not in S:
        return None
    if i == S['index']:
        return 'yellow'
    return None


CONFIG = dict(
    num=2297, title='跳跃游戏 VIII', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='DP + 两个单调栈找落脚点',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minCost(self, nums, costs):

        f = [0]
        mi = [0]
        ma = [0]

        n = len(nums)
        for index in range(1, n):
            f.append(f[-1] + costs[index])

            while mi and nums[mi[-1]] <= nums[index]:
                f[-1] = min(f[-1], f[mi[-1]] + costs[index])
                mi.pop()
            
            while ma and nums[ma[-1]] > nums[index]:
                f[-1] = min(f[-1], f[ma[-1]] + costs[index])
                ma.pop()
            
            mi.append(index)
            ma.append(index)
        
        return f[-1]
''',
    call='Solution().minCost([3,2,4,4,1], [3,7,6,4,2])',
    expect=8,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums', h=190,
             color=_col),
        dict(type='array', var='f', label='f[i] = 跳到 i 的最小代价', h=170, color=lambda S, i, v: 'green' if 'index' in S and i == S['index'] else None),
        dict(type='stack', var='mi', label='mi 栈（存下标，nums 递减：等着被 ≥ 它的数接住）', fmt=lambda i: f'{i}:{NUMS[i]}', h=140),
        dict(type='stack', var='ma', label='ma 栈（存下标，nums 递增：等着被 < 它的数接住）', fmt=lambda i: f'{i}:{NUMS[i]}', h=140),
    ],
    watch=[('index', 'index', 'blue'), ('nums[index]', 'nums[index]'), ('costs[index]', 'costs[index]'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f = [0]': '`f[i]` = 跳到 `i` 的最小代价，起点 `f[0] = 0`（起点不收费）',
        'mi = [0]': '`mi`：条件 1 的候选起点栈（要等一个 ≥ 它的数）',
        'ma = [0]': '`ma`：条件 2 的候选起点栈（要等一个 < 它的数）',
        'f.append': '先假设从 `i-1` 走一步过来（==每个位置必能跳到下一个==）：`f[{index}]` = `{f[index-1]} + {costs[index]}` = =={f[-1]}==',
        'while mi and': lambda S, B, r: (
            f'`mi` 栈顶下标 `{S.mi[-1]}`：`nums[{S.mi[-1]}] = {S.nums[S.mi[-1]]} <= {S.nums[S.index]}` → 成立，它的唯一落脚点就是 `{S.index}`'
            if S.mi and S.nums[S.mi[-1]] <= S.nums[S.index] else '`mi` 栈空了或栈顶 `> nums[index]`：不能再接住，停'),
        'while ma and': lambda S, B, r: (
            f'`ma` 栈顶下标 `{S.ma[-1]}`：`nums[{S.ma[-1]}] = {S.nums[S.ma[-1]]} > {S.nums[S.index]}` → 成立，它的唯一落脚点就是 `{S.index}`'
            if S.ma and S.nums[S.ma[-1]] > S.nums[S.index] else '`ma` 栈空了或栈顶 `<= nums[index]`：不能再接住，停'),
        'f[-1] = min(f[-1], f[mi[-1]]': '条件 1 跳过来：`f[{mi[-1]}] + {costs[index]}`，取小 → `f[{index}]` = =={f[-1]}==',
        'f[-1] = min(f[-1], f[ma[-1]]': '条件 2 跳过来：`f[{ma[-1]}] + {costs[index]}`，取小 → `f[{index}]` = =={f[-1]}==',
        'mi.pop()': '落脚点已经找到，栈顶不会再有别的落脚点（==至多一个==）→ 弹出',
        'ma.pop()': '落脚点已经找到，栈顶不会再有别的落脚点（==至多一个==）→ 弹出',
        'mi.append': '`{index}` 入两个栈，等着后面的数来接',
        'return f[-1]': '到达最后一个位置，最小代价 =={ret}==',
    },
    cards=dict(
        one_liner='每个位置往后最多只有一个跳跃落脚点，用两个单调栈找出来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 与 `costs`，从下标 0 出发，目标是 `n-1`，落到 `j` 付 `costs[j]`',
                 '从 `i` 只能跳到 `j > i` 且满足下面之一：',
                 '`nums[i] <= nums[j]` 且中间都 `< nums[i]`；或 `nums[i] > nums[j]` 且中间都 `>= nums[i]`',
                 '示例：`nums=[3,2,4,4,1]`，`costs=[3,7,6,4,2]` → `8`'],
        quote='每个位置如果要越过某些位置向后跳，那么其最多只有一个落脚点 j。……不可能同时满足。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个条件互斥，而且各自连续满足不了 → 每个位置的落脚点最多各一个',
              '条件 1 的落脚点用单调递减栈 `mi` 找，条件 2 的用单调递增栈 `ma` 找',
              '`f[i]` 初值 `f[i-1] + costs[i]`；每次被栈顶接住就用 `f[栈顶] + costs[i]` 更新'],
        summary=['时间 `O(n)`，空间 `O(n)`（每个下标各入、出两个栈一次）',
                 '一步到下一个位置总是合法的：`f[i-1] + costs[i]` 当初值',
                 '`mi` 用 `<=`、`ma` 用 `>`：别搞混两个条件的等号',
                 '代码本身是 Python 3 写法，无需改动',
                 '同类题：单调栈找「下一个更大/更小」'],
    ),
)
