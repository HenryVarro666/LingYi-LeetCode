def _c(key):
    def f(S, n):
        if n.left is None and n.right is None and n.val in S.get(key, []):
            return 'green'
        return None
    return f


CONFIG = dict(
    num=872, title='叶子相似的树', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='两次 dfs 收集叶子，比较数组',
    tags=['灵神题单', '链表树与回溯', '难度分 1288'],
    code='''
class Solution(object):
    def leafSimilar(self, root1, root2):

        list1 = []
        list2 = []
        self.dfs(root1, list1)
        self.dfs(root2, list2)
        return list1 == list2
    
    def dfs(self, now, leaf_list):
        if not now.left and not now.right:
            leaf_list.append(now.val)
        else:
            if now.left:
                self.dfs(now.left, leaf_list)
            if now.right:
                self.dfs(now.right, leaf_list)
''',
    call='''s = Solution()
s.t1 = Tr([3,5,1,6,2,9,8])
s.t2 = Tr([1,6,5,None,None,2,7,None,None,9,8])
s.leafSimilar(s.t1, s.t2)''',
    expect=True,
    views=[
        dict(type='tree', var='self.t1', label='第 1 棵树（绿 = 已收集的叶子，蓝 = now）', pointers={'now': 'blue'}, h=230, color=_c('list1')),
        dict(type='tree', var='self.t2', label='第 2 棵树', pointers={'now': 'blue'}, h=230, color=_c('list2')),
        dict(type='text', fn=lambda S: f"`list1 = {S.get('list1')}`　`list2 = {S.get('list2')}`" if 'list1' in S else '', size=26, h=50),
        dict(type='calls', h=170, hide=('leaf_list',)),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'), ('list1', lambda S: S.get('list1'), 'green'), ('list2', lambda S: S.get('list2'), 'green')],
    captions={
        'list1 = []': '`list1` 存第 1 棵树的叶子值',
        'list2 = []': '`list2` 存第 2 棵树的叶子值',
        'self.dfs(root1': '对第 1 棵树 dfs，叶子都收进 `list1`',
        'self.dfs(root2': '第 1 棵收集完 `list1 = {list1}`；再对第 2 棵树 dfs，收进 `list2`',
        'if not now.left and not now.right': lambda S, B, r: (f'`{S.now.val}` ==没有左右孩子== → 它是叶子' if (not S.now.left and not S.now.right) else f'`{S.now.val}` 有孩子 → 不是叶子，往下递归'),
        'leaf_list.append': '叶子 `{now.val}` 加入数组 → `{leaf_list}`',
        'if now.left:': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 递归左边' if S.now.left else f'`{S.now.val}` 没有左孩子，跳过'),
        'if now.right:': lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 递归右边' if S.now.right else f'`{S.now.val}` 没有右孩子，跳过'),
        'self.dfs(now.left': '递归进入左孩子 `{B.now.left.val}`',
        'self.dfs(now.right': '递归进入右孩子 `{B.now.right.val}`',
        'return list1 == list2': lambda S, B, r: f'两个叶子数组 `{S.list1}` 与 `{S.list2}` 一致吗？→ =={r}==',
    },
    cards=dict(
        one_liner='对两棵树各 dfs 一次，叶子收进数组，最后比较数组',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['把一棵二叉树所有叶子从左到右排成「叶值序列」',
                 '两棵树的叶值序列相同，就是叶相似，返回 `true`',
                 '本视频：两棵形状不同的树，叶值序列都是 `[6, 2, 9, 8]` → `true`'],
        quote='叶子节点是没有左右孩子的节点，于是只需要对两棵树分别进行dfs，若当前节点没有左右孩子，那么该节点就是一个叶子节点，将其加入对应的数组',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now, leaf_list)` 把数组当参数传进去，叶子直接 `append`',
              '有孩子就先左后右递归，叶子的顺序就是从左到右',
              '`leafSimilar` 里建 `list1`、`list2`，dfs 两次后直接 `==` 比较'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '叶子 = ==没有左也没有右==；只缺一边的节点不是叶子',
                 '`dfs` 里先判叶子，else 里才递归，所以不会碰到空节点',
                 '对比灵神：灵神 `leafValues` 返回列表、遇空节点返回；yiduobo 把列表传参、只递归非空孩子',
                 '原文代码无需改动，已直接在 Python 3 运行'],
    ),
)
