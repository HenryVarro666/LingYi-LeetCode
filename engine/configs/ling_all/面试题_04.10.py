def _nv(x):
    return '空' if x is None else str(x.val)


def _dfs_cap(S, B, ret):
    if S.node is None:
        return '空节点：高度 `0`，当然找不到 `subRoot` → 返回 `(0, False)`'
    return f'进入节点 `{S.node.val}`：先递归左右儿子，拿到它们的高度和「是否已找到」'


def _found(S, B, ret):
    return f'左右子树里已经找到了 `subRoot` → ==直接向上传 True==，不再算高度，也不再匹配'


def _h(S, B, ret):
    return (f'节点 `{S.node.val}` 的高度 `max({S.left_h}, {S.right_h}) + 1 = {S.node_h}`；'
            f'`hs = {S.hs}`')


def _ret(S, B, ret):
    if S.node_h != S.hs:
        return f'节点 `{S.node.val}` 高度 `{S.node_h}` ≠ `hs = {S.hs}` → ==不可能相同，跳过匹配==，返回 `False`'
    return (f'节点 `{S.node.val}` 高度 `{S.node_h}` = `hs`：只有高度相同才值得做 `isSameTree` → '
            f'结果 =={ret[1]}==')


CONFIG = dict(
    num='面试题 04.10', title='检查子树', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='只在高度相同时匹配',
    tags=[],
    code='''
class Solution:
    # 代码逻辑同 104. 二叉树的最大深度
    def getHeight(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        left_h = self.getHeight(root.left)
        right_h = self.getHeight(root.right)
        return max(left_h, right_h) + 1

    # 100. 相同的树
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None or q is None:
            return p is q  # 必须都是 None
        return p.val == q.val and \\
            self.isSameTree(p.left, q.left) and \\
            self.isSameTree(p.right, q.right)

    def checkSubTree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        hs = self.getHeight(subRoot)

        # 返回 node 的高度，以及是否找到了 subRoot
        def dfs(node: Optional[TreeNode]) -> (int, bool):
            if node is None:
                return 0, False
            left_h, left_found = dfs(node.left)
            right_h, right_found = dfs(node.right)
            if left_found or right_found:
                return 0, True
            node_h = max(left_h, right_h) + 1
            return node_h, node_h == hs and self.isSameTree(node, subRoot)
        return dfs(root)[1]
''',
    call='''s = Solution()
s.t1 = Tr([3, 4, 5, 1])
s.t2 = Tr([4, 1])
s.checkSubTree(s.t1, s.t2)''',
    expect=True,
    views=[
        dict(type='tree', var='self.t1', label='root（t1）', pointers={'node': 'blue'}, h=250,
             color=lambda S, n: 'green' if S.get('node') is not None and n is S.get('node') and S.get('node_h') == S.get('hs') else None),
        dict(type='tree', var='self.t2', label='subRoot（t2）', path=False, h=200),
        dict(type='calls', h=170, hide=('root', 'subRoot')),
    ],
    watch=[('hs', 'hs', 'yellow'), ('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') is not None else None, 'blue'),
           ('node_h', lambda S: S['_inner'].get('node_h'), 'green')],
    skip=['if left_found or right_found', 'left_h = self.getHeight', 'right_h = self.getHeight'],
    captions={
        'hs = self.getHeight': '先算 `subRoot` 的高度 `hs = {hs}`：以后只有高度等于 `hs` 的节点才可能与它相同',
        'return max(left_h, right_h) + 1': '`getHeight` 返回 `max({left_h}, {right_h}) + 1 = {ret}`（同 104 题）',
        'if node is None': _dfs_cap,
        'left_h, left_found = dfs': '递归左儿子 `dfs({_nv(S.node.left)})`：返回它的高度和是否找到',
        'right_h, right_found = dfs': '左边：高度 `{left_h}`，找到 `{left_found}`；再递归右儿子',
        'return 0, True': _found,
        'node_h = max': _h,
        'return node_h, node_h == hs': _ret,
        'return dfs(root)[1]': '从根开始 `dfs(root)`，最后取返回值的第二项：是否找到',
        'return p.val == q.val': lambda S, B, ret: f'比较 `p.val = {S.p.val}`、`q.val = {S.q.val}`，相同才继续比左右子树',
        'return p is q': lambda S, B, ret: ('其中一个为空 → 必须==两个都为空==才算相同：' + f'`{ret}`'),
    },
    max_steps=90,
    cards=dict(
        one_liner='先算 subRoot 的高度，只在高度相同的节点上做匹配',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['判断 `t2` 是否为 `t1` 的子树：`t1` 中存在节点 `n`，从 `n` 砍断后与 `t2` ==一模一样==',
                 '示例：`t1 = [1,2,3], t2 = [2]` → `true`',
                 '本视频：`t1 = [3,4,5,1,2]`，`t2 = [4,1,2]` → `true`'],
        quote='对于 root 中的所有与 hs 高度相同的节点，对应的子树==两两不相交==，这些子树的节点个数之和不超过 n。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['暴力法：对每个节点都跑一遍「相同的树」，链状且值全相同时退化成 `O(n·min(n,m))`',
              '高度相同的两个节点不可能互为祖先，子树互不相交 → 匹配总代价 `O(n)`',
              '`dfs` 同时返回「高度」和「是否找到」，找到后一路向上传 True'],
        result='在节点 `4` 处高度和结构都匹配 → 返回 `True`',
        summary=['时间 `O(n+m)`：dfs 每个节点只访问一次，所有匹配的总代价不超过 n',
                 '易错：`subRoot` 与 `root` 前几个节点匹配也不行，节点的儿子必须也相同（示例 2）',
                 '`isSameTree` 里空节点要用 `p is q`：必须两个都为空',
                 '方法一（暴力）：`checkSubTree` 自己递归遍历，每个节点都调用 `isSameTree`'],
    ),
)
