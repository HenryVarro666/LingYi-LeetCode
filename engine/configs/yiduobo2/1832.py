SENT = 'thequickbrownfoxjumpsoverthelazydog'
ABC = 'abcdefghijklmnopqrstuvwxyz'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cur = S.get('char')
    cs = S.get('char_set') or set()
    new = cur is not None and cur not in (B.get('char_set') or set()) and cur in cs
    # ---- sentence (2 rows)
    cv.text((x0 + 18, y0 + 4), 'sentence（黄 = 当前字母 char 出现的位置）', 22, T['muted'], bold=True)
    per = 18
    cell = min(52, (x1 - x0 - 60) / per)
    sx = x0 + 30
    for k, ch in enumerate(SENT):
        r, c = divmod(k, per)
        X, Y = sx + c * cell, y0 + 48 + r * (cell + 12)
        hit = ch == cur
        fill = T['yellow'] if hit else T['panel2']
        cv.rect((X + 2, Y, X + cell - 2, Y + cell), fill=fill, r=6, outline=T['border'], width=1)
        cv.text((X + cell / 2, Y + cell / 2), ch, 26, T['bg'] if hit else T['text'], anchor='mm', bold=True, mono=True)
    # ---- alphabet board
    ay = y0 + 48 + 2 * (cell + 12) + 50
    cv.text((x0 + 18, ay - 34), f'char_set（绿 = 已出现，黄 = 新加入，橙 = 重复；len = {len(cs)} / 26）', 22, T['muted'], bold=True)
    acell = min(72, (x1 - x0 - 60) / 13)
    for k, ch in enumerate(ABC):
        r, c = divmod(k, 13)
        X, Y = sx + c * acell, ay + r * (acell + 14)
        on = ch in cs
        if ch == cur:
            fill = T['yellow'] if new else T['orange']
        else:
            fill = T['green'] if on else T['panel2']
        cv.rect((X + 3, Y, X + acell - 3, Y + acell), fill=fill, r=8, outline=T['border'], width=1)
        cv.text((X + acell / 2, Y + acell / 2), ch, 30, T['bg'] if (on or ch == cur) else T['dim'],
                anchor='mm', bold=True, mono=True)
    # progress bar
    py = ay + 2 * (acell + 14) + 22
    w = 13 * acell - 6
    cv.rect((sx + 3, py, sx + 3 + w, py + 22), fill=T['panel2'], r=11)
    if cs:
        cv.rect((sx + 3, py, sx + 3 + w * len(cs) / 26, py + 22), fill=T['green'], r=11)
    cv.text((sx + 3 + w / 2, py + 34), f'{len(cs)} / 26', 24, T['green'] if len(cs) == 26 else T['text'],
            anchor='mt', bold=True, mono=True)


def _add(S, B, ret):
    c = S.char
    before, after = len(B.char_set), len(S.char_set)
    if after > before:
        tail = '，==26 个字母凑齐了==' if after == 26 else ''
        return f'`{c}` 第一次出现 → 加入集合，大小 `{before} → {after}`{tail}'
    return f'`{c}` 已经在集合里 → set ==自动去重==，大小仍是 `{after}`'


CONFIG = dict(
    num=1832, title='判断句子是否为全字母句', difficulty='Easy', category='哈希',
    author='yiduobo', technique='set 去重 · 数一数有几种字母',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def checkIfPangram(self, sentence):
        char_set = set()
        for char in sentence:
            char_set.add(char)

        return len(char_set) == 26
''',
    call=f'Solution().checkIfPangram({SENT!r})',
    expect=True,
    skip=['for char in'],
    max_steps=40,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('char', 'char', 'yellow'), ('len(char_set)', 'len(char_set)', 'green')],
    captions={
        'char_set = set()': '用 `set` 记录出现过的字母：同一个字母只会存一份',
        'char_set.add(char)': _add,
        'return len(char_set)': lambda S, B, ret: (f'`len(char_set) = {len(S.char_set)}`'
                                                   + (' == 26 → 每种字母都出现了 → ==True==' if ret
                                                      else ' ≠ 26 → 缺了字母 → ==False==')),
    },
    cards=dict(
        one_liner='一趟扫描丢进 set，大小等于 26 就是全字母句',
        complexity='时间 `O(n)`，空间 `O(Σ)`，`Σ = 26`',
        problem=['句子 `sentence` 只含小写字母',
                 '判断它是否包含 a~z ==每个字母至少一次==',
                 '示例：`"thequickbrownfoxjumpsoverthelazydog"` → `true`',
                 '示例：`"leetcode"` → `false`'],
        quote='可以一趟扫描，使用set来进行去重。最终set的大小如果为26，那么就说明句子中包含了每一种字母，否则就缺失了部分的字母。',
        quote_src='—— yiduobo 题解原文',
        idea=['只含小写字母 → 字母一共只有 ==26 种==',
              '重复的字母对答案没影响 → 交给 `set` 去重',
              '最后只看集合大小：`26` 说明一个不缺'],
        result='35 个字符里有 26 种不同字母 → 返回 `True`',
        summary=['时间 `O(n)`，空间 `O(26)`',
                 '依赖“只含小写字母”：有大写/标点时要先过滤',
                 '可提前结束：集合满 26 就能直接返回 True',
                 '位运算写法：用 26 位掩码 `mask |= 1 << idx`，判 `mask == (1<<26)-1`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
