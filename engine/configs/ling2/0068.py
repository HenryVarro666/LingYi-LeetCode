WORDS = ["This", "is", "an", "example", "of", "text", "justification."]
MAXW = 16
ROWC = ['blue', 'pink', 'green', 'purple', 'orange', 'cyan']


def _row_of_word(S):
    """word index -> finished row index (words already placed into ans)"""
    out, k = {}, 0
    ans = S.get('ans') or []
    for r, line in enumerate(ans):
        for _ in line.split():
            out[k] = r
            k += 1
    return out


def _cur_end(S):
    """words[start:end] are in the line currently being built"""
    return S.get('i', 0)


def _words(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'words（同色 = 同一行；黄框 = 正在组的这一行，下标 i 指向下一个要尝试的单词）', 22, T['muted'], bold=True)
    ws = S.get('words') or WORDS
    done = _row_of_word(S)
    st = S.get('start')
    i = S.get('i')
    unit = 17
    gap = 14
    total = sum(len(w) * unit + 24 for w in ws) + gap * (len(ws) - 1)
    X = x0 + 20 + max(0, (x1 - x0 - 40 - total) / 2)
    Y = y0 + 50
    for k, w in enumerate(ws):
        wd = len(w) * unit + 24
        if k in done:
            fill, tc = T[ROWC[done[k] % len(ROWC)]], T['bg']
        elif st is not None and i is not None and st <= k < i:
            fill, tc = T['yellow'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((X, Y, X + wd, Y + 50), fill=fill, r=8, outline=T['border'])
        cv.text((X + wd / 2, Y + 25), w, 24, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + wd / 2, Y + 56), k, 18, T['dim'], anchor='mt', mono=True)
        if k == i:
            cv.tri_up(X + wd / 2, Y + 82, 9, T['blue'])
            cv.text((X + wd / 2, Y + 96), 'i', 22, T['blue'], anchor='mt', bold=True)
        X += wd + gap
    if i is not None and i >= len(ws):
        px = min(X + 10, x1 - 46)
        cv.tri_up(px, Y + 82, 9, T['blue'])
        cv.text((px, Y + 96), 'i = n', 22, T['blue'], anchor='mt', bold=True)


def _ruler(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    st, i = S.get('start'), S.get('i')
    if st is None or 'sum_len' not in S:
        return
    ws = S['words']
    mw = S['maxWidth']
    ln = S.get('_line')
    line = ' '.join(ws[st:i])
    cand = ''
    if ln == 9 and i < len(ws):
        cand = ' ' + ws[i] if line else ws[i]
    cell = min(56, (x1 - x0 - 60) / (mw + 6))
    sx = x0 + 30
    Y = y0 + 44
    cv.text((x0 + 18, y0 + 4), f'这一行最少要占 sum_len = {S["sum_len"]} 格（单词之间先放 1 个空格），上限 maxWidth = {mw}', 22, T['muted'], bold=True)
    full = line + cand
    n = max(mw, len(full))
    for k in range(n):
        X = sx + k * cell
        if k < len(line):
            ch = line[k]
            fill = T['yellow'] if ch != ' ' else T['panel2']
            tc = T['bg'] if ch != ' ' else T['dim']
        elif k < len(full):
            ch = full[k]
            over = k >= mw
            fill = T['red'] if over else T['cyan']
            tc = T['bg']
        else:
            ch = ''
            fill, tc = T['panel'], T['dim']
        cv.rect((X + 2, Y, X + cell - 2, Y + cell * 1.1), fill=fill, r=5, outline=T['border'])
        if ch:
            cv.text((X + cell / 2, Y + cell * 0.55), ch if ch != ' ' else '␣', int(cell * 0.55), tc, anchor='mm', bold=True, mono=True)
    edge = sx + mw * cell
    cv.line([(edge, Y - 10), (edge, Y + cell * 1.1 + 10)], T['red'], 4)
    cv.text((edge, Y + cell * 1.1 + 14), f'maxWidth = {mw}', 20, T['red'], anchor='mt', bold=True)
    if cand:
        ok = len(full) <= mw
        msg = f"再放 `{ws[i]}` 要 `{S['sum_len']} + {len(ws[i])} + 1 = {S['sum_len'] + len(ws[i]) + 1}` 格 → " + ('==放得下==' if ok else '==放不下==，这一行到此为止')
        cv.rich(x0 + 30, Y + cell * 1.1 + 46, msg, x1 - x0 - 60, size=26, accent=T['orange'])


def _ans(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ans = S.get('ans')
    if ans is None:
        return
    mw = S['maxWidth']
    cv.text((x0 + 18, y0 + 4), 'ans（␣ = 空格，每行恰好 maxWidth 个字符）', 22, T['muted'], bold=True)
    cell = min(56, (x1 - x0 - 60) / (mw + 6))
    sx = x0 + 30
    for r, line in enumerate(ans):
        Y = y0 + 40 + r * (cell * 1.1 + 10)
        new = B.get('ans') is not None and r >= len(B['ans'])
        c = T[ROWC[r % len(ROWC)]]
        for k, ch in enumerate(line):
            X = sx + k * cell
            fill = c if ch != ' ' else T['panel2']
            cv.rect((X + 2, Y, X + cell - 2, Y + cell * 1.1), fill=fill, r=5,
                    outline=T['yellow'] if new else T['border'], width=2 if new else 1)
            cv.text((X + cell / 2, Y + cell * 0.55), ch if ch != ' ' else '␣', int(cell * 0.55),
                    T['bg'] if ch != ' ' else T['dim'], anchor='mm', bold=True, mono=True)


def _formula(S, B):
    ln = S.get('_line')
    if ln == 28 and 'avg' in S:
        if S['rem'] == 0:
            return f"`rem = 0`：空格正好平均，每个空隙 `spaces` = {S['avg'] + 1} 个"
        return (f"`spaces` = {S['avg'] + 1} 个空格；前 `rem = {S['rem']}` 个空隙用 `spaces + ' '`（{S['avg'] + 2} 个）")
    if ln in (23, 24) and 'avg' in S:
        return (f"`extra_spaces = {S['extra_spaces']}` 分给 `gaps = {S['gaps']}` 个空隙："
                f"每个 `{S['avg']} + 1`，前 `rem = {S['rem']}` 个再多 1")
    if ln in (13, 14, 17, 18, 19, 20) and 'extra_spaces' in S:
        g = S.get('gaps')
        return f"剩余空格 `extra_spaces = {S['extra_spaces']}`" + (f"，空隙 `gaps = {g}`" if g is not None and ln != 13 else '')
    return ''


def _cap_outer(S, B, ret):
    if B.i < B.n:
        return f'`i = {B.i} < n`：还有单词 → 开始组新的一行（==分组循环的外层==）'
    return '`i == n`：所有单词都排好了'


def _cap_inner(S, B, ret):
    i, n, ws, sl, mw = B.i, B.n, B.words, B.sum_len, B.maxWidth
    if i >= n:
        return '`i == n`：没有单词了 → 这一组结束'
    need = sl + len(ws[i]) + 1
    if need <= mw:
        return f'`{sl} + len("{ws[i]}") + 1 = {need} ≤ {mw}` → 放得下，加入这一行'
    return f'`{sl} + len("{ws[i]}") + 1 = {need} > {mw}` → ==放不下==，这一组结束'


def _cap_special(S, B, ret):
    if S.gaps == 0 and S.i == S.n:
        return '只有一个单词，并且是最后一行 → ==左对齐==，末尾补空格'
    if S.gaps == 0:
        return '这一行只有一个单词 → ==左对齐==，末尾补空格'
    if S.i == S.n:
        return '`i == n`：最后一行 → ==左对齐==，单词间只放 1 个空格'
    return f'`gaps = {S.gaps}` 且不是最后一行 → 一般情况：两端对齐'


def _cap_append(S, B, ret):
    if S._line == 19:
        return f'第 `{len(S.ans)}` 行排好：`"{S.row}"`'
    if S.rem == 0:
        return f'`rem = 0`：每个空隙都是 `{len(S.spaces)}` 个空格 → 第 `{len(S.ans)}` 行：`"{S.row}"`'
    return (f'前 `rem = {S.rem}` 个空隙用 `{len(S.spaces) + 1}` 个空格，其余用 `{len(S.spaces)}` 个 → '
            f'第 `{len(S.ans)}` 行：`"{S.row}"`')


CONFIG = dict(
    num=68, title='文本左右对齐', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='分组循环',
    tags=['面试经典150'],
    code='''
class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        ans = []
        n = len(words)
        i = 0
        while i < n:
            start = i  # 这一行第一个单词的下标
            sum_len = -1  # 第一个单词之前没有空格
            while i < n and sum_len + len(words[i]) + 1 <= maxWidth:
                sum_len += len(words[i]) + 1  # 单词之间至少要有一个空格
                i += 1

            extra_spaces = maxWidth - sum_len  # 这一行剩余未分配的空格个数
            gaps = i - start - 1  # 这一行单词之间的空隙个数（单词个数减一）

            # 特殊情况：如果只有一个单词，或者是最后一行，那么左对齐，末尾补空格
            if gaps == 0 or i == n:
                row = ' '.join(words[start: i]) + ' ' * extra_spaces  # 末尾补空格
                ans.append(row)
                continue

            # 一般情况：把 extra_spaces 个空格均匀分配到 gaps 个空隙中（靠左的空格更多）
            avg, rem = divmod(extra_spaces, gaps)
            spaces = ' ' * (avg + 1)  # +1 表示加上单词之间已有的一个空格
            # 前 rem 个空隙多一个空格
            row = (spaces + ' ').join(words[start: start + rem + 1]) + \\
                  spaces + spaces.join(words[start + rem + 1: i])
            ans.append(row)
        return ans
''',
    call=f'Solution().fullJustify({WORDS!r}, {MAXW})',
    expect=["This    is    an", "example  of text", "justification.  "],
    views=[
        dict(type='text', fn=_formula, h=56),
        dict(type='custom', draw=_words, h=180),
        dict(type='custom', draw=_ruler, h=190),
        dict(type='custom', draw=_ans, h=230),
    ],
    skip=['i += 1', 26, 27],
    watch=[('start', 'start', 'yellow'), ('i', 'i', 'blue'), ('sum_len', 'sum_len'), ('extra', 'extra_spaces'),
           ('gaps', 'gaps')],
    captions={
        'ans = []': '`ans` 收集每一行',
        'n = len(words)': '`n = {n}` 个单词，每行宽 `maxWidth = {maxWidth}`',
        'i = 0': '`i` 指向下一个要放的单词',
        'while i < n:': _cap_outer,
        'start = i': '这一行从 `words[{start}] = "{words[start]}"` 开始',
        'sum_len = -1': lambda S, B, ret: ('`sum_len = -1`：每个单词都按「==1 个空格 + 单词==」计入，第一个单词前面多算的那个空格正好抵消'
                                           if not S.ans else '`sum_len = -1`，重新开始累计这一行'),
        'while i < n and sum_len': _cap_inner,
        'sum_len += len': '`sum_len += {len(words[i])} + 1` → {sum_len}，`i` 右移',
        'extra_spaces = maxWidth': '还剩 `extra_spaces = {maxWidth} − {sum_len} = {extra_spaces}` 个空格没分配',
        'gaps = i - start - 1': '这一行有 `{i - start}` 个单词 → `gaps = {gaps}` 个空隙',
        'if gaps == 0 or i == n': _cap_special,
        "row = ' '.join": '单词间放 1 个空格，末尾补 `{extra_spaces}` 个：`"{row}"`',
        'ans.append(row)': _cap_append,
        'continue': '`continue`：直接去组下一行',
        'avg, rem = divmod': '`divmod({extra_spaces}, {gaps}) = ({avg}, {rem})`：每个空隙至少 `{avg}` 个，前 `{rem}` 个再多 1',
        "spaces = ' ' * (avg + 1)": '`spaces` = ==`{avg} + 1` = {len(spaces)}== 个空格（+1 是本来就有的那个）',
        'return ans': '全部排完，返回 `{len(ans)}` 行',
    },
    cards=dict(
        one_liner='分组循环：内层找出一行最多放几个词，外层负责分配空格',
        complexity='时间 `O(L)`，`L` 为所有单词长度之和；空间 `O(1)`（不计答案）',
        problem=['把单词排成每行==恰好== `maxWidth` 个字符的文本，每行尽量多放单词',
                 '空格尽量均匀分配，分不匀时==左边的空隙多==',
                 '最后一行、以及只有一个单词的行：左对齐，末尾补空格',
                 f'示例：`{WORDS}`，`maxWidth = {MAXW}`'],
        quote='外层循环负责遍历组之前的准备工作（记录开始位置），和遍历组之后的统计工作（更新答案）。内层循环负责遍历组，找出这一组最远在哪结束。',
        quote_src='—— 灵茶山艾府题解 · 分组循环',
        idea=['内层：从第二个单词起，每个单词前面至少一个空格，`sum_len += len + 1`',
              '外层：`extra_spaces` 分给 `gaps` 个空隙，`divmod` 得到 `avg` 和 `rem`',
              '前 `rem` 个空隙多一个空格 → 前 `rem + 1` 个单词用 `avg + 2` 个空格连接'],
        summary=['时间 `O(L)`：每个单词只进出一次内层循环',
                 '分组循环的好处：==不需要特判最后一组==（易错点）',
                 '`sum_len` 初始为 `-1`：第一个单词前面没有空格',
                 '最后一行和单词数为 1 的行都左对齐，统一用 `gaps == 0 or i == n` 处理',
                 '同类题：分组循环题单（1446、1869、2414 等）'],
    ),
)
