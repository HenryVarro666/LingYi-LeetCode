_CODE = '''
class Solution(object):
    def maxActiveSectionsAfterTrade(self, s, queries):
        
        n = len(s)

        intervals = []
        p = 0
        one = n
        while p < n:
            while p < n and s[p] == '1':
                p += 1
            
            if p == n:
                break
            
            q = p + 1
            while q < n and s[q] == '0':
                q += 1
            
            intervals.append((p, q - 1))
            one -= q - p
            p = q

        if not intervals:
            return [one] * len(queries)

        length = [0]
        for index in range(1, len(intervals)):
            length.append(intervals[index][1] - intervals[index][0] + 1 + intervals[index - 1][1] - intervals[index - 1][0] + 1)
        
        n = len(intervals)
        f = [0] * (n * 4)

        def build(p, start, end):
            if start == end:
                f[p] = length[start]
                return
            
            mid = (start + end) // 2
            build(p * 2 + 1, start, mid)
            build(p * 2 + 2, mid + 1, end)
            f[p] = max(f[p * 2 + 1], f[p * 2 + 2])
        
        def find(p, start, end, i, j):
            if start == i and end == j:
                return f[p]
            mid = (start + end) // 2
            if j <= mid:
                return find(p * 2 + 1, start, mid, i, j)
            elif i >= mid + 1:
                return find(p * 2 + 2, mid + 1, end, i, j)
            else:
                return max(find(p * 2 + 1, start, mid, i, mid), find(p * 2 + 2, mid + 1, end, mid + 1, j))

        build(0, 0, n - 1)

        res = []
        for left, right in queries:
            if left > intervals[-1][-1] or right < intervals[0][0]:
                res.append(one)
                continue
            
            lo = 0
            hi = len(intervals) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if intervals[mid][1] >= left:
                    hi = mid
                else:
                    lo = mid + 1

            p = lo

            lo = 0
            hi = len(intervals) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if intervals[mid][0] <= right:
                    lo = mid
                else:
                    hi = mid - 1
            
            q = hi

            best = 0
            if p + 2 <= q - 1:
                best = find(0, 0, n - 1, p + 2, q - 1)
            if q > p:
                best = max(best, min(intervals[p + 1][1], right) - intervals[p + 1][0] + 1 + intervals[p][1] - max(intervals[p][0], left) + 1)
                best = max(best, intervals[q - 1][1] - max(intervals[q - 1][0], left) + 1 + min(intervals[q][1], right) - intervals[q][0] + 1)
            
            res.append(one + best)
        
        return res
'''


_LINES = _CODE.strip('\n').split('\n')


def _ln(text, nth=1):
    k = 0
    for i, l in enumerate(_LINES):
        if text in l:
            k += 1
            if k == nth:
                return i + 1
    return 10 ** 6


L_LO1, L_P, L_LO2, L_Q = _ln('lo = 0', 1), _ln('p = lo'), _ln('lo = 0', 2), _ln('q = hi')
L_BEST = _ln('best = 0')

S0 = '01001010'
QUERIES = [[0, 7], [3, 7]]


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


def _draw_s(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    n0 = len(s)
    cw = min(84, (x1 - x0 - 120) / n0)
    sx = x0 + 100
    iv = S.get('intervals', [])
    ln = S['_line']
    cv.text((x0 + 18, y0 + 4), 's 与 0 的区间 intervals（闭区间 [p, q-1]）', 24, T['muted'], bold=True)
    ys = y0 + 62
    cv.text((sx - 14, ys + 22), 's', 22, T['muted'], anchor='rm', bold=True)
    for k, ch in enumerate(s):
        X = sx + k * cw
        run = None
        for idx, (l, r) in enumerate(iv):
            if l <= k <= r:
                run = idx
        fill = T['panel2'] if run is None else ((88, 62, 30) if run % 2 else (60, 52, 80))
        cv.rect((X + 2, ys, X + cw - 2, ys + 44), fill=fill, outline=T['border'], width=2, r=6)
        cv.text((X + cw / 2, ys + 22), ch, 26, T['text'] if ch == '1' else T['orange'], anchor='mm', bold=True, mono=True)
        cv.text((X + cw / 2, ys - 4), k, 16, T['dim'], anchor='mb', mono=True)
    if 'left' in S and 'right' in S and 'res' in S and ln >= _ln('for left, right in queries'):
        cv.rect((sx + S['left'] * cw, ys - 8, sx + (S['right'] + 1) * cw, ys + 52), outline=T['yellow'], width=4, r=8)
    yb = ys + 84
    cv.text((sx - 14, yb + 18), 'intervals', 20, T['muted'], anchor='rm', bold=True)
    for idx, (l, r) in enumerate(iv):
        col = T['orange'] if idx % 2 else T['purple']
        cv.rect((sx + l * cw + 2, yb, sx + (r + 1) * cw - 2, yb + 36), fill=col, alpha=200, r=6)
        cv.text(((sx + l * cw + sx + (r + 1) * cw) / 2, yb + 18), f'[{idx}] 长{r - l + 1}', 19, T['bg'], anchor='mm', bold=True)
    if iv and 'lo' in S and L_LO1 <= ln <= L_Q:
        for name, c, dx in (('lo', T['blue'], -12), ('hi', T['pink'], 12)):
            idx = S.get(name)
            if idx is not None and 0 <= idx < len(iv):
                l, r = iv[idx]
                X = (sx + l * cw + sx + (r + 1) * cw) / 2 + dx
                cv.tri_up(X, yb + 44, 9, c)
                cv.text((X, yb + 62), name, 21, c, anchor='mt', bold=True)
    if iv and 'p' in S and 'q' in S and ln >= L_Q and ln >= 0 and 'left' in S:
        for name, c, dx in (('p', T['green'], -12), ('q', T['cyan'], 12)):
            idx = S.get(name)
            if idx is not None and 0 <= idx < len(iv):
                l, r = iv[idx]
                X = (sx + l * cw + sx + (r + 1) * cw) / 2 + dx
                cv.tri_up(X, yb + 44, 9, c)
                cv.text((X, yb + 62), name, 21, c, anchor='mt', bold=True)


def _seg(m):
    out = []

    def go(p, a, b, d):
        out.append((p, a, b, d))
        if a < b:
            mid = (a + b) // 2
            go(p * 2 + 1, a, mid, d + 1)
            go(p * 2 + 2, mid + 1, b, d + 1)
    go(0, 0, m - 1, 0)
    return out


def _draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    iv = S.get('intervals')
    f = S.get('f')
    if not iv or f is None:
        cv.text((x0 + 18, y0 + 4), '线段树 f：区间最大值（还没建）', 24, T['muted'], bold=True)
        return
    m = len(iv)
    sk = _seg(m)
    bf = B.get('f', f)
    maxd = max(d for *_, d in sk) + 1
    cv.text((x0 + 18, y0 + 4), '线段树 f：每个节点 = 相邻两个 0 区间长度和 的最大值', 24, T['muted'], bold=True)
    slot = (x1 - x0 - 40) / m
    bw, bh = min(slot * 0.9, 120), 62
    dy = min(110, (y1 - y0 - 100 - bh) / max(1, maxd - 1))
    inner = S.get('_inner', {})
    cur = (inner.get('start'), inner.get('end')) if 'start' in inner and 'end' in inner else None
    pos = {}
    for p, a, b, d in sk:
        pos[p] = (x0 + 20 + (a + b + 1) / 2 * slot, y0 + 64 + d * dy + bh / 2)
    for p, a, b, d in sk:
        if a < b:
            for c in (p * 2 + 1, p * 2 + 2):
                cv.line([(pos[p][0], pos[p][1] + bh / 2), (pos[c][0], pos[c][1] - bh / 2)], T['border'], 3)
    ql, qr = inner.get('i'), inner.get('j')
    for p, a, b, d in sk:
        X, Y = pos[p]
        v = f[p] if p < len(f) else 0
        ov = bf[p] if p < len(bf) else 0
        outline, width = T['border'], 2
        if v != ov:
            outline, width = T['yellow'], 4
        if cur == (a, b):
            outline, width = T['blue'], 4
        cv.rect((X - bw / 2, Y - bh / 2, X + bw / 2, Y + bh / 2), fill=T['panel2'], outline=outline, width=width, r=10)
        cv.text((X, Y - bh / 2 + 4), f'[{a},{b}]' if a < b else f'[{a}]', 17, T['muted'], anchor='mt', mono=True)
        cv.text((X, Y + 12), v, 28, T['green'] if v else T['dim'], anchor='mm', bold=True)
    length = S.get('length')
    if length:
        cv.text((x0 + 18, y1 - 10), '叶子对应 length = ' + str(length) + '（第 k 项 = 区间 k 与区间 k-1 的长度和）', 19, T['dim'], anchor='lb')


def _best_text(S, B):
    if 'best' not in S or 'left' not in S or S['_line'] <= L_BEST:
        return ''
    return f"本次查询 `[{S['left']}, {S['right']}]`：答案 = `one` ({S['one']}) + `best` ({S['best']})"


CONFIG = dict(
    num=3501, title='操作后最大活跃区段数 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='0 区间 + 二分定位 + 线段树',
    tags=['灵神题单·常用数据结构', '难度分 2941'],
    code=_CODE,
    call=f'Solution().maxActiveSectionsAfterTrade({S0!r}, {QUERIES!r})',
    expect=EXPECT,
    views=[
        dict(type='custom', draw=_draw_s, h=250),
        dict(type='custom', draw=_draw_tree, h=300),
        dict(type='text', fn=_best_text, h=50),
    ],
    watch=['one', 'p', 'q', 'best', ('res', 'res', 'green')],
    skip=['n = len(s)', 'intervals = []', 'p = 0', 'while p < n:', "s[p] == '1'", 'p += 1', 'if p == n', 'break',
          'q = p + 1', 'while q < n and s[q] == \'0\'', 'q += 1', 'p = q', 'for index in range(1', 'lo = 0',
          'while lo < hi', 'mid = (lo + hi', 'if start == end', 'mid = (start + end)', 'return', 'if not intervals',
          'n = len(intervals)', 'if res >= mod', 'res = []', 'hi = mid', 'lo = mid', 'one = n', 'left > intervals[-1][-1] or', 'length.append', 'f[p] = length[start]', 'build(p * 2 + 1, start, mid)', 'build(p * 2 + 2, mid + 1, end)'],
    max_steps=62,
    captions={
        'one = n': '`one`：先假设全是 1，扫描时把每段 0 扣掉，最后剩下的就是原有 1 的个数',
        'intervals.append((p, q - 1))': '找到一段连续 0：闭区间 `[{p}, {q - 1}]`，记为 `intervals[{len(intervals) - 1}]`',
        'one -= q - p': '这段 0 长 `{q - p}`，从 `one`（先假设全是 1）里扣掉 → =={one}==',
        'length = [0]': '`length[k]`：区间 k 与区间 k-1 的长度之和（相邻两段 0）；第 0 项没有前一段，记 0；接着算出整个 `length`',
        'length.append': '`length[{len(length) - 1}]` = 两段长度之和 = =={length[-1]}==',
        'f = [0] * (n * 4)': '线段树数组 `f`，用来查 `length` 的区间最大值',
        'build(0, 0, n - 1)': '建树：根节点管 `[0, {n - 1}]`',
        'build(p * 2 + 1, start, mid)': '先建左半',
        'build(p * 2 + 2, mid + 1, end)': '再建右半',
        'f[p] = length[start]': '叶子 `[{start}]`：`f[{p}] = length[{start}]` = =={length[start]}==',
        'f[p] = max(f[p * 2 + 1]': '内部节点 `[{start}, {end}]`：取左右子节点的最大值 = =={f[p]}==',
        'left > intervals[-1][-1] or': '查询区间里有 0 区间吗？没有的话答案就是 `one`',
        L_LO1 + 1: '二分找 `p`：最左的、右端点 `>= left` 的区间，搜索范围 `[0, {hi}]`',
        L_LO2 + 1: '二分找 `q`：最右的、左端点 `<= right` 的区间，搜索范围 `[0, {hi}]`',
        'if intervals[mid][1] >= left': '`mid = {mid}`：右端点 `{intervals[mid][1]}` {">=" if intervals[mid][1] >= left else "<"} `left = {left}` → =={"够大 → hi = mid，往左收缩" if intervals[mid][1] >= left else "太靠左 → lo = mid + 1，丢掉左边"}==',
        'hi = mid': '`hi = {hi}`：往左收缩（mid 本身可能就是答案）',
        'lo = mid + 1': '`lo = {lo}`：mid 太靠左，整段丢掉',
        'p = lo': '`p = {p}`：第一个与查询区间有交的 0 区间 `{intervals[p]}`',
        'if intervals[mid][0] <= right': '`mid = {mid}`：左端点 `{intervals[mid][0]}` {"<=" if intervals[mid][0] <= right else ">"} `right = {right}` → =={"够靠左 → lo = mid，往右收缩" if intervals[mid][0] <= right else "太靠右 → hi = mid - 1，丢掉右边"}==',
        'lo = mid': '`lo = {lo}`：往右收缩（取右中位，避免死循环）',
        'hi = mid - 1': '`hi = {hi}`：mid 太靠右，丢掉',
        'q = hi': '`q = {q}`：最后一个与查询区间有交的 0 区间 `{intervals[q]}`',
        'best = 0': '`best`：这次查询里「相邻两段 0 被截断后」的最大长度和，先设 0',
        'if p + 2 <= q - 1': '中间完整的区间 `[{p + 2}, {q - 1}]`：{"有，查线段树" if p + 2 <= q - 1 else "没有，跳过"}',
        'best = find(0, 0, n - 1': '线段树查 `[{p + 2}, {q - 1}]` 里 `length` 的最大值：从根往下，只走相关的节点',
        'if start == i and end == j': '节点 `[{start}, {end}]` 对查询 `[{i}, {j}]`：{"完全一致，直接用 f[p]" if start == i and end == j else "还没对上，继续往下"}',
        'if j <= mid': '`j <= mid`（`{j} <= {mid}`）→ =={"整段在左半" if j <= mid else "不全在左半"}==',
        'elif i >= mid + 1': '`i >= mid + 1`（`{i} >= {mid + 1}`）→ =={"整段在右半" if i >= mid + 1 else "跨过 mid"}==',
        'return find(p * 2 + 1, start, mid, i, j)': '只查左儿子 `[{start}, {mid}]`',
        'return find(p * 2 + 2, mid + 1, start': '只查右儿子',
        'if q > p': '{"线段树给出 `best` = =="+str(best)+"==。" if p + 2 <= q - 1 else ""}`q > p`（`{q} > {p}`）：至少跨两个区间，才有两端截断的候选',
        'best = max(best, min(intervals[p + 1]': '候选一：区间 `p+1`（截到 right）+ 区间 `p`（从 left 截起）→ `best` = =={best}==',
        'best = max(best, intervals[q - 1]': '候选二：区间 `q-1`（从 left 截起）+ 区间 `q`（截到 right）→ `best` = =={best}==',
        'res.append(one + best)': '答案 = `one + best` = {one} + {best} = =={one + best}==',
    },
    cards=dict(
        one_liner='先拆出所有 0 段，再在查询区间里找「相邻两段 0 的最大长度和」',
        complexity='时间 `O((n + q) log n)`，空间 `O(n)`',
        problem=['二进制串 `s`，一次操作：把被 0 包围的一段 1 变成 0，再把被 1 包围的一段 0 变成 1',
                 '每个查询 `[l, r]` 只看子串（两端补 1），查询互相独立',
                 '返回每个查询操作后最多的 1 的个数'],
        quote='本题从单次查询变成了多次查询，但是整体思路类似，依然是先分离连续的0和1，记录所有0的区间intervals。接下来对于每次查询，想办法找出查询区间内相邻0区间的最大长度之和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`one` 先记下原有的 1 的个数；0 段存成 `intervals`',
              '每次查询用二分找最左的 `p`（右端点 ≥ left）和最右的 `q`（左端点 ≤ right）',
              '中间完整区间的相邻和不变，用线段树查最大值；两端被截断的区间单独算'],
        summary=['时间 `O((n + q) log n)`，空间 `O(n)`',
                 '`p` 找最左右端点 `>= left`，`q` 找最右左端点 `<= right`，两次二分的取中位方式不同',
                 '两端的区间要用 `max(.., left)`、`min(.., right)` 截断后再算长度',
                 '没有任何 0 区间在查询内时，直接答案 `one`；`p+2 <= q-1` 才需要查线段树',
                 '原文本身可直接在 Python 3 运行（整数除法已是 `//`），代码未改动',
                 '对比灵神：灵神用 ST 表 + 哨兵，yiduobo 用线段树 + 手写二分'],
    ),
)
