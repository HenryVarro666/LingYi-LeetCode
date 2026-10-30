CH = {6: (2, 8), 2: (0, 4), 8: (7, 9), 4: (3, 5)}


def _path_vals(S):
    r = S.get('root')
    if r is None:
        return set()
    cur, out = 6, {6}
    while cur != r.val and cur in CH:
        cur = CH[cur][0] if r.val < cur else CH[cur][1]
        out.add(cur)
    return out


def _is(a, b):
    return a is not None and b is not None and a._uid == b._uid


def _color(S, n):
    if _is(n, S.get('p')):
        return 'green'
    if _is(n, S.get('q')):
        return 'pink'
    if n.val in _path_vals(S):
        return 'yellow'
    return None


def _rel(S):
    r = (S.get('_inner') or {}).get('root') or S.get('root')
    if r is None or 'p' not in S:
        return ''
    p, q, x = S['p'].val, S['q'].val, r.val
    if p < x and q < x:
        return f'x = `{x}`：`{p}` < `{x}` 且 `{q}` < `{x}` → 都在==左子树=='
    if p > x and q > x:
        return f'x = `{x}`：`{p}` > `{x}` 且 `{q}` > `{x}` → 都在==右子树=='
    return f'x = `{x}`：`{min(p, q)}` ≤ `{x}` ≤ `{max(p, q)}` → ==其它==情况，答案就是当前节点'


def _cap_x(S, B, ret):
    return f'当前节点值 `x = {S.x}`，拿 p、q 的值和它比大小'


def _cap_if1(S, B, ret):
    x, p, q = S.x, S.p.val, S.q.val
    if p < x and q < x:
        return f'`{p}` 和 `{q}` 都 < `{x}` → p 和 q ==都在左子树==，答案也在左子树'
    return f'`{p}`、`{q}` 不都小于 `{x}` → 不全在左子树'


def _cap_if2(S, B, ret):
    x, p, q = S.x, S.p.val, S.q.val
    if p > x and q > x:
        return f'`{p}` 和 `{q}` 都 > `{x}` → p 和 q ==都在右子树=='
    return f'`{p}`、`{q}` 也不都大于 `{x}` → p、q 分在两侧，或者 `{x}` 就是 p/q'


def _cap_ret_left(S, B, ret):
    if ret is None:
        return f'递归左子树：进入 `{B.root.left.val}`，答案原样往上返回'
    return f'左子树返回了 `{ret.val}` → 原样往上返回'


def _cap_ret_right(S, B, ret):
    if ret is None:
        return f'递归右子树：进入 `{B.root.right.val}`，答案原样往上返回'
    return f'右子树返回了 `{ret.val}` → 原样往上返回'


CONFIG = dict(
    num=235, title='二叉搜索树的最近公共祖先', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='分类讨论 · 递归',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        x = root.val
        if p.val < x and q.val < x:  # p 和 q 都在左子树
            return self.lowestCommonAncestor(root.left, p, q)
        if p.val > x and q.val > x:  # p 和 q 都在右子树
            return self.lowestCommonAncestor(root.right, p, q)
        return root  # 其它
''',
    call='''root = Tr([6,2,8,0,4,7,9,None,None,3,5])
p = root.left.right.left
q = root.left.right.right
Solution().lowestCommonAncestor(root, p, q)''',
    result_fn=lambda x: x.val,
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"p = `{S['p'].val}`（绿）　q = `{S['q'].val}`（粉）　BST：左 < 根 < 右"
                                        if 'p' in S else ''), size=26, h=60),
        dict(type='tree', h=440, path=False, label='二叉搜索树（蓝箭头 = 当前 root，黄 = 递归经过的节点）',
             pointers={'root': 'blue'}, color=_color),
        dict(type='text', fn=_rel, h=70),
        dict(type='calls', h=170, hide=('p', 'q')),
    ],
    watch=[('x', 'x', 'blue'),
           ('p.val', lambda S: S['p'].val if 'p' in S else None, 'green'),
           ('q.val', lambda S: S['q'].val if 'q' in S else None, 'pink')],
    captions={
        'x = root.val': _cap_x,
        'if p.val < x': _cap_if1,
        'return self.lowestCommonAncestor(root.left': _cap_ret_left,
        'if p.val > x': _cap_if2,
        'return self.lowestCommonAncestor(root.right': _cap_ret_right,
        'return root  #': '其它情况：p、q 不在同一侧子树（或当前节点就是 p/q）→ 当前节点 `{ret.val}` ==就是最近公共祖先==',
    },
    max_steps=30,
    cards=dict(
        one_liner='分类讨论：都在左递归左，都在右递归右，其它情况返回当前节点',
        complexity='时间 `O(n)`，空间 `O(n)`（树可能退化成链）',
        problem=['给定一棵==二叉搜索树==和其中两个节点 `p`、`q`，找它们的最近公共祖先',
                 '一个节点也可以是它自己的祖先；所有节点值唯一',
                 '示例：`root = [6,2,8,0,4,7,9,null,null,3,5]`',
                 '`p = 2, q = 8 → 6`；`p = 2, q = 4 → 2`；本视频 `p = 3, q = 5 → 4`'],
        quote='在二叉搜索树的情况下，只有发现 p（或者 q）在左/右子树中才会递归左/右子树，这==间接说明递归到的节点一定不是空节点==',
        quote_src='—— 灵茶山艾府题解（答疑）',
        idea=['设当前节点值为 `x`，按 p、q 与 `x` 的大小分类讨论',
              '`p.val`、`q.val` 都 `< x` → 都在左子树，递归左子树；都 `> x` → 递归右子树',
              '其它情况（分居两侧，或 `x` 就是 p/q）→ 当前节点就是答案',
              '和 236 不同：只往有 p、q 的那边递归，所以==不用判断空节点=='],
        summary=['时间 `O(n)`：题目没保证平衡，最坏退化成链；空间 `O(n)` 递归栈',
                 '易错：比较用严格的 `<` / `>`，等于时属于「其它」，返回当前节点',
                 '每层只递归一边，本质是==从根往下走一条路==，也可改成 `while` 迭代做到 `O(1)` 空间',
                 '对比 236：普通二叉树没有大小关系，要递归左右两边再合并'],
    ),
)
