# 手工排好的布局：值 -> (横向槽位, 深度)
_POS = {1: (2.125, 0), 2: (1.25, 1), 3: (3.0, 1), 4: (0.5, 2), 5: (2.0, 2), 6: (3.0, 2), 7: (0.0, 3), 8: (1.0, 3)}
_EDGES = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8)]
_LEAVES = [7, 8, 5, 6]

SETUP = '''
nd = {v: TreeNode(v) for v in range(1, 9)}
for p, l, r in [(1, 2, 3), (2, 4, 5), (4, 7, 8)]:
    nd[p].left, nd[p].right = nd[l], nd[r]
nd[3].right = nd[6]
lv = [7, 8, 5, 6]
for i, v in enumerate(lv):
    nd[v].left = nd[lv[i - 1]]
    nd[v].right = nd[lv[(i + 1) % len(lv)]]
root = nd[1]
'''


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '特殊二叉树（橙色箭头 = 叶子之间的环：leaf.left 指向前一个叶子）', 22, T['muted'], bold=True)
    vis = S.get('vis') or set()
    ls = S.get('leaf_set') or set()
    q = {n.val for n in (S.get('q') or [])}
    now = S.get('now')
    nv = getattr(now, 'val', None)
    sp = (x1 - x0 - 120) / 3.0
    dy = min(88, (y1 - y0 - 150) / 3.0)
    R = 26

    def P(v):
        sx, d = _POS[v]
        return x0 + 60 + sx * sp, y0 + 62 + d * dy

    for a, b in _EDGES:
        cv.line([P(a), P(b)], T['border'], 3)
    import math as _m
    for i, v in enumerate(_LEAVES):
        pv = _LEAVES[i - 1]
        (ax, ay), (bx, by) = P(v), P(pv)
        if i == 0:  # 首叶子的 left 指向末叶子：从下方绕回去
            yy = ay + R + 22
            cv.line([(ax, ay + R), (ax, yy), (bx, yy), (bx, by + R + 6)], T['orange'], 3)
            cv.tri_up(bx, by + R + 2, 9, T['orange'])
        else:
            d = _m.hypot(bx - ax, by - ay)
            ux, uy = (bx - ax) / d, (by - ay) / d
            cv.arrow((ax + ux * (R + 3), ay + uy * (R + 3)), (bx - ux * (R + 6), by - uy * (R + 6)), T['orange'], width=3)
    for v in range(1, 9):
        X, Y = P(v)
        if v in ls:
            fill = T['orange']
        elif v in q:
            fill = T['green']
        elif v in vis:
            fill = T['yellow']
        else:
            fill = T['panel2']
        on = fill != T['panel2']
        out = T['blue'] if v == nv else T['border']
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=out, width=5 if v == nv else 2)
        cv.text((X, Y), v, 26, T['bg'] if on else T['text'], anchor='mm', bold=True)
    if nv in _POS:
        X, Y = P(nv)
        cv.text((X + R + 4, Y - R - 2), 'now', 19, T['blue'], anchor='lb', bold=True)
    cv.text((x1 - 20, y0 + 6), '黄 = 走过  橙 = 叶子  绿 = 层序已入队', 18, T['dim'], anchor='ra')


def _w1(S, B, ret):
    return f'`now = {S.now.val}` 存在且 {S.now.val} 不在 `vis` 里 → 继续往下走'


def _w1e(S, B, ret):
    return f'`now = {S.now.val}` 已经在 `vis` 里 → ==走回了走过的点，说明进了叶子环==，停下'


def _step(S, B, ret):
    n = B.now
    if n.left:
        return f'`{n.val}` 有左孩子 `{n.left.val}` → 往左走'
    return f'`{n.val}` 没有左孩子 → 往右走'


def _leafwalk(S, B, ret):
    return f'`now = {S.now.val}`，不在 `leaf_set` → 它在叶子环上，继续往左转一圈' if S.now.val not in S.leaf_set else f'`now = {S.now.val}` 已在 `leaf_set`：叶子环转完一圈'


def _kids(side):
    def f(S, B, ret):
        c = getattr(S.now, side)
        w = '左' if side == 'left' else '右'
        if c is None:
            return f'`{S.now.val}` 没有{w}孩子'
        if c.val in S.leaf_set:
            return f'{w}孩子 `{c.val}` 是==叶子==（在 `leaf_set` 里）→ 不入队，否则会绕进环里'
        return f'{w}孩子 `{c.val}` 不是叶子 → 加入队列 `q`'
    return f


CONFIG = dict(
    num=2773, title='特殊二叉树的高度', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='先找出叶子环，再层序遍历',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def heightOfTree(self, root):

        vis = set()
        now = root
        while now and now.val not in vis:
            vis.add(now.val)
            if now.left:
                now = now.left
            else:
                now = now.right
        
        if now:
            leaf_set = set([now.val])
            now = now.left
            while now.val not in leaf_set:
                leaf_set.add(now.val)
                now = now.left
        else:
            leaf_set = set()

        q = [root]
        head, tail = 0, 1
        level = 0
        while head < tail:
            level += 1
            for now in q[head: tail]:
                if now.left and now.left.val not in leaf_set:
                    q.append(now.left)
                if now.right and now.right.val not in leaf_set:
                    q.append(now.right)
            
            head, tail = tail, len(q)
        
        return level
''',
    setup=SETUP,
    call='Solution().heightOfTree(root)',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='set', var='vis', label='vis（沿左侧走过的点）', fmt=lambda x: str(x), h=95),
        dict(type='set', var='leaf_set', label='leaf_set（叶子）', fmt=lambda x: str(x), h=95),
        dict(type='queue', var='q', label='q（层序遍历）', fmt=lambda x: str(x.val), h=100),
    ],
    watch=[('now', lambda S: getattr(S['now'], 'val', None) if 'now' in S else None, 'blue'),
           ('head', 'head', 'cyan'), ('tail', 'tail', 'orange'), ('level', 'level', 'green')],
    captions={
        'vis = set()': '`vis` 记录从根出发「优先向左」走过的节点',
        'now = root': '从根节点出发',
        'while now and now.val not in vis': lambda S, B, r: (_w1(S, B, r) if S.now and S.now.val not in S.vis else (_w1e(S, B, r) if S.now else '`now` 为空，停止')),
        'vis.add': '记录 `{now.val}`，`vis` = {vis}',
        'if now.left:': _step,
        'now = now.left': '`now` → {now.val}',
        'now = now.right': '`now` → {now.val}',
        'if now:': '走到了一个叶子环上的点 `{now.val}`（左边先走回它自己的那个点）',
        'leaf_set = set([now.val])': '这个点一定是叶子，`leaf_set` = {leaf_set}',
        'while now.val not in leaf_set': _leafwalk,
        'leaf_set.add': '`{now.val}` 也是叶子：`leaf_set` = {leaf_set}',
        'leaf_set = set()': '没有环（空树）',
        'q = [root]': '层序遍历从根开始；叶子绝不入队',
        'head, tail = 0, 1': '`q[head:tail]` 就是当前这一层',
        'level = 0': '`level` 记录遍历的轮次',
        'while head < tail': lambda S, B, r: (f'这一层 `q[{S.head}:{S.tail}]` 非空，继续' if S.head < S.tail else '没有新节点了，结束'),
        'level += 1': '进入新的一层：`level` = =={level}==',
        'for now in q[head: tail]': lambda S, B, r: ('本层节点都处理完，退出 for' if (B.get('now') is not None and S.now.val == B.now.val) else f'取本层节点 `{S.now.val}`'),
        'if now.left and': _kids('left'),
        'if now.right and': _kids('right'),
        'q.append(now.left)': '`q` = {[x.val for x in q]}',
        'q.append(now.right)': '`q` = {[x.val for x in q]}',
        'head, tail = tail, len(q)': '本层处理完：下一层是 `q[{head}:{tail}]`',
        'return level': '最后一轮是第 `{level}` 层的节点，高度（边数）= ==`{level}`==',
    },
    cards=dict(
        one_liner='先把叶子环认出来，层序时绕开它，轮次就是高度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一棵二叉树的叶子被连成了环：每个叶子的 `left` 指向前一个叶子、`right` 指向后一个叶子，首尾相接',
                 '求这棵树的高度（根到最深叶子的边数）',
                 '本视频：叶子 `7→8→5→6` 成环，答案 `3`'],
        quote='只需从根节点不断向左侧行走，若当前节点不存在左孩子，则向右侧行走。这样一来，一旦来到某个叶子节点，那么就会不断向左行走，直到走回到这个叶子节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['普通树的高度 = 层序遍历轮次 - 1；这里叶子会绕圈，==只要不碰叶子==，轮次就是高度',
              '优先向左走必到最左叶子，之后沿 `left` 转圈，==第一次遇到重复就是叶子==',
              '再沿环走一圈，把所有叶子收进 `leaf_set`，层序时不入队'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '节点值互不相同，所以用 `val` 放进集合判断',
                 '层序遍历不让叶子入队，所以轮次比常规写法少 1：不用再减 1',
                 '原文代码未改动，Python 3 可直接运行'],
    ),
)
