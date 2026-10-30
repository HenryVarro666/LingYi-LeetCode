def _rg(pos, m):
    out = set()
    for p in pos:
        out.update(range(p, p + m))
    return out


def _col(S, i, v):
    a, b = S.get('a', ''), S.get('b', '')
    if 'match_a' in S and 'p' in S and 'index' in S and 'nxt_a' in S and S['_line'] < 43:
        idx = S['index']
        if i == idx:
            return 'blue'
        if S['p'] > 0 and idx - S['p'] < i < idx:
            return 'yellow'
    if 'match_a' in S:
        ra = _rg(S['match_a'], len(a))
        rb = _rg([x for x in S['match_b'] if x >= 0], len(b))
        if 'q' in S and 'index' not in S:
            pass
        if i in ra and i in rb:
            return 'green'
        if i in ra:
            return 'yellow'
        if i in rb:
            return 'purple'
    return None


def _txt(S):
    a, b = S.get('a', ''), S.get('b', '')
    if 'p' in S and 'index' in S and 'nxt_a' in S and 'match_a' in S and S['_line'] < 38:
        return (f"同时扫描 s：a = `{a}` 已匹配 `p = {S['p']}` 个，b = `{b}` 已匹配 `q = {S['q']}` 个；"
                f"起点：match_a = `{S['match_a']}`，match_b = `{S['match_b']}`")
    if 'match_a' in S and 'q' in S and S['_line'] >= 38:
        extra = ''
        if S['p'] < len(S['match_a']):
            extra = f"；当前 a 起点 `match_a[{S['p']}] = {S['match_a'][S['p']]}`，q = {S['q']}"
        return f"match_a（黄）= `{S['match_a']}`，match_b（紫）= `{S['match_b']}`（首项是哨兵 −k−1）{extra}"
    if 'nxt_a' in S and 'nxt_b' not in S and 'f' in S:
        return f"建 a 的 next 数组：`f = {S['f']}`"
    return f"s = `{S.get('s')}`，a = `{a}`，b = `{b}`，k = {S.get('k')}"


def _g1(S, B, r):
    if S.p and S.t[S.p] != S.t[S.index]:
        return f'`t[{S.p}] = {S.t[S.p]}` ≠ `t[{S.index}] = {S.t[S.index]}` → ==p 退到 f[p-1]=={S.f[S.p - 1]}'
    return '不失配（或 p 已是 0），不回退'


def _wa(S, B, r):
    if S.p and S.a[S.p] != S.s[S.index]:
        return f'`a[{S.p}]` ≠ `s[{S.index}]`：a 失配 → ==p 退到 nxt_a[p-1]=={S.nxt_a[S.p - 1]}'
    return 'a 不用回退'


def _wb(S, B, r):
    if S.q and S.b[S.q] != S.s[S.index]:
        return f'`b[{S.q}]` ≠ `s[{S.index}]`：b 失配 → ==q 退到 nxt_b[q-1]=={S.nxt_b[S.q - 1]}'
    return 'b 不用回退'


def _near(S, B, r):
    if S.q + 1 < len(S.match_b) and S.match_b[S.q + 1] <= S.match_a[S.p]:
        return f'`match_b[{S.q + 1}] = {S.match_b[S.q + 1]}` ≤ `{S.match_a[S.p]}`：b 的起点还在 a 左边 → ==q 右移=='
    return f'`match_b[q]` 已是 ≤ 当前 a 起点 `{S.match_a[S.p]}` 的最大 b 起点（q = {S.q}）'


def _l1(S, B, r):
    d = S.match_a[S.p] - S.match_b[S.q]
    if S.q != 0 and d <= S.k:
        return f'左边最近的 b：`{S.match_a[S.p]} − {S.match_b[S.q]} = {d} ≤ {S.k}` → ==美丽下标=='
    return '左边没有 b（q = 0 是哨兵）或距离 > k'


def _l2(S, B, r):
    if S.q + 1 < len(S.match_b):
        d = S.match_b[S.q + 1] - S.match_a[S.p]
        return (f'右边最近的 b：`{S.match_b[S.q + 1]} − {S.match_a[S.p]} = {d} ≤ {S.k}` → ==美丽下标==' if d <= S.k
                else f'右边最近的 b：距离 `{d} > {S.k}` → 不是')
    return '右边没有 b 了 → 不是'


CONFIG = dict(
    num=3006, title='找出数组中的美丽下标 I', difficulty='Medium', category='字符串',
    author='yiduobo', technique='KMP 同时扫描 + 单调指针找最近 b',
    code='''
class Solution(object):
    def beautifulIndices(self, s, a, b, k):

        def get_nxt(t):
            f = [0]
            p = 0
            for index in range(1, len(t)):
                while p and t[p] != t[index]:
                    p = f[p - 1]
                
                if t[p] == t[index]:
                    p += 1
                
                f.append(p)
            
            return f

        nxt_a = get_nxt(a)
        nxt_b = get_nxt(b)

        p = q = 0
        match_a = []
        match_b = [-k - 1]

        for index in range(len(s)):
            while p and a[p] != s[index]:
                p = nxt_a[p - 1]
            if a[p] == s[index]:
                p += 1
                if p == len(a):
                    match_a.append(index - p + 1)
                    p = nxt_a[p - 1]
            
            while q and b[q] != s[index]:
                q = nxt_b[q - 1]
            if b[q] == s[index]:
                q += 1
                if q == len(b):
                    match_b.append(index - q + 1)
                    q = nxt_b[q - 1]
        
        
        p = q = 0
        res = []
        while p < len(match_a):
            while q + 1 < len(match_b) and match_b[q + 1] <= match_a[p]:
                q += 1
            
            if q != 0 and match_a[p] - match_b[q] <= k:
                res.append(match_a[p])
            elif q + 1 < len(match_b) and match_b[q + 1] - match_a[p] <= k:
                res.append(match_a[p])

            p += 1
            
        
        return res
''',
    call="Solution().beautifulIndices('abxab', 'ab', 'x', 1)",
    expect=[3],
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='string', var='s', color=_col, h=190),
        dict(type='array', var='match_b', h=120, label='match_b'),
    ],
    watch=['index', 'p', 'q', ('match_a', 'match_a', 'yellow'), ('match_b', 'match_b', 'purple'), ('res', 'res', 'green')],
    skip=['p = q = 0', 'match_a = []', 'res = []', 'return f'],
    max_steps=130,
    captions={
        'nxt_a = get_nxt': '`a` 的 next 数组：`{nxt_a}`（最长相等前后缀长度）',
        'nxt_b = get_nxt': '`b` 的 next 数组：`{nxt_b}`',
        'f = [0]': '`f[i]`：t[:i+1] 的最长相等前后缀长度，`f[0] = 0`',
        'for index in range(1, len(t))': lambda S, B, r: ('next 表建完' if S.get('index') == B.get('index')
                                                          else f'建表：处理 `t[{S.index}]`'),
        'while p and t[p]': _g1,
        'f.append(p)': '`f = {f}`',
        'match_b = [-k - 1]': '`match_b` 先放一个==哨兵== `-k-1`：保证它离任何 a 起点都超过 k',
        'for index in range(len(s))': lambda S, B, r: ('s 扫描完了' if S.get('index') == B.get('index') and 'index' in B
                                                       else f'同时用 KMP 扫 a 和 b：`s[{S.index}] = {S.s[S.index]}`'),
        'while p and a[p]': _wa,
        'if a[p] == s[index]': lambda S, B, r: (f'`a[{S.p}] = {S.a[S.p]}` 与 `s[{S.index}] = {S.s[S.index]}` '
                                                + ('相等 → a 多匹配一个' if S.a[S.p] == S.s[S.index] else '不等 → a 这一轮没匹配上')),
        29: '`p` → {p}（a 多匹配一个字符）',
        54: '这个 a 起点检查完，换下一个：`p` → {p}',
        'if p == len(a)': lambda S, B, r: (f'`p = {S.p} == len(a)`：==a 完整出现一次==' if S.p == len(S.a) else f'`p = {S.p}` < `len(a) = {len(S.a)}`：还没匹配完'),
        'match_a.append': '记录 a 的起点 `index − p + 1`：`match_a = {match_a}`',
        'p = nxt_a[p - 1]': '`p` 退回 `nxt_a[p-1]` = {p}，允许下一次重叠匹配',
        'while q and b[q]': _wb,
        'if b[q] == s[index]': lambda S, B, r: (f'`b[{S.q}] = {S.b[S.q]}` 与 `s[{S.index}] = {S.s[S.index]}` '
                                                + ('相等 → b 多匹配一个' if S.b[S.q] == S.s[S.index] else '不等 → b 这一轮没匹配上')),
        37: '`q` → {q}（b 多匹配一个字符）',
        47: '`match_b[q+1]` 还在 a 起点左边：`q` → {q}',
        'if q == len(b)': lambda S, B, r: (f'`q = {S.q} == len(b)`：==b 完整出现一次==' if S.q == len(S.b) else f'`q = {S.q}` < `len(b) = {len(S.b)}`'),
        'match_b.append': '记录 b 的起点：`match_b = {match_b}`',
        'q = nxt_b[q - 1]': '`q` 退回 `nxt_b[q-1]` = {q}',
        'while p < len(match_a)': lambda S, B, r: (f'枚举 a 的第 `{S.p}` 个起点 `{S.match_a[S.p]}`' if S.p < len(S.match_a)
                                                   else '所有 a 的起点都检查完了'),
        'while q + 1 < len(match_b)': _near,
        'if q != 0 and': _l1,
        'elif q + 1': _l2,
        'res.append': '`res = {res}`',
        'return res': '美丽下标：`{res}`',
    },
    cards=dict(
        one_liner='KMP 一趟找出 a、b 的所有起点，再单调扫描比距离',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 中 a 的起点 `i`，若存在 b 的起点 `j` 使 `|j − i| ≤ k`，`i` 就是美丽下标',
                 '按从小到大返回所有美丽下标',
                 '本视频：`s=abxab, a=ab, b=x, k=1` → `[3]`'],
        quote='对于a在s中出现的所有起点下标以及b在s中出现的所有起点下标，若对于某个a的起点i，存在某个b的起点j与i的距离小于等于k，那么就将i加入到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['分别对 a、b 求 next 数组，扫一遍 s 同时跑两个 KMP，得到 `match_a`、`match_b`',
              '对每个 a 起点，只需看离它最近的两个 b：左边 `match_b[q]`，右边 `match_b[q+1]`',
              '`match_a` 递增 → `q` 也只增不减，均摊 `O(1)`；`match_b` 开头放哨兵 `-k-1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '哨兵 `-k-1` 让「左边没有 b」自然变成「距离 > k」，但代码里仍用 `q != 0` 区分',
                 '匹配成功后 `p = nxt_a[p-1]`，才能找到重叠的出现位置',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码本身 Python 3 可直接运行',
                 '对比灵神：灵神用 `kmp` 函数分别求位置；yiduobo 一趟同时扫 a、b，并用哨兵处理左边界'],
    ),
)
