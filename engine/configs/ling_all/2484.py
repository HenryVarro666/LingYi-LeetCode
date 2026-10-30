S0 = '103301'
N = len(S0)


def _nz(name):
    return lambda S: {f'{k // 10}{k % 10}': v for k, v in enumerate(S[name]) if v} if name in S else None


def _cur(S):
    """当前处理的下标（第一轮从右往左，第二轮从左往右）"""
    ln = S.get('_line', 0)
    if 'pre' in S and ln >= 13:
        i = sum(S['pre']) - (1 if ln == 20 else 0)
        return i if 0 <= i < N else None
    if 'suf' in S and ln <= 8:
        k = sum(S['suf'])
        i = N - k if ln == 8 else N - 1 - k
        return i if 0 <= i < N else None
    return None


def _scol(S, i, v):
    c = _cur(S)
    if c is None:
        return None
    ln = S.get('_line', 0)
    if ln <= 8:
        return 'pink' if i == c else ('green' if i > c else None)
    return 'blue' if i == c else ('cyan' if i < c else ('green' if i > c else None))


def _mid(S, B, ret):
    d = S.d
    tot = sum(a * b for a, b in zip(S.pre2, S.suf2))
    parts = [f'`{k // 10}{k % 10}`: {a}×{b}' for k, (a, b) in enumerate(zip(S.pre2, S.suf2)) if a * b]
    ps = '，'.join(parts[:4]) + ('…' if len(parts) > 4 else '') if parts else '没有能配对的'
    return f'以 `s[{_cur(S)}]={d}` 为中心：左边的两位数 × 右边的两位数，逐格相乘求和（{ps}）→ 新增 =={tot}==，`ans` = {S.ans}'


def _fm(S):
    ln = S.get('_line', 0)
    if ln >= 13 and 'pre2' in S:
        return '回文 `ab d ba`：左边选 `ab`（`pre2`）、右边选 `ba`（`suf2`），==两个计数相乘=='
    return '先倒着扫一遍：`suf2[ab]` = 右侧能凑成 `ab` 两位子序列的个数'


CONFIG = dict(
    num=2484, title='统计回文子序列数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 · 枚举回文中心',
    tags=['灵神题单·动态规划', '难度分 2223'],
    code='''
class Solution:
    def countPalindromes(self, s: str) -> int:
        suf = [0] * 10
        suf2 = [0] * 100
        for d in map(int, reversed(s)):
            for j, c in enumerate(suf):
                suf2[d * 10 + j] += c
            suf[d] += 1

        ans = 0
        pre = [0] * 10
        pre2 = [0] * 100
        for d in map(int, s):
            suf[d] -= 1
            for j, c in enumerate(suf):
                suf2[d * 10 + j] -= c  # 撤销
            ans += sum(c1 * c2 for c1, c2 in zip(pre2, suf2))  # 枚举所有字符组合
            for j, c in enumerate(pre):
                pre2[d * 10 + j] += c
            pre[d] += 1
        return ans % (10 ** 9 + 7)
''',
    call=f'Solution().countPalindromes({S0!r})',
    expect=2,
    skip=['for j, c in enumerate', 'suf2[d * 10 + j] += c', 'suf2[d * 10 + j] -= c', 'pre2[d * 10 + j] += c'],
    views=[
        dict(type='string', var='s', label='s（蓝 = 回文中心，绿 = 已算过后缀，青 = 已进前缀）', h=150, cell=84, color=_scol),
        dict(type='array', var='suf', label='suf[a]：右侧数字 a 的个数', h=150, cell=64),
        dict(type='array', var='pre', label='pre[a]：左侧数字 a 的个数', h=150, cell=64),
        dict(type='map', var=_nz('suf2'), label='suf2[ab] ≠ 0（右侧两位子序列个数，高位在前）', h=110, font=22),
        dict(type='map', var=_nz('pre2'), label='pre2[ab] ≠ 0（左侧两位子序列个数）', h=110, font=22),
        dict(type='text', fn=_fm, size=24, h=60),
    ],
    watch=[('d', 'd', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'suf = [0] * 10': '`suf[a]`：右侧数字 `a` 出现次数，先全 0',
        'suf2 = [0] * 100': '`suf2[a*10+b]`：右侧长为 2 的子序列「ab」个数，共 100 种',
        'for d in map(int, reversed(s))': lambda S, B, r: (f'倒着扫到 `s[{_cur(S)}] = {S.d}`：让它当两位子序列的==第一位==，接在右边每个数字 `j` 前面：`suf2[d*10+j] += suf[j]`' if _cur(S) is not None else '倒着扫完了，`suf`/`suf2` 记录的是整个 `s`'),
        'suf[d] += 1': lambda S, B, r: f'`suf[{S.d}]` 加一 → {S.suf[S.d]}；已记录两位子序列共 {sum(S.suf2)} 个',
        'ans = 0': '第二轮：正着扫，枚举每个 `s[i]` 当回文中心',
        'pre = [0] * 10': '`pre`/`pre2` 同理，统计左侧',
        'for d in map(int, s)': lambda S, B, r: (f'中心 `s[{_cur(S)}] = {S.d}`' if _cur(S) is not None else '每个中心都枚举完了'),
        'pre2 = [0] * 100': '`pre2[a*10+b]`：左侧两位子序列「ab」个数',
        'suf[d] -= 1': lambda S, B, r: f'中心自己不能算在右侧：`suf[{S.d}]` 减一 → {S.suf[S.d]}；同时把以它开头的两位组合从 `suf2` ==撤销==',
        'ans += sum': _mid,
        'pre[d] += 1': lambda S, B, r: f'中心用完了：把 `{S.d}` 并入左侧，`pre2` 里以它结尾的组合增加，`pre[{S.d}]` → {S.pre[S.d]}',
        'return ans': '答案最坏是 `C(n,5)` < 10^18，Python 大整数不怕，==最后才取模==：`{ans} % (10^9+7)`',
    },
    cards=dict(
        one_liner='枚举回文中心，左边两位 × 右边两位，逐格相乘',
        complexity='时间 `O(n·10²)`，空间 `O(10²)`',
        problem=['数字串 `s`，数其中长度为 5 的==回文子序列==个数，对 `10^9+7` 取模',
                 '子序列按位置区分：相同内容但下标不同算不同的',
                 '示例：`"103301"` → `2`（两个 `10301`）'],
        quote='枚举每个 s[i]，当作回文子序列的回文中心，此时的子序列个数就是 s[0..i-1] 中的 pre2[a][b] 与 s[i+1..n-1] 中的 suf2[a][b] 的组合。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长为 5 的回文 = `a b c b a`，中间 `c` 固定，左右各取两位',
              '右边两位 `ab` 要和左边的 `ba` 配对：倒着统计 `suf2`，两边方向就对上了',
              '一边往右走一边==撤销 `suf2`、累加 `pre2`==，一遍搞定'],
        summary=['时间 `O(n|Σ|²)`，空间 `O(|Σ|²)`，这里 `|Σ| = 10`',
                 '先倒着建好 `suf`/`suf2`，正着扫时再「撤销」中心及其以左的贡献',
                 '最坏全同字符答案 `C(n,5) < 10^18`，所以可以最后再取模',
                 '同类题：1930 长度为 3 的不同回文子序列（前后缀分解）'],
    ),
)
