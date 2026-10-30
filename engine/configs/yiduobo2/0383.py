CASES = [("aab", "acab"), ("aa", "ab")]


def _idx(S):
    line = S.get('_line')
    rd, md = S.get('ransom_dict'), S.get('magazine_dict')
    if rd is None or md is None or 'char' not in S:
        return None, None
    r, m = S['ransomNote'], S['magazine']
    tr, tm = sum(rd.values()), sum(md.values())
    if line == 6 and tr < len(r):
        return 'r', tr
    if line == 7:
        return 'r', tr - 1
    if line == 8 and tm < len(m):
        return 'm', tm
    if line == 9:
        return 'm', tm - 1
    return None, None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'magazine' not in S:
        return
    which, k = _idx(S)
    line = S.get('_line')
    cell = 80
    for row, (name, s, key, c0) in enumerate((('ransomNote', S['ransomNote'], 'r', T['pink']),
                                               ('magazine', S['magazine'], 'm', T['green']))):
        Y = y0 + 40 + row * 130
        cv.text((x0 + 18, Y - 36), f'{name} = "{s}"', 24, T['muted'], bold=True)
        for i, ch in enumerate(s):
            X = x0 + 40 + i * cell
            hit = which == key and i == k
            cv.rect((X + 3, Y, X + cell - 3, Y + cell - 6), fill=c0 if hit else T['panel2'], r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + (cell - 6) / 2), ch, 32, T['bg'] if hit else T['text'], anchor='mm', bold=True)
    # 对比表
    rd, md = S.get('ransom_dict'), S.get('magazine_dict')
    Y0 = y0 + 300
    cv.text((x0 + 18, Y0 - 34), '逐个字符比较：magazine 里的个数够不够 ransomNote 用', 24, T['muted'], bold=True)
    if rd is None:
        return
    keys = sorted(set(rd) | set(md or {}))
    cols = [x0 + 40, x0 + 200, x0 + 450, x0 + 720]
    for X, h in zip(cols, ['字符', 'ransom_dict', 'magazine_dict', '结论']):
        cv.text((X, Y0), h, 22, T['muted'], bold=True)
    cur = S.get('char') if line in (11, 12, 13) else None
    checking = line in (12, 13)
    for i, ch in enumerate(keys):
        Y = Y0 + 36 + i * 50
        on = checking and ch == cur
        if on:
            cv.rect((x0 + 24, Y - 6, x1 - 24, Y + 40), fill=T['yellow'], alpha=40, r=8)
        a, b = rd.get(ch), (md or {}).get(ch)
        cv.text((cols[0], Y), f"'{ch}'", 26, T['text'], mono=True)
        cv.text((cols[1] + 40, Y), '-' if a is None else a, 26, T['pink'], mono=True, bold=True)
        cv.text((cols[2] + 50, Y), '-' if b is None else b, 26, T['green'], mono=True, bold=True)
        if on:
            ok = (b or 0) >= a
            cv.text((cols[3], Y), f'{b or 0} ≥ {a} 够用' if ok else f'{b or 0} < {a} 不够', 24,
                    T['green'] if ok else T['red'], bold=True)
        elif a is None:
            cv.text((cols[3], Y), '用不到', 22, T['dim'])


def _cap_for(name, key):
    def f(S, B, ret):
        which, k = _idx(S)
        if which == key:
            return f'遍历 {name}：`char = \'{S.char}\'`'
        return f'{name} 统计完毕'
    return f


def _cap_if(S, B, ret):
    ch = S.char
    a, b = S.ransom_dict[ch], S.magazine_dict.get(ch, 0)
    if b < a:
        return f'`\'{ch}\'`：magazine 只有 `{b}` 个，ransomNote 要 `{a}` 个 → ==不够=='
    return f'`\'{ch}\'`：magazine 有 `{b}` 个 ≥ 需要的 `{a}` 个 → 够用'


CONFIG = dict(
    num=383, title='赎金信', difficulty='Easy', category='哈希',
    author='yiduobo', technique='两个字典分别计数，再逐个比较',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        ransom_dict = {}
        magazine_dict = {}

        for char in ransomNote:
            ransom_dict[char] = ransom_dict.get(char, 0) + 1
        for char in magazine:
            magazine_dict[char] = magazine_dict.get(char, 0) + 1

        for char in ransom_dict:
            if magazine_dict.get(char, 0) < ransom_dict[char]:
                return False

        return True
''',
    call=f'[Solution().canConstruct(r, m) for r, m in {CASES}]',
    expect=[True, False],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('char', 'char'), ('ransom_dict', 'ransom_dict', 'pink'), ('magazine_dict', 'magazine_dict', 'green')],
    captions={
        'ransom_dict = {}': lambda S, B, r: f'新的一组：`("{S.ransomNote}", "{S.magazine}")`。`ransom_dict` 统计 ransomNote 每个字符的次数',
        'magazine_dict = {}': '`magazine_dict` 统计 magazine 每个字符的次数',
        'for char in ransomNote': _cap_for('ransomNote', 'r'),
        'ransom_dict[char] =': lambda S, B, r: (f"`ransom_dict['{S.char}'] = {S.ransom_dict[S.char]}`"
                                                + ('（第一次出现，`get(char, 0)` 取到 0）' if S.ransom_dict[S.char] == 1 else '')),
        'for char in magazine': _cap_for('magazine', 'm'),
        'magazine_dict[char] =': '`magazine_dict[\'{char}\'] = {magazine_dict[char]}`',
        'for char in ransom_dict': lambda S, B, r: (f'逐个比较 ransomNote 里出现过的字符：`\'{S.char}\'`'
                                                    if B.get('char') != S.get('char')
                                                    else '比较完毕'),
        'if magazine_dict.get': _cap_if,
        'return False': '有字符不够用 → 返回 ==False==',
        'return True': '每个字符都够用 → 返回 ==True==',
    },
    cards=dict(
        one_liner='分别数出两个字符串里每个字符的个数，再逐个比较够不够',
        complexity='时间 `O(n + m)`，空间 `O(|Σ|)`',
        problem=['判断 `ransomNote` 能不能由 `magazine` 里的字符构成',
                 '`magazine` 中的==每个字符只能用一次==',
                 '示例：`("a","b")` → `false`；`("aa","ab")` → `false`；`("aa","aab")` → `true`',
                 '本视频依次跑 `("aab","acab")` 和 `("aa","ab")`'],
        quote='比较基础的题目。==分别统计==ransom和magazine中每个字符出现的次数，然后==逐个比较==即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个字典：`ransom_dict`、`magazine_dict`，用 `dict.get(char, 0) + 1` 计数',
              '只查 ransomNote 里出现过的字符：magazine 中个数更少就返回 `False`',
              '全部检查通过才返回 `True`'],
        result='两组答案：`True`、`False`',
        summary=['时间 `O(n + m)`，空间 `O(|Σ|)`（字符集最多 26 个字母）',
                 '易错：magazine 里没有的字符要用 `get(char, 0)`，不能直接 `magazine_dict[char]`',
                 '对比灵神：一个 cnt 记次数之差（+1 / −1），或直接 `Counter(r) <= Counter(m)`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
