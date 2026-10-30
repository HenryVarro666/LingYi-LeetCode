_CODE = '''
class Solution(object):
    def separateSquares(self, squares):

        x_set = set()
        for x, y, l in squares:
            x_set.add(x)
            x_set.add(x + l)
        
        x_mapping = {}
        re_x_mapping = sorted(list(x_set))
        for index, x in enumerate(re_x_mapping):
            x_mapping[x] = index
        
        m = len(x_mapping)
        
        lines = []
        for x, y, l in squares:
            lines.append((y, x_mapping[x], x_mapping[x + l], 1))
            lines.append((y + l, x_mapping[x], x_mapping[x + l], -1))

        def get(p, left, right):
            if g[p] is None:
                if f[p] > 0:
                    g[p] = re_x_mapping[right + 1] - re_x_mapping[left]
                elif left == right:
                    g[p] = 0
                else:
                    mid = (left + right) >> 1
                    g[p] = get(p * 2 + 1, left, mid) + get(p * 2 + 2, mid + 1, right)
            return g[p]

        def put(p, left, right, i, j, delta):
            g[p] = None
            if left == i and right == j:
                f[p] += delta
            else:
                mid = (left + right) >> 1
                if j <= mid:
                    put(p * 2 + 1, left, mid, i, j, delta)
                elif i > mid:
                    put(p * 2 + 2, mid + 1, right, i, j, delta)
                else:
                    put(p * 2 + 1, left, mid, i, mid, delta)
                    put(p * 2 + 2, mid + 1, right, mid + 1, j, delta)

        lines.sort()
        pre_y = lines[0][0]
        f = [0] * (m * 4)
        g = [None] * (m * 4)
        s = 0
        area_list = []
        for y, start_x, end_x, delta in lines:
            if pre_y != y:
                tot_l = get(0, 0, m - 1)
                s += (y - pre_y) * tot_l
                area_list.append((s, tot_l, pre_y, y))

            put(0, 0, m - 1, start_x, end_x - 1, delta)
            pre_y = y

        for below, tot_l, pre_y, y in area_list:
            if below * 2 >= s:
                pre_below = below - (y - pre_y) * tot_l
                return pre_y + (s / 2.0 - pre_below) / tot_l
'''
_CL = {ln.strip(): i for i, ln in enumerate(_CODE.strip('\n').split('\n'), 1)}
_PUT_CALL = _CL['put(0, 0, m - 1, start_x, end_x - 1, delta)']
_LOOP = _CL['for y, start_x, end_x, delta in lines:']


def _tree(S):
    f, g = S.get('f'), S.get('g')
    return f, g


def _cur_idx(S):
    lines = S.get('lines')
    if not lines or 'delta' not in S or 'start_x' not in S or 'f' not in S:
        return None
    try:
        return lines.index((S['y'], S['start_x'], S['end_x'], S['delta']))
    except ValueError:
        return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    sq, xs, lines = S.get('squares'), S.get('re_x_mapping'), S.get('lines')
    if not sq or not xs or not lines or 'f' not in S:
        return
    ln = S.get('_line', 0)
    phase2 = 'below' in S
    cur = _cur_idx(S)
    cv.text((x0 + 18, y0 + 4), '扫描线 · 绿 = 已扫面积', 24, T['muted'], bold=True)
    X0, X1 = min(xs), max(xs)
    ys = sorted({e[0] for e in lines})
    Y0, Y1 = ys[0], ys[-1]
    sc = min(300 / (X1 - X0), 300 / (Y1 - Y0))
    ox, oy = x0 + 60, y1 - 60
    px = lambda x: ox + (x - X0) * sc
    py = lambda y: oy - (y - Y0) * sc
    if phase2:
        ycur = Y1
    elif cur is not None:
        ycur = lines[cur][0]
    else:
        ycur = Y0
    for k in range(len(xs) - 1):
        a, b = xs[k], xs[k + 1]
        segs = sorted((max(y, Y0), min(y + l, ycur)) for (x, y, l) in sq if x <= a and b <= x + l and y < ycur)
        lo_, hi_ = None, None
        for lo, hi in segs:
            if hi <= lo:
                continue
            if hi_ is None or lo > hi_:
                if hi_ is not None:
                    cv.rect((px(a), py(hi_), px(b), py(lo_)), fill=T['green'], alpha=120)
                lo_, hi_ = lo, hi
            else:
                hi_ = max(hi_, hi)
        if hi_ is not None:
            cv.rect((px(a), py(hi_), px(b), py(lo_)), fill=T['green'], alpha=120)
    cols = ['blue', 'pink', 'purple', 'cyan', 'orange']
    for i, (x, y, l) in enumerate(sq):
        cv.rect((px(x), py(y + l), px(x + l), py(y)), outline=T[cols[i % 5]], width=4)
    for x in xs:
        cv.text((px(x), oy + 10), x, 20, T['dim'], anchor='mt', mono=True)
    for y in ys:
        cv.text((ox - 12, py(y)), y, 20, T['dim'], anchor='rm', mono=True)
    cv.line([(ox, oy), (px(X1) + 10, oy)], T['border'], 2)
    if phase2:
        if 'pre_y' in S and 'y' in S:
            cv.rect((px(X0) - 4, py(S['y']), px(X1) + 4, py(S['pre_y'])), outline=T['yellow'], width=3)
        if 'pre_below' in S:
            ya = S['pre_y'] + (S['s'] / 2.0 - S['pre_below']) / S['tot_l']
            cv.line([(ox - 6, py(ya)), (px(X1) + 24, py(ya))], T['red'], 4)
            cv.text((px(X1) + 30, py(ya)), f'答案 y={ya:g}', 22, T['red'], anchor='lm', bold=True)
    else:
        cv.line([(ox - 6, py(ycur)), (px(X1) + 24, py(ycur))], T['yellow'], 4)
        cv.text((px(X1) + 30, py(ycur)), f'y={ycur}', 22, T['yellow'], anchor='lm', bold=True)
    # 线段树（堆式下标：左 2p+1，右 2p+2）
    f, g, m = S.get('f'), S.get('g'), S.get('m')
    if f is None or g is None or not m:
        return
    tx0 = x0 + 400
    cv.text((tx0, y0 + 4), '线段树：f 覆盖次数 / g 宽度（? = 待重算）', 22, T['muted'], bold=True)
    Bf, Bg = B.get('f'), B.get('g')
    pos = {}

    def lay(p, l, r, d, lo, hi):
        pos[p] = ((lo + hi) / 2, y0 + 90 + d * 120, l, r, hi - lo)
        if l == r:
            return
        mid_ = (l + r) >> 1
        c = (lo + hi) / 2
        lay(p * 2 + 1, l, mid_, d + 1, lo, c)
        lay(p * 2 + 2, mid_ + 1, r, d + 1, c, hi)

    lay(0, 0, m - 1, 0, tx0, x1 - 10)
    for p, (cx, cy, l, r, ww) in pos.items():
        for c in (p * 2 + 1, p * 2 + 2):
            if c in pos:
                cv.line([(cx, cy + 34), (pos[c][0], pos[c][1] - 34)], T['border'], 2)
    for p, (cx, cy, l, r, ww) in pos.items():
        ch = Bf is not None and p < len(Bf) and (Bf[p], Bg[p]) != (f[p], g[p])
        w = min(150, ww * 0.92)
        cv.rect((cx - w / 2, cy - 34, cx + w / 2, cy + 34), fill=(30, 36, 46),
                outline=T['yellow'] if ch else T['border'], width=4 if ch else 2, r=8)
        lab = '(哨兵)' if l >= len(xs) - 1 else f'[{xs[l]},{xs[min(r + 1, len(xs) - 1)]})'
        cv.text((cx, cy - 26), lab, 18, T['dim'], anchor='mt', mono=True)
        gv = '?' if g[p] is None else g[p]
        cv.text((cx, cy + 2), f'{f[p]} / {gv}', 24, T['text'], anchor='mt', bold=True, mono=True)


def _text(S):
    if 'below' in S:
        s = S['s']
        r = f"总面积 `s` = {s}，一半 = {s / 2.0}；第 `{S['y']}` 段结束时下方面积 `below` = =={S['below']}=="
        return r
    if 'tot_l' in S and 's' in S and 'pre_y' in S:
        return f"`s` = ==`{S['s']}`==（并集面积），这一段宽 `tot_l` = {S['tot_l']}，扫描线 `pre_y` = {S['pre_y']}"
    return '把 x 离散化成下标，用线段树统计「覆盖宽度」，扫描线从下往上'


CONFIG = dict(
    num=3454, title='分割正方形 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='扫描线 + 线段树（覆盖计数） + 离散化',
    tags=['灵神题单', '常用数据结构', '难度分 2671'],
    code=_CODE,
    call='Solution().separateSquares([[0, 0, 2], [1, 1, 1]])',
    expect=1.0,
    views=[
        dict(type='text', fn=_text, size=24, h=80),
        dict(type='custom', draw=_draw, h=470),
        dict(type='array', var='re_x_mapping', label='re_x_mapping（离散化后的 x）', h=110, cell=70),
    ],
    watch=['pre_y', 's', ('tot_l', 'tot_l', 'cyan'), 'area_list'],
    skip=['if j <= mid:', 'elif i > mid:', 'for x, y, l in squares:', 'for index, x in enumerate', 'def get', 'def put', 'x_set.add', 'x_set = set()', 'x_mapping = {}', 'x_mapping[x] = index', 'lines = []', 'area_list = []',
          'mid = (left + right) >> 1', 'g[p] = None', 'return g[p]', 'f = [0]', 'g = [None]', 's = 0', 'm = len(x_mapping)'],
    max_steps=56,
    captions={
        're_x_mapping = sorted': '所有出现过的 x 和 x+l 排序：`{re_x_mapping}`，下标就是线段树里用的坐标',
        'lines.append((y, x_mapping[x], x_mapping[x + l], 1))': '下边：`y = {y}`，覆盖离散化区间 `[{x_mapping[x]}, {x_mapping[x + l]})`，`+1`',
        'lines.append((y + l': '上边：`y = {y + l}`，失效，`-1`',
        'lines.sort()': '事件按 y 从小到大排序，扫描线只停在这些位置',
        'pre_y = lines[0][0]': '`pre_y` 记录上一次扫描线停的位置，从最低的边开始 = {pre_y}',
        'if pre_y != y': lambda S, B, r: (f'`pre_y = {S.pre_y}` ≠ `y = {S.y}`：扫描线移动了一段，先结算这段面积' if S.pre_y != S.y
                                            else f'`pre_y = y = {S.y}`：同一高度的事件，不用结算面积'),
        'tot_l = get(': '`get` 取当前被覆盖的总宽度 `tot_l` = =={tot_l}==（g 是缓存，`f>0` 时整段都算）',
        's += (y - pre_y) * tot_l': '这一段面积 = `{y - pre_y} × {tot_l}`，累计并集面积 `s` → =={s}==',
        'area_list.append': '记录：到 `y = {y}` 为止下方面积 `{s}`、这一段宽 `{tot_l}`、区间 `[{pre_y}, {y}]`；总面积要等扫完才知道',
        'put(0, 0, m - 1, start_x, end_x - 1, delta)': '把下标区间 `[{start_x}, {end_x - 1}]` 的覆盖次数 `{"+1" if delta > 0 else "-1"}`',
        'f[p] += delta': '整段命中：`f[{p}]` 直接加 `{delta}`，不下推（g 在上面已清空，等下次 get 重算）',
        'pre_y = y': '扫描线停在 `y = {y}`',
        'for below, tot_l, pre_y, y in area_list': '第二趟：逐段看「下方面积」`below` 第一次 ≥ 一半是哪一段',
        'if below * 2 >= s': lambda S, B, r: (f'`below × 2 = {S.below * 2} ≥ s = {S.s}`：下方面积已过半，答案就在这一段里' if S.below * 2 >= S.s
                                              else f'`below × 2 = {S.below * 2} < s = {S.s}`：还没过半，看下一段'),
        'pre_below = below': '这一段开始前的下方面积 `pre_below` = `{below} − {y - pre_y} × {tot_l}` = =={pre_below}==',
        'return pre_y + ': lambda S, B, r: f'`y = {S.pre_y} + ({S.s}/2 − {S.pre_below}) / {S.tot_l}` = =={r}==：还差的面积 ÷ 这一段的宽，就是在这段里再升多高',
    },
    cards=dict(
        one_liner='离散化 x，线段树数「被盖住的宽度」，扫完再回头找一半',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一些可能重叠的正方形 `[x, y, l]`，重叠部分只算一次',
                 '找最小的 `y`，使水平线下方的面积 = 上方的面积',
                 '本视频：`[[0,0,2],[1,1,1]]`（题目示例 2），答案 `1.0`'],
        quote='扫描线只会停留在所有的y以及y + l这些位置……在这里可以设置一个数组arr，其中arr[index]表示当前生效的正方形是否包含了下标index……这样一来，arr中非0元素的数量就是当前生效的tot_l。',
        quote_src='—— yiduobo 题解原文',
        idea=['x 范围很大，先离散化：把出现过的 `x` 和 `x+l` 排序，用下标代替',
              '扫描线遇到下边就给区间 `+1`，遇到上边就 `-1`；覆盖次数 > 0 的宽度之和就是 `tot_l`',
              '总面积一开始不知道，所以每次移动都记下 (下方面积, 宽度, 起止 y)，扫完再找过半的那一段'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '线段树不下推：`f` 记录整段被覆盖的次数，`g` 缓存宽度，改动经过的节点把 `g` 置空',
                 '同一高度的多个事件不结算面积（`pre_y != y` 才算）',
                 '最后 `pre_y + (s/2 − pre_below) / tot_l`：在过半的这一段里按比例补足',
                 '原文已是 Python 3 可运行的写法（`s / 2.0` 本来就是浮点除法），未做改动',
                 '对比灵神：灵神用「最小覆盖次数 + 懒标记」线段树，并用二分找答案；yiduobo 用 f/g 缓存，扫完线性找'],
    ),
)
