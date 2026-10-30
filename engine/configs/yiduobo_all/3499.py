def _col(S, k, v):
    iv = S.get('intervals')
    if iv is None:
        return None
    for a, b in iv:
        if a <= k <= b:
            return 'cyan'
    return None


def _top(S):
    if 'intervals' not in S:
        return ''
    if 'length' in S and S['_line'] >= 18:
        return f"已找到的 0 段 `{S['intervals']}`，基础 1 的个数 `res = {S['res']}`"
    return f"`res = {S['res']}`（= n − 所有 0 段长度之和 = 原有 1 的个数），0 段 `{S['intervals']}`"


CONFIG = dict(
    num=3499, title='操作后最大活跃区段数 I', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='区间拆分 · 相邻 0 段取最大和',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1729'],
    code='''
class Solution(object):
    def maxActiveSectionsAfterTrade(self, s):
        n = len(s)
        intervals = []
        p = 0
        res = n
        while p < n:
            while p < n and s[p] == '1':
                p += 1
            if p == n:
                break
            q = p + 1
            while q < n and s[q] == '0':
                q += 1
            intervals.append((p, q - 1))
            res -= q - p
            p = q
        length = 0
        for index in range(1, len(intervals)):
            length = max(length, intervals[index][1] - intervals[index][0] + 1 + intervals[index - 1][1] - intervals[index - 1][0] + 1)
        return res + length
''',
    call='Solution().maxActiveSectionsAfterTrade("0100110")',
    expect=6,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='string', var='s', label='s（青 = 已记录的连续 0 段）', cell=76, pointers={'p': 'pink', 'q': 'blue'}, color=_col, h=260),
        dict(type='text', fn=lambda S: (f"相邻两段 0：`{S['intervals'][S['index']-1]}` + `{S['intervals'][S['index']]}`，长度和 `{S['intervals'][S['index']-1][1]-S['intervals'][S['index']-1][0]+1} + {S['intervals'][S['index']][1]-S['intervals'][S['index']][0]+1}`，当前最大 `length = {S['length']}`" if 'index' in S and 'length' in S and S['index'] >= 1 else ''), size=24),
    ],
    watch=[('p', 'p', 'pink'), ('q', 'q', 'blue'), ('res', 'res', 'green'), ('length', 'length', 'orange')],
    captions={
        'n = len(s)': '`n = {n}`',
        'intervals = []': '`intervals` 记录每段连续 0 的 `(起点, 终点)`',
        'p = 0': '`p` 从头扫描',
        'res = n': '`res` 先当作全是 1，之后每找到一段 0 就扣掉它的长度，剩下的就是==原有 1 的个数==',
        'while p < n:': lambda S, B, r: (f"`p = {S.p} < n`，继续找下一段 0" if S.p < S.n else "`p` 到头了，所有 0 段都找完"),
        "s[p] == '1'": lambda S, B, r: (f"`s[{S.p}] = 1`，不是 0 → 跳过" if S.p < S.n and S.s[S.p] == '1' else (f"`s[{S.p}] = 0` → 停在这一段 0 的起点" if S.p < S.n else "走到末尾")),
        'p += 1': '`p` → {p}',
        'if p == n': lambda S, B, r: ("`p == n`：后面全是 1，没有 0 段了 → 退出" if S.p == S.n else f"`p = {S.p}` 是一段 0 的起点"),
        'break': '结束扫描',
        'q = p + 1': '`q` 从 `p` 的下一位开始，往右找这段 0 的终点',
        "s[q] == '0'": lambda S, B, r: (f"`s[{S.q}] = 0` → 这段 0 还在继续" if S.q < S.n and S.s[S.q] == '0' else "遇到 1 或到末尾 → 这段 0 到 `q - 1` 结束"),
        'q += 1': '`q` → {q}',
        'intervals.append': '记下这段 0：`({p}, {q - 1})`，长度 `{q - p}`',
        'res -= q - p': '`res` 扣掉这段 0：`res = {res}`',
        'p = q': '`p = q`，从这段 0 之后继续找（下一个必是 1）',
        'length = 0': '操作等价于==把相邻的两段 0 都变成 1==（擦掉中间那段 1 再填满），所以要找长度和最大的相邻两段',
        'for index': '`index = {index}`：比较第 `{index - 1}` 段和第 `{index}` 段',
        'length = max': '相邻两段 0 的长度和，取最大：`length = {length}`',
        'return': '`res + length = {res} + {length}` = =={ret}==',
    },
    cards=dict(
        one_liner='原有的 1 不会丢，再加上相邻两段 0 的最大长度和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把被 0 包围的一段 1 变成 0，再把被 1 包围的一段 0 变成 1，至多一次',
                 '求最多的 1 的个数',
                 '本视频：`"0100110"` → `6`'],
        quote='题目中的操作可以认为是将s中被连续1分割的两段连续的0都变为1。为了使得s中最终的1数量最多，在这里就应该选择数量最多的两段连续的0。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍：把每段连续 0 的区间存进 `intervals`，同时算出原来 1 的个数 `res`',
              '相邻两段 0 之间恰好隔着一段 1，正是题目允许的操作',
              '再遍历 `intervals`，找相邻两段长度和最大的 `length`，答案 `res + length`'],
        summary=['时间 `O(n)`，空间 `O(n)`（存区间）',
                 '易错：少于两段 0 时 `length = 0`，什么也不用做',
                 '`res = n` 再逐段扣除 0 的长度，得到的就是原有的 1 的个数',
                 '对比灵神：灵神一遍遍历、`O(1)` 空间；yiduobo 先存区间再比较'],
    ),
)
