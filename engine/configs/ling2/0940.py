S_IN = 'abcb'


def _totals(s):
    f, total, out = [0] * 26, 0, [0]
    for ch in s:
        c = ord(ch) - 97
        others = total - f[c]
        f[c] = 1 + total
        total = f[c] + others
        out.append(total)
    return out


def _pos(S):
    """(正在处理的下标 idx, 已经更新进 f 的字符数 done)"""
    if 'total' not in S or 's' not in S:
        return None, 0
    tots = _totals(S['s'])
    line = S.get('_line')
    if line == 12:
        return None, len(S['s'])
    if S['total'] not in tots:
        return None, 0
    k = tots.index(S['total'])
    if line == 11:
        return k - 1, k
    if line == 10:
        return k, k + 1
    return k, k


def _P(S):
    return _pos(S)[0]


def _groups(prefix):
    g = {}
    for x in prefix:
        new = {y + x for ys in g.values() for y in ys} | {x}
        g[x] = new
    return g


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 's' not in S:
        return
    s = S['s']
    idx, done = _pos(S)
    cv.text((x0 + 18, y0 + 4), f'按结尾字母分组：前 {done} 个字符能组成的不同子序列', 23, T['muted'], bold=True)
    g = _groups(s[:done])
    letters = sorted(set(s))
    y = y0 + 48
    cur = s[idx] if idx is not None and idx < len(s) else None
    just = S.get('_line') == 10
    for ch in letters:
        items = sorted(g.get(ch, ()), key=lambda t: (len(t), t))
        is_cur = ch == cur
        c = T['yellow'] if is_cur else T['text']
        h = 112
        cv.rect((x0 + 20, y, x1 - 20, y + h - 10), fill=(60, 52, 30) if is_cur else T['panel2'], r=12,
                outline=T['yellow'] if is_cur else T['border'], width=2 if is_cur else 1)
        cv.text((x0 + 40, y + 24), f'以 {ch} 结尾', 24, c, anchor='lm', bold=True)
        cv.text((x0 + 40, y + 62), f'f[{ch}] = {len(items)}', 24, T['cyan'], anchor='lm', mono=True, bold=True)
        X = x0 + 200
        Y = y + 14
        for it in items:
            w = cv.tlen(it, 22, mono=True) + 20
            if X + w > x1 - 30:
                X = x0 + 200
                Y += 40
            fresh = just and is_cur
            cv.rect((X, Y, X + w, Y + 32), fill=T['green'] if fresh else T['panel'], r=8, outline=T['border'])
            cv.text((X + w / 2, Y + 16), it, 22, T['bg'] if fresh else T['text'], anchor='mm', mono=True, bold=True)
            X += w + 8
        if not items:
            cv.text((X, y + 44), '（还没有）', 22, T['dim'], anchor='lm')
        y += h
    total = sum(len(v) for v in g.values())
    tail = '；变量 `total` 下一行才更新' if just else ''
    cv.rich(x0 + 30, y + 6, f'各组之和 = =={total}==（结尾不同 → ==不会重复==）{tail}', x1 - x0 - 60, size=24)


CONFIG = dict(
    num=940, title='不同的子序列 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='按结尾字母细分 · 维护 total',
    tags=['字节30天'],
    code='''
MOD = 1_000_000_007

class Solution:
    def distinctSubseqII(self, s: str) -> int:
        f = [0] * 26
        total = 0
        for c in s:
            c = ord(c) - ord('a')
            others = total - f[c]  # total 中不含 f[c] 的部分
            f[c] = 1 + total
            total = (f[c] + others) % MOD
        return total
''',
    call=f"Solution().distinctSubseqII('{S_IN}')",
    expect=13,
    views=[
        dict(type='string', var='s', label='s（指针 = 当前字符）', cell=90, h=190,
             pointers={_P: 'yellow'}, pointer_labels={_P: '当前'}),
        dict(type='custom', draw=_draw, h=440),
    ],
    watch=[('c', 'c', 'yellow'), ('others', 'others'), ('total', 'total', 'green'),
           ('f[a..c]', lambda S: S['f'][:3] if 'f' in S else None, 'cyan')],
    captions={
        'f = [0] * 26': '`f[j]`：以字母 j 结尾的不同子序列个数（a~z 用 0~25 表示）',
        'total = 0': '`total = Σ f[j]`：所有不同子序列的个数',
        'for c in s': lambda S, B, ret: (f'下一个字符 `{S.c}`' if isinstance(S.c, str) and _pos(S)[0] is not None else '字符串遍历完了'),
        "c = ord(c) - ord('a')": '`{chr(c + 97)}` → 下标 `{c}`',
        'others = total - f[c]': lambda S, B, ret: (
            f'`others = total − f[{chr(S.c + 97)}] = {S.total} − {S.f[S.c]} = {S.others}`：==不以 {chr(S.c + 97)} 结尾==的子序列，这次不会变'),
        'f[c] = 1 + total': lambda S, B, ret: (
            f'把 `{chr(S.c + 97)}` 接到前面 ==所有 {B.total} 个== 子序列后面，再加上 `{chr(S.c + 97)}` 单独一个：'
            f'`f[{chr(S.c + 97)}] = 1 + {B.total} = {S.f[S.c]}`'
            + ('；旧的以它结尾的都被包含了，==不会重复==' if B.f[S.c] else '')),
        'total = (f[c] + others)': '`total = f[c] + others = {f[c]} + {others} = {total}`',
        'return total': '共 =={ret}== 个不同的非空子序列',
    },
    cards=dict(
        one_liner='分别统计以 a~z 结尾的不同子序列，s[i] 接到前面所有子序列后面',
        complexity='时间 `O(n + 26)`，空间 `O(26)`',
        problem=['求字符串 `s` 的==不同非空子序列==个数，答案对 `10^9 + 7` 取余',
                 '示例：`"abc"` → `7`；`"aba"` → `6`；`"aaa"` → `3`',
                 '本视频：`"abcb"` → `13`'],
        quote='如果把原问题细分一下，改为==分别统计以 a, b, ⋯, z 结尾的不同子序列的个数==，问题就迎刃而解了。',
        quote_src='—— 灵茶山艾府题解 · 提示 2',
        idea=['把 `s[i]` 加到==前面所有==不同子序列末尾，再加上它自己 → 以 `s[i]` 结尾的全部子序列',
              '以其他字母结尾的个数不变；所以 `f[s[i]] = 1 + Σf`',
              '`total` 里只有 `f[c]` 在变：先算 `others = total − f[c]`，就不用每次 `sum(f)`'],
        result='`f[a] + f[b] + f[c] = 1 + 8 + 4 = 13` ✓',
        summary=['时间 `O(n + 26)`，空间 `O(26)`',
                 '为什么不重复？同一个子序列只在它==最后一次出现的位置==被统计',
                 '易错：`others` 要在更新 `f[c]` 之前算；记得取模',
                 '原题解先写二维 `f[i+1][j]`，再压成一维 `sum(f)`，最后用 `total` 优化到 `O(n + 26)`'],
    ),
)
