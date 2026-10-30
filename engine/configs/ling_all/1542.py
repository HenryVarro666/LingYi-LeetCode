S0 = '3242415'


def _b(x):
    return format(x, '06b')


def _txt(S):
    if 'pre' not in S or 'i' not in S or S['_line'] < 9:
        return '`pre` 的第 x 位 = 数字 x 出现次数的奇偶性（这里只画低 6 位，从右到左 0 1 2 3 4 5）'
    n = S['n']
    pre, i, pos = S['pre'], S['i'], S['pos']
    ev = pos[pre]
    odd = [(d, pos[pre ^ (1 << d)]) for d in range(S['D']) if pos[pre ^ (1 << d)] != n]
    se = f'偶数：`pos[{_b(pre)}] = {ev}` → 长度 {i - ev}' if ev != n else '偶数：该状态没出现过'
    so = ('；奇数：' + '、'.join(f'翻转第 {d} 位 → 长度 {i - p}' for d, p in odd)) if odd else '；奇数：没有匹配'
    return f'`pre = {_b(pre)}`　{se}{so}'


def _pos_var(S):
    n = S['n']
    return {format(k, '06b'): v for k, v in enumerate(S['pos']) if v != n}


_seen = {}


def _ans_cap(S, B):
    if _seen.get('i') != S.i:
        _seen['i'] = S.i
        return '查表：偶数看 `pos[pre]`，奇数枚举翻转 `pre` 的某一位再查 `pos`，取最长的子串长度 `i - pos`'
    n, i, pre, pos = S.n, S.i, S.pre, S.pos
    ev = i - pos[pre] if pos[pre] != n else None
    od = [(i - pos[pre ^ (1 << d)], d) for d in range(S.D) if pos[pre ^ (1 << d)] != n]
    if S.ans == B.ans:
        return f'当前前缀没有带来更长的超赞子串，`ans` 仍是 `{S.ans}`'
    if ev is not None and ev == S.ans:
        return f'偶数情况：同样的 `pre` 在 `{pos[pre]}` 出现过，中间子串长 `{ev}`（每个数字都是偶数次）→ `ans = {S.ans}`'
    L, d = max(od)
    return f'奇数情况：翻转第 `{d}` 位的状态在 `{i - L}` 出现过，中间子串长 `{L}`（只有数字 {d} 是奇数次）→ `ans = {S.ans}`'


CONFIG = dict(
    num=1542, title='找出最长的超赞子字符串', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='异或前缀和 + 首次出现下标',
    tags=['前缀和', '状态压缩前缀和', '难度分 2222'],
    code='''
class Solution:
    def longestAwesome(self, s: str) -> int:
        D = 10  # s 中的字符种类数
        n = len(s)
        pos = [n] * (1 << D)  # n 表示没有找到异或前缀和
        pos[0] = -1  # pre[-1] = 0
        ans = pre = 0
        for i, x in enumerate(map(int, s)):
            pre ^= 1 << x
            ans = max(ans, i - pos[pre],  # 偶数
                      max(i - pos[pre ^ (1 << d)] for d in range(D)))  # 奇数
            if pos[pre] == n:  # 首次遇到值为 pre 的前缀异或和，记录其下标 i
                pos[pre] = i
        return ans
''',
    call=f'Solution().longestAwesome({S0!r})',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（指针 = 当前读到的 i）', cell=100, h=170, pointers={'i': 'blue'}),
        dict(type='map', var=_pos_var, label='pos（异或前缀和 → 首次出现的下标；其余都是 n）', fmt=lambda k, v: f'{k}: {v}', h=220, font=26),
        dict(type='text', h=120, size=26, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('pre', 'format(pre, "06b")', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'D = 10': '数字有 10 种 → 用 `10` 位二进制记奇偶',
        'pos = [n]': '`pos[mask]` = 该异或前缀和==首次==出现的下标；`n` 表示没出现过',
        'pos[0] = -1': '空前缀 `pre[-1] = 0`，位置记为 `-1`，这样从头开始的子串也能算',
        'ans = pre = 0': '`pre` 是当前前缀里各数字出现次数的奇偶性，一开始全是偶数',
        'for i, x': lambda S, B, ret: (f'读入 `s[{S.i}] = {S.x}`' if 'i' in S and S.get('i') != B.get('i') or 'ans' not in B else '遍历结束'),
        'pre ^= 1 << x': '数字 `{x}` 出现一次，翻转第 `{x}` 位：`{B.pre:06b}` → ==`{pre:06b}`==',
        'ans = max': lambda S, B, ret: _ans_cap(S, B),
        'if pos[pre] == n': lambda S, B, ret: (f'`pos[{S.pre:06b}]` 还是 n → 首次出现，要记录' if S.pos[S.pre] == S.n
                                                else f'`pos[{S.pre:06b}] = {S.pos[S.pre]}` 已有记录，保留更靠左的（子串更长）'),
        'pos[pre] = i': '记录 `pos[{pre:06b}] = {i}`',
        'return ans': '最长超赞子串长度 `{ans}`',
    },
    skip=['max(i - pos[pre ^'],
    max_steps=60,
    cards=dict(
        one_liner='子串异或值为 0 或只有一位是 1，就能重排成回文',
        complexity='时间 `O(nD)`，空间 `O(2^D)`，D = 10',
        problem=['超赞子串：非空，且交换字符后能变成回文串',
                 '求 `s` 里最长超赞子串的长度，`s` 只含数字',
                 '示例：`"3242415"` → `5`（`"24241"` → `"24142"`）'],
        quote='如果从 s[i] 到 s[j] 的子串长度是奇数，要使子串可以重排成回文串，必须恰好有一个数字的出现次数是奇数，其余数字的出现次数都是偶数，所以 pre[j] ^ pre[i] = 2^k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['10 位二进制 `pre` 记录每个数字出现次数的奇偶性',
              '偶数长度：每个数字都是偶数次 → `pre[i] == pre[j]`',
              '奇数长度：恰有一个奇数次 → `pre[i] == pre[j] ^ 2^k`，枚举 k',
              '`j` 固定时 `i` 越小越长 → 只存==首次==出现的下标'],
        summary=['时间 `O(nD)`，空间 `O(2^D)`',
                 '`pos[0] = -1` 不能漏，否则从下标 0 开始的子串会漏掉',
                 '先用当前 `pre` 查表更新答案，再记录首次下标',
                 '偶数情况是 `pos[pre]`，奇数情况要枚举翻转每一位',
                 '前置：1177 的异或前缀和；同类：1371、1915'],
    ),
)
