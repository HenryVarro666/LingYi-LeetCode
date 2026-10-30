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
        if record and S.get('now') is not None:
            DONE[S['now']._uid] = ret
        for n in _walk(S.get('root')):
            n._d = DONE.get(n._uid)
        if callable(fn):
            return fn(S, B, ret)
        return eval('f' + repr(fn), {'B': B, 'ret': ret}, dict(S))
    return cap


def _layout(root, box):
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
        s = FMT(d)
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def FMT(d):
    return str(d)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_res0(S, B, ret):
    return (f'`res[0]`：==不染 `{S.now.val}`==，两边各取最优：`max(左)={max(S.left_res)}` + `max(右)={max(S.right_res)}` = {S.res[0]}')


def cap_inner(S, B, ret):
    lc, cnt = S.left_cnt, S.cnt
    return (f'染 `{S.now.val}`，块大小 `{cnt}`：左块 `{lc}` + 右块 `{cnt - lc - 1}` + 自己 1。'
            f'`{S.left_res[lc]} + {S.right_res[cnt - lc - 1]} + {S.now.val}` → `res[{cnt}] = =={S.res[-1]}==`')


CONFIG = dict(
    num='LCP 34', title='二叉树染色', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='树形 DP · 状态含块大小',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def maxValue(self, root, k):

        def dfs(now):
            if now.left:
                left_res = dfs(now.left)
            else:
                left_res = [0] * k

            if now.right:
                right_res = dfs(now.right)
            else:
                right_res = [0] * k

            res = [max(left_res) + max(right_res)]
            for cnt in range(1, k + 1):
                res.append(0)
                for left_cnt in range(cnt):
                    res[-1] = max(res[-1], left_res[left_cnt] + right_res[cnt - left_cnt - 1] + now.val)

            return res

        return max(dfs(root))
''',
    call='Solution().maxValue(Tr([5,2,3,4]), 2)',
    expect=12,
    views=[
        dict(type='tree', label='二叉树（蓝 = now，绿 = 已算出 res）', pointers={'now': 'blue'}, h=TREE_H),
        dict(type='custom', draw=badges, h=0),
        dict(type='array', var='res', label='res[cnt]：now 所在蓝块大小为 cnt 时的最大和', cell=60, h=100),
        dict(type='calls', h=130, hide=('root',)),
    ],
    watch=[('now', 'now.val', 'blue'), ('left_res', lambda S: S['_inner'].get('left_res'), 'cyan'),
           ('right_res', lambda S: S['_inner'].get('right_res'), 'pink'),
           ('cnt', lambda S: S['_inner'].get('cnt'), 'yellow')],
    captions={
        'if now.left:': track(lambda S, B, r: f'节点 `{S.now.val}` 有左儿子吗？' + ('有 → 先递归求左子树' if S.now.left else '没有 → 左边没有蓝块可用，当成全 0')),
        'left_res = dfs': track('左子树的 `res` = `{left_res}`'),
        'left_res = [0] * k': track('没有左儿子：`left_res = [0] * {k}`，什么也贡献不了'),
        'if now.right:': track(lambda S, B, r: f'节点 `{S.now.val}` 有右儿子吗？' + ('有 → 递归求右子树' if S.now.right else '没有 → 右边当成全 0')),
        'right_res = dfs': track('右子树的 `res` = `{right_res}`'),
        'right_res = [0] * k': track('没有右儿子：`right_res = [0] * {k}`'),
        'res = [max(left_res)': track(cap_res0),
        'for cnt in range': track('枚举 `now` 所在蓝块大小 `cnt`（≤ k = {k}）：当前 `cnt = {cnt}`'),
        'res.append(0)': track('先给 `res[{cnt}]` 占位 0，下面用 `max` 更新'),
        'for left_cnt in range': track('枚举左子树分走的块大小 `left_cnt`，剩下的给右边：`left_cnt = {left_cnt}`'),
        'res[-1] = max': track(cap_inner),
        'return res': track('`now = {now.val}` 的结果 `res = {ret}`：下标 = 块大小，值 = 最大和', record=True),
        'return max(dfs(root))': track('根的 `res` 里取最大 = ==`{ret}`==（染 5 和 3，再单独染 4，中间的 2 不染）'),
    },
    skip=['for left_cnt in range', 'res.append(0)', 'for cnt in range', 'if now.left:', 'if now.right:'],
    max_steps=70,
    cards=dict(
        one_liner='把「包含当前点的蓝块大小」放进状态，枚举左右分块大小',
        complexity='时间 `O(n·k²)`，空间 `O(n·k)`',
        problem=['二叉树，每个节点有权值；可以把一些节点染成蓝色',
                 '每个相连的蓝色块大小不能超过 `k`，求蓝色节点权值和的最大值',
                 '示例：`root = [5,2,3,4]`，`k = 2` → `12`'],
        quote='k规模很小，那么完全可以将其表示在状态中，即f[now][cnt]表示以now为根节点，且包含根节点的蓝色块大小为cnt时，子树中蓝色节点的最大和。',
        quote_src='—— yiduobo 题解',
        idea=['`res[0]`：不染 now，左右子树各自取最大即可',
              '`res[cnt]`：染 now，左块 + 右块 + 自己 = `cnt`',
              '所以枚举 `left_cnt`，右块大小就是 `cnt - left_cnt - 1`'],
        result='运行结束，返回 `12`：染 `5`、`3` 一块（8），`4` 单独一块（4）',
        summary=['时间 `O(n·k²)`：每个节点枚举 `cnt` 和 `left_cnt`；空间 `O(n·k)`',
                 '易错：没有儿子时用 `[0] * k`，下标 `0..k-1` 刚好够用（块最大 `k-1`）',
                 '易错：`res[0]` 是「不染 now」，要取左右 `max`，不是只取 `res[0]`',
                 '换根的思路：状态里带「当前块大小」是这类连通块计数的常用套路'],
    ),
)
