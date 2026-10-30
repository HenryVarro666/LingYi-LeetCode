# ---- 树上“已返回”标注：caption 回调里记录每个节点的返回值，custom 叠加层（h=0）画在 tree 视图里的节点下方
TREE_H = 400
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
        s = '不平衡 -1' if d == -1 else f'高度 {d}'
        c = T['red'] if d == -1 else T['green']
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=c, width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, c, anchor='mm', bold=True)


def _nc(S, n):
    d = getattr(n, '_d', None)
    if d is None:
        return None
    return 'red' if d == -1 else 'green'


def cap_if(S, B, ret):
    return f'节点 `{S.now.val}` 非空，开始检查它'


def cap_hasl(S, B, ret):
    if S.now.left:
        return f'`{S.now.val}` 有左儿子 `{S.now.left.val}` → 递归检查左子树'
    return f'`{S.now.val}` 没有左儿子：左子树高度保持 `0`，==不递归空节点=='


def cap_hasr(S, B, ret):
    if S.now.right:
        tail = '（左边已经是 -1 了，这里==仍会继续递归==）' if S.left_height < 0 else ''
        return f'`{S.now.val}` 有右儿子 `{S.now.right.val}` → 递归检查右子树{tail}'
    return f'`{S.now.val}` 没有右儿子：右子树高度保持 `0`'


def cap_chk(S, B, ret):
    l, r = S.left_height, S.right_height
    if l < 0 or r < 0:
        return f'`left_height = {l}`，`right_height = {r}`：==有子树返回了 -1==，说明下面已经不平衡'
    if abs(l - r) > 1:
        return f'`|{l} - {r}| = {abs(l - r)} > 1`：节点 `{S.now.val}` 两边==高度差超过 1=='
    return f'`|{l} - {r}| = {abs(l - r)} ≤ 1`：以 `{S.now.val}` 为根的子树平衡'


CONFIG = dict(
    num=110, title='平衡二叉树', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='递归检查 + 返回高度（-1 表示不平衡）',
    tags=['热题173'],
    code='''
class Solution(object):
    def isBalanced(self, root):
        return self.check(root) >= 0

    def check(self, now):
        if now is None:
            return 0

        left_height = 0
        if now.left:
            left_height = self.check(now.left)

        right_height = 0
        if now.right:
            right_height = self.check(now.right)

        if left_height < 0 or right_height < 0 or abs(left_height - right_height) > 1:
            return -1

        return max(left_height, right_height) + 1
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,4,None,5,None,6])
s.isBalanced(s.tree)''',
    expect=False,
    skip=['left_height = 0', 'right_height = 0'],
    views=[
        dict(type='tree', label='二叉树（绿 = 已返回高度，红 = 返回 -1）', pointers={'now': 'blue'}, h=TREE_H, color=_nc),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=225),
    ],
    watch=[('now', 'now', 'blue'), ('left_height', lambda S: S['_inner'].get('left_height')),
           ('right_height', lambda S: S['_inner'].get('right_height'))],
    captions={
        'return self.check(root) >= 0': track(lambda S, B, ret: ('`check(root)` 返回高度；约定==不平衡就返回 -1==，所以 `>= 0` 就是平衡' if ret is None
                                                                 else f'返回 `{ret}`')),
        'if now is None': track(cap_if),
        'if now.left': track(cap_hasl),
        'left_height = self.check': track(lambda S, B, ret: f'递归 `check({S.now.val})`：左子树'),
        'if now.right': track(cap_hasr),
        'right_height = self.check': track(lambda S, B, ret: f'递归 `check({S.now.val})`：右子树'),
        'if left_height < 0': track(cap_chk),
        'return -1': track(lambda S, B, ret: (f'子树传上来的 -1 ==继续往上返回==：`check({S.now.val}) = -1`'
                                              if min(S.left_height, S.right_height) < 0
                                              else f'节点 `{S.now.val}` 处不平衡 → 返回 `-1`'), key='now'),
        'return max(': track(lambda S, B, ret: f'较高的一边加一作为当前高度：`max({S.left_height}, {S.right_height}) + 1 = {ret}`', key='now'),
    },
    max_steps=60,
    cards=dict(
        result='`check(root) = -1 < 0` → 返回 `False`；注意节点 2 已返回 -1，==右子树 3、5 仍被完整检查==',
        one_liner='边检查边算高度：平衡返回高度，不平衡返回 -1',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['判断二叉树是不是==平衡二叉树==',
                 '平衡：==每个节点==的左右子树高度差都不超过 1',
                 '示例：`[3,9,20,null,null,15,7]` → `true`',
                 '本视频：`[1,2,3,4,null,5,null,6]` → `false`'],
        quote='先分别递归求解左右子树是否满足平衡的条件，同时在求解过程中计算左右子树各自的高度。……方便起见，我在实现的时候约定如果不平衡，则返回-1，否则返回树的高度。',
        quote_src='—— yiduobo 题解',
        idea=['`check(now)`：一个返回值同时回答“平不平衡”和“有多高”',
              '有子树返回 -1，或两边高度差 > 1 → 当前也返回 -1',
              '否则返回 `max(左高, 右高) + 1`；没有儿子就不递归，高度直接记 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：-1 必须一路传上去，所以判断条件里要先看 `left_height < 0 or right_height < 0`',
                 '这份写法左边已经 -1 了还会继续递归右边；灵神写法二会提前退出，省掉这部分',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
