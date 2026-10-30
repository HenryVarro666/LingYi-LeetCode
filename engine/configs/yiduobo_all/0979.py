# 树上标注：每个节点 dfs 返回的 (金币数, 节点数)，画在节点下方
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
        if record and S.now is not None:
            DONE[S.now._uid] = ret
        for n in _walk(S.get('self.tree')):
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
    root = S.get('self.tree')
    if root is None:
        return
    pos, rad, order = _layout(root, (box[0], box[1] - TREE_H, box[2], box[1]))
    for n in order:
        d = getattr(n, '_d', None)
        if d is None:
            continue
        X, Y = pos[n._uid]
        s = f'{d[0]}币/{d[1]}点'
        w = cv.tlen(s, 19, bold=True) + 16
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 31), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 18), s, 19, T['green'], anchor='mm', bold=True)


def _nv(x):
    return '空' if x is None else str(x.val)


def _cap_ret(S, B, ret):
    n = S.now
    return (f'`{n.val}` 的子树：金币 `{S.s_l} + {S.s_r} + {n.val}` = =={ret[0]}==，节点 `{S.cnt_l} + {S.cnt_r} + 1` = =={ret[1]}==，'
            f'累计操作 `{ret[2]}` 次 → 一起返回给父亲')


CONFIG = dict(
    num=979, title='在二叉树中分配硬币', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='递归返回（金币数, 节点数, 操作数）',
    tags=['贪心与思维', '链表树与回溯', '难度分 1709'],
    code='''
class Solution(object):
    def distributeCoins(self, root):

        s, cnt, res = self.dfs(root)
        return res
    
    def dfs(self, now):
        if not now:
            return 0, 0, 0
        
        s_l, cnt_l, res_l = self.dfs(now.left)
        s_r, cnt_r, res_r = self.dfs(now.right)
        res = res_l + res_r
        res += abs(s_l - cnt_l) + abs(s_r - cnt_r)
        
        return s_l + s_r + now.val, cnt_l + cnt_r + 1, res
''',
    call='''sol = Solution()
sol.tree = Tr([1,0,0,None,3])
sol.distributeCoins(sol.tree)''',
    expect=4,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回，标注 = 子树金币数 / 节点数）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=220, hide=('root',)),
    ],
    watch=[('now', lambda S: _nv(S['_inner'].get('now')), 'blue'),
           ('s_l', lambda S: S['_inner'].get('s_l'), 'cyan'), ('cnt_l', lambda S: S['_inner'].get('cnt_l'), 'cyan'),
           ('s_r', lambda S: S['_inner'].get('s_r'), 'pink'), ('cnt_r', lambda S: S['_inner'].get('cnt_r'), 'pink'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        's, cnt, res = self.dfs(root)': '从根出发：`dfs` 返回 ==(子树金币数, 子树节点数, 子树内部操作数)==',
        'if not now': lambda S, B, r: '空节点：金币、节点、操作都是 0' if S.now is None else f'节点 `{S.now.val}` 非空，先去求左右子树',
        'return 0, 0, 0': track('空子树 → 返回 `(0, 0, 0)`，==递归边界=='),
        's_l, cnt_l, res_l': track('递归左子树，拿到 `(金币数, 节点数, 操作数)`'),
        's_r, cnt_r, res_r': track(lambda S, B, r: f'左子树 `(s_l, cnt_l, res_l) = ({B.s_l}, {B.cnt_l}, {B.res_l})` 已拿到；再递归右子树'),
        'res = res_l + res_r': track(lambda S, B, r: f'左右子树内部的操作数相加：`res = {S.res_l} + {S.res_r} = {S.res}`'),
        'res += abs': track(lambda S, B, r: f'`now` 与两个孩子之间还要搬：左 `|{S.s_l} − {S.cnt_l}| = {abs(S.s_l - S.cnt_l)}`，右 `|{S.s_r} − {S.cnt_r}| = {abs(S.s_r - S.cnt_r)}` → `res = {B.res} + {abs(S.s_l - S.cnt_l) + abs(S.s_r - S.cnt_r)}` = =={S.res}=='),
        'return s_l + s_r': track(_cap_ret, record=True),
        'return res': '根的 `res` 就是答案：最少移动 `{res}` 次',
    },
    skip=[],
    cards=dict(
        one_liner='只数「每个节点和孩子之间」要搬多少枚',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['二叉树每个节点有 `val` 枚硬币，总数恰好等于节点数',
                 '一次移动：把一枚硬币移到相邻（父/子）节点',
                 '求让每个节点恰好 1 枚的最少移动次数',
                 '示例：`[3,0,0]` → `2`；本视频：`[1,0,0,null,3]` → `4`'],
        quote='若某棵子树中节点的数量不等于金币的数量，那么就需要从now移进或者移出一些金币，这个移动的量就是子树中节点数量与金币数量的差值。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个节点可能和父亲、孩子都交换，全算会重复 → ==只统计「与孩子」这一侧==',
              '递归返回三个值：子树金币数 `s`、节点数 `cnt`、内部操作数 `res`',
              '`res = res_l + res_r + |s_l − cnt_l| + |s_r − cnt_r|`',
              '子树金币和节点数的差，就是它和 `now` 之间要搬的数量'],
        result='运行结束，返回 `4`：各子树内部操作数一层层累加到根',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '操作数放在返回值里层层累加；灵神则用一个外部变量 `ans` 累加',
                 '易错：差值要取绝对值（缺硬币和多硬币都要搬）',
                 '原文为 Python 2 风格，仅沿用原代码，没有需要改动的地方',
                 '返回 `(金币, 节点)` 两个量；灵神的优化写法把它们合成一个 `d = 金币 − 节点`'],
    ),
)
