def _fmt(v):
    return '−∞' if v == -inf else str(v)


def _tcolor(S, i, j, v):
    if 'i' not in S or 'j' not in S or S.get('_line') not in (11, 12):
        return None
    if (i, j) == (S['i'], S['j']):
        return 'yellow'
    if (i, j) == (S['i'], S['j'] - 1):
        return 'blue'
    if (i, j) == (S['i'] - 1, S['j'] - 1) and S.get('_line') == 11:
        return 'green'
    return None


def _formula(S):
    if 'w' not in S or 'j' not in S:
        return '`f[i][j]` = 前 `j` 个数里选 `i` 个子数组的最大能量值；第 `i` 个子数组的权重 `w`'
    i, j, w = S['i'], S['j'], S['w']
    if S.get('_line') == 11:
        return (f"`mx` = max( `f[i-1][L] − s[L]·w` ) = ==`{S['mx']}`==　　"
                f"(`w` = {w})")
    if S.get('_line') == 12:
        return f"`f[{i}][{j}] = max(f[{i}][{j-1}], s[{j}]·w + mx)` = max({S['f'][i][j-1]}, {S['s'][j]}×{w} + {S['mx']})"
    return f"第 {i} 个子数组的权重 `w = (k−i+1)·(±1)` = ==`{w}`=="


CONFIG = dict(
    num=3077, title='K 个不相交子数组的最大能量值', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 前缀和 + 维护最大值',
    tags=['灵神题单·动态规划', '难度分 2557'],
    code='''
class Solution:
    def maximumStrength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        f = [[0] * (n + 1) for _ in range(k + 1)]
        for i in range(1, k + 1):
            f[i][i - 1] = mx = -inf
            w = (k - i + 1) * (1 if i % 2 else -1)
            # j 不能太小也不能太大，要给前面留 i-1 个数，后面留 k-i 个数
            for j in range(i, n - k + i + 1):
                mx = max(mx, f[i - 1][j - 1] - s[j - 1] * w)
                f[i][j] = max(f[i][j - 1], s[j] * w + mx)
        return f[k][n]
''',
    call='Solution().maximumStrength([1,2,3,-1,2], 3)',
    expect=22,
    views=[
        dict(type='array', var='nums', label='nums（粉 = nums[j-1]，当前右端点）', h=125, cell=76,
             color=lambda S, p, v: 'pink' if S.get('j') is not None and p == S['j'] - 1 and S.get('_line') in (11, 12) else None),
        dict(type='array', var='s', label='s（前缀和，蓝 = s[j]）', h=125, cell=76,
             color=lambda S, p, v: 'blue' if S.get('j') is not None and p == S['j'] and S.get('_line') in (11, 12) else None),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = f[i][j-1]，绿 = f[i-1][j-1]）', h=330, cell=66,
             rows=lambda S: [f'i={r}' for r in range(len(S['f']))], cols=lambda S: [f'j={c}' for c in range(len(S['f'][0]))],
             fmt=lambda v: _fmt(v), color=_tcolor),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('w', 'w', 'orange'), ('mx', 'mx', 'purple')],
    captions={
        'n = len': '`n = {n}`',
        's = list(accumulate': '前缀和 `s`：子数组 `nums[L..j-1]` 的和 = `s[j] − s[L]`',
        'f = [[0] * (n + 1)': '`f[i][j]`：前 `j` 个数里选 `i` 个子数组的最大能量值；`f[0][j] = 0`（一个都不选）',
        'for i in range(1, k + 1)': lambda S, B, r: ('`i` 从 1 到 k 都算完了' if 'i' in B and B.i == S.i else f'开始算选 `i = {S.i}` 个子数组'),
        'f[i][i - 1] = mx': '前 `{i-1}` 个数选不出 `{i}` 个子数组 → `f[{i}][{i-1}] = −∞`；`mx` 清成 −∞',
        'w = (k - i + 1)': '第 `{i}` 个子数组的符号 × 系数：`w = {w}`（奇数个为正，偶数个为负）',
        'for j in range(i, n - k + i + 1)': lambda S, B, r: (
            f'第 `{S.i}` 个子数组：`j` 走完范围，换下一层 `i`' if B.get('j') == S.j and B.get('i') == S.i else
            f'`j = {S.j}`：`j` 只在 `[{S.i}, {S.n-S.k+S.i}]` 内（前面留 `{S.i-1}` 个数、后面留 `{S.k-S.i}` 个数）'),
        'mx = max(mx': '`mx = max({B.mx}, f[{i-1}][{j-1}] − s[{j-1}]·w)`，新候选 = `{f[i-1][j-1]} − {s[j-1]}×({w})` → ==`{mx}`==（左端点 L 取遍 i-1..j-1 的最优）',
        'f[i][j] = max': '不选 `nums[{j-1}]`：`f[{i}][{j-1}] = {f[i][j-1]}`；选它作右端点：`s[{j}]·w + mx = ({s[j]*w}) + ({mx})`；取大 → ==`{f[i][j]}`==',
        'return f[k][n]': '选 `k` 个子数组、用前 `n` 个数：`f[{k}][{n}]` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='划分型 DP：枚举左端点的那层循环，用变量 mx 一路维护',
        complexity='时间 `O(k(n−k))`，空间 `O(nk)`（滚动数组可到 `O(n)`）',
        problem=['在 `nums` 中选 `k`（奇数）个不相交子数组，第 `i` 个子数组的和乘以 `(−1)^(i+1)·(k−i+1)`，求总和最大',
                 '子数组按从左到右编号，不必覆盖整个数组',
                 '示例：`nums = [1,2,3,-1,2], k = 3` → `22`'],
        quote='把 nums[j-1] 作为第 i 个子数组的最右元素，枚举第 i 个子数组最左元素的下标，记作 L，那么子数组元素和为 s[j] − s[L]……将上式变形……可以在枚举 j 计算 f[i][j] 的同时，用一个变量 mx 维护。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j] = max(f[i][j-1], f[i-1][L] + (s[j]-s[L])·w)`，直接枚举 `L` 是 `O(n^2 k)`',
              '拆括号：`s[j]·w + max(f[i-1][L] − s[L]·w)`，后半段只和 `L` 有关',
              '`j` 每右移一格，只需把新的 `L = j-1` 并入 `mx`，转移变成 `O(1)`'],
        summary=['时间 `O(k(n−k))`；`j` 的范围要给前后的子数组留位置',
                 '易错：`f[i][i-1] = −∞` 与 `mx` 初值 −∞ 要同时设；`w` 的符号随 `i` 奇偶变化',
                 '空间优化：去掉第一维，用变量 `pre` 记录 `f[i-1][j-1]`，空间 `O(n)`',
                 '同类划分型 DP：410、813、2911'],
    ),
)
