def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    p, q = S.p, S.q
    if p is None or q is None:
        return f'`p = {nv(p)}`、`q = {nv(q)}`：至少一个为空 → 进入==递归边界==，看是不是两个都空'
    return f'`p = {p.val}`、`q = {q.val}` 都不为空 → 比较值，再比较它们的子树'


def cap_ret0(S, B, ret):
    assert ret is not None
    if ret:
        return '两个都是空 → 对称，返回 `True`'
    return f'一个空一个不空（`{nv(S.p)}` 和 `{nv(S.q)}`）→ 不对称，返回 `False`'


def cap_ret1(S, B, ret):
    assert ret is not None
    p, q = S.p, S.q
    if ret:
        return f'节点 `{p.val}` 与 `{q.val}`：值相等，且 外侧对外侧、内侧对内侧 都对称 → 返回 `True`'
    return f'节点 `{p.val}` 与 `{q.val}` 不对称 → 返回 `False`'


CONFIG = dict(
    num='LCR 145', title='判断对称二叉树', difficulty='Easy', category='二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 左子树与右子树镜像比较',
    tags=[],
    code='''
class Solution:
    # 在【100. 相同的树】的基础上稍加改动
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None or q is None:
            return p is q
        return p.val == q.val and self.isSameTree(p.left, q.right) and self.isSameTree(p.right, q.left)

    def checkSymmetricTree(self, root: Optional[TreeNode]) -> bool:
        return root is None or self.isSameTree(root.left, root.right)
''',
    call='''s = Solution()
s.tree = Tr([6,7,7,8,9,9,8])
s.checkSymmetricTree(s.tree)''',
    expect=True,
    views=[
        dict(type='tree', label='二叉树（蓝 = p，粉 = q）', pointers={'p': 'blue', 'q': 'pink'}, h=380, path=False),
        dict(type='calls', h=250),
    ],
    watch=[('p', lambda S: S['_inner'].get('p').val if S['_inner'].get('p') else None, 'blue'),
           ('q', lambda S: S['_inner'].get('q').val if S['_inner'].get('q') else None, 'pink')],
    captions={
        'if p is None or q is None': cap_if,
        'return p is q': cap_ret0,
        'return p.val == q.val': cap_ret1,
        'return root is None': lambda S, B, ret: (None if ret is None else '空树 → 对称' if S.root is None else
                                                  f'把根的左右子树 `{nv(S.root.left)}` 和 `{nv(S.root.right)}` 当成两棵树，看它们是否镜像 → ==`{ret}`==')
    },
    cards=dict(
        one_liner='对称 = 左子树和右子树互为镜像：比较时「外对外、内对内」',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断一棵二叉树是否==轴对称==',
                 '示例：`root = [6,7,7,8,9,9,8]` → `true`',
                 '示例：`root = [1,2,2,null,3,null,3]` → `false`'],
        quote='在【100. 相同的树】的基础上稍加改动',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['先会「相同的树」：两棵树 `p`、`q` 每个位置的值都一样',
              '镜像只改一处：`p.left` 对 `q.right`，`p.right` 对 `q.left`',
              '根的左右子树当作 `p` 和 `q` 传进去；空树直接对称'],
        summary=['时间 `O(n)`；空间 `O(n)`：退化成链时递归栈有 `n` 层',
                 '`p is q`：两个都为 `None` 才是 `True`，一空一不空是 `False`',
                 '易错：别写成 `p.left` 对 `q.left`，那是判断相同而不是对称',
                 '`and` 会短路：左边已经不对称，右边不再递归'],
    ),
)
