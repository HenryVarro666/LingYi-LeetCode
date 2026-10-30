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


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S['root']
    pos, dep, md, mw = _lay(root)
    cv.text((x0 + 18, y0 + 4), 'N 叉树：黄 = 当前 now，绿 = 刚返回的 child，数字 = 节点值', 22, T['muted'], bold=True)
    R = 32
    w, h = x1 - x0 - 2 * R - 80, y1 - y0 - 2 * R - 90
    nodes, P = [], {}

    def walk(nd):
        nodes.append(nd)
        P[id(nd)] = (x0 + 40 + R + pos[id(nd)] / mw * w, y0 + 56 + R + dep[id(nd)] / max(md, 1) * h)
        for c in nd.children:
            walk(c)
    walk(root)
    for nd in nodes:
        for c in nd.children:
            cv.line([P[id(nd)], P[id(c)]], T['dim'], 4)
    now, ch = S.get('now'), S.get('child')
    for nd in nodes:
        cx, cy = P[id(nd)]
        c = 'yellow' if nd is now else ('green' if nd is ch else None)
        cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=T[c] if c else T['panel2'], outline=T['border'], width=3)
        cv.text((cx, cy), nd.val, 28, T['bg'] if c else T['text'], anchor='mm', bold=True)


def _info(S):
    if 'now' not in S or 'first' not in S:
        return ''
    return f"结点 `{S['now'].val}`：往下最长的两条链 `first = {S['first']}`，`second = {S['second']}`"


def _cmp(S, B, r):
    d, f, sc = S.d, S.first, S.second
    if d > f:
        return f'`d = {d} > first = {f}` → 成立：这条更长，要当最长链，原来的最长链退居第二'
    return f'`d = {d} > first = {f}` → 不成立：不比最长的长，再去和第二长比'


def _for(S, B, r):
    I = S._inner
    if 'child' not in I:
        return '没有孩子（叶子）→ 直接往下走'
    if B._inner.get('child') is not None and I['child'].val == B._inner['child'].val:
        return f'`{S.now.val}` 的孩子都遍历完了'
    return f'下一个孩子 `{I["child"].val}`'


CONFIG = dict(
    num=1522, title='N叉树的直径', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='递归求最长链 · 取 top 2 拼直径',
    tags=['动态规划', '链表树与回溯'],
    setup='''
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

n = {i: Node(i) for i in range(1, 9)}
n[1].children = [n[2], n[3], n[4]]
n[2].children = [n[5], n[6]]
n[5].children = [n[7]]
n[4].children = [n[8]]
tree_root = n[1]
''',
    code='''
class Solution(object):
    def diameter(self, root):

        if not root:
            return 0

        global res
        res = 0

        def dfs(now):
            first = second = 0
            for child in now.children:
                d = dfs(child)
                if d > first:
                    first, second = d, first
                elif d > second:
                    second = d
            
            global res

            res = max(res, first + second + 1)
            return first + 1
        
        dfs(root)
        return res - 1
''',
    call='Solution().diameter(tree_root)',
    expect=5,
    skip=['if not root', 'return 0', 'global res', 'res = 0', 'def dfs'],
    max_steps=90,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_info, h=60, size=24),
        dict(type='calls', h=170, hide=('root',)),
    ],
    watch=[('d', 'd', 'green'), ('first', 'first', 'blue'), ('second', 'second', 'pink')],
    captions={
        'first = second = 0': '`first` / `second`：以 `now` 为起点、往下的==最长和第二长==的树链长度，先都是 0',
        'for child in now.children': _for,
        'd = dfs(child)': '孩子 `{child.val}` 往下最长链 `d = {d}`（它自己算 1）',
        'if d > first': _cmp,
        'first, second = d, first': '最长链换成 `{first}`，原来的最长链顶替成第二长 `{second}`',
        'elif d > second': '`d = {d} > second = {second}` → 成立，它是新的第二长' if False else lambda S, B, r: (f'`d = {S.d} > second = {S.second}` → 成立：它成为新的第二长' if S.d > S.second else f'`d = {S.d} > second = {S.second}` → 不成立：这条链用不上'),
        'second = d': '`second` 更新为 `{second}`',
        'res = max': '以 `now` 为拐点的最长路径 = `first + second + 1` = `{first} + {second} + 1` = ==`{first + second + 1}`== 个结点，和 `res` 取大',
        'return first + 1': '返回给上层：从 `now` 往下最长链 `first + 1 = {first + 1}`',
        'dfs(root)': '从根开始递归',
        'return res - 1': '`res` 记的是结点数，边数 = `res - 1` = =={ret}==',
    },
    cards=dict(
        one_liner='直径一定是某个结点往下最长的两条链拼起来',
        complexity='时间 `O(n)`，空间 `O(h)`（递归深度）',
        problem=['给一棵 N 叉树的根，求树的直径：任意两个结点之间最长路径的==边数==',
                 '路径不一定经过根',
                 '本视频：8 个结点，直径是 `7→5→2→1→4→8`，共 5 条边'],
        quote='树的直径必然是由两条从某棵子树的根节点出发的树链构成的……记录这些孩子节点为根节点的子树中从根节点出发的最长的树链长度，取其中的==top 2==就组成了以now为根节点的子树中最长的路径。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now)` 返回「从 now 往下最长链的结点数」',
              '遍历孩子，维护最长 `first` 和第二长 `second`',
              '以 now 为最高点的路径有 `first + second + 1` 个结点，更新全局 `res`'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '`res` 是==结点数==，最后要减 1 才是边数',
                 '更新 first/second 要用 `if / elif`，替换最长时别忘了把旧的 first 降为 second',
                 '原文开头的 Node 类说明是注释，视频里在 setup 里定义了等价的 Node，代码本身无需改动',
                 '另一种做法：两次 BFS/DFS（先找最远点，再从它出发找最远）'],
    ),
)
