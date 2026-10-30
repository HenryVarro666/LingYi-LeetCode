def _fmt(v):
    return '–' if v is None else str(v)


def _cur(S, p, v):
    return 'yellow' if S.get('j') == p and S.get('_line', 0) >= 21 and S.get('_line') <= 28 else None


def _txt(S):
    if 'sign' not in S or 'mul' not in S:
        return '`f[j]` = 选了 `j` 个子数组的最大能量；`g[j]` = 「再接第 j+1 个子数组」的最佳起点值'
    j = S['j']
    s = S['s'][S['i']] if 's' in S and len(S['s']) > S['i'] else '?'
    return (f"j={j}：符号 `{'+' if S['sign'] > 0 else '−'}`，系数 `mul = {S['mul']}`　"
            f"`s[i]·sign·mul = {s}×{S['sign']}×{S['mul']}` = ==`{S['p']}`==" if 'p' in S else f"j={j}")


CONFIG = dict(
    num=3077, title='K 个不相交子数组的最大能量值', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前缀和 + 滚动 DP（f 与最优起点 g）',
    tags=['灵神题单·动态规划', '难度分 2557'],
    code='''
class Solution(object):
    def maximumStrength(self, nums, k):

        n = len(nums)
        f = [None] * (k + 1)
        f[0] = 0
        g = [None] * (k + 1)
        g[0] = 0

        s = [nums[0]]
        for v in nums[1:]:
            s.append(s[-1] + v)
        
        for i in range(n):
            for j in range(min(i + 1, k), 0, -1):
                if j % 2 == 1:
                    sign = 1
                else:
                    sign = -1
                mul = k - j + 1
                p = s[i] * sign * mul
                q = s[i] * sign * (mul - 1)

                v = g[j - 1] + p
                if f[j] is None or f[j] < v:
                    f[j] = v
                if g[j] is None or g[j] < f[j] + q:
                    g[j] = f[j] + q

            g[0] = max(g[0], -s[i] * mul)

        return f[-1]
''',
    call='Solution().maximumStrength([1,2,-1,3], 3)',
    expect=14,
    skip=['f = [None]', 'g = [None]', 'f[0] = 0', 'g[0] = 0', 's = [nums[0]]', 'for v in nums', 's.append',
          'if j % 2', 'sign = ', 'mul = ', 'q = ', 'for j in range', 'p = s[i]'],
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 第 i 个数）', h=150, cell=80,
             color=lambda S, p, v: 'blue' if S.get('i') == p else None),
        dict(type='array', var='f', label='f[j]：选 j 个子数组的最大能量（• = 还没有）', h=160, cell=84, fmt=_fmt, color=_cur),
        dict(type='array', var='g', label='g[j]：f[p][j] − s[p]·系数 的最大值（下一段的最优起点）', h=160, cell=84, fmt=_fmt, color=_cur),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('p', 'p', 'orange'), ('q', 'q', 'purple'), ('v', 'v', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'for i in range(n)': lambda S, B, r: ('所有数都处理完了' if 'i' in B and B.i == S.i else f'处理 `nums[{S.i}] = {S.nums[S.i]}`，前缀和 `s[{S.i}] = {S.s[S.i]}`'),
        'v = g[j - 1]': '`j = {j}`（倒序）：`p = s[{i}]·sign·mul` = `{s[i]}×{sign}×{mul}` = =={p}==；以 `nums[{i}]` 结尾作第 `{j}` 段：`v = g[{j-1}] + p` = `{B.g[j-1]} + {p}` = =={v}==',
        'if f[j] is None': lambda S, B, r: (f'`f[{S.j}]` 还没有值 → 直接用 `v`' if S.f[S.j] is None
                                            else f'`f[{S.j}] = {S.f[S.j]}` 对比 `v = {S.v}`：' + ('==v 更大，要更新==' if S.f[S.j] < S.v else '不用更新')),
        'f[j] = v': '`f[{j}]` = =={f[j]}==',
        'if g[j] is None': lambda S, B, r: (f'`g[{S.j}]` 还没有值 → 直接用 `f[j]+q`' if S.g[S.j] is None
                                            else f'`g[{S.j}] = {S.g[S.j]}` 对比 `f[j]+q = {S.f[S.j]+S.q}`：' + ('==更大，更新==' if S.g[S.j] < S.f[S.j] + S.q else '不用更新')),
        'g[j] = f[j] + q': '`g[{j}] = f[{j}] + q` = `{f[j]} + {q}` = =={g[j]}==：以后段的第 `{j+1}` 个子数组可从这里接',
        'g[0] = max': '`j` 都算完（`mul` 停在 `k`）：`g[0] = max(g[0], −s[i]·mul)` = ==`{g[0]}`==：第 1 段可以从任意位置开始（前面一个都没选）',
        'return f[-1]': '`f[k]` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='把「枚举上一段的终点」压成数组 g，每个 j 一次 O(1)',
        complexity='时间 `O(nk)`，空间 `O(n + k)`',
        problem=['选 `k`（奇数）个不相交子数组，第 `j` 段的和乘 `(−1)^(j+1)·(k−j+1)`，求总和最大',
                 '示例：`[1,2,3,-1,2], k = 3` → `22`',
                 '本视频：`[1,2,-1,3], k = 3`'],
        quote='朴素的动态规划的状态表示是O(nk)的，转移时需要枚举最后这一段的起点，最终的时间复杂度为O(n^2 * k)，必须进行优化。……使用一个数组g记录最优的p。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素：`f[i][j] = max(f[i-1][j], f[p][j-1] + (s[i]-s[p])·系数)`，要枚举 `p`',
              '拆括号：与 `p` 有关的部分 `f[p][j-1] − s[p]·系数` 记成 `g[j-1]`',
              '`g[j]` 用的系数是 `k−j`（比 f 少 1），符号改写成 `+`；去掉 `i` 维，`j` 倒序防覆盖'],
        summary=['时间 `O(nk)`，空间 `O(n + k)`（含前缀和）',
                 '易错：`g` 的系数是 `k−j` 不是 `k−j+1`；`j` 要==倒序==，否则 `f[j-1]` 被本轮覆盖',
                 '`g[0]` 单独更新：第 1 段可从任意位置开始',
                 '对比灵神：灵神用 `f[i][j]` 二维表并用 `mx` 边扫边维护；这里把最优起点存进数组 `g`'],
    ),
)
