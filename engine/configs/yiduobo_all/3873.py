PTS = [[1, 1], [1, 2], [2, 2], [3, 5], [4, 5], [6, 7]]
PAL = ['blue', 'pink', 'green', 'orange', 'purple', 'cyan']


def _rt(fa, i):
    n = 0
    while fa[i] != i and n < 50:
        i = fa[i]
        n += 1
    return i


def _cur(S):
    if S.get('_line') in (16, 17, 18, 20, 21, 22, 24, 25, 27, 28, 29, 30, 31) and 'index' in S and 'x' in S:
        return S['index']
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = S['points']
    fa = S.get('fa')
    xs = sorted({p[0] for p in pts})
    ys = sorted({p[1] for p in pts})
    R, C = len(xs), len(ys)
    cw = min(130, (x1 - x0 - 220) / max(C - 1, 1))
    chh = min(80, (y1 - y0 - 150) / max(R - 1, 1))
    rad = min(28, chh * 0.42)
    gx = x0 + (x1 - x0 - cw * (C - 1)) / 2
    gy = y0 + 100
    cv.text((x0 + 18, y0 + 4), '点（编号 = 下标；同色 = 同一连通分量，白圈 = 正在处理的点）', 22, T['muted'], bold=True)
    seen = S['_line'] >= 16
    if 'index' in S and S['_line'] < 33:
        n_done = S['index'] + (1 if S['_line'] > 30 else 0)
    else:
        n_done = len(pts) if seen else 0
    # 已处理 = 下标 < index，或当前点已经完成两次合并（第 31 行以后）
    cur = S.get('index') if 'index' in S and S['_line'] < 33 else None
    done = set(range(len(pts))) if (cur is None and seen) else set(range(cur if cur is not None else 0))
    if cur is not None and S['_line'] >= 17:
        done.add(cur)
    roots = sorted({_rt(fa, i) for i in done}) if fa is not None else []
    col = {r: T[PAL[k % len(PAL)]] for k, r in enumerate(roots)}
    pos = lambda p: (gx + ys.index(p[1]) * cw, gy + xs.index(p[0]) * chh)
    for i, r in enumerate(xs):
        cv.text((gx - 60, gy + i * chh), f'x={r}', 20, T['dim'], anchor='rm', bold=True)
    for i, c in enumerate(ys):
        cv.text((gx + i * cw, gy - 40), f'y={c}', 20, T['dim'], anchor='mb', bold=True)
    dl = sorted(done)
    for a_i, a in enumerate(dl):
        for b in dl[a_i + 1:]:
            pa, pb = pts[a], pts[b]
            if pa[0] == pb[0] or pa[1] == pb[1]:
                if fa is not None and _rt(fa, a) == _rt(fa, b):
                    cv.line([pos(pa), pos(pb)], col.get(_rt(fa, a), T['muted']), 5)
    for i, p in enumerate(pts):
        X, Y = pos(p)
        ok = i in done and fa is not None
        c = col.get(_rt(fa, i)) if ok else T['panel2']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=c, outline=T['border'])
        cv.text((X, Y - 4), f'{p[0]},{p[1]}', 19, T['bg'] if ok else T['muted'], anchor='mm', bold=True)
        cv.text((X, Y + 16), f'#{i}', 14, T['bg'] if ok else T['dim'], anchor='mm', bold=True)
        if cur is not None and cur == i and S['_line'] >= 16:
            cv.d.ellipse((X - rad - 7, Y - rad - 7, X + rad + 7, Y + rad + 7), outline=T['text'], width=4)


def _xy(S):
    if 'xs' not in S:
        return ''
    f = lambda d, n: '{' + ', '.join(f'{k}→#{v}' for k, v in d.items()) + '}'
    return f'`xs` 第一个具有 x 的点：{f(S["xs"], "x")}\n`ys` 第一个具有 y 的点：{f(S["ys"], "y")}'


def _info(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    if 'first' in S and S['_line'] >= 33:
        return f'最大 `first = {S["first"]}`，次大 `second = {S["second"]}` → 加新点 1 → =={S["first"] + S["second"] + 1}=='
    roots = [i for i in range(len(fa)) if fa[i] == i]
    return '分量根与大小：' + '，'.join(f'#{r}→=={S["size"][r]}==' for r in roots)


CONFIG = dict(
    num=3873, title='添加一个点后可激活的最大点数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按点编号并查集 · 取最大两块',
    tags=['七、并查集', '§7.3 中介并查集'],
    code='''
class Solution(object):
    def maxActivated(self, points):

        n = len(points)
        fa = [index for index in range(n)]
        size = [1] * n
        parts = {}
        xs = {}
        ys = {}

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for index, (x, y) in enumerate(points):
            if x not in xs:
                xs[x] = index
            else:
                fa_s = find(fa, xs[x])
                fa[index] = fa_s
                size[fa_s] += size[index]

            if y not in ys:
                ys[y] = index
            else:
                fa_s = find(fa, ys[y])
                fa_index = find(fa, index)
                if fa_s != fa_index:
                    fa[fa_index] = fa_s
                    size[fa_s] += size[fa_index]

        first, second = 0, 0
        for index in range(n):
            if find(fa, index) != index:
                continue
            if size[index] > first:
                first, second = size[index], first
            elif size[index] > second:
                second = size[index]

        return first + second + 1
''',
    call=f'Solution().maxActivated({PTS})',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=370),
        dict(type='array', var='fa', label='fa（下标 = 点编号，值 = 父亲）', cell=80, h=170,
             pointers={'index': 'blue'}),
        dict(type='text', fn=_xy, size=26, h=110),
        dict(type='text', fn=_info, size=28, h=60),
    ],
    watch=[('index', 'index', 'blue'), ('x', 'x'), ('y', 'y'), ('first', 'first', 'green'), ('second', 'second', 'orange')],
    skip=['n = len', 'parts = {}', 'def find', 'if fa[x] != x', 'return fa[x]', 'if x not in xs', 'if y not in ys', 'else:', 'continue', 'ys = {}', 'fa[x] = find'],
    captions={
        'fa = [index': '每个点一开始自成一个连通分量：`fa[i] = i`',
        'size = [1]': '`size[i]` 记录以 `i` 为根的分量里有几个点，初始都是 1',
        'xs = {}': '`xs[x]` 记第一个具有 x 坐标的点，`ys[y]` 同理',
        'for index, (x, y)': lambda S, B, r: (f'取第 `{S.index}` 个点 `({S.x}, {S.y})`' if 'index' not in B or S.index != B.index or S.x != B.x
                                              else '所有点处理完，开始找最大、次大的分量'),
        'xs[x] = index': 'x = {x} 第一次出现：记下 `xs[{x}] = {index}`，不用合并',
        'fa_s = find(fa, xs[x])': 'x = {x} 以前出现过 → 找到 `xs[{x}]` 所在分量的根 `fa_s`',
        'fa[index] = fa_s': '新点直接挂到这个根下，并入同一分量',
        'size[fa_s] += size[index]': '根的大小加上新点的大小：`size[{fa_s}] = {size[fa_s]}`',
        'ys[y] = index': 'y = {y} 第一次出现：记下 `ys[{y}] = {index}`，不用合并',
        'fa_s = find(fa, ys[y])': 'y = {y} 以前出现过 → 先找到 `ys[{y}]` 所在分量的根 `fa_s`',
        'fa_index = find(fa, index)': '再找新点自己现在的根 `fa_index`（它可能因为 x 相同已并入某个分量）',
        'if fa_s != fa_index': lambda S, B, r: (f'两个根 `{S.fa_s}` 与 `{S.fa_index}` 不同 → 要把两个分量合并' if S.fa_s != S.fa_index
                                                else f'两个根相同（都是 `{S.fa_s}`），已在同一分量，不用合并'),
        'fa[fa_index] = fa_s': '`fa_index` 挂到 `fa_s` 下：==两个分量合并==',
        'size[fa_s] += size[fa_index]': '大小相加：`size[{fa_s}] = {size[fa_s]}`',
        'first, second = 0, 0': '`first` 记最大分量，`second` 记次大分量，初始为 0',
        'for index in range(n)': '依次看每个点：只关心作为根的点（它代表一个分量）',
        'if find(fa, index) != index': lambda S, B, r: (f'`{S.index}` 的根不是自己，不是分量的代表 → 跳过' if S.fa[S.index] != S.index else f'`{S.index}` 是根，代表一个大小为 `{S.size[S.index]}` 的分量'),
        'if size[index] > first': lambda S, B, r: (f'`size = {S.size[S.index]}` > `first = {S.first}`：成立 → 成为最大，原最大退为次大' if S.size[S.index] > S.first
                                                   else f'`size = {S.size[S.index]}` 没超过最大 `{S.first}`，再看能否当次大'),
        'first, second = size[index], first': '最大更新为 `{first}`，次大成了 `{second}`',
        'elif size[index] > second': lambda S, B, r: (f'`size = {S.size[S.index]}` > `second = {S.second}`：成立' if S.size[S.index] > S.second
                                                      else f'`size = {S.size[S.index]}` 不超过次大 `{S.second}`，忽略'),
        'second = size[index]': '次大更新为 `{second}`',
        'return first + second + 1': '新点接在最大两分量之间：`{first} + {second} + 1` = =={first + second + 1}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='点当节点、同 x 或同 y 连边：取最大两个分量 + 新点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['点被激活后，==同 x 或同 y 的点也被激活==，一直传下去',
                 '可额外加一个点，从它开始激活；求最多激活多少个点（含新点）',
                 '本视频：`[[1,1],[1,2],[2,2],[3,5],[4,5],[6,7]]` → `6`'],
        quote='为了使得激活的点数最多，只需选择点数最多的两个连通分量，新增一个点将这两个连通分量连接起来就行了，答案就是这两个连通分量的大小加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一连通分量的点要么全被激活，要么都不被激活',
              '用两个哈希表 `xs`、`ys` 记下每个坐标第一次出现的点，之后再遇到同坐标就和它合并',
              '合并时顺便用 `size` 数组记录分量大小，最后取最大和次大之和再加 1'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：只有一个分量时 `second = 0`，答案是 `first + 1`',
                 'y 方向要先找 `ys[y]` 的根、再找新点自己的根；它们可能已因 x 相同而合并',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神把行 / 列当中介节点，yiduobo 直接以点的编号做并查集，用 `xs` / `ys` 记第一个点'],
    ),
)
