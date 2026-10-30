TREE_H = 330


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
        X, Y = pos[n._uid]
        s = f'len={n.len}' if n.len else '叶子'
        w = cv.tlen(s, 18, bold=True) + 14
        cv.rect((X - w / 2, Y + rad + 4, X + w / 2, Y + rad + 28), fill=T['panel'], outline=T['border'], width=2, r=8)
        cv.text((X, Y + rad + 16), s, 18, T['yellow'] if n.len else T['green'], anchor='mm', bold=True)


def _info(S):
    r = S['_inner'].get('root')
    k = S['_inner'].get('k')
    if r is None:
        return ''
    if r.len == 0:
        return f'当前 `k = {k}`，节点是==叶子==，字符串 `"{r.val}"`'
    lc = max(r.left.len, len(r.left.val)) if r.left else 0
    return f'当前 `k = {k}`，左子树字符数 `p = {lc}`'


def cap_leaf(S, B, ret):
    return f'`len == 0` → 叶子节点，直接取 `"{S.root.val}"[{S.k} - 1]` = =={ret}=='


def cap_cmp(S, B, ret):
    r = B.root
    p = max(r.left.len, len(r.left.val))
    if p >= B.k:
        return f'左子树有 `{p}` 个字符 >= `k = {B.k}` → 第 k 个字符在==左子树==里'
    return f'左子树只有 `{p}` 个字符 < `k = {B.k}` → 第 k 个字符在==右子树==里'


CONFIG = dict(
    num=2689, title='从Rope树中提取第K个字符', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 按左子树长度分流',
    tags=['灵神题单', '链表树与回溯'],
    setup='''
class RopeTreeNode(TreeNode):
    def __init__(self, len=0, val="", left=None, right=None):
        super().__init__(val, left, right)
        self.len = len
''',
    code='''
class Solution(object):
    def getKthCharacter(self, root, k):

        if root.len == 0:
            return root.val[k - 1]
        
        if root.left:
            if max(root.left.len, len(root.left.val)) >= k:
                return self.getKthCharacter(root.left, k)
            else:
                return self.getKthCharacter(root.right, k - max(root.left.len, len(root.left.val)))
        else:
            return self.getKthCharacter(root.right, k)
''',
    call='''s = Solution()
A, B_, C = RopeTreeNode(0, "ab"), RopeTreeNode(0, "cd"), RopeTreeNode(0, "ef")
X = RopeTreeNode(4, "", A, B_)
s.tree = RopeTreeNode(6, "", X, C)
s.getKthCharacter(s.tree, 3)''',
    expect='c',
    views=[
        dict(type='text', fn=_info, size=26, h=56),
        dict(type='tree', label='Rope 树（蓝 = root；叶子存字符串，内部节点存总长 len）', pointers={'root': 'blue'}, h=TREE_H),
        dict(type='custom', draw=badges, h=0),
        dict(type='calls', h=200),
    ],
    watch=[('root.len', lambda S: S['_inner'].get('root').len if S['_inner'].get('root') else None, 'blue'),
           ('k', lambda S: S['_inner'].get('k'), 'yellow')],
    captions={
        'if root.len == 0': '`root.len = {root.len}`：==等于 0 是叶子==，不等于 0 是内部节点',
        'return root.val[k - 1]': cap_leaf,
        'if root.left:': lambda S, B, r: ('内部节点有左孩子 → 要比较 `k` 和左子树的字符数' if B.root.left else '没有左孩子 → 答案一定在右子树'),
        'if max(root.left.len': cap_cmp,
        'return self.getKthCharacter(root.left, k)': '进入左子树，`k` 不变 = `{k}`',
        'k - max(': '进入右子树，左边 `{B.k - k}` 个字符都不要了，`k` 变成 `{B.k} - {B.k - k} = {k}`',
        'return self.getKthCharacter(root.right, k)': '没有左孩子，直接进入右子树，`k` 不变',
    },
    cards=dict(
        one_liner='看左子树有多少字符：k 落在左边就往左，否则减去 p 往右',
        complexity='时间 `O(h)`（一条路径），空间 `O(h)`',
        problem=['Rope 树：叶子节点存字符串 `val`（`len = 0`），内部节点存左右子树字符串拼接后的总长 `len`（`val` 为空）',
                 '给定根 `root` 和 `k`，返回整棵树表示的字符串的第 `k` 个字符（从 1 开始）',
                 '本视频：`"ab" "cd" "ef"` 组成的树，`k = 3` → `c`'],
        quote='若当前的root.len等于0，那么说明当前是一个叶子节点，其对应的第k个字符自然就是root.val[k - 1]。否则的话说明这是一个内部节点，此时就需要在其左子树或者右子树中递归求解。',
        quote_src='—— yiduobo 题解',
        idea=['叶子：`len == 0`，直接下标取字符',
              '内部节点：左子树字符数 `p = max(left.len, len(left.val))`',
              '`k <= p` 去左子树；否则去右子树，`k` 减去 `p`（无左孩子则必在右）'],
        result='返回 `c`：先去左子树 `"abcd"`，再去其右叶子 `"cd"` 的第 1 个字符',
        summary=['时间 `O(h)`，空间 `O(h)`：每层只走一个方向',
                 '易错：`k` 从 1 开始，叶子里用 `val[k - 1]`',
                 '`max(left.len, len(left.val))` 同时兼容叶子（`len=0`）和内部节点（`val` 为空）',
                 '去右子树时一定要把 `k` 减掉左边的字符数'],
    ),
)
