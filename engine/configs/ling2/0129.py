# ---- 树上标注：caption 回调里记录每个节点算出的 x，custom 叠加层（h=0）画在 tree 视图里节点的下方
TREE_H = 360
XS = {}      # uid -> 走到该节点时的 x
ADDED = set()  # 已经把 x 加进 ans 的叶子


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


def track(fn):
    def cap(S, B, ret):
        if S.get('_line') == 7 and S.get('node') is not None:
            XS[S.node._uid] = S.x
        if S.get('_line') == 10 and S.get('node') is not None:
            ADDED.add(S.node._uid)
        for n in _walk(S.get('root')):
            n._x = XS.get(n._uid)
            n._done = n._uid in ADDED
        if callable(fn):
            return fn(S, B, ret)
        env = dict(S)
        env.update(B=B, ret=ret)
        return eval('f' + repr(fn), {}, env)
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
        x = getattr(n, '_x', None)
        if x is None:
            continue
        X, Y = pos[n._uid]
        s = f'x={x}'
        c = T['green'] if getattr(n, '_done', False) else T['cyan']
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, c, anchor='mm', bold=True)


def _formula(S, B):
    if S.get('_line') == 7:
        return f'`x = {B["x"]} × 10 + {S["node"].val}` = =={S["x"]}=='
    if S.get('_line') == 10:
        return f'叶子：`ans += {S["x"]}` → `ans` = =={S["ans"]}=='
    return '往下走一层：`x = x × 10 + node.val`，到叶子时把 `x` 加进答案'


def nv(x):
    return 'None' if x is None else str(x.val)


def cap_none(S, B, ret):
    if S.node is None:
        return '`node` 是空节点 → 这里没有路径，==直接返回=='
    return f'`node = {S.node.val}` 不是空节点，继续'


def cap_leaf(S, B, ret):
    n = S.node
    if n.left is None and n.right is None:
        return f'`{n.val}` 没有儿子 → 是==叶子==：一条根到叶子的路径走完了，数字就是 `{S.x}`'
    return f'`{n.val}` 不是叶子 → 把 `x = {S.x}` 继续往下传'


CONFIG = dict(
    num=129, title='求根节点到叶节点数字之和', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='DFS · 自顶向下传 x',
    tags=['热题173', '面试经典150'],
    code='''
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        ans = 0
        def dfs(node: Optional[TreeNode], x: int) -> None:
            if node is None:
                return
            x = x * 10 + node.val
            if node.left is None and node.right is None:  # node 是叶子节点
                nonlocal ans
                ans += x
                return
            dfs(node.left, x)
            dfs(node.right, x)
        dfs(root, 0)
        return ans
''',
    call='Solution().sumNumbers(Tr([4,9,0,None,1]))',
    expect=531,
    views=[
        dict(type='text', fn=_formula),
        dict(type='tree', label='二叉树（青 = 走到这里时的 x，绿 = 已加进 ans 的叶子）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_done', False) else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=200),
    ],
    watch=[('node', 'node', 'blue'), ('x', lambda S: S['_inner'].get('x'), 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': track('`ans` 累加所有根到叶子的数字'),
        'if node is None': track(cap_none),
        6: track('空节点不产生数字，返回上一层'),
        'x = x * 10': track('数字往下“长”一位：`x = {B.x} × 10 + {node.val} = {x}`'),
        'if node.left is None': track(cap_leaf),
        'ans += x': track('把这条路径的数字加进答案：`ans = {B.ans} + {x} = {ans}`'),
        11: track('叶子处理完，返回'),
        'dfs(node.left': track(lambda S, B, ret: f'递归左子树 `{nv(S.node)}`，把 `x = {B.x}` 传下去'),
        'dfs(node.right': track(lambda S, B, ret: f'左边算完；递归右子树 `{nv(S.node)}`，同样带着 `x = {B.x}`'),
        'dfs(root, 0)': track('从根出发，初始 `x = 0`'),
        'return ans': track('所有叶子都加过了：返回 `ans = {ans}`'),
    },
    cards=dict(
        one_liner='把 x 当参数往下传：每走一层 x = x·10 + val，到叶子就加进答案',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['二叉树每个节点是 `0~9`，每条==根到叶子==的路径代表一个数字',
                 '例如 `1 → 2 → 3` 表示 `123`，求所有这些数字之和',
                 '示例：`[4,9,0,5,1]` → `495 + 491 + 40 = 1026`',
                 '本视频：`[4,9,0,null,1]` → `491 + 40 = 531`'],
        quote='当我们递归到叶子节点时，把 x 加到答案中。为了实现上述算法，把 x 作为 DFS 的参数，并在 DFS 中按照 x = x·10 + node.val 去更新 x。',
        quote_src='—— 灵茶山艾府题解（写法一：没有返回值）',
        idea=['路径 `4 → 9 → 1`：`x` 依次是 `4`、`49`、`491`，==数字随深度一位位长出来==',
              '`x` 是参数，每层有自己的一份：回到上一层时 `x` ==自动恢复==，不用手动撤销',
              '叶子 = 左右儿子都为空；空节点直接返回'],
        summary=['时间 `O(n)`；空间 `O(n)`：最坏退化成链',
                 '易错：只在==叶子==处累加，不能在空节点处累加（会把一条路径加两次）',
                 '写法一用 `nonlocal ans` 修改外层变量',
                 '写法二：把和放进返回值，`return f(left, x) + f(right, x)`'],
    ),
)
