def _tree_draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S.get('self.root')
    cv.text((x0 + 18, y0 + 4), '线段树（建在 dfs 序上）：框内 = 区间、区间和 v；绿 = 区间全 0，橙「懒」= 待清零标记', 20, T['muted'], bold=True)
    if root is None:
        cv.text((x0 + 18, y0 + 60), '（线段树还没建好）', 24, T['dim'])
        return
    inner = S.get('_inner') or {}
    now = inner.get('now')
    ql, qr = inner.get('l'), inner.get('r')
    qry = now is not None and isinstance(ql, int) and isinstance(qr, int)
    # 收集叶子，确定横坐标
    leaves = []

    def walk(nd, d):
        if nd.left is None:
            leaves.append(nd)
        else:
            walk(nd.left, d + 1)
            walk(nd.right, d + 1)
    walk(root, 0)
    nL = len(leaves)
    cell = min(130, (x1 - x0 - 40) / nL)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * nL) / 2
    pos = {}

    def place(nd, d):
        if nd.left is None:
            pos[id(nd)] = (sx + (leaves.index(nd) + 0.5) * cell, d)
        else:
            place(nd.left, d + 1)
            place(nd.right, d + 1)
            pos[id(nd)] = ((pos[id(nd.left)][0] + pos[id(nd.right)][0]) / 2, d)
    place(root, 0)
    depth = max(d for _, d in pos.values())
    top = y0 + 95
    gap = min(112, (y1 - y0 - 270) / max(1, depth))
    nw, nh = min(cell * 0.92, 112), 66

    def XY(nd):
        x, d = pos[id(nd)]
        return x, top + d * gap

    def edges(nd):
        if nd.left is not None:
            for c in (nd.left, nd.right):
                a, b = XY(nd), XY(c)
                cv.line([(a[0], a[1] + nh / 2), (b[0], b[1] - nh / 2)], T['border'], 2)
                edges(c)
    edges(root)

    def nodes(nd):
        X, Y = XY(nd)
        zero = nd.all_zero
        out = T['yellow'] if nd is now else (T['orange'] if nd.set_zero else T['border'])
        fill = T['panel2']
        if qry and ql <= nd.l and nd.r <= qr and nd is not now:
            fill = (60, 66, 84)
        cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, outline=out, width=5 if nd is now else 3, r=10)
        cv.text((X, Y - 13), f'[{nd.l},{nd.r}]' if nd.l != nd.r else f'[{nd.l}]', 19, T['muted'], anchor='mm', mono=True)
        cv.text((X, Y + 14), f'v={nd.v}', 24, T['green'] if zero else T['text'], anchor='mm', bold=True, mono=True)
        if nd.set_zero:
            cv.text((X + nw / 2 - 4, Y - nh / 2 - 2), '懒', 18, T['orange'], anchor='rb', bold=True)
        if nd.left is not None:
            nodes(nd.left)
            nodes(nd.right)
    nodes(root)
    # 叶子下方：dfs 序
    ol = S.get('self.order_list') or []
    lo = S.get('self.left_order') or []
    ybase = top + depth * gap + nh / 2 + 34
    cv.text((x0 + 18, ybase - 24), '', 12, T['dim'])
    for i, nd in enumerate(leaves):
        X, _ = XY(nd)
        if i < len(ol):
            who = ol[i]
            enter = lo[who] == i
            cv.text((X, ybase), f'{who}{"入" if enter else "出"}', 24, T['cyan'] if enter else T['pink'], anchor='mm', bold=True)
        cv.text((X, ybase + 26), i, 17, T['dim'], anchor='mm', mono=True)
        if qry and ql <= i <= qr:
            cv.rect((X - cell / 2 + 6, ybase + 40, X + cell / 2 - 6, ybase + 48), fill=T['yellow'], r=4)
    cv.text((x0 + 18, ybase + 62), 'dfs 序：第一次进入记「入」，子树遍历完记「出」；黄条 = 本次递归关心的区间 [l, r]', 18, T['dim'])


def _lk(S, B, r):
    return ''


CONFIG = dict(
    num=1993, title='树上的操作', difficulty='Medium', category='设计',
    author='yiduobo', technique='dfs 序 + 线段树（区间清零懒标记）',
    tags=[],
    code='''
class Node(object):

    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.left = self.right = None
        self.all_zero = True
        self.set_zero = False
        self.v = 0

class LockingTree(object):

    def __init__(self, parent):

        n = len(parent)
        g = {x : set() for x in range(n)}
        for index in range(1, n):
            g[parent[index]].add(index)
        

        self.left_order = [0] * n
        self.right_order = [0] * n
        self.order_list = []

        def dfs(now):
            self.left_order[now] = len(self.order_list)
            self.order_list.append(now)
            for next in g[now]:
                dfs(next)

            self.right_order[now] = len(self.order_list)
            self.order_list.append(now)

        dfs(0)
        self.root = Node(0, len(self.order_list) - 1)
        self.build(self.root)

    def build(self, now):
        if now.l == now.r:
            return
        
        mid = (now.l + now.r) >> 1
        now.left = Node(now.l, mid)
        self.build(now.left)
        now.right = Node(mid + 1, now.r)
        self.build(now.right)

    def set_v(self, now, l, r, v):
        if l == now.l and r == now.r:
            if l == r:
                now.v = v
                if v == 0:
                    now.all_zero = True
                else:
                    now.all_zero = False
                now.set_zero = False
            else:
                now.v = 0
                now.all_zero = now.set_zero = True
            return

        if now.set_zero:
            now.set_zero = False
            now.left.set_zero = now.left.all_zero = True
            now.left.v = 0
            now.right.set_zero = now.right.all_zero = True
            now.right.v = 0

        mid = (now.l + now.r) >> 1
        if r <= mid:
            self.set_v(now.left, l, r, v)
        elif l > mid:
            self.set_v(now.right, l, r, v)
        else:
            self.set_v(now.left, l, mid, v)
            self.set_v(now.right, mid + 1, r, v)

        now.v = now.left.v + now.right.v

        if now.left.all_zero and now.right.all_zero:
            now.all_zero = True
        else:
            now.all_zero = False

    def get_v(self, now, l, r):
        if l == now.l and r == now.r:
            return now.v

        if now.set_zero:
            now.set_zero = False
            now.left.set_zero = now.left.all_zero = True
            now.left.v = 0
            now.right.set_zero = now.right.all_zero = True
            now.right.v = 0
            return 0

        mid = (now.l + now.r) >> 1
        if r <= mid:
            return self.get_v(now.left, l, r)
        elif l > mid:
            return self.get_v(now.right, l, r)
        else:
            return self.get_v(now.left, l, mid) + self.get_v(now.right, mid + 1, r)

    def check_zero(self, now, l, r):
        if now.l == now.r:
            if now.v == 0:
                now.all_zero = True
            else:
                now.all_zero = False
            return now.all_zero
        
        if now.set_zero:
            now.set_zero = False
            now.left.set_zero = now.left.all_zero = True
            now.left.v = 0
            now.right.set_zero = now.right.all_zero = True
            now.right.v = 0
            return True
        
        if l == now.l and r == now.r:
            return now.all_zero
        
        mid = (now.l + now.r) >> 1
        if r <= mid:
            return self.check_zero(now.left, l, r)
        elif l > mid:
            return self.check_zero(now.right, l, r)
        else:
            return self.check_zero(now.left, l, mid) and self.check_zero(now.right, mid + 1, r)

    def lock(self, num, user):
        if self.get_v(self.root, self.left_order[num], self.left_order[num]) == 0:
            self.set_v(self.root, self.left_order[num], self.left_order[num], user)
            self.set_v(self.root, self.right_order[num], self.right_order[num], -user)
            return True
        else:
            return False

    def unlock(self, num, user):
        if self.get_v(self.root, self.left_order[num], self.left_order[num]) == user:
            self.set_v(self.root, self.left_order[num], self.left_order[num], 0)
            self.set_v(self.root, self.right_order[num], self.right_order[num], 0)
            return True
        else:
            return False

    def upgrade(self, num, user):
        if self.get_v(self.root, 0, self.left_order[num]) != 0:
            return False
        if self.check_zero(self.root, self.left_order[num], self.right_order[num]):
            return False

        self.set_v(self.root, self.left_order[num] + 1, self.right_order[num] - 1, 0)
        self.set_v(self.root, self.left_order[num], self.left_order[num], user)
        self.set_v(self.root, self.right_order[num], self.right_order[num], -user)
        return True
''',
    setup='t = LockingTree([-1, 0])',
    call='''out = []
out.append(t.lock(1, 2))
out.append(t.upgrade(0, 1))
out''',
    expect=[True, True],
    views=[
        dict(type='custom', draw=_tree_draw, h=480),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=['num', 'user', 'l', 'r', 'v'],
    max_steps=110,
    skip=['now.left.v = 0', 'now.right.v = 0', 'now.left.set_zero = now.left.all_zero = True',
          'now.right.set_zero = now.right.all_zero = True', 'mid = (now.l + now.r) >> 1', 'if now.set_zero',
          'now.set_zero = False', 'if v == 0', 'now.all_zero = False', 'now.all_zero = True', 'if now.left.all_zero and', 'if l == r', 'if r <= mid', 'elif l > mid', 60, 87, 106, 136],
    captions={
        'if self.get_v(self.root, self.left_order[num]': '==lock({num}, {user})==：线段树查入位置 `{self.left_order[num]}` 的值，是 0 才没上锁',
        'if self.get_v(self.root, 0, self.left_order[num]) != 0': '==upgrade({num}, {user})==：先查前缀 `[0, {self.left_order[num]}]` 的和：不为 0 说明祖先（或自己）有锁',
        'if self.check_zero(': '再查 `num` 的子树区间 `[{self.left_order[num]}, {self.right_order[num]}]` 是不是全 0：全 0 说明没有上锁的子孙 → 不能升级',
        'self.left_order[num] + 1, self.right_order[num] - 1, 0': '子树里面 `[{self.left_order[num] + 1}, {self.right_order[num] - 1}]` 整段清零：所有子孙的锁都解除',
        'self.left_order[num], self.left_order[num], user': '入位置 `{self.left_order[num]}` 写 `{user}`（上锁人）',
        'self.right_order[num], self.right_order[num], -user': '出位置 `{self.right_order[num]}` 写 `-{user}`：和入位置抵消，不影响后面的祖先判断',
        'return self.get_v(now.left': '`r <= mid = {mid}`：目标整个在左半边，往左走',
        'return self.get_v(now.right': '`l > mid = {mid}`：目标整个在右半边，往右走',
        'if l == now.l and r == now.r': lambda S, B, r: (f'目标 `[{S.l},{S.r}]` 正好等于结点 `[{S.now.l},{S.now.r}]` → ==命中==' if (S.l, S.r) == (S.now.l, S.now.r)
                                                            else f'目标 `[{S.l},{S.r}]` ≠ 结点 `[{S.now.l},{S.now.r}]` → 继续往下找'),
        'return now.v': '命中结点，返回它的区间和 `{now.v}`',
        'return now.all_zero': '命中结点，返回「是否全 0」：`{now.all_zero}`',
        'self.set_v(now.left, l, mid, v)': '目标 `[{B.l},{B.r}]` 跨过中点 `{B.mid}`：先递归左段 `[{B.l},{B.mid}]`',
        'self.set_v(now.right, mid + 1, r, v)': '再递归右段 `[{B.mid + 1},{B.r}]`',
        'self.set_v(now.left, l, r, v)': '`r <= mid = {mid}`：整个在左半边，往左递归',
        'self.set_v(now.right, l, r, v)': '`l > mid = {mid}`：整个在右半边，往右递归',
        'now.v = v': '叶子：写入 `v = {v}`',
        'now.v = now.left.v + now.right.v': '回溯：结点 `[{now.l},{now.r}]` 的区间和 = 左 + 右 = `{now.v}`',
        'return True': '返回 `True`',
        'return False': '返回 `False`',
    },
    cards=dict(
        before=[dict(heading='先看 dfs 序与线段树', lines=['树 `[-1,0]` 的 dfs 序：`0入 → 1入 → 1出 → 0出`，位置 0~3', '节点 1 的子树 = 区间 `[1, 2]`；节点 0 的子树 = 区间 `[0, 3]`'])],
        one_liner='dfs 序把子树变成区间，加线段树做区间和与区间清零',
        complexity='每个操作 `O(log n)`，空间 `O(n)`',
        problem=['一棵树，节点可被某用户上锁。设计 `lock`、`unlock`、`upgrade`',
                 '`upgrade(num, user)`：`num` 自己没锁、==子树里至少一个锁==、祖先都没锁，才能升级：清空子树的锁，给 `num` 上锁',
                 '本视频：树 `[-1,0]`（0 是 1 的父节点），演示 `lock(1,2)` 和 `upgrade(0,1)`'],
        quote='dfs序中区间[1, 6]描述的是以1为根节点的子树。这样做的好处就是题目从一个树中的问题转化成了一个数组上的区间操作问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['dfs 序：进入记一次，离开再记一次 → 子树 = 入到出的一段区间',
              '上锁：入位置写 `user`，出位置写 `-user`；祖先判断就变成「前缀和是否为 0」（已完成的节点正负抵消）',
              'upgrade 要三件事：区间和、检测全 0、区间清零 → 线段树 + 清零懒标记'],
        summary=['时间：每次操作 `O(log n)`；空间 `O(n)`；题目规模小，`O(n²)` 暴力也能过',
                 '正负号的妙用：`+user`、`-user` 成对，已离开的节点对前缀和的贡献为 0',
                 '易错：区间清零必须带懒标记，且读写前先下推；`upgrade` 前缀和包含 `num` 自己的入位置',
                 '本视频只演示 lock / upgrade；unlock 与 lock 对称（校验 `user` 后把两端清零）；建树已在开场完成'],
    ),
)
