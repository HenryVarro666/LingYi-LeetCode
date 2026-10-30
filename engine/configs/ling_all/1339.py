import re as _re

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


def _rec(fn, record=False, var='node'):
    def cap(S, B, ret):
        n = S.get(var)
        if record and n is not None:
            DONE[n._uid] = ret
        for m in _walk(S.get('self.tree')):
            m._d = DONE.get(m._uid)
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _fmt(t):
    def f(S, B, r):
        env = {'B': B, 'ret': r, 'sorted': sorted, 'len': len, 'max': max, 'min': min}
        return _re.sub(r'\{([^{}]+)\}', lambda m: str(eval(m.group(1), env, S)), t)
    return f


def _wrap(d):
    return {k: _rec(v if callable(v) else _fmt(v)) for k, v in d.items()}


def _sum_color(S, n):
    return 'green' if getattr(n, '_d', None) is not None else None


def _badges(cv, S, B, box, T):
    root = S.get('self.tree')
    if root is None:
        return
    x0, y0, x1, y1 = box[0], box[1] - TREE_H, box[2], box[1]
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
    for i, n in enumerate(order):
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = sx + i * sp, y0 + 60 + depth[n._uid] * dy + rad
        s = '和 %d' % d
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


TREE_H = 330


def _info(S):
    ss = S.get('sub_sum')
    if not ss:
        return ''
    t = S.get('total')
    if t is None:
        return f'已算出的子树和 `sub_sum = {ss}`'
    return f'整棵树和 `total = {t}`，删掉某条边后两块的和是 `s` 与 `{t} - s`'


CONFIG = dict(
    num=1339, title='分裂二叉树的最大乘积', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='后序 DFS 求子树和',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1675'],
    code='''
class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            s = node.val + dfs(node.left) + dfs(node.right)
            sub_sum.append(s)
            return s

        sub_sum = []
        total = dfs(root)

        ans = max(s * (total - s) for s in sub_sum)
        return ans % 1_000_000_007
''',
    call='''sol = Solution()
sol.tree = Tr([1,2,3,4,5,6])
sol.maxProduct(sol.tree)''',
    expect=110,
    setup='',
    views=[
        dict(type='tree', label='二叉树（绿 = 已算出子树和）', pointers={'node': 'blue'}, h=TREE_H, color=_sum_color),
        dict(type='custom', draw=_badges, h=0),
        dict(type='array', var='sub_sum', label='sub_sum（后序收集的子树和）', cell=64, h=122),
        dict(type='text', fn=_info, size=24, h=44),
        dict(type='calls', h=138, hide=('sub_sum', 'sol')),
    ],
    watch=[('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') else None, 'blue'),
           ('s', lambda S: S['_inner'].get('s')), ('total', 'total', 'yellow'), ('ans', 'ans', 'green')],
    captions=_wrap({
        'sub_sum = []': lambda S, B, r: DONE.clear() or '`sub_sum` 记下每棵子树的点权和：==删掉它与父节点的边==，这棵子树就被分出去了',
        'total = dfs': '开始 DFS：后序遍历，==先算左右子树的和，再算自己的==',
        'if node is None': lambda S, B, r: '空节点' if S.node is None else f'节点 `{S.node.val}` 非空 → 子树和等于自己 + 左 + 右',
        'return 0': '空子树点权和为 `0`',
        's = node.val': lambda S, B, r: '递归到空节点 → 没有点权，马上返回 `0`' if S.node is None else f'节点 `{S.node.val}` 非空 → 先递归左右子树，==回来后== 再加上自己：`s = {S.node.val} + 左 + 右`',
        'sub_sum.append': '`s = {s}` 存入 `sub_sum`：删掉 `{node.val}` 与父亲的边，这一块的和就是 `{s}`',
        'return s': _rec(lambda S, B, r: f'把 `{r}` 返回给父节点，父节点用它累加自己的和', True, 'node'),
        'ans = max': lambda S, B, r: (lambda best: f'`total = {S.total}`，枚举每个 `s` 算 `s * (total - s)`：最大是 `{best} * {S.total - best}` = =={S.ans}==')(max(S.sub_sum, key=lambda x: x * (S.total - x))),
        'return ans %': '答案要对 `10^9 + 7` 取模：`{ans} % 1_000_000_007` = =={ret}==',
    }),
    skip=['if node is None'],
    max_steps=90,
    cards=dict(
        one_liner='删掉一条边，等价于选一棵子树：两块的和是 `s` 与 `total - s`',
        complexity='时间 `O(n)`，空间 `O(n)`（`sub_sum` 列表）；两次 DFS 版空间 `O(h)`',
        problem=['给你一棵二叉树，删除 `1` 条边把它分成两棵子树',
                 '求两棵子树点权和乘积的最大值，结果对 `10^9 + 7` 取模',
                 '本视频：`root = [1,2,3,4,5,6]` → `110`',
                 '删掉 `1-2` 这条边：和分别为 `11` 与 `10`，乘积 `110`'],
        quote='删除当前节点到其父节点的边后，另一部分的和就是 total - s，二者乘积为 s·(total - s)，用其更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs` 返回子树点权和，顺手把每个 `s` 存进 `sub_sum`；根节点那次返回的就是 `total`',
              '删边 = 选一棵子树：它的和是 `s`，剩下的是 `total - s`',
              '枚举所有 `s` 取乘积最大，最后再取模（==先比大小再取模==）'],
        result='`sub_sum` 里 `11` 最合适：`11 * (21 - 11) = 110`，返回 `110`',
        summary=['时间 `O(n)`，空间 `O(n)`；也可以写成两次 DFS（先求 total，再边算边更新），空间 `O(h)`',
                 '点权非负，所以根节点（`s = total`）的乘积是 `0`，不用特判',
                 '易错：==不能先取模再比大小==，Python 整数不会溢出，最后取一次模即可',
                 '同类题：「§2.3 自底向上 DFS」，如 543、124、2265'],
    ),
)
