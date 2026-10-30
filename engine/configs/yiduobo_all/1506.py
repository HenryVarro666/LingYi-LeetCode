SETUP = '''
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []
    def __repr__(self):
        return f'Node({self.val})'

n5, n4 = Node(5), Node(4)
n3 = Node(3, [n5, n4])
n2 = Node(2)
n1 = Node(1, [n3, n2])
tree = [n3, n5, n1, n4, n2]   # 以任意顺序给出所有节点
'''

def _lay(root):
    pos, dep, nxt = {}, {}, [0]

    def go(nd, d):
        if not nd.children:
            pos[id(nd)] = nxt[0]
            nxt[0] += 1
        else:
            for c in nd.children:
                go(c, d + 1)
            pos[id(nd)] = (pos[id(nd.children[0])] + pos[id(nd.children[-1])]) / 2
        dep[id(nd)] = d
    go(root, 0)
    return pos, dep, max(dep.values()), max(nxt[0] - 1, 1)


def _ser(t):
    if t is None:
        return ''
    s = str(t.val)
    if t.children:
        s += '(' + ' '.join(_ser(c) for c in t.children) + ')'
    return s


def _tree(cv, box, root, T, color_fn, tag=None, R=28):
    """在 box 内画一棵 N 叉树；color_fn(node) -> 颜色名或 None"""
    x0, y0, x1, y1 = box
    pos, dep, md, mw = _lay(root)
    w, h = x1 - x0 - 2 * R - 120, y1 - y0 - 2 * R - 8
    P, nodes = {}, []

    def walk(nd):
        nodes.append(nd)
        fx = 0.5 if mw == 1 and len(pos) == 1 else pos[id(nd)] / mw
        P[id(nd)] = (x0 + 60 + R + fx * w, y0 + R + 4 + dep[id(nd)] / max(md, 1) * h)
        for c in nd.children:
            walk(c)
    walk(root)
    for nd in nodes:
        for c in nd.children:
            cv.line([P[id(nd)], P[id(c)]], T['dim'], 4)
    for nd in nodes:
        cx, cy = P[id(nd)]
        c = color_fn(nd)
        cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=T[c] if c else T['panel2'],
                     outline=T['border'], width=3)
        cv.text((cx, cy), nd.val, 26, T['bg'] if c else T['text'], anchor='mm', bold=True)
    if tag:
        cv.text((x0 + 8, y0 + 4), tag, 20, T['muted'], bold=True)
    return P


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    tree = S['tree']
    allk = {id(c) for n in tree for c in n.children}
    I = S['_inner']
    node, ch = I.get('node'), I.get('child')
    root = next(n for n in tree if id(n) not in allk)
    ans = S['_inner'].get('fa_val')
    fin = I.get('fa_val') is not None
    P = _tree(cv, (x0, y0 + 34, x1, y1 - 70), root, T,
              lambda n: 'green' if (fin and n.val == ans) else ('yellow' if n is node else ('orange' if n is ch else None)),
              '树（黄 = node，橙 = 刚异或进 child_xor 的孩子；输入顺序是乱的）')
    seq = ' '.join(str(n.val) for n in tree)
    cv.text((x0 + 20, y1 - 52), f'tree = [{seq}]', 26, T['muted'], bold=True, mono=True)


def _xv(S):
    return f"fa_xor = {S.get('fa_xor')}   child_xor = {S.get('child_xor')}   (二进制 {S.get('fa_xor', 0):03b} / {S.get('child_xor', 0):03b})"


CONFIG = dict(
    num=1506, title='找到N叉树的根节点', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='异或 · 只出现一次的数就是根',
    tags=['链表树与回溯', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def findRoot(self, tree):

        fa_xor = child_xor = 0

        for node in tree:
            fa_xor ^= node.val
            for child in node.children:
                child_xor ^= child.val
        
        fa_val = fa_xor ^ child_xor
        for node in tree:
            if node.val == fa_val:
                return node
''',
    setup=SETUP,
    call='Solution().findRoot(tree)',
    expect=1,
    result_fn=lambda n: n.val,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', size=28, h=70, fn=_xv),
    ],
    watch=[('fa_xor', 'fa_xor', 'blue'), ('child_xor', 'child_xor', 'pink'), ('fa_val', 'fa_val', 'green'),
           ('node', lambda S: getattr(S.get('node'), 'val', None), 'yellow')],
    captions={
        'fa_xor = child_xor = 0': '两个累加器：`fa_xor` 异或所有节点，`child_xor` 异或所有孩子',
        6: lambda S, B, r: ('所有节点都异或完了' if getattr(B._inner.get('node'), 'val', None) == S.node.val else f'取节点 `{S.node.val}`（顺序是乱的，没关系）'),
        12: lambda S, B, r: ('一圈扫完' if getattr(B._inner.get('node'), 'val', None) == S.node.val and S._line == B._line else f'按值找回节点：看 `{S.node.val}`'),
        'fa_xor ^= node.val': '`fa_xor` 异或进 `{node.val}` → =={fa_xor}==',
        'for child in node.children': lambda S, B, r: (f'`{S.node.val}` 没有孩子' if not S.node.children else ('孩子都异或完了' if getattr(B._inner.get('child'), 'val', None) == S.child.val else f'取孩子 `{S.child.val}`')),
        'child_xor ^= child.val': '孩子 `{child.val}` 异或进 `child_xor` → =={child_xor}==',
        'fa_val = fa_xor ^ child_xor': '每个非根节点在两边各出现一次、抵消；只有根只在 `fa_xor` 里出现：`{fa_xor} ^ {child_xor}` = =={fa_val}==',
        'if node.val == fa_val': lambda S, B, r: (f'`{S.node.val} == {S.fa_val}` → 找到了' if S.node.val == S.fa_val else f'`{S.node.val} != {S.fa_val}`，不是根'),
        'return node': '节点 `{node.val}` 就是根',
    },
    cards=dict(
        one_liner='非根节点都是别人的孩子——把「所有节点」和「所有孩子」异或，剩下的就是根',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给出 N 叉树的==全部节点==（顺序任意），找出根节点',
                 '节点值互不相同，每个节点有 `val` 和 `children`',
                 '本视频：5 个节点 `[3,5,1,4,2]`，根是 `1`'],
        quote='除了根节点之外，树中其他节点都是某个节点的孩子节点……问题就转化成了给出一个数组，其中有一种数字只出现了一次，其他所有数都出现了两次。',
        quote_src='—— yiduobo 题解原文',
        idea=['把「所有节点值」和「所有孩子值」放在一起看：根只出现 1 次，其他都出现 2 次',
              '相同的数异或为 0，所以全部异或起来 = 根的值',
              '再遍历一遍 `tree`，按值找回根节点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：返回的是==节点==不是值，所以还要再扫一遍按值找回',
                 '依赖「节点值互不相同」；值重复就不能用异或',
                 '同类题：只出现一次的数（136），用异或抵消',
                 '原文为 Python 2 风格，这里只删去了 Node 定义说明；Node 放在 setup 中'],
    ),
)
