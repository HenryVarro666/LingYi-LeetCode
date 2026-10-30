# ---- 树上"已返回"标注：caption 回调里记录每个节点返回的 [抢, 不抢]，custom 叠加层（h=0）画在节点下方
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


def track(fn, key=None):
    def cap(S, B, ret):
        if key and S.get(key) is not None:
            DONE[S[key]._uid] = ret
        for n in _walk(S.get('root')):
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
        s = f'[{d[0]}, {d[1]}]'
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, T['green'], anchor='mm', bold=True)


def formula(S):
    I = S['_inner']
    if S.get('_line') == 10 and 'right' in I:
        n, l, r = I['now'].val, I['left'], I['right']
        return (f"抢 `{n}`：`{n} + {l[1]} + {r[1]} = {n + l[1] + r[1]}`；"
                f"不抢：`max({l[0]},{l[1]}) + max({r[0]},{r[1]}) = {max(l) + max(r)}`")
    return '`dfs(now)` 返回 `[抢 now 的最大收益, 不抢 now 的最大收益]`'


def cap_if(S, B, ret):
    if S.now is None:
        return '空节点 → 递归边界'
    return f'节点 `{S.now.val}`：先递归求出左右子树抢 / 不抢的最大收益'


def cap_l(S, B, ret):
    if S.now is None:
        return f'`{B.now.val}` 没有左孩子 → 左边是 `[0, 0]`'
    return f'递归左子树 `dfs({S.now.val})`'


def cap_r(S, B, ret):
    head = f'`left = {B.left}`；'
    if S.now is None:
        return head + '没有右孩子 → 右边是 `[0, 0]`'
    return head + f'递归右子树 `dfs({S.now.val})`'


def cap_ret(S, B, ret):
    n = S.now.val
    return (f'`right = {S.right}`。==抢== `{n}`：孩子只能不抢 → `{ret[0]}`；'
            f'==不抢==：孩子抢不抢都行，各取 max → `{ret[1]}`')


CONFIG = dict(
    num=337, title='打家劫舍 III', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='树形 DP · list[0] 抢 / list[1] 不抢',
    tags=['热题173'],
    code='''
class Solution(object):
    def rob(self, root):
        return max(self.dfs(root))

    def dfs(self, now):
        if not now:
            return [0, 0]
        left = self.dfs(now.left)
        right = self.dfs(now.right)
        return [now.val + left[1] + right[1], max(left) + max(right)]
''',
    call='Solution().rob(Tr([3,4,5,1,3,None,1]))',
    expect=9,
    views=[
        dict(type='tree', var='root', label='房子二叉树（绿 = 已算完，下方 = [抢, 不抢] 的最大收益）', pointers={'now': 'blue'},
             h=TREE_H, color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='text', fn=formula, size=26, h=60),
        dict(type='calls', h=200, hide=('root',)),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') is not None else None, 'blue'),
           ('left', lambda S: S['_inner'].get('left')), ('right', lambda S: S['_inner'].get('right'))],
    captions={
        'return max(self.dfs(root))': track('从根节点下来一趟 `dfs`：每个点返回 `[抢, 不抢]` 两种情况的最大收益'),
        'if not now': track(cap_if),
        'return [0, 0]': track('空节点，抢不抢都是 `0` → `[0, 0]`'),
        'left = self.dfs': track(cap_l),
        'right = self.dfs': track(cap_r),
        'return [now.val': track(cap_ret, key='now'),
    },
    cards=dict(
        one_liner='每个点算出「抢它」和「不抢它」时子树的最大收益，一趟 DFS 搞定',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['房子排成一棵二叉树，==直接相连==的两间房子同一晚被偷会报警',
                 '求不触动警报时最多能偷多少钱',
                 '示例：`root = [3,4,5,1,3,null,1]` → `9`（`4 + 5`）'],
        quote='对于某个节点，我们可以选择抢也可以选择不抢……我们使用一个list来记录，==list[0]表示抢，而list[1]表示不抢==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['抢该节点：左右孩子只能不抢 → `now.val + left[1] + right[1]`',
              '不抢该节点：孩子既可以抢也可以不抢 → `max(left) + max(right)`',
              '空节点返回 `[0, 0]`，答案是根节点的 `max(dfs(root))`'],
        result='根节点返回 `[8, 9]`：不抢根，抢 `4` 和 `5` 得 `9` 更大 → 答案 `9` ✓',
        summary=['时间 `O(n)`：每个点只访问一次；空间 `O(h)`',
                 '易错：抢当前点时要用孩子的 `[1]`（不抢），不能用 `max`',
                 '本例：偷根和第三层 `3 + 1 + 3 + 1 = 8`，不如只偷第二层 `4 + 5 = 9`',
                 '原文为 Python 2 风格：删去了文档字符串和 TreeNode 注释，逻辑未改'],
    ),
)
