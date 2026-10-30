def _rows(S):
    return ['-'] + [str(v) for v in S['nums1']]


def _cols(S):
    return ['-'] + [str(v) for v in S['nums2']]


def _fc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is not None and j is not None and S.get('_line') == 10 and (r, c) == (i, j):
        return 'green'
    return None


def _nc(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') != 10:
        return None
    if (r, c) == (i + 1, j + 1):
        return 'yellow'
    if (r, c) in ((i, j + 1), (i + 1, j)):
        return 'blue'
    return None


def _done(S):
    try:
        return S['nf'][S['i'] + 1][S['j'] + 1] != float('-inf')
    except Exception:
        return False


def _formula(S):
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    if i is None or j is None or S.get('_line') != 10:
        return '`f` = 选 `k-1` 对时的结果；`nf[i+1][j+1]` = 选 `k` 对、用到 `nums1[:i+1]` 和 `nums2[:j+1]`'
    a, b = S['nums1'][i], S['nums2'][j]
    return (f'选这对：`f[{i}][{j}] + {a}×{b}` = {S["f"][i][j] + a * b}　'
            f'不选 nums1[{i}]：{S["nf"][i][j + 1]}　不选 nums2[{j}]：{S["nf"][i + 1][j]}')


CONFIG = dict(
    num=3836, title='恰好 K 个下标对的最大得分', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='LCS 型 DP · 多一维「还剩几对」',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1988'],
    code='''
class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], K: int) -> int:
        n, m = len(nums1), len(nums2)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        for k in range(1, K + 1):
            # 更快的写法见【Python3 写法二】
            nf = [[-inf] * (m + 1) for _ in range(n + 1)]
            for i in range(k - 1, n - (K - k)):  # 后面还要选 K-k 个下标对
                for j in range(k - 1, m - (K - k)):
                    nf[i + 1][j + 1] = max(nf[i][j + 1], nf[i + 1][j], f[i][j] + nums1[i] * nums2[j])
            f = nf
        return f[n][m]
''',
    call='Solution().maxScore([1, 3, 2], [4, 5, 1], 2)',
    expect=22,
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f：已选 k-1 对（绿 = f[i][j]）', h=250, cell=64, rows=_rows, cols=_cols, color=_fc),
        dict(type='table', var='nf', label='nf：正在算选 k 对（黄 = 正在算，蓝 = 不选的两种来源）', h=250, cell=64, rows=_rows, cols=_cols, color=_nc),
    ],
    watch=[('k', 'k', 'cyan'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('K', 'K', 'yellow')],
    captions={
        'n, m = len': '`n = {n}`，`m = {m}`',
        'f = [[0]': '`f` 表示「还要选 0 对」时的得分：点积为 0，所以全是 `0`',
        'for k in range': lambda S, B, r: (f'现在要选恰好 `{S.k}` 对：`nf` 由「选 `{S.k - 1}` 对」的 `f` 推出' if S.k != B.get('k') else '`K` 层都推完了'),
        'nf = [[-inf]': '`nf` 先全设为 `-inf`：没法选出恰好 `k` 对的状态不合法，`max` 不会取到它',
        'for i in range': lambda S, B, r: ('这一层的 `i` 都枚举完' if _done(S) else f'`i = {S.i}`：范围 `k-1 = {S.k - 1}` 到 `n-(K-k)-1 = {S.n - (S.K - S.k) - 1}`，后面要给 `{S.K - S.k}` 对留位置'),
        'for j in range': lambda S, B, r: ('这一行的 `j` 枚举完' if _done(S) else f'`j = {S.j}`：同理 `nums2` 后面要留 `{S.K - S.k}` 个位置'),
        'nf[i + 1][j + 1] = max': '三选一：选 `{nums1[i]}×{nums2[j]}` 加 `f[{i}][{j}]` = {f[i][j] + nums1[i] * nums2[j]}；不选 nums1[{i}] = {B.nf[i][j + 1]}；不选 nums2[{j}] = {B.nf[i + 1][j]} → =={nf[i + 1][j + 1]}==',
        'f = nf': '这一层算完：`nf` 变成下一层的 `f`（滚动数组，只留一层）',
        'return f[n][m]': '`f[{n}][{m}]` = =={ret}==：两个数组都用完、恰好选 `{K}` 对的最大得分',
    },
    cards=dict(
        one_liner='1458 题多一维：k = 还要选几对下标对',
        complexity='时间 `O(k(n-k)(m-k))`，空间 `O(nm)`',
        problem=['两数组各选==恰好 `k` 个==、下标严格递增的元素配对，得分是对应乘积之和',
                 '示例：`[1,3,2]`、`[4,5,1]`、`k=2` → `22`（`3×4 + 2×5`）',
                 '本视频即该示例；其实就是「长度恰为 k」的 1458 题'],
        quote='从 nums1 和 nums2 中各选一个长度恰好为 k 的子序列，计算 1458. 两个子序列的最大点积。……额外用一个参数 k 表示剩余需要选的下标对数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(k,i,j)`：前缀 `[0,i]`、`[0,j]` 中选恰好 `k` 对的最大点积',
              '「选或不选」：不选 `nums1[i]`、不选 `nums2[j]`，或两个都选并转移到 `k-1`',
              '递推 `f[k][i+1][j+1]`，`k` 只依赖 `k-1` → 滚动数组，只留两层',
              '`i`、`j` 从 `k-1` 开始、到 `n-(K-k)` 止：前后都留够位置，不会取到非法状态'],
        summary=['时间 `O(k(n-k)(m-k))`，空间 `O(nm)`',
                 '易错：无解状态用 `-inf` 而不是 0；`nf` 每层都要重新初始化为 `-inf`',
                 '易错：`i`、`j` 的循环上界要给后面留 `K-k` 对，下界 `k-1` 保证前面够选',
                 '题解前面还有记忆化搜索和三维递推，本视频是滚动数组版',
                 '同类题：1458. 两个子序列的最大点积（不限个数）'],
    ),
)
