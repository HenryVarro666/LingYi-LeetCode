def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    si = S.get('sorted_intervals')
    if si is None:
        raw = S.get('intervals') or []
        si = [(i, tuple(v)) for i, v in enumerate(raw)]
    n = len(si)
    cur = S.get('index') if 'weight' in S else None
    lo = S.get('lo') if cur is not None and line >= 12 else None
    done_lo = lo is not None and line >= 16
    cv.text((x0 + 18, y0 + 2), '区间（按终点排序；黄 = 当前 index，蓝 = 二分得到的前 lo 个，可接在它前面）', 22, T['muted'], bold=True)
    allv = [v for _, t in si for v in (t[0], t[1])]
    lo_v, hi_v = min(allv), max(allv)
    L, R = x0 + 190, x1 - 50

    def X(v):
        return L + (v - lo_v) / max(1, hi_v - lo_v) * (R - L)
    y = y0 + 40
    for t, (orig, (l, r, w)) in enumerate(si):
        col, tc = T['panel2'], T['text']
        if cur is not None and t == cur:
            col, tc = T['yellow'], T['bg']
        elif done_lo and t < lo:
            col, tc = T['blue'], T['bg']
        cv.rect((X(l), y, max(X(r), X(l) + 10), y + 28), fill=col, r=8, outline=T['border'])
        cv.text(((X(l) + max(X(r), X(l) + 10)) / 2, y + 14), f'w={w}', 18, tc, anchor='mm', bold=True)
        cv.text((X(l) - 8, y + 14), f'[{l},{r}] #{orig}', 17, T['muted'], anchor='rm', mono=True)
        y += 34
    y += 18
    cv.text((x0 + 18, y), 'f[p][t]：前 t 个区间选 p+1 个的 最大和 · 下标列表（黄 = 刚算出，粉 = f[p-1][lo]）', 20, T['muted'], bold=True)
    y += 34
    f = S.get('f')
    if not f:
        return
    cw = (x1 - x0 - 150) / (n + 1)
    rh = min(54, (y1 - y - 40) / (len(f) + 0.2))
    for t in range(n + 1):
        cv.text((x0 + 110 + (t + 0.5) * cw, y), f't={t}', 20, T['dim'], anchor='mt', mono=True)
    y += 28
    pp = S.get('p')
    for p_, row in enumerate(f):
        Y = y + p_ * rh
        cv.text((x0 + 90, Y + rh / 2), f'p={p_}', 20, T['dim'], anchor='rm', mono=True)
        for t in range(n + 1):
            cx0 = x0 + 110 + t * cw
            if t >= len(row):
                cv.rect((cx0 + 4, Y + 3, cx0 + cw - 4, Y + rh - 3), outline=T['border'], r=8)
                continue
            s_, ids = row[t]
            fill, tc = T['panel2'], T['text']
            if cur is not None and pp is not None and line >= 20:
                if p_ == pp and t == cur + 1 and line >= 20 and len(row) == cur + 2:
                    fill, tc = T['yellow'], T['bg']
            if cur is not None and pp is not None and p_ == pp - 1 and t == lo and line == 23:
                fill, tc = T['pink'], T['bg']
            cv.rect((cx0 + 4, Y + 3, cx0 + cw - 4, Y + rh - 3), fill=fill, outline=T['border'], r=8)
            cv.text((cx0 + cw / 2, Y + rh / 2), f'{-s_}·{ids}', 17, tc, anchor='mm', mono=True, bold=True)


def _cap_app(S, B, ret):
    p = S.p
    ch = S.choose
    keep = S.f[p][-2]
    new = S.f[p][-1]
    ks, cs = -keep[0], -ch[0]
    if ks > cs:
        why = f'不选更大（{ks} > {cs}）'
    elif ks < cs:
        why = f'选它更大（{cs} > {ks}）'
    else:
        why = f'和相同（{ks}），字典序更小的 {new[1]} 胜'
    src = '只选当前区间' if p == 0 else f'接在 `f[{p - 1}][{S.lo}]` 后面'
    return f'`p = {p}`：{src}得 `{cs}·{ch[1]}`；放弃则是 `{ks}·{keep[1]}`。{why} → `f[{p}][{S.index + 1}]` = =={-new[0]}·{new[1]}=='


CONFIG = dict(
    num=3414, title='不重叠区间的最大得分', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按终点排序 · 手写二分 · 二元组 (收益, 字典序) 取 min',
    tags=['灵神题单', '动态规划', '难度分 2723'],
    code='''
class Solution(object):
    def maximumWeight(self, intervals):
        
        f = [[[0, []]] for _ in range(4)]
        sorted_intervals = sorted(enumerate(intervals), key=lambda d:d[1][1])

        for index, (original_index, (left, right, weight)) in enumerate(sorted_intervals):
            hi = index
            lo = 0
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if sorted_intervals[mid - 1][1][1] < left:
                    lo = mid
                else:
                    hi = mid - 1

            for p in range(4):
                if p == 0:
                    choose = [-weight, [original_index]]
                else:
                    choose = [f[p - 1][lo][0] - weight, sorted(f[p - 1][lo][1] + [original_index])]

                f[p].append(min(f[p][-1], choose))

        return f[-1][-1][1]
''',
    call='Solution().maximumWeight([[1,3,2],[4,5,3],[1,5,5],[6,9,3]])',
    expect=[0, 1, 3],
    skip=['hi = index', 'lo = 0', 'for p in range', 'if p == 0', 'choose = [', 'f = [[[0, []]]'],
    max_steps=80,
    views=[
        dict(type='custom', h=640, draw=_draw),
        dict(type='text', h=50, size=24, fn=lambda S: (
            f"区间 `[{S['left']},{S['right']}]` 权重 `{S['weight']}`（原下标 {S['original_index']}）：前面可接 `lo = {S['lo']}` 个区间" if 'lo' in S and 'weight' in S
            else '`f[p][t] = min(f[p][t-1], (f[p-1][lo] 的收益取负 − w, 下标排序))`')),
    ],
    watch=[('index', 'index', 'yellow'), ('lo', 'lo', 'blue'), ('hi', 'hi', 'orange'), ('p', 'p', 'pink')],
    captions={
        'f = [[[0, []]]': '`f[p][t]`：前 `t` 个区间选 `p+1` 个的（收益取负，下标列表）；每行先放一个空状态 `[0, []]`',
        'sorted_intervals = ': '`enumerate` 带上原下标，再按终点（`d[1][1]`）排序',
        'for index, (original': lambda S, B, r: (f'第 `index = {S.index}` 个区间 `[{S.left}, {S.right}]`，权重 {S.weight}：选它还是放弃' if S.get('index') != B.get('index') else '区间全部处理完'),
        'while lo < hi': lambda S, B, r: (f'二分找 `t`：`lo = {S.lo}`，`hi = {S.hi}`，还没收拢' if S.lo < S.hi else f'二分结束：终点 `< {S.left}` 的区间有 `lo = {S.lo}` 个，它们都能放在当前区间前面'),
        'mid = (': '取 `mid = {mid}`（向上取整，避免死循环）',
        'if sorted_intervals[mid - 1]': lambda S, B, r: (f'第 `mid-1 = {S.mid - 1}` 个区间终点 `{S.sorted_intervals[S.mid - 1][1][1]}` ' + ('`<` ' if S.sorted_intervals[S.mid - 1][1][1] < S.left else '`≥` ') + f'`left = {S.left}`：' + ('==不重叠==，前 `mid` 个都可用' if S.sorted_intervals[S.mid - 1][1][1] < S.left else '重叠，答案更小')),
        'lo = mid': '`lo` 上移到 `{lo}`',
        'hi = mid - 1': '`hi` 下移到 `{hi}`',
        'f[p].append': _cap_app,
        'return f[-1][-1][1]': '`f[3][n]`：最多选 4 个的最优方案 = =={ret}==',
    },
    cards=dict(
        one_liner='f 里存 (收益, 下标) 二元组，一个 min 同时管大小与字典序',
        complexity='时间 `O(n log n)`（`p` 固定 4 层），空间 `O(n)`',
        problem=['给若干区间 `[l, r, weight]`，最多选 4 个==互不重叠==（共端点也算）的区间',
                 '返回得分最大且字典序最小的下标数组',
                 '示例：`[[1,3,2],[4,5,3],[1,5,5],[6,9,3]]` → `[0,1,3]`（和同为 8，下标更小）'],
        quote='对于字典序最小的方案这个要求，则可以将f保留的值从最大的收益，改为最大的收益与最小的字典序形成的二元组，在状态转移时先判断收益的大小，若收益相同再判断字典序就行了。',
        quote_src='—— yiduobo 题解',
        idea=['无个数限制时是经典 DP：按终点排序，`f[index] = max(f[index-1], f[t] + w)`，`t` 用二分找',
              '限制 4 个：加一维 `p`，`f[p][index]` 表示前 `index` 个区间选 `p+1` 个',
              '`p = 0` 只能选当前区间；`p > 0` 从 `f[p-1][lo]` 转移，收益取负后一个 `min` 搞定'],
        summary=['时间 `O(n log n)`，空间 `O(n)`：4 行 × `n+1` 列',
                 '易错：二分里 `mid - 1` 是第 `mid` 个区间；终点要==严格小于== `left`',
                 '收益存成负数，`min` 才是最大收益；相同再比下标列表',
                 '二分取 `mid = (lo + hi + 1) // 2` 向上取整，配合 `hi = mid - 1`，否则可能死循环',
                 '原文就是 Python 3 写法（`//` 已是整除），未改动'],
    ),
)
