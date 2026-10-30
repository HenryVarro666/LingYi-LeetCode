VALS = [1, 2, 3, None, 5]
TREE_H = 360
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
    """在字幕回调里记录每个节点返回的路径列表，并标到这一步的快照上"""
    def cap(S, B, ret):
        if record and S.get('now') is not None:
            DONE[S.now._uid] = ret
        root = S.get('root')
        if root is not None:
            for n in _walk(root):
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
    root = S.get('root')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = ', '.join(d)
        w = cv.tlen(s, 18, bold=True) + 16
        X = min(max(X, box[0] + w / 2 + 8), box[2] - w / 2 - 8)
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 18, T['green'], anchor='mm', bold=True)


def _cur(S):
    i = S['_inner']
    if 'now' not in i:
        return '每个节点返回==以它为根的子树==的所有路径（绿框）'
    return f"节点 `{i['now'].val}`：`left_res = {i.get('left_res')}`，`right_res = {i.get('right_res')}`"


CONFIG = dict(
    num=257, title='二叉树的所有路径', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='自底向上 · 合并子树路径',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def binaryTreePaths(self, root):

        if not root:
            return []

        res = []
        return self.dfs(root)

    def dfs(self, now):
        left_res = right_res = []
        if now.left:
            left_res = self.dfs(now.left)
        if now.right:
            right_res = self.dfs(now.right)

        res = ["%d->" % now.val + x for x in left_res] + ["%d->" % now.val + x for x in right_res]
        if not res:
            res = [str(now.val)]

        return res
''',
    call=f'Solution().binaryTreePaths(Tr({VALS}))',
    expect=['1->2->5', '1->3'],
    views=[
        dict(type='text', fn=_cur, size=24, h=56),
        dict(type='tree', label='二叉树（绿 = 已返回路径列表）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=200),
    ],
    watch=[('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue'),
           ('res', lambda S: S['_inner'].get('res') if 'now' in S['_inner'] else None, 'green')],
    captions={
        'if not root:': track('树非空，开始递归'),
        7: track('（这个 `res` 没有用到，答案直接来自 `dfs(root)`）'),
        'return self.dfs(root)': track('`dfs(now)`：返回以 now 为根的子树中，==从 now 到叶子的所有路径=='),
        'left_res = right_res = []': track(lambda S, B, r: f'来到节点 `{S.now.val}`：左右孩子的路径先设为空列表'),
        'if now.left:': track(lambda S, B, r: f'`{S.now.val}` 有左孩子 `{S.now.left.val}`' if S.now.left
                              else f'`{S.now.val}` 没有左孩子，`left_res` 保持为空'),
        'left_res = self.dfs': track(lambda S, B, r: f'递归求左孩子 `{S.now.val}` 的所有路径'),
        'if now.right:': track(lambda S, B, r: (f'拿到 `left_res = {S.left_res}`；' if S.left_res else '')
                               + (f'`{S.now.val}` 有右孩子 `{S.now.right.val}`' if S.now.right
                                  else f'`{S.now.val}` 没有右孩子')),
        'right_res = self.dfs': track(lambda S, B, r: f'递归求右孩子 `{S.now.val}` 的所有路径'),
        'res = ["%d->"': track(lambda S, B, r: f'拿到 `right_res = {S.right_res}`；' * bool(S.right_res)
                               + (f'左右孩子的每条路径前面接上 `"{S.now.val}->"` → `{S.res}`' if S.res
                                  else '左右都没有路径 → `res` 为空')),
        'if not res:': track(lambda S, B, r: f'`res` 为空 → `{S.now.val}` 是==叶子==' if not S.res
                             else f'`res` 非空，`{S.now.val}` 不是叶子'),
        'res = [str(now.val)]': track(lambda S, B, r: f'叶子的路径就是它自己：`res = {S.res}`'),
        'return res': track(lambda S, B, r: f'节点 `{S.now.val}` 返回 =={r}==', record=True),
    },
    cards=dict(
        one_liner='子树的路径先递归求出来，再在每条前面接上自己',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`（路径字符串）',
        problem=['给你二叉树的根 `root`，按任意顺序返回所有==从根到叶子==的路径',
                 '示例：`root = [1,2,3,null,5]` → `["1->2->5","1->3"]`',
                 '叶子节点 = 没有子节点的节点'],
        quote='若该节点是叶子节点，那么直接返回该节点。若该节点不是叶子节点，那么递归求解其左孩子与右孩子的所有路径，然后==将该节点添加到左孩子与右孩子的所有路径中==即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now)` 返回 now 子树里从 now 到各叶子的路径',
              '非叶子：拿到左右孩子的路径列表，每条前面加 `"now->"`',
              '叶子：左右都空，`res` 为空 → 返回 `[str(now.val)]`'],
        summary=['时间 `O(n^2)`：每层都要拼接一遍字符串；空间同阶',
                 '叶子判断很巧：拼出来的 `res` 为空，就说明没有孩子',
                 '`left_res = right_res = []` 共用一个空列表，但之后只会被重新赋值，不会出错',
                 '对比灵神：灵神自顶向下，用外部 `path` 回溯；yiduobo 自底向上合并',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
