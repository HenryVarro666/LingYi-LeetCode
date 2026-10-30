def _order(s, n):
    """yiduobo 的输出顺序：每个字符在 res 里依次对应原串哪个下标"""
    if n == 1:
        return list(range(len(s)))
    mod = 2 * n - 2
    k = (len(s) - 1) // mod + 1
    out = [i * mod for i in range(k)]
    for row in range(1, n - 1):
        for i in range(k):
            for p in (i * mod + row, i * mod + mod - row):
                if p < len(s):
                    out.append(p)
    out += [i * mod + n - 1 for i in range(k) if i * mod + n - 1 < len(s)]
    return out


def _cell(p, n):
    """原串下标 p 在“竖钩”排列里的 (行, 列)"""
    mod = 2 * n - 2
    part, r = divmod(p, mod)
    if r < n:
        return r, part * (n - 1)
    return mod - r, part * (n - 1) + (r - n + 1)


def _used(S):
    res = S.get('res')
    if not isinstance(res, str):
        return set()
    return set(_order(S['s'], S['numRows'])[:len(res)])


def _just(S, B):
    if not isinstance(S.get('res'), str) or not isinstance(B.get('res'), str) or len(S['res']) == len(B['res']):
        return None
    return _order(S['s'], S['numRows'])[len(S['res']) - 1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s, n = S['s'], S['numRows']
    mod = 2 * n - 2
    cv.text((x0 + 18, y0 + 4), '按“竖钩”排列（同色 = 同一个竖钩；绿 = 已加入 res，黄 = 这一步加入）', 22, T['muted'], bold=True)
    cells = [_cell(p, n) for p in range(len(s))]
    C = max(c for _, c in cells) + 1
    size = min(66, (x1 - x0 - 120) / C, (y1 - y0 - 70) / n)
    sx = x0 + 80 + ((x1 - x0 - 120) - size * C) / 2
    sy = y0 + 50
    used, just = _used(S), _just(S, B)
    ln = S.get('_line', 0)
    cur_row = None
    if ln == 13:
        cur_row = 0
    elif 15 <= ln <= 22 and 'row' in S:
        cur_row = S['row']
    elif 24 <= ln <= 27:
        cur_row = n - 1
    for r in range(n):
        Y = sy + r * size + size / 2
        cv.text((sx - 16, Y), f'行{r}', 20, T['yellow'] if r == cur_row else T['dim'], anchor='rm', bold=r == cur_row)
    if cur_row is not None:
        cv.rect((sx - 6, sy + cur_row * size + 2, sx + C * size + 6, sy + (cur_row + 1) * size - 2), fill=T['yellow'], alpha=28, r=8)
    hues = ['blue', 'pink', 'purple', 'cyan', 'orange']
    for p, (r, c) in enumerate(cells):
        X, Y = sx + c * size, sy + r * size
        part = p // mod
        if p == just:
            fill, tc = T['yellow'], T['bg']
        elif p in used:
            fill, tc = T['green'], T['bg']
        else:
            fill, tc = T['panel2'], T[hues[part % len(hues)]]
        cv.rect((X + 4, Y + 4, X + size - 4, Y + size - 4), fill=fill, r=8,
                outline=T[hues[part % len(hues)]], width=2)
        cv.text((X + size / 2, Y + size / 2 - 4), s[p], int(size * 0.42), tc, anchor='mm', bold=True, mono=True)
        cv.text((X + size - 8, Y + size - 6), p, 13, tc if fill != T['panel2'] else T['dim'], anchor='rb', mono=True)


CONFIG = dict(
    num=6, title='Z字形变换', difficulty='Medium', category='字符串',
    author='yiduobo', technique='找规律 · 按“竖钩”分组直接算下标',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def convert(self, s, numRows):
        if numRows == 1:
            return s

        res = ''
        mod = numRows * 2 - 2
        length = len(s)

        k = (length - 1) // mod + 1

        for index in range(k):
            res = res + s[index * mod]

        for row in range(1, numRows - 1):
            for index in range(k):
                pos = index * mod + row
                if pos < length:
                    res += s[pos]
                pos = index * mod + mod - row
                if pos < length:
                    res += s[pos]

        for index in range(k):
            pos = index * mod + numRows - 1
            if pos < length:
                res += s[pos]

        return res
''',
    call='Solution().convert("PAYPALISHIRING", 4)',
    expect='PINALSIGYAHRPI',
    skip=['for index in range(k)'],
    views=[
        dict(type='text', size=26, fn=lambda S: (f"周期 `mod = {S['mod']}`：竖线 `{S['numRows']}` 个 + 钩子 `{S['numRows'] - 2}` 个"
                                                 + (f"，共 `k = {S['k']}` 个竖钩" if 'k' in S else '')) if 'mod' in S
             else '每个竖钩 = 一条竖线 + 一个钩子'),
        dict(type='string', var='s', label='s（原串，绿 = 已经取走）', cell=62, h=170,
             pointers={'pos': 'yellow'},
             color=lambda S, i, v: 'green' if i in _used(S) else None),
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', size=28, fn=lambda S: f"res = `\"{S['res']}\"`" if isinstance(S.get('res'), str) and S['res'] else 'res = `""`'),
    ],
    watch=[('row', lambda S: S['row'] if S['_line'] < 24 else None, 'cyan'), ('index', 'index', 'purple'), ('pos', 'pos', 'yellow'), ('len(res)', lambda S: len(S['res']), 'green')],
    captions={
        'if numRows == 1': '`numRows = {numRows}`：只有 1 行时没有钩子，`mod` 会是 0 → 要特判直接返回',
        "res = ''": '`res` 从空串开始，==一行一行==往里拼',
        'mod = numRows * 2 - 2': '竖线 `{numRows}` 个 + 钩子 `{numRows}-2` 个 → 每个竖钩 `mod = {mod}` 个字符',
        'length = len(s)': '`length = {length}`',
        'k = (length - 1) // mod + 1': '一共 `k = ({length}-1)//{mod}+1 = {k}` 个竖钩（最后一个可能不完整）',
        'res = res + s[index * mod]': '第 0 行只有竖线顶端：`s[{index}×{mod}] = {s[index * mod]!r}`',
        'for row in range(1, numRows - 1)': lambda S, B, r: (f'中间第 `{S.row}` 行：每个竖钩贡献==两个==字符（竖线 + 钩子）'
                                                             if S.get('row') != B.get('row') else '中间行处理完毕'),
        'pos = index * mod + row': '竖线上的字符：`pos = {index}×{mod}+{row} = {pos}`',
        'pos = index * mod + mod - row': '钩子是==从下往上==生成的：`pos = {index}×{mod}+{mod}−{row} = {pos}`',
        'if pos < length': lambda S, B, r: (f'`{S.pos} < {S.length}` → 这个位置有字符' if S.pos < S.length
                                            else f'`pos = {S.pos} ≥ {S.length}`：最后一个竖钩不完整 → ==跳过=='),
        'res += s[pos]': '加入 `s[{pos}] = {s[pos]!r}`',
        'pos = index * mod + numRows - 1': '最后一行只有竖线底端：`pos = {index}×{mod}+{numRows - 1} = {pos}`',
        'return res': '逐行拼完，返回 =={res}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='别看 Z 字，看“竖钩”：每个竖钩 2·numRows−2 个字符',
        complexity='时间 `O(n)`，空间 `O(1)`（不算答案）',
        problem=['把 `s` 按 Z 字形排成 `numRows` 行，再==逐行==从左到右读出来',
                 '示例：`s = "PAYPALISHIRING"`，`numRows = 4`',
                 '→ `"PINALSIGYAHRPI"`'],
        quote='题目说的虽然是Z字形变换，但是实际上==按照竖钩的形式进行划分==会更加清晰。……每个部分一共有numRows * 2 - 2个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['令 `mod = 2·numRows − 2`，第 `index` 个竖钩从 `index·mod` 开始',
              '第 `row` 行：竖线上是 `index·mod + row`，钩子上是 `index·mod + mod − row`',
              '第 0 行和最后一行没有钩子，单独处理；越界的位置跳过'],
        summary=['时间 `O(n)`：每个字符恰好被算到一次；不需要真的开二维数组',
                 '易错：==numRows = 1 要特判==，否则 `mod = 0` 会除零',
                 '钩子字符从下往上生成，所以是 `mod − row` 而不是 `+ row`',
                 '原文为 Python 2 写法：`/` 整除已改为 `//`，并删去了类型说明文档字符串'],
    ),
)
