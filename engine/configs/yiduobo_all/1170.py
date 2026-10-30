K = 6  # 只画前 K 个频次


def _phase(S):
    if 'res' in S:
        return 'q'
    return 'w'


def _top(S):
    if 'word' not in S:
        return '`f(s)`：s 中==最小字母==的出现次数'
    who = 'query' if _phase(S) == 'q' else 'word'
    now, cnt = S.get('now'), S.get('cnt')
    if now is None:
        return f"扫描 {who} `{S['word']}`：还没看到字母"
    return f"扫描 {who} `{S['word']}`：目前最小字母 `'{now}'`，出现 =={cnt}== 次"


def _cmp(S, B, ret):
    ch, now = S.char, B.now
    if now is None:
        return f"第一个字母 `'{ch}'`：直接当作最小字母"
    if now > ch:
        return f"`'{ch}' < '{now}'`：出现==更小的字母== → 换成 `'{ch}'`，计数从 1 重来"
    if now == ch:
        return f"`'{ch}'` 就是当前最小字母 → 计数 +1"
    return f"`'{ch}' > '{now}'`：比最小字母大，不影响"


CONFIG = dict(
    num=1170, title='比较字符串中最小字母出现频次', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='计数 + 前缀和',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def numSmallerByFrequency(self, queries, words):

        t = [0] * 2001
        for word in words:
            cnt = 0
            now = None
            for char in word:
                if now is None or now > char:
                    now = char
                    cnt = 1
                elif now == char:
                    cnt += 1
            t[cnt] += 1

        s = t[:]
        for index in range(1, 2001):
            s[index] += s[index - 1]

        res = []
        for word in queries:
            cnt = 0
            now = None
            for char in word:
                if now is None or now > char:
                    now = char
                    cnt = 1
                elif now == char:
                    cnt += 1

            res.append(s[-1] - s[cnt])

        return res
''',
    call='Solution().numSmallerByFrequency(["cbd", "bbb"], ["zaaz", "ab", "cc"])',
    expect=[2, 0],
    skip=['for char in word', 'elif now == char', 'for index in range', 's[index] +=', 'now = None', 'now = char'],
    max_steps=80,
    views=[
        dict(type='text', fn=_top, size=27, h=90),
        dict(type='string', var='word', label='当前字符串', cell=90, h=170),
        dict(type='array', var=lambda S: S['t'][:K], label=f't[f]：words 中 f 值为 f 的个数（只画前 {K} 个，共 2001 个）',
             color=lambda S, i, v: 'yellow' if 'cnt' in S and i == S['cnt'] and _phase(S) == 'w' and v else None,
             cell=90, h=170),
        dict(type='array', var=lambda S: S['s'][:K] if 's' in S else None, label='s[f] = t[0] + … + t[f]（前缀和）',
             color=lambda S, i, v: 'pink' if _phase(S) == 'q' and 'cnt' in S and i == S['cnt'] else None,
             cell=90, h=170),
        dict(type='array', var='res', label='res', cell=90, h=150),
    ],
    watch=[('now', 'now', 'cyan'), ('cnt', 'cnt', 'yellow'), ('s[-1]', "s[-1]", 'green')],
    captions={
        't = [0] * 2001': '`t` 是计数表：`t[f]` = 有多少个 word 的 f 值等于 `f`',
        'for word in words': lambda S, B, r: ('words 统计完毕' if B.get('word') == S.word
                                              else f'处理 word `{S.word}`，先求它的 f 值'),
        'cnt = 0': '`cnt = 0`，`now = None`：从头扫描 `{word}`',
        'if now is None': _cmp,
        'cnt = 1': "最小字母变为 `'{now}'`，`cnt = 1`",
        'elif now == char': lambda S, B, r: (f"`'{S.char}' == '{S.now}'` → 计数 +1" if S.char == S.now
                                             else f"`'{S.char}' > '{S.now}'`：比最小字母大，不影响"),
        'cnt += 1': '`cnt` → {cnt}',
        't[cnt] += 1': '`f({word}) = {cnt}` → `t[{cnt}]` 变成 =={t[cnt]}==',
        's = t[:]': '复制一份 `s`，再求==前缀和==：`s[f]` = f 值 ≤ f 的 word 个数',
        'res = []': '前缀和算好了：`s[-1] = {s[-1]}` 是 word 总数',
        'for word in queries': lambda S, B, r: ('queries 处理完毕' if 'res' in B and len(S.res) == len(S.queries)
                                                else f'处理 query `{S.word}`，同样求 f 值'),
        'res.append': lambda S, B, r: (f'`f({S.word}) = {S.cnt}`：f 值 `> {S.cnt}` 的 word 有 '
                                       f'`s[-1] − s[{S.cnt}] = {S.s[-1]} − {S.s[S.cnt]}` = =={S.res[-1]}== 个'),
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='先统计 words 的 f 值分布，前缀和一减就知道有多少个比 query 大',
        complexity='时间 `O(总字符数 + U)`，空间 `O(U)`，`U = 2001`',
        problem=['`f(s)` = 字符串 s 中==字典序最小的字母==的出现次数，如 `f("dcce") = 2`',
                 '对每个 `queries[i]`，统计 words 中满足 `f(queries[i]) < f(W)` 的词数',
                 '示例：`queries = ["cbd"], words = ["zaaaz"]` → `[1]`',
                 '本视频：`["cbd","bbb"], ["zaaz","ab","cc"]` → `[2,0]`'],
        quote='此时我们要求a中要多少个值大于k的数，那么就等于res = t[k + 1] + t[k + 2] + ... + t[-1]。这是一个子段和问题，那么可以再进一步转化成==前缀和==的问题来解决了，即 res = s[-1] - s[k]',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描求 f：遇到更小的字母就重置为 1，相等就 +1',
              'f 值不超过 2000 → 用数组 `t` 当哈希表计数',
              '`> k` 的个数 = 总数 − `≤ k` 的个数 = `s[-1] − s[k]`'],
        summary=['时间 `O(总字符数 + U)`；每个 query `O(1)` 回答',
                 '求 f 时 `now > char` 要==重置 cnt = 1==，不是累加',
                 '要的是==严格大于==：减去 `s[k]`（含 `t[k]`），不是 `s[k − 1]`',
                 '也可以把 words 的 f 值排序后对每个 query 二分（`bisect_right`）'],
    ),
)
