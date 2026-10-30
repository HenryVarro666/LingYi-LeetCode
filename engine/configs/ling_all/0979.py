# 树上标注：每个节点 dfs 返回的 d（流出 > 0 / 流入 < 0），画在节点下方
TREE_H = 380
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


def track(fn, record=False):
    def cap(S, B, ret):
        if record and S.node is not None:
            DONE[S.node._uid] = ret
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
        s = f'd={d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def _nv(x):
    return '空' if x is None else str(x.val)


def cap_none(S, B, ret):
    return '空节点：没有硬币也没有节点，净流出 `0`，==递归边界=='


CONFIG = dict(
    num=979, title='在二叉树中分配硬币', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='贡献法 · 自底向上 DFS',
    tags=['贪心与思维', '链表树与回溯', '难度分 1709'],
    code='''
class Solution:
    def distributeCoins(self, root: Optional[TreeNode]) -> int:
        ans = 0
        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            d = dfs(node.left) + dfs(node.right) + node.val - 1
            nonlocal ans
            ans += abs(d)
            return d
        dfs(root)
        return ans
''',
    call='''s = Solution()
s.tree = Tr([1,0,0,None,3])
s.distributeCoins(s.tree)''',
    expect=4,
    views=[
        dict(type='tree', label='二叉树（绿 = 已算出 d，d = 子树硬币数 − 节点数）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=220),
    ],
    watch=[('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') is not None else '空', 'blue'),
           ('d', lambda S: S['_inner'].get('d'), 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计所有「边」上要搬运的硬币数',
        'if node is None': lambda S, B, r: '空节点 → 直接返回 `0`' if S.node is None else f'节点 `{S.node.val}` 不为空，继续算它的 `d`',
        'return 0': track(cap_none),
        'd = dfs': track('先递归左右子树拿到它们的 `d`，再用 `d = d左 + d右 + node.val − 1` 算自己'),
        'ans += abs(d)': track(lambda S, B, r: f'节点 `{S.node.val}` 的 `d` = =={S.d}==：' + (f'子树多 `{S.d}` 枚，要往上送' if S.d > 0 else f'子树缺 `{-S.d}` 枚，要从上面运进来' if S.d < 0 else '刚好够用') + f'；这条边过 `{abs(S.d)}` 枚 → `ans = {B.ans} + {abs(S.d)}` = =={S.ans}=='),
        'return d': track(lambda S, B, r: f'把 `d = {S.d}` 交给父亲：它会并入父亲的 `d`', record=True),
        'dfs(root)': '从根开始递归；根的 `d` 一定是 0（硬币总数 = 节点总数）',
        'return ans': '每条边的贡献加起来：最少移动 `{ans}` 次',
    },
    skip=['nonlocal ans'],
    cards=dict(
        one_liner='不看每枚硬币怎么走，只数每条边要过几枚',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['二叉树每个节点有 `val` 枚硬币，总数恰好等于节点数 `n`',
                 '一次移动：把一枚硬币移到相邻（父/子）节点',
                 '求让每个节点恰好 1 枚的最少移动次数',
                 '示例：`[3,0,0]` → `2`；本视频：`[1,0,0,null,3]` → `4`'],
        quote='每枚硬币移动的路径长度并不好计算，但是把这些路径==叠起来==，转换成每条边经过了多少枚硬币，就容易计算了。',
        quote_src='—— 灵茶山艾府题解答疑「这种思路的本质」',
        idea=['子树里 `coins` 枚硬币、`nodes` 个节点，差 `d = coins − nodes`',
              '这条边上必须恰好流过 `|d|` 枚：多了往上送，少了从上拿',
              '化简得 `d = d左 + d右 + node.val − 1`，只用一个返回值（算法二）',
              '所有边的 `|d|` 相加就是答案，这就是==贡献法=='],
        result='运行结束，返回 `4`：各条边的 `|d|` 之和',
        summary=['时间 `O(n)`：每个节点递归一次；空间 `O(n)`：最坏退化成链',
                 '易错：`d` 带符号向上传（正负会互相抵消），只在累加答案时取绝对值',
                 '根节点 `d = 0`，无需特判',
                 '算法一：同时返回 `(coins, nodes)` 两个值，`ans += abs(coins - nodes)`，本视频讲的是优化后的算法二',
                 '同类：贡献法题目见灵神题单「贡献法」，如 2477 到达首都的最少油耗'],
    ),
)
