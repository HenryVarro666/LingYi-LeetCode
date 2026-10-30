def _fmt_min(v):
    return '∞' if v == float('inf') else str(v)


CONFIG = dict(
    num=3445, title='奇偶频次间的最大差值 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举 x,y + 前缀和奇偶状态 + 滑窗',
    tags=['前缀和', '难度分 2694'],
    code='''
class Solution:
    def maxDifference(self, s: str, k: int) -> int:
        s = list(map(int, s))
        ans = -inf
        for x in range(5):
            for y in range(5):
                if y == x:
                    continue
                cur_s = [0] * 5
                pre_s = [0] * 5
                min_s = [[inf, inf], [inf, inf]]
                left = 0
                for i, v in enumerate(s):
                    cur_s[v] += 1
                    r = i + 1
                    while r - left >= k and cur_s[x] > pre_s[x] and cur_s[y] > pre_s[y]:
                        p, q = pre_s[x] & 1, pre_s[y] & 1
                        min_s[p][q] = min(min_s[p][q], pre_s[x] - pre_s[y])
                        pre_s[s[left]] += 1
                        left += 1
                    if r >= k:
                        ans = max(ans, cur_s[x] - cur_s[y] - min_s[cur_s[x] & 1 ^ 1][cur_s[y] & 1])
        return ans
''',
    call='Solution().maxDifference("0001100", 4)',
    expect=3,
    views=[
        dict(type='array', var='s', label='s', h=200, pointers={'i': 'blue', 'left': 'pink'}, window=('left', 'i'),
             dim=lambda S, i, v: 'left' in S and i < S['left']),
        dict(type='table', var='min_s', label='min_s[p][q]：左边 sum[l][x]−sum[l][y] 的最小值', h=190,
             rows=['p=0', 'p=1'], cols=['q=0', 'q=1'], cell=110,
             fmt=lambda v: '∞' if v == float('inf') else str(v)),
        dict(type='array', var='cur_s', label='cur_s：前缀 [0, r) 各数字的次数（绿 x 橙 y）', h=150, color=lambda S, i, v: 'green' if i == S.get('x') else 'orange' if i == S.get('y') else None),
        dict(type='array', var='pre_s', label='pre_s：前缀 [0, left) 各数字的次数', h=150, color=lambda S, i, v: 'green' if i == S.get('x') else 'orange' if i == S.get('y') else None),
    ],
    watch=['x', 'y', 'i', 'r', 'left', ('ans', 'ans', 'green')],
    max_steps=50,
    skip=['cur_s = [0]', 'pre_s = [0]', 'if y == x', 'continue', 'p, q =', 'r = i + 1', 'left += 1', 'if r >= k'],
    captions={
        's = list(map': '字符串转成数字列表，方便当下标用',
        'for x in range(5)': '枚举出现==奇数次==的数字 `x = {x}`',
        'for y in range(5)': '枚举出现==偶数次==的数字 `y = {y}`（`x = {x}`）',
        'min_s = ': '`min_s[p][q]`：左端点 `l` 里 `x`、`y` 前缀次数奇偶为 `p`、`q` 时，`sum[l][x]−sum[l][y]` 的最小值',
        'left = 0': '`left`：滑窗左边界，`[0, left-1]` 里的 `l` 都已合格并记进 `min_s`',
        'cur_s[v] += 1': '读入 `s[{i}] = {v}`，`cur_s[{v}] = {cur_s[v]}`；前缀长度 `r = {i+1}`',
        'r = i + 1': '当前前缀 `[0, r)`，`r = {r}`',
        'while r - left >= k': lambda S, B, r: (
            f'窗口 `r−left = {S.r - S.left}` ≥ `k = {S.k}`，且 x 的次数 `{S.cur_s[S.x]} > {S.pre_s[S.x]}`、y 的次数 `{S.cur_s[S.y]} > {S.pre_s[S.y]}` → ==left 合格=='
            if S.r - S.left >= S.k and S.cur_s[S.x] > S.pre_s[S.x] and S.cur_s[S.y] > S.pre_s[S.y]
            else f'`r−left = {S.r - S.left}`，`k = {S.k}`；x 差 `{S.cur_s[S.x] - S.pre_s[S.x]}`，y 差 `{S.cur_s[S.y] - S.pre_s[S.y]}` → 不满足，不动 left'),
        'min_s[p][q] = min': '`left = {left}` 的奇偶 `p={pre_s[x] & 1}, q={pre_s[y] & 1}`：`min_s[{pre_s[x] & 1}][{pre_s[y] & 1}]` = `min(…, {pre_s[x]} − {pre_s[y]})` = =={min_s[pre_s[x] & 1][pre_s[y] & 1]}==',
        'pre_s[s[left]] += 1': '这个 `left` 记完了，把 `s[{left}] = {s[left]}` 并入 `pre_s`',
        'left += 1': '`left → {left}`：窗口左边界右移',
        'if r >= k': '`r = {r}`，`k = {k}`：前缀长度{"够" if r >= k else "不够"}，{"可以结算答案" if r >= k else "先不结算"}',
        'ans = max': lambda S, B, r: (
            f'差值 `cur_s[x] − cur_s[y] − min_s[{(S.cur_s[S.x] & 1) ^ 1}][{S.cur_s[S.y] & 1}]` = `{S.cur_s[S.x]} − {S.cur_s[S.y]} − {_fmt_min(S.min_s[(S.cur_s[S.x] & 1) ^ 1][S.cur_s[S.y] & 1])}`；`ans = {S.ans}`'),
        'return ans': '所有 `(x, y)` 枚举完，答案 `{ans}`',
    },
    cards=dict(
        one_liner='枚举 x、y，前缀和差 + 4 种奇偶状态的最小值，滑窗保证长度和次数',
        complexity='时间 `O(n·|Σ|²)`，空间 `O(|Σ|)`',
        problem=['找子串里 `freq[a] − freq[b]` 的最大值：`a` 出现==奇数次==，`b` 出现==非 0 偶数次==，长度 `≥ k`',
                 '`s` 只含 `0` 到 `4`',
                 '示例：`s="1122211", k=3` → `1`'],
        quote='枚举 r（枚举右），问题变成计算满足上述约束的 sum[l][x] − sum[l][y] 的最小值（维护左）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `x`、`y`：答案 = `(sum[r][x]−sum[r][y]) − (sum[l][x]−sum[l][y])`，右边固定，左边要最小',
              '奇偶要求 → `l` 处 x 的奇偶与 `r` 相反、y 相同 → 4 种状态各存一个最小值 `min_s[p][q]`',
              '`left` 滑窗：长度 `≥ k` 且 x、y 次数都增加，合格的 `l` 才收进 `min_s`'],
        after=[dict(heading='本视频的输入', lines=['`s="0001100", k=4`', '首对 `(0, 1)` 就能得到答案 `3`；后面的 `(x, y)` 缺 x 或 y，什么都不会发生，视频会快进'])],
        summary=['时间 `O(n·|Σ|²)`，`|Σ| = 5`',
                 '`min_s` 初始为 `inf`，用 `ans = max(ans, … − inf)` 不会误更新',
                 '`pre_s` 只统计窗口左边的前缀，==不统计窗口内部==',
                 '`cur_s[x] & 1 ^ 1` 取反奇偶：左边与右边奇偶不同，差才是奇数'],
    ),
)
