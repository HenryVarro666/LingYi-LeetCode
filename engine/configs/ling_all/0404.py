# 记录哪些左叶子的值已经被累加（caption 回调里按步骤顺序记录），给树上色用
ADD = set()


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


def mark(fn, add=False):
    def cap(S, B, ret):
        if add:
            ADD.add(S.left._uid)
        t = S.get('self.tree')
        for n in _walk(t):
            n._lf = n._uid in ADD
        return fn(S, B, ret) if callable(fn) else fn
    return cap


def _nv(n):
    return '空' if n is None else str(n.val)


def _is_leaf(n):
    return n is not None and n.left is None and n.right is None


CONFIG = dict(
    num=404, title='左叶子之和', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 判断左儿子是不是叶子',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution:
    def sumOfLeftLeaves(self, root: TreeNode) -> int:
        if root is None:  # 空节点
            return 0

        # 递归左右子树，收集左右子树中的「节点的左儿子是叶子」的叶子节点值之和
        ans = self.sumOfLeftLeaves(root.left) + self.sumOfLeftLeaves(root.right)

        left = root.left  # 当前节点的左儿子
        if left and left.left is None and left.right is None:  # 当前节点的左儿子是叶子
            ans += left.val  # 累加节点值

        return ans
''',
    call='''s = Solution()
s.tree = Tr([3,9,20,None,None,15,7])
s.sumOfLeftLeaves(s.tree)''',
    expect=24,
    views=[
        dict(type='tree', var='self.tree', label='二叉树（蓝 = root，绿 = 已被累加的左叶子）', pointers={'root': 'blue'}, h=270,
             color=lambda S, n: 'green' if getattr(n, '_lf', False) else None),
        dict(type='text', fn=lambda S: f"当前这一层：`root = {_nv(S.get('root'))}`，左儿子 `{_nv(S['root'].left) if S.get('root') else '—'}`", size=26, h=56),
        dict(type='calls', h=230),
    ],
    watch=[('root', lambda S: S['_inner'].get('root') and S['_inner']['root'].val, 'blue'), ('ans', lambda S: S['_inner'].get('ans'), 'green')],
    captions={
        'if root is None': mark(lambda S, B, r: ('空节点 → 没有左叶子，返回 `0`' if S.root is None else f'节点 `{S.root.val}` 非空，先去左右子树收集左叶子')),
        'return 0': mark('==递归边界==：空节点返回 `0`，交给上一层去相加'),
        'ans = self': mark(lambda S, B, r: (f'左右子树的左叶子之和已拿到：`ans = {S.ans}`（还没算 `{S.root.val}` 自己的左儿子）' if 'ans' in S['_inner'] else f'递归左右子树：先把节点 `{B.root.val}` 两边子树各自的左叶子和求出来')),
        'left = root.left': mark(lambda S, B, r: f'取出左儿子 `left = {_nv(S.left)}`'),
        'if left and': mark(lambda S, B, r: (f'`{S.left.val}` 左右儿子都空 → ==是叶子==，而且是左儿子 → 是左叶子' if _is_leaf(S.left) else ('没有左儿子 → 没有左叶子' if S.left is None else f'左儿子 `{S.left.val}` 还有孩子 → 不是叶子，不累加'))),
        'ans += left.val': mark(lambda S, B, r: f'左叶子 `{S.left.val}` 累加：`ans` → =={S.ans}==', add=True),
        'return ans': mark(lambda S, B, r: f'节点 `{S.root.val}` 这棵子树的左叶子之和 = `{r}`，返回给上一层'),
    },
    cards=dict(
        one_liner='父节点看一眼左儿子：是叶子就累加，其余交给递归',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['给定二叉树的根节点 `root`，返回所有==左叶子==之和',
                 '左叶子：是父节点的左儿子，并且自己没有孩子',
                 '本视频：`root = [3,9,20,null,null,15,7]`，左叶子 `9` 和 `15` → `24`'],
        quote='如果当前节点的左儿子是叶子，即==左儿子的左右儿子均为空==，那么把左儿子的节点值加到答案中。',
        quote_src='—— 灵茶山艾府题解（写法一）',
        idea=['视频用写法二：直接把 `sumOfLeftLeaves` 当递归函数，返回「这棵子树的左叶子和」',
              '`ans` = 左子树的和 + 右子树的和',
              '再看自己的左儿子：是叶子就把它的值加进 `ans`'],
        summary=['时间 `O(n)`，空间 `O(h)`：`h` 是树高，即递归栈深度',
                 '只有「是父节点的左儿子」的叶子才算；根节点单独一个也不算左叶子',
                 '写法一：用外层变量 `ans` + 内层 `dfs`（`nonlocal`），先递归再判断左儿子',
                 '判断顺序不能反：先 `left and`，再看 `left.left`、`left.right`，否则空指针'],
    ),
)
