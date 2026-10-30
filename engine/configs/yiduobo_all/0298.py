TREE_H = 330
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


def _root(S):
    return S.get('root') or S.get('self.tree')


def track(fn, record=False):
    def cap(S, B, ret):
        if S['_line'] == 5:
            DONE.clear()
        if record:
            DONE[S.now._uid] = ret
        r = max(DONE.values(), default=0)
        if S['_line'] == 21:
            r = max(r, S['_inner'].get('v') or 0)
        for n in _walk(_root(S)):
            n._d = DONE.get(n._uid)
        _root(S)._res = r
        if callable(fn):
            return fn(S, B, ret)
        ctx = dict(S)
        ctx.update(B=B, ret=ret)
        return eval('f' + repr(fn), {}, ctx)
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
    root = _root(S)
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'连续 {d}'
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, T['green'], anchor='mm', bold=True)


def cap_chk(side):
    def f(S, B, ret):
        n = S.now
        ch = getattr(n, side)
        if ch.val == n.val + 1:
            return f'子节点 `{ch.val}` == `{n.val} + 1` → 值连续，可以==接在 {n.val} 后面=='
        return f'子节点 `{ch.val}` != `{n.val} + 1` → 值不连续，这条链在 `{n.val}` 处断开'
    return f


CONFIG = dict(
    num=298, title='二叉树最长连续序列', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 自底向上',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def longestConsecutive(self, root):

        global res
        res = 0

        def dfs(now):
            global res

            v = 1
            if now.left:
                left_v = dfs(now.left)
                if now.left.val == now.val + 1:
                    v = max(v, left_v + 1)
            
            if now.right:
                right_v = dfs(now.right)
                if now.right.val == now.val + 1:
                    v = max(v, right_v + 1)

            res = max(res, v)
            return v
        
        dfs(root)
        return res
''',
    call='''s = Solution()
s.tree = Tr([1,None,3,2,4,None,None,None,5])
s.longestConsecutive(s.tree)''',
    expect=3,
    views=[
        dict(type='tree', label='二叉树（蓝 = now；绿 = 已返回：以它为起点的连续序列长度）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=210),
    ],
    watch=[('now', lambda S: S['_inner'].get('now').val if S['_inner'].get('now') else None, 'blue'),
           ('v', lambda S: S['_inner'].get('v'), 'green'),
           ('res', lambda S: getattr(_root(S), '_res', None), 'yellow')],
    captions={
        'res = 0': track('`res` 是全局答案，最长连续序列长度，先设为 `0`'),
        'v = 1': track('`v` = 以 `{now.val}` 为起点的连续序列长度，至少是 `1`（它自己）'),
        'if now.left:': track(lambda S, B, r: ('有左孩子 → 先递归求出以它为起点的长度' if B.now.left else '没有左孩子，跳过')),
        'left_v = dfs': track(lambda S, B, r: f'进入左孩子 `{B.now.left.val}`：它先算好自己的链长，回来再比较'),
        'if now.left.val == now.val + 1': track(cap_chk('left')),
        'v = max(v, left_v + 1)': track('`v = max({B.v}, {left_v} + 1) = =={v}==`：把 `{now.val}` 接在左边链的头部'),
        'if now.right:': track(lambda S, B, r: ('有右孩子 → 先递归求出以它为起点的长度' if B.now.right else '没有右孩子，跳过')),
        'right_v = dfs': track(lambda S, B, r: f'进入右孩子 `{B.now.right.val}`：它先算好自己的链长，回来再比较'),
        'if now.right.val == now.val + 1': track(cap_chk('right')),
        'v = max(v, right_v + 1)': track('`v = max({B.v}, {right_v} + 1) = =={v}==`：把 `{now.val}` 接在右边链的头部'),
        'res = max(res, v)': track(lambda S, B, r: f"以 `{S.now.val}` 为起点的长度 `v = {S['_inner'].get('v')}`，更新答案：`res = max(旧 res, {S['_inner'].get('v')}) = =={_root(S)._res}==`"),
        'return v': track('节点 `{now.val}` 返回 `v = {ret}` 给父节点用', record=True),
        'return res': '全部节点处理完，最长连续序列长度 = `res = {res}`',
    },
    skip=['dfs(root)'],
    cards=dict(
        one_liner='自底向上：每个节点算「以我为起点向下的最长连续链」',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['给你一棵二叉树的根 `root`，求最长的「连续序列路径」的长度',
                 '路径只能==从父到子==，且每往下一步值恰好 `+1`',
                 '本视频：`root = [1,null,3,2,4,null,null,null,5]` → `3`（`3→4→5`）'],
        quote='对于当前节点now，不妨先递归求解其左右子树，分别得到以now.left和now.right为起点的连续序列的长度，记为left_v和right_v。',
        quote_src='—— yiduobo 题解',
        idea=['先递归，再处理自己：`dfs(now)` 返回以 `now` 为起点的最长连续长度 `v`',
              '子节点值恰好是 `now.val + 1`，就能把 `now` 接在它前面：`v = left_v + 1`',
              '每个节点都用 `v` 更新全局 `res`，同时把 `v` 返回给父亲'],
        result='返回 `3`：节点 `3` 为起点的链 `3 → 4 → 5`',
        summary=['时间 `O(n)`，空间 `O(h)`（递归栈）',
                 '易错：只有子节点值恰好等于 `now.val + 1` 才能延长；否则 `v` 保持 `1`',
                 '`v` 必须==返回==给父亲，`res` 才用全局变量记录最大值',
                 '左右两边分别判断、取较大者，而不是相加（路径不能拐弯）'],
    ),
)
