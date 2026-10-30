# ---- 树上“已返回”标注：caption 回调里记录每个节点的返回值，custom 叠加层（h=0）画在 tree 视图里的节点下方
TREE_H = 390
DONE = {}


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


def track(fn, key=None):
    def cap(S, B, ret):
        if key and S.get(key) is not None:
            DONE[S[key]._uid] = ret
        for n in _walk(S.get('self.tree')):
            n._d = DONE.get(n._uid)
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
        s = f'深度 {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def cap_left_if(S, B, ret):
    if S.now.left:
        return f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 递归求左子树深度'
    return f'`{S.now.val}` 没有左孩子 → ==不递归==，走 `else`'


def cap_right_if(S, B, ret):
    if S.now.right:
        return f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 递归求右子树深度'
    return f'`{S.now.val}` 没有右孩子 → ==不递归==，走 `else`'


def cap_ret(S, B, ret):
    return (f'节点 `{S.now.val}`：`max({S.left_depth}, {S.right_depth}) + 1 = {ret}`，'
            f'==较深的子树 + 当前这一层==')


CONFIG = dict(
    num=104, title='二叉树的最大深度', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='递归（只递归非空孩子）',
    code='''
class Solution(object):
    def maxDepth(self, root):
        return self.dfs(root)

    def dfs(self, now):
        if now is None:
            return 0

        if now.left:
            left_depth = self.dfs(now.left)
        else:
            left_depth = 0
        if now.right:
            right_depth = self.dfs(now.right)
        else:
            right_depth = 0

        return max(left_depth, right_depth) + 1
''',
    call='''s = Solution()
s.tree = Tr([3,9,20,None,None,15,7])
s.maxDepth(s.tree)''',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回深度）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=230),
    ],
    watch=[('now', 'now', 'blue'), ('left_depth', lambda S: S['_inner'].get('left_depth')), ('right_depth', lambda S: S['_inner'].get('right_depth'))],  # 只显示当前这层
    captions={
        'return self.dfs': track('`maxDepth` 只是入口：把根节点交给 `dfs(now)` 去算'),
        'if now is None': track(lambda S, B, ret: f'`now = {S.now.val}` 不为空（只有整棵树为空时这里才成立）'
                                if S.now is S['self.tree'] else f'`now = {S.now.val}` 非空 → 继续往下'),
        'if now.left': track(cap_left_if),
        'left_depth = self': track(lambda S, B, ret: f'进入 `dfs({S.now.val})`：它返回的就是左子树深度 `left_depth`'),
        'left_depth = 0': track('左子树为空 → `left_depth = 0`，==省掉一次空节点调用=='),
        'if now.right': track(cap_right_if),
        'right_depth = self': track(lambda S, B, ret: f'`left_depth = {B.left_depth}`；进入 `dfs({S.now.val})` 求右子树深度'),
        'right_depth = 0': track('右子树为空 → `right_depth = 0`'),
        'return max': track(cap_ret, key='now'),
    },
    cards=dict(
        one_liner='当前树的深度 = 较深的子树深度 + 当前这一层',
        complexity='时间 `O(n)`，空间 `O(h)`（`h` 为树高，递归栈）',
        problem=['给你二叉树的根 `root`，返回它的最大深度',
                 '最大深度 = 从根到最远叶子的路径上的 ==节点数==',
                 '示例：`root = [3,9,20,null,null,15,7]` → `3`'],
        quote='当前树的深度为左子树深度和右子树深度中==较深的那一个，再加上当前这一层==，因此可以递归求解左子树的深度left_depth与右子树的深度right_depth。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(now)` 返回以 `now` 为根的子树深度',
              '先看孩子在不在：==只对非空孩子递归==，空孩子深度直接记 `0`',
              '最后 `max(left_depth, right_depth) + 1` 交给上一层'],
        result='运行结束，返回 `3`：`3 → 20 → 15`（或 `7`）这条路径最长',
        summary=['时间 `O(n)`：每个节点进一次 `dfs`；空间 `O(h)`',
                 '`if now is None` 只在整棵树为空时生效，递归前已经判断过孩子',
                 '易错：两个分支都要给 `left_depth`/`right_depth` 赋值',
                 '原文为 Python 2 风格，仅删去 docstring 和定义注释，其余照搬'],
    ),
)
