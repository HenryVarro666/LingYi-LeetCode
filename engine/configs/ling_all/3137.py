def _col(S, i, v):
    if 'cnt' not in S or 'k' not in S:
        return None
    w, k = S['word'], S['k']
    b = w[i // k * k: i // k * k + k]
    if 'mx' in S:
        return 'green' if S['cnt'][b] == S['mx'] else 'pink'
    return 'blue'


def _txt(S):
    if 'mx' in S:
        return f"块总数 `n/k = {S['n'] // S['k']}`，最多重复 `mx = {S['mx']}` 块 → 其余 ==`{S['n'] // S['k']} − {S['mx']}`== 块要被替换"
    if 'cnt' in S:
        return '把 word 按长 k 切成 `n/k` 块，统计每种块出现几次'
    return '操作只能整块替换（起点是 k 的倍数）→ 先切块'


CONFIG = dict(
    num=3137, title='K 周期字符串需要的最少操作次数', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='分块计数 + 众数',
    tags=[],
    code='''
class Solution:
    def minimumOperationsToMakeKPeriodic(self, word: str, k: int) -> int:
        n = len(word)
        cnt = Counter(word[i - k: i] for i in range(k, n + 1, k))
        mx = max(cnt.values())
        return n // k - mx
''',
    call='Solution().minimumOperationsToMakeKPeriodic("leetcodeleet", 4)',
    expect=1,
    views=[
        dict(type='string', var='word', label='word（绿 = 众数块，保留；粉 = 要被替换的块）', cell=70, color=_col, h=230),
        dict(type='map', var='cnt', label='cnt：每种块出现的次数', fmt=lambda k, v: f"'{k}': {v}", h=160, font=34),
        dict(type='text', fn=_txt, size=28, h=120),
    ],
    watch=['n', 'k', ('mx', 'mx', 'green')],
    captions={
        'n = len': '`n = len(word) = {n}`，`k = {k}` 是 n 的因数，共 `n/k = {n // k}` 块',
        'cnt = Counter': lambda S, B, r: f"只有首下标是 `0, k, 2k, …` 的长 k 子串能参与操作 → 切成 {S.n // S.k} 块并计数：`{dict(S.cnt)}`",
        'mx = max': '出现最多的块出现了 `mx = {mx}` 次：==把它当模板，其余块都覆盖成它==',
        'return n // k': '答案 = 总块数 − 保留的块数 = `{n // k} − {mx}` = =={ret}==',
    },
    cards=dict(
        after=[dict(heading='再看一个例子', lines=['`"leetcoleet", k=2`：切成 `le, et, co, le, et`', '`le`、`et` 各 2 次，`mx = 2`', '答案 `5 − 2 = 3`，和题目示例 2 的三次操作吻合'])],
        one_liner='最多保留几块不动？众数块的出现次数 mx，其余全替换',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一次操作：把某个 k 的倍数起点的长 k 子串，覆盖成另一个这样的子串',
                 '求最少操作几次，让 `word` 变成某个长 k 串重复若干次',
                 '示例：`"leetcodeleet", k=4` → `1`（把 `code` 换成 `leet`）'],
        quote='用出现次数最多的子串，替换其余子串。所以用子串的个数 n/k 减去 mx，就是最少操作次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['能动的只有整块，周期串 = 所有块相等',
              '每次操作最多让一个块变对 → 想少操作就让「不用动的块」尽量多',
              '不用动的块最多是众数的个数 `mx`，答案 `n/k − mx`'],
        summary=['时间 `O(n)`：每块 k 个字符，共 n/k 块，哈希总开销 O(n)',
                 '易错：切块下标 `word[i-k:i]` 配 `range(k, n+1, k)`，终点要写 n+1',
                 '不用关心块内容怎么变，只统计块的出现次数'],
    ),
)
