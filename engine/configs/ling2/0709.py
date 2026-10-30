S_IN = 'Hi@LC'


def _bits(cv, x, y, cell, val, T, label, hl_col=5, color=None):
    b = format(val, '07b')
    cv.text((x - 14, y + cell / 2), label, 24, T['muted'], anchor='rm', bold=True, mono=True)
    for k, ch in enumerate(b):
        bitpos = 6 - k                       # 从低到高第 bitpos 位（0 起）
        X = x + k * cell
        hl = bitpos == hl_col
        fill = (color if (hl and color) else (T['panel2']))
        cv.rect((X + 3, y + 3, X + cell - 3, y + cell - 3), fill=fill, r=6,
                outline=T['yellow'] if hl else T['border'], width=3 if hl else 1)
        cv.text((X + cell / 2, y + cell / 2), ch, 26, T['bg'] if (hl and color) else T['text'], anchor='mm', bold=True, mono=True)


def _draw_bits(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'ASCII 二进制（黄框 = 从低到高第六位，值 32）', 22, T['muted'], bold=True)
    ch = S.get('ch')
    if ch is None:
        cv.text((x0 + 18, y0 + 50), 'A = 65 = 1000001，a = 97 = 1100001：只差第六位', 24, T['dim'])
        return
    cell = 70
    x = x0 + 300
    y = y0 + 70
    o = ord(ch)
    upper = 'A' <= ch <= 'Z'
    _bits(cv, x, y, cell, o, T, f"'{ch}' = {o}", color=T['orange'] if upper else None)
    for k in range(7):  # 位号：从低到高第 1~7 位
        cv.text((x + k * cell + cell / 2, y - 2), f'第{7 - k}位', 16, T['yellow'] if k == 1 else T['dim'], anchor='mb')
    if upper and S.get('_line') == 6:
        _bits(cv, x, y + cell + 12, cell, 32, T, '| 32', color=T['blue'])
        r = o | 32
        cv.line([(x, y + 2 * cell + 20), (x + 7 * cell, y + 2 * cell + 20)], T['border'], 2)
        _bits(cv, x, y + 2 * cell + 28, cell, r, T, f"'{chr(r)}' = {r}", color=T['green'])
        cv.text((x0 + 40, y + 3 * cell + 56), f'其余位不变：低五位 {o & 31:05b} = {o & 31} → 仍是第 {o & 31} 个字母', 24, T['muted'], bold=True)
    elif upper:
        cv.text((x0 + 40, y + cell + 36), f'低五位 {o & 31:05b} = {o & 31}：它是第 {o & 31} 个字母；第六位是 0 → 大写', 24, T['muted'], bold=True)
    else:
        cv.text((x0 + 40, y + cell + 36), '不是大写字母 → 不改（@ = 1000000，若 OR 32 会变成反引号 ` ）'
                if ch == '@' else f'不是大写字母 → 原样保留', 24, T['muted'], bold=True)


def _if_cap(S, B, ret):
    ch = S.ch
    if 'A' <= ch <= 'Z':
        return f'`\'{ch}\'` 在 `A`~`Z` 之间 → 大写字母'
    if ch == '@':
        return f'`\'@\'`（64）紧挨着 `A`（65），但==不是字母== → 不能动它'
    return f'`\'{ch}\'` 不是大写字母 → 跳过'


CONFIG = dict(
    num=709, title='转换成小写字母', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='位运算 · OR 32',
    tags=['List.md'],
    code='''
class Solution:
    def toLowerCase(self, s: str) -> str:
        t = list(s)
        for i, ch in enumerate(t):
            if 'A' <= ch <= 'Z':
                t[i] = chr(ord(ch) | 32)
        return ''.join(t)
''',
    call=f'Solution().toLowerCase({S_IN!r})',
    expect='hi@lc',
    views=[
        dict(type='string', var='t', label='t = list(s)（绿 = 已转成小写）', pointers={'i': 'blue'}, cell=84,
             color=lambda S, i, v: ('green' if (S['s'][i] != v) else None) if 't' in S else None),
        dict(type='custom', draw=_draw_bits, h=420),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch'), ('ord(ch)', lambda S: ord(S['ch']) if 'ch' in S else None, 'orange')],
    captions={
        't = list(s)': 'Python 字符串不可变 → 先转成列表 `t`，原地修改',
        'for i, ch in': lambda S, B, ret: (f'第 `i = {S.i}` 个字符 `\'{S.ch}\'`' if B.get('i') != S.get('i') or 'i' not in B
                                           else '所有字符都看完了'),
        "if 'A' <= ch <= 'Z'": _if_cap,
        't[i] = chr(': lambda S, B, ret: (f'`{ord(S.ch)} | 32 = {ord(S.ch) | 32}`：==把第六位改成 1== → `\'{S.t[S.i]}\'`'),
        "return ''.join(t)": '拼回字符串：`"{ret}"`',
    },
    cards=dict(
        one_liner='大小写字母只差二进制第六位：OR 32 就把它改成 1',
        complexity='时间 `O(n)`，空间 `O(n)` 或 `O(1)`',
        problem=['把字符串 `s` 中的==大写字母==转成对应的小写字母，返回新字符串',
                 '`s` 由 ASCII 可打印字符组成（不只有字母）',
                 '示例：`"Hello"` → `"hello"`，`"LOVELY"` → `"lovely"`',
                 '本视频：`"Hi@LC"` → `"hi@lc"`'],
        quote='大写字母的二进制 ASCII 值，从低到高第六位是 0；小写字母的二进制 ASCII 值，从低到高第六位是 1。……把大写字母的 ASCII 值和 32 计算按位或（OR）。',
        quote_src='—— 灵茶山艾府题解（方法三：位运算）',
        idea=['`A` = 65 = `1000001`，`a` = 97 = `1100001`：==只差第六位==',
              '`32` = `100000`：`ord(ch) | 32` 把第六位置 1，其余位不变',
              '低五位正好表示是第几个字母，所以 OR 之后还是同一个字母'],
        summary=['时间 `O(n)`；空间 `O(n)`（Python 字符串不可变，要转列表）',
                 '易错：必须先判断 `\'A\' <= ch <= \'Z\'`，`@`、`[` 等字符 OR 32 会变成别的符号',
                 '方法一：`s.lower()`；方法二：`chr(ord(\'a\') + ord(ch) - ord(\'A\'))`',
                 '相关技巧：`^ 32` 大小写互换，`& ~32` 转大写'],
    ),
)
