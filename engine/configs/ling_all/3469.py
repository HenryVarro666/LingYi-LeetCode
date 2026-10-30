NUMS = [6, 2, 8, 4, 5, 3]


def _ncol(S, k, v):
    if 'i' not in S:
        return None
    if 'j' in S and k == S['j'] and S.get('_line') in (8, 9):
        return 'blue'
    if k == S['i']:
        return 'pink'
    if k == S['i'] + 1:
        return 'purple'
    return None


def _fcol(S, k, v):
    if 'j' in S and k == S['j'] and S.get('_line') in (8, 9):
        return 'yellow'
    if 'i' in S and S.get('_line') in (8, 9) and k in (S['i'], S['i'] + 1):
        return 'cyan'
    return None


def _txt(S):
    if 'i' not in S or 'j' not in S or S.get('_line') not in (8, 9):
        return '`f[j]`：剩下 `nums[j]` 和后缀 `nums[i..]` 时的最小总成本（`j < i`）'
    i, j, nums = S['i'], S['j'], S['nums']
    a, b, c = nums[j], nums[i], nums[i + 1]
    return f'`a={a}` `b={b}` `c={c}`：去 bc 花 `{max(b, c)}`，去 ac 花 `{max(a, c)}`，去 ab 花 `{max(a, b)}`'


def _cap9(S, B, ret):
    i, j = S.i, S.j
    a, b, c = S.nums[j], S.nums[i], S.nums[i + 1]
    o, p, q = B.f[j], B.f[i], B.f[i + 1]
    x, y, z = o + max(b, c), p + max(a, c), q + max(a, b)
    return (f'三选一取最小：留 `a={a}`：`{o} + {max(b, c)} = {x}`；留 `b={b}`：`{p} + {max(a, c)} = {y}`；'
            f'留 `c={c}`：`{q} + {max(a, b)} = {z}` → `f[{j}]` = =={S.f[j]}==')


CONFIG = dict(
    num=3469, title='移除所有数组元素的最小代价', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='多维 DP · 1:1 翻译 + 空间优化',
    tags=['难度分 2112'],
    code='''
class Solution:
    def minCost(self, nums: List[int]) -> int:
        n = len(nums)
        f = nums.copy() if n % 2 else [max(x, nums[-1]) for x in nums]
        for i in range(n - 3 + n % 2, 0, -2):
            b, c = nums[i], nums[i + 1]
            for j in range(i):
                a = nums[j]
                f[j] = min(f[j] + max(b, c), f[i] + max(a, c), f[i + 1] + max(a, b))
        return f[0]
''',
    call=f'Solution().minCost({NUMS})',
    expect=16,
    views=[
        dict(type='text', size=26, h=80, fn=_txt),
        dict(type='array', var='nums', label='nums（蓝 = 留下的 a，粉 = b，紫 = c）', h=190, cell=100, color=_ncol),
        dict(type='array', var='f', label='f[j]（黄 = 正在算，青 = 依赖的 f[i]、f[i+1]）', h=190, cell=100, color=_fcol),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), ('a', 'a', 'blue'), ('b', 'b', 'pink'), ('c', 'c', 'purple')],
    captions={
        'n = len': '`n = {n}`',
        'f = nums.copy()': lambda S, B, r: (f'`n = {S.n}` 是奇数：最后会剩一个数，`f[j] = nums[j]`' if S.n % 2
                                            else f'`n = {S.n}` 是偶数：最后剩 `j` 和 `nums[n-1]` 两个，`f[j] = max(nums[j], nums[-1])`'),
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：剩下 `nums[j]` 和后缀 `nums[{S.i}..]`，每次拿走前三个里的两个，`i` 每次 `+2`，倒着算'
                                           if S.get('i') != B.get('i') else '所有 `i` 都处理完，`f[0]` 就是剩 `nums[0]` + 后缀 `[1..]` 的答案'),
        'b, c = nums': '`b = nums[{i}] = {b}`，`c = nums[{i + 1}] = {c}`：后缀最前面的两个数',
        'for j in range': lambda S, B, r: (f'`j` 枚举留下的那个下标（`j < i`）' if S.get('j') != B.get('j') else '`j` 都算完了，更新到下一个 `i`'),
        'a = nums[j]': '`a = nums[{j}] = {a}`：留在最前面的那个数',
        'f[j] = min': _cap9,
        'return f[0]': '答案 `f[0]`：一开始剩 `[0] + [1, n-1]`，最小总成本 ==`{ret}`==',
    },
    cards=dict(
        one_liner='至多留一个“落单”下标，其余是连续后缀，状态只要 (i, j)',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['每步从 `nums` 前三个里选两个移除，花费 ==较大值==',
                 '不足三个时一次移除全部，花费剩余的最大值',
                 '求移除所有元素的最小总成本；示例 `[6,2,8,4]` → `12`',
                 '本视频：`[6,2,8,4,5,3]`'],
        quote='可以发现，自始至终，至多有一个独立的下标，其他都是连续的后缀。为什么不能有两个独立的下标？',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `dfs(i, j)`：剩下 `[j] + [i, n-1]`，三种取法各去掉两个，留一个变成新的“落单”下标',
              '1:1 翻译成递推 `f[i][j]`，只依赖 `f[i+2]`',
              '所以去掉第一维，一个数组 `f[j]` 就够（`j` 从小到大，`f[i]`、`f[i+1]` 还是旧值）'],
        summary=['时间 `O(n^2)`，空间 `O(n)`',
                 '易错：`i` 的起点是 `n - 3 + n % 2`（奇偶不同），步长 `-2`',
                 '边界：奇数 `f[j] = nums[j]`；偶数 `f[j] = max(nums[j], nums[-1])`',
                 '题解还有记忆化 `dfs(i, j)`、二维递推 `f[i][j]` 和“值域”写法，这里用最后的空间优化版'],
    ),
)
