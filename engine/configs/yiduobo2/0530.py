# ---- yiduobo 沿用他第 94 题“改树结构”的中序遍历：最右节点连回当前节点、断开 now.left。
# ---- tree 视图自动布局会乱跳，所以用 custom 视图：节点位置按原树固定，边按当前真实指针画；
# ---- 新连的边画粉色弧线，被断开的原边画虚线。s.nodes 只是让可视化拿到全部节点（断开左孩子后有的节点没有变量能指到）
VALS = [1, 0, 48, None, None, 12, 49]
REF = Tr(VALS)
SORTED = sorted(v for v in VALS if v is not None)
PTRS = [('now', 'blue'), ('rightest', 'pink')]


def _ref_info(root):
    pos, kids, order = {}, {}, []

    def ino(n, d):
        if n is None:
            return
        ino(n.left, d + 1)
        order.append((n.val, d))
        ino(n.right, d + 1)
        kids[n.val] = (n.left.val if n.left else None, n.right.val if n.right else None)
    ino(root, 0)
    for i, (v, d) in enumerate(order):
        pos[v] = (i, d)
    return pos, kids


POS, KIDS = _ref_info(REF)


def _done(S):
    last = S.get('last')
    return set() if last is None else {v for v in SORTED if v <= last}


def draw_tree(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '二叉搜索树（粉色箭头 = 新连的边，虚线 = 被断开的原边，绿 = 已访问）', 22, T['muted'], bold=True)
    nodes = {n.val: n for n in S.get('self.nodes', [])}
    n_cols = len(POS)
    sp = min(150, (x1 - x0 - 80) / n_cols)
    dy, rad = min(100, (y1 - y0 - 110) / 2.2), 28
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * n_cols) / 2 + sp / 2

    def P(v):
        i, d = POS[v]
        return sx + i * sp, y0 + 105 + d * dy

    done = _done(S)
    for v, (lv, rv) in KIDS.items():
        n = nodes.get(v)
        for side, c in (('left', lv), ('right', rv)):
            if c is None:
                continue
            ch = getattr(n, side) if n is not None else None
            (X, Y), (X2, Y2) = P(v), P(c)
            if ch is not None and ch.val == c:
                cv.line([(X, Y), (X2, Y2)], T['border'], 4)
            else:
                cv.dashed((X, Y), (X2, Y2), T['dim'], 2, 8, 8)
    for v, n in nodes.items():
        for side, idx in (('left', 0), ('right', 1)):
            ch = getattr(n, side)
            if ch is None or ch.val == KIDS[v][idx]:
                continue
            (X, Y), (X2, Y2) = P(v), P(ch.val)
            p0, p1 = (X + rad * 0.95, Y), (X2, Y2 + rad + 2)
            mid = cv.arc_arrow(p0, p1, (Y2 + rad) - Y, T['pink'], 3, 13)
            cv.text((mid[0] + 8, mid[1] + 4), '新连的边', 19, T['pink'], anchor='lt', bold=True)
    hits = {}
    for name, c in PTRS:
        x = S.get(name)
        if isinstance(x, TreeNode):
            hits.setdefault(x.val, []).append((name, T[c]))
    for v in POS:
        X, Y = P(v)
        hs = hits.get(v, [])
        fill = T['green'] if v in done else T['panel2']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=hs[0][1] if hs else T['border'],
                     width=5 if hs else 2)
        cv.text((X, Y), str(v), 24, T['bg'] if v in done else T['text'], anchor='mm', bold=True)
        for r, (name, c) in enumerate(hs):
            cv.text((X + rad + 6, Y - rad - 2 - r * 24), name, 21, c, anchor='lb', bold=True)
    if 'now' in S and S['now'] is None:
        cv.text((x1 - 20, y0 + 40), 'now = None', 22, T['blue'], anchor='ra', mono=True)


LAST = lambda S: SORTED.index(S['last']) if S.get('last') in SORTED else None   # noqa: E731


def cap_while(S, B, ret):
    if B.now is not None:
        return f'`now = {B.now.val}` 不为空 → 继续'
    return '`now` 为空 → 中序遍历结束'


def cap_if(S, B, ret):
    if B.now.left is not None:
        return f'`{B.now.val}` 有左孩子 → 先找左子树中==最右侧的节点== `rightest`'
    if KIDS[B.now.val][0] is not None:
        return f'`{B.now.val}` 的左孩子==已经被断开==（左子树访问完了）→ 访问它'
    return f'`{B.now.val}` 没有左孩子 → 轮到访问它'


def cap_last(S, B, ret):
    if B['last'] is None:
        return '`last` 为空：这是中序第一个节点，没有可比的'
    if B['last'] == 0:
        return f'`last = 0` 也不是 `None`（==所以不能写成 if last==）→ 和 `{S.now.val}` 比较'
    return f'中序上一个数 `last = {B["last"]}` → 和 `{S.now.val}` 比较'


def cap_res_if(S, B, ret):
    d = abs(S.now.val - S['last'])
    if S.res is None:
        return f'`res` 还是空 → 直接记下差值 `{d}`'
    if d < S.res:
        return f'`|{S.now.val} − {S["last"]}| = {d} < res = {S.res}` → 更新'
    return f'`|{S.now.val} − {S["last"]}| = {d} ≥ res = {S.res}` → 不更新'


def cap_next(S, B, ret):
    if S.now is None:
        return f'`{B.now.val}` 没有右边的路了 → `now = None`'
    if KIDS[B.now.val][1] != S.now.val:
        return f'顺着之前连的边，==自然回到== `{S.now.val}`'
    return f'进入右子树：`now = {S.now.val}`'


CONFIG = dict(
    num=530, title='二叉搜索树的最小绝对差', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='改树结构的中序遍历 · O(1) 空间',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def getMinimumDifference(self, root):
        last = None
        res = None

        now = root
        while now:
            if now.left:
                rightest = now.left
                while rightest.right:
                    rightest = rightest.right
                rightest.right = now
                tmp = now.left
                now.left = None
                now = tmp
            else:
                if last is not None:
                    if res is None or abs(now.val - last) < res:
                        res = abs(now.val - last)
                last = now.val
                now = now.right

        return res
''',
    call=f'''s = Solution()
t = Tr({VALS})
s.nodes = [t, t.left, t.right, t.right.left, t.right.right]
s.getMinimumDifference(t)''',
    expect=1,
    views=[
        dict(type='custom', draw=draw_tree, h=400),
        dict(type='array', var=lambda S: SORTED, label='中序序列（绿 = 已访问，last = 上一个访问的值）', cell=80, h=190,
             pointers={LAST: 'cyan'}, pointer_labels={LAST: 'last'},
             color=lambda S, i, v: 'green' if v in _done(S) else None),
    ],
    watch=[('now', 'now', 'blue'), ('rightest', 'rightest', 'pink'), ('last', 'last', 'cyan'), ('res', 'res', 'green')],
    captions={
        'last = None': '`last`：中序遍历中上一个访问的值；还没有，先为 `None`',
        'res = None': '`res`：答案，先为 `None`',
        'now = root': '`now` 从根开始；==不用递归也不用栈==，空间 `O(1)`',
        'while now:': cap_while,
        'if now.left:': cap_if,
        'rightest = now.left': lambda S, B, r: f'从左孩子 `{S.rightest.val}` 出发找最右节点',
        'while rightest.right': lambda S, B, r: (f'`{B.rightest.val}` 还有右孩子 → 继续往右' if B.rightest.right
                                                 else f'`{B.rightest.val}` 没有右孩子：它是左子树中==最后被访问==的节点'),
        'rightest = rightest.right': '往右走：`rightest = {rightest.val}`',
        'rightest.right = now': lambda S, B, r: (f'`{S.rightest.val}.right = {S.now.val}`：'
                                                 f'==访问完左子树会自然回到 {S.now.val}=='),
        'tmp = now.left': '先记下左孩子 `tmp = {tmp.val}`',
        'now.left = None': lambda S, B, r: f'断开 `{S.now.val}` 的左孩子：==否则回到它时又会再进左子树==',
        'now = tmp': '去遍历左子树：`now = {now.val}`',
        'if last is not None': cap_last,
        'if res is None or': cap_res_if,
        'res = abs(now.val - last)': '`res = {res}`',
        'last = now.val': '记下 `last = {last}`，下一个访问的节点和它比',
        'now = now.right': cap_next,
        'return res': '返回 =={ret}==（注意：原树结构已被修改）',
    },
    cards=dict(
        one_liner='BST 中序天然有序，比较相邻的数；用改树结构的遍历省掉栈',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给二叉搜索树的根节点 `root`，返回==任意两不同节点值之差的最小值==',
                 '示例 1：`root = [4,2,6,1,3]` → `1`',
                 '示例 2（本视频）：`root = [1,0,48,null,null,12,49]` → `1`'],
        quote='bst的==中序遍历是天然有序的==，因此我们只需要求出其中序遍历，比较中序遍历中所有相邻的数来求解答案即可。',
        quote_src='—— yiduobo 题解',
        idea=['数组求两数差的最小值：排序后比较相邻的数',
              'BST 的中序遍历已经有序 → 边遍历边和上一个数 `last` 比',
              '用第 94 题==修改树结构==的中序遍历，省下存遍历序列和栈的空间'],
        result='返回 `1`；遍历结束后原树被改成了一条只往右走的链',
        summary=['时间 `O(n)`：每条边最多走两次；空间 `O(1)`',
                 '代价：会==破坏原树结构==（左孩子被断开），面试时要说明',
                 '易错：`last` 可能是 0，判断要写 `is not None`，不能写 `if last`',
                 '对比灵神：灵神递归 + `pre = -∞`，代码更短，空间 `O(n)`',
                 '原文为 Python 2 风格，只删去了文档字符串和节点定义注释'],
    ),
)
