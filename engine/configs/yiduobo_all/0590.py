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
    res = S.get('res') or []
    st = {x._uid for x in (S.get('stack') or [])}
    _nary(cv, S, box, T, 'N 叉树（青 = 在栈中，绿 = 已出栈加入 res）',
          lambda n: 'green' if n.val in res else ('cyan' if n._uid in st else None),
          ptrs=(('now', S.get('now'), 'blue'),))


def _pop(S, B, ret):
    return f'弹出栈顶 `now = {S.now.val}`（==后进先出==）'


def _ext(S, B, ret):
    ch = [c.val for c in S.now.children]
    if not ch:
        return f'`{S.now.val}` 没有孩子，栈不变'
    return f'孩子 `{ch}` ==按原顺序==压栈 → 最右边的 `{ch[-1]}` 在栈顶，下次先处理它'


def _w(S, B, ret):
    if S.stack:
        return f'栈非空（{len(S.stack)} 个节点），继续'
    return '栈空了：得到的 `res` 是「根 → 子树 n → … → 子树 1」的顺序'


CONFIG = dict(
    num=590, title='N 叉树的后序遍历', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='栈迭代 · 反向前序再翻转',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def postorder(self, root):

        if not root:
            return []

        res = []
        stack = [root]
        while stack:
            now = stack.pop()
            res.append(now.val)
            stack.extend(now.children)

        return res[::-1]
''',
    setup=SETUP,
    call='Solution().postorder(root)',
    expect=[5, 6, 3, 2, 4, 1],
    views=[
        dict(type='text', size=24, h=56, fn=lambda S: '后序 `子树1→…→子树n→根` 翻转 = ==根→子树n→…→子树1=='),
        dict(type='custom', draw=_draw, h=340),
        dict(type='stack', var='stack', label='stack（栈顶在右）', fmt=lambda x: str(x.val), h=120),
        dict(type='array', var='res', label='res（反向的后序）', cell=80, h=130),
    ],
    watch=[('now', lambda S: _v(S.get('now')), 'blue')],
    captions={
        'if not root': '树非空',
        'res = []': '`res` 记录「根 → 子树 n → … → 子树 1」的访问顺序',
        'stack = [root]': '根节点先入栈',
        'while stack': _w,
        'now = stack.pop()': _pop,
        'res.append': '先访问根：`res = {res}`',
        'stack.extend': _ext,
        'return res[::-1]': '把 `res` ==整体翻转==，就是后序遍历 `{ret}`',
    },
    cards=dict(
        one_liner='后序翻转后是「根→子树n→…→子树1」，用栈做完再反转',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定 N 叉树的根 `root`，返回节点值的==后序遍历==',
                 '输入按层序序列化，每组孩子用 `null` 分隔',
                 '示例：`root = [1,null,3,2,4,null,5,6]` → `[5,6,3,2,4,1]`'],
        quote='如果将其翻转，就是 根节点 -> 子树n -> 子树n-1 -> ... ->子树1 这种形式……在处理到某个节点时，==直接按顺序将该节点的子树压入栈中==。得到最终的答案后，将其反序输出即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['后序 `子树1, …, 子树n, 根` 反过来是 `根, 子树n, …, 子树1`',
              '这和前序几乎一样，只是孩子顺序反了',
              '孩子按原顺序压栈 → 最右孩子先出栈，正好是「子树 n 先」'],
        result='`res = [1, 4, 2, 3, 6, 5]`，翻转得 `[5, 6, 3, 2, 4, 1]`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '关键：前序要把孩子==逆序==压栈，这里==按原序==压栈，最后再翻转',
                 '易错：别忘了最后的 `res[::-1]`',
                 '对比灵神：灵神直接递归「先孩子后根」，yiduobo 用迭代回答了进阶问题',
                 '原文为 Python 2 风格，只删去了 Node 定义说明和类型文档字符串'],
    ),
)
