TARGET = 'abcd'
WORDS = ['ab', 'cd', 'abcd']
COSTS = [1, 1, 5]


def _word_costs(S):
    """words 中每个词的最小成本（用当前 BASE 的哈希去 min_cost 里查）"""
    mc, MOD, BASE = S.get('min_cost'), S.get('MOD'), S.get('BASE')
    out = {}
    if mc is None or MOD is None or BASE is None:
        return out
    for w in WORDS:
        h = 0
        for b in w:
            h = (h * BASE + ord(b)) % MOD
        if h in mc and mc[h] != float('inf'):
            out[w] = mc[h]
    return out


def _mc(S):
    wc = _word_costs(S)
    return ('`min_cost`：' + '，'.join(f'{w}→{c}' for w, c in wc.items())) if wc else '`min_cost`：单词的哈希 → 最小成本'


def _sub(S):
    if 'f' in S and 'i' in S and 'sz' in S and S['sz'] <= S['i']:
        i, sz = S['i'], S['sz']
        t = TARGET[i - sz:i]
        wc = _word_costs(S)
        return f"子串 `target[{i - sz}:{i}]` = =={t}=={'，在 min_cost 里，成本 ' + str(wc[t]) if t in wc else '，不是任何单词'}"
    return '`f[i]`：拼出 target 前 i 个字符的最小成本'


CONFIG = dict(
    num=3213, title='最小代价构造字符串', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='字符串哈希 + DP · 只枚举 O(√L) 种长度',
    tags=['字符串', '难度分 2171'],
    code='''
class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        n = len(target)

        # 多项式字符串哈希（方便计算子串哈希值）
        # 哈希函数 hash(s) = s[0] * BASE^(n-1) + s[1] * BASE^(n-2) + ... + s[n-2] * BASE + s[n-1]
        MOD = 1_070_777_777
        BASE = randint(8 * 10 ** 8, 9 * 10 ** 8)  # 随机 BASE，防止 hack
        pow_base = [1] + [0] * n  # pow_base[i] = BASE^i
        pre_hash = [0] * (n + 1)  # 前缀哈希值 pre_hash[i] = hash(s[:i])
        for i, b in enumerate(target):
            pow_base[i + 1] = pow_base[i] * BASE % MOD
            pre_hash[i + 1] = (pre_hash[i] * BASE + ord(b)) % MOD  # 秦九韶算法计算多项式哈希

        # 每个 words[i] 的哈希值 -> 最小成本
        min_cost = defaultdict(lambda: inf)
        for w, c in zip(words, costs):
            h = 0
            for b in w:
                h = (h * BASE + ord(b)) % MOD
            min_cost[h] = min(min_cost[h], c)

        # 有 O(√L) 个不同的长度
        sorted_lens = sorted(set(map(len, words)))

        f = [0] + [inf] * n
        for i in range(1, n + 1):
            for sz in sorted_lens:
                if sz > i:
                    break
                # 计算子串 target[i-sz:i] 的哈希值（计算方法类似前缀和）
                sub_hash = (pre_hash[i] - pre_hash[i - sz] * pow_base[sz]) % MOD
                # 手写 min，避免超时
                tmp = f[i - sz] + min_cost[sub_hash]
                if tmp < f[i]:
                    f[i] = tmp
        return -1 if f[n] == inf else f[n]
''',
    setup="import random\nrandom.seed(0)\nfrom random import randint",
    call="Solution().minimumCost('abcd', ['ab', 'cd', 'abcd'], [1, 1, 5])",
    expect=2,
    views=[
        dict(type='text', fn=_mc, size=30, h=50),
        dict(type='text', fn=_sub, size=30, h=50),
        dict(type='string', var='target', label='target（蓝框 = 当前子串 target[i-sz:i]）', h=190,
             window=('(i - sz) if f else None', '(i - 1) if f else None')),
        dict(type='array', var='f', label='f[i]：target 前 i 个字符的最小成本', h=190, pointers={'i': 'blue', 'i - sz': 'orange'},
             color=lambda S, idx, v: ('green' if v != float('inf') else None)),
        dict(type='array', var='sorted_lens', label='sorted_lens：words 里出现过的长度（只枚举这些）', h=150, color=lambda S, idx, v: 'pink' if S.get('sz') == v and 'f' in S else None),
    ],
    watch=[('i', 'i', 'blue'), ('sz', 'sz', 'pink'), 'tmp'],
    captions={
        'for w, c in zip': lambda S, B, r: ('单词都处理完了' if B.get('w') == S.w else ('前缀哈希 `pre_hash`、`pow_base` 已预处理好，之后任意子串哈希都能 `O(1)` 算出。' if 'w' not in B else '') + f"取单词 `{S.w}`，成本 `{S.c}`：算它的哈希"),
        'min_cost[h] = min': lambda S, B, r: f"这个单词的哈希 `{S.h}` → 最小成本 =={S.min_cost[S.h]}==（重复单词取最小）",
        'sorted_lens = sorted': '`words` 里不同的长度只有 `O(√L)` 个：长度和 `1+2+3+…≤L` → 只需枚举这些长度 = =={sorted_lens}==',
        'for i in range': lambda S, B, r: ('所有 `i` 都算完了' if B.get('i') == S.i else f'`i = {S.i}`：求拼出 `target[:{S.i}]` 的最小成本 `f[{S.i}]`，枚举最后一个单词的长度'),
        'sub_hash = ': lambda S, B, r: f"枚举长度 `sz = {S.sz}`（只枚举 `sorted_lens` 里的，更长的直接 break）：子串 `target[{S.i - S.sz}:{S.i}]` = '{TARGET[S.i - S.sz:S.i]}'，哈希 = `pre_hash[{S.i}] − pre_hash[{S.i - S.sz}] × BASE^{S.sz}`",
        'tmp = f': lambda S, B, r: (f"`f[{S.i - S.sz}] + 成本` = {S.f[S.i - S.sz]} + {S.min_cost[S.sub_hash]} = =={S.tmp}==" if S.tmp != float('inf')
                                    else f"子串 '{TARGET[S.i - S.sz:S.i]}' 不是单词（或前面拼不出）→ `inf`，不会更新"),
        'if tmp < f[i]': lambda S, B, r: (f'`tmp = {S.tmp}` < `f[{S.i}] = {S.f[S.i]}`：更小 → 更新' if S.tmp < S.f[S.i] else f'`tmp = {S.tmp}` 不比 `f[{S.i}] = {S.f[S.i]}` 小 → 不更新'),
        'f[i] = tmp': '更新：`f[{i}] = {tmp}`',
        'return -1': '`f[n] = {f[n]}`：拼出整个 target 的最小成本',
    },
    skip=['for i, b in enumerate', 'pow_base[i + 1]', 'pre_hash[i + 1]', 'for b in w', 'h = (h *', 'h = 0', 'for sz in', 'if sz > i', 'break', 'pow_base = [1]', 'pre_hash = [0]', 'n = len(target)', 'MOD = ', 'BASE = ', 'min_cost = defaultdict'],
    max_steps=100,
    cards=dict(
        one_liner='用哈希 O(1) 判断子串是不是单词，只枚举 O(√L) 种长度',
        complexity='时间 `O(L + n√L)`，空间 `O(n + m)`',
        problem=['有 `words` 和对应 `costs`，每个单词可以用任意次，拼接成 `target`，成本是用到的单词成本之和',
                 '拼不出返回 `-1`，求最小成本',
                 '本视频：`target = abcd`，`words = [ab, cd, abcd]`，`costs = [1,1,5]` → `2`'],
        quote='设 L 是 words 中所有字符串的长度之和，那么 words 中至多有 O(√L) 个长度不同的字符串……所以我们只需要枚举这 O(√L) 个长度，而不是枚举 O(n) 个 j。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]` = 拼出前 `i` 个字符的最小成本，枚举最后一个单词：`f[i] = f[j] + costs[k]`',
              '朴素枚举 `j` 是 `O(n²)`。但单词长度只有 `O(√L)` 种，只需枚举这些长度 `sz`',
              '子串是否等于某个单词：用多项式哈希，像前缀和一样 `O(1)` 取子串哈希，查 `min_cost`'],
        summary=['时间 `O(L + n√L)`，空间 `O(n + m)`',
                 '相同的单词要取最小成本：`min_cost[h] = min(min_cost[h], c)`',
                 '单模哈希有生日攻击风险，题解写法二改用 `10^18+3` 双大模数；BASE 取随机防 hack',
                 '题解还有后缀数组（匹配位置建图）和 AC 自动机（标准做法）两种方法，本视频讲哈希 + DP'],
    ),
)
