def _i(S, k):
    return S['_inner'].get(k)


CONFIG = dict(
    num=3176, title='求出最长好子序列 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='O(1) 转移：last 哈希表 + best 前缀最大',
    tags=['灵神题单·动态规划', '难度分 1849'],
    code='''
class Solution(object):
    def maximumLength(self, nums, k):

        n = len(nums)

        last = {}
        best = [0] * (k + 1)

        for v in nums:
            last[v] = [0] * (k + 1)

        res = 0
        for i in range(len(nums)):
            for j in range(k, -1, -1):
                v = last[nums[i]][j] + 1
                if j > 0:
                    v = max(v, best[j - 1] + 1)
                
                last[nums[i]][j] = v
                best[j] = max(best[j], v)

        return best[-1]
''',
    call='Solution().maximumLength([1, 2, 1, 1], 1)',
    expect=3,
    skip=['for j in range', 'n = len', 'for v in nums', 'res = 0', 'if j > 0', 'last[v] = [0]'],
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前 nums[i]，作为子序列结尾）', cell=80, h=210, pointers={"_inner.get('i', -1)": 'blue'},
             pointer_labels={"_inner.get('i', -1)": 'i'},
             color=lambda S, i, v: 'yellow' if _i(S, 'i') == i else None),
        dict(type='map', var='last', label='last[x][j]：以值 x 结尾、最多 j 次不同的最长长度', h=170,
             fmt=lambda key, val: f'{key} → {val}'),
        dict(type='array', var='best', label='best[j]：所有结尾里，最多 j 次不同的最长长度（j = 0..k）', cell=90, h=170,
             pointers={"_inner.get('j', -1)": 'pink'}, pointer_labels={"_inner.get('j', -1)": 'j'},
             color=lambda S, i, v: 'green' if _i(S, 'j') == i and S.get('_line') == 20 else None),
    ],
    watch=[('i', "i", 'blue'), ('j', 'j', 'pink'), ('v', 'v', 'yellow')],
    captions={
        'last = {}': '`last[x][j]`：以数值 `x` 结尾、最多 `j` 对相邻不等的最长子序列长度（nums 里每个值先备一行全 0）',
        'best = [0]': '`best[j]`：不管以谁结尾、最多 `j` 对不等的最长长度，`j` 从 0 到 `k = {k}`',
        'for i in range': lambda S, B, r: (f'处理 `nums[{S.i}] = {S.nums[S.i]}`，把它接到某个子序列后面' if S.get('i') != B.get('i') else '所有元素处理完了'),
        'v = last[nums[i]][j] + 1': '情况 1：接在同值结尾后面，==不产生新的不等对==：`last[{nums[i]}][{j}] + 1` = =={v}=='  ,
        'v = max(v, best[j - 1] + 1)': '`j = {j} > 0`，还能花一次不等机会。情况 2：接在任意不同值结尾后面，用 `best[{j - 1}] + 1` = {best[j - 1] + 1}，取大 → =={v}==',
        'last[nums[i]][j] = v': '更新 `last[{nums[i]}][{j}]` = =={v}==',
        'best[j] = max': '`best[{j}]` = `max({B.best[j]}, {v})` = =={best[j]}==',
        'return best[-1]': '`best[k]`：最多 `k` 个不等对的最长好子序列 = =={ret}==',
    },
    cards=dict(
        one_liner='同值接 last，异值接 best[j-1]：转移降到 O(1)',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['给整数数组 `nums` 和非负整数 `k`',
                 '子序列里==相邻不相等的位置最多 k 个==，就是好子序列；求最长长度',
                 '示例：`nums = [1,2,1,1,3], k = 2` → `4`；本视频：`[1,2,1,1], k=1` → `3`'],
        quote='对于两个下标p < q，若nums[p] = nums[q]，那么f[p][j]必然小于f[q][j]……那么就应该选择nums[i]在0到i - 1中最后一次出现的下标对应的f值来更新f[i][j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素 DP：`f[i][j]` 枚举前一个结尾 `p`，`O(n^2 k)` 太慢',
              '同值转移：只需最近一次同值结尾 → 哈希表 `last[x][j]`',
              '异值转移：只需 `best[j-1]` 前缀最大；`j` 倒序遍历，滚动省掉 `i` 这一维'],
        summary=['时间 `O(nk)`，空间 `O(nk)`（`last` 最坏占 `O(nk)`）',
                 '`j` 要倒序：`best[j-1]` 必须还是处理 `nums[i]` 之前的值',
                 '`best[j-1]` 恰好以同值结尾时会多花一次机会，但同值情况已经覆盖，不影响答案',
                 '原文同时讲了 3177（数据更大），代码相同，这里用 3176 的小数据演示'],
    ),
)
