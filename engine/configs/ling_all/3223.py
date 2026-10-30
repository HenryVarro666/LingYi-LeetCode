def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    cnt = Counter(s)
    cv.text((x0 + 18, y0 + 4), f's = "{s}"　每种字母留下 (c − 1) % 2 + 1 个', 24, T['muted'], bold=True)
    cell = 44
    rows = sorted(cnt)
    rh = min(120, (y1 - y0 - 150) / max(len(rows), 1))
    tot = 0
    for r, ch in enumerate(rows):
        c = cnt[ch]
        left = (c - 1) % 2 + 1
        tot += left
        Y = y0 + 56 + r * rh
        cv.text((x0 + 30, Y + 22), ch, 36, T['text'], anchor='lm', bold=True, mono=True)
        cv.text((x0 + 80, Y + 22), f'c = {c}', 26, T['muted'], anchor='lm')
        for j in range(c):
            X = x0 + 200 + j * (cell + 8)
            keep = j < left
            cv.rect((X, Y, X + cell, Y + 44), fill=T['green'] if keep else (70, 76, 86), r=8)
        cv.text((x0 + 200 + c * (cell + 8) + 16, Y + 22), f'({c}−1)%2+1 = {left}', 26, T['green'], anchor='lm', bold=True)
    cv.text((x0 + 24, y1 - 30), f'绿色 = 剩下，灰色 = 被删。合计 {tot}', 28, T['text'], bold=True)


CONFIG = dict(
    num=3223, title='操作后字符串的最短长度', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='计数 · 每次减 2',
    code='''
class Solution:
    def minimumLength(self, s: str) -> int:
        return sum((c - 1) % 2 + 1 for c in Counter(s).values())
''',
    call='Solution().minimumLength("abaacbcbb")',
    expect=5,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['s'],
    captions={
        'return sum': lambda S, B, r: '每种字母出现 `c` 次，只要 `c ≥ 3` 就能一次删掉 2 个，最后剩 `(c − 1) % 2 + 1`：' + '，'.join(f'`{ch}`:{c}→{(c-1)%2+1}' for ch, c in sorted(Counter(S.s).items())) + f' → 累加得 =={r}==',
    },
    cards=dict(
        one_liner='操作次数只看字母出现次数，和位置无关',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
        problem=['选下标 `i`，左右各至少有一个和 `s[i]` 相同的字符，就删掉左右最近的那两个',
                 '可以操作任意次，求最短长度',
                 '示例：`"abaacbcbb"` → `5`'],
        quote='操作次数取决于每种字母的出现次数，与字母的位置无关。',
        quote_src='—— 灵茶山艾府题解',
        idea=['出现 `c` 次的字母：只有 `c ≥ 3` 才能操作，每次减 2',
              '奇数次：3,5,7… 一路减到 1；偶数次：4,6,8… 一路减到 2',
              '合并成 `(c − 1) % 2 + 1`，`c = 0, 1, 2` 也适用',
              '把每种字母剩下的个数加起来就是答案'],
        after=[dict(heading='本例手算', lines=['`a` 出现 3 次 → 剩 1', '`b` 出现 4 次 → 剩 2', '`c` 出现 2 次 → 无法操作，剩 2', '合计 `1 + 2 + 2 = 5`'])],
        summary=['时间 `O(n + |Σ|)`，本题 `|Σ| = 26`，空间 `O(|Σ|)`',
                 '易错点：`c = 2` 不能操作，仍剩 2；公式 `(c−1)%2+1` 刚好覆盖',
                 '不用模拟删除，也不用关心字母在哪',
                 '一行写法：`sum(...)` 里直接遍历 `Counter(s).values()`'],
    ),
)
