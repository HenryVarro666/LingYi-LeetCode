# ---- 已返回节点：caption 回调里记录每个节点 dfs 的返回值（最长链长），在节点下方画徽标
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
        nd = S.get('now')
        if record and nd is not None:
            DONE[nd._uid] = ret
        root = S.get('root')
        if root is not None:
            for n in _walk(root):
                n._d = DONE.get(n._uid)
        if callable(fn):
            return fn(S, B, ret)
        g = dict(S)
        g.update(B=B, ret=ret)
        try:
            return eval('f' + repr(fn), g)
        except Exception:
            return fn
    cap._t = True
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
        s = f'链长 {d}'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def _l(S, B, ret):
    n = S.now
    if not n.left:
        return '没有左孩子，`left` 保持 0'
    if n.left.val == n.val:
        return f'左孩子 `{n.left.val}` = `{n.val}` → 可以接上'
    return f'左孩子 `{n.left.val}` ≠ `{n.val}` → 不能往左延伸，`left` 仍是 ==0=='


def _r(S, B, ret):
    n = S.now
    if not n.right:
        return '没有右孩子，`right` 保持 0'
    if n.right.val == n.val:
        return f'右孩子 `{n.right.val}` = `{n.val}` → 可以接上'
    return f'右孩子 `{n.right.val}` ≠ `{n.val}` → 不能往右延伸，`right` 仍是 ==0=='


CONFIG = dict(
    num=687, title='最长同值路径', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归求树链 · 左链 + 右链',
    tags=['灵神题单·动态规划', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def longestUnivaluePath(self, root):

        if not root:
            return 0
        
        self.res = 0
        self.dfs(root)
        return self.res - 1

    def dfs(self, now):
        left = right = 0

        if now.left:
            tmp = self.dfs(now.left)
            if now.left.val == now.val:
                left = tmp

        if now.right:
            tmp = self.dfs(now.right)
            if now.right.val == now.val:
                right = tmp
        
        self.res = max(self.res, left + right + 1)
        return max(left, right) + 1
''',
    call='Solution().longestUnivaluePath(Tr([4,4,4,4,5,None,4]))',
    expect=4,
    views=[
        dict(type='tree', label='二叉树（蓝 = now，绿 = 已返回树链长）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='text', fn=lambda S: (f"经过 now 的路径节点数：`{S['_inner']['left']} + {S['_inner']['right']} + 1`　`self.res = {S['self.res']}`"
                                        if 'left' in S['_inner'] and 'self.res' in S else ''), size=24, h=50),
        dict(type='calls', h=210, hide=('root',)),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') is not None else None, 'blue'),
           ('left', lambda S: S['_inner'].get('left')), ('right', lambda S: S['_inner'].get('right')),
           ('res', lambda S: S.get('self.res'), 'green')],
    captions={
        'self.res = 0': '`self.res` 记录最长路径的==节点数==（不是边数），先设为 0',
        'self.dfs(root)': '从根开始，递归求每个节点的「包含自己在内的最长树链」',
        'left = right = 0': lambda S, B, r: f'节点 `{S.now.val}`：左右树链长先都设为 0（可以不往下延伸）',
        'if now.left:': lambda S, B, r: ('有左孩子 → 先递归求它的树链长' if B.now.left else '没有左孩子，跳过'),
        'tmp = self.dfs(now.left)': track('递归求左孩子的树链长，放进 `tmp`'),
        'if now.left.val == now.val': track(_l),
        'left = tmp': track('值相同才能接：`left = {left}`'),
        'if now.right:': lambda S, B, r: ('有右孩子 → 同样递归' if B.now.right else '没有右孩子，跳过'),
        'tmp = self.dfs(now.right)': track('递归求右孩子的树链长，放进 `tmp`'),
        'if now.right.val == now.val': track(_r),
        'right = tmp': track('值相同才能接：`right = {right}`'),
        'self.res = max': track(lambda S, B, r: f"经过 `{S.now.val}` 的路径：`{S.left} + {S.right} + 1` = {S.left + S.right + 1} 个节点；`self.res = max({B.get('self.res')}, {S.left + S.right + 1})` → =={S['self.res']}=="),
        'return max': track('向父亲只能带一条链：`max({left}, {right}) + 1` = =={ret}==', record=True),
        'return self.res - 1': '`res` 是节点数，边数 = 节点数 - 1 = =={ret}==',
        'if not root': '`root` 非空才往下走；空树直接返回 0',
    },
    max_steps=90,
    cards=dict(
        one_liner='每个节点递归求最长树链，左链 + 右链 + 1 就是一条路径',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你二叉树 `root`，返回==每个节点值都相同==的最长路径的长度（边数）',
                 '路径可以不经过根',
                 '本视频：`[4,4,4,4,5,null,4]` → `4`'],
        quote='这条路径必然是由某棵子树的根节点，加上其左子树中的一条树链以及右子树中的一条树链构成，这里树链的长度可以为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now)` 返回「包含 now 在内的最长树链」的节点数',
              '孩子的值和 now 不同 → 对应的 `left` / `right` 置零',
              '经过 now 的最长路径 = `left + right + 1`，用它更新 `self.res`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '全程用==节点数==计数，最后 `res - 1` 才是边数',
                 '孩子要==先递归==，再比较值：不同也得走下去，答案可能在深处',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神空节点返回 `-1` 直接用边数；yiduobo 不进空节点，用节点数最后减 1'],
    ),
)

CONFIG['captions'] = {k: (v if getattr(v, '_t', False) else track(v)) for k, v in CONFIG['captions'].items()}
