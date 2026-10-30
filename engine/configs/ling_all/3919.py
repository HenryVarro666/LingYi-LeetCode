NUMS = [0, 2, 3, 9]
QS = [[3, 0], [1, 2], [2, 0]]
PI = "i if _line < 22 else None"
QI = "i if _line >= 22 else None"


def _q(S):
    if 'ans' not in S:
        return '先预处理两个前缀和，再用 `O(1)` 回答每个询问'
    l, r = S.get('l'), S.get('r')
    if l is None or S['_line'] < 22:
        return '预处理结束，开始回答询问'
    if l < r:
        return f'`{l} → {r}` 往右走：`sum_r[{r}] − sum_r[{l}]` = {S["sum_r"][r]} − {S["sum_r"][l]}'
    return f'`{l} → {r}` 往左走：`sum_l[{l}] − sum_l[{r}]` = {S["sum_l"][l]} − {S["sum_l"][r]}'


def _cl(S, B, r):
    i, n, a = S.i, S.n, S.nums
    if i < n - 1 and a[i] - a[i - 1] > a[i + 1] - a[i]:
        return f'往左走 `{i} → {i - 1}`：左差 {a[i] - a[i - 1]} > 右差 {a[i + 1] - a[i]}，`closest({i})` 是右边 → 方式二用不了'
    why = '已是最右端' if i == n - 1 else f'左差 {a[i] - a[i - 1]} <= 右差 {a[i + 1] - a[i]}'
    return f'往左走 `{i} → {i - 1}`：{why}，`closest({i})` 就是左边 → ==方式二花 1=='


def _cr(S, B, r):
    i, a = S.i, S.nums
    if i > 1 and a[i - 1] - a[i - 2] <= a[i] - a[i - 1]:
        return f'往右走 `{i - 1} → {i}`：`{i - 1}` 左差 {a[i - 1] - a[i - 2]} <= 右差 {a[i] - a[i - 1]}，`closest` 取左边（相等取小）→ 方式二用不了'
    return f'往右走 `{i - 1} → {i}`：`closest({i - 1})` 就是右边 `{i}` → ==方式二花 1=='


CONFIG = dict(
    num=3919, title='在下标间移动的最小代价', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='两个方向的前缀和',
    tags=['前缀和', '进阶', '难度分 1777'],
    code='''
class Solution:
    def minCost(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        n = len(nums)
        sum_l = [0] * n  # sum_l[i] 等于从 i 移动到 0 的代价和
        sum_r = [0] * n  # sum_r[i] 等于从 0 移动到 i 的代价和
        for i in range(1, n):
            # 往左走 i -> i-1
            if i < n - 1 and nums[i] - nums[i - 1] > nums[i + 1] - nums[i]:  # closest(i) = i+1
                cost = nums[i] - nums[i - 1]  # 只能用方式一往左走
            else:
                cost = 1
            sum_l[i] = sum_l[i - 1] + cost

            # 往右走 i-1 -> i
            if i > 1 and nums[i - 1] - nums[i - 2] <= nums[i] - nums[i - 1]:  # closest(i-1) = i-2
                cost = nums[i] - nums[i - 1]  # 只能用方式一往右走
            else:
                cost = 1
            sum_r[i] = sum_r[i - 1] + cost

        ans = [0] * len(queries)
        for i, (l, r) in enumerate(queries):
            if l < r:
                # cost(0 -> r) - cost(0 -> l) = cost(l -> r)
                ans[i] = sum_r[r] - sum_r[l]
            else:
                # cost(l -> 0) - cost(r -> 0) = cost(l -> r)
                ans[i] = sum_l[l] - sum_l[r]
        return ans
''',
    call=f'Solution().minCost({NUMS!r}, {QS!r})',
    expect=[4, 1, 3],
    views=[
        dict(type='table', var=lambda S: [S['nums'], S['sum_l'], S['sum_r']] if 'sum_r' in S else [S['nums']],
             rows=['nums', '左和', '右和'], cols=lambda S: list(range(len(S['nums']))), cell=96, h=330,
             label='左和 = sum_l（i 走到 0）；右和 = sum_r（0 走到 i）',
             color=lambda S, i, j, v: 'blue' if i > 0 and S.get('_line', 0) < 22 and j == S.get('i') else None),
        dict(type='text', h=70, size=28, fn=_q),
        dict(type='text', h=70, size=28, fn=lambda S: ('ans = `' + str(S['ans']) + '`') if 'ans' in S else ''),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('cost', 'cost', 'yellow')],
    captions={
        'sum_l = [0]': '`sum_l[i]`：一步步从 `i` 走回 `0` 的总代价。数组严格递增，一步步走和直接跳代价相同',
        'sum_r = [0]': '`sum_r[i]`：一步步从 `0` 走到 `i` 的总代价',
        'if i < n - 1 and nums': _cl,
        'cost = nums[i] - nums[i - 1]': '只能走方式一：代价 =={cost}==（差值）',
        'cost = 1': '`closest` 恰好指向目标，方式二只要 =={cost}==',
        'sum_l[i] = ': '`sum_l[{i}] = sum_l[{i - 1}] + {cost}` = =={sum_l[i]}==',
        'if i > 1 and nums': _cr,
        'sum_r[i] = ': '`sum_r[{i}] = sum_r[{i - 1}] + {cost}` = =={sum_r[i]}==',
        'ans = [0]': '预处理完毕，开始回答询问；每个询问 `O(1)`',
        'ans[i] = sum_r[r]': '右走：前缀和相减，`{sum_r[r]} − {sum_r[l]}` = =={ans[i]}==',
        'ans[i] = sum_l[l]': '左走：`{sum_l[l]} − {sum_l[r]}` = =={ans[i]}==',
    },
    cards=dict(
        one_liner='一步步走就好：能用「最近」就花 1，否则就是差值',
        complexity='时间 `O(n + q)`，空间 `O(n)`',
        problem=['`nums` 严格递增，可以直接跳（代价为差值），或跳到最近下标（代价 1）',
                 '每个询问 `[l, r]` 求从 `l` 到 `r` 的最小总代价',
                 '示例：`nums=[0,2,3,9]`，`queries=[[3,0],[1,2],[2,0]]` → `[4,1,3]`'],
        quote='能用方式二移动，就用方式二。此外，由于走回头路一定会包含往返的一段，这会花费多余的代价，所以我们不会走回头路。',
        quote_src='—— 灵茶山艾府题解',
        idea=['严格递增 → 直接跳 = 一步步走的总和，所以==一步步走==',
              '每一步贪心：能用方式二就用，代价 1；否则只能付差值',
              '正反各做一遍前缀和，询问用相减 `O(1)` 回答'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '往右走判断 `closest(i-1)` 用 `<=`（相等取较小下标，即左边）',
                 '往左走判断 `closest(i)` 用 `>`（相等时取左边，可以一步到）',
                 '`l == r` 时走 else 分支得 0'],
    ),
)
