def _seg(cv, box, T, lo, hi, kids, root, label, cur=None, title='', hot=()):
    """线段树绘制：按区间 [l,r] 摆放节点；label(o)->(主文本, 副文本, 填充色或None)"""
    x0, y0, x1, y1 = box
    N = hi - lo + 1
    cell = min(120, (x1 - x0 - 40) / N)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * N) / 2
    nodes, par = [], {}

    def walk(o, l, r, d, p):
        nodes.append((o, l, r, d))
        par[o] = p
        if l < r:
            m = (l + r) // 2
            a, b = kids(o)
            walk(a, l, m, d + 1, o)
            walk(b, m + 1, r, d + 1, o)
    walk(root, lo, hi, 0, None)
    D = max(n[3] for n in nodes)
    top = y0 + 44
    rowh = (y1 - top - 30) / (D + 1)
    pos = {o: (sx + ((l + r) / 2 - lo + 0.5) * cell, top + d * rowh + rowh / 2) for o, l, r, d in nodes}
    rng = {o: (l, r) for o, l, r, d in nodes}
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for o, l, r, d in nodes:
        if par[o] is not None:
            cv.line([pos[par[o]], pos[o]], T['border'], 2)
    bw = min(cell * 0.92, 104)
    bh = min(rowh * 0.74, 78)
    for o, l, r, d in nodes:
        px, py = pos[o]
        main, sub, fill = label(o)
        fill = fill or T['panel2']
        on = fill != T['panel2']
        cv.rect((px - bw / 2, py - bh / 2, px + bw / 2, py + bh / 2), fill=fill, r=10,
                outline=T['yellow'] if (o == cur or o in hot) else T['border'], width=5 if o == cur else (3 if o in hot else 1))
        cv.text((px, py - (8 if sub else 0)), main, 26, T['bg'] if on else T['text'], anchor='mm', bold=True)
        if sub:
            cv.text((px, py + 18), sub, 16, T['bg'] if on else T['muted'], anchor='mm')
        rr = f'[{l}]' if l == r else f'[{l},{r}]'
        cv.text((px, py - bh / 2 - 3), rr, 14, T['dim'], anchor='mb', mono=True)
    return pos


MM = 3   # m = max(x) + 1，线段树维护下标 [0, m]


def _tree(S):
    return S.get('t') if isinstance(S.get('t'), list) else None


def _draw(cv, S, B, box, T):
    t = _tree(S)
    if t is None:
        return
    inner = S.get('_inner', {})
    cur = inner.get('o') if 'o' in inner and 'l' in inner else None
    old = _tree(B) or t

    def label(o):
        v = t[o] if o < len(t) else 0
        ch = o < len(old) and old[o] != v
        return (str(v), '', T['yellow'] if ch else (T['green'] if v else None))
    _seg(cv, box, T, 0, MM, lambda o: (o * 2, o * 2 + 1), 1, label, cur=cur,
         title='线段树 t：叶子 = d[x]（x 处障碍物到其左侧最近障碍物的距离），内部节点 = 区间最大值')


CONFIG = dict(
    num=3161, title='物块放置查询', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='有序集合 + 线段树',
    tags=['灵神题单·常用数据结构', '难度分 2513'],
    setup='''
class SortedList:  # 最小替代：LeetCode 自带 sortedcontainers.SortedList
    def __init__(self, it=()):
        self.a = sorted(it)
    def bisect_left(self, x):
        return bisect_left(self.a, x)
    def add(self, x):
        insort(self.a, x)
    def __getitem__(self, i):
        return self.a[i]
''',
    code='''
class Solution:
    def getResults(self, queries: List[List[int]]) -> List[bool]:
        m = max(q[1] for q in queries) + 1
        t = [0] * (2 << m.bit_length())

        # 把 i 处的值改成 val
        def update(o: int, l: int, r: int, i: int, val: int) -> None:
            if l == r:
                t[o] = val
                return
            m = (l + r) // 2
            if i <= m:
                update(o * 2, l, m, i, val)
            else:
                update(o * 2 + 1, m + 1, r, i, val)
            t[o] = max(t[o * 2], t[o * 2 + 1])

        # 查询 [0,R] 中的最大值
        def query(o: int, l: int, r: int, R: int) -> int:
            if r <= R:
                return t[o]
            m = (l + r) // 2
            if R <= m:
                return query(o * 2, l, m, R)
            return max(t[o * 2], query(o * 2 + 1, m + 1, r, R))

        sl = SortedList([0, m])  # 哨兵
        ans = []
        for q in queries:
            x = q[1]
            i = sl.bisect_left(x)
            pre = sl[i - 1]  # x 左侧最近障碍物的位置
            if q[0] == 1:
                nxt = sl[i]  # x 右侧最近障碍物的位置
                sl.add(x)
                update(1, 0, m, x, x - pre)    # 更新 d[x] = x - pre
                update(1, 0, m, nxt, nxt - x)  # 更新 d[nxt] = nxt - x
            else:
                # 最大长度要么是 [0,pre] 中的最大 d，要么是 [pre,x] 这一段的长度
                max_gap = max(query(1, 0, m, pre), x - pre)
                ans.append(max_gap >= q[2])
        return ans
''',
    call='Solution().getResults([[1,2],[2,2,2],[1,1],[2,2,2]])',
    expect=[True, False],
    views=[
        dict(type='text', fn=lambda S: (f"操作 1：在 x={S['q'][1]} 放障碍物" if S['q'][0] == 1 else f"操作 2：[0,{S['q'][1]}] 内能放下长 {S['q'][2]} 的物块吗？") if 'q' in S else '', size=30, h=60),
        dict(type='array', var=lambda S: S['sl'].a if 'sl' in S else [], label='sl 有序集合（障碍物位置，0 和 m 是哨兵）', h=170),
        dict(type='custom', draw=_draw, h=470),
        dict(type='array', var='ans', label='ans', h=120),
    ],
    watch=['x', 'pre', 'nxt', ('max_gap', 'max_gap', 'green')],
    captions={
        'm = max(q[1]': '`m = max x + 1 = {m}`：线段树维护下标 `[0, {m}]`，值域不大，直接开数组',
        't = [0] *': '线段树数组 `t` 开 `{len(t)}` 个位置，初值 0：此时没有障碍物，所有 `d[x] = 0`',
        'sl = SortedList': '有序集合放入哨兵 `0` 和 `{m}`：保证任何 x 都能找到左、右邻居',
        'i = sl.bisect_left': '在 `sl` 里二分找 `x={x}` 的位置 → `i = {i}`',
        'pre = sl[i - 1]': 'x 左侧最近的障碍物（或哨兵 0）在 ==`{pre}`==',
        'nxt = sl[i]': 'x 右侧最近的障碍物（或哨兵 m）在 ==`{nxt}`==：放下 x 后，这段空隙会被切成两段',
        'sl.add(x)': '把 `{x}` 加入有序集合',
        'update(1, 0, m, x, x - pre)': '新障碍物 x 成了一段空隙 `[{pre},{x}]` 的右端点：`d[{x}] = {x} - {pre} = {x - pre}`',
        'update(1, 0, m, nxt, nxt - x)': '原来 `nxt` 的那段 `[{pre},{nxt}]` 被切短：`d[{nxt}] = {nxt} - {x} = {nxt - x}`',
        'if l == r': lambda S, B, r: '到叶子了：`t[{}]` 就是 `d[{}]`'.format(B._inner['o'], B._inner['l']) if B._inner['l'] == B._inner['r'] else '`[{},{}]` 还没缩成一个点，继续往下找 `i={}`'.format(B._inner['l'], B._inner['r'], B._inner['i']),
        't[o] = val': '叶子 `t[{o}]` 直接改成 `{val}`',
        't[o] = max(': '回溯时重算区间最大值：`t[{o}] = max(t[{o*2}], t[{o*2+1}]) = {t[o]}`',
        'max_gap = max(': '空隙最大长度 = `max(前缀 [0,{pre}] 内完整空隙的最大 d, 不完整的一段 {x}-{pre})` = =={max_gap}==',
        'ans.append': '`{max_gap} >= sz={q[2]}` → ==`{max_gap >= q[2]}`==：{"能放下" if max_gap >= q[2] else "放不下"}',
        'if r <= R': lambda S, B, r: ('区间 `[{l},{r}]` 整个落在 `[0,{R}]` 里 → 直接用 `t[{o}]`' if B._inner['r'] <= B._inner['R'] else '区间 `[{l},{r}]` 超出了 `[0,{R}]`，要拆开查').format(**B._inner),
        'if R <= m': lambda S, B, r: ('`R={R}` ≤ 中点 `{m}`：右半边完全用不到，只查左半边' if B._inner['R'] <= B._inner['m'] else '`R={R}` 超过中点 `{m}`：左半边 `[{l},{m}]` 整段都要').format(**B._inner),
        'return max(t[o * 2]': lambda S, B, r: '左半边整段在范围内，直接取 `t[{}]` = {}；右半边继续往下查，两者取最大'.format(B._inner['o'] * 2, B.t[B._inner['o'] * 2]),
    },
    skip=['m = (l + r) // 2', 'x = q[1]', 'ans = []', 'update(o * 2', 'return query(o * 2 ', 8, 10],
    max_steps=70,
    cards=dict(
        one_liner='空隙长度记在右端点，查询就变成前缀最大值',
        complexity='时间 `O(U + q log U)`，空间 `O(U)`',
        problem=['数轴上两种操作：1 = 在 x 放障碍物；2 = 问 `[0,x]` 内能否放下长 `sz` 的物块（不真放）',
                 '物块不能压障碍物，可以紧贴',
                 '示例：`[[1,2],[2,2,2],[1,1],[2,2,2]]` → `[True, False]`'],
        quote='由于==右端点==在 [0,x] 中的区间是「完整」的，所以要把区间的长度保存在区间的右端点处。如此一来，计算最长长度，就变成一个 RMQ（区间最值查询）问题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`d[x]`：x 是障碍物时，它到左侧最近障碍物的距离；否则为 0',
              '查询 `[0,x]` = 「完整空隙」的最大 `d`（线段树查前缀 `[0,pre]`）与「不完整的一段」`x - pre` 取最大',
              '放障碍物 x：有序集合找 `pre`、`nxt`，各更新一次 `d[x]`、`d[nxt]`'],
        summary=['时间 `O(U + q log U)`，`U ≤ 3q`；空间 `O(U)`',
                 '要先二分、取到 `pre`、`nxt`，再 `add(x)`，顺序别反',
                 '加哨兵 `0` 和 `m`：不用特判边界',
                 '题解还有倒序 + 树状数组、倒序 + 并查集两种写法，这里演示的是线段树',
                 '原文用 `sortedcontainers.SortedList`，本视频在 setup 里用 `bisect` 写了最小替代'],
    ),
)
