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
    done = {v for row in (S.get('ans') or []) for v in row} | set(S['_inner'].get('vals') or [])
    inq = {x._uid for x in (S.get('q') or [])}
    _nary(cv, S, box, T, 'N 叉树（青 = 在队列中，绿 = 已出队记录）',
          lambda n: 'green' if n.val in done else ('cyan' if n._uid in inq else None),
          ptrs=(('node', S['_inner'].get('node'), 'blue'),))


def _w(S, B, ret):
    if S.q:
        return f'队列里恰好是==同一层==的 {len(S.q)} 个节点 `{[x.val for x in S.q]}`'
    return '队列空了：所有层都处理完'


LEVEL = [0]


def _vals(S, B, ret):
    LEVEL[0] = len(S.q)
    return f'新的一层开始：`vals` 收集这一层的值；本层有 `len(q) = {LEVEL[0]}` 个节点'


def _for(S, B, ret):
    k, n = len(B.vals), LEVEL[0]
    if k == 0:
        return f'`range(len(q))` ==进入循环时就固定为 {n} 次==，之后入队的孩子不会被本层弹出'
    if k < n:
        return f'弹出本层第 {k + 1}/{n} 个节点'
    return f'本层 {n} 个节点都弹完了，退出循环'


def _ext(S, B, ret):
    ch = [c.val for c in S.node.children]
    if not ch:
        return f'`{S.node.val}` 没有孩子'
    return f'`{S.node.val}` 的孩子 `{ch}` 入队（它们属于==下一层==，排在本层后面）'


CONFIG = dict(
    num=429, title='N 叉树的层序遍历', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='BFS · 一个队列按层弹出',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        if root is None:
            return []
        ans = []
        q = deque([root])
        while q:
            vals = []
            for _ in range(len(q)):
                node = q.popleft()
                vals.append(node.val)
                q.extend(node.children)
            ans.append(vals)
        return ans
''',
    setup=SETUP,
    call='Solution().levelOrder(root)',
    expect=[[1], [3, 2, 4], [5, 6]],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='queue', var='q', label='q（队首在左）', fmt=lambda x: str(x.val), h=120),
        dict(type='array', var=lambda S: S['_inner'].get('vals') or [], label='vals（本层的值）', cell=80, h=120),
        dict(type='text', size=26, h=56, fn=lambda S: f"`ans = {S['ans']}`" if 'ans' in S else ''),
    ],
    watch=[('node', lambda S: _v(S['_inner'].get('node')), 'blue'), ('len(q)', lambda S: len(S['q']) if 'q' in S else None)],
    captions={
        'if root is None': '树非空',
        'ans = []': '`ans` 按层收集结果',
        'q = deque([root])': '第 0 层只有根节点：入队',
        'while q': _w,
        'vals = []': _vals,
        'for _ in range(len(q))': _for,
        'node = q.popleft()': '队首出队：`node = {node.val}`',
        'vals.append': '记录本层的值：`vals = {vals}`',
        'q.extend': _ext,
        'ans.append(vals)': '这一层弹完了，`{ans[-1]}` 加入答案；==此时队列里正好是下一层==',
        'return ans': '层序遍历结果 `{ret}`',
    },
    cards=dict(
        one_liner='队列里每次只装一层：先记个数，弹这么多次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定 N 叉树，返回节点值的==层序遍历==（从左到右，逐层）',
                 '输入按层序序列化，每组孩子用 `null` 分隔',
                 '示例：`root = [1,null,3,2,4,null,5,6]` → `[[1],[3,2,4],[5,6]]`'],
        quote='本题只需要在 102. 二叉树的层序遍历的基础上，==把访问左右子树改成遍历 children 列表==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`range(len(q))` 在循环开始时就算好，正好是本层节点数',
              '弹出本层节点时把孩子 `extend` 到队尾，下一层排在后面',
              '本层弹完，队列里剩下的恰好是下一层'],
        summary=['时间 `O(n)`，空间 `O(n)`（最坏根有 `n-1` 个孩子）',
                 '易错：不能写 `while q` 来弹本层，必须先固定 `len(q)`',
                 '方法一「两个数组」：`q = [c for node in q for c in node.children]` 直接生成下一层',
                 '同类：102 二叉树层序遍历、107、103'],
    ),
)
