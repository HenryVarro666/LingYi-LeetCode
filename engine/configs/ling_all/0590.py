VALS = [1, None, 3, 2, 4, None, 5, 6]

SETUP = '''
def NT(vals):
    """按 LeetCode 的 N 叉树层序序列化建树（每组孩子以 null 分隔）"""
    if not vals:
        return None
    root = TreeNode(vals[0])
    root.children = []
    q = deque([root])
    i = 2
    while q and i <= len(vals):
        nd = q.popleft()
        while i < len(vals) and vals[i] is not None:
            c = TreeNode(vals[i])
            c.children = []
            nd.children.append(c)
            q.append(c)
            i += 1
        i += 1
    return root
'''
SETUP += f'root = NT({VALS})\n'


def _layout(root):
    """叶子从左到右等距，父节点居中于孩子之上"""
    pos, depth, leaves = {}, {}, [0]

    def go(n, d):
        depth[n._uid] = d
        if not n.children:
            pos[n._uid] = leaves[0]
            leaves[0] += 1
        else:
            for c in n.children:
                go(c, d + 1)
            pos[n._uid] = sum(pos[c._uid] for c in n.children) / len(n.children)
    go(root, 0)
    return pos, depth, leaves[0]


def _all(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        out.append(n)
        st += n.children[::-1]
    return out


def _anc(root, target):
    """root 到 target 的路径（DFS 时仍在递归栈里的节点）"""
    if root is None or target is None:
        return []
    if root._uid == target._uid:
        return [root]
    for c in root.children:
        p = _anc(c, target)
        if p:
            return [root] + p
    return []


def _nary(cv, S, box, T, title, fill_fn, ptrs=(), ring=(), legend=''):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    if legend:
        cv.text((x1 - 20, y0 + 6), legend, 18, T['dim'], anchor='ra')
    root = S.get('root')
    if root is None:
        return
    pos, depth, nl = _layout(root)
    D = max(depth.values()) + 1
    sp = min(150, (x1 - x0 - 80) / max(1, nl))
    dy = min(130, (y1 - y0 - 100) / max(1, D))
    R = 28
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * nl) / 2 + sp / 2

    def P(n):
        return sx + pos[n._uid] * sp, y0 + 80 + depth[n._uid] * dy

    nodes = _all(root)
    for n in nodes:
        X, Y = P(n)
        for c in n.children:
            X2, Y2 = P(c)
            cv.line([(X, Y), (X2, Y2)], T['border'], 3)
    ring = {getattr(n, '_uid', None) for n in ring}
    hit = {}
    for name, v, c in ptrs:
        if v is not None and getattr(v, '_uid', None) in pos:
            hit.setdefault(v._uid, []).append((name, T[c]))
    for n in nodes:
        X, Y = P(n)
        c = fill_fn(n)
        hs = hit.get(n._uid, [])
        fill = T[c] if c else T['panel2']
        outline = hs[0][1] if hs else (T['yellow'] if n._uid in ring else T['border'])
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=fill, outline=outline, width=5 if (hs or n._uid in ring) else 2)
        cv.text((X, Y), n.val, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X + R + 4, Y + 4 + r * 22), name, 19, cc, anchor='lt', bold=True)


def _v(x):
    return None if x is None else getattr(x, 'val', x)



def _draw(cv, S, B, box, T):
    ans = S.get('ans') or []
    node = S['_inner'].get('node')
    _nary(cv, S, box, T, 'N 叉树（绿 = 已加入 ans，黄圈 = 递归路径）',
          lambda n: 'green' if n.val in ans else None,
          ptrs=(('node', node, 'blue'),), ring=_anc(S.get('root'), node))


def _if(S, B, ret):
    n = S.node
    if n is None:
        return '空节点 → 返回'
    if n.children:
        return f'来到节点 `{n.val}`：它有 {len(n.children)} 个孩子 `{[c.val for c in n.children]}`，==先依次递归它们=='
    return f'来到节点 `{n.val}`：没有孩子'


def _for(S, B, ret):
    i = S['_inner']
    n, c = i.get('node'), i.get('c')
    bc = B['_inner'].get('c')
    if c is None or (bc is not None and bc._uid == c._uid):
        return f'`{n.val}` 的孩子都递归完了' if n.children else f'`{n.val}.children` 为空，循环一次也不执行'
    k = [x._uid for x in n.children].index(c._uid)
    return f'`{n.val}` 的第 {k + 1} 个孩子 `c = {c.val}`'


def _app(S, B, ret):
    n = S.node
    if n.children:
        return f'`{n.val}` 的所有子树都访问完了，==最后才访问根== → `ans = {S.ans}`'
    return f'`{n.val}` 是叶子，没有子树 → 直接访问：`ans = {S.ans}`'


CONFIG = dict(
    num=590, title='N 叉树的后序遍历', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='递归 DFS · 先孩子后根',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def postorder(self, root: 'Node') -> List[int]:
        ans = []
        def dfs(node: 'Node') -> None:
            if node is None:
                return
            for c in node.children:
                dfs(c)
            ans.append(node.val)
        dfs(root)
        return ans
''',
    setup=SETUP,
    call='Solution().postorder(root)',
    expect=[5, 6, 3, 2, 4, 1],
    views=[
        dict(type='text', size=26, h=56, fn=lambda S: '后序：==子树 1 → 子树 2 → … → 子树 n → 根=='),
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='ans', label='ans（后序结果）', cell=80, h=120),
        dict(type='calls', h=230),
    ],
    watch=[('node', lambda S: _v(S['_inner'].get('node')), 'blue'), ('c', lambda S: _v(S['_inner'].get('c')))],
    captions={
        'ans = []': '`ans` 按后序收集节点值',
        'dfs(root)': '从根节点 `1` 开始递归',
        'if node is None': _if,
        'for c in node.children': _for,
        'dfs(c)': lambda S, B, r: f'递归子树 `{S.node.val}`：==整棵子树访问完==才轮到下一个孩子',
        'ans.append': _app,
        'return ans': '后序遍历结果 `{ret}`',
    },
    skip=[6],
    cards=dict(
        one_liner='先依次递归每个孩子，最后再访问根',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定 N 叉树的根 `root`，返回节点值的==后序遍历==',
                 '输入按层序序列化，每组孩子用 `null` 分隔',
                 '示例：`root = [1,null,3,2,4,null,5,6]` → `[5,6,3,2,4,1]`'],
        quote='对于二叉树来说，后序遍历的顺序为：递归左儿子 - 递归右儿子 - 根节点。推广到 N 叉树，顺序是==先依次递归其 children 数组中的节点（子树），再访问根节点==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['二叉树的「左、右」换成 `for c in node.children` 依次递归',
              '所有孩子递归完，再 `ans.append(node.val)`',
              '空节点直接返回（只有空树时会遇到）'],
        summary=['时间 `O(n)`：每个节点访问一次；空间 `O(n)`：递归栈 + 答案',
                 '后序 = 「根在最后」：append 写在循环之后',
                 '换成写在循环之前就是 589 前序遍历',
                 '进阶迭代写法：前序（孩子逆序）再整体反转'],
    ),
)
