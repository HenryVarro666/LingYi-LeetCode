VALS = [1, 2, 3, 4, 5, None, 6, 7]
TREE_H = 390


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


def _md(n):
    if n.left is None and n.right is None:
        return 1
    if n.left is None:
        return _md(n.right) + 1
    if n.right is None:
        return _md(n.left) + 1
    return min(_md(n.left), _md(n.right)) + 1


def _path(root, target):
    """根到 target 的路径（DFS 中仍在调用栈里的节点）"""
    if root is None:
        return None
    if root is target:
        return [root]
    for ch in (root.left, root.right):
        p = _path(ch, target)
        if p:
            return [root] + p
    return None


def _how(n):
    if n.left is None and n.right is None:
        return f'`{n.val}` 返回 1'
    if n.left is None:
        return f'`{n.val}` 返回 `{_md(n.right)} + 1 = {_md(n)}`'
    if n.right is None:
        return f'`{n.val}` 返回 `{_md(n.left)} + 1 = {_md(n)}`'
    return f'`{n.val}` 返回 `min({_md(n.left)}, {_md(n.right)}) + 1 = {_md(n)}`'


VIS, PREV = set(), set()


def track(fn, leaf=False):
    """已返回 = 访问过且不在当前调用栈上；把子树最小深度标到这一步的快照上，并在字幕前补一句谁刚返回"""
    def cap(S, B, ret):
        root, now = S.get('root'), S['_inner'].get('now')
        if root is None:
            return fn(S, B, ret) if callable(fn) else fn
        nodes = _walk(root)
        if now is not None:
            VIS.add(now._uid)
        stack = {n._uid for n in (_path(root, now) or [])} if now is not None else set()
        if leaf and now is not None:
            stack.discard(now._uid)
        done = VIS - stack
        new = [n for n in nodes if n._uid in done and n._uid not in PREV and not (leaf and n is now)]
        PREV.update(done)
        for n in nodes:
            n._d = _md(n) if n._uid in done else None
        text = fn(S, B, ret) if callable(fn) else fn
        if new:
            text = '、'.join(_how(n) for n in new) + '；' + text
        return text
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
    root = S.get('root')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'= {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def _v(x):
    return '空' if x is None else str(x.val)


def _nl(S, B, ret):
    n = S.now
    if n.left is None:
        return f'`{n.val}` ==没有左孩子==，再看右孩子'
    return f'`{n.val}` 有左孩子 `{n.left.val}`，再看右孩子'


def _nr(S, B, ret):
    n = S.now
    if n.left is None and n.right is None:
        return f'`{n.val}` 左右都为空 → 它是叶子'
    if n.left is None:
        return f'`{n.val}` 只有右孩子 `{n.right.val}` → 答案只能来自右边'
    if n.right is None:
        return f'`{n.val}` 只有左孩子 `{n.left.val}` → 答案只能来自左边，==不能拿空的右边取 min=='
    return f'`{n.val}` 左右孩子都有 → 两边取较小的'


CONFIG = dict(
    num=111, title='二叉树的最小深度', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='自底向上递归 · 分类讨论空子树',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution(object):
    def minDepth(self, root):

        return self.dfs(root)

    def dfs(self, now):
        if not now:
            return 0

        if not now.left:
            if not now.right:
                return 1
            else:
                return self.dfs(now.right) + 1
        else:
            if not now.right:
                return self.dfs(now.left) + 1
            else:
                return min(self.dfs(now.left), self.dfs(now.right)) + 1
''',
    call=f'Solution().minDepth(Tr({VALS}))',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（绿 = 已求出子树最小深度）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=240),
    ],
    watch=[('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue')],
    captions={
        'return self.dfs(root)': track('答案就是整棵树的 `dfs(root)`：以 now 为根的子树的最小深度'),
        'if not now:': track(lambda S, B, r: '空节点 → 深度 0' if S.now is None else f'来到节点 `{S.now.val}`'),
        'return 0': track('空树返回 `0`'),
        'if not now.left:': track(_nl),
        'if not now.right:': track(_nr),
        'return 1': track(lambda S, B, r: f'叶子 `{S.now.val}` 的最小深度是 ==1==，返回', leaf=True),
        'return self.dfs(now.right) + 1': track(
            lambda S, B, r: f'递归右子树 `{S.now.val}`，它返回后 `+1` 就是 `{B.now.val}` 的答案'),
        'return self.dfs(now.left) + 1': track(
            lambda S, B, r: f'递归左子树 `{S.now.val}`，它返回后 `+1` 就是 `{B.now.val}` 的答案'),
        'return min(': track(
            lambda S, B, r: f'先递归左子树 `{S.now.val}`，再递归右子树 `{B.now.right.val}`，==取较小的再 +1=='),
    },
    cards=dict(
        one_liner='先求左右子树最小深度，取小的加一；有一边为空就只看另一边',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链）',
        problem=['求二叉树的最小深度：根到==最近叶子==的路径上的节点数',
                 '叶子 = 没有子节点的节点',
                 '示例：`[3,9,20,null,null,15,7]` → `2`；本视频：`[1,2,3,4,5,null,6,7]` → `3`'],
        quote='做法与上一题类似，也是先递归求解左右子树的最小深度，然后取较小的那一边加一作为当前树的最小深度返回。==需要注意左右子树为空的情况==。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 104 最大深度一样自底向上，只是 `max` 换成 `min`',
              '但空子树深度是 0：直接取 `min` 会选到空的一侧',
              '所以按左右是否为空分 4 种情况：叶子返回 1，单侧只递归非空的那侧'],
        result='`3` 返回 `1 + 1 = 2`，根 `1` 返回 `min(2, 2) + 1 = 3`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：节点 `4` 只有左孩子，若直接 `min(左, 0) + 1` 会得到 1，错误',
                 '对比灵神：灵神主推自顶向下传 `cnt`，配合 `cnt ≥ ans` 剪枝',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
