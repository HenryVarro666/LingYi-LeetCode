S0 = 'abcd'
P0 = 'bcc'


def _inner(S):
    return S.get('_inner') or S


def _in_z(S):
    return 'box_l' in _inner(S) and 'z' in _inner(S)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    I = _inner(S)
    m = len(P0)
    W = x1 - x0 - 40
    if _in_z(S):
        t, z = I['s'], I['z']
        second = 'pre_z' in S
        n = len(t)
        cell = min(84, W / n)
        sx = x0 + 20 + (W - cell * n) / 2
        ys = y0 + 110
        ch = cell * 0.85
        i = I.get('i', 1)
        bl, br = I['box_l'], I['box_r']
        ln = S.get('_line', 0)
        cv.text((x0 + 18, y0 + 4), f"calc_z（{'反转后的' if second else '正向的'} pattern + s）：z[i] = t[i:] 与 t 的最长公共前缀", 22, T['muted'], bold=True)
        cv.text((sx, ys - 40), 'pattern 部分' if not second else 'rev(pattern) 部分', 20, T['blue'], anchor='lb', bold=True)
        cv.text((sx + m * cell + 8, ys - 40), 's 部分' if not second else 'rev(s) 部分', 20, T['cyan'], anchor='lb', bold=True)
        if br >= bl and br > 0:
            cv.rect((sx + bl * cell + 2, ys - 8, sx + (br + 1) * cell - 2, ys + ch + 8), fill=T['yellow'], alpha=45, r=10)
            cv.text((sx + bl * cell + 4, ys + ch + 32), f'z-box [{bl}, {br}]', 20, T['yellow'], anchor='lt', bold=True)
        zi = z[i] if i < n else 0
        for k, c in enumerate(t):
            X = sx + k * cell
            base = T['blue'] if k < m else T['cyan']
            fill = T['panel2']
            cv.rect((X + 3, ys, X + cell - 3, ys + ch), fill=fill, r=8, outline=base, width=2)
            cv.text((X + cell / 2, ys + ch / 2), c, 34, T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, ys + ch + 6), k, 18, T['dim'], anchor='mt', mono=True)
        # 当前比较
        if ln in (9, 10, 11) and i < n:
            a, b = zi, i + zi
            if ln == 9 and b < n:
                for k, col in ((a, 'pink'), (b, 'green' if t[a] == t[b] else 'red')):
                    X = sx + k * cell
                    cv.rect((X + 1, ys - 3, X + cell - 1, ys + ch + 3), outline=T[col], width=5, r=10)
        # 指针
        if i < n:
            X = sx + i * cell + cell / 2
            cv.tri_up(X, ys + ch + 68, 10, T['yellow'])
            cv.text((X, ys + ch + 82), 'i', 22, T['yellow'], anchor='mt', bold=True)
        # z 值
        yz = ys + ch + 150
        cv.text((x0 + 18, yz - 8), 'z 数组（已算出的部分；黄框 = 正在算的 z[i]）', 22, T['muted'], bold=True)
        for k in range(n):
            X = sx + k * cell
            known = k < i or (k == i and ln in (8, 9, 10, 11)) or i >= n or ln >= 12
            cur = k == i and i < n
            cv.rect((X + 3, yz + 30, X + cell - 3, yz + 30 + ch), fill=T['panel2'], r=8,
                    outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
            cv.text((X + cell / 2, yz + 30 + ch / 2), z[k] if (known or k == 0) else '·', 32,
                    T['text'] if known else T['dim'], anchor='mm', bold=True, mono=True)
        return
    # ---- minStartingIndex 里
    s = S.get('s', S0)
    n = len(s)
    cell = min(80, W / max(n, m + 1))
    sx = x0 + 20 + (W - cell * n) / 2
    ys = y0 + 50
    ch = cell * 0.75
    ln = S.get('_line', 0)
    i = S.get('i') if ln >= 19 else None
    cv.text((x0 + 18, y0 + 4), '枚举窗口 s[i-m .. i-1]，看它和 pattern 差几个字符', 22, T['muted'], bold=True)
    if i is not None:
        cv.rect((sx + (i - m) * cell, ys - 8, sx + i * cell, ys + ch + 8), fill=T['blue'], alpha=40, r=12)
    for k, c in enumerate(s):
        X = sx + k * cell
        cv.rect((X + 4, ys, X + cell - 4, ys + ch), fill=T['panel2'], r=8, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), c, 34, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + ch + 10), k, 16, T['dim'], anchor='mt', mono=True)
    cv.text((sx - 10, ys + ch / 2), 's', 28, T['muted'], anchor='rm', bold=True)
    yp = ys + ch + 40
    if i is not None:
        for k, c in enumerate(P0):
            X = sx + (i - m + k) * cell
            cv.rect((X + 4, yp, X + cell - 4, yp + ch), fill=T['panel2'], r=8, outline=T['pink'], width=2)
            cv.text((X + cell / 2, yp + ch / 2), c, 34, T['pink'], anchor='mm', bold=True, mono=True)
        cv.text((sx - 10, yp + ch / 2), 'pattern', 22, T['pink'], anchor='rm', bold=True)
    pre, suf = S.get('pre_z'), (S.get('suf_z') if ln >= 17 else None)
    yr = yp + ch + 50
    j_pre = (i - m) if i is not None else None
    j_suf = (i - 1) if i is not None else None
    cv.text((x0 + 18, yr - 4), 'pre_z[j+m]：从 s[j] 开始能匹配 pattern 前缀多长', 22, T['blue'], bold=True)
    for k in range(n):
        X = sx + k * cell
        cur = j_pre == k
        cv.rect((X + 4, yr + 30, X + cell - 4, yr + 30 + ch), fill=T['panel2'], r=8,
                outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
        cv.text((X + cell / 2, yr + 30 + ch / 2), pre[m + k] if pre else '·', 30, T['text'] if pre else T['dim'], anchor='mm', bold=True, mono=True)
    yr2 = yr + ch + 70
    cv.text((x0 + 18, yr2 - 4), 'suf_z[j]：到 s[j] 结束能匹配 pattern 后缀多长', 22, T['purple'], bold=True)
    for k in range(n):
        X = sx + k * cell
        cur = j_suf == k
        cv.rect((X + 4, yr2 + 30, X + cell - 4, yr2 + 30 + ch), fill=T['panel2'], r=8,
                outline=T['yellow'] if cur else T['border'], width=4 if cur else 1)
        cv.text((X + cell / 2, yr2 + 30 + ch / 2), suf[k] if suf else '·', 30, T['text'] if suf else T['dim'], anchor='mm', bold=True, mono=True)


def _fm(S):
    ln = S.get('_line', 0)
    if not _in_z(S) and ln >= 19 and 'i' in S and 'pre_z' in S and 'suf_z' in S:
        i, m = S['i'], S['m']
        a, b = S['pre_z'][i], S['suf_z'][i - 1]
        ok = a + b >= m - 1
        return f"`pre_z[{i}] + suf_z[{i - 1}]` = `{a} + {b}` = =={a + b}== {'≥' if ok else '<'} `m − 1` = `{m - 1}` → {'==能改成一样（至多改 1 个）==' if ok else '要改的字符超过 1 个'}"
    return ''


def _zcap_if(S, B, r):
    i, bl, br = S.i, S.box_l, S.box_r
    if i <= br:
        return f'`i = {i}` ≤ `box_r = {br}`：落在 z-box 里，==可以借用镜像位置== `z[{i - bl}] = {S.z[i - bl]}` 的结果'
    return f'`i = {i}` > `box_r = {br}`：在 z-box 外面，没有现成结果，只能一格一格比'


def _zcap_min(S, B, r):
    i, bl, br = S.i, S.box_l, S.box_r
    return f'`i = {i}` 落在 z-box `[{bl}, {br}]` 里：`z[{i}] = min(z[{i - bl}], box_r − i + 1)` = `min({S.z[i - bl]}, {br - i + 1})` = =={S.z[i]}==，==直接借用镜像位置的结果=='


def _zcap_while(S, B, r):
    i, z, t = S.i, S.z, S.s
    k = i + z[i]
    if k >= len(t):
        return f'`i + z[i] = {k}` 到头了 → `z[{i}] = {z[i]}` 定下来'
    ok = t[z[i]] == t[k]
    return (f'比 `s[z[i]]={t[z[i]]}`（前缀）和 `s[i+z[i]]={t[k]}`（当前）：' + ('==相等== → 再多匹配一个' if ok else '==不等== → `z[%d] = %d` 定下来' % (i, z[i])))


def _loop_cap(S, B, r):
    n = len(S.get('pre_z', [])) and 0
    return ''


CONFIG = dict(
    num=3303, title='第一个几乎相等子字符串的下标', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 + Z 函数',
    tags=['灵神题单·动态规划', '灵神题单·字符串', '难度分 2509'],
    code='''
class Solution:
    def calc_z(self, s: str) -> List[int]:
        n = len(s)
        z = [0] * n
        box_l = box_r = 0  # z-box 左右边界
        for i in range(1, n):
            if i <= box_r:
                z[i] = min(z[i - box_l], box_r - i + 1)  # 改成手动 if 可以加快速度
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                box_l, box_r = i, i + z[i]
                z[i] += 1
        return z

    def minStartingIndex(self, s: str, pattern: str) -> int:
        pre_z = self.calc_z(pattern + s)
        suf_z = self.calc_z(pattern[::-1] + s[::-1])
        suf_z.reverse()  # 也可以不反转，下面写 suf_z[-i]
        m = len(pattern)
        for i in range(m, len(s) + 1):
            if pre_z[i] + suf_z[i - 1] >= m - 1:
                return i - m
        return -1
''',
    call=f'Solution().minStartingIndex({S0!r}, {P0!r})',
    expect=1,
    skip=['if i <= box_r', 'for i in range(1, n)', 'box_l, box_r = i, i + z[i]', 'n = len(s)', 'z = [0] * n'],
    views=[
        dict(type='custom', draw=_draw, h=620),
        dict(type='text', fn=_fm, size=26, h=70),
    ],
    watch=[('i', 'i', 'yellow'), ('box_l', 'box_l', 'blue'), ('box_r', 'box_r', 'pink'), ('m', 'm', 'cyan')],
    captions={
        'box_l = box_r = 0': '`z-box` = 目前找到的、最靠右的「和前缀匹配的区间」`[box_l, box_r]`，一开始是空的',
        'z[i] = min': _zcap_min,
        'while i + z[i] < n': _zcap_while,
        'z[i] += 1': '匹配长度 +1：`z[{i}] = {z[i]}`，z-box 扩到 `[{box_l}, {box_r}]`',
        'return z': 'Z 数组算完：`z = {z}`',
        'pre_z = self.calc_z': '第一个问题：`pre_z[i+m]` = `s[i..]` 能匹配 `pattern` 前缀的长度（把 `pattern` 拼在前面求 Z）',
        'suf_z = self.calc_z': '第二个问题：两个串都反转再求 Z，得到「以 `s[j]` 结尾能匹配 `pattern` 后缀」的长度',
        'suf_z.reverse()': '反转回来，`suf_z[j]` 就对应原串 `s[..j]` 的后缀匹配长度：`{suf_z}`',
        'm = len(pattern)': '`m = {m}`',
        'for i in range(m, len(s) + 1)': lambda S, B, r: f'枚举窗口 `s[{S.i - S.m}..{S.i - 1}]`（`i` 是窗口右端 +1）',
        'if pre_z[i] + suf_z[i - 1] >= m - 1': lambda S, B, r: (
            f'前缀能匹配 `{S.pre_z[S.i]}` 个、后缀能匹配 `{S.suf_z[S.i - 1]}` 个，合计 `{S.pre_z[S.i] + S.suf_z[S.i - 1]}`，'
            + ('≥ `m−1`：==中间最多一个字符不同==，窗口合格' if S.pre_z[S.i] + S.suf_z[S.i - 1] >= S.m - 1 else '< `m−1`：至少 2 个字符不同，下一个窗口'))
        ,
        'return i - m': '最早的合格窗口从 `i − m = {i - m}` 开始',
    },
    cards=dict(
        one_liner='前缀匹配 + 后缀匹配 ≥ m−1，说明至多差一个字符',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['在 `s` 里找下标最小的子串，它和 `pattern` ==至多改一个字符==就能相等',
                 '没有就返回 `-1`',
                 '示例：`s = "abcdefg", pattern = "bcdffg"` → `1`'],
        quote='对于每个从 s[i] 开始的字符串 s[i..]，计算它能匹配 pattern 多长的前缀；对于每个以 s[j] 结尾的字符串 s[..j]，计算它能匹配 pattern 多长的后缀。',
        quote_src='—— 灵茶山艾府题解',
        idea=['窗口 `s[i..i+m-1]` 和 `pattern` 最多差一个字符 ⇔ ==前缀匹配长度 + 后缀匹配长度 ≥ m−1==',
              '前缀匹配长度：对 `pattern + s` 求 Z 数组；后缀匹配长度：反转后求 Z 再反转',
              '枚举窗口，第一个满足的就是答案（本视频用 `"abcd"` 和 `"bcc"` 演示）'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '后缀那一半：`rev(pattern) + rev(s)` 的 Z 数组要 ==再反转== 才和原下标对齐',
                 '`pre_z[i]` 和 `suf_z[i-1]` 的下标差一位，别写错',
                 '进阶「至多改 k 个」：把 `>= m-1` 改成 `>= m-k`',
                 '同类题：2223 构造字符串的总得分和、3031/3045（Z 函数）'],
    ),
)
