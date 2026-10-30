_I = lambda S: S['_inner'].get('i', -1)


def _rows(j, m):
    return [r for r in range(m) if j >> r & 1]


def _cell(S, r, c, v):
    d = S['_inner']
    if 'i' not in d or 'j' not in d or 'all_nums' not in S or d['i'] < 0:
        return None
    x = S['all_nums'][d['i']]
    if r in _rows(d['j'], len(S['grid'])):
        return 'green' if v == x and False else 'blue'
    if v == x:
        return 'yellow'
    return None


def _dim(S, r, c, v):
    d = S['_inner']
    return 'j' in d and r in _rows(d['j'], len(S['grid']))


def _fx(S):
    d = S['_inner']
    if 'j' not in d:
        return '`dfs(i, j)`：只在前 `i+1` 个数里选，==行集合 j 里的行不能再选=='
    m = len(S['grid'])
    rs = _rows(d['j'], m)
    if d['i'] < 0:
        return f'`dfs(-1, {d["j"]:0{m}b})` = 0：没有数可选了，已选行 `{rs}`'
    x = S['all_nums'][d['i']]
    return f'当前数 `x = {x}`，所在行 `{S["pos"][x]}`；已选行集合 `j = {d["j"]:0{m}b}`（行 {rs}）'


def _if(S, B, ret):
    d = S['_inner']
    k = d['k']
    if d['j'] >> k & 1:
        return f'第 `{k}` 行已经在 `j` 里选过数了 → 不能再选'
    return f'第 `{k}` 行还没选过 → ==可以选这一行的 {S["all_nums"][d["i"]]}=='


CONFIG = dict(
    num=3276, title='选择矩阵中单元格的最大得分', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='从大到小枚举数值 + 行集合状压记忆化',
    tags=['状压 DP', '其他状压 DP', '难度分 2403'],
    code='''
class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        pos = defaultdict(list)
        for i, row in enumerate(grid):
            for x in set(row):  # 去重
                pos[x].append(i)
        all_nums = sorted(pos)  # 下面从大到小递归

        @cache  # 缓存装饰器，避免重复计算 dfs 的结果（记忆化）
        def dfs(i: int, j: int) -> int:
            if i < 0:
                return 0
            res = 0  # 如果循环结束后 res > 0，就不再递归不选的情况
            for k in pos[all_nums[i]]:
                if (j >> k & 1) == 0:
                    res = max(res, dfs(i - 1, j | 1 << k) + all_nums[i])
            return res if res else dfs(i - 1, j)
        return dfs(len(all_nums) - 1, 0)
''',
    call='Solution().maxScore([[1,2,3],[4,3,2],[1,1,1]])',
    expect=8,
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前数值 x；蓝 = 已选过数的行）', h=240, cell=64,
             color=_cell, dim=_dim),
        dict(type='array', var='all_nums', label='all_nums（升序，从最后一个往前递归）', h=190, cell=64,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'}),
        dict(type='text', fn=_fx, size=24, h=70),
        dict(type='calls', h=200),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('j', lambda S: S['_inner'].get('j'), 'pink'),
           ('k', lambda S: S['_inner'].get('k'), 'yellow'), ('res', lambda S: S['_inner'].get('res'), 'green')],
    skip=['for k in pos', 'pos = defaultdict', 'for i, row in enumerate', 'for x in set', 'pos[x].append', '@cache'],
    captions={
        'all_nums = sorted': '把出现过的数去重后==升序排好==，递归时从最大的数往小处理 → `{all_nums}`',
        'def dfs': '`dfs(i, j)`：在 `all_nums[0..i]` 里选数，行集合 `j` 里的行不能再用',
        'if i < 0': lambda S, B, r: ('`i < 0`：没有数可选了 → ==递归边界==，返回 0' if S._inner.get('i', 0) < 0
                                     else f'`i = {S._inner["i"]}`，还有数可选 → 继续'),
        'res = 0': '`res = 0`：先假设这个数选不了；若能选，就==不用再考虑“不选”==',
        'if (j >> k & 1) == 0': _if,
        'res = max(': lambda S, B, r: (f'选第 `{S._inner["k"]}` 行的 `{S.all_nums[S._inner["i"]]}`：'
                                        f'`max({B._inner["res"]}, 后面最优 + {S.all_nums[S._inner["i"]]})` = =={S._inner["res"]}=='),
        'return res if res': lambda S, B, r: (f'`res = {S._inner["res"]} > 0`：这个数选得了，==不再算“不选”==，返回 {r}'
                                              if S._inner['res'] else f'`res = 0`：这个数的行都被占了 → 只能跳过它，`dfs(i-1, j)` = {r}'),
        'return dfs(len': '入口 `dfs({len(all_nums) - 1}, 0)`：从最大的数开始，一开始没选任何行',
    },
    max_steps=70,
    cards=dict(
        one_liner='从大到小选数，能选就一定选，行号用二进制集合记录',
        complexity='时间 `O(mn·2^m)`，空间 `O(mn + 2^m)`',
        problem=['矩阵 `grid` 里选一个或多个格子：==任意两个不同行，值互不相同==',
                 '得分是所选值之和，求最大得分',
                 '示例：`[[1,2,3],[4,3,2],[1,1,1]]` → `8`（选 1、3、4）'],
        quote='从大到小递归所有元素，如果当前元素可以选（有之前没选过的行），那么就==不用考虑不选的情况==了。',
        quote_src='—— 灵茶山艾府题解（二、记忆化搜索（优化））',
        idea=['按==值==枚举而不是按格子：值互不相同自然满足',
              '状态 `dfs(i, j)`：只看前 `i+1` 个数，已占用的行集合是 `j`',
              '最大值必选；往后只要还有空行能放，选一定不亏'],
        result='最大得分 8：选 4（第 1 行）、3（第 0 行）、1（第 2 行）',
        summary=['时间 `O(mn·2^m)`：状态 `O(k·2^m)`，每个状态枚举至多 `m` 行',
                 '易错：同一行相同的数要先 `set(row)` 去重；行号用 `j | 1 << k` 标记',
                 '优化前写法要同时算“选/不选”；这里能选就不用算不选',
                 '题解还给了递推、空间压缩和费用流写法',
                 '同类题：1434. 每个人戴不同帽子的方案数'],
    ),
)
