TREE_H = 340
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


def _i(x):
    return '∞' if x == inf or x == 1001 else str(x)


def track(fn, record=False):
    def cap(S, B, ret):
        node = S.get('node') if S.get('node') is not None else S.get('now')
        if record and node is not None:
            DONE[node._uid] = ret
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
        s = '/'.join(_i(v) for v in d)
        w = cv.tlen(s, 20, bold=True, mono=True) + 14
        cv.rect((X - w / 2, Y + rad + 5, X + w / 2, Y + rad + 33), fill=T['panel'], outline=T['green'], width=2, r=8)
        cv.text((X, Y + rad + 19), s, 20, T['green'], anchor='mm', bold=True, mono=True)
def _info(S):
    inn = S['_inner']
    base = '标注 ==own/fa/child==：自己装 / 靠父亲 / 靠孩子（1001 当作无穷大）'
    if 'now' not in inn or inn['now'] is None:
        return base
    parts = []
    for side in ('left', 'right'):
        if f'{side}_own' in inn:
            parts.append(f"{'左' if side == 'left' else '右'}孩子 `{_i(inn[side + '_own'])}/{_i(inn[side + '_fa'])}/{_i(inn[side + '_child'])}`")
    if not parts:
        return base
    return f"节点 `{inn['now'].val}`：" + '，'.join(parts)


def _case(S):
    inn = S['_inner']
    hl, hr = 'left_own' in inn, 'right_own' in inn
    return hl, hr


def cap_own(S, B, ret):
    inn = S['_inner']
    hl, hr = _case(S)
    if not hl and not hr:
        return '叶子：自己装一个摄像头 → ==own = 1=='
    if hl and not hr:
        return f"只有左孩子：自己装 → 左孩子装不装都行：`own = 1 + min({_i(inn['left_own'])}, {_i(inn['left_fa'])})` = =={inn['own']}=="
    if hr and not hl:
        return f"只有右孩子：自己装 → 右孩子装不装都行：`own = 1 + min({_i(inn['right_own'])}, {_i(inn['right_fa'])})` = =={inn['own']}=="
    return (f"自己装：两个孩子都可装可不装：`own = 1 + min({_i(inn['left_own'])}, {_i(inn['left_fa'])}) + "
            f"min({_i(inn['right_own'])}, {_i(inn['right_fa'])})` = =={inn['own']}==")


def cap_fa(S, B, ret):
    inn = S['_inner']
    hl, hr = _case(S)
    if not hl and not hr:
        return '叶子靠父亲监控，自己不装，没有孩子要管 → ==fa = 0=='
    if hl and not hr:
        return f"自己不装、父亲装：左孩子只能自己装或靠它的孩子：`fa = min({_i(inn['left_own'])}, {_i(inn['left_child'])})` = =={inn['fa']}=="
    if hr and not hl:
        return f"自己不装、父亲装：右孩子只能自己装或靠它的孩子：`fa = min({_i(inn['right_own'])}, {_i(inn['right_child'])})` = =={inn['fa']}=="
    return (f"自己不装、父亲装：`fa = min({_i(inn['left_own'])}, {_i(inn['left_child'])}) + "
            f"min({_i(inn['right_own'])}, {_i(inn['right_child'])})` = =={inn['fa']}==")


def cap_child(S, B, ret):
    inn = S['_inner']
    hl, hr = _case(S)
    if not hl and not hr:
        return '叶子没有孩子，不可能靠孩子监控 → `child = 1001`，==当作无穷大=='
    if hl and not hr:
        return f"靠孩子：唯一的左孩子必须装 → `child = left_own` = =={inn['child']}=="
    if hr and not hl:
        return f"靠孩子：唯一的右孩子必须装 → `child = right_own` = =={inn['child']}=="
    return (f"靠孩子：至少一个孩子要装，三种搭配（都装 / 只装左 / 只装右）取最小 = =={inn['child']}==")


def cap_ret(S, B, ret):
    return f"节点 `{S.now.val}` 的三种状态：own `{_i(ret[0])}`，fa `{_i(ret[1])}`，child `{_i(ret[2])}`"


CONFIG = dict(
    num=968, title='监控二叉树', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='树形 DP · 三种状态',
    tags=['灵神题单·动态规划', '难度分 2124'],
    code='''
class Solution(object):
    def minCameraCover(self, root):
        
        own, fa, child = self.dfs(root)
        return min(own, child)

    def dfs(self, now):
        if now.left:
            left_own, left_fa, left_child = self.dfs(now.left)
        if now.right:
            right_own, right_fa, right_child = self.dfs(now.right)
        
        if not now.left:
            if not now.right:
                own = 1
                fa = 0
                child = 1001
            else:
                own = 1 + min(right_own, right_fa)
                fa = min(right_own, right_child)
                child = right_own
        elif not now.right:
            own = 1 + min(left_own, left_fa)
            fa = min(left_own, left_child)
            child = left_own
        else:
            own = 1 + min(left_own, left_fa) + min(right_own, right_fa)
            fa = min(left_own, left_child) + min(right_own, right_child)
            child = min(left_own + right_own, left_own + right_child, right_own + left_child)

        return own, fa, child
''',
    call='''s = Solution()
s.tree = Tr([1,2,None,3,4])
s.minCameraCover(s.tree)''',
    expect=1,
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回 own/fa/child 的值）', pointers={'now': 'blue'}, h=TREE_H,
             color=lambda S, n: 'green' if getattr(n, '_d', None) is not None else None),
        dict(type='custom', draw=badges, h=0),
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='calls', h=200),
    ],
    watch=[('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue'),
           ('own', lambda S: S['_inner'].get('own'), 'green'),
           ('fa', lambda S: S['_inner'].get('fa'), 'yellow'),
           ('child', lambda S: S['_inner'].get('child'), 'cyan')],
    skip=['if now.left:', 'if now.right:'],
    max_steps=80,
    captions={
        'self.dfs(root)': track('从根开始 dfs：返回根的 `own / fa / child`，最后取 `own` 和 `child` 的较小值'),
        'self.dfs(now.left)': track(lambda S, B, r: f'先递归左孩子 `{B.now.left.val}`，得到它的三种状态'),
        'self.dfs(now.right)': track(lambda S, B, r: f'再递归右孩子 `{B.now.right.val}`，得到它的三种状态'),
        'if not now.left': track(lambda S, B, r: ('没有左孩子' if not S.now.left else '有左孩子') + ' → 按孩子情况分四类讨论'),
        'elif not now.right': track(lambda S, B, r: '有左孩子、没有右孩子：只看左孩子' if not S.now.right else '有左孩子，也有右孩子 → 两个孩子都要考虑'),
        'own = ': track(cap_own),
        'fa = ': track(cap_fa),
        'child = ': track(cap_child),
        'return own, fa, child': track(cap_ret, record=True),
        'return min(own, child)': track(lambda S, B, r: f'根没有父亲，不能靠父亲：`min(own, child)` = `min({_i(S.own)}, {_i(S.child)})` = =={r}=='),
    },
    cards=dict(
        one_liner='把「父亲有没有装」也写进状态：自己装、靠父亲、靠孩子',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['在二叉树的节点上装摄像头，每个摄像头能监控==父节点、自己、直接孩子==',
                 '求监控所有节点所需的最少摄像头数',
                 '示例：`[0,0,null,0,0]` → `1`',
                 '视频里为了区分节点，把值改写成 `1,2,null,3,4`'],
        quote='孩子节点可以监控到父亲节点，那么在设置状态的时候==必须涵盖父亲节点的状态==……分三种情况讨论，分别设为own，fa，child。',
        quote_src='—— yiduobo 题解原文',
        idea=['`own`：自己装摄像头；孩子装不装都行',
              '`fa`：自己不装，被父亲监控；孩子只能自己装或靠它的孩子',
              '`child`：自己不装，父亲也不装 → ==至少一个孩子要装==',
              '按「有无左右孩子」分四类写转移；没有孩子时 `child = 1001`（视作无穷大）'],
        summary=['只需一趟 dfs：时间 `O(n)`，空间 `O(n)`',
                 '`child = 1001` 是「不可能」的哨兵：题目节点数不超过 1000，足够大',
                 '根没有父亲，所以答案是 `min(own, child)`，不含 `fa`',
                 '对比灵神：他让空节点返回 `(inf, 0, 0)` 统一处理，不必分四类；yiduobo 的写法显式分了有无孩子',
                 '原文可直接在 Python 3 运行，未改动'],
    ),
)
