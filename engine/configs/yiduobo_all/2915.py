NUMS, TARGET = [1, 2, 1, 3], 4

CONFIG = dict(
    num=2915, title='和为目标值的最长子序列的长度', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='0-1 背包：倒序遍历 index 压掉 i 维',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1659'],
    code='''
class Solution(object):
    def lengthOfLongestSubsequence(self, nums, target):

        f = [-1] * (target + 1)
        f[0] = 0
        for v in nums:
            for index in range(target, v - 1, -1):
                if f[index - v] >= 0 and f[index] < f[index - v] + 1:
                    f[index] = f[index - v] + 1

        return f[-1]
''',
    call=f'Solution().lengthOfLongestSubsequence({NUMS}, {TARGET})',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前数 v）', h=170, cell=90,
             color=lambda S, i, x: 'blue' if 'v' in S and x == S['v'] else None),
        dict(type='array', var='f', label='f[j]：和恰好为 j 时最多选几个数（-1 = 凑不出）', h=230, cell=90,
             pointers={'index': 'pink'},
             color=lambda S, i, x: ('green' if i == S.get('index') and S.get('_line', 0) == 9 else
                                    'cyan' if 'index' in S and 'v' in S and i == S['index'] - S['v'] and S.get('_line', 0) in (8, 9) else None)),
        dict(type='text', h=60, size=26,
             fn=lambda S: (f"f[{S['index']}] = max(f[{S['index']}], f[{S['index']-S['v']}] + 1)，f[{S['index']-S['v']}] = {S['f'][S['index']-S['v']]}"
                           if 'index' in S and 'v' in S and S['index'] >= S['v'] else '`f[index]`：选 `v` 则由 `f[index-v] + 1` 转移')),
    ],
    watch=[('v', 'v', 'blue'), ('index', 'index', 'pink'), ('f[index-v]', 'f[index-v]', 'cyan'), ('f[-1]', 'f[-1]', 'green')],
    max_steps=70,
    captions={
        'f = [-1]': '`f[j]` = 和恰为 `j` 时最多选几个数；`-1` 表示凑不出',
        'f[0] = 0': '和为 0：什么都不选，个数 0',
        'for v in nums': lambda S, B, r: ('所有数都处理完了' if B.get('v') == S.v and S.v == S.nums[-1] else f'处理数 `v = {S.v}`：只能用一次'),
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：==倒序==遍历，`f[{S.index - S.v}]` 还没被本轮改过，所以 `v` 只会选一次'
                                               if 'index' in S and S.index != B.get('index') and S.index == S.target
                                               else (f'`index = {S.index}`' if 'index' in S and S.index != B.get('index') else '这个数处理完')),
        'if f[index - v] >= 0': lambda S, B, r: (
            f'`f[{S.index - S.v}] = {S.f[S.index - S.v]}` < 0 → 凑不出和 `{S.index - S.v}`，不能转移' if S.f[S.index - S.v] < 0
            else (f'`f[{S.index - S.v}] + 1 = {S.f[S.index - S.v] + 1}` > `f[{S.index}] = {S.f[S.index]}` → 选 `v` 更多，更新' if S.f[S.index] < S.f[S.index - S.v] + 1
                  else f'`f[{S.index - S.v}] + 1 = {S.f[S.index - S.v] + 1}` ≤ `f[{S.index}] = {S.f[S.index]}` → 不选更好，不变')),
        'f[index] = f[index - v] + 1': '`f[{index}] = {f[index]}`',
        'return f[-1]': lambda S, B, r: (f'`f[{S.target}] = {r}`：和恰为 target 的最长子序列长度' if r >= 0 else '`f[-1] = -1`，凑不出 target'),
    },
    cards=dict(
        one_liner='标准背包：f[j] 记最多选几个数，index 倒序',
        complexity='时间 `O(n·target)`，空间 `O(target)`',
        problem=['给整数数组 `nums` 和 `target`，求和为 `target` 的子序列的==最大长度==，凑不出返回 `-1`',
                 '示例：`[4,1,3,2,1,5]`，`target = 7` → `4`',
                 '本视频：`[1,2,1,3]`，`target = 4` → `3`（`1+2+1`）'],
        quote='非常标准的背包问题。令f[i][j]表示前i个数中选取若干个数使得和为j时最多可以选多少个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['二维 `f[i][j]`：前 `i` 个数凑出和 `j` 最多选几个',
              '转移：`f[i][j] = max(f[i][j], f[i-1][j-nums[i]] + 1)`',
              '倒序遍历 `j`，就能把 `i` 这一维滚掉；`f[index-v] >= 0` 才表示凑得出',
              '`j` 的范围只需 `v` 到 `target`'],
        summary=['时间 `O(n·target)`，空间 `O(target)`',
                 '易错：`index` 必须倒序，否则同一个数被重复选（变完全背包）',
                 '易错：用 `-1` 表示凑不出，转移前要先判 `f[index-v] >= 0`',
                 '对比灵神：灵神用 `-inf` 表示不合法再 `max`，yiduobo 用 `-1` 加判断；灵神另有记忆化搜索与时间优化'],
    ),
)
