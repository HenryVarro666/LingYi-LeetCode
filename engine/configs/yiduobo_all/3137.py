def _col(S, i, v):
    if 'k' not in S or 'index' not in S:
        return None
    if S['index'] <= i < S['index'] + S['k']:
        return 'blue'
    return None


def _txt(S):
    if 'freq' not in S:
        return '起点必须是 k 的倍数、长度为 k → 原串天然分成 `n/k` 个子串，统计各自出现次数'
    return f"已有 {sum(S['freq'].values())} 个子串入表，种类 {len(S['freq'])}　　`freq = {dict(S['freq'])}`"


CONFIG = dict(
    num=3137, title='K 周期字符串需要的最少操作次数', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按 k 切子串 + 哈希计数',
    tags=[],
    code='''
class Solution(object):
    def minimumOperationsToMakeKPeriodic(self, word, k):

        freq = Counter()
        for index in range(0, len(word), k):
            substr = word[index : index + k]
            freq[substr] += 1
        
        return len(word) // k - max(freq.values())
''',
    call='Solution().minimumOperationsToMakeKPeriodic("leetcoleet", 2)',
    expect=3,
    skip=['freq = Counter()'],
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前取出的子串）', cell=76, color=_col, h=220),
        dict(type='map', var='freq', label='freq：子串出现次数', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', fn=_txt, size=26, h=110),
    ],
    watch=[('index', 'index', 'blue'), ('substr', 'substr'), ('k', 'k')],
    captions={
        'for index in range': '`index = {index}`：每隔 `k = {k}` 个字符取一段，起点都是 k 的倍数',
        'substr = word': '取出子串 `substr = word[{index}:{index + k}]` = `{substr}`',
        'freq[substr] += 1': '`freq[{substr}]` 加一 → =={freq[substr]}==',
        'return len': lambda S, B, r: f"子串总数 `{len(S.word) // S.k}`，出现最多的 `{max(S.freq.values())}` 次 → 其余 =={r}== 个要被覆盖",
    },
    cards=dict(
        one_liner='把字符串切成 n/k 段，数最多的那段出现几次，其余就是操作数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`word` 长 n，k 是 n 的约数；每次可用一段长 k 的子串覆盖另一段',
                 '起点都必须是 k 的倍数，求变成 k 周期字符串的最少次数',
                 '演示：`"leetcoleet", k=2` → `3`'],
        quote='本题实际上就是将原字符串按k的长度划分为若干个子串，问其中出现次数最多的子串的出现次数是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['覆盖的起点和长度都被限制，只能整段整段地换',
              '遍历所有起点，用哈希表数各种子串出现的次数',
              '子串总数 − 最大次数 = 需要被覆盖的段数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '子串总数是 `len(word) // k`，不是 `len(word)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
