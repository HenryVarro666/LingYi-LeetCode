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
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, T['green'], anchor='mm', bold=True)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.now is None:
        return '`now` 为空 → 递归边界'
    return f'`now = {S.now.val}` 非空 → 先求左右子树的最长路径'


def cap_l(S, B, ret):
    if S.now is None:
        return f'`{B.now.val}` 没有左孩子 → `dfs(None)` 会返回 `0`'
    return f'递归左孩子 `dfs({S.now.val})`：得到==到达左孩子的最长路径== `left_depth`（按节点数）'


def cap_r(S, B, ret):
    if S.now is None:
        return f'`left_depth = {B.left_depth}`；`{B.now.val}` 没有右孩子 → `right_depth` 为 `0`'
    return f'`left_depth = {B.left_depth}`；再递归右孩子 `dfs({S.now.val})` 得到 `right_depth`'


def cap_res(S, B, ret):
    s = S.left_depth + S.right_depth + 1
    tail = '，==刷新答案==' if S['self.res'] > B['self.res'] else ''
    return (f'经过 `{S.now.val}` 的最长路径：`{S.left_depth} + {S.right_depth} + 1 = {s}` 个节点，'
            f'`res = {S["self.res"]}`{tail}')


def cap_ret(S, B, ret):
    return f'返回到达 `{S.now.val}` 的最长路径：`max({S.left_depth}, {S.right_depth}) + 1 = {ret}`'


CONFIG = dict(
    num=543, title='二叉树的直径', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='递归 · 子树根 + 左右最长路径',
    code='''
class Solution(object):
    def diameterOfBinaryTree(self, root):
        self.res = 1

        self.dfs(root)
        return self.res - 1

    def dfs(self, now):
        if not now:
            return 0

        left_depth = self.dfs(now.left)
        right_depth = self.dfs(now.right)
        self.res = max(self.res, left_depth + right_depth + 1)
        return max(left_depth, right_depth) + 1
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,5])
s.diameterOfBinaryTree(s.tree)''',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回深度，按节点数）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=230),
    ],
    watch=[('now', 'now', 'blue'), ('left_depth', lambda S: S['_inner'].get('left_depth')), ('right_depth', lambda S: S['_inner'].get('right_depth')), ('res', 'self.res', 'green')],
    captions={
        'self.res = 1': track('`self.res` 记录最长路径的==节点数==，至少有根这 1 个节点'),
        'self.dfs(root)': track('从根开始 `dfs`：每个节点都当一次“子树的根”'),
        'if not now': track(cap_if),
        'return 0': track('空子树 → 返回 `0`'),
        'left_depth = self': track(cap_l),
        'right_depth = self': track(cap_r),
        'self.res = max': track(cap_res),
        'return max': track(cap_ret, key='now'),
        'return self.res': track(lambda S, B, ret: f'`res` 数的是节点，直径数的是边：所以==减 1==：返回 `{S["self.res"]} - 1 = {ret}`'),
    },
    cards=dict(
        one_liner='直径 = 某棵子树的根 + 左边最长路径 + 右边最长路径',
        complexity='时间 `O(n)`，空间 `O(h)`（`h` 为树高）',
        problem=['二叉树的直径：任意两个节点之间==最长路径的边数==',
                 '这条路径可能经过也可能不经过根节点',
                 '示例：`root = [1,2,3,4,5]` → `3`（路径 `4-2-1-3`）'],
        quote='树的直径必然是由==某棵子树的根节点==，加上其左子树中到达左孩子的最长路径，再加上右子树中到达右孩子的最长路径组成。',
        quote_src='—— yiduobo 题解',
        idea=['常规做法是两趟 dfs，但这里==从儿子回不到父亲==，要另想办法',
              '`dfs(now)` 返回到达 `now` 的最长路径（按==节点数==）',
              '经过 `now` 的路径节点数 = 左 + 右 + 1，用它更新 `res`'],
        result='运行结束，返回 `3`：最长路径 `4-2-1-3` 有 4 个节点、3 条边',
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：`res` 按节点数统计，最后要 `- 1` 才是边数',
                 '`res` 初始为 `1`（单个节点），保证答案至少为 `0`',
                 '原文为 Python 2 风格，仅删去 docstring 和定义注释，其余照搬'],
    ),
)
