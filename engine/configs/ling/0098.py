# ---- 每个访问过的节点下方标出它的合法开区间 (left, right)：绿 = 子树合法，红 = 不合法，黄 = 正在检查
TREE_H = 380
INFO = {}      # uid -> [区间文字, 状态]
SEEN = set()   # 第 7 行第一次执行过的节点（第 7 行在递归返回后会再次触发）


def f(v):
    return '-∞' if v == -inf else ('∞' if v == inf else str(v))


def _walk(root):
    out, st, seen = [], [root], set()
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        out.append(n)
        st += [n.left, n.right]
    return out


def track(fn, visit=False, result=False):
    def cap(S, B, ret):
        r = S.get('root')
        if visit and r is not None:
            INFO[r._uid] = [f'({f(S.left)}, {f(S.right)})', 'run']
        if result and ret is not None and r is not None:
            INFO[r._uid][1] = 'ok' if ret else 'bad'
        for n in _walk(S.get('self.tree')):
            n._d = tuple(INFO[n._uid]) if n._uid in INFO else None  # 拷贝：之后状态改变不影响这一步
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _layout(root, box):  # 与 views.v_tree 相同的布局
    x0, y0, x1, y1 = box
    order, depth = [], {}

    def ino(n, d):
        if n is None or n._uid in depth:
            return
        depth[n._uid] = d
        ino(n.left, d + 1)
        order.append(n)
        ino(n.right, d + 1)
    ino(root, 0)
    maxd = max(depth.values()) + 1
    sp = min(78, (x1 - x0 - 60) / max(1, len(order)))
    dy = min(95, (y1 - y0 - 80) / max(1, maxd))
    rad = max(14, min(26, sp * 0.4, dy * 0.32))
    sx = x0 + 30 + ((x1 - x0 - 60) - sp * len(order)) / 2 + sp / 2
    pos = {n._uid: (sx + i * sp, y0 + 60 + depth[n._uid] * dy + rad) for i, n in enumerate(order)}
    return pos, rad, order


def badges(cv, S, B, box, T):
    root = S.get('self.tree')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if not d:
            continue
        X, Y = pos[n._uid]
        c = {'ok': T['green'], 'bad': T['red'], 'run': T['yellow']}[d[1]]
        w = cv.tlen(d[0], 17, bold=True, mono=True) + 12
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 27), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 15), d[0], 17, c, anchor='mm', bold=True, mono=True)


def tree_color(S, n):
    d = getattr(n, '_d', None)
    return {'ok': 'green', 'bad': 'red'}.get(d[1]) if d else None


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.root is None:
        return '空节点 → 合法（递归边界）'
    return f'节点 `{S.root.val}` 必须落在开区间 `({f(S.left)}, {f(S.right)})` 里'


def cap_ret7(S, B, ret):
    r = S.root
    if ret is None:
        if r._uid not in SEEN:
            SEEN.add(r._uid)
            return f'判断 `{f(S.left)} < {S.x} < {f(S.right)}` → ==成立==，接着检查子树'
        return f'左子树合法 ✓（`and` 继续往后算）→ 去检查右子树'
    if ret:
        return f'`{S.x}` 在区间内，左右子树也都合法 → 返回 `True`'
    if not (S.left < S.x < S.right):
        return f'`{S.x}` 不在 `({f(S.left)}, {f(S.right)})` 里 → ==不是二叉搜索树==，返回 `False`'
    return '子树不合法 → `and` 短路，直接返回 `False`'


def cap_l(S, B, ret):
    return (f'递归左子树 `{nv(S.root)}`：左边的数都要 ==小于 {B.x}==，'
            f'上界收紧为 `{B.x}` → 区间 `({f(S.left)}, {f(S.right)})`')


def cap_r(S, B, ret):
    return (f'递归右子树 `{nv(S.root)}`：右边的数都要 ==大于 {B.x}==，'
            f'下界收紧为 `{B.x}` → 区间 `({f(S.left)}, {f(S.right)})`')


CONFIG = dict(
    num=98, title='验证二叉搜索树', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='前序遍历 · 传递上下界',
    code='''
class Solution:
    def isValidBST(self, root: Optional[TreeNode], left=-inf, right=inf) -> bool:
        if root is None:
            return True
        x = root.val
        return left < x < right and \\
               self.isValidBST(root.left, left, x) and \\
               self.isValidBST(root.right, x, right)
''',
    call='''s = Solution()
s.tree = Tr([5,4,6,None,None,3,7])
s.isValidBST(s.tree)''',
    expect=False,
    views=[
        dict(type='tree', label='二叉树（下方 = 合法区间；绿 合法 / 红 不合法）', pointers={'root': 'blue'},
             h=TREE_H, color=tree_color),
        dict(type='custom', draw=badges, h=0),
        dict(type='text', h=60, fn=lambda S: (f"当前节点 `{S['root'].val}` 的合法区间：==({f(S['left'])}, {f(S['right'])})=="
                                               if S.get('root') is not None else '')),
        dict(type='calls', h=190),
    ],
    watch=[('root', 'root', 'blue'), ('left', 'left'), ('right', 'right')],
    captions={
        'if root is None': track(cap_if, visit=True),
        'return True': track('空树是合法的二叉搜索树 → `True`'),
        'x = root.val': track(lambda S, B, ret: f'`x = {S.x}`'),
        'return left < x < right': track(cap_ret7, result=True),
        'self.isValidBST(root.left': track(cap_l),
        'self.isValidBST(root.right': track(cap_r),
    },
    cards=dict(
        one_liner='从根往下传区间：往左走收紧上界，往右走收紧下界',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
        problem=['判断二叉树是否是==有效的二叉搜索树==',
                 '左子树==所有==节点 < 根 < 右子树==所有==节点，且子树也是 BST',
                 '本视频：`[5,4,6,null,null,3,7]` → `false`（3 在 5 的右子树里）'],
        quote='dfs 额外传入两个参数，分别表示==从根到当前节点路径上的最小值和最大值==。当前节点的值必须在最小值和最大值之间（不能等于）。',
        quote_src='—— 灵茶山艾府题解「方法一：前序遍历」',
        idea=['只和父节点比较不够：`3 < 6` 没问题，但 `3` 在 `5` 的右边，必须 `> 5`',
              '根的区间是 `(-∞, ∞)`；往左走，上界变成当前值；往右走，下界变成当前值',
              '一旦有节点不在区间里，`and` 短路，直接返回 `False`'],
        result='运行结束，返回 `False`：节点 `3` 的合法区间是 `(5, 6)`，3 不在里面',
        summary=['时间 `O(n)`，空间 `O(n)`；前序在某些数据下不用递归到叶子就能返回，最快',
                 '易错：区间是==开区间==，等于也不行；Java 等语言要用 `long` 防溢出',
                 '灵神方法二「中序」：中序遍历严格递增 ⇔ 是 BST，只需记录上一个值 `pre`',
                 '灵神方法三「后序」：返回子树最小值和最大值，思想最通用（DP 的自底向上）'],
    ),
)
