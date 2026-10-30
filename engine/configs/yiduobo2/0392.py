S_IN, T_IN = 'abc', 'ahbgdc'
COLS = sorted(set(S_IN + T_IN))   # 只画出现过的字母列


def _old_now(S):
    """当前 char 查表时用的行号：按 s 前面的字母模拟一遍"""
    f, s, ch = S['f'], S['s'], S.get('char')
    if ch is None or ch not in s:
        return None
    r = 0
    for c in s[:s.index(ch)]:
        r = f[r][ord(c) - 97]
        if r is None:
            return None
    return r


def _cell(S):
    ln = S.get('_line')
    if ln == 6 and 'index' in S:
        return S['index'], COLS.index(S['t'][S['index']])
    if ln in (9, 10, 11) and S.get('char') is not None:
        r = S['now'] if ln == 9 else _old_now(S)
        if r is not None:
            return r, COLS.index(S['char'])
    return None


def _color(S, i, j, v):
    ln = S.get('_line')
    if ln == 5 and i == S.get('index'):
        return 'purple'
    if ln in (10, 11) and isinstance(S.get('now'), int) and i == S['now']:
        return 'cyan'
    return None


def _hits(S):
    """沿着 now 的跳跃链，已经匹配到的 t 下标"""
    now = S.get('now')
    if not isinstance(now, int) or now == 0:
        return set()
    r, out = 0, set()
    for c in S['s']:
        r = S['f'][r][ord(c) - 97]
        if r is None:
            break
        out.add(r - 1)
        if r == now:
            break
    return out


def _t_color(S, k, v):
    if S.get('_line') in (5, 6) and k == S.get('index'):
        return 'blue'
    if k in _hits(S):
        return 'green'
    return None


def _q(S, B, ret):
    old, ch, now = B.now, S.char, S.now
    if now is None:
        return f"`f[{old}]['{ch}'] = None`：t 中下标 ≥ {old} 的部分==没有== `'{ch}'`"
    return f"`now = f[{old}]['{ch}'] = {now}`：`'{ch}'` 在第 {now} 个位置（下标 {now - 1}），==一步跳过去=="


CONFIG = dict(
    num=392, title='判断子序列', difficulty='Easy', category='双指针',
    author='yiduobo', technique='预处理「下一次出现位置」表 + 跳跃',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def isSubsequence(self, s, t):
        f = [[None] * 26 for _ in range(len(t) + 1)]
        for index in range(len(t) - 1, -1, -1):
            f[index] = f[index + 1][:]
            f[index][ord(t[index]) - 97] = index + 1

        now = 0
        for char in s:
            now = f[now][ord(char) - 97]
            if not now:
                return False

        return True
''',
    call=f'Solution().isSubsequence("{S_IN}", "{T_IN}")',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"`s = \"{S['s']}\"`：正在匹配 `char = '{S['char']}'`（s 的第 {S['s'].index(S['char'])} 个字母）"
                                        if S.get('_line', 0) >= 9 and S.get('char') else f"`s = \"{S['s']}\"`，`t = \"{S['t']}\"`：先预处理 t"), size=26),
        dict(type='string', var='t', label='t（蓝 = 正在填的行对应的字母，绿 = 跳到的匹配位置）', cell=72, h=200,
             pointers={"index if _line in (4, 5, 6) else None": 'blue'}, pointer_labels={"index if _line in (4, 5, 6) else None": 'index'},
             color=_t_color),
        dict(type='table', var=lambda S: [[row[ord(ch) - 97] for ch in COLS] for row in S['f']] if 'f' in S else None,
             label="f[i][c] = 下标 ≥ i 的第一个 c 的下标 + 1（· = None）", cell=56, h=450,
             rows=lambda S: list(range(len(S['t']) + 1)), cols=COLS,
             cursors=[(lambda S: (_cell(S) or (None, None))[0], lambda S: (_cell(S) or (None, None))[1], 'yellow')],
             color=_color),
    ],
    watch=[('index', lambda S: S['index'] if S['_line'] in (4, 5, 6) else None, 'blue'), ('char', 'char', 'pink'), ('now', 'now', 'cyan')],
    captions={
        3: "`f[i][c]`：t 中位置 i 之后第一次出现字母 c 的位置（==下标 + 1==），先全是 `None`",
        4: lambda S, B, ret: (f'从后往前，填第 `{S.index}` 行' if S.get('index') != B.get('index') or 'index' not in B
                              else '预处理完成：每个位置、每个字母的“下一次出现”都知道了'),
        5: lambda S, B, ret: (f'先==复制== `f[{S.index + 1}]`：其他字母下一次出现的位置和后一行一样' if S.index == len(S.t) - 1
                              else f'复制 `f[{S.index + 1}]` 到 `f[{S.index}]`'),
        6: "`t[{index}] = '{t[index]}'` 就在这里：`f[{index}]['{t[index]}'] = {index} + 1 = {index + 1}`",
        8: '`now = 0`：下次从 t 的下标 `now` 开始找',
        9: lambda S, B, ret: (f"要匹配 `'{S.char}'`：查表 `f[{S.now}]['{S.char}']`" if S.get('char') != B.get('char') or 'char' not in B
                              else 's 的每个字母都匹配上了'),
        10: _q,
        11: lambda S, B, ret: ('`now` 是 `None` → 匹配失败' if not S.now else f'`now = {S.now}` 不为空 → 继续匹配下一个字母'),
        12: '返回 `False`',
        14: 's 的每个字母都能在 t 上==跳==到 → 是子序列，返回 `True`',
    },
    max_steps=60,
    cards=dict(
        one_liner='预处理每个位置之后各字母第一次出现的位置，匹配时直接跳',
        complexity='预处理 `O(26·|t|)`，每个 s 只要 `O(|s|)`',
        problem=['判断 `s` 是否为 `t` 的==子序列==（删掉 t 的一些字符、不改变相对顺序得到 s）',
                 '示例：`s = "abc"`，`t = "ahbgdc"` → `true`',
                 '进阶：有大量 s（k ≥ 10 亿）依次询问，怎么改？'],
        before=[dict(heading='yiduobo 的第一步：贪心双指针', lines=[
            '若 `t[j] = t[k] = s[i]` 且 `j < k`，选 `t[j]` 匹配 `s[i]` ==显然更好==',
            '用 t[k] 能得到结果，换成 t[j] 也能；反过来则不一定',
            '于是两个指针从头扫：匹配成功才移动 s 的指针，t 的指针每次都动，`O(m + n)`'])],
        quote='设f[i][char]表示字符串t中，在位置i之后第一次出现char的位置……于是我们可以使用动态规划从后往前进行计算。',
        quote_src='—— yiduobo 题解（后续挑战）',
        idea=['只有小写字母 → 对 t 的每个位置预处理 26 个字母的“下一次出现位置”',
              '`f[i]` = 复制 `f[i + 1]`，再把 `t[i]` 那一列改成 `i + 1`',
              '询问时 `now = f[now][c]` 在 t 上跳跃，遇到 None 就失败'],
        result='`a → 1`，`b → 3`，`c → 6`：三次跳跃全部成功 → True ✓',
        summary=['预处理 `O(26·|t|)`，之后每个 s 只要 `O(|s|)` → 总计 `O(26·|t| + Σ|s|)`',
                 '存「下标 + 1」：`now` 正好是下次开始找的下标；找不到是 `None`，所以 `if not now` 只被 None 触发',
                 '对比灵神：灵神主写法是遍历 t 的双指针，进阶的 nxt 表把“找不到”记成 `n`',
                 '原文为 Python 2 风格，代码未改，仅删去 docstring；`ord(c) - 97` 是字母序号'],
    ),
)
