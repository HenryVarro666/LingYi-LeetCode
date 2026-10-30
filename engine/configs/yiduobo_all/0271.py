def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '每个字符拆成两个 4 位：高 4 位 → 字母，低 4 位 → 字母；"00" = 一个字符串结束', 22, T['muted'], bold=True)
    strs = S.get('strs')
    if strs is not None:
        cv.text((x0 + 24, y0 + 56), 'strs = ' + repr(strs), 28, T['text'], mono=True)
    res = S.get('res')
    if res is None:
        return
    enc = None if strs is not None else S.get('s')
    y = y0 + 130
    if enc is None:
        # 编码阶段：res 是片段列表
        cv.text((x0 + 24, y), '密文片段 res（每个字符 2 个字母）', 24, T['cyan'], bold=True)
        txt = ''.join(res)
        cv.text((x0 + 24, y + 44), txt if txt else '（空）', 32, T['green'], mono=True)
        ch = S.get('char')
        if ch is not None and 'v' in S:
            v = S['v']
            cv.text((x0 + 24, y + 120), f"字符 {ch!r}：ord = {v}  →  {v} // 16 = {v // 16}, {v} % 16 = {v % 16}", 26, T['yellow'], mono=True)
            cv.text((x0 + 24, y + 170), f"chr({v // 16} + 97) = {chr(v // 16 + 97)!r}，chr({v % 16} + 97) = {chr(v % 16 + 97)!r}", 26, T['blue'], mono=True)
    else:
        cv.text((x0 + 24, y), '密文 s（两个字母一组，"00" 是分隔）', 24, T['cyan'], bold=True)
        i = S.get('i', -1)
        n = len(enc)
        cell = min(44, (x1 - x0 - 48) / max(1, n))
        for k, c in enumerate(enc):
            X = x0 + 24 + k * cell
            at = k in (i, i + 1) if i >= 0 else False
            fill = T['blue'] if k == i else (T['pink'] if (at and k == i + 1) else T['panel2'])
            cv.rect((X, y + 40, X + cell - 3, y + 40 + 46), fill=fill, r=5, outline=T['border'], width=1)
            cv.text((X + (cell - 3) / 2, y + 63), c, 24, T['bg'] if at else T['text'], anchor='mm', mono=True, bold=True)
        tmp = S.get('tmp') or []
        cv.text((x0 + 24, y + 120), f'tmp（当前字符串的字符）= {"".join(tmp)!r}', 26, T['yellow'], mono=True)
        cv.text((x0 + 24, y + 170), f'res（已还原的字符串）= {res!r}', 26, T['green'], mono=True)


CONFIG = dict(
    num=271, title='字符串的编码与解码', difficulty='Medium', category='设计',
    author='yiduobo', technique='字符拆成两个 4 位 · "00" 作分隔',
    code='''
class Codec:

    def encode(self, strs):
        res = []
        for s in strs:
            for char in s:
                v = ord(char)
                res.append(chr(v // 16 + 97))
                res.append(chr(v % 16 + 97))
            res.append('00')
        
        return ''.join(res)

    def decode(self, s):
        res = []
        tmp = []
        for i in range(0, len(s), 2):
            if s[i] != '0':
                tmp.append(chr((ord(s[i]) - 97) * 16 + ord(s[i + 1]) - 97))
            else:
                res.append(''.join(tmp))
                tmp = []
        
        return res
''',
    call='''c = Codec()
e = c.encode(['Hi', '', 'a'])
c.decode(e)''',
    expect=['Hi', '', 'a'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=['v', 'i'],
    max_steps=90,
    captions={
        'res = []': lambda S, B, ret: '准备收集结果（编码：密文片段；解码：还原出的字符串）',
        'for s in strs': '逐个取字符串（`strs` 取完就结束循环）',
        'for char in s': '逐个取字符（取完这个字符串就结束内层循环）',
        'v = ord(char)': '`ord({char!r}) = {v}`，8 位二进制，拆成两个 4 位',
        'chr(v // 16 + 97)': '高 4 位：`{v} // 16 = {v // 16}` → 字母 `{res[-1]!r}`（取值只有 16 种，从 `a` 开始）',
        'chr(v % 16 + 97)': '低 4 位：`{v} % 16 = {v % 16}` → 字母 `{res[-1]!r}`',
        "res.append('00')": '字符串结束，加 `"00"` 做分隔：字母都 ≥ `a`，不会和 `0` 混淆（空串就是只有 `00`）',
        "return ''.join(res)": '拼成一个密文 `{ret!r}`',
        'tmp = []\n': '准备收集当前字符串的字符',
        'for i in range': '步长 2：每次看一对字母（`s` 看完就结束循环）',
        "if s[i] != '0'": lambda S, B, ret: (f"`s[{S.i}] = {S.s[S.i]!r}` ≠ `'0'` → 这是一个字符的两个字母" if S.s[S.i] != '0'
                                             else f"`s[{S.i}] = '0'` → 遇到 `00`，当前字符串结束"),
        'tmp.append(chr': '还原字符：`({ord(s[i]) - 97}) × 16 + {ord(s[i + 1]) - 97}` = {ord(tmp[-1])} → `{tmp[-1]!r}`',
        "res.append(''.join(tmp))": '把 `tmp` 拼成字符串 `{res[-1]!r}` 放进结果（空串也能还原）',
        'tmp = []': '`tmp` 清空，开始下一个字符串',
        'return res': '解码结果 `{ret}`，和原来的 `strs` 一致',
    },
    cards=dict(
        one_liner='把字符拆成两个 4 位，只占 16 个字母，剩下的字符当分隔',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['设计 `encode`：把字符串列表编码成一个字符串',
                 '设计 `decode`：从这个字符串还原出原列表',
                 '字符是 ASCII（0~255），长度也不限，==不能随便挑个分隔符=='],
        quote='如果将其拆分为两个4位的二进制，实际需要占用的ascii码的数量就从256变成了16，……此时就可以使用其他字符来做特殊标识，表示当前字符串已经结束。',
        quote_src='—— yiduobo 题解原文',
        idea=['分隔符会出现在内容里，长度前缀又没有上限，这两条路都有问题',
              '每个字符 8 位 = 两个 4 位，各用 `chr(x + 97)` 表示，只出现 `a`~`p`',
              '于是字符 `0` 不会出现在密文的字符里，`"00"` 就能无歧义地表示==字符串结束=='],
        summary=['编码、解码都是线性扫描：时间、空间 `O(L)`',
                 '易错：解码时每次步长为 2；遇到 `00` 要把 `tmp` 存入结果，空串也要存',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去了 `:type` 文档字符串中的类型说明',
                 '代价：密文长度是原来的 2 倍多；常用做法是 `长度 + 分隔符 + 内容`'],
    ),
)
