NUMS = [-3, 2, -2, -1, 4, -2, 3]
PRE = [0]
for _v in NUMS:
    PRE.append(PRE[-1] + _v)


def _idx(S):
    """当前处理到 nums 的哪个下标（用 x 和前缀和 s 反推）"""
    x, s, ln = S.get('x'), S.get('s'), S.get('_line', 0)
    if x is None or s is None or ln < 6 or ln > 12:
        return None
    for i, v in enumerate(NUMS):
        if v == x and ((ln == 6 and PRE[i] == s) or (ln >= 7 and PRE[i + 1] == s)):
            return i
    return None


_PTR = lambda S: _idx(S)  # noqa: E731


def _col(S, i, v):
    k = _idx(S)
    if k is None:
        return None
    if i == k:
        return 'blue'
    return 'pink' if (v < 0 and i < k and False) else None


def _dim(S, i, v):
    k = _idx(S)
    return k is not None and i > k


def _mapvar(S):
    d = S.get('del_min_s')
    return None if d is None else {k: v for k, v in d.items()}


def _fm(S):
    ln = S.get('_line', 0)
    if 'all_min' not in S or _idx(S) is None:
        return '右端点 `j` 的最佳答案 = `s[j] − allMin`，`allMin` = 最小的「左端 + 被删的数」'
    if ln in (11, 12):
        return f"`all_min` = {S['all_min']}：删任何一个负数时，左端前缀和最小能到多少；`non_del_min_s` = {S['non_del_min_s']}"
    return f"`s − all_min` = `{S['s']} − ({S['all_min']})` = =={S['s'] - S['all_min']}==；`ans` = {S['ans']}"


def _c_ans(S, B, r):
    v = S.s - S.all_min
    return f'以当前位置结尾的最大子数组和 = `s − all_min` = `{S.s} − ({S.all_min})` = =={v}==，`ans = max({B.ans}, {v})` = {S.ans}'


def _c_del(S, B, r):
    x = S.x
    old = B.del_min_s.get(x, 0) if B.get('del_min_s') else 0
    nd = S.non_del_min_s_before if False else B.non_del_min_s
    keep = old <= nd
    how = (f'已经有 `{x}` 被删过：接着上一个 `{x}` 的最优（`{old}`）更小' if keep and x in (B.get('del_min_s') or {})
           else f'从「没删过的最小前缀和 `{nd}`」重新开始')
    return (f'`x = {x}` < 0，值得删。删掉它后左端「`s[i] + k·x`」最小是多少？`min({old}, {nd}) + ({x})` = =={S.del_min_s[x]}==（{how}）')


CONFIG = dict(
    num=3410, title='删除所有值为某个元素后的最大子数组和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 · 枚举右维护左',
    tags=['灵神题单·动态规划', '难度分 2844'],
    code='''
class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        ans = -inf
        s = non_del_min_s = all_min = 0
        del_min_s = defaultdict(int)
        for x in nums:
            s += x
            ans = max(ans, s - all_min)
            if x < 0:
                del_min_s[x] = min(del_min_s[x], non_del_min_s) + x
                all_min = min(all_min, del_min_s[x])
                non_del_min_s = min(non_del_min_s, s)
        return ans
''',
    call=f'Solution().maxSubarraySum({NUMS})',
    expect=8,
    skip=['for x in nums', 'if x < 0'],
    views=[
        dict(type='array', var=lambda S: NUMS, label='nums（蓝 = 当前的 x，灰 = 还没扫到）', h=230, cell=84,
             pointers={_PTR: 'blue'}, pointer_labels={_PTR: 'x'},
             color=_col, dim=_dim),
        dict(type='map', var=_mapvar, label='del_min_s[x]：删掉 x 时，左端 s[i] + k·x 的最小值', h=190,
             fmt=lambda k, v: f'删 {k}: {v}'),
        dict(type='text', fn=_fm, size=24, h=110),
    ],
    watch=[('s', 's', 'cyan'), ('non_del_min_s', 'non_del_min_s', 'blue'), ('all_min', 'all_min', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = -inf': '子数组非空，所以 `ans` 先设为负无穷',
        's = non_del_min_s': '`s` 是前缀和（`s[0] = 0`）；`non_del_min_s` 是「没删任何数」时左端最小前缀和；`all_min` 是「删某个数」后的最小左端值',
        'del_min_s = defaultdict': '`del_min_s[x]`：删除负数 `x` 后，左端 `s[i] + k·x` 的最小值（`k` 是区间里 `x` 的个数）',
        's += x': lambda S, B, r: f'`s += {S.x}` → 前缀和 `s = {S.s}`',
        'ans = max': _c_ans,
        'del_min_s[x] = min': _c_del,
        'all_min = min': '`all_min = min({B.all_min}, {del_min_s[x]})` = =={all_min}==：删哪个负数、左端怎么选，总的最小值',
        'non_del_min_s = min': '`non_del_min_s` 也要把当前前缀和纳入：`min({B.non_del_min_s}, {s})` = {non_del_min_s}（后面新出现的负数从这里开始算）',
        'return ans': '最大子数组和 = ==`{ans}`==',
    },
    cards=dict(
        one_liner='删掉 x，等价于把区间里的 x 全部「抵消」：s[j] − (s[i] + k·x)',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选一个数 `X`，==删掉所有等于 X 的元素==（至多一次，剩下的数组不能为空）',
                 '求删完之后，所有可能数组里的最大子数组和',
                 '示例：`[-3,2,-2,-1,3,-2,3]` → `7`（删 `-2`）；本视频：`[-3,2,-2,-1,4,-2,3]` → `8`'],
        quote='枚举 j，那么 s[i] + k·x 越小，答案越大。所以我们需要在枚举 j 的过程中，维护 s[i] + k·x 的最小值，记作 delMinS[x]。',
        quote_src='—— 灵茶山艾府题解（方法三）',
        idea=['子数组 `[i, j)` 里有 `k` 个 `x` 时，删掉后的和 = `s[j] − s[i] − k·x` = `s[j] − (s[i] + k·x)`',
              '==枚举右端 j，维护左边 `s[i] + k·x` 的最小值==：每个负数 `x` 一份 `del_min_s[x]`',
              '`all_min` 是所有 `del_min_s` 与 0 的最小值，`s − all_min` 就是以 j 结尾的最优答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '只有负数才值得删；先算 `s − all_min` 再更新 `all_min`，保证子数组非空',
                 '全是负数时 `all_min` 不会让区间为空，`ans` 退化成最大的单个数',
                 '题解另有线段树（O(n log n)）和前后缀分解两种写法，本视频演示方法三',
                 '同类题：53 最大子数组和（本题是它的「删数」版本）'],
    ),
)
