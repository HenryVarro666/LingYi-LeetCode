def _col(S, i, v):
    t = S.get('total')
    c = S.get('c')
    if t is None:
        return None
    if i == t:
        return 'blue'
    if c is not None and i == t - c - 1:
        return 'yellow'
    return None


CONFIG = dict(
    num=3333, title='找到初始输入字符串 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='反向计数 · 前缀和优化 DP',
    tags=['动态规划', '数学算法', '难度分 2629'],
    code='''
class Solution(object):
    def possibleStringCount(self, word, k):
        
        if len(word) < k:
            return 0

        cnt = []
        pre = 0
        t = 0
        for index in range(1, len(word)):
            if word[index] != word[index - 1]:
                t += 1
                cnt.append(index - pre)
                pre = index
        
        t += 1
        cnt.append(len(word) - pre)
        k = max(0, k - t)

        res = 1
        mod = 10 ** 9 + 7
        for c in cnt:
            res = res * c % mod

        if k > 0:
            f = [0] * k
            s = [1] * k
            for c in cnt:
                if c == 1:
                    continue
                c -= 1

                for total in range(k):
                    if c >= total:
                        f[total] = s[total]
                    else:
                        f[total] = (s[total] - s[total - c - 1] + mod) % mod

                s[0] = f[0]
                for total in range(1, k):
                    s[total] = (s[total - 1] + f[total]) % mod

            for total in range(k):
                res -= f[total]
                if res < 0:
                    res += mod

        return res
''',
    call="Solution().possibleStringCount('aabbccdd', 7)",
    expect=5,
    max_steps=100,
    skip=['pre = 0', 't = 0', 'for index in range(1', 'if word[index]', 'pre = index', 'mod = 10', 'for c in cnt:', 'if c == 1', 'continue', 'for total in range(k)', 'for total in range(1, k)', 'f[total] = s[total]', 'if res < 0', 'res += mod'],
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前扫描位置 index）', h=140, pointers={'index': 'blue'}, cell=56),
        dict(type='array', var='cnt', label='cnt：各段连续相同字符的长度', h=140, cell=56),
        dict(type='array', var='f', label='f[total]：从多余字符中恰好选 total 个的方案数', h=170, cell=64, color=_col),
        dict(type='array', var='s', label='s[total]：f 的前缀和（蓝 = total，黄 = 要减去的 total-c-1）', h=170, cell=64, color=_col),
        dict(type='text', fn=lambda S: (f"所有原串共 `res` = =={S['res']}== 种" if 'res' in S else ''), size=28),
    ],
    watch=[('t', 't', 'blue'), ('k', 'k', 'pink'), ('res', 'res', 'green'), ('c', 'c', 'orange'), ('total', 'total', 'cyan')],
    captions={
        'if len(word) < k': lambda S, B, r: ('`len(word) < k`：再怎么输入也不够长 → 答案 0' if len(S.word) < S.k else f'`len(word) = {len(S.word)} ≥ k = {S.k}`，有可能，继续'),
        7: '`cnt` 记录每一段相同字符的长度，`t` 记录段数',
        12: '字符变了：前一段结束，段数 `t = {t}`',
        13: '一段相同字符结束：长度 `{index - B.pre}` 加入 `cnt`；已有 `{t}` 段',
        16: '循环只会在「字符变化」时结算，最后一段还没加入，`t` 补上 1',
        'cnt.append(len(word)': '最后一段长度 `{len(word) - pre}` 加入 `cnt` → `{cnt}`',
        'k = max(0, k - t)': '最短原串是每段取 1 个，长度 `t = {t}`；还差 `k - t` → `k = {k}`（<=0 说明已经够长）',
        'res = 1': '先算==不考虑 k== 的原串总数：每段有 `c` 种取法，连乘',
        'res = res * c': '乘上这一段的 `{c}` 种可能 → `res` = =={res}==',
        'if k > 0': lambda S, B, r: (f'`k = {S.k} > 0`：长度可能不足，要减去「长度 < k」的原串（DP）' if S.k > 0 else '`k = 0`：最短原串已经达标，答案就是连乘结果'),
        'f = [0] * k': '`f`：本段额外字符取 `total` 个的方案数',
        's = [1] * k': '`s`：`f` 的前缀和；还没加入任何段时，只有「全不取」一种，所以全是 1',
        'c -= 1': '这段只有 `c - 1` 个多余字符可选（必选的那个已经算进最短原串）→ `c = {c}`',
        'if c >= total': lambda S, B, r: (f'`c = {S.c} ≥ total = {S.total}`：余量足 → `f[{S.total}] = s[{S.total}]` = =={S.s[S.total]}==，前面所有取法之和' if S.c >= S.total else f'`c = {S.c} < total = {S.total}`：这段最多取 c 个 → 前缀和之差 `s[{S.total}] − s[{S.total - S.c - 1}]`'),
        'f[total] = (s[total] - s': '`f[{total}] = s[{total}] − s[{total - c - 1}]` = =={f[total]}==（+mod 防负数）',
        's[0] = f[0]': '用新的 `f` 重算前缀和 `s`：`s[0] = f[0] = {f[0]}`',
        's[total] = (s[total - 1]': '`s[{total}] = s[{total - 1}] + f[{total}]` = =={s[total]}==',
        'res -= f[total]': '减去额外字符恰好 {total} 个（长度不足）的方案 `f[{total}] = {f[total]}` → `res` = =={res}==；变负就加回 mod',
        'return res': '答案 `res` = =={ret}==',
    },
    cards=dict(
        one_liner='总数减去「长度不足 k」的，后者用前缀和优化的 DP 算',
        complexity='时间 `O(n + t·k)`，空间 `O(t + k)`',
        problem=['`word` 是最终显示的字符串，同一个字符可能被误按多次；`k` 是原串长度的下限',
                 '求原串有多少种可能，对 `10^9+7` 取模',
                 '示例：`"aabbccdd", k=7` → `5`；`"aaabbb", k=3` → `8`'],
        quote='长度至少的为k的原始字符串的数量，等于情况1中计算的所有可能的原始字符串数量，减去长度小于k的原始字符串的数量，而后面这个值在转化后可以通过动态规划求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['先切成 `t` 段相同字符，最短原串每段 1 个；`t >= k` 时直接把各段长度连乘',
              '`t < k`：连乘总数 − 长度不足 `k` 的个数；`f[total]` 表示从多余字符里选 `total` 个的方案数',
              '转移是上一轮 `f` 的区间和 → 用前缀和 `s`：`s[total] − s[total−c−1]`，`f` 与 `s` 轮流更新，省去一维'],
        summary=['时间 `O(n + t·k)`：`k` 最大 2000，段数 `t` 也至多 n',
                 '`k = max(0, k - t)` 之后，`k` 表示还差几个额外字符',
                 '长度为 1 的段没有多余字符，`continue` 跳过，`f`/`s` 保持不变',
                 '最后减去的是 `f[0..k-1]`（额外字符数小于 `k`），差值可能为负，要加回 `mod`',
                 '原文为 Python 2 写法，代码无需修改（无整数除法）'],
    ),
)
