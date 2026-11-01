def _treap(S):
    t = S.get('self')
    if type(t).__name__ != 'Treap':
        t = S.get('treap')
    return t if type(t).__name__ == 'Treap' else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'Treap：key = 区间终点，节点里记 length 与子树最小 min_length', 22, T['muted'], bold=True)
    t = _treap(S)
    if t is None or t.root.right is None:
        cv.text((x0 + 30, y0 + 70), '（还没有候选区间）', 26, T['dim'])
        return
    now = S.get('now')
    order = []

    def walk(nd, d):
        if nd is None:
            return
        walk(nd.left, d + 1)
        order.append((nd, d))
        walk(nd.right, d + 1)
    walk(t.root.right, 0)
    n = len(order)
    maxd = max(d for _, d in order)
    W = x1 - x0 - 60
    cw = min(170, W / n)
    gap = min(96, (y1 - y0 - 130) / max(1, maxd))
    pos = {}
    for k, (nd, d) in enumerate(order):
        pos[id(nd)] = (x0 + 30 + cw * (k + 0.5), y0 + 80 + d * gap)
    for nd, d in order:
        px, py = pos[id(nd)]
        for ch in (nd.left, nd.right):
            if ch is not None:
                cx, cy = pos[id(ch)]
                cv.line([(px, py + 30), (cx, cy - 30)], T['border'], 3)
    for nd, d in order:
        px, py = pos[id(nd)]
        hit = now is not None and getattr(now, 'right_bound', None) == nd.right_bound
        fill = T['yellow'] if hit else T['panel2']
        tc = T['bg'] if hit else T['text']
        w = min(cw - 8, 150) / 2
        cv.rect((px - w, py - 30, px + w, py + 30), fill=fill, r=10, outline=T['blue'], width=2)
        cv.text((px, py - 12), f'终点 {nd.right_bound}  长 {nd.length}', 20, tc, anchor='mm', bold=True)
        cv.text((px, py + 12), f'min {nd.min_length}', 20, T['bg'] if hit else T['green'], anchor='mm', bold=True)


def _fml(S):
    if 'q' not in S or S.get('_line', 0) < 150:
        return '先把区间、询问按起点/位置排序，再用 Treap 维护「起点已满足」的候选区间'
    return f"处理询问 `q = {S['q']}`：候选区间里找 ==终点 ≥ {S['q']}== 的最小长度"


CONFIG = dict(
    num=1851, title='包含每个查询的最小区间', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='离线 + 双指针 + Treap（终点为键，维护子树最小长度）',
    tags=['常用数据结构', '难度分 2286'],
    setup='import random\nrandom.seed(0)',
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
    call='Solution().minInterval([[1,4],[2,4],[3,6]], [2,4,5])',
    expect=[3, 3, 4],
    max_steps=66,
    skip=['grand_fa = now.fa.fa', 'now.fa.fa = now', 'now.right.fa = now.fa', 'now.left.fa = now.fa',
          'if now.fa == grand_fa.left', 'grand_fa.left = now', 'grand_fa.right = now', 'now.fa = grand_fa',
          'now.fa.left = now.right', 'now.fa.right = now.left', 'now.right = now.fa', 'now.left = now.fa',
          'self.left = self.right', 'break', 'now = self.root', 'while True', 'self.right_bound =', 'self.length =', 'self.min_length =', 'self.key =', 'self.fa ='],
    views=[
        dict(type='text', fn=_fml, size=26, h=60),
        dict(type='custom', draw=_draw, h=280),
        dict(type='array', var=lambda S: [q[0] for q in S['sorted_queries']], label='sorted_queries 的位置（当前 q 黄色）', cell=90, h=130,
             color=lambda S, i, v: 'yellow' if v == S.get('q') else None),
        dict(type='array', var='res', label='res（按原询问顺序）', cell=90, h=130,
             color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    watch=[('q', 'q', 'blue'), ('p', 'p', 'yellow'), ('now', lambda S: S['now'].right_bound if S.get('now') is not None else None, 'pink'), 'res'],
    captions={
        'treap = Treap()': '建一棵 Treap：==以区间终点为 key==，用来存「起点已经 ≤ 当前询问」的候选区间',
        'sorted_intevals =': '区间按起点从小到大排序',
        'sorted_queries =': '询问带上原下标，按位置从小到大排序（离线）',
        'for q, index': '处理询问 `q = {q}`（原下标 {index}）',
        'while p <': lambda S, B, r: (f"起点 `{S.sorted_intevals[S.p][0]} <= q = {S.q}`：这个区间的起点够得着 → ==放进 Treap==" if S.p < len(S.sorted_intevals) and S.sorted_intevals[S.p][0] <= S.q
                                     else '起点都已加入，或下一个区间起点 > q：停止加区间'),
        'treap.insert(': '插入区间：终点 `{sorted_intevals[p][1]}`，长度 `{sorted_intevals[p][1] - sorted_intevals[p][0] + 1}`',
        'p += 1': '`p` → {p}：指针只往后走，==均摊 O(1)==',
        'now.min_length = min(now.min_length, length)': '沿途每个节点的子树最小长度，都要用新长度 `{length}` 更新',
        'if right_bound == now.right_bound': lambda S, B, r: (f"终点 `{S.right_bound}` 和节点终点 `{S.now.right_bound}` 相同 → 只需取更短的长度" if S.right_bound == S.now.right_bound
                                                             else f"终点 `{S.right_bound}` ≠ 节点终点 `{S.now.right_bound}`" + ('（-1 是假根，真树在它右边）' if S.now.right_bound == -1 else '') + '，继续比大小'),
        'elif right_bound < now.right_bound': lambda S, B, r: (f"`{S.right_bound} < {S.now.right_bound}`：终点更小 → 去左边" if S.right_bound < S.now.right_bound
                                                             else f"`{S.right_bound} > {S.now.right_bound}`：终点更大 → 去右边"),
        'now.length = min(now.length, length)': '终点相同：区间长度只保留更短的，`min({B.now.length}, {length})`',
        'now.left = node': '把新节点挂到 `now` 的左边',
        'now.right = node': '把新节点挂到 `now` 的右边',
        'node = Node': '找到空位，新建节点：key 是随机数（堆序用）',
        'now = node': '新节点就位，开始按随机 key 做旋转，维持堆性质',
        'while now.key < now.fa.key': lambda S, B, r: ('子节点 key 比父节点小 → ==需要旋转上去==' if S.now.key < S.now.fa.key else '堆性质满足，不用旋转了'),
        'if now == now.fa.left': '是左孩子 → 右旋；是右孩子 → 左旋',
        'now.fa.min_length = now.fa.length': '旋转后父节点的子树变了：重算它的 `min_length`（自己 + 左右子树）',
        'now.min_length = min(now.min_length, now.fa.min_length)': '新的子树根 `now` 的 `min_length` 也要合并进来',
        'if self.root.right is None': '假根的右边就是真正的树根；空树直接 `-1`',
        'now = self.root.right': '查询从树根开始：目标是 ==终点 ≥ q== 的区间里最小的长度',
        'res = 10000001': '`res` 先设成一个比所有长度都大的数',
        'while now:': lambda S, B, r: (f'当前节点终点 `{S.now.right_bound}`' if S.get('now') else '走到空了，查询结束'),
        'if q <= now.right_bound': lambda S, B, r: (f"`q = {S.q} <= 终点 {S.now.right_bound}`：它和它右子树的区间都盖住 q" if S.q <= S.now.right_bound
                                                   else f"`q = {S.q} > 终点 {S.now.right_bound}`：它和左子树都盖不住 q，只能去右边"),
        'res = min(res, now.length)': '用这个节点的长度更新答案：`res = {res}`',
        'res = min(res, now.right.min_length)': '右子树整棵都满足终点 ≥ q → ==直接取 min_length==：`res = {res}`',
        'now = now.left': '左子树里可能还有终点 ≥ q 的，继续向左',
        'now = now.right': '去右子树找终点更大的',
        'if res == 10000001': '`res` 没变过说明没有区间盖住 q → `-1`',
        'res[index] = treap.query(q)': '查询 `{q}` 的答案写进原位置 `res[{index}]`',
        'return res': '全部询问处理完，返回 `{res}`',
    },
    cards=dict(
        one_liner='不想写线段树：把候选区间放进 Treap 查最小长度',
        complexity='时间 `O((n+m) log n)`，空间 `O(n)`',
        problem=['区间 `[l, r]` 长度 `r-l+1`；每个询问 `q` 要找==盖住 q 的最短区间==的长度，没有则 `-1`',
                 '示例：`intervals=[[1,4],[2,4],[3,6],[4,4]]`，`queries=[2,3,4,5]`，输出 `[3,3,1,4]`',
                 '本视频：`intervals=[[1,4],[2,4],[3,6]]`，`queries=[2,4,5]` → `[3,3,4]`'],
        quote='设p为满足起点小于等于q[index]的左右区间中最后那一个，那么在这里由于q[index]是单调不减的，因此p同样是单调不减的。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素逐点更新区间必超时；线段树要离散化 + 延迟更新，太繁琐',
              '离线：区间按起点排序、询问按位置排序，起点满足的区间用指针 `p` 依次加入',
              '剩下只需「终点 ≥ q 的区间里取最小长度」：==Treap 以终点为 key，每个节点维护子树最小长度 min_length=='],
        summary=['时间 `O((n+m) log n)`，空间 `O(n)`；Treap 的随机 key 来自 `random`，视频里固定种子 0',
                 '查询时「当前节点 + 右子树」都满足终点 ≥ q，所以可直接取 `now.right.min_length`',
                 '易错点：旋转后 `fa` 与 `now` 的 `min_length` 都要重算；终点相同的节点只保留更短长度',
                 '原文可直接在 Python 3 运行，代码未做改动；与灵神的「并查集跳过已回答」思路完全不同'],
    ),
)
