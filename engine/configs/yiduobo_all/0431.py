SETUP = '''
_ctr = itertools.count(1000)


class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
        self._uid = next(_ctr)


def NT(vals):
    root = Node(vals[0], [])
    q = deque([root])
    i = 2
    while q and i <= len(vals):
        nd = q.popleft()
        while i < len(vals) and vals[i] is not None:
            c = Node(vals[i], [])
            nd.children.append(c)
            q.append(c)
            i += 1
        i += 1
    return root


src = NT([1, None, 3, 2, 4, None, 5, 6])
'''


def _ser(n):
    return [n.val, [_ser(c) for c in n.children]]


_KIDS = {1: [3, 2, 4], 3: [5, 6]}


def _layout():
    pos, depth, leaves = {}, {}, [0]

    def go(v, d):
        depth[v] = d
        ch = _KIDS.get(v, [])
        if not ch:
            pos[v] = leaves[0]
            leaves[0] += 1
        else:
            for c in ch:
                go(c, d + 1)
            pos[v] = sum(pos[c] for c in ch) / len(ch)
    go(1, 0)
    return pos, depth, leaves[0]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inner = S['_inner']
    cv.text((x0 + 18, y0 + 4), '原 N 叉树（蓝圈 = 当前处理的节点）', 22, T['muted'], bold=True)
    pos, depth, nl = _layout()
    D = max(depth.values()) + 1
    sp = min(130, (x1 - x0 - 80) / max(1, nl))
    dy = min(90, (y1 - y0 - 100) / max(1, D))
    R = 26
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * nl) / 2 + sp / 2

    def P(v):
        return sx + pos[v] * sp, y0 + 70 + depth[v] * dy

    cur = None
    if inner.get('root') is not None:
        cur = inner['root'].val
    elif inner.get('data') is not None:
        cur = inner['data'].val
    for v, ch in _KIDS.items():
        for c in ch:
            cv.line([P(v), P(c)], T['border'], 3)
        for a, b in zip(ch, ch[1:]):
            (ax, ay), (bx, by) = P(a), P(b)
            cv.dashed((ax + R, ay), (bx - R, by), T['orange'], 2)
    for v in pos:
        X, Y = P(v)
        hot = v == cur
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['panel2'], outline=T['blue'] if hot else T['border'],
                     width=5 if hot else 2)
        cv.text((X, Y), v, 26, T['text'], anchor='mm', bold=True)
    cv.text((x1 - 20, y0 + 6), '橙色虚线 = 兄弟（对应二叉树的 right）', 18, T['dim'], anchor='ra')


def _kids(S):
    r = S['_inner'].get('res')
    if r is not None and hasattr(r, 'children'):
        return f"`res = Node({r.val})`，children = `{[c.val for c in r.children]}`"
    return ''


def _for(S, B, ret):
    sc, bc = S['_inner'].get('child'), B['_inner'].get('child')
    if sc is None:
        return f'`{S.root.val}` 没有孩子，不用循环（叶子，二叉树里 left/right 都空）'
    if bc is not None and bc.val == sc.val:
        return f'`{S.root.val}` 的孩子都处理完，退出循环'
    return f'`{S.root.val}` 的下一个孩子：`{sc.val}`'


def _unused(S, B, r):
    if 'child' in B and B.child is not None and S.child.val == B.child.val and S.get('now') is not None and False:
        return ''
    return f'处理 `{S.root.val}` 的孩子 `{S.child.val}`'


CONFIG = dict(
    num=431, title='将N叉树编码为二叉树', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='孩子兄弟表示法',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Codec:
    def encode(self, root):
        if not root:
            return None

        res = TreeNode(root.val)
        now = None
        for child in root.children:
            if now is None:
                res.left = self.encode(child)
                now = res.left
            else:
                now.right = self.encode(child)
                now = now.right

        return res

    def decode(self, data):
        if data is None:
            return None

        res = Node(data.val, [])
        now = data.left
        while now:
            res.children.append(self.decode(now))
            now = now.right
        return res
''',
    setup=SETUP,
    call='c = Codec()\nb = c.encode(src)\nc.decode(b)',
    result_fn=_ser,
    expect=[1, [[3, [[5, []], [6, []]]], [2, []], [4, []]]],
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='tree', label='二叉树（编码结果：left = 第一个孩子，right = 下一个兄弟）', pointers={'now': 'blue', 'res': 'green'}, h=260),
        dict(type='calls', hide=('self',), h=130),
        dict(type='text', size=24, h=44, fn=lambda S: _kids(S)),
    ],
    watch=[('root', lambda S: getattr(S['_inner'].get('root'), 'val', None), 'blue'),
           ('child', lambda S: getattr(S['_inner'].get('child'), 'val', None), 'cyan'),
           ('data', lambda S: getattr(S['_inner'].get('data'), 'val', None), 'purple'),
           ('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'orange')],
    captions={
        'if not root': lambda S, B, r: f'`{S.root.val}` 非空，继续' if S.root else '空节点，返回 None',
        'res = TreeNode(root.val)': '用 `{root.val}` 新建二叉树节点 `res`',
        'now = None': '`now` 记录「最近挂好的孩子」，还没有孩子',
        'for child in root.children': _for,
        'if now is None': lambda S, B, r: ('`now` 为空：这是第一个孩子 → 它挂在 `res.left`' if S.now is None else f'`now = {S.now.val}` 已有 → 这是后面的孩子，要挂在兄弟的 `right`'),
        'res.left = self.encode(child)': '第一个孩子递归编码后，成为 `res.left`',
        'now = res.left': '`now` → {now.val}（长子）',
        'now.right = self.encode(child)': '后一个孩子递归编码后，成为上一个孩子的 `right`（兄弟）',
        14: '`now` → {now.val}（指向刚挂好的兄弟）',
        16: lambda S, B, r: f'`{S.res.val}` 的整棵子树编码完成，返回 `res`',
        'if data is None': lambda S, B, r: ('空，返回 None' if S.data is None else f'`{S.data.val}` 非空，开始还原'),
        'res = Node(data.val, [])': '建 N 叉树节点 `{res.val}`，`children` 先空着',
        'now = data.left': '`data.left` 是==第一个孩子==：从它出发',
        'while now': lambda S, B, r: (f'`now = {S.now.val}` 非空 → 是 `{S.res.val}` 的一个孩子' if S.now else '`now` 为空：兄弟走完了，所有孩子都收齐'),
        'res.children.append': '递归还原 `{now.val}` 的子树，结果追加进 `res.children`',
        26: lambda S, B, r: (f'沿 `right` 走到下一个兄弟 `{S.now.val}`' if S.now else '没有下一个兄弟了'),
        27: lambda S, B, r: f'`{S.res.val}` 的 N 叉树节点还原完成，`children` = `{[c.val for c in S.res.children]}`',
    },
    cards=dict(
        one_liner='孩子兄弟表示法：left 是长子，right 是下一个兄弟',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['把 N 叉树编码成二叉树（`encode`），再能还原回来（`decode`），要保证 decode(encode(root)) 等于原树',
                 '编码方式不限，只要可逆',
                 '本视频：`[1,null,3,2,4,null,5,6]`，节点 1 有孩子 3、2、4'],
        quote='若node有左孩子，那么node.left表示就是node在N叉树中所有孩子节点的其中一个……若node有右孩子，那么now.right表示的则是node在N叉树的某个兄弟节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['encode：长子挂 `res.left`，其余孩子依次挂在前一个孩子的 `right` 上，形成一条兄弟链',
              '`now` 始终指向最近挂好的孩子，所以第一个孩子和后面的孩子分开处理',
              'decode：`data.left` 是长子，沿着 `right` 一路走就是全部孩子，逐个递归还原'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '`now is None` 区分长子与后续孩子，别把所有孩子都挂到 left',
                 '二叉树的 right 是兄弟，不是 N 叉树里的孩子',
                 '原文代码只删去了顶部的类说明和两个 `:type` 文档字符串，逻辑不变；Node 在 setup 里按题目给出'],
    ),
)
