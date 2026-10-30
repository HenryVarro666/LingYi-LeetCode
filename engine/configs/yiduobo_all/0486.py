NUMS = [1, 5, 233, 7]


def _cell(S, r, c, v):
    f = S.get('f')
    if f is None or 'l' not in S or 'r' not in S:
        return None
    l, r_ = S['l'], S['r']
    if (r, c) == (l, r_):
        return 'yellow'
    if (r, c) in ((l + 1, r_), (l, r_ - 1)) and r <= c:
        return 'blue'
    return None


def _formula(S):
    if 'sum_list' not in S or 'l' not in S:
        return '`f[l][r]` = 先手在 `l..r` 这段最优策略下==最多能拿的分=='
    l, r = S['l'], S['r']
    sl = S['sum_list']
    s = sl[r] - (sl[l - 1] if l else 0)
    return f'`f[{l}][{r}]` = 区间和 `{s}` − `min(f[{l+1}][{r}], f[{l}][{r-1}])`' if r - l + 1 > 2 else f'区间 `[{l},{r}]` 只剩 ≤ 2 个数：先手拿大的'


CONFIG = dict(
    num=486, title='预测赢家', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间 DP · 先手最高得分 + 前缀和',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def PredictTheWinner(self, nums):

        if len(nums) <= 2:
            return True

        sum_list = [nums[0]]
        for num in nums[1:]:
            sum_list.append(sum_list[-1] + num)

        f = [[None] * len(nums) for _ in range(len(nums))]

        return self.dfs(0, len(nums) - 1, nums, f, sum_list) * 2 >= sum_list[-1]

    def dfs(self, l, r, nums, f, sum_list):
        if f[l][r] is not None:
            return f[l][r]

        if r - l + 1 <= 2:
            f[l][r] = max(nums[l], nums[r])
            return f[l][r]

        if l == 0:
            s = sum_list[r]
        else:
            s = sum_list[r] - sum_list[l - 1]

        f[l][r] = s - min(self.dfs(l + 1, r, nums, f, sum_list), self.dfs(l, r - 1, nums, f, sum_list))
        return f[l][r]
''',
    call=f'Solution().PredictTheWinner({NUMS!r})',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums', h=215, cell=80, pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f', label='f[l][r]（黄 = 正在算，蓝 = 它依赖的两格，点 = 还没算）', h=290, cell=76,
             rows=lambda S: list(range(len(NUMS))), cols=lambda S: list(range(len(NUMS))),
             fmt=lambda v: '' if v is None else str(v), color=_cell),
        dict(type='calls', h=240, hide=('nums', 'f', 'sum_list')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 's', ('sum_list', 'sum_list', 'cyan')],
    captions={
        'if len(nums) <= 2': '只有 1~2 个数，先手全拿走，必赢',
        'sum_list = [nums[0]]': '准备前缀和 `sum_list`：区间和 = 前缀和相减',
        'f = [[None]': '`f[l][r]` 记录先手在 `l..r` 最多拿多少分，`None` 表示还没算',
        'return self.dfs(0': '`f[0][{len(nums)-1}] × 2 = {f[0][len(nums)-1] * 2}` 与总和 `{sum_list[-1]}` 比：先手分 >= 一半 → =={ret}==',
        'if f[l][r] is not None': lambda S, B, r: (f'`f[{S.l}][{S.r}]` 已经算过 = {S.f[S.l][S.r]}，==直接返回=={""}' if S.f[S.l][S.r] is not None
                                                   else f'`f[{S.l}][{S.r}]` 还没算，往下算'),
        'if r - l + 1 <= 2': lambda S, B, r: (f'区间 `[{S.l},{S.r}]` 长度 {S.r-S.l+1} <= 2：先手直接拿较大的' if S.r - S.l + 1 <= 2
                                              else f'区间长度 {S.r-S.l+1} > 2，需要递归'),
        'f[l][r] = max(nums[l], nums[r])': '`f[{l}][{r}] = max({nums[l]}, {nums[r]})` = =={f[l][r]}=='
        ,
        'if l == 0': '区间和用前缀和算：`l == 0` 时直接取 `sum_list[r]`',
        24: '区间 `[{l},{r}]` 的和 `s = sum_list[{r}]` = =={s}==',
        26: '区间 `[{l},{r}]` 的和 `s = sum_list[{r}] − sum_list[{l-1}]` = =={s}==',
        'f[l][r] = s - min': '`f[l][r] = s − min(f[l+1][r], f[l][r-1])`：先手拿走区间和 `s`，扣掉对手较少的那份，==先递归算这两个子区间==',
        'return f[l][r]': '返回 `f[{l}][{r}] = {f[l][r]}`',
    },
    cards=dict(
        one_liner='区间和是固定的：先手拿到的 = 总和 − 后手能拿到的最少',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['两人轮流从数组==两端==取数，玩家 1 先手，各自累加',
                 '玩家 1 分数 `>=` 玩家 2 就返回 `true`',
                 '示例：`[1,5,2]` → `false`；本视频：`[1,5,233,7]` → `true`'],
        quote='f[i][j] = nums[i] + nums[i + 1] + ... + nums[j] - min(f[i + 1][j], f[i][j - 1])',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]` 是先手在 `i..j` 最多拿的分（不是分差）',
              '先手拿一端后，对手变先手，能拿 `f[i+1][j]` 或 `f[i][j-1]`；区间和固定，先手得其余',
              '对手会让自己最大，所以先手剩下的是 `s − min(...)`；最后 `2 × f[0][n-1] >= 总和` 即赢'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`；用 `None` 做未计算标记 + 记忆化递归',
                 '长度 <= 2 时先手拿较大的，是递归边界',
                 '前缀和 `sum_list` 求区间和，注意 `l == 0` 要单独处理',
                 '判定不是 `f >= 0`，而是 `f * 2 >= 总和`（f 是得分，不是分差）',
                 '对比灵神：他定义「分差」，转移直接相减；yiduobo 定义「得分」+ 前缀和'],
    ),
)
