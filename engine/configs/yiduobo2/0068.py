WORDS = ["Science", "is", "what", "we", "understand", "well", "enough"]
MAXW = 20
ROWC = ['blue', 'pink', 'green', 'purple', 'orange', 'cyan']


def _row_of_word(S):
    out, k = {}, 0
    for r, line in enumerate(S.get('res') or []):
        for _ in line.split():
            out[k] = r
            k += 1
    return out


def _words(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'words（同色 = 同一行；黄 = 当前行 [left, right)）', 22, T['muted'], bold=True)
    ws = S.get('words') or WORDS
    done = _row_of_word(S)
    lf, rt = S.get('left'), S.get('right')
    unit, gap = 15, 10
    total = sum(len(w) * unit + 20 for w in ws) + gap * (len(ws) - 1)
    X = x0 + 20 + max(0, (x1 - x0 - 40 - total) / 2)
    Y = y0 + 46
    for k, w in enumerate(ws):
        wd = len(w) * unit + 20
        if k in done:
            fill, tc = T[ROWC[done[k] % len(ROWC)]], T['bg']
        elif lf is not None and rt is not None and lf <= k < rt:
            fill, tc = T['yellow'], T['bg']
        else:
            fill, tc = T['panel2'], T['text']
        cv.rect((X, Y, X + wd, Y + 48), fill=fill, r=8, outline=T['border'])
        cv.text((X + wd / 2, Y + 24), w, 22, tc, anchor='mm', bold=True, mono=True)
        cv.text((X + wd / 2, Y + 54), k, 18, T['dim'], anchor='mt', mono=True)
        marks = []
        if k == lf:
            marks.append(('left', T['green']))
        if k == rt:
            marks.append(('right', T['pink']))
        for r, (nm, c) in enumerate(marks):
            if r == 0:
                cv.tri_up(X + wd / 2, Y + 80, 9, c)
            cv.text((X + wd / 2, Y + 94 + r * 24), nm, 20, c, anchor='mt', bold=True)
        X += wd + gap
    if rt is not None and rt >= len(ws):
        px = min(X + 10, x1 - 60)
        cv.tri_up(px, Y + 80, 9, T['pink'])
        cv.text((px, Y + 94), 'right = n', 20, T['pink'], anchor='mt', bold=True)


def _cells(cv, x, y, text, cell, color, T, new=False, limit=None):
    for k, ch in enumerate(text):
        X = x + k * cell
        over = limit is not None and k >= limit
        fill = T['red'] if over else (color if ch != ' ' else T['panel2'])
        cv.rect((X + 2, y, X + cell - 2, y + cell * 1.1), fill=fill, r=5,
                outline=T['yellow'] if new else T['border'], width=2 if new else 1)
        cv.text((X + cell / 2, y + cell * 0.55), ch if ch != ' ' else '␣', int(cell * 0.55),
                T['bg'] if (ch != ' ' or over) else T['dim'], anchor='mm', bold=True, mono=True)


def _build(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mw = S.get('maxWidth', MAXW)
    cell = min(44, (x1 - x0 - 60) / (mw + 4))
    sx = x0 + 30
    ln = S.get('_line')
    lf, rt = S.get('left'), S.get('right')
    if 'tmp_res' in S and ln in range(15, 35) and (ln >= 20 or ln in (15, 16, 17)):
        t = S['tmp_res']
        cv.text((x0 + 18, y0 + 4), f'tmp_res（逐段拼出这一行，长度 {len(t)} / {mw}）', 22, T['muted'], bold=True)
        for k in range(mw):
            X = sx + k * cell
            cv.rect((X + 2, y0 + 40, X + cell - 2, y0 + 40 + cell * 1.1), fill=T['panel'], r=5, outline=T['border'])
        _cells(cv, sx, y0 + 40, t, cell, T['yellow'], T)
        bt = B.get('tmp_res') if ln != 22 else ''
        if isinstance(bt, str) and len(t) > len(bt) and t.startswith(bt):
            X0 = sx + len(bt) * cell
            X1 = sx + len(t) * cell
            cv.rect((X0, y0 + 36, X1, y0 + 44 + cell * 1.1), outline=T['cyan'], width=3, r=6)
            cv.text(((X0 + X1) / 2, y0 + 50 + cell * 1.1), f'+{len(t) - len(bt)}', 20, T['cyan'], anchor='mt', bold=True)
    elif 'sum_len' in S and lf is not None and rt is not None:
        ws = S['words']
        line = ' '.join(ws[lf:rt])
        cand = ''
        if ln == 10 and rt < len(ws):
            cand = ' ' + ws[rt]
        cv.text((x0 + 18, y0 + 4), f'当前行至少占 sum_len = {S["sum_len"]} 格（词间 1 个空格），上限 {mw}', 22, T['muted'], bold=True)
        for k in range(max(mw, len(line + cand))):
            X = sx + k * cell
            cv.rect((X + 2, y0 + 40, X + cell - 2, y0 + 40 + cell * 1.1), fill=T['panel'], r=5, outline=T['border'])
        _cells(cv, sx, y0 + 40, line, cell, T['yellow'], T)
        if cand:
            _cells(cv, sx + len(line) * cell, y0 + 40, cand, cell, T['cyan'], T, limit=mw - len(line))
    else:
        return
    edge = sx + mw * cell
    cv.line([(edge, y0 + 30), (edge, y0 + 50 + cell * 1.1)], T['red'], 4)
    cv.text((edge + 8, y0 + 40), f'maxWidth', 18, T['red'], anchor='lt', bold=True)


def _res(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    res = S.get('res')
    if res is None:
        return
    mw = S['maxWidth']
    cv.text((x0 + 18, y0 + 4), 'res（每行恰好 maxWidth 个字符）', 22, T['muted'], bold=True)
    cell = min(44, (x1 - x0 - 60) / (mw + 4))
    for r, line in enumerate(res):
        new = B.get('res') is not None and r >= len(B['res'])
        _cells(cv, x0 + 30, y0 + 40 + r * (cell * 1.1 + 10), line, cell, T[ROWC[r % len(ROWC)]], T, new=new)


def _formula(S, B):
    ln = S.get('_line')
    if 'num_space' in S and ln in (28, 29, 30, 31, 32):
        return (f"每个空隙 `num_space = {S['num_space']}` 个空格，"
                f"前 `other_space = {S['other_space']}` 个空隙再多 1 个")
    if ln == 27:
        return f"`num_space = 1 + {B['other_space']} // {S['num_word'] - 1} = {S['num_space']}`（1 是必须的那个空格）"
    if ln in (20, 21, 22, 24) and 'num_word' in S:
        o = S.get('other_space')
        return f"这一行 `num_word = {S['num_word']}` 个词" + (f"，多出 `other_space = {o}` 个空格" if o is not None and ln != 20 else '')
    return ''


def _cap_inner(S, B, ret):
    r, ws, sl, mw, L = B.right, B.words, B.sum_len, B.maxWidth, B.len_list
    if r >= len(ws):
        return '`right == len(words)`：单词用完了'
    need = sl + L[r] + 1
    if need <= mw:
        return f'`{sl} + {L[r]} + 1 = {need} ≤ {mw}`：`"{ws[r]}"` 连同前面 1 个空格放得下'
    return f'`{sl} + {L[r]} + 1 = {need} > {mw}`：`"{ws[r]}"` ==放不下== → 这一行的词确定了'


def _cap_if_index(S, B, ret):
    i, o = S.index, S.other_space
    if i <= o:
        return f'第 `{i}` 个空隙：`{i} ≤ other_space = {o}` → ==多放 1 个空格=='
    return f'第 `{i}` 个空隙：`{i} > {o}` → 只放 `num_space` 个'


CONFIG = dict(
    num=68, title='文本左右对齐', difficulty='Hard', category='字符串',
    author='yiduobo', technique='贪心装词 · 余数空格分给左边',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def fullJustify(self, words, maxWidth):
        len_list = [len(word) for word in words]

        left = 0
        res = []
        while left < len(words):
            sum_len = len_list[left]
            right = left + 1
            while right < len(words) and sum_len + len_list[right] + 1 <= maxWidth:
                sum_len += len_list[right] + 1
                right += 1

            if right == len(words):
                tmp_res = ' '.join(words[left : right])
                tmp_res += ' ' * (maxWidth - len(tmp_res))
                res.append(tmp_res)
                break
            else:
                num_word = right - left
                other_space = maxWidth - sum_len
                tmp_res = words[left]

                if num_word == 1:
                    tmp_res += ' ' * other_space
                else:
                    num_space = 1 + other_space // (num_word - 1)
                    other_space %= (num_word - 1)
                    for index in range(1, num_word):
                        if index <= other_space:
                            tmp_res += ' '
                        tmp_res += ' ' * num_space + words[left + index]

                res.append(tmp_res)
                left = right
        return res
''',
    call=f'Solution().fullJustify({WORDS!r}, {MAXW})',
    expect=["Science  is  what we", "understand      well", "enough              "],
    views=[
        dict(type='text', fn=_formula, h=56),
        dict(type='custom', draw=_words, h=170),
        dict(type='custom', draw=_build, h=150),
        dict(type='custom', draw=_res, h=210),
    ],
    skip=['right += 1', 'right = left + 1', 31],
    watch=[('left', 'left', 'green'), ('right', 'right', 'pink'), ('sum_len', 'sum_len'), ('num_space', 'num_space'),
           ('other_space', 'other_space')],
    captions={
        'len_list = [': '先算好每个单词的长度 `len_list = {len_list}`',
        'left = 0': '`left`：当前行第一个单词',
        'res = []': '`res` 收集排好的每一行',
        'while left < len(words)': lambda S, B, ret: (f'从 `words[{B.left}]` 开始排新的一行' if B.left < len(B.words) else '全部排完'),
        'sum_len = len_list[left]': '先放第一个词：`sum_len = {sum_len}`',
        'right = left + 1': '`right` 尝试往这一行再加词',
        'while right < len(words) and': _cap_inner,
        'sum_len += len_list[right]': lambda S, B, ret: (
            (f'==第二个词起要多 1 个空格==：' if S.right == S.left + 1 else '') + f'`sum_len += {S.len_list[S.right]} + 1` → {S.sum_len}'),
        'if right == len(words)': lambda S, B, ret: ('`right == len(words)`：这一行装进了最后一个词 → ==最后一行，左对齐=='
                                                      if S.right == len(S.words) else '不是最后一行 → 要分配空格'),
        "tmp_res = ' '.join": '最后一行：词间只放 1 个空格 `"{tmp_res}"`',
        "tmp_res += ' ' * (maxWidth": '末尾补 `{len(tmp_res) - len(B.tmp_res)}` 个空格凑满 `{maxWidth}`',
        'break': '最后一行处理完，直接 `break`',
        'num_word = right - left': '这一行有 `num_word = {num_word}` 个词',
        'other_space = maxWidth - sum_len': '除了词间必须的空格，还多出 `other_space = {maxWidth} − {sum_len} = {other_space}` 个',
        'tmp_res = words[left]': '先写下第一个词 `"{tmp_res}"`',
        'if num_word == 1': lambda S, B, ret: ('只有一个词 → 空格全补在末尾' if S.num_word == 1 else f'`{S.num_word}` 个词 → 平均分配空格'),
        "tmp_res += ' ' * other_space": '单个词左对齐，末尾补 `{other_space}` 个空格',
        'num_space = 1 +': '`{num_word - 1}` 个空隙平分 `{B.other_space}` 个空格：每个空隙 `1 + {B.other_space} // {num_word - 1}` = =={num_space}== 个',
        'other_space %=': lambda S, B, ret: (f'余数 `{B.other_space} % {S.num_word - 1} = {S.other_space}`：==给左边 {S.other_space} 个空隙各多 1 个=='
                                              if S.other_space else f'`{B.other_space} % {S.num_word - 1} = 0`：正好分匀，没有余数'),
        'for index in range(1, num_word)': lambda S, B, ret: (f'处理第 `{S.index}` 个空隙，后面接 `"{S.words[S.left + S.index]}"`'
                                                              if S.get('index') != B.get('index') else '所有空隙都分配完了'),
        'if index <= other_space': _cap_if_index,
        'tmp_res += \' \' * num_space': lambda S, B, ret: (
            (f'多 1 个 + `{S.num_space}` 个空格，再接 `"{S.words[S.left + S.index]}"` → `"{S.tmp_res}"`'
             if S.index <= S.other_space else
             f'放 `{S.num_space}` 个空格，再接 `"{S.words[S.left + S.index]}"` → `"{S.tmp_res}"`')),
        'res.append(tmp_res)': '第 `{len(res)}` 行完成：`"{res[-1]}"`',
        'left = right': '下一行从 `words[{left}]` 开始',
        'return res': '返回全部 `{len(res)}` 行',
    },
    cards=dict(
        one_liner='每行贪心多装词；空格平均分，余数从左往右每个空隙多 1 个',
        complexity='时间 `O(L)`，`L` 为所有单词长度之和；空间 `O(n)`',
        problem=['把单词排成每行==恰好== `maxWidth` 个字符的文本，每行尽量多放单词',
                 '空格尽量均匀分配，分不匀时==左边的空隙多==；最后一行左对齐',
                 '示例：`["This","is","an","example",...]`，`maxWidth = 16`',
                 f'本视频：`{WORDS}`，`maxWidth = {MAXW}`'],
        quote='每一行都尽可能加入词，需要注意从当前行加入的第二个词开始就需要至少一个空格来区分。确定好一行里面词的个数之后，可以计算出有多少空格剩余，然后将这些空格平均分配。',
        quote_src='—— yiduobo 题解原文',
        idea=['第二个 while：把词尽量塞进当前行，第二个词起每个词多算 1 个空格',
              '`if`：装进了最后一个词 → 最后一行，词间 1 个空格，末尾补齐',
              '`else`：`num_space = 1 + other_space // 空隙数`，余数给左边的空隙各多 1 个',
              '只有一个词的行单独处理：空格全补在末尾'],
        summary=['时间 `O(L)`，每个词只被装进一次',
                 '`num_space` 已经包含词间必须的 1 个空格，所以要 `1 +`',
                 '余数 `other_space %= 空隙数`，`index <= other_space` 的空隙多 1 个 → 左多右少',
                 '原文为 Python 2 写法：`other_space / (num_word - 1)` 是整除，已改为 `//`；并删去了类型说明文档字符串',
                 '对比灵神：灵神用分组循环 + `divmod` + `join` 一次拼好；yiduobo 用 for 循环逐个空隙拼接'],
    ),
)
