# 原树（二叉搜索树 [4,2,5,1,3]）：值 = 中序名次；静态位置 / 深度 / 子树最小值（只用于画图和推导 first、prev）
SPEC = (4, (2, (1, None, None), (3, None, None)), (5, None, None))
DEPTH = {4: 0, 2: 1, 5: 1, 1: 2, 3: 2}
MINSUB = {4: 1, 2: 1, 5: 5, 1: 1, 3: 3}
TREE_EDGES = {(4, 2), (4, 5), (2, 1), (2, 3)}
N = 5


def _vis(S, B):
    """这一步执行完后，已经「处理完」（执行过 prev = now）的节点值范围 hi，以及 first / prev 的值。
    原文的 first / prev 是全局变量，追踪不到，这里根据「刚执行的行 + 当前节点」推出来。"""
    L = S.get('_line')
    nb = (B.get('_inner') or {}).get('now')
    if nb is None:
        hi = 0 if L <= 26 else N
        return hi, (1 if hi else None), (hi or None)
    v = nb.val
    if L in (13, 14):
        hi = MINSUB[v] - 1
    elif L in (16, 17, 19, 20):
        hi = v - 1
    else:
        hi = v
    first = 1 if (hi >= 1 or (L == 17 and v == 1)) else None
    return hi, first, (hi or None)


def _collect(root):
    seen, order, st = set(), [], [root]
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        order.append(n)
        st += [n.left, n.right]
    return order


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    root = S.get('root')
    cv.text((x0 + 18, y0 + 4), '蓝箭头 = left 指针，粉箭头 = right 指针；绿底 = 已按中序接进链表', 21, T['muted'], bold=True)
    if root is None:
        return
    nodes = _collect(root)
    sp = min(150, (x1 - x0 - 80) / N)
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * N) / 2 + sp / 2
    dy = min(110, (y1 - y0 - 200) / 2)
    ty = y0 + 90
    rad = 27

    def P(n):
        return sx + (n.val - 1) * sp, ty + DEPTH[n.val] * dy

    first_v = prev_v = None
    _, first_v, prev_v = _vis(S, B)
    hi = _vis(S, B)[0]
    now = (S.get('_inner') or {}).get('now')
    wraps = []
    for n in nodes:
        for side, c in (('left', T['blue']), ('right', T['pink'])):
            t = getattr(n, side)
            if t is None or t is n:
                continue
            (ax, ay), (bx, by) = P(n), P(t)
            if abs(n.val - t.val) == N - 1 and (n.val, t.val) not in TREE_EDGES and (t.val, n.val) not in TREE_EDGES:
                wraps.append((n, t, c))
                continue
            dx, dyy = bx - ax, by - ay
            d = math.hypot(dx, dyy) or 1
            ux, uy = dx / d, dyy / d
            off = 7 if side == 'right' else -7
            ox, oy = -uy * off, ux * off
            cv.arrow((ax + ux * rad + ox, ay + uy * rad + oy), (bx - ux * (rad + 2) + ox, by - uy * (rad + 2) + oy), c, 3, 11)
    for n, t, c in wraps:
        (ax, ay), (bx, by) = P(n), P(t)
        cv.arc_arrow((ax, ay + rad), (bx, by + rad), -(200 if c == T['blue'] else 255), c, 3, 12)
    for n in nodes:
        X, Y = P(n)
        done = n.val <= hi
        outline = T['green'] if n.val == first_v else (T['yellow'] if n.val == prev_v else T['border'])
        if now is not None and n.val == now.val:
            outline = T['blue']
        fill = (45, 95, 70) if done else T['panel2']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outline, width=4 if outline != T['border'] else 2)
        cv.text((X, Y), n.val, 30, T['text'], anchor='mm', bold=True)
        labs = []
        if now is not None and n.val == now.val:
            labs.append(('now', T['blue']))
        if n.val == first_v:
            labs.append(('first', T['green']))
        if n.val == prev_v:
            labs.append(('prev', T['yellow']))
        for k, (t, c) in enumerate(labs):
            cv.text((X, Y - rad - 6 - k * 24), t, 21, c, anchor='mb', bold=True)


def _info(S, B):
    hi, f, p = _vis(S, B)
    fs = f'`{f}`' if f else '`None`'
    ps = f'`{p}`' if p else '`None`'
    return f'全局变量：`first` = =={fs[1:-1]}==（链表最小节点），`prev` = =={ps[1:-1]}==（上一个中序节点）'


def _nb(S):
    return S['_inner']['now']


def _cap_first(S, B, ret):
    return f"`first is None`：这是中序遍历==第一个==处理的节点，也是最左的叶子 → `first = {B._inner['now'].val}`（最小值）"


def _cap_link(S, B, ret):
    n = B._inner['now'].val
    return f'`now.left = prev`：`{n}` 的 left 指向前驱 `{n - 1}`'


def _cap_link2(S, B, ret):
    n = B._inner['now'].val
    return f'`prev.right = now`：前驱 `{n - 1}` 的 right 指向 `{n}` → 两个节点双向相连'


def _cap_prev(S, B, ret):
    n = B._inner['now'].val
    return f'`prev = now`：`prev` 更新为 `{n}`，下一个中序节点来了才会和它相连'


def _cap_isfirst(S, B, ret):
    n = B._inner['now'].val
    first = (n == 1)
    return ('`first is None` 成立' if first else '`first` 已有值 → 走 `else`，和前驱相连')


CONFIG = dict(
    num=426, title='将二叉搜索树转化为排序的双向链表', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='中序遍历 + prev 指针',
    tags=['链表树与回溯'],
    setup='''
import tracer
class Node(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self._uid = tracer.next_uid()
    def __repr__(self):
        return 'Node(%s)' % self.val

def _mk(s):
    if s is None:
        return None
    return Node(s[0], _mk(s[1]), _mk(s[2]))

def _lst(h):
    r, x = [], h
    while True:
        r.append(x.val)
        x = x.right
        if x is h:
            break
    l, x = [], h
    while True:
        l.append(x.val)
        x = x.left
        if x is h:
            break
    return r, l

T0 = _mk((4, (2, (1, None, None), (3, None, None)), (5, None, None)))
''',
    code='''
class Solution(object):
    def treeToDoublyList(self, root):

        if not root:
            return None

        global first, prev
        first = None
        prev = None

        def dfs(now):
            global first, prev
            if now.left:
                dfs(now.left)
            
            if first is None:
                first = now
            else:
                now.left = prev
                prev.right = now

            prev = now
            if now.right:
                dfs(now.right)

        dfs(root)
        
        first.left = prev
        prev.right = first

        return first
''',
    call='_lst(Solution().treeToDoublyList(T0))',
    expect=([1, 2, 3, 4, 5], [1, 5, 4, 3, 2]),
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='text', fn=_info, size=24, h=56),
        dict(type='calls', h=190, hide=()),
    ],
    watch=[('now', lambda S: S['_inner']['now'].val if 'now' in S.get('_inner', {}) else None, 'blue')],
    captions={
        4: '空树直接返回 `None`；否则做中序遍历',
        'first = None': '`first` 记录链表头（最小节点），`prev` 记录中序里的上一个节点；都是全局变量，先清空',
        26: '从根出发做中序遍历：==左 - 根 - 右==，二叉搜索树的中序正好是升序',
        13: lambda S, B, r: (f"`now = {B._inner['now'].val}` 有左孩子 → 先去处理左子树" if B._inner['now'].left is not None and B._inner['now'].left.val < B._inner['now'].val and (B._inner['now'].val, B._inner['now'].left.val) in TREE_EDGES else f"`now = {B._inner['now'].val}` 没有左孩子 → 左边没有更小的了，轮到自己"),
        14: '先递归处理左子树（比 `now` 小的都先处理）',
        16: _cap_isfirst,
        17: _cap_first,
        19: _cap_link,
        20: _cap_link2,
        22: _cap_prev,
        23: lambda S, B, r: (f"`now = {B._inner['now'].val}` 有右孩子 → 处理右子树" if B._inner['now'].right is not None and (B._inner['now'].val, B._inner['now'].right.val) in TREE_EDGES else f"`now = {B._inner['now'].val}` 没有右孩子 → 这棵子树处理完，回到上一层"),
        24: '再递归处理右子树（比 `now` 大的）',
        28: '遍历完：`prev` 是最大节点 → `first.left = prev`，头的 left 指向尾',
        29: '`prev.right = first`：尾的 right 指向头 → ==首尾相连，成环==',
        31: lambda S, B, r: f'返回 `first`（值最小的节点 `{r.val}`）',
    },
    skip=[],
    max_steps=140,
    cards=dict(
        one_liner='中序遍历是升序：边遍历边用 prev 把相邻节点连成双向链表',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['把二叉搜索树原地转换成排序的==循环双向链表==',
                 '树的 `left` 当作链表的前驱，`right` 当作后继；首尾也要相连',
                 '返回链表中最小元素的节点',
                 '本视频：`[4,2,5,1,3]` → `1 ⇄ 2 ⇄ 3 ⇄ 4 ⇄ 5`（首尾相连）'],
        quote='每遍历到一个节点now，若prev非空，就都应该对prev和now之间建立双向的连接，同时将prev置为now然后继续进行中序遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['要排好序，就得==中序遍历==；用 `prev` 记住上一个遍历到的节点',
              '`first` 是最小节点：中序里 `prev` 还为空的那一轮（最左叶子）就是它',
              '每个 `now`：`now.left = prev`、`prev.right = now`；遍历完再把 `first` 和最后的 `prev` 相连成环'],
        summary=['时间 `O(n)`，空间 `O(h)`；原地修改，没有新建节点',
                 '易错点：先递归左子树，再连 `prev` 和 `now`；顺序错了链表不再有序',
                 '`first` 只在第一次赋值（`first is None`），`prev` 每个节点都更新',
                 '别忘了最后的首尾相连：`first.left = prev`，`prev.right = first`',
                 '`first` / `prev` 在原文里是 `global` 全局变量，视频里的 first / prev 标记是按遍历顺序推出来的；`Node` 类原文是注释，在 setup 补上'],
    ),
)
