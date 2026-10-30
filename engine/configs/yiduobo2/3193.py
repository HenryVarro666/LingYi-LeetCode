N, REQS = 3, [[2, 2], [0, 0]]


def _fcolor(S, j, v):
    line, cj = S.get('_line'), S.get('j')
    if cj is None or 'start' not in S:
        return None
    if line in (20, 21, 22, 24, 26) and j == cj:
        return 'yellow'
    return None


def _scolor(S, j, v):
    line, cj, i = S.get('_line'), S.get('j'), S.get('i')
    if cj is None or i is None:
        return None
    if line == 22 and j == cj:
        return 'blue'
    if line == 24 and j in (cj, cj - i):
        return 'blue' if j == cj else 'pink'
    if line == 30 and j == cj:
        return 'yellow'
    return None


def _info(S):
    i, line = S.get('i'), S.get('_line', 0)
    if i is None:
        return '`f[j]`：i 个数的排列中，逆序对恰好为 j 的个数；`s` 是 `f` 的==前缀和=='
    if line >= 28:
        return f'用新的 `f` 重新算前缀和 `s`：`s[j] = s[j − 1] + f[j]`（供下一轮 i = {i + 1} 使用）'
    if 'start' not in S:
        return f'第 `i = {i}` 轮：从 i−1 个数推 i 个数'
    st, en = S['start'], S['end']
    rng = f'只算 `j = {st}`（有要求）' if st == en else f'`j` 取 `[{st}, {en}]`'
    return f'`i = {i}` 个数，{rng}；`f[j] = s[j]`（j < i）或 `s[j] − s[j−i]`'


CONFIG = dict(
    num=3193, title='统计逆序对的数目', difficulty='Hard', category='多维动态规划',
    author='yiduobo', technique='DP · 前缀和优化 + 一维滚动',
    tags=['字节30天'],
    code='''
class Solution(object):
    def numberOfPermutations(self, n, requirements):
        req_dict = {}
        for end, cnt in requirements:
            req_dict[end] = cnt
            if end == 0 and cnt != 0:
                return 0

        mod = 10 ** 9 + 7
        f = [0] * (req_dict[n - 1] + 1)
        f[0] = 1
        s = [1] * (req_dict[n - 1] + 1)
        for i in range(2, n + 1):
            if i - 1 in req_dict:
                start = end = req_dict[i - 1]
            else:
                start, end = 0, req_dict[n - 1]

            for j in range(req_dict[n - 1] + 1):
                if start <= j <= end:
                    if j <= i - 1:
                        f[j] = s[j]
                    else:
                        f[j] = (s[j] - s[j - i] + mod) % mod
                else:
                    f[j] = 0

            s[0] = f[0]
            for j in range(1, req_dict[n - 1] + 1):
                s[j] = (s[j - 1] + f[j]) % mod

        return f[-1]
''',
    call=f'Solution().numberOfPermutations({N}, {REQS})',
    expect=2,
    skip=['for j in range', 'mod = 10 ** 9 + 7'],
    views=[
        dict(type='text', h=90, size=24, lines=2, fn=_info),
        dict(type='map', var='req_dict', label='req_dict（end → cnt：前 end+1 个数的逆序对要求）', fmt=lambda k, v: f'{k} → {v}', h=100),
        dict(type='array', var='f', label='f[j]（黄 = 正在算）', cell=100, h=190, pointers={'j': 'yellow'}, color=_fcolor),
        dict(type='array', var='s', label='s[j] = f[0] + … + f[j]（蓝/粉 = 用来求区间和）', cell=100, h=190, color=_scolor),
    ],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'yellow'), ('start', 'start'), ('end', 'end')],
    captions={
        'req_dict = {}': '`req_dict`：`end → cnt`',
        'for end, cnt in requirements': lambda S, B, ret: (f'要求：前 `{S.end + 1}` 个数恰好 `{S.cnt}` 个逆序对' if S.get('cnt') != B.get('cnt') or 'cnt' not in B
                                                           else '要求都记好了'),
        'req_dict[end] = cnt': '`req_dict[{end}] = {cnt}`',
        'if end == 0 and cnt != 0': lambda S, B, ret: ('只有一个数却要求有逆序对 → 无解' if S.end == 0 and S.cnt != 0
                                                       else '这条要求没有矛盾'),
        'f = [0] * (req_dict[n - 1] + 1)': '`f` 长度 = 最终要求的逆序对数 `+ 1` = `{len(f)}`',
        'f[0] = 1': '`i = 1`（只有一个数）：逆序对只能是 0 → `f = {f}`',
        's = [1] * (req_dict[n - 1] + 1)': '前缀和 `s[j] = f[0] + … + f[j]`，此时全是 1',
        'for i in range(2, n + 1)': lambda S, B, ret: (f'第 `i = {S.i}` 轮：由 `{S.i - 1}` 个数的结果推出 `{S.i}` 个数' if S.get('i') != B.get('i') or 'i' not in B
                                                       else '所有轮次结束'),
        'if i - 1 in req_dict': lambda S, B, ret: (f'`req_dict` 有 `{S.i - 1}`：前 `{S.i}` 个数==必须恰好== `{S.req_dict[S.i - 1]}` 个逆序对'
                                                   if S.i - 1 in S.req_dict else f'前 `{S.i}` 个数没有要求 → 所有 j 都要算'),
        'start = end = req_dict[i - 1]': '只算 `j = {start}`，其余置 0',
        'start, end = 0, req_dict[n - 1]': '`j` 取 `[0, {end}]`',
        'if start <= j <= end': lambda S, B, ret: (f'`j = {S.j}` 在 `[{S.start}, {S.end}]` 内 → 要算' if S.start <= S.j <= S.end
                                                   else f'`j = {S.j}` 不在 `[{S.start}, {S.end}]` 内 → 不满足要求，置 0'),
        'if j <= i - 1': lambda S, B, ret: (f'`j = {S.j} ≤ i − 1 = {S.i - 1}`：区间 `[0, j]` 不会越界' if S.j <= S.i - 1
                                            else f'`j = {S.j} > i − 1`：区间是 `[j − i + 1, j]`'),
        'f[j] = s[j]': lambda S, B, ret: f'`f[{S.j}] = s[{S.j}] = {S.f[S.j]}`：最后一个数和前面组成 `0..{S.j}` 个逆序对，求和',
        'f[j] = (s[j] - s[j - i]': lambda S, B, ret: f'`f[{S.j}] = s[{S.j}] − s[{S.j - S.i}] = {S.f[S.j]}`：前缀和相减得区间和',
        'f[j] = 0': '`f[{j}] = 0`',
        's[0] = f[0]': '重算前缀和：`s[0] = f[0] = {s[0]}`',
        's[j] = (s[j - 1] + f[j])': '`s[{j}] = s[{j - 1}] + f[{j}] = {s[j]}`',
        'return f[-1]': '`f[-1]` 就是 n 个数、逆序对为要求值的方案数：返回 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='看最后一个数放第几大，区间和用前缀和 O(1) 求出',
        complexity='时间 `O(n*max(cnt))`，空间 `O(max(cnt))`',
        problem=['求 `[0, 1, …, n−1]` 的排列 `perm` 的个数（模 `10^9+7`）',
                 '满足每个要求 `[end, cnt]`：`perm[0..end]` 中==恰好 cnt 个逆序对==',
                 '示例：`n = 3, requirements = [[2,2],[0,0]]` → `2`（`[2,0,1]`、`[1,2,0]`）'],
        quote='令f[i][j]表示由i个数构成，且有j组逆序对的排列的数量……如果选择这i个数中最大的数……f[i][j] += f[i - 1][j]。接下来，如果选择次大的数……f[i][j] += f[i - 1][j - 1]。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j] = f[i−1][j] + f[i−1][j−1] + … + f[i−1][max(0, j−i+1)]`',
              '这是区间和 → 前缀和 `s`：`j ≤ i−1` 时 `f = s[j]`，否则 `f = s[j] − s[j−i]`',
              '有要求的 i 只保留 `j = cnt`；`f` 只依赖上一轮的 `s` → 去掉 i 这一维'],
        result='`f = [0, 0, 2]` → 返回 `f[-1] = 2`',
        summary=['时间 `O(n*max(cnt))`，空间 `O(max(cnt))`',
                 '易错：`s[j] − s[j − i]` 取模后可能为负，原文 `+ mod` 再 `% mod`',
                 '易错：有要求的轮次，其余 `j` 必须置 0，否则会把不合法的方案带到下一轮',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神讲清记忆化 → 递推 → 前缀和优化的完整推导'],
    ),
)
