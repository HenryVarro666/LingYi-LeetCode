SEED = 0


def _nodes(root):
    out = []

    def ino(n, d):
        if n is None:
            return
        ino(n.left, d + 1)
        out.append((n, d))
        ino(n.right, d + 1)
    ino(root, 0)
    return out


def _rooms(S):
    if 'sorted_rooms' not in S:
        return ''
    p = S.get('p', 0)
    parts = [(f'==[{a},{b}]==' if i < p else f'`[{a},{b}]`') for i, (a, b) in enumerate(S['sorted_rooms'])]
    return '房间 [id,面积]：' + ' '.join(parts) + '　（强调 = 已加入 Treap）'


def _queries(S):
    if 'sorted_queries' not in S:
        return ''
    cur = S.get('index')
    parts = [(f'==[{a},{b},{c}]==' if c == cur else f'`[{a},{b},{c}]`') for a, b, c in S['sorted_queries']]
    return '询问 [preferred,minSize,原下标]：' + ' '.join(parts)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    tr = S.get('treap') or S.get('self')
    cv.text((x0 + 18, y0 + 2), 'Treap（二叉搜索树按 id；括号里是随机 key，小顶堆）', 24, T['muted'], bold=True)
    if tr is None or not hasattr(tr, 'root'):
        return
    lst = _nodes(tr.root.right)
    if not lst:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2), '（空树）', 30, T['dim'], anchor='mm')
        return
    n = len(lst)
    maxd = max(d for _, d in lst) + 1
    gx = min(150, (x1 - x0 - 120) / max(n, 1))
    sx = (x0 + x1) / 2 - gx * (n - 1) / 2
    top, gy = y0 + 90, min(110, (y1 - y0 - 150) / max(maxd, 1))
    pos = {id(nd): (sx + i * gx, top + d * gy) for i, (nd, d) in enumerate(lst)}
    for nd, d in lst:
        X, Y = pos[id(nd)]
        for ch in (nd.left, nd.right):
            if ch is not None and id(ch) in pos:
                cv.line([(X, Y), pos[id(ch)]], T['border'], 3)
    now, lm, rm = S.get('now'), S.get('l_max'), S.get('r_min')
    node = S.get('node')
    for nd, d in lst:
        X, Y = pos[id(nd)]
        outline, fill, w = T['border'], T['panel2'], 2
        if nd is now:
            outline, w = T['blue'], 5
        if nd is node:
            outline, w = T['green'], 5
        if lm is not None and nd.v == lm:
            fill = (40, 70, 110)
        if rm is not None and nd.v == rm:
            fill = (110, 50, 80)
        cv.d.ellipse((X - 34, Y - 34, X + 34, Y + 34), fill=fill, outline=outline, width=w)
        cv.text((X, Y - 4), nd.v, 28, T['text'], anchor='mm', bold=True)
        cv.text((X, Y + 48), f'({nd.key % 1000})', 18, T['dim'], anchor='mm')
    if lm is not None:
        cv.text((x1 - 20, y1 - 56), f'l_max = {lm}（蓝底）', 22, T['blue'], anchor='ra', bold=True)
    if rm is not None:
        cv.text((x1 - 20, y1 - 28), f'r_min = {rm}（粉底）', 22, T['pink'], anchor='ra', bold=True)


CONFIG = dict(
    num=1847, title='最近的房间', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='离线排序 + 手写 Treap',
    tags=['灵神题单·常用数据结构', '难度分 2082'],
    setup=f'import random\nrandom.seed({SEED})',
    code='''
class Node(object):
    def __init__(self, v, key, fa):
        self.left = self.right = None
        self.v = v
        self.key = key
        self.fa = fa

class Treap(object):
    def __init__(self):
        self.root = Node(-1, -1, None) #设置假根节点，方便后续的旋转操作
    
    def insert(self, v):
        now = self.root
        while True: #从根节点向下迭代，找到v应该放置的位置
            if v < now.v:
                if now.left is None:
                    node = Node(v, random.randint(0, 2147483647), now)
                    now.left = node
                    break
                else:
                    now = now.left
            elif v > now.v:
                if now.right is None:
                    node = Node(v, random.randint(0, 2147483647), now)
                    now.right = node
                    break
                else:
                    now = now.right
        
        now = node
        while now.key < now.fa.key: #按照key的大小进行树结构的调整
            grand_fa = now.fa.fa
            if now == now.fa.left: #右旋操作
                if now.right:
                    now.right.fa = now.fa
                now.fa.left = now.right
                if now.fa == grand_fa.left:
                    grand_fa.left = now
                else:
                    grand_fa.right = now
                now.fa.fa = now
                now.right = now.fa
                now.fa = grand_fa
            else: #左旋操作
                if now.left:
                    now.left.fa = now.fa
                now.fa.right = now.left
                if now.fa == grand_fa.left:
                    grand_fa.left = now
                else:
                    grand_fa.right = now
                now.fa.fa = now
                now.left = now.fa
                now.fa = grand_fa

    def query(self, v):
        if self.root.right is None:
            return -1
        now = self.root.right
        l_max = r_min = None
        while now:
            if now.v == v: #恰好相等时直接返回
                return now.v
            elif now.v < v: #更新左侧备选答案
                l_max = now.v
                now = now.right
            else:
                r_min = now.v #更新右侧备选答案
                now = now.left
        
        if l_max is None:
            return r_min
        elif r_min is None:
            return l_max
        elif v - l_max <= r_min - v:
            return l_max
        else:
            return r_min

class Solution(object):
    def closestRoom(self, rooms, queries):

        treap = Treap()
        n = len(rooms)
        sorted_rooms = sorted(rooms, key=lambda d:d[1], reverse=True)
        m = len(queries)
        sorted_queries = sorted([[preferred, minSize, index] for index, [preferred, minSize] in enumerate(queries)], key=lambda d:d[1], reverse=True)
        res = [-1] * m

        p = 0 #p指向当前面积最小的备选房间
        for preferred, minSize, index in sorted_queries:
            while p < n and sorted_rooms[p][1] >= minSize:
                treap.insert(sorted_rooms[p][0])
                p += 1
            
            res[index] = treap.query(preferred)
        
        return res
''',
    call='Solution().closestRoom([[1,4],[2,3],[3,5]], [[2,3],[2,4]])',
    expect=[2, 1],
    views=[
        dict(type='text', h=80, size=28, fn=_rooms),
        dict(type='text', h=80, size=28, fn=_queries),
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='res', label='res（按原下标写入）', cell=64, h=110),
    ],
    watch=[('p', 'p', 'pink'), 'preferred', 'minSize', ('res', 'res', 'green')],
    captions={
        83: '建一棵空 Treap；根是一个假根节点（`v = -1`），真正的树挂在 `root.right`',
        85: '房间按面积从大到小排：面积大的先成为候选',
        87: '询问也按 `minSize` 从大到小排，并记下原下标 `index`（答案要按原顺序放）',
        88: '`res` 先全填 `-1`（没有满足条件的房间就是 -1）',
        90: '`p` 指向下一个还没加入候选集的房间',
        91: lambda S, B, r: ('所有询问处理完了' if getattr(B, 'index', None) == S.get('index') and 'preferred' in B else f'处理询问：`preferred = {S.preferred}`，`minSize = {S.minSize}`，原下标 `{S.index}`'),
        92: lambda S, B, r: (f'`sorted_rooms[{S.p}]` 面积 {S.sorted_rooms[S.p][1]} ≥ `{S.minSize}` → 它也是候选，插入 Treap' if S.p < S.n and S.sorted_rooms[S.p][1] >= S.minSize else '面积够的房间都已经在 Treap 里了；候选集只增不减，不用回头'),
        93: '把房间 id `{sorted_rooms[p][0]}` 插入 Treap：先按 id 找位置，再按随机 key 旋转调平衡',
        13: '插入 `{v}`：从根出发，按二叉搜索树的规则往下找位置',
        15: lambda S, B, r: f'`{S.v} < {S.now.v}`？' + ('成立，走左边' if S.v < S.now.v else '不成立，再看是否更大'),
        16: '左孩子为空吗？为空就挂在这里',
        23: '右孩子为空吗？为空就挂在这里',
        21: '往左走：`now = now.left`',
        28: '往右走：`now = now.right`',
        17: '新节点：`v = {v}`，key 是随机数',
        24: '新节点：`v = {v}`，key 是随机数',
        18: '挂成 `now` 的左孩子',
        25: '挂成 `now` 的右孩子',
        30: '从新节点开始，检查 key 是否满足“父亲的 key 更小”的堆性质',
        31: lambda S, B, r: (f'`{S.now.key} < {S.now.fa.key}`：key 比父亲小，破坏堆性质 → ==要旋转==' if S.now.key < S.now.fa.key else f'`{S.now.key} ≥ {S.now.fa.key}`：堆性质成立，不用调整'),
        32: '记下爷爷节点，旋转后要把 `now` 挂到它下面',
        42: '右旋完成：`now` 升到父亲的位置，原父亲成了它的右孩子',
        53: '左旋完成：`now` 升到父亲的位置，原父亲成了它的左孩子',
        33: lambda S, B, r: ('`now` 是左孩子 → 右旋：`now` 升到父亲的位置，父亲成为 `now` 的右孩子' if S.now == S.now.fa.left else '`now` 是右孩子 → 左旋：`now` 升到父亲的位置，父亲成为 `now` 的左孩子'),
        57: '树是空的就没有答案，返回 -1',
        59: '查询 `{v}`：从真正的根 `root.right` 往下走',
        60: '查询 `{v}`，从真正的根 `root.right` 往下走。`l_max`：比 `{v}` 小的最大 id；`r_min`：比 `{v}` 大的最小 id',
        61: lambda S, B, r: ('走到空位，搜索结束' if S.now is None else f'当前节点 `{S.now.v}`'),
        62: lambda S, B, r: (f'`{S.now.v} == {S.v}`：正好有这个 id，直接返回' if S.now.v == S.v else f'`{S.now.v} ≠ {S.v}`，继续'),
        64: lambda S, B, r: (f'`{S.now.v} < {S.v}`：当前 id 偏小，它是左侧候选，往右找更接近的' if S.now.v < S.v else f'`{S.now.v} > {S.v}`：当前 id 偏大，它是右侧候选，往左找更接近的'),
        65: '更新左侧候选：`l_max = {l_max}`',
        66: '往右走，看有没有更大的（仍然小于 `v`）',
        68: '更新右侧候选：`r_min = {r_min}`',
        69: '往左走，看有没有更小的（仍然大于 `v`）',
        71: lambda S, B, r: ('左侧没有候选 → 只能取 `r_min`' if S.l_max is None else '左侧有候选，再看右侧'),
        73: lambda S, B, r: ('右侧没有候选 → 只能取 `l_max`' if S.r_min is None else '两侧都有候选，比较距离'),
        75: lambda S, B, r: f'距离：左 `{S.v} − {S.l_max} = {S.v - S.l_max}`，右 `{S.r_min} − {S.v} = {S.r_min - S.v}`' + ('，左侧不远于右侧（平局取小 id）→ ==l_max==' if S.v - S.l_max <= S.r_min - S.v else '，右侧更近 → ==r_min=='),
        76: '返回 `{ret}`',
        78: '返回 `{ret}`',
        72: '返回 `{ret}`',
        74: '返回 `{ret}`',
        96: '在 Treap 里查 `preferred = {preferred}`，结果写入 `res[{index}]`',
        63: '`{now.v} == {v}`：正好有这个 id，直接返回',
        94: '候选指针后移：`p = {p}`',
        'return res': '答案 `{res}`',
    },
    skip=[3, 4, 5, 6, 10, 84, 86, 14, 30, 32, 34, 35, 36, 37, 38, 39, 40, 41, 43, 45, 46, 47, 48, 49, 50, 51, 52, 54, 57, 59, 88, 13, 19, 26, 94, 62],
    max_steps=130,
    cards=dict(
        one_liner='先按面积排序成“只增不减”的候选集，再在平衡树里找最近 id',
        complexity='时间 `O(n log n + q log n)`，空间 `O(n + q)`',
        problem=['`rooms[i] = [id, size]`，查询 `[preferred, minSize]`：找面积 ≥ `minSize` 且 id 离 `preferred` 最近的房间（平局取小 id，没有则 -1）',
                 '本视频：`rooms=[[1,4],[2,3],[3,5]]`，`queries=[[2,3],[2,4]]` → `[2,1]`'],
        quote='拿到这种在线询问式，但又给出了全部询问的问题，第一反应就是能否通过离线算法来简化问题。能成为当前房间备选答案的房间，必然也能成为后续任意房间的备选答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['房间和询问都按面积从大到小排；询问的 `minSize` 越来越小，候选房间只增不减',
              '指针 `p` 随询问往后扫，把面积够的房间 id 插进 Treap',
              '在 Treap 里往下走，记录比 `preferred` 小的最大 id 和大的最小 id，取更近的'],
        summary=['时间 `O(n log n + q log n)`，空间 `O(n + q)`',
                 '只有插入和查询，没有删除，所以 Treap 的实现比较简单',
                 '易错：距离相等取较小 id（`v - l_max <= r_min - v`）；树空返回 -1',
                 '原文已是 Python 3 可运行写法，代码未改动；随机 key 在 setup 里固定了种子',
                 '对比灵神：灵神用 SortedList + 二分，思路相同，数据结构更省事'],
    ),
)
