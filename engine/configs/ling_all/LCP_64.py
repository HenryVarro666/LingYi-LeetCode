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
        if record and S.get('now') is not None:
            DONE[S['now']._uid] = ret
        for n in _walk(S.get('root')):
            n._d = DONE.get(n._uid)
        if callable(fn):
            return fn(S, B, ret)
        return eval('f' + repr(fn), {'B': B, 'ret': ret}, dict(S))
    return cap


def _layout(root, box):
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
        s = FMT(d)
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def FMT(d):
    return str(d)


def _lit(S):
    n = S.node
    on = (n.val == 1) == (S.switch2 == S.switch3)
    return on


def _info(S):
    n = S.get('node')
    if n is None or 'switch2' not in S['_inner']:
        return '状态 = (当前节点，祖先开关 2 的奇偶性，父节点是否按了开关 3)'
    i = S['_inner']
    s2, s3 = i['switch2'], i['switch3']
    on = (n.val == 1) == (s2 == s3)
    return (f"节点 `{n.val}`｜`switch2 = {s2}`，`switch3 = {s3}` → 受影响后 ==" + ('亮着' if on else '已灭') + '==')


def _cap_if(S, B, ret):
    n, s2, s3 = S.node, S.switch2, S.switch3
    on = (n.val == 1) == (s2 == s3)
    return (f'节点值 `{n.val}`；`switch2 = {s2}`，`switch3 = {s3}`' +
            ('，两者相同 → 不翻转，灯保持原样' if s2 == s3 else '，两者不同 → 翻转一次') +
            f'。当前灯 ==' + ('亮' if on else '灭') + '==')


def _op(name, what, effect, child, cost):
    def f(S, B, ret):
        i = S['_inner']
        if name in i:
            return f'{what}：{effect}，+{cost} 次 → `{name}` = ' + f'=={i[name]}=='
        return f'试「{what}」（+{cost} 次）：{effect}；儿子收到 {child}，先去算儿子'
    return f


CONFIG = dict(
    num='LCP 64', title='二叉树灯饰', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='树形 DP · 记忆化搜索',
    tags=['动态规划', '链表树与回溯'],
    code='''
class Solution:
    def closeLampInTree(self, root: TreeNode) -> int:
        @cache  # 记忆化搜索
        def dfs(node: TreeNode, switch2: bool, switch3: bool) -> int:
            if node is None:
                return 0
            if (node.val == 1) == (switch2 == switch3):  # 当前节点为开灯
                res1 = dfs(node.left, switch2, False) + dfs(node.right, switch2, False) + 1
                res2 = dfs(node.left, not switch2, False) + dfs(node.right, not switch2, False) + 1
                res3 = dfs(node.left, switch2, True) + dfs(node.right, switch2, True) + 1
                res123 = dfs(node.left, not switch2, True) + dfs(node.right, not switch2, True) + 3
                return min(res1, res2, res3, res123)
            else:  # 当前节点为关灯
                res0 = dfs(node.left, switch2, False) + dfs(node.right, switch2, False)
                res12 = dfs(node.left, not switch2, False) + dfs(node.right, not switch2, False) + 2
                res13 = dfs(node.left, switch2, True) + dfs(node.right, switch2, True) + 2
                res23 = dfs(node.left, not switch2, True) + dfs(node.right, not switch2, True) + 2
                return min(res0, res12, res13, res23)
        return dfs(root, False, False)
''',
    call='Solution().closeLampInTree(Tr([1,1]))',
    expect=1,
    views=[
        dict(type='text', fn=_info, size=24, h=56),
        dict(type='tree', var='root', label='二叉树（1 = 开灯，蓝 = node）', pointers={'node': 'blue'}, h=300,
             color=lambda S, n: 'yellow' if n.val == 1 else None),
        dict(type='calls', h=250, hide=('root',)),
    ],
    watch=[('node', 'node.val', 'blue'), ('switch2', lambda S: S['_inner'].get('switch2'), 'cyan'),
           ('switch3', lambda S: S['_inner'].get('switch3'), 'pink')],
    captions={
        'if (node.val == 1) == (switch2 == switch3)': _cap_if,
        'res1 =': _op('res1', '只拨开关 1', '翻自己，子树不受影响', '`switch2` 不变，`switch3 = False`', 1),
        'res2 =': _op('res2', '拨开关 2', '整棵子树翻转', '`switch2` 取反，`switch3 = False`', 1),
        'res3 =': _op('res3', '拨开关 3', '自己和两个儿子各翻一次', '`switch2` 不变，`switch3 = True`', 1),
        'res123 =': _op('res123', '三个开关全拨', '自己被翻 3 次，相当于 1 次；子树翻转 + 儿子再翻', '`switch2` 取反，`switch3 = True`', 3),
        'res0 =': _op('res0', '什么都不拨', '灯已经灭了', '`switch2` 不变，`switch3 = False`', 0),
        'res12 =': _op('res12', '拨开关 1、2', '自己翻两次抵消，子树整体翻转', '`switch2` 取反，`switch3 = False`', 2),
        'res13 =': _op('res13', '拨开关 1、3', '自己翻两次抵消，儿子各翻一次', '`switch2` 不变，`switch3 = True`', 2),
        'res23 =': _op('res23', '拨开关 2、3', '自己翻两次抵消，子树翻转，儿子再翻', '`switch2` 取反，`switch3 = True`', 2),
        'return min(res1': '亮着：四种拨法取最小 `min({res1}, {res2}, {res3}, {res123}) = =={ret}==`',
        'return min(res0': '已灭：四种拨法取最小 `min({res0}, {res12}, {res13}, {res23}) = =={ret}==`',
        'return dfs(root': lambda S, B, ret: ('从根出发 `dfs(root, False, False)`：祖先什么都没拨' if ret is None else f'整棵树最少 ==`{ret}`== 次操作'),
    },
    skip=['if node is None', 'return 0', '@cache'],
    max_steps=80,
    cards=dict(
        one_liner='状态 = (节点，祖先开关 2 奇偶，父开关 3)，四种拨法取最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树每个节点有一盏灯和三个开关',
                 '开关 1 翻自己；开关 2 翻整棵子树；开关 3 翻自己和左右儿子',
                 '求最少操作几次让所有灯都关闭',
                 '示例：`[1,1,0,null,null,null,1]` → `2`；下面演示更小的 `[1,1]` → `1`'],
        quote='定义状态 (当前节点，祖先节点开关 2 的切换次数的奇偶性，父节点是否切换了开关 3)，每个状态表示从当前状态出发，最少需要操作多少次开关，可以关闭子树所有节点的灯。',
        quote_src='—— 灵茶山艾府题解',
        idea=['当前灯的真实状态 = 原值 ⊕ 开关 2 奇偶 ⊕ 开关 3',
              '亮着：拨 1 / 2 / 3 / 123 四种；已灭：不拨 / 12 / 13 / 23 四种',
              '每种拨法决定传给儿子的 `switch2`、`switch3`，再 `@cache` 记忆化'],
        result='运行结束，返回 `1`：在根上拨一次开关 2，两盏灯一起关掉',
        summary=['时间 `O(n)`：状态数 `4n`，每个状态 `O(1)`；空间 `O(n)`',
                 '易错：开关 1 不影响儿子，所以拨不拨 1 只看自己是否亮着',
                 '易错：同一个开关拨两次等于没拨，所以每个开关最多拨一次',
                 '`switch3` 只管下一层：传给儿子时要重置为 `False` 或 `True`'],
    ),
)
