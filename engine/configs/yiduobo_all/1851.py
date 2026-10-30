def _tr(S):
    t = S.get('treap')
    if t is None:
        t = S.get('self')
    return t


def _root(S):
    t = _tr(S)
    try:
        return t.root.right
    except Exception:
        return None


def _layout(root, x0, y0, x1, y1):
    order, depth, seen = [], {}, set()

    def ino(n, d):
        if n is None or id(n) in seen or d > 8:
            return
        seen.add(id(n))
        depth[id(n)] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(root, 0)
    if not order:
        return {}, order, 0, 0
    maxd = max(depth.values()) + 1
    sp = min(150, (x1 - x0 - 40) / len(order))
    dy = min(110, (y1 - y0 - 100) / max(1, maxd))
    sx = x0 + 20 + ((x1 - x0 - 40) - sp * len(order)) / 2 + sp / 2
    pos = {id(n): (sx + i * sp, y0 + 80 + depth[id(n)] * dy) for i, n in enumerate(order)}
    return pos, order, sp, dy


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'treap：key = 终点（左小右大）；len = 区间长度，min = 子树最小长度', 22, T['muted'], bold=True)
    root = _root(S)
    if root is None:
        cv.text((x0 + 18, y0 + 56), '（空树：还没有备选区间）', 24, T['dim'])
        return
    pos, order, sp, dy = _layout(root, x0, y0, x1, y1)
    cur, new = S.get('now'), S.get('node')
    w = min(132, sp - 8)
    h = 62
    for n in order:
        px, py = pos[id(n)]
        for ch in (n.left, n.right):
            if ch is not None and id(ch) in pos:
                cx, cy = pos[id(ch)]
                cv.line([(px, py + h / 2), (cx, cy - h / 2)], T['border'], 3)
    q = S.get('q')
    for n in order:
        px, py = pos[id(n)]
        fill = T['panel2']
        fg = T['text']
        if new is n:
            fill, fg = T['green'], T['bg']
        elif cur is n:
            fill, fg = T['yellow'], T['bg']
        elif q is not None and 77 <= S.get('_line', 0) <= 94 and n.right_bound >= q:
            fill, fg = T['blue'], T['bg']
        cv.rect((px - w / 2, py - h / 2, px + w / 2, py + h / 2), fill=fill, r=10, outline=T['border'])
        cv.text((px, py - 14), f'终点 {n.right_bound}', 22, fg, anchor='mm', bold=True)
        cv.text((px, py + 14), f'len {n.length}  min {n.min_length}', 19, fg, anchor='mm', mono=True)
        cv.text((px, py + h / 2 + 4), f'key {n.key % 1000}', 16, T['dim'], anchor='mt', mono=True)


ITV = [[1, 5], [2, 3], [3, 7]]
QS = [3, 6]


def _brute(q):
    ls = [r - l + 1 for l, r in ITV if l <= q <= r]
    return min(ls) if ls else -1


def _status(S):
    if 'q' not in S:
        return ''
    return f"当前查询 `q = {S['q']}`（原第 {S['index']} 个）；已加入树的区间数 `p = {S['p']}` / {len(S['sorted_intevals'])}"


def _itv(S):
    if 'sorted_intevals' not in S or 'p' not in S:
        return ''
    parts = []
    for k, (l, r) in enumerate(S['sorted_intevals']):
        parts.append(f'`[{l},{r}]`' if k < S['p'] else (f'==[{l},{r}]==' if k == S['p'] else f'[{l},{r}]'))
    return '按起点排序的区间：' + '  '.join(parts) + '　（强调 = 下一个）'


def _answers(S):
    if 'sorted_queries' not in S or 'index' not in S:
        return ''
    order = sorted(range(len(QS)), key=lambda i: QS[i])
    pos = order.index(S['index'])
    done_cur = S.get('_line') in (78, 92, 94, 111)
    parts = []
    for k, i in enumerate(order):
        known = k < pos or (k == pos and done_cur)
        parts.append(f"q={QS[i]} → ==" + (str(_brute(QS[i])) if known else '?') + '==')
    return '已得到的答案：' + '　'.join(parts)


CONFIG = dict(
    num=1851, title='包含每个查询的最小区间', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='离线排序 + treap（右端点为 key，维护子树最小长度）',
    tags=['难度分 2286'],
    code='''
class Node(object):
    def __init__(self, right_bound, length, key, fa):
        self.left = self.right = None
        self.right_bound = right_bound
        self.length = length
        self.min_length = length
        self.key = key
        self.fa = fa

class Treap(object):
    def __init__(self):
        self.root = Node(-1, 0, -1, None) #设置假根节点，方便后续的旋转操作
    
    def insert(self, right_bound, length):
        now = self.root
        while True: #从根节点向下迭代，找到right_bound应该放置的位置
            now.min_length = min(now.min_length, length) #更新迭代路径上的min_length
            if right_bound == now.right_bound: #如果终点一样，更新length后可以直接返回
                now.length = min(now.length, length)
                return
            elif right_bound < now.right_bound:
                if now.left is None:
                    node = Node(right_bound, length, random.randint(0, 2147483647), now)
                    now.left = node
                    break
                else:
                    now = now.left
            else:
                if now.right is None:
                    node = Node(right_bound, length, random.randint(0, 2147483647), now)
                    now.right = node
                    break
                else:
                    now = now.right
        
        now = node
        while now.key < now.fa.key: #按照key的大小进行树结构的调整
            grand_fa = now.fa.fa
            if now == now.fa.left: #右旋操作
                #在这里三行fa.min_length相关的语句，分别对应了旋转后fa自身的length,fa右子树的min_length以及fa左子树的min_length
                now.fa.min_length = now.fa.length
                if now.fa.right:
                    now.fa.min_length = min(now.fa.min_length, now.fa.right.min_length)
                if now.right:
                    now.right.fa = now.fa
                    now.fa.min_length = min(now.fa.min_length, now.right.min_length)
                now.fa.left = now.right

                if now.fa == grand_fa.left:
                    grand_fa.left = now
                else:
                    grand_fa.right = now
                now.fa.fa = now
                now.right = now.fa
                now.min_length = min(now.min_length, now.fa.min_length)
                now.fa = grand_fa
            else: #左旋操作
                #与上面类似，不过结构是反过来的
                now.fa.min_length = now.fa.length
                if now.fa.left:
                    now.fa.min_length = min(now.fa.min_length, now.fa.left.min_length)
                if now.left:
                    now.left.fa = now.fa
                    now.fa.min_length = min(now.fa.min_length, now.left.min_length)
                now.fa.right = now.left

                if now.fa == grand_fa.left:
                    grand_fa.left = now
                else:
                    grand_fa.right = now
                now.fa.fa = now
                now.left = now.fa
                now.min_length = min(now.min_length, now.fa.min_length)
                now.fa = grand_fa
        
    def query(self, q):
        if self.root.right is None:
            return -1
        now = self.root.right
        res = 10000001
        while now:
            if q <= now.right_bound:
                #使用now的length以及now右侧子树的min_length更新答案
                res = min(res, now.length)
                if now.right:
                    res = min(res, now.right.min_length)
                now = now.left
            else:
                now = now.right
        
        if res == 10000001:
            return -1
        
        return res

class Solution(object):
    def minInterval(self, intervals, queries):

        treap = Treap()
        sorted_intevals = sorted(intervals, key=lambda d:d[0])
        sorted_queries = sorted([[q, index] for index, q in enumerate(queries)], key=lambda d:d[0])
        p = 0
        res = [-1] * len(queries)
        for q, index in sorted_queries:
            while p < len(sorted_intevals) and sorted_intevals[p][0] <= q:
                treap.insert(sorted_intevals[p][1], sorted_intevals[p][1] - sorted_intevals[p][0] + 1)
                p += 1
            
            res[index] = treap.query(q)

        return res
''',

    setup='import random\nrandom.seed(1)',
    call='Solution().minInterval([[1,5],[2,3],[3,7]], [3,6])',
    expect=[2, 5],
    views=[
        dict(type='text', fn=_status, h=56, size=24),
        dict(type='text', fn=_itv, h=70, size=24),
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_answers, h=56, size=24),
    ],
    watch=[('q', lambda S: S.get('q', ''), 'orange'), ('p', lambda S: S.get('p', ''), 'blue'),
           ('right_bound', lambda S: S['_inner'].get('right_bound', ''), 'pink'),
           ('length', lambda S: S['_inner'].get('length', ''), 'cyan')],
    skip=[3, 4, 5, 6, 7, 8, 16, 25, 32, 20, 15, 27, 34, 38, 42, 44, 49, 53, 79, 80, 77, 109, 56, 17, 36, 85, 91],
    captions={
        12: '`Treap` 里放一个==假根==（key=-1，最小），真正的树挂在 `root.right`，旋转时不用特判根',
        99: '建一棵空 treap',
        100: '区间按==起点==排序：查询 q 变大时，起点 ≤ q 的区间只会越来越多',
        101: '查询带上原下标，按 q 从小到大排序（离线）',
        102: '`p`：下一个还没加入 treap 的区间',
        103: '答案默认 `-1`',
        104: '处理查询 `q = {q}`（原第 {index} 个）',
        105: lambda S, B, r: (
            f'`sorted_intevals[{S.p}]` 起点 `{S.sorted_intevals[S.p][0]} <= q = {S.q}` → 这个区间的起点已满足，加入备选'
            if S.p < len(S.sorted_intevals) and S.sorted_intevals[S.p][0] <= S.q else
            (f'下一个区间起点 `{S.sorted_intevals[S.p][0]} > q = {S.q}`，还不能加入' if S.p < len(S.sorted_intevals) else '区间已全部加入')),
        106: '插入区间：终点 `{sorted_intevals[p][1]}`，长度 `{sorted_intevals[p][1] - sorted_intevals[p][0] + 1}`',
        107: '`p` → {p}',
        15: '从假根出发，按终点往下找位置',
        17: '沿途结点的子树都会多一个区间：`min_length` 取小 → `{now.min_length}`',
        18: lambda S, B, r: (
            f'终点 `{S.right_bound}` 和结点相同 → 起点已不重要，只留更短的 length' if S.right_bound == S.now.right_bound
            else f'终点 `{S.right_bound}` ≠ 结点终点 `{S.now.right_bound}`，继续找位置'),
        19: '终点相同，保留较短的长度：`length = {now.length}`',
        21: lambda S, B, r: (
            f'`{S.right_bound} < {S.now.right_bound}` → 往左子树' if S.right_bound < S.now.right_bound
            else f'`{S.right_bound} > {S.now.right_bound}` → 往右子树'),
        22: lambda S, B, r: ('左边是空位 → 新结点放这里' if S.now.left is None else '左边还有结点，继续往下'),
        29: lambda S, B, r: ('右边是空位 → 新结点放这里' if S.now.right is None else '右边还有结点，继续往下'),
        23: '新建结点：终点 `{right_bound}`，长度 `{length}`，再配一个随机优先级 key（treap 的堆序，旋转用）',
        30: '新建结点：终点 `{right_bound}`，长度 `{length}`，再配一个随机优先级 key（treap 的堆序，旋转用）',
        24: '挂到左边',
        31: '挂到右边',
        27: '往左走',
        34: '往右走',
        36: '从新结点开始，检查堆序（父亲的 key 必须更小）',
        37: lambda S, B, r: (
            f'`key {S.now.key} < 父亲 key {S.now.fa.key}` → 新结点比父亲小，需要==旋转==上去' if S.now.key < S.now.fa.key
            else f'`key {S.now.key} > 父亲 key {S.now.fa.key}` → 堆序满足，不用旋转'),
        39: lambda S, B, r: ('是左孩子 → 右旋' if S.now == S.now.fa.left else '是右孩子 → 左旋'),
        41: '旋转后父亲的子树变了：先从它自己的 length 重算 `min_length`',
        43: '再并入父亲右子树的 `min_length`',
        45: '`now` 的右子树改挂到父亲下面',
        46: '并入这棵子树的 `min_length`',
        47: '父亲的左子树 = `now` 原来的右子树',
        50: '`now` 顶替父亲，接到祖父的左边',
        52: '`now` 顶替父亲，接到祖父的右边',
        53: '父亲的 `fa` 改成 `now`',
        54: '原父亲成为 `now` 的右孩子（右旋完成）',
        55: '`now` 的子树现在包含原父亲 → `min_length = {now.min_length}`',
        56: '`now` 接到祖父下面，一次旋转完成',
        59: '旋转后父亲的子树变了：先从它自己的 length 重算 `min_length`',
        65: '父亲的右子树 = `now` 原来的左子树',
        68: '`now` 顶替父亲，接到祖父的左边',
        70: '`now` 顶替父亲，接到祖父的右边',
        72: '原父亲成为 `now` 的左孩子（左旋完成）',
        73: '`now` 的子树现在包含原父亲 → `min_length = {now.min_length}`',
        74: '`now` 接到祖父下面，一次旋转完成',
        77: lambda S, B, r: ('树是空的 → 没有区间包含 q，答案 -1' if S.self.root.right is None else '树不空，开始查'),
        79: '从真正的根开始查 `q = {q}`',
        80: '`res` 先设成比任何长度都大的数',
        81: lambda S, B, r: (f'看结点：终点 `{S.now.right_bound}`' if S.now else '走到空，查询结束'),
        82: lambda S, B, r: (
            f'`q = {S.q} <= 终点 {S.now.right_bound}` → 此结点和右子树的终点都 `>= q`，起点又都 `<= q` → ==全都包含 q=='
            if S.q <= S.now.right_bound else
            f'`q = {S.q} > 终点 {S.now.right_bound}` → 此结点和它的左子树都够不到 q，==整块排除==，去右子树'),
        84: '用该结点自己的长度更新：`res = {res}`',
        85: lambda S, B, r: ('有右子树 → 用它的 `min_length`' if S.now.right else '没有右子树'),
        86: '右子树整棵都包含 q，用 `min_length` 一步更新：`res = {res}`',
        87: '左子树里可能还有终点 `>= q` 的，继续往左',
        89: '往右子树找',
        91: lambda S, B, r: ('一直没更新 → 没有区间包含 q' if S.res == 10000001 else f'找到了，最小长度 `{S.res}`'),
        92: '返回 -1',
        94: '返回最小长度 `{ret}`',
        109: '`q = {q}` 的最短区间长度已写入 `res`',
        111: '全部查询答完：`{ret}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='查询离线排序，区间按起点加入 treap，终点做 key、子树里存最小长度',
        complexity='时间 `O((n + q) log n)`，空间 `O(n)`',
        problem=['给若干闭区间 `[l, r]`（长度 `r-l+1`）和一组查询点 `q`',
                 '每个查询求「包含 `q` 的区间中长度最小的」，没有则 `-1`',
                 '本视频：区间 `[[1,5],[2,3],[3,7]]`，查询 `[3,6]` → `[2,5]`'],
        quote='对于当前的查询q[index]而言，设p为满足起点小于等于q[index]的左右区间中最后那一个，那么在这里由于q[index]是单调不减的，因此p同样是单调不减的。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间按起点、查询按 `q` 排序：起点 `<= q` 的区间只增不减，用指针 `p` 逐个加入',
              '备选区间起点都合格，只需要「终点 `>= q`」中长度最小 → treap 以终点为 key，结点维护子树最小长度 `min_length`',
              '查询时：`q <= 终点` 就收下该结点和整个右子树，再去左边；否则整块丢掉去右边'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`；treap 靠随机优先级期望平衡',
                 '易错点：终点相同时只更新 length；旋转后要同步重算 `min_length`',
                 '用假根结点（key=-1）省去旋转时对根的特判，真树在 `root.right`',
                 '原文用到 `random`，视频里固定 `random.seed(1)`，树形随种子而变，结果不变',
                 '题解首选线段树 + 离散化 + 延迟更新，作者嫌麻烦，改用复用 1847 题的 treap'],
    ),
)
