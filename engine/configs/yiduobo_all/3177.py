NUMS, K = [1, 2, 1, 1, 3], 1


def _last_table(S):
    last = S.get('last') or {}
    return [list(v) for v in last.values()] or [[0] * (S['k'] + 1)]


def _cell(S, r, c, v):
    last = S.get('last') or {}
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 14:
        return None
    keys = list(last)
    if r < len(keys) and keys[r] == S['nums'][i]:
        return 'yellow' if c == j else 'blue'
    return None


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`last[x][j]` = 以值 x 结尾、恰好用掉 j 个不同对的最长长度；`best[j]` = 所有结尾里的最大值'
    x = S['nums'][i]
    if j == 0:
        return f'`v = last[{x}][0] + 1`：`j = 0` 不能有不同对，只能接在同值后面'
    return f'`v = max(last[{x}][{j}] + 1, best[{j - 1}] + 1)`：接同值，或接任意结尾并用掉一个不同对'


CONFIG = dict(
    num=3177, title='求出最长好子序列 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='DP · last 哈希表 + best 前缀最大',
    tags=['其他线性 DP', '难度分 2365'],
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
    call=f'Solution().maximumLength({NUMS!r}, {K})',
    expect=4,
    skip=['last[nums[i]][j] = v', 'n = len(nums)', 'last = {}', 'best = [0]', 'for v in nums', 'last[v] = [0]', 'res = 0', 'for j in range', 'for i in range', 'if j > 0'],
    max_steps=80,
    views=[
        dict(type='array', var='nums', label='nums（箭头 = 当前处理的 nums[i]）', h=210, cell=80, pointers={'i': 'blue'}),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='table', var=_last_table, label='last[x][j]（黄 = 正在更新，蓝 = 同一个值的整行）', h=250, cell=80,
             rows=lambda S: [f'x={key}' for key in (S.get('last') or {})] or [''], cols=lambda S: [f'j={t}' for t in range(S['k'] + 1)], color=_cell),
        dict(type='array', var='best', label='best[j]：所有结尾里 j 个不同对的最大长度', h=170, cell=80, pointers={'j': 'pink'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('v', 'v', 'green')],
    captions={
        'v = last[nums[i]][j] + 1': lambda S, B, r: f'`j = {S.j}`：接在同值 `{S.nums[S.i]}` 后面，不产生不同对：`last[{S.nums[S.i]}][{S.j}] + 1` = `{S.v}`',
        'if j > 0': lambda S, B, r: (f'`j = {S.j} > 0`：还允许一个不同对，可以考虑接在别的数后面' if S.j > 0 else '`j = 0`：不允许不同对，只能接同值（上一行已算）'),
        'v = max(v, best': lambda S, B, r: f'接在任意结尾后面要用掉一个不同对：`best[{S.j - 1}] + 1` = `{S.best[S.j - 1] + 1}`，与 `{B.v}` 取 `max` → ==`{S.v}`=='
                                           ,
        'best[j] = max': '`last[{nums[i]}][{j}] = {v}`（记下以 `{nums[i]}` 结尾的最长长度）；`best[{j}] = max({B.best[j]}, {v}) = {best[j]}`',
        'return best[-1]': '`best[k]` 就是至多 `k` 个不同对的最长好子序列：=={ret}==',
    },
    cards=dict(
        one_liner='同值接尾查 last，异值接尾查前缀最大 best',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['在 `nums` 中选子序列，相邻两数不相等的对数 ==不超过 k==，求最长长度',
                 '这里 `n ≤ 5000`，`k ≤ 50`，`O(n²k)` 太慢',
                 '示例：`nums=[1,2,1,1,3], k=2` → `4`；视频用 `k=1`，答案也是 `4`'],
        quote='对于两个下标p < q，若nums[p] = nums[q]，那么f[p][j]必然小于f[q][j]……选择nums[i]在0到i - 1中最后一次出现的下标对应的f值来更新f[i][j]。',
        quote_src='—— yiduobo 题解',
        idea=['朴素 DP：`f[i][j]` 枚举前一个结尾 `p`，同值转移 `f[p][j]+1`，异值转移 `f[p][j-1]+1`，`O(n²k)`',
              '同值：只需最近一次出现的结果，用哈希表 `last[x][j]` 保存',
              '异值：不关心结尾是谁，取前缀最大 `best[j-1]`；`j` 倒序枚举，省掉 `i` 这一维'],
        summary=['时间 `O(nk)`：每个 `(i, j)` 转移 `O(1)`',
                 '易错：`j` ==倒序==，否则 `best[j-1]` 已被本轮更新',
                 '`best[j-1]` 恰好来自同值时浪费一个不同对，但同值转移已覆盖，不影响答案',
                 '代码里 `last` 哈希表最坏占 `O(nk)` 空间'],
    ),
)
