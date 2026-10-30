S0 = 'aaaaa'


def _in(S):
    return S.get('_inner', {})


def _ij(S):
    I = _in(S)
    if 'start' in I and 'end' in I:
        return I['start'], I['end']
    return None


def _ws(S):
    c = _ij(S)
    return None if c is None or S.get('_line', 0) < 20 else c[0]


def _we(S):
    c = _ij(S)
    return None if c is None or S.get('_line', 0) < 20 else c[1]


def _fcolor(S, r, c, v):
    ij = _ij(S)
    if ij is None or S.get('_line', 0) < 20:
        return None
    start, end = ij
    if (r, c) == (start, end):
        return 'yellow'
    I = _in(S)
    t, cp = I.get('t'), I.get('cut_pos')
    line = S.get('_line')
    if line in (28, 29, 30, 31, 32, 33) and t is not None and (r, c) == (start, start + t - 1):
        return 'blue'
    if line in (36, 37, 38, 39, 40, 41) and cp is not None and ((r, c) == (start, cp) or (r, c) == (cp + 1, end)):
        return 'green'
    return None


def _txt(S):
    I = _in(S)
    ij = _ij(S)
    if ij is None or S.get('_line', 0) < 20:
        if 'start' in I or S.get('_line', 0) >= 20:
            pass
        return '`f[start][end]` = 子串 `s[start..end]` 编码后的最短长度；`g[i][j]` = `s[i:]` 与 `s[j:]` 的最长公共前缀'
    start, end = ij
    sub = S['s'][start:end + 1]
    return f'子串 `s[{start}..{end}] = "{sub}"`，长 `{end - start + 1}`；先假设不压缩：`f = {end - start + 1}`'


def _cap_t(S, B, ret):
    I = _in(S)
    length, t = I['length'], I['t']
    return (f'试压缩前缀长度 `t = {t}`：`length % t = {length % t}` → ' +
            ('==能整除==，子串可能由前缀重复 `' + str(length // t) + '` 次得到' if length % t == 0 else '不整除，换下一个 `t`'))


def _cap_flag(S, B, ret):
    I = _in(S)
    start, t, p = I['start'], I['t'], I['p']
    g = I['g'][start][p]
    return f'`g[{start}][{p}] = {g}` ' + ('≥' if g >= t else '<') + f' `t = {t}`：' + ('这一块和前缀相同' if g >= t else '==不是重复==，放弃这个 `t`')


CONFIG = dict(
    num=471, title='编码最短长度的字符串', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 重复子串压缩 / 切分',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def encode(self, s):

        n = len(s)
        g = [[0] * n for _ in range(n)]
        for j in range(n - 1, 0, -1):
            for i in range(j - 1, -1, -1):
                if s[i] == s[j]:
                    if j == n - 1:
                        g[i][j] = 1
                    else:
                        g[i][j] = g[i + 1][j + 1] + 1
        
        f = [[None] * n for _ in range(n)]
        cut = [[False] * n for _ in range(n)]
        method = [[0] * n for _ in range(n)]
        for length in range(1, n + 1):
            for start in range(n - length + 1):
                end = start + length - 1
                f[start][end] = length
                if start == end:
                    continue
                for t in range(1, length):
                    if length % t == 0:
                        flag = True
                        for p in range(start + t, end + 1, t):
                            if g[start][p] < t:
                                flag = False
                                break
                        if flag:
                            abbr_len = f[start][start + t - 1] + len(str(length // t)) + 2
                            if f[start][end] > abbr_len:
                                f[start][end] = abbr_len
                                method[start][end] = t

                for cut_pos in range(start, end):
                    if f[start][cut_pos] + f[cut_pos + 1][end] < f[start][end]:
                        cut[start][end] = True
                        method[start][end] = cut_pos
                        f[start][end] = f[start][cut_pos] + f[cut_pos + 1][end]

        def generate(start, end):
            if cut[start][end]:
                return generate(start, method[start][end]) + generate(method[start][end] + 1, end)
            elif method[start][end] > 0:
                return str((end - start + 1) // method[start][end]) + '[' + generate(start, start + method[start][end] - 1)+ ']'
            else:
                return s[start : end + 1]

        return generate(0, n - 1)
''',
    call=f'Solution().encode({S0!r})',
    expect='5[a]',
    max_steps=64,
    skip=['n = len(s)', 'g = [[0]', 'f = [[None]', 'cut = [[False]', 'method = [[0]', 'end = start + length - 1',
          'for g_', 'for j in range(n - 1', 'for i in range(j - 1', 'if s[i] == s[j]', 'if j == n - 1', 'g[i][j] =',
          'if start == end', 'continue', 'flag = True', 'for p in range', 'for start in range', 'for t in range',
          'for cut_pos in range', 'flag = False', 'break', 'if flag', 'if length % t == 0', 'if g[start][p] < t', 'f[start][end] = length'],
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='string', var='s', label='s（框 = 当前子串 [start, end]）', cell=80, h=170, window=(_ws, _we)),
        dict(type='table', var='f', label='f[start][end]（黄 = 正在算，蓝 = 压缩时用的前缀，绿 = 切分的两半）', h=330, cell=70,
             rows=lambda S: [f'{k}' for k in range(len(S0))], cols=lambda S: [f'{k}' for k in range(len(S0))],
             color=_fcolor),
    ],
    watch=[('length', lambda S: _in(S).get('length'), 'yellow'), ('start', lambda S: _in(S).get('start'), 'blue'),
           ('end', lambda S: _in(S).get('end'), 'pink'), ('t', lambda S: _in(S).get('t'), 'cyan')],
    captions={
        'for length in range': lambda S, B, r: (f'按子串长度 `length = {S.length}` 从短到长算：长串要用到短串的结果'
                                                if S.get('length') != B.get('length') else '所有长度都算完了，`f[0][n-1]` 就是最短编码长度'),
        'f[start][end] = length': '`s[{start}..{end}]` 长 `{length}`：先假设不压缩，`f = {length}`',
        'if length % t == 0': _cap_t,
        'if g[start][p] < t': _cap_flag,
        'abbr_len =': '`t = {t}` 可整除，重复 `{length // t}` 次：压缩长 `{f[start][start + t - 1]} + {len(str(length // t))} + 2` = =={abbr_len}==',
        'if f[start][end] > abbr_len': lambda S, B, r: (f'当前 `f[{S.start}][{S.end}] = {S.f[S.start][S.end]}`，压缩要 `{S.abbr_len}` → ' +
                                                       ('==压缩更短==' if S.f[S.start][S.end] > S.abbr_len else '没有更短，不用压缩')),
        'f[start][end] = abbr_len': '压缩更短：`f[{start}][{end}]` = =={f[start][end]}==，`method` 记下前缀长度 `t = {t}`',
        'if f[start][cut_pos] + f': '切分：`{f[start][cut_pos]} + {f[cut_pos + 1][end]}` vs 当前 `{f[start][end]}`',
        'cut[start][end] = True': '切成两段更短：标记 `cut`',
        'f[start][end] = f[start][cut_pos] + ': '`f[{start}][{end}]` = =={f[start][end]}==',
        'def generate': '`f` 只给了最短长度，题目要字符串 → 用 `cut`/`method` 倒推构造',
        'if cut[start][end]': lambda S, B, r: ('这段是切分的 → 左右两半各自生成' if S.cut[S.start][S.end]
                                               else '没有切分，看是不是压缩'),
        'elif method[start][end] > 0': lambda S, B, r: (f'`method = {S.method[S.start][S.end]} > 0`：重复压缩 → ==次数[前缀编码]=='
                                                         if S.method[S.start][S.end] > 0 else '`method = 0`：不压缩，原样输出'),
        'return str((end': '`{ret}`：`次数 = {(end - start + 1) // method[start][end]}`，加上 `[` 前缀的编码 `]`',
        'return s[start': '不压缩，直接输出 `{ret}`',
        'return generate(0': '`f[0][{n - 1}] = {f[0][n - 1]}`：从 `[0][{n - 1}]` 出发，倒推出字符串',
    },
    cards=dict(
        one_liner='三种选择取最短：不压缩、重复压缩、切成两段',
        complexity='时间 `O(n^3)`~`O(n^4)`，空间 `O(n^2)`',
        problem=['把字符串 `s` 编码成 `k[encoded_string]`（`encoded_string` 重复 `k` 次）',
                 '编码后长度不变短就保持原样，返回==最短的编码字符串==',
                 '示例：`aaaaa` → `5[a]`；本视频就用这个'],
        quote='s[start : start + t]占据的空间一定要用f[start][start + t - 1]来表示，因此可能出现嵌套压缩的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[start][end]`：子串编码后的最短长度；三种转移：不压缩 `length`、压缩 `f[前缀] + 位数 + 2`、切分 `f[左] + f[右]`',
              '压缩要判断子串是否由长 `t` 的前缀重复：先预处理最长公共前缀 `g[i][j]`，再检查每隔 `t` 位的 `g ≥ t`',
              '动态规划后用 `cut`/`method` 数组倒推具体字符串（写完才发现要返回字符串）'],
        summary=['时间约 `O(n^3)`~`O(n^4)`，空间 `O(n^2)`；`n ≤ 150` 够用',
                 '前缀的长度必须用 `f[start][start+t-1]`，这样才会嵌套压缩，如 `2[2[ab]c]`',
                 '`method` 在压缩时记前缀长度 `t`，切分时记切分点 `cut_pos`，靠 `cut` 区分',
                 '原文为 Python 2 写法，整数除法 `/` 已改成 `//`（两处：`len(str(length // t))` 与 `generate` 里的次数）',
                 '省略了 `g` 的预处理循环的逐行动画（它只是算最长公共前缀）'],
    ),
)
