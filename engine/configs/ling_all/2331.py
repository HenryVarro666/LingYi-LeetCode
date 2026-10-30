# ---- 树上“已算出”标注：每一步的 caption 回调里按调用栈判断哪些节点已经返回，custom 叠加层（h=0）画在 tree 视图的节点下方
TREE_H = 340
SEEN = set()  # 已经进入过的节点


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


def _path(root, target):
    """根 -> target 的节点列表（= 当前递归调用栈）"""
    if root is None:
        return None
    if root._uid == target._uid:
        return [root]
    for ch in (root.left, root.right):
        p = _path(ch, target)
        if p:
            return [root] + p
    return None


def truth(n):
    if n.left is None:
        return n.val == 1
    if n.val == 2:
        return truth(n.left) or truth(n.right)
    return truth(n.left) and truth(n.right)


def _op(n):
    return {0: '叶子 0 = False', 1: '叶子 1 = True', 2: 'OR 节点', 3: 'AND 节点'}[n.val]


def _mark(S):
    """把「已经算完 / 被短路跳过」的状态记到这一步快照的节点上（n._d：True/False/'skip'）"""
    tree, cur = S.get('self.tree'), S.get('root')
    if tree is None or cur is None:
        return
    path = {n._uid for n in (_path(tree, cur) or [])}
    SEEN.update(path)
    nodes = _walk(tree)
    for n in nodes:
        n._d = truth(n) if (n._uid in SEEN and n._uid not in path) else None
    for p in nodes:
        if p.left is not None and p.left._d in (True, False):
            if (p.val == 2 and p.left._d) or (p.val == 3 and not p.left._d):
                if p.right._uid not in SEEN:
                    for q in _walk(p.right):
                        q._d = 'skip'


def track(fn):
    def cap(S, B, ret):
        _mark(S)
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
        if d is None:
            continue
        X, Y = pos[n._uid]
        if d == 'skip':
            cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=(36, 41, 49), outline=T['border'], width=2)
            cv.text((X, Y), n.val, int(rad * 0.95), T['dim'], anchor='mm', bold=True)
            s, c = '跳过', T['muted']
        else:
            s, c = ('True', T['green']) if d else ('False', T['red'])
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, c, anchor='mm', bold=True)


def _info(S):
    cur = S.get('root')
    if cur is None:
        return '叶子是 `0`（False）/ `1`（True）；`2` 是 OR，`3` 是 AND'
    if cur.left is None:
        return f'当前节点 `{cur.val}`：==叶子==，值就是它自己'
    word = 'OR：有一个真就真' if cur.val == 2 else 'AND：两个都真才真'
    return f'当前节点 `{cur.val}`：=={_op(cur)}==，{word}'


def cap_leaf_test(S, B, ret):
    n = S.root
    if n.left is None:
        return f'`root.left` 是空 → 完整二叉树里没有左孩子就是==叶子==，值 `{n.val}`'
    return f'`{n.val}` 有左孩子 → 是运算节点（{"OR" if n.val == 2 else "AND"}），要先算出两个孩子的值'


def cap_leaf_ret(S, B, ret):
    n = S.root
    path = _path(S.get('self.tree'), n)
    head = f'叶子 `{n.val}`：`{n.val} == 1` → =={ret}=='
    if len(path) == 1:
        return head + '，它就是整棵树的值'
    p = path[-2]
    left = p.left._uid == n._uid
    if left and ((p.val == 2 and ret) or (p.val == 3 and not ret)):
        w = ('or', '真') if p.val == 2 else ('and', '假')
        return head + f'；它是 `{p.val}` 的左孩子，`{w[0]}` 左边已经为{w[1]} → ==短路==，右孩子不用算，`{p.val}` 直接返回 =={ret}=='
    if left:
        return head + f'；交给父节点 `{p.val}`，还得去算右孩子 `{p.right.val}`'
    return head + f'；右孩子也有结果了，回到父节点 `{p.val}`'


def cap_val2(S, B, ret):
    n = S.root
    if n.val == 2:
        return '`root.val == 2` 成立 → 这是 ==OR== 节点，走 `or`'
    return f'`root.val == {n.val}`，不是 2 → 这是 ==AND== 节点，走最后一行的 `and`'


def _back(S, ret):
    """两个孩子都算完，回到这一行准备返回"""
    n = S.root
    op = 'or' if n.val == 2 else 'and'
    l, r = truth(n.left), truth(n.right)
    tail = '，==整棵树的值就是它==' if len(_path(S.get('self.tree'), n)) == 1 else '，返回给上一层'
    return f'`{n.val}` 的两个孩子都算完：`{l} {op} {r}` → =={ret}=={tail}'


def cap_or(S, B, ret):
    if ret is not None:
        return _back(S, ret)
    n = B.root
    return (f'OR 节点 `{n.val}`：先递归左孩子 `{n.left.val}`；==左边为真，`or` 就不再算右边==，'
            f'左边为假才去算右孩子 `{n.right.val}`')


def cap_and(S, B, ret):
    if ret is not None:
        return _back(S, ret)
    n = B.root
    return (f'AND 节点 `{n.val}`：先递归左孩子 `{n.left.val}`；==左边为假，`and` 就不再算右边==，'
            f'左边为真才去算右孩子 `{n.right.val}`')


CONFIG = dict(
    num=2331, title='计算布尔二叉树的值', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 自底向上（Go 原文转写）',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1304'],
    code='''
class Solution:
    def evaluateTree(self, root: Optional[TreeNode]) -> bool:
        if root.left is None:
            return root.val == 1
        if root.val == 2:
            return self.evaluateTree(root.left) or self.evaluateTree(root.right)
        return self.evaluateTree(root.left) and self.evaluateTree(root.right)
''',
    call='''s = Solution()
s.tree = Tr([3,2,3,1,0,1,2,None,None,None,None,None,None,0,1])
s.evaluateTree(s.tree)''',
    expect=True,
    views=[
        dict(type='tree', var='self.tree', label='2=OR  3=AND  叶子 0/1（绿=True 红=False 蓝=root）', pointers={'root': 'blue'}, h=TREE_H,
             color=lambda S, n: ('green' if n._d else 'red') if getattr(n, '_d', None) in (True, False) else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='calls', h=200),
    ],
    watch=[('root', lambda S: None if S.get('root') is None else S['root'].val, 'blue')],
    captions={
        'if root.left is None': track(cap_leaf_test),
        'return root.val == 1': track(cap_leaf_ret),
        'if root.val == 2': track(cap_val2),
        'return self.evaluateTree(root.left) or': track(cap_or),
        'return self.evaluateTree(root.left) and': track(cap_and),
    },
    cards=dict(
        one_liner='叶子直接取值，运算节点先算两个孩子再 or / and',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['完整二叉树：叶子是 `0`（False）或 `1`（True）',
                 '非叶子是 `2`（OR）或 `3`（AND），对两个孩子的值做运算',
                 '返回根节点的布尔值；每个节点要么 0 个孩子，要么 2 个',
                 '本视频：`[3,2,3,1,0,1,2,…,0,1]` → `True`'],
        quote='`if root.Left == nil { return root.Val == 1 }`；`if root.Val == 2 { return evaluateTree(root.Left) || evaluateTree(root.Right) }`；否则返回左 `&&` 右',
        quote_src='—— 灵茶山艾府题解（原文只有 Go 代码）',
        idea=['没有左孩子就是叶子 → 直接 `root.val == 1`',
              '`root.val == 2` 是 OR：==左右孩子的值做 `or`==；否则 `val == 3` 是 AND，做 `and`',
              '只有孩子的值都算出来，才能算自己 → ==自底向上==，不需要任何额外变量'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`||` → `or`，`&&` → `and`，`nil` → `None`）',
                 '时间 `O(n)`：每个节点最多算一次；空间 `O(h)`：递归栈深度等于树高',
                 '完整二叉树只有 0 或 2 个孩子，所以只看 `root.left` 就能判断是不是叶子',
                 '`or` / `and` 会==短路==：OR 左边为真、AND 左边为假时，右子树直接跳过',
                 '叶子 `0/1` 与运算符 `2/3` 的取值互不重叠，不会混淆'],
    ),
)
