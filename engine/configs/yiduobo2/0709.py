S_IN = 'LeetCode'
LO, HI = 60, 127


def _draw_ascii(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'ASCII 码数轴：大写 65~90，小写 97~122，相差 32', 22, T['muted'], bold=True)
    L, R = x0 + 50, x1 - 50
    axis_y = y0 + 210

    def X(v):
        return L + (v - LO) * (R - L) / (HI - LO)

    # 两段区间
    for a, b, c, name in ((65, 90, T['blue'], '大写 A~Z'), (97, 122, T['green'], '小写 a~z')):
        cv.rect((X(a), axis_y - 34, X(b), axis_y - 6), fill=c, alpha=90, r=6)
        cv.text(((X(a) + X(b)) / 2, axis_y - 40), name, 22, c, anchor='mb', bold=True)
        for v in (a, b):
            cv.text((X(v), axis_y + 10), v, 18, T['muted'], anchor='mt', mono=True)
    cv.line([(L, axis_y), (R, axis_y)], T['border'], 2)
    if 'index' not in S:
        return
    ch = S['str_list'][S['index']]
    if S.get('_line') == 6:
        ch = B['str_list'][B['index']]
    o = ord(ch)
    up = 65 <= o <= 90
    col = T['orange'] if up else T['muted']
    if LO <= o <= HI:
        cv.tri_up(X(o), axis_y + 40, 10, col)
        cv.text((X(o), axis_y + 60), f"'{ch}' = {o}", 22, col, anchor='mt', bold=True)
    if S.get('_line') == 6:
        n = o + 32
        cv.arrow((X(o), axis_y + 110), (X(n), axis_y + 110), T['yellow'], 4)
        cv.text(((X(o) + X(n)) / 2, axis_y + 120), '+32', 26, T['yellow'], anchor='mt', bold=True)
        cv.tri_up(X(n), axis_y + 40, 10, T['green'])
        cv.text((X(n), axis_y + 60), f"'{chr(n)}' = {n}", 22, T['green'], anchor='mt', bold=True)


def _if_cap(S, B, ret):
    c = S.str_list[S.index]
    o = ord(c)
    if 'A' <= c <= 'Z':
        return f'`\'{c}\'` 的 ASCII 码 `{o}` 在 ==65~90== 之间 → 大写字母'
    return f'`\'{c}\'` 的 ASCII 码 `{o}` 不在 65~90 → 不是大写，跳过'


CONFIG = dict(
    num=709, title='转换成小写字母', difficulty='Easy', category='字符串',
    author='yiduobo', technique='ASCII 码 +32',
    tags=['List.md'],
    code='''
class Solution(object):
    def toLowerCase(self, str):
        str_list = list(str)
        for index in range(len(str_list)):
            if str_list[index] >= 'A' and str_list[index] <= 'Z':
                str_list[index] = chr(ord(str_list[index]) + 32)

        return ''.join(str_list)
''',
    call=f'Solution().toLowerCase({S_IN!r})',
    expect='leetcode',
    views=[
        dict(type='string', var='str_list', label='str_list = list(str)（绿 = 已转成小写）', pointers={'index': 'blue'}, cell=96, h=210,
             color=lambda S, i, v: ('green' if S['str'][i] != v else None) if 'str_list' in S else None),
        dict(type='custom', draw=_draw_ascii, h=380),
    ],
    watch=[('index', 'index', 'blue'), ('str_list[index]', lambda S: S['str_list'][S['index']] if 'index' in S else None),
           ('ord', lambda S: ord(S['str_list'][S['index']]) if 'index' in S else None, 'orange')],
    captions={
        'str_list = list(str)': '字符串不能原地改 → 先转成字符列表 `str_list`',
        'for index in range': lambda S, B, ret: (f'看第 `index = {S.index}` 个字符 `\'{S.str_list[S.index]}\'`'
                                                 if B.get('index') != S.get('index') or 'index' not in B else '所有字符都看完了'),
        "if str_list[index] >= 'A'": _if_cap,
        'str_list[index] = chr(': lambda S, B, ret: (f'`{ord(B.str_list[B.index])} + 32 = {ord(S.str_list[S.index])}`，'
                                                     f'再转回字母：`\'{B.str_list[B.index]}\'` → ==小写 {S.str_list[S.index]}=='),
        "return ''.join": '拼回字符串：`"{ret}"`',
    },
    cards=dict(
        one_liner='大写字母 ASCII 码在 65~90，加上 32 就是对应的小写字母',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把字符串中的==大写字母==转成对应的小写字母，返回新字符串',
                 '示例：`"Hello"` → `"hello"`，`"here"` → `"here"`',
                 '本视频：`"LeetCode"` → `"leetcode"`'],
        quote='大写字母ascii码在65到90之间，而小写字母则是97到122之间。……将其转换成ascii码之后加上32，再转换回字母就得到对应的小写字母了。',
        quote_src='—— yiduobo 知乎题解',
        idea=['高级语言都有现成函数，这里手动做 ASCII 码转换',
              '判断大写：`\'A\' <= c <= \'Z\'`（ASCII 码 65~90）',
              '`chr(ord(c) + 32)`：大写与小写的 ASCII 码==恰好相差 32=='],
        summary=['时间 `O(n)`；空间 `O(n)`（Python 字符串不可变，转成列表再 join）',
                 '易错：只对 `A~Z` 加 32，其他字符（数字、符号、小写）原样保留',
                 '`+ 32` 对大写字母等价于灵神的 `| 32`（第六位原本是 0）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（参数名 `str` 原样保留）'],
    ),
)
