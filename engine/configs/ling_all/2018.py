BOARD = [['#', 'c', '#'], ['a', ' ', ' ']]
WORD = 'ca'


def _rc(S):
    """当前格子 (行, 列)；行扫描时 row 是当前行对象，列扫描时 i 是行号"""
    if 'i' in S:
        return (S['i'], S['j']) if 'j' in S else None
    if 'row' in S and 'j' in S:
        r = next((k for k, x in enumerate(S['board']) if x is S['row']), None)
        return (r, S['j']) if r is not None else None
    return None


def _cur_r(S):
    rc = _rc(S)
    return None if rc is None else (min(rc[0], len(S['board']) - 1) if 'i' in S else rc[0])


def _cur_c(S):
    rc = _rc(S)
    return None if rc is None else (rc[1] if rc[1] < len(S['board'][0]) else None) if 'i' not in S else rc[1]


_SLOT_LINES = set(range(12, 22)) | set(range(30, 40))


def _slot(S, r, c, v):
    if v == '#' or 'ok1' not in S or 'j' not in S or S.get('_line') not in _SLOT_LINES:
        return None
    if 'i' in S:
        if c != S['j'] or 'i0' not in S or S['i'] > len(S['board']):
            return None
        lo, hi = S['i0'], S['i']
        if not (lo <= r <= hi) or r >= len(S['board']):
            return None
    else:
        if 'j0' not in S or r != _rc(S)[0]:
            return None
        lo, hi = S['j0'], S['j']
        if not (lo <= c <= hi):
            return None
    return 'red' if not (S['ok1'] or S['ok2']) else 'blue'


def _txt(S):
    if 'ok1' not in S or 'k' not in S or S.get('_line') not in _SLOT_LINES:
        return f"word = `{WORD}`：两个 `#` 之间的一段叫槽位，要把 word ==正着或倒着==恰好填进去"
    lab = '列' if 'i' in S else '行'
    return f"槽位起点 `{'i0' if 'i' in S else 'j0'} = {S['i0'] if 'i' in S else S['j0']}`（{lab}扫描）    正序 `ok1 = {S['ok1']}`    倒序 `ok2 = {S['ok2']}`"


CONFIG = dict(
    num=2018, title='判断单词是否能放入填字游戏内', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='按行按列扫描槽位 · 正倒序匹配（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def placeWordInCrossword(self, board: List[List[str]], word: str) -> bool:
        m, n, k = len(board), len(board[0]), len(word)
        # 遍历行
        for row in board:
            j = 0
            while j < n:
                if row[j] == '#':
                    j += 1
                    continue
                # 遍历并匹配两个 # 之间的字符
                j0, ok1, ok2 = j, True, True
                while j < n and row[j] != '#':  # 注意这里的 j 就是外层循环的 j，因此整体复杂度是线性的
                    if j - j0 >= k or row[j] != ' ' and row[j] != word[j - j0]:  # 正序匹配 word
                        ok1 = False
                    if j - j0 >= k or row[j] != ' ' and row[j] != word[k - 1 - j + j0]:  # 倒序匹配 word
                        ok2 = False
                    j += 1
                if (ok1 or ok2) and j - j0 == k:  # 只要正序和倒序中有一个匹配成功，且两个 # 之间的字符长度恰好为 word 的长度，就返回 true
                    return True
                j += 1

        # 遍历列（同上）
        for j in range(n):
            i = 0
            while i < m:
                if board[i][j] == '#':
                    i += 1
                    continue
                i0, ok1, ok2 = i, True, True
                while i < m and board[i][j] != '#':
                    if i - i0 >= k or board[i][j] != ' ' and board[i][j] != word[i - i0]:
                        ok1 = False
                    if i - i0 >= k or board[i][j] != ' ' and board[i][j] != word[k - 1 - i + i0]:
                        ok2 = False
                    i += 1
                if (ok1 or ok2) and i - i0 == k:
                    return True
                i += 1
        return False
''',
    call=f'Solution().placeWordInCrossword({BOARD}, {WORD!r})',
    expect=True,
    max_steps=110,
    skip=['j = 0', 'i = 0', 'continue', 'j += 1', 'i += 1'],
    views=[
        dict(type='grid', var='board', label='board（蓝 = 槽位已扫格子，红 = 已失败，黄框 = 当前格）', cell=100, h=340,
             color=_slot, cursors=[(_cur_r, _cur_c, 'yellow')]),
        dict(type='string', var='word', label='word', cell=70, h=130),
        dict(type='text', fn=_txt, size=24, h=60),
    ],
    watch=[('j', 'j', 'yellow'), ('j0', 'j0', 'blue'), ('i0', 'i0', 'blue'), ('ok1', 'ok1', 'green'), ('ok2', 'ok2', 'pink')],
    captions={
        'm, n, k = ': '`m = {m}` 行，`n = {n}` 列，单词长度 `k = {k}`',
        'for row in board': '遍历每一行：把行里两个 `#` 之间的连续格子当作一个槽位',
        'while j < n:': lambda S, B, r: ('这一行扫完了' if S.j >= S.n else f'`j = {S.j}`：还在这一行里，继续找下一个槽位'),
        "if row[j] == '#'": lambda S, B, r: (f"`row[{S.j}] = '#'` → 障碍不属于任何槽位，跳过" if S.row[S.j] == '#'
                                             else f"`row[{S.j}] = '{S.row[S.j]}'` 不是 `#` → 这里是槽位的起点"),
        'j0, ok1, ok2': '槽位起点 `j0 = {j}`；先假设正序、倒序都能匹配：`ok1 = ok2 = True`',
        'while j < n and row[j]': lambda S, B, r: (f"`row[{S.j}] = '{S.row[S.j]}'`，还在槽位里，继续匹配" if S.j < S.n and S.row[S.j] != '#'
                                                   else '碰到 `#` 或行尾：槽位结束，槽位长度 = `j - j0`'),
        '# 正序匹配': lambda S, B, r: (f"槽位已经比单词长（`{S.j - S.j0} >= {S.k}`）→ 正序失败，`ok1 = False`" if S.j - S.j0 >= S.k
                                       else f"格子是 `'{S.row[S.j]}'`，单词第 {S.j - S.j0} 个字母是 `'{S.word[S.j - S.j0]}'`："
                                            + ('空格可以填，或者字母相同 → 正序继续' if S.row[S.j] in (' ', S.word[S.j - S.j0]) else '字母冲突 → 正序失败')
                                       ),
        '# 倒序匹配': lambda S, B, r: (f"槽位已经比单词长 → 倒序失败，`ok2 = False`" if S.j - S.j0 >= S.k
                                       else f"倒序：格子 `'{S.row[S.j]}'` 对 `word[{S.k - 1 - S.j + S.j0}] = '{S.word[S.k - 1 - S.j + S.j0]}'`："
                                            + ('可以 → 倒序继续' if S.row[S.j] in (' ', S.word[S.k - 1 - S.j + S.j0]) else '字母冲突 → 倒序失败')),
        'ok1 = False': '`ok1 = False`：正序放不下',
        'ok2 = False': '`ok2 = False`：倒序放不下',
        '# 只要正序和倒序': lambda S, B, r: (f"槽位长 `{S.j - S.j0}`，单词长 `{S.k}`，`ok1 = {S.ok1}`、`ok2 = {S.ok2}`"
                                            + (' → ==恰好填入，返回 True==' if (S.ok1 or S.ok2) and S.j - S.j0 == S.k else ' → 这个槽位不行，继续找')),
        '# 遍历列': '行里没有可放的槽位，换成按列扫描，做法同上',
        'for j in range(n)': '按列扫描：`j = {j}` 列',
        'i0, ok1, ok2': '槽位起点 `i0 = {i}`；先假设正序、倒序都能匹配',
        'while i < m and board': lambda S, B, r: (f"`board[{S.i}][{S.j}] = '{S.board[S.i][S.j]}'`，还在槽位里，继续匹配" if S.i < S.m and S.board[S.i][S.j] != '#'
                                                  else '碰到 `#` 或列尾：槽位结束，槽位长度 = `i - i0`'),
        'word[i - i0]': lambda S, B, r: (f"槽位已经比单词长 → 正序失败，`ok1 = False`" if S.i - S.i0 >= S.k
                                         else f"格子 `'{S.board[S.i][S.j]}'` 对单词第 {S.i - S.i0} 个字母 `'{S.word[S.i - S.i0]}'`："
                                              + ('空格可以填，或字母相同 → 正序继续' if S.board[S.i][S.j] in (' ', S.word[S.i - S.i0]) else '字母冲突 → 正序失败')),
        'word[k - 1 - i + i0]': lambda S, B, r: (f"槽位已经比单词长 → 倒序失败，`ok2 = False`" if S.i - S.i0 >= S.k
                                                 else f"倒序：格子 `'{S.board[S.i][S.j]}'` 对 `word[{S.k - 1 - S.i + S.i0}] = '{S.word[S.k - 1 - S.i + S.i0]}'`："
                                                      + ('可以 → 倒序继续' if S.board[S.i][S.j] in (' ', S.word[S.k - 1 - S.i + S.i0]) else '字母冲突 → 倒序失败')),
        'if (ok1 or ok2) and i - i0 == k': lambda S, B, r: (f"槽位长 `{S.i - S.i0}`，单词长 `{S.k}`，`ok1 = {S.ok1}`、`ok2 = {S.ok2}`"
                                                            + (' → ==恰好填入，返回 True==' if (S.ok1 or S.ok2) and S.i - S.i0 == S.k else ' → 这个槽位不行，继续找')),
        'return True': '找到了能放单词的槽位，返回 `True`',
        'return False': '所有槽位都不行，返回 `False`',
    },
    cards=dict(
        one_liner='把两个 # 之间当成槽位，正着倒着各试一次，长度要恰好相等',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`board` 里有字母、空格 `\' \'` 和障碍 `\'#\'`，问单词能否水平或竖直（正反方向都行）填进去',
                 '要求：不碰 `#`、字母与已有字母匹配、==两端紧邻的格子必须是 `#` 或边界==',
                 '示例：`[["#","c","#"],["a"," "," "]]`，`"ca"` → `true`（第 1 列从上往下）'],
        quote='遍历每一行和每一列，将两个 # 之间的字符当作一个槽位（矩阵边界也视作 #），我们要做的就是遍历（正序+倒序）每个槽位，判断 word 能否恰好填入该槽位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['槽位 = 两个 `#`（或边界）之间的一段，两端自然就紧邻 `#`',
              '槽位里每个格子：空格可填，字母必须和单词对应位置相同',
              '同时跑 `ok1`（正序）和 `ok2`（倒序），最后看槽位长度 `j - j0 == k`'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python（Go 的 `for ; j < n && ...; j++` 共用外层 `j`，转写成 `while` 并手动 `j += 1`）',
                 '内层 while 与外层共用下标 `j`，每个格子只扫一次，所以是线性的',
                 '易错：槽位长度必须 `== k`；碰到 `#` 结束后外层要再 `j += 1` 跳过它'],
    ),
)
