def _fmt(v):
    return '-inf' if v == float('-inf') else str(v)


def _formula(S):
    if S.get('_line') not in (9, 10) or 'tmp' not in S or 'y' not in S:
        return '`f[j]`：`nums1` 已处理部分与 `nums2` 前 `j` 个，选两个等长非空子序列的最大点积（-inf = 无解）'
    x, y, pre, tmp, left = S['x'], S['y'], S['pre'], S['tmp'], S['f'][S['j']]
    if S['_line'] == 10:
        return f'`pre` ← 旧的 `f[{S["j"] + 1}]` = =={_fmt(tmp)}==，留给下一格当「左上角」'
    take = max(pre, 0) + x * y
    return (f'选：`max({_fmt(pre)}, 0) + {x}×{y}` = {_fmt(take)}　不选 x：{_fmt(tmp)}　不选 y：{_fmt(left)}')


def _xcolor(S, i, v):
    return 'blue' if 'x' in S and v == S['x'] else None


def _ycolor(S, i, v):
    return 'pink' if 'y' in S and i == S.get('j') else None


CONFIG = dict(
    num=1458, title='两个子序列的最大点积', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='LCS 型 DP · 空间优化为一维',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1824'],
    code='''
class Solution:
    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
        m = len(nums2)
        f = [-inf] * (m + 1)
        for x in nums1:
            pre = f[0]
            for j, y in enumerate(nums2):
                tmp = f[j + 1]
                f[j + 1] = max(max(pre, 0) + x * y, f[j + 1], f[j])
                pre = tmp
        return f[m]
''',
    call='Solution().maxDotProduct([2, 1, -2], [3, 0, -6])',
    expect=18,
    views=[
        dict(type='array', var='nums1', label='nums1（蓝 = 当前 x）', h=150, cell=80, color=_xcolor),
        dict(type='array', var='nums2', label='nums2（粉 = 当前 y）', h=150, cell=80, color=_ycolor),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var='f', label='f[j]（下标 0 = nums2 为空，恒为 -inf）', h=190, cell=96, fmt=_fmt,
             pointers={'j + 1': 'blue'},
             color=lambda S, i, v: 'yellow' if S.get('_line') == 9 and i == S.get('j', -9) + 1 else None),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('j', 'j', 'cyan'), ('pre', 'pre', 'yellow'), ('tmp', 'tmp', 'orange')],
    captions={
        'm = len': '`m = {m}`，`f` 长 `m + 1`，让「nums2 为空」也有一格',
        'f = [-inf]': '`-inf` 表示不合法：子序列必须==非空==，所以没选任何元素时不能当作 0',
        'for x in nums1': lambda S, B, r: (f'`nums1` 的下一个数 `x = {S.x}`：`f` 现在记着「不含 x」的结果' if S.x != B.get('x') or 'j' not in B or B.get('j') != S.get('j') else '`nums1` 都处理完了'),
        'pre = f[0]': '`pre = f[0]` = =={f[0]}==：它是 `f[i][j]` 的左上角 `f[i-1][j-1]`，一维数组里要手动保存',
        'for j, y in enumerate': lambda S, B, r: (f'`j = {S.j}`，配对 `x = {S.x}` 与 `y = {S.y}`' if S.j != B.get('j') or S.get('y') != B.get('y') else '这一行（一个 x）算完'),
        'tmp = f[j + 1]': '先把旧的 `f[{j + 1}]` = {tmp} 存进 `tmp`：马上要被覆盖，下一格还要当左上角',
        'f[j + 1] = max': '选 `x·y` 接在 `max(pre, 0)` 后 = {max(pre, 0) + x * y}；不选 x = {tmp}；不选 y = {f[j]} → 取最大 =={f[j + 1]}==',
        'pre = tmp': '`pre = tmp` = {pre}：下一格的左上角',
        'return f[m]': '`f[{m}]` = =={ret}==：两个数组都用完时的最大点积',
    },
    cards=dict(
        one_liner='选 a[i]·b[j] 接前面（前面为负就不接），或各丢一个',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['两数组各选一个==长度相同的非空子序列==，求对应位置乘积之和的最大值',
                 '示例：`[2,1,-2,5]` 与 `[3,0,-6]` → `18`（`2×3 + (-2)×(-6)`）',
                 '本视频：`[2,1,-2]` 与 `[3,0,-6]` → `18`'],
        quote='选 a[i] 和 b[j]，且前面不再选数字；或前面还要选数字。前两种情况可以合并为：max(dfs(i-1,j-1), 0) + a[i]·b[j]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用「选或不选」：同时选 `a[i]`、`b[j]`，或丢掉其中一个',
              '前面的最大点积若为负，宁可不接：`max(f[i-1][j-1], 0)`',
              '非空：边界用 `-inf` 表示「没有元素可选」，不能当 0',
              '`f[i+1][j+1]` 只依赖上一行，所以压成一维，`pre` 保存左上角'],
        summary=['时间 `O(nm)`，空间 `O(m)`',
                 '易错：初始值是 `-inf` 而不是 0，否则会选出空子序列',
                 '易错：`pre` 必须在 `f[j+1]` 被覆盖前用 `tmp` 保存',
                 '题解前面还有记忆化搜索和二维递推，本视频是最后的空间优化写法',
                 '同类题：1143. 最长公共子序列'],
    ),
)
