_CODE = '''
class SparseTable:
    def __init__(self, nums: List[int]):
        n = len(nums) - 1
        w = n.bit_length()
        st = [[0] * n for _ in range(w)]
        st[0] = [r1 - l1 + r2 - l2 for (l1, r1), (l2, r2) in pairwise(nums)]
        for i in range(1, w):
            for j in range(n - (1 << i) + 1):
                st[i][j] = max(st[i - 1][j], st[i - 1][j + (1 << (i - 1))])
        self.st = st

    # 查询区间最大值，[l, r) 左闭右开
    def query(self, l: int, r: int) -> int:
        if l >= r:
            return 0
        k = (r - l).bit_length() - 1
        return max(self.st[k][l], self.st[k][r - (1 << k)])

class Solution:
    def maxActiveSectionsAfterTrade(self, s: str, queries: List[List[int]]) -> List[int]:
        n = len(s)
        total1 = 0
        belong = [0] * n  # 每个 0 所属的区间下标，每个 1 右边最近的 0 区间下标
        a = [(-1, -1)]
        start = 0
        for i, b in enumerate(s):
            belong[i] = len(a)  # 标记
            if i == n - 1 or b != s[i + 1]:
                if b == '1':
                    total1 += i - start + 1
                else:
                    a.append((start, i + 1))
                start = i + 1
        a.append((n + 1, n + 1))

        def merge(x: int, y: int) -> int:
            return x + y if x > 0 and y > 0 else 0

        st = SparseTable(a)
        ans = []
        for ql, qr in queries:
            i = belong[ql]
            if ql and s[ql] == '0' == s[ql - 1]:
                i += 1  # i 在残缺区间中
            j = belong[qr] - 1
            if qr + 1 < n and s[qr] == '0' != s[qr + 1]:
                j += 1  # j 刚好在完整区间的右端点，无需减一
            qr += 1

            mx = 0
            if i <= j:
                mx = max(
                    st.query(i, j),
                    merge(a[i - 1][1] - ql, a[i][1] - a[i][0]),
                    merge(qr - a[j + 1][0], a[j][1] - a[j][0]),
                )
            elif i == j + 1:
                mx = merge(a[i - 1][1] - ql, qr - a[j + 1][0])
            ans.append(total1 + mx)
        return ans
'''
_LN = {k: i + 1 for i, l in enumerate(_CODE.strip('\n').split('\n')) for k in ['qr += 1'] if l.strip() == k}
_QR_LINE = _LN['qr += 1']

S0 = '010010'
QUERIES = [[0, 5], [3, 5]]


def _brute(s, l, r):
    import re
    t = '1' + s[l:r + 1] + '1'
    best = 0

    def blocks(u):
        return [(m.start(), m.end(), m.group()[0]) for m in re.finditer(r'0+|1+', u)]
    for a, b, c in blocks(t):
        if c == '1' and a > 0 and b < len(t):
            u = t[:a] + '0' * (b - a) + t[b:]
            for a2, b2, c2 in blocks(u):
                if c2 == '0' and a2 > 0 and b2 < len(u):
                    best = max(best, (u[:a2] + '1' * (b2 - a2) + u[b2:]).count('1') - 2)
    best = max(best, t.count('1') - 2)
    return s.count('1') - s[l:r + 1].count('1') + best


EXPECT = [_brute(S0, l, r) for l, r in QUERIES]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    n = len(s)
    cw = min(84, (x1 - x0 - 120) / n)
    sx = x0 + 100
    a = S.get('a', [])
    belong = S.get('belong')
    in_q = 'ql' in S
    cv.text((x0 + 18, y0 + 4), 's 与 0 的区间 a（左闭右开）', 24, T['muted'], bold=True)
    ys = y0 + 62
    cv.text((sx - 14, ys + 22), 's', 22, T['muted'], anchor='rm', bold=True)
    cv.text((sx - 14, ys + 70), 'belong', 20, T['muted'], anchor='rm', bold=True)
    for k, ch in enumerate(s):
        X = sx + k * cw
        run = None
        for idx, (l, r) in enumerate(a):
            if l <= k < r and l >= 0:
                run = idx
        fill = T['panel2']
        if run is not None:
            fill = (88, 62, 30) if run % 2 else (60, 52, 80)
        cv.rect((X + 2, ys, X + cw - 2, ys + 44), fill=fill, outline=T['border'], width=2, r=6)
        cv.text((X + cw / 2, ys + 22), ch, 26, T['text'] if ch == '1' else T['orange'], anchor='mm', bold=True, mono=True)
        cv.text((X + cw / 2, ys - 4), k, 16, T['dim'], anchor='mb', mono=True)
        if belong is not None and k < len(belong):
            cv.text((X + cw / 2, ys + 70), belong[k], 22, T['cyan'], anchor='mm', mono=True)
    if in_q:
        ql, qr = S['ql'], S['qr']
        qe = qr if S['_line'] >= _QR_LINE else qr + 1
        cv.rect((sx + ql * cw, ys - 8, sx + qe * cw, ys + 52), outline=T['yellow'], width=4, r=8)
    # 0 区间
    yb = ys + 112
    cv.text((sx - 14, yb + 18), 'a', 22, T['muted'], anchor='rm', bold=True)
    for idx, (l, r) in enumerate(a):
        if l < 0 or l > n:
            continue
        col = T['orange'] if idx % 2 else T['purple']
        cv.rect((sx + l * cw + 2, yb, sx + r * cw - 2, yb + 36), fill=col, alpha=200, r=6)
        cv.text(((sx + l * cw + sx + r * cw) / 2, yb + 18), f'a[{idx}] 长{r - l}', 19, T['bg'], anchor='mm', bold=True)
    if in_q and 'j' in S and S['_line'] >= _QR_LINE - 4:
        for name, idx, c in (('i', S['i'], T['blue']), ('j', S['j'], T['pink'])):
            if 0 <= idx < len(a) and 0 <= a[idx][0] <= n:
                l, r = a[idx]
                X = (sx + l * cw + sx + r * cw) / 2
                cv.tri_up(X + (-14 if name == 'i' else 14), yb + 44, 9, c)
                cv.text((X + (-14 if name == 'i' else 14), yb + 62), name, 22, c, anchor='mt', bold=True)
            elif 0 <= idx < len(a):
                cv.text((sx + 0, yb + 70), f'{name} = {idx}（哨兵）', 19, c)


def _mx_text(S, B):
    if 'mx' not in S or 'ql' not in S or S['_line'] < _QR_LINE + 2:
        return ''
    return f"本次查询 `[{S['ql']}, {S['qr'] - 1}]`：答案 = `total1` ({S['total1']}) + `mx` ({S['mx']})"


CONFIG = dict(
    num=3501, title='操作后最大活跃区段数 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='区间化 + ST 表（每个字符标记所属区间）',
    tags=['灵神题单·常用数据结构', '难度分 2941'],
    code=_CODE,
    call=f'Solution().maxActiveSectionsAfterTrade({S0!r}, {QUERIES!r})',
    expect=EXPECT,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='table', var='st.st', label='ST 表：st[k][j] = 从 j 开始 2^k 个「相邻两段长度和」的最大值', h=170, values=True, cell=52),
        dict(type='text', fn=_mx_text, h=50),
    ],
    watch=['total1', 'i', 'j', 'mx', ('ans', 'ans', 'green')],
    skip=['start = i + 1', 'ans = []', 'n = len(nums) - 1', 'w = n.bit_length()', 'for i, b in enumerate(s)',
          'if i == n - 1 or b != s[i + 1]', 'for i in range(1, w)', 'for j in range(n - (1 << i) + 1)',
          'start = 0', 'total1 = 0', 'n = len(s)'],
    max_steps=70,
    captions={
        'belong = [0] * n': '`belong[k]`：每个 0 属于哪个区间；每个 1 指向它右边最近的 0 区间',
        'a = [(-1, -1)]': '`a` 存所有 0 段（左闭右开）。先放哨兵 `(-1, -1)`，后面不用判断边界',
        'belong[i] = len(a)': '第 `{i}` 位是 `{s[i]}`：`belong[{i}] = {len(a)}`，' + '{"这一段到此结束" if (i == n - 1 or s[i] != s[i + 1]) else "这一段还没结束"}',
        "if b == '1'": '`{s[i]}` 段 `[{start}, {i + 1})` 结束 → {"是 1，计入 total1" if b == "1" else "是 0，记成一个区间"}',
        'total1 +=': '这段 1 长 `{i - start + 1}`，`total1` → =={total1}==',
        'a.append((start': '0 段 `[{start}, {i + 1})` 加入 `a[{len(a) - 1}]`',
        'a.append((n + 1': '末尾也放一个哨兵 `(n+1, n+1)`',
        'st = SparseTable(a)': '用 `a` 建 ST 表：存「相邻两个 0 区间长度之和」的区间最大值',
        'st[0] = [': '第 0 层：相邻两个 0 区间的长度和 `{st[0]}`（哨兵参与的格子是 0 附近的无效值）',
        'st[i][j] = max': '`st[{i}][{j}]` = 前一层相邻两格取大 = =={st[i][j]}==',
        'self.st = st': 'ST 表建好，之后每次区间最大值 `O(1)`',
        'i = belong[ql]': '`i = belong[{ql}] = {i}`：从 `ql` 起第一个 0 区间的下标',
        'j = belong[qr] - 1': '`j = belong[{qr}] - 1 = {j}`：`qr` 左边最后一个 0 区间',
        'qr += 1': '改成左闭右开：`qr` = {qr}',
        'mx = 0': '`mx`：能额外换来的 0 的个数，先设 0',
        'if i <= j': '`i <= j`（`{i} <= {j}`）→ ==' + '{"[ql,qr) 里有完整的 0 区间" if i <= j else "没有完整区间"}' + '==',
        'elif i == j + 1': '`i == j + 1`（`{i} == {j + 1}`）→ =={"成立：只有两个相邻的残缺区间" if i == j + 1 else "不成立"}==',
        'mx = max(': '三个候选里取最大，作为 `mx`（目前 `mx` = {mx}）',
        'st.query(i, j)': '候选一：完整区间 `[{i}, {j})` 内相邻两段长度和的最大值，查 ST 表 `O(1)`',
        'merge(a[i - 1][1] - ql': '候选二：左端残缺区间（{"没有" if a[i - 1][1] - ql <= 0 else "长 " + str(a[i - 1][1] - ql)}）+ 第一个完整区间',
        'merge(qr - a[j + 1][0]': '候选三：最后一个完整区间 + 右端残缺区间（{"没有" if qr - a[j + 1][0] <= 0 else "长 " + str(qr - a[j + 1][0])}）',
        'mx = merge(': '只有两个残缺区间：`merge(左残缺 {a[i - 1][1] - ql}, 右残缺 {qr - a[j + 1][0]})`',
        'return x + y if': '`merge({x}, {y})`：两段都 > 0 才能一起换，否则得 0 → =={x + y if x > 0 and y > 0 else 0}==',
        'ans.append': '答案 = `total1 + mx` = {total1} + {mx} = =={total1 + mx}==',
    },
    cards=dict(
        one_liner='把 0 的连续段当成区间：答案 = 1 的总数 + 最长的相邻两段 0',
        complexity='时间 `O(n log n + q)`，空间 `O(n log n)`',
        problem=['二进制串 `s`，一次操作：把被 0 包围的一段 1 变成 0，再把被 1 包围的一段 0 变成 1',
                 '每个查询 `[l, r]` 只看子串，两端当作各有一个 1，查询互相独立',
                 '返回每个查询操作后最多有多少个 1'],
        quote='设 s 中的所有连续 0 对应的（左闭右开）区间列表为 a ……答案为 total1 加上 0 最多的 010 子串中的 0 的个数 mx。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把所有 0 段存成区间 `a`，两端加哨兵，省去边界判断',
              '查询里分类：完整区间之间的相邻和用 ST 表查；两端的残缺区间单独和最近的完整区间相加',
              '写法二：预处理 `belong`，每个查询 `O(1)` 找到 i、j，不用二分'],
        summary=['时间 `O(n log n + q)`（写法一用二分，每次查询 `O(log n)`），空间 `O(n log n)`',
                 '`total1` 是整个 `s` 里 1 的个数，答案 = `total1 + mx`',
                 '残缺区间长度要对着 `ql / qr` 截断；`merge` 要求两段都存在（> 0）',
                 '`qr += 1` 之后是左闭右开，下标 i、j 必须在它之前算',
                 '同类：3499（单次查询版）；ST 表也可换成线段树'],
    ),
)
