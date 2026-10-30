def _leaves(n):
    if n is None:
        return []
    if n.left is None and n.right is None:
        return [n]
    return _leaves(n.left) + _leaves(n.right)


def _phase(S):
    r = S.get('root')
    if r is None:
        return 0
    return 1 if r._uid == S['self.t1']._uid else 2


def _color(which):
    def f(S, n):
        ph = _phase(S)
        if ph == 0 or n.left is not None or n.right is not None:
            return None
        if ph > which:
            return 'green'
        if ph == which and n.val in S.get('res', []):
            return 'green'
        return None
    return f


def _got(S, B, ret):
    return f'叶子 `{S.node.val}`：左右儿子都是空 → 把值加进 `res` → `{S.res}`'


def _ret(S, B, ret):
    return f'这棵树遍历完，叶值序列 `{ret}`'


def _info(S):
    ph = _phase(S)
    if ph == 0:
        return ''
    if ph == 1:
        return f'第 1 棵收集中：`res = {S.get("res")}`'
    return f'第 1 棵 `{[n.val for n in _leaves(S["self.t1"])]}`　第 2 棵收集中 `res = {S.get("res")}`'


CONFIG = dict(
    num=872, title='叶子相似的树', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS 收集叶值序列',
    tags=['灵神题单', '链表树与回溯', '难度分 1288'],
    code='''
class Solution:
    def leafValues(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:  # 空节点
                return
            if node.left is None and node.right is None:  # 叶子
                res.append(node.val)
                return
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return res

    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        return self.leafValues(root1) == self.leafValues(root2)
''',
    call='''s = Solution()
s.t1 = Tr([3,5,1,6,2,9,8])
s.t2 = Tr([1,6,5,None,None,2,7,None,None,9,8])
s.leafSimilar(s.t1, s.t2)''',
    expect=True,
    views=[
        dict(type='tree', var='self.t1', label='第 1 棵树（绿 = 已收集的叶子，蓝 = 当前节点）', pointers={'node': 'blue'}, h=230,
             color=_color(1)),
        dict(type='tree', var='self.t2', label='第 2 棵树', pointers={'node': 'blue'}, h=230,
             color=_color(2)),
        dict(type='text', fn=_info, size=26, h=50),
        dict(type='calls', h=170, hide=('leafValues',)),
    ],
    watch=[('node', lambda S: S['_inner'].get('node') and S['_inner']['node'].val, 'blue'), ('res', lambda S: S.get('res'), 'green')],
    captions={
        'res = []': '新建 `res`，存这棵树从左到右的叶子值',
        'if node is None': lambda S, B, r: ('空节点 → 直接返回' if S.node is None else f'节点 `{S.node.val}` 非空，看它是不是叶子'),
        'if node.left is None and node.right is None': lambda S, B, r: (f'`{S.node.val}` 左右儿子都空 → ==是叶子==' if S.node.left is None and S.node.right is None else f'`{S.node.val}` 还有儿子 → 不是叶子，继续往下走'),
        'res.append': _got,
        'dfs(node.left)': '先左子树：保证叶子按==从左到右==的顺序收集',
        'dfs(node.right)': '再右子树',
        'dfs(root)': '从根开始 DFS',
        'return res': _ret,
        'return self.leafValues(root1) ==': lambda S, B, r: ('分别算出两棵树的叶值序列，再比较它们是否相等' if r is None else f'两个叶值序列相等吗？→ =={r}=='),
    },
    cards=dict(
        one_liner='两棵树按同样的 DFS 顺序收集叶子，比较两个列表',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['叶子从左到右排成的值序列叫「叶值序列」',
                 '给两棵二叉树 `root1`、`root2`，叶值序列相同就叫叶相似，返回 `true`',
                 '本视频：叶值序列都是 `[6, 2, 9, 8]`，树形却不同 → `true`'],
        quote='按照同样的 DFS 顺序遍历这两棵二叉树，比如都按照先左子树再右子树的方式。遍历到叶子时，把节点值加到一个列表中。最后判断两个列表是否相同。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`leafValues` 只管一棵树：DFS 到叶子（左右儿子都空）就记录',
              '先左后右 → 叶子天然是从左到右',
              '`leafSimilar` 直接比较两棵树的返回列表'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`（两个列表 + 递归栈）',
                 '叶子 = 左右儿子==都==为空；只有一个儿子的节点不是叶子',
                 '必须两棵树用同样的遍历顺序（先左后右）',
                 '只有一个叶子的树（如单节点）也适用，根本身就是叶子'],
    ),
)
