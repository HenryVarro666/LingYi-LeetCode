TREE_H = 340
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


def _i(x):
    return '∞' if x == inf or x == 1001 else str(x)


def track(fn, record=False):
    def cap(S, B, ret):
        node = S.get('node') if S.get('node') is not None else S.get('now')
        if record and node is not None:
            DONE[node._uid] = ret
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
        s = '/'.join(_i(v) for v in d)
        w = cv.tlen(s, 20, bold=True, mono=True) + 14
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 33), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 19), s, 20, T['green'], anchor='mm', bold=True, mono=True)
def _info(S):
    n = S.get('node')
    base = '标注 ==选/被父/被子==：选 = 自己装；被父 = 靠父节点；被子 = 靠儿子'
    if n is None or 'l_choose' not in S['_inner']:
        return base
    return f"节点 `{n.val}`：左儿子 `{_i(S['l_choose'])}/{_i(S['l_by_fa'])}/{_i(S['l_by_children'])}`"


def cap_if(S, B, ret):
    if S.node is None:
        return '`node` 是空节点 → 递归边界'
    return f'节点 `{S.node.val}` 非空 → 先问左右儿子要三种状态'


def cap_l(S, B, ret):
    v = B.node.left
    if v is None:
        return f'节点 `{B.node.val}` 没有左儿子 → `dfs(None)` 直接返回边界值'
    return f'递归左儿子 `{v.val}`：==相信它返回的三个数是对的=='


def cap_r(S, B, ret):
    v = B.node.right
    lc = f"`{_i(B.l_choose)}/{_i(B.l_by_fa)}/{_i(B.l_by_children)}`"
    if v is None:
        return f'左儿子三元组 {lc} 已拿到；没有右儿子 → 右边用边界值'
    return f'左儿子三元组 {lc} 已拿到；再递归右儿子 `{v.val}`'


def cap_choose(S, B, ret):
    return (f'`choose` = `min({_i(S.l_choose)}, {_i(S.l_by_fa)})` + `min({_i(S.r_choose)}, {_i(S.r_by_fa)})` + 1 = =={_i(S.choose)}=='
            '：自己装，儿子装不装都行（装了也监控到儿子）')


def cap_fa(S, B, ret):
    return (f'`by_fa` = `min({_i(S.l_choose)}, {_i(S.l_by_children)})` + `min({_i(S.r_choose)}, {_i(S.r_by_children)})` = =={_i(S.by_fa)}==：'
            '自己不装、被父亲看着 → 儿子不能靠父亲，只能自己装或靠它的儿子')


def cap_ch(S, B, ret):
    if S.by_children >= 1001:
        return '`by_children` = ==∞==：自己不装、父亲也不装，又没有能装的儿子 → ==不可能=='
    return (f'`by_children` = =={_i(S.by_children)}==：自己不装、父亲也不装 → ==至少一个儿子要装==，'
            '三种搭配取最小')


def cap_ret(S, B, ret):
    n = S.node
    return f'节点 `{n.val}` 的三种状态：选 `{_i(ret[0])}`，被父 `{_i(ret[1])}`，被子 `{_i(ret[2])}`'


CONFIG = dict(
    num=968, title='监控二叉树', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树形 DP · 最小支配集',
    tags=['灵神题单·动态规划', '难度分 2124'],
    code='''
class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if node is None:
                return inf, 0, 0  # 空节点不能安装摄像头，也无需被监控到
            l_choose, l_by_fa, l_by_children = dfs(node.left)
            r_choose, r_by_fa, r_by_children = dfs(node.right)
            choose = min(l_choose, l_by_fa) + min(r_choose, r_by_fa) + 1
            by_fa = min(l_choose, l_by_children) + min(r_choose, r_by_children)
            by_children = min(l_choose + r_by_children, l_by_children + r_choose, l_choose + r_choose)
            return choose, by_fa, by_children

        choose, _, by_children = dfs(root)  # 根节点没有父节点
        return min(choose, by_children)
''',
    call='''s = Solution()
s.tree = Tr([1,2,None,3,4])
s.minCameraCover(s.tree)''',
    expect=1,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回 选/被父/被子 的值）', pointers={'node': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='calls', h=200),
    ],
    watch=[('node', lambda S: getattr(S.get('node'), 'val', None), 'blue'),
           ('choose', lambda S: S['_inner'].get('choose'), 'green'),
           ('by_fa', lambda S: S['_inner'].get('by_fa'), 'yellow'),
           ('by_children', lambda S: S['_inner'].get('by_children'), 'cyan')],
    max_steps=80,
    captions={
        'if node is None': track(cap_if),
        'return inf, 0, 0': track('空节点：不能装摄像头 → `choose = ∞`；不需要被监控 → `by_fa = by_children = 0`'),
        'dfs(node.left)': track(cap_l),
        'dfs(node.right)': track(cap_r),
        'choose = min(': track(cap_choose),
        'by_fa = min': track(cap_fa),
        'by_children = min': track(cap_ch),
        'return choose, by_fa': track(cap_ret, record=True),
        'choose, _, by_children = dfs(root)': track('从根开始 dfs：根没有父节点，返回的 `by_fa` 用不上（用 `_` 丢掉）'),
        'return min(choose': track(lambda S, B, r: f'根只能选自己装或靠儿子：`min({_i(S.choose)}, {_i(S.by_children)})` = =={r}=='),
    },
    cards=dict(
        one_liner='每个节点算三个数：自己装、靠父亲、靠儿子，最后取最小',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['在二叉树的节点上装摄像头，每个摄像头能监控==父节点、自己、直接儿子==',
                 '求监控所有节点所需的最少摄像头数',
                 '示例：`[0,0,null,0,0]` → `1`（装在第二层的节点）','视频里为了区分节点，把值改写成 `1,2,null,3,4`'],
        quote='学会树形 DP 后，可以用同样的方法解决这些变形题目。更一般的形式：==改成一般树，或给每个节点不同的 cost==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`choose`：当前节点装摄像头，儿子可装可不装',
              '`by_fa`：当前节点被父亲监控（自己不装）',
              '`by_children`：当前节点被儿子监控 → ==至少一个儿子装==',
              '空节点：`choose = ∞`、其余为 `0`，让边界自然成立'],
        summary=['每个节点只递归一次：时间 `O(n)`，空间 `O(n)`',
                 '空节点的 `choose` 取 `inf`：它不能装摄像头，也不能当「被儿子监控」的那个儿子',
                 '根没有父亲，所以答案是 `min(choose, by_children)`，不含 `by_fa`',
                 '推广：改成多叉树、加 `cost` 都只需改转移，这就是「最小支配集」模板'],
    ),
)
