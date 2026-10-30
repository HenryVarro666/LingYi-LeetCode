WORD = 'abbcbccdbccdcdde'   # 操作 4 次后的 word（前 16 个字符）
KS = list(range(1, 11))


def _trace(p):
    """把下标 p 一路“折回”前半段：每去掉一个最高位的 1，字符就减 1"""
    parts = [str(p)]
    while p:
        hb = 1 << (p.bit_length() - 1)
        p -= hb
        parts.append(f'(−{hb}, +1) {p}')
    return ' → '.join(parts)


def word_view(cv, S, B, box, T):
    """word 的前 16 个字符；按“翻倍”的分组画出前半段 / 后半段；高亮第 k 个"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'word（每次操作：把整个 word 的每个字母 +1 后接在后面，长度翻倍）', 24, T['muted'], bold=True)
    k = S.get('k')
    n = len(WORD)
    cw = min(56, (x1 - x0 - 60) / n)
    sx = x0 + (x1 - x0 - cw * n) / 2
    y = y0 + 160
    # 翻倍分组的括号：长度 1 → 2 → 4 → 8 → 16
    L = 1
    lv = 0
    while L < n:
        yb = y - 26 - lv * 22
        cv.rect((sx + L * cw + 3, yb, sx + 2 * L * cw - 3, yb + 10), fill=T['purple'] if lv % 2 else T['cyan'], r=5)
        L *= 2
        lv += 1
    for i, ch in enumerate(WORD):
        X = sx + i * cw
        hot = k is not None and i == k - 1
        cv.rect((X + 2, y, X + cw - 2, y + cw), fill=T['yellow'] if hot else T['panel2'],
                outline=T['border'], width=1, r=8)
        cv.text((X + cw / 2, y + cw / 2), ch, 28, T['bg'] if hot else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cw / 2, y + cw + 6), str(i), 16, T['dim'], anchor='mt', mono=True)
    cv.text((x0 + 30, y + cw + 40), '彩条 = 每次翻倍新接上的后半段：它 = 前半段每个字母 +1', 22, T['muted'])


def _bin(S):
    k = S.get('k')
    if k is None:
        return '答案 = `a` + (`k - 1` 的二进制里 1 的个数)'
    p = k - 1
    return f"`k - 1 = {p}` = `{p:04b}`（二进制），有 =={p.bit_count()}== 个 1"


def _path(S):
    k = S.get('k')
    if k is None:
        return ''
    p = k - 1
    return f"下标 `{_trace(p)}`：折回 `0`（`'a'`）共 `+{p.bit_count()}`"


def _cap(S, B, ret):
    p = S.k - 1
    return f"`k = {S.k}`：`k - 1 = {p}`（`{p:04b}`）有 `{p.bit_count()}` 个 1 → `ascii_lowercase[{p.bit_count()}]` = =={ret}=="


CONFIG = dict(
    num=3304, title='找出第 K 个字符 I', difficulty='Easy', category='技巧',
    author='灵茶山艾府', technique='O(1)：k-1 的二进制里 1 的个数',
    tags=['字节30天'],
    code='''
class Solution:
    def kthCharacter(self, k: int) -> str:
        return ascii_lowercase[(k - 1).bit_count()]
''',
    call=f'[Solution().kthCharacter(k) for k in {KS}]',
    expect=list('abbcbccdbc'),
    views=[
        dict(type='custom', draw=word_view, h=300),
        dict(type='text', fn=_bin, size=28, h=70),
        dict(type='text', fn=_path, size=26, h=110, lines=2),
    ],
    watch=[('k', 'k', 'yellow'), ('k - 1', lambda S: S['k'] - 1 if 'k' in S else None),
           ('二进制', lambda S: format(S['k'] - 1, '04b') if 'k' in S else None, 'cyan'),
           ('1 的个数', lambda S: (S['k'] - 1).bit_count() if 'k' in S else None, 'green')],
    captions={
        'return ascii_lowercase': _cap,
    },
    cards=dict(
        one_liner='第 k 个字符 = a 往后数 (k-1 的二进制中 1 的个数) 个字母',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['一开始 `word = "a"`；每次操作把 word 的==每个字母换成下一个字母==，再接到 word 后面',
                 '例如 `"c"` → `"cd"`，`"zb"` → `"zbac"`',
                 '操作足够多次后，返回 word 的第 `k` 个字符（`1 <= k <= 500`）',
                 '示例：`k = 5` → `"b"`（`"abbcbccd"`）；`k = 10` → `"c"`'],
        quote='根据迭代写法二，我们相当于在遍历 k−1 二进制的每个比特 1……由于本题 operations[i]=1，所以我们计算的是 k−1 二进制中的 1 的个数。==最终答案为 a 加上 k−1 二进制中的 1 的个数==。',
        quote_src='—— 灵茶山艾府题解（本题是 3307 的特例）',
        idea=['长度翻倍：下标 `p` 落在后半段，就等于前半段 `p - 2^t` 处的字母 ==+1==',
              '把 `p = k-1` 的最高位 1 一个个去掉，每去掉一个就 +1，最后回到下标 0 的 `a`',
              '所以答案 = `a` + `popcount(k-1)`；`k ≤ 500` 时至多 +8，不用模 26'],
        result='依次返回 `a b b c b c c d b c` ✓（`k = 5` → `b`，`k = 10` → `c`）',
        summary=['时间、空间都是 `O(1)`：一行 `ascii_lowercase[(k - 1).bit_count()]`',
                 '易错：要用 `k - 1`（下标从 0 开始），不是 `k`',
                 '`int.bit_count()` 需要 Python 3.10+；老版本用 `bin(k - 1).count("1")`',
                 '视频里对 `k = 1..10` 各调用一次，方便对照 word',
                 '进阶：3307 每次操作可能不 +1，答案是 k-1 的二进制中 1 对应的 operations 之和'],
    ),
)
