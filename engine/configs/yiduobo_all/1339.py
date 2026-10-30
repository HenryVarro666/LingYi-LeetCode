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


def _rec(fn, record=False, var='now'):
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


TREE_H = 360


CONFIG = dict(
    num=1339, title='分裂二叉树的最大乘积', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 子树和 + 枚举',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1675'],
    code='''
class Solution(object):
    def maxProduct(self, root):

        weight_list = []
        self.dfs(root, weight_list)
        res = 0
        for weight in weight_list:
            res = max(res, (weight_list[-1] - weight) * weight)
        
        return res % (10 ** 9 + 7)
    
    def dfs(self, now, weight_list):
        weight = now.val
        if now.left:
            weight += self.dfs(now.left, weight_list)
        if now.right:
            weight += self.dfs(now.right, weight_list)
        
        weight_list.append(weight)
        return weight
''',
    call='''sol = Solution()
sol.tree = Tr([1,2,3,4,5,6])
sol.maxProduct(sol.tree)''',
    expect=110,
    views=[
        dict(type='tree', label='二叉树（绿 = 已算出子树和）', pointers={'now': 'blue'}, h=TREE_H, color=_sum_color),
        dict(type='custom', draw=_badges, h=0),
        dict(type='array', var='weight_list', label='weight_list（每个节点为根的子树和，后序）', cell=64, h=150),
        dict(type='calls', h=170, hide=('weight_list', 'sol', 'self')),
    ],
    watch=[('now', lambda S: S['_inner'].get('now').val if S['_inner'].get('now') else None, 'blue'),
           ('weight', lambda S: S['_inner'].get('weight')), ('res', 'res', 'green')],
    captions=_wrap({
        'weight_list = []': lambda S, B, r: DONE.clear() or '`weight_list` 收集「以每个节点为根的子树和」`f[x]`：==后序追加，根的和排在最后==',
        'self.dfs(root, weight_list)': '先从根 DFS 一遍，把所有 `f[x]` 算出来',
        'weight = now.val': '节点 `{now.val}`：子树和从自己的点权 `{weight}` 开始，再加左右子树的和',
        'weight += self.dfs(now.left': '节点 `{B.now.val}` 有左孩子 → 先递归求左子树和，回来后加到 `weight` 上',
        'weight += self.dfs(now.right': '节点 `{B.now.val}` 有右孩子 → 递归求右子树和，回来后加到 `weight` 上',
        'weight_list.append': '节点 `{now.val}` 的子树和 `{weight}` 记入列表 `{weight_list}`',
        'return weight': _rec(lambda S, B, r: f'把 `{r}` 返回给父节点去累加', True, 'now'),
        'res = 0': '开始枚举：删掉 `x` 与父亲的边，两块的和是 `f[x]` 与 `f[root] - f[x]`',
        'for weight in': lambda S, B, r: f'枚举 `weight = {S.weight}`（某个节点 `x` 的 `f[x]`）' if S.weight != B.get('weight') or B.get('res') == 0 and S.res == 0 else '所有 `f[x]` 都枚举完了，循环结束',
        'res = max': lambda S, B, r: f'`({S.weight_list[-1]} - {S.weight}) * {S.weight}` = {(S.weight_list[-1] - S.weight) * S.weight}，`res = max({B.res}, ...)` = =={S.res}==',
        'return res %': '结果对 `10^9 + 7` 取模：`{res} % (10 ** 9 + 7)` = =={ret}==',
    }),
    skip=['if now.left', 'if now.right'],
    max_steps=90,
    cards=dict(
        one_liner='先求出每个节点为根的子树和 `f[x]`，再枚举 `f[x] * (f[root] - f[x])`',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你一棵二叉树，删除 `1` 条边把它分成两棵子树',
                 '求两棵子树点权和乘积的最大值，结果对 `10^9 + 7` 取模',
                 '本视频：`root = [1,2,3,4,5,6]` → `110`',
                 '删掉 `1-2` 这条边：和分别为 `11` 与 `10`'],
        quote='设删除的边连接的孩子节点为x，那么新的两棵树的节点权重之和分别是以x为根节点的子树的节点和，以及除了以x为根节点的子树之外的其他节点和。',
        quote_src='—— yiduobo 题解',
        idea=['删掉的边连着孩子 `x`：一块是 `x` 的子树（和 `f[x]`），另一块是其余部分（和 `f[root] - f[x]`）',
              '`dfs(now)` 先递归左右孩子，`f[now] = 左 + 右 + now.val`，并追加进 `weight_list`',
              '后序追加 ==⇒ 最后一个元素就是根的和==，所以直接用 `weight_list[-1]` 当总和'],
        result='`weight_list = [4, 5, 11, 6, 9, 21]`，最大乘积 `11 * 10 = 110`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '对比灵神：灵神用 `total` 变量接 `dfs` 的返回值；这里利用后序把根的和放在列表末尾',
                 '枚举到根时 `f[root] - f[root] = 0`，不影响最大值',
                 '易错：先取最大再取模；原文已是 Python 3 可运行写法，无需改动'],
    ),
)
