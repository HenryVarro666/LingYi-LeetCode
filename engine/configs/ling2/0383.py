CASES = [("aa", "aab"), ("aa", "ab")]


def _idx(S):
    """(which string, index) currently being scanned"""
    line = S.get('_line')
    cnt = S.get('cnt')
    if cnt is None or 'c' not in S:
        return None, None
    tot = sum(cnt.values())
    m, r = S['magazine'], S['ransomNote']
    if line == 6 and tot < len(m):
        return 'm', tot
    if line == 7:
        return 'm', tot - 1
    if line == 8 and len(m) - tot < len(r):
        return 'r', len(m) - tot
    if line == 9:
        return 'r', len(m) - tot - 1
    return None, None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'magazine' not in S:
        return
    which, k = _idx(S)
    cell = 84
    for row, (name, s, key, c0, sign) in enumerate((('magazine', S['magazine'], 'm', T['green'], '每个字母 +1'),
                                                     ('ransomNote', S['ransomNote'], 'r', T['pink'], '每个字母 −1'))):
        Y = y0 + 40 + row * 140
        cv.text((x0 + 18, Y - 36), f'{name} = "{s}"（{sign}）', 24, T['muted'], bold=True)
        for i, ch in enumerate(s):
            X = x0 + 40 + i * cell
            hit = which == key and i == k
            line = S.get('_line')
            if key == 'm':
                done = line in (8, 9, 10) or (line == 6 and which is None) or (which == 'm' and i < k)
            else:
                done = line == 10 or (line == 8 and which is None) or (which == 'r' and i < k)
            fill = c0 if hit else T['panel2']
            cv.rect((X + 3, Y, X + cell - 3, Y + cell - 6), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + (cell - 6) / 2), ch, 34, T['bg'] if hit else (T['dim'] if done else T['text']),
                    anchor='mm', bold=True)
    # cnt 柱状图
    cnt = S.get('cnt')
    Y0 = y0 + 330
    cv.text((x0 + 18, Y0 - 30), 'cnt[c] = magazine 中的个数 − ransomNote 中的个数（红 = 不够用）', 24, T['muted'], bold=True)
    if cnt is None:
        cv.text((x0 + 40, Y0 + 30), '（尚未创建）', 24, T['dim'])
        return
    base = Y0 + 110
    cv.line([(x0 + 30, base), (x1 - 30, base)], T['border'], 2)
    bcnt = B.get('cnt') or {}
    for i, (ch, v) in enumerate(sorted(cnt.items())):
        X = x0 + 60 + i * 130
        h = v * 40
        col = T['green'] if v >= 0 else T['red']
        if v:
            cv.rect((X, min(base, base - h), X + 70, max(base, base - h)), fill=col, r=6)
        changed = bcnt.get(ch) != v
        cv.text((X + 35, base - h - 8 if v >= 0 else base - h + 8), v, 26, T['yellow'] if changed else T['text'],
                anchor='mb' if v >= 0 else 'mt', bold=True)
        cv.text((X + 35, base + 10 if v >= 0 else base - 10), f"'{ch}'", 24, T['muted'], anchor='mt' if v >= 0 else 'mb', mono=True)


def _cap_for_m(S, B, ret):
    which, k = _idx(S)
    if which == 'm':
        return f'遍历 magazine：`c = \'{S.c}\'`'
    return 'magazine 遍历完：`cnt` 记下了每种字母有几个可用'


def _cap_for_r(S, B, ret):
    which, k = _idx(S)
    if which == 'r':
        return f'遍历 ransomNote：要用掉一个 `\'{S.c}\'`'
    return 'ransomNote 遍历完，检查 cnt'


def _cap_ret(S, B, ret):
    if ret:
        return f'`cnt` 全部 `≥ 0`：每种字母都够用 → 返回 ==True=='
    bad = [k for k, v in S.cnt.items() if v < 0]
    return f'`cnt[\'{bad[0]}\'] = {S.cnt[bad[0]]} < 0`：`\'{bad[0]}\'` 不够用 → 返回 ==False=='


CONFIG = dict(
    num=383, title='赎金信', difficulty='Easy', category='哈希',
    author='灵茶山艾府', technique='计数：出现次数之差',
    tags=['面试经典150'],
    code='''
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False
        cnt = defaultdict(int)
        for c in magazine:
            cnt[c] += 1
        for c in ransomNote:
            cnt[c] -= 1
        return all(c >= 0 for c in cnt.values())
''',
    call=f'[Solution().canConstruct(r, m) for r, m in {CASES}]',
    expect=[True, False],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('c', 'c'), ('cnt', 'dict(cnt)', 'green')],
    captions={
        'if len(ransomNote) > len(magazine)': lambda S, B, r: (
            f'新的一组：`ransomNote = "{S.ransomNote}"`，`magazine = "{S.magazine}"`。'
            f'特判：`{len(S.ransomNote)} ≤ {len(S.magazine)}`，长度没超，继续'),
        'cnt = defaultdict(int)': '`cnt` 统计每种字母的==出现次数之差==',
        'for c in magazine': _cap_for_m,
        'cnt[c] += 1': 'magazine 里多一个可用的 `\'{c}\'`：`cnt[\'{c}\'] = {cnt[c]}`',
        'for c in ransomNote': _cap_for_r,
        'cnt[c] -= 1': lambda S, B, r: (f'用掉一个 `\'{S.c}\'`：`cnt[\'{S.c}\'] = {S.cnt[S.c]}`'
                                        + ('，==变成负数，不够用了==' if S.cnt[S.c] < 0 else '')),
        'return all': _cap_ret,
    },
    cards=dict(
        one_liner='统计每种字母的出现次数之差，全都 ≥ 0 才能拼出来',
        complexity='时间 `O(m)`，空间 `O(|Σ|)`',
        problem=['判断 `ransomNote` 能不能由 `magazine` 里的字符构成',
                 '`magazine` 中的==每个字符只能用一次==',
                 '示例：`("a","b")` → `false`；`("aa","ab")` → `false`；`("aa","aab")` → `true`',
                 '本视频依次跑 `("aa","aab")` 和 `("aa","ab")`'],
        quote='判断 ransomNote 中的每种字母的出现次数，是否都==小于或等于== magazine 中的每种字母的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['magazine 中遇到字母 c：`cnt[c] += 1`；ransomNote 中遇到 c：`cnt[c] -= 1`',
              '最后每个 `cnt[c] ≥ 0` → `true`，否则 `false`',
              '如果 ransomNote 比 magazine 还长，==一定不行==，直接返回'],
        result='两组答案：`True`、`False`',
        summary=['时间 `O(m)`，`m` 是 magazine 的长度；空间 `O(|Σ|)`，`|Σ| = 26`',
                 '原文主写法只有一行：`return Counter(ransomNote) <= Counter(magazine)`',
                 '本视频演示的是原文「写法二」，把 Counter 的比较拆成了计数之差',
                 '易错：只判断字母是否出现过不够，==次数==也要够'],
    ),
)
