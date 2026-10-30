def _lvl(root):
    out, q = [], [root]
    while q:
        nd = q.pop(0)
        if nd is None:
            out.append(None)
            continue
        out.append(nd.val)
        q += [nd.left, nd.right]
    while out and out[-1] is None:
        out.pop()
    return out


POS = {3: (0.5, 0), 5: (0.28, 1), 1: (0.72, 1), 6: (0.14, 2), 2: (0.42, 2), 7: (0.32, 3), 4: (0.52, 3)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '二叉树（实线 = 当前 left/right，蓝圈 = now，粉圈 = fa）', 24, T['muted'], bold=True)
    W, H = x1 - x0 - 120, y1 - y0 - 140
    def xy(v):
        a, b = POS[v]
        return (x0 + 60 + a * W, y0 + 80 + b * H / 3)
    nodes = type(S['leaf'])._all
    now, fa = S.get('now'), S.get('fa')
    r = 26
    for n in nodes:
        for c, side in ((n.left, 'L'), (n.right, 'R')):
            if c is not None:
                (ax, ay), (bx, by) = xy(n.val), xy(c.val)
                cv.arrow((ax, ay + (r if by > ay else -r)), (bx, by + (-r if by > ay else r)), T['muted'], 3, 10)
                cv.text(((ax + bx) / 2 + (-14 if side == 'L' else 14), (ay + by) / 2), side, 18, T['dim'], anchor='mm', mono=True)
    for n in nodes:
        X, Y = xy(n.val)
        col = None
        if now is not None and n.val == now.val:
            col = T['blue']
        elif fa is not None and n.val == fa.val:
            col = T['pink']
        cv.rect((X - r, Y - r, X + r, Y + r), fill=T['panel2'], outline=col or T['border'], width=5 if col else 2, r=r)
        cv.text((X, Y), n.val, 26, T['text'], anchor='mm', bold=True)
        if n.val == S['leaf'].val:
            cv.text((X, Y + r + 6), 'leaf', 18, T['green'], anchor='mt', bold=True)


def _v(n):
    return 'None' if n is None else str(n.val)


CONFIG = dict(
    num=1666, title='改变二叉树的根节点', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='沿 parent 向上翻转',
    tags=['灵神题单', '链表树与回溯'],
    setup='''
class Node:
    _all = []

    def __init__(self, val):
        Node._all.append(self)
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        return f'Node({self.val})'

N = {v: Node(v) for v in [3, 5, 1, 6, 2, 7, 4]}
for p, l, r in [(3, 5, 1), (5, 6, 2), (2, 7, 4)]:
    N[p].left = N[l]
    N[l].parent = N[p]
    N[p].right = N[r]
    N[r].parent = N[p]
''',
    code='''
class Solution(object):
    def flipBinaryTree(self, root, leaf):

        now = leaf
        prev_fa = now.parent
        while prev_fa:
            if now.left:
                now.right = now.left
                now.left = None
            
            fa = prev_fa

            if fa.left == now:
                fa.left = None
            else:
                fa.right = None
            
            now.left = fa
            prev_fa = fa.parent
            fa.parent = now
            now = fa
        
        leaf.parent = None
        return leaf
''',
    call='Solution().flipBinaryTree(N[3], N[7])',
    expect=[7, 2, None, 5, 4, 3, 6, None, None, None, 1],
    result_fn=lambda r: _lvl(r),
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=lambda S: f"`now = {_v(S.get('now'))}`，原父亲 `prev_fa = {_v(S.get('prev_fa'))}`，`now.parent = {_v(S['now'].parent) if S.get('now') else 'None'}`", size=24, h=60),
    ],
    watch=[('now', lambda S: _v(S.get('now')), 'blue'), ('prev_fa', lambda S: _v(S.get('prev_fa')), 'pink'),
           ('leaf', lambda S: _v(S.get('leaf')), 'green')],
    captions={
        'now = leaf': '从 `leaf` 出发，一路向上，把每条边的方向翻过来',
        'prev_fa = now.parent': '==先存下原来的父亲== `prev_fa = {prev_fa.val}`：马上要改 `parent` 指针，不存就丢了',
        'while prev_fa': lambda S, B, r: (f'`prev_fa = {S.prev_fa.val}` 存在 → 还没到原来的根，继续翻' if S.prev_fa else '`prev_fa` 为空 → `now` 已是原来的根，翻转完毕'),
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 它要先挪到右边，给新的左孩子（原父亲）腾位置' if S.now.left else f'`{S.now.val}` 没有左孩子，不用挪'),
        'now.right = now.left': '原左孩子变成右孩子：`{now.val}.right = {now.right.val}`',
        'now.left = None': '`{now.val}.left` 先清空',
        'fa = prev_fa': '`fa = {fa.val}`：`now` 的原父亲，它将变成 `now` 的左孩子',
        'if fa.left == now': lambda S, B, r: (f'`fa.left` 就是 `now` → 把这条边从 `{S.fa.val}` 上断开' if S.fa.left == S.now else f'`fa.left` 不是 `now`，那 `now` 是右孩子 → 断开右边'),
        'fa.left = None': '`{fa.val}.left = None`：断开 `fa → now`',
        'fa.right = None': '`{fa.val}.right = None`：断开 `fa → now`',
        'now.left = fa': '`fa` 成为 `now` 的左孩子：`{now.val}.left = {fa.val}`',
        'prev_fa = fa.parent': lambda S, B, r: f'`fa` 的 `parent` 还没改，先记下 `prev_fa = {_v(S.prev_fa)}`，下一轮处理它',
        'fa.parent = now': '`fa.parent = {now.val}`（`parent` 指针也要翻）',
        'now = fa': '`now` 上移到 `{now.val}`',
        'leaf.parent = None': '`leaf` 成为新的根，它没有父亲',
        'return leaf': '返回新的根 `{leaf.val}`',
    },
    cards=dict(
        one_liner='从 leaf 沿 parent 一路向上，把每条边反过来',
        complexity='时间 `O(h)`，空间 `O(1)`',
        problem=['给二叉树 `root` 和其中一个叶子 `leaf`，把 `leaf` 变成新的根',
                 '对 `leaf` 到 `root` 路径上除 `leaf` 外的每个 `cur`：',
                 '`cur` 的左孩子变右孩子；`cur` 的原父亲变成它的左孩子',
                 '示例：`root = 3`，`leaf = 7` → `[7,2,null,5,4,3,6,null,null,null,1]`'],
        quote='需要特别注意的是，题目中的移动同样也需要修改节点的parent指针，因此需要使用一个额外的变量储存待处理节点now的原始父亲节点，然后才能修改now的父亲节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 `leaf` 开始，每轮处理 `now` 和它的原父亲 `fa`',
              '`now` 原来的左孩子挪到右边，断开 `fa → now`，`fa` 接成 `now.left`',
              '`prev_fa` 要在改 `fa.parent` 之前取出，供下一轮使用'],
        summary=['时间 `O(h)`，空间 `O(1)`',
                 '易错：先存原父亲再改 `parent`；断开 `fa` 的旧孩子指针',
                 '原文开头的 `Node` 类定义在注释字符串里，视频里放进了 setup，作者代码未改',
                 '原文为 Python 2 风格，无需改动'],
    ),
)
