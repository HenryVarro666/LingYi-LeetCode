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
    q = S.get('q') or []
    l, r = S.get('l', 0), S.get('r', 0)
    cur = {x._uid for x in q[l:r]}
    nxt = {x._uid for x in q[r:]}
    old = {x._uid for x in q[:l]}
    done = {v for row in (S.get('res') or []) for v in row}
    _nary(cv, S, box, T, 'N 叉树（绿 = 已记录，青 = 本层 q[l:r]，紫 = 已入队的下一层）',
          lambda n: 'green' if (n._uid in old or (n._uid in cur and n.val in done)) else
          ('cyan' if n._uid in cur else ('purple' if n._uid in nxt else None)),
          ptrs=(('now', S.get('now'), 'blue'),))


def _qv(S):
    return [x.val for x in S['q']] if 'q' in S else []


def _w(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：`q[{S.l}:{S.r}]` 是新的一层 `{_qv(S)[S.l:S.r]}`'
    return f'`l = r = {S.r}`：没有新入队的节点 → 结束'


def _for(S, B, ret):
    if S.get('index') is None:
        return ''
    if B.get('index') is not None and B['index'] == S['index']:
        return f'本层 `q[{S.l}:{S.r}]` 遍历完'
    return f'处理本层第 `index = {S.index}` 个节点'


def _cfor(S, B, ret):
    if not S.now.children:
        return f'`{S.now.val}` 没有孩子'
    bc = B.get('child')
    if bc is not None and bc._uid == S.child._uid:
        return f'`{S.now.val}` 的孩子都入队了'
    return f'取孩子 `child = {S.child.val}`'


def _child(S, B, ret):
    return f'孩子 `{S.child.val}` 追加到 `q` 末尾'


CONFIG = dict(
    num=429, title='N 叉树的层序遍历', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS · 数组 + 左右下标分层',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def levelOrder(self, root):

        if not root:
            return []

        q = [root]
        l = 0
        r = 1
        res = []
        while l < r:
            res.append([])
            newr = r
            for index in range(l, r):
                now = q[index]
                res[-1].append(now.val)
                for child in now.children:
                    q.append(child)
                    newr += 1
            l = r
            r = newr

        return res
''',
    setup=SETUP,
    call='Solution().levelOrder(root)',
    expect=[[1], [3, 2, 4], [5, 6]],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var=_qv, label='q（数组不出队，q[l:r] 是当前层）', cell=80, h=190,
             pointers={'l': 'blue', 'r': 'pink', 'index': 'yellow', 'newr': 'purple'},
             window=('l', lambda S: S['r'] - 1)),
        dict(type='text', size=26, h=56, fn=lambda S: f"`res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('newr', 'newr', 'purple'), ('now', lambda S: _v(S.get('now')))],
    captions={
        'if not root': '树非空',
        'q = [root]': '`q` 是普通数组，==节点只追加不删除==',
        'l = 0': '`[l, r)` 表示当前层在 `q` 中的范围',
        'r = 1': '第 0 层只有根：`q[0:1]`',
        'res = []': '`res` 按层收集结果',
        'while l < r': _w,
        'res.append([])': '为这一层开一个新列表',
        'newr = r': '`newr` 记录下一层的右边界，先等于 `r`，每入队一个孩子 `+1`',
        'for index in range': _for,
        'now = q[index]': '`now = q[{index}] = {now.val}`',
        'res[-1].append': '记录到当前层：`{res[-1]}`',
        'for child in now.children': _cfor,
        'q.append(child)': _child,
        'newr += 1': '下一层多了一个节点：`newr = {newr}`',
        'l = r': '这一层处理完：`l` 移到旧的 `r = {l}`',
        'r = newr': lambda S, B, r: (f'`r = newr = {S.r}`：==q[{S.l}:{S.r}] 正好是下一层==' if S.l < S.r
                                     else f'`r = newr = {S.r}`：这一层没有孩子入队，下一层为空'),
        'return res': '层序遍历结果 `{ret}`',
    },
    cards=dict(
        one_liner='用数组当队列，l、r 圈出当前层，newr 记下一层的边界',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定 N 叉树，返回节点值的==层序遍历==（从左到右，逐层）',
                 '输入按层序序列化，每组孩子用 `null` 分隔',
                 '示例：`root = [1,null,3,2,4,null,5,6]` → `[[1],[3,2,4],[5,6]]`'],
        quote='与二叉树的层序遍历没有什么不同，==依然是一遍bfs就可以了==。',
        quote_src='—— yiduobo 题解原文',
        idea=['不真正出队：`q` 只追加，用下标 `[l, r)` 表示当前层',
              '遍历本层时孩子追加到末尾，`newr` 跟着 `+1`',
              '本层结束：`l = r`，`r = newr`，就切换到下一层'],
        summary=['时间 `O(n)`，空间 `O(n)`：`q` 最终装下所有节点',
                 '易错：`newr` 要从 `r` 开始累加，而不是从 0',
                 '`range(l, r)` 在循环开始时固定，新入队的孩子不会混进本层',
                 '对比灵神：灵神用 `deque` + `len(q)` 分层；yiduobo 用下标分层，不出队',
                 '原文为 Python 2 风格，只删去了 Node 定义说明和类型文档字符串'],
    ),
)
