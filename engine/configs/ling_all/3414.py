def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    a = S.get('a')
    if a is None:
        raw = S.get('intervals') or []
        a = [(r, l, w, i) for i, (l, r, w) in enumerate(raw)]
    n = len(a)
    cur = S.get('i') if 'idx' in S else None
    k = S.get('k') if line >= 8 and 'idx' in S else None
    srt = 'a' in S and line >= 5
    cv.text((x0 + 18, y0 + 2), '区间（' + ('已按右端点排序；黄 = 当前 i，蓝 = 下标 < k 的区间（右端点 < l））' if srt else '原始顺序') + '', 22, T['muted'], bold=True)
    lo = min(t[1] for t in a)
    hi = max(t[0] for t in a)
    L, R = x0 + 190, x1 - 50
    def X(v):
        return L + (v - lo) / max(1, hi - lo) * (R - L)
    y = y0 + 40
    for t, (r, l, w, idx) in enumerate(a):
        col = T['panel2']
        txt = T['text']
        if cur is not None and t == cur:
            col, txt = T['yellow'], T['bg']
        elif k is not None and t < k:
            col, txt = T['blue'], T['bg']
        cv.rect((X(l), y, max(X(r), X(l) + 10), y + 28), fill=col, r=8, outline=T['border'])
        cv.text(((X(l) + max(X(r), X(l) + 10)) / 2, y + 14), f'w={w}', 18, txt, anchor='mm', bold=True)
        cv.text((X(l) - 8, y + 14), f'[{l},{r}] #{idx}', 17, T['muted'], anchor='rm', mono=True)
        y += 34
    y += 18
    cv.text((x0 + 18, y), 'f[i][j] = 最大和 · 下标列表（黄 = 正在写，粉 = f[k][j-1]，白框 = f[i][j]）', 20, T['muted'], bold=True)
    y += 34
    f = S.get('f')
    if not f:
        return
    cw = (x1 - x0 - 150) / 4
    rh = min(54, (y1 - y - 40) / (len(f) + 0.2))
    for j in range(1, 5):
        cv.text((x0 + 110 + (j - 0.5) * cw, y), f'j={j}', 20, T['dim'], anchor='mt', mono=True)
    y += 28
    jj = S.get('j')
    for r_, row in enumerate(f):
        Y = y + r_ * rh
        cv.text((x0 + 90, Y + rh / 2), f'i={r_}', 20, T['dim'], anchor='rm', mono=True)
        for j in range(1, 5):
            s_, ids = row[j]
            fill = T['panel2']
            outline = T['border']
            tc = T['text']
            if cur is not None and jj is not None and line >= 10:
                if r_ == cur + 1 and j == jj and line == 12:
                    fill, tc = T['yellow'], T['bg']
                elif r_ == S.get('k') and j == jj - 1:
                    fill, tc = T['pink'], T['bg']
                elif r_ == cur and j == jj:
                    outline = T['text']
            cx0 = x0 + 110 + (j - 1) * cw
            cv.rect((cx0 + 4, Y + 3, cx0 + cw - 4, Y + rh - 3), fill=fill, outline=outline, width=2 if outline == T['text'] else 1, r=8)
            cv.text((cx0 + cw / 2, Y + rh / 2), f'{-s_} · {ids}', 22, tc, anchor='mm', mono=True, bold=True)


def _cap_f(S, B, ret):
    s2, w = S.s2, S.weight
    keep, take = S.f[S.i][S.j], S.f[S.i + 1][S.j]
    cand = (s2 - w, sorted(S.id2 + [S.idx]))
    ks, ts = -keep[0], -cand[0]
    if ks > ts:
        why = f'不选更大（{ks} > {ts}）'
    elif ks < ts:
        why = f'选它更大（{ts} > {ks}）'
    else:
        why = f'和相同（{ks}），比下标列表：{keep[1]} 与 {cand[1]}，字典序小的胜'
    return f'不选 `{ks}·{keep[1]}`，选 `{ts}·{cand[1]}`：{why} → `f[{S.i + 1}][{S.j}]` = =={-take[0]}·{take[1]}=='


CONFIG = dict(
    num=3414, title='不重叠区间的最大得分', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='按右端点排序 · 二分 · 线性 DP（min 同时比和与字典序）',
    tags=['灵神题单', '动态规划', '难度分 2723'],
    code='''
class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        a = [(r, l, weight, i) for i, (l, r, weight) in enumerate(intervals)]
        a.sort(key=lambda t: t[0])  # 按照右端点排序
        f = [[(0, []) for _ in range(5)] for _ in range(len(intervals) + 1)]
        for i, (r, l, weight, idx) in enumerate(a):
            k = bisect_left(a, (l,), hi=i)  # hi=i 表示二分上界为 i（默认为 n）
            for j in range(1, 5):
                # 为什么是 f[k] 不是 f[k+1]：上面算的是 >= l，-1 后得到 < l，但由于还要 +1，抵消了
                s2, id2 = f[k][j - 1]
                # 注意这里是减去 weight，这样取 min 后相当于计算的是最大和
                f[i + 1][j] = min(f[i][j], (s2 - weight, sorted(id2 + [idx])))
        return f[-1][4][1]
''',
    call='Solution().maximumWeight([[1,3,2],[4,5,3],[1,5,5],[6,9,3]])',
    expect=[0, 1, 3],
    skip=['for j in range', 'f = [[(0, [])'],
    max_steps=70,
    views=[
        dict(type='custom', h=640, draw=_draw),
        dict(type='text', h=50, size=24, fn=lambda S: (
            f"当前区间 `[{S['l']},{S['r']}]` 权重 `{S['weight']}`（下标 {S['idx']}），二分得 `k = {S['k']}`（前面有 {S['k']} 个区间可接）" if 'k' in S and 'idx' in S
            else '`f[i+1][j] = min(f[i][j], (f[k][j-1] 的和取负 − weight, 下标排序后))`')),
    ],
    watch=[('i', 'i', 'yellow'), ('k', 'k', 'blue'), ('j', 'j', 'pink'), ('s2', 's2', 'cyan')],
    captions={
        'a = [(r, l': '把每个区间改成 `(右端点, 左端点, 权重, 原下标)`，方便按右端点排序、保留原下标',
        'a.sort': '按右端点排序：之后“前 i 个区间”里，任意区间都不会越过第 i 个的右端点',
        'for i, (r, l': lambda S, B, r: (f'第 `i = {S.i}` 个区间 `[{S.l}, {S.r}]`，权重 {S.weight}：选还是不选' if S.get('i') != B.get('i') else '全部区间处理完毕'),
        'k = bisect_left': lambda S, B, r: f'二分：右端点 `< {S.l}` 的区间有 `k = {S.k}` 个' + ('，下标 `0..%d` 都能放前面' % (S.k - 1) if S.k else '，前面放不了任何区间') + '；转移用 `f[k]`（bisect 少算 1，正好抵消 +1）',
        's2, id2 = f[k]': '选它：接在 `f[{k}][{j - 1}]` = `{-s2}·{id2}` 后面',
        'f[i + 1][j] = min': _cap_f,
        'return f[-1][4][1]': '答案是 `f[n][4]` 的下标列表 = =={ret}==',
    },
    cards=dict(
        one_liner='1235 的 DP 多加一维 j，min 里同时比较和与字典序',
        complexity='时间 `O(n(log n + k²))`，空间 `O(nk²)`，`k = 4`',
        problem=['给若干区间 `[l, r, weight]`，最多选 4 个==互不重叠==（共端点也算重叠）的区间',
                 '返回得分最大、且==字典序最小==的下标数组',
                 '示例：`[[1,3,2],[4,5,3],[1,5,5],[6,9,3]]` → `[0,1,3]`（和相同，下标更小）'],
        quote='定义 f[i+1][j] 表示在下标 [0,i] 中选至多 j 个不重叠区间的最大总和。……本题需要额外维护所选区间的字典序最小下标序列。我们可以在 f 中额外维护下标数组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先按右端点排序，`f[i+1][j]` = 前 `i+1` 个区间里至多选 `j` 个',
              '第 `i` 个区间：不选 `f[i][j]`；选则接在 `f[k][j-1]` 后，`k` 由二分得出',
              '把和==取负==，用元组 `(−和, 下标列表)` 取 `min`：和大的优先，相同则字典序小的优先'],
        summary=['时间 `O(n(log n + k²))`：排序 + 二分，下标列表长度 ≤ 4，排序近似 `O(k)`',
                 '易错：`bisect_left(a, (l,), hi=i)` 找的是右端点 `< l`；严格小于才不重叠',
                 '易错：存的是 `s2 - weight`（负数），所以 `min` 才是最大和',
                 '基础题是 1235 规划兼职工作；相似题见 DP 题单 §6.4 / §7.5'],
    ),
)
