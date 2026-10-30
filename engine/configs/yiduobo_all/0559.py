def _layout(root):
    pos, cnt = {}, [0]

    def go(n, d):
        if not n.children:
            x = cnt[0]
            cnt[0] += 1
        else:
            xs = [go(c, d + 1) for c in n.children]
            x = (xs[0] + xs[-1]) / 2
        pos[id(n)] = (x, d, n)
        return x
    go(root, 0)
    return pos, cnt[0]


def _path(root, target):
    if root is target:
        return [root]
    for c in root.children or []:
        p = _path(c, target)
        if p:
            return [root] + p
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S.get('root')
    cv.text((x0 + 18, y0 + 4), 'N 叉树（蓝 = now，黄 = 递归路径上的祖先，下方 depth = 当前 depth 变量）', 22, T['muted'], bold=True)
    if root is None:
        return
    pos, nleaf = _layout(root)
    maxd = max(d for _, d, _ in pos.values()) + 1
    sp = min(130, (x1 - x0 - 80) / max(1, nleaf))
    dy = min(120, (y1 - y0 - 120) / max(1, maxd - 1 + 0.01))
    sx = x0 + 40 + ((x1 - x0 - 80) - sp * nleaf) / 2 + sp / 2
    rad = 28
    now = S.get('now')
    path = {id(n) for n in (_path(root, now) or [])} if now is not None else set()
    done = S.get('_done') or {}

    def P(n):
        x, d, _ = pos[id(n)]
        return sx + x * sp, y0 + 80 + d * dy

    for x, d, n in pos.values():
        X, Y = P(n)
        for c in n.children or []:
            X2, Y2 = P(c)
            cv.line([(X, Y), (X2, Y2)], T['border'], 3)
    for x, d, n in pos.values():
        X, Y = P(n)
        isnow = n is now
        fill = T['blue'] if isnow else ((70, 60, 30) if id(n) in path else T['panel2'])
        outline = T['yellow'] if id(n) in path else T['border']
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=outline, width=4 if id(n) in path else 2)
        cv.text((X, Y), n.val, 28, T['bg'] if isnow else T['text'], anchor='mm', bold=True)
        if isnow:
            cv.text((X + rad + 6, Y - rad - 2), 'now', 20, T['blue'], anchor='lb', bold=True)
    dep = S.get('depth')
    if now is not None and dep is not None:
        X, Y = P(now)
        cv.text((X, Y + rad + 8), f'depth={dep}', 22, T['green'], anchor='mt', bold=True)
    for k in range(maxd):
        cv.text((x0 + 18, y0 + 80 + k * dy), f'第 {k + 1} 层', 20, T['dim'], anchor='lm')


def _cap_for(S, B, r):
    i = S['_inner']
    kids = i['now'].children
    if not kids:
        return f"`{i['now'].val}` 是叶子，没有孩子，循环不进入"
    prev = B.get('child')
    if 'child' in i and prev is not None and prev._uid == i['child']._uid:
        return f"`{i['now'].val}` 的孩子都看完了，退出循环"
    return f"取 `{i['now'].val}` 的下一个孩子：`{i['child'].val}`，先递归求它的深度"


CONFIG = dict(
    num=559, title='N 叉树的最大深度', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='递归：最深子树 + 1',
    tags=['链表树与回溯'],
    setup='''
import tracer
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
        self._uid = tracer.next_uid()

def _mk(spec):
    v, kids = spec
    return Node(v, [_mk(k) for k in kids])

tree = _mk((1, [(3, [(5, []), (6, [])]), (2, []), (4, [])]))
''',
    code='''
class Solution(object):
    def maxDepth(self, root):

        return self.dfs(root)

    def dfs(self, now):
        if not now:
            return 0
        
        depth = 0
        for child in now.children:
            depth = max(depth, self.dfs(child))
        return depth + 1
''',
    call='Solution().maxDepth(tree)',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=lambda S: f"当前节点 `{S['now'].val}`：已看过的子树里最深 `depth = {S['depth']}`" if 'now' in S and 'depth' in S else '', size=26, h=60),
        dict(type='calls', h=200, hide=()),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') is not None else None, 'blue'), ('depth', 'depth', 'green')],
    captions={
        'return self.dfs(root)': '从根节点出发：深度 = 最深的那棵子树深度 + 1',
        'if not now': '`now` 为空 → 深度是 `0`；否则继续',
        'depth = 0': lambda S, B, r: f"进入节点 `{S['_inner']['now'].val}`：先假设没有孩子，`depth = 0`",
        'for child in now.children': _cap_for,
        'depth = max': lambda S, B, r: f"递归求孩子 `{S['_inner']['child'].val}` 的深度，回来后 `depth = max(depth, 它)`，只保留最深的",
        'return depth + 1': lambda S, B, r: f"`{S['_inner']['now'].val}` 子树的深度 = 最深孩子 `{S['_inner']['depth']}` + 自己这一层 = =={r}==",
        'return 0': '空节点深度为 `0`',
    },
    skip=['if not now'],
    cards=dict(
        one_liner='一棵树的深度 = 最深的子树深度 + 1',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈，h 为树高）',
        problem=['给定一个 N 叉树，找到它的最大深度',
                 '最大深度 = 根节点到最远叶子节点的最长路径上的节点数',
                 '本视频：根 `1` 有孩子 `3, 2, 4`，`3` 有孩子 `5, 6` → `3`'],
        quote='对于以节点p为根节点的子树而言，其深度取决于其最深的子树有多深，于是可以优先递归求解其所有子树的深度，然后其中的最大值加一即为以p为根节点的子树。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个孩子的深度递归算出来，`depth` 里只留最大的',
              '节点自己占一层，所以返回 `depth + 1`',
              '叶子的 `children` 是空列表，循环不进入，直接返回 `0 + 1 = 1`'],
        summary=['时间 `O(n)`：每个节点访问一次；空间 `O(h)`',
                 '易错点：返回的是 `depth + 1`，别忘了加上自己这一层',
                 '`dfs` 里判空是给 `root = None` 兜底；孩子列表里不会有 `None`',
                 '和二叉树最大深度同一个套路：二叉树取 `max(左, 右)`，N 叉树取 `max(所有孩子)`',
                 '题目类定义 `Node` 在原文里是注释，视频里在 setup 里补上，题解代码未改动'],
    ),
)
