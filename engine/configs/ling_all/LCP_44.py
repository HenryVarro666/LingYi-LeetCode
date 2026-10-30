CONFIG = dict(
    num='LCP 44', title='开幕式焰火', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS + 哈希集合',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution:
    def numColor(self, root: TreeNode) -> int:
        s = set()
        def dfs(node: Optional[ListNode]) -> None:
            if node is None:
                return
            s.add(node.val)
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return len(s)
''',
    call='''s = Solution()
s.tree = Tr([1,3,2,1,None,2])
s.numColor(s.tree)''',
    expect=3,
    views=[
        dict(type='tree', var='self.tree', label='焰火二叉树（蓝 = 当前节点）', pointers={'node': 'blue'}, h=250),
        dict(type='set', var='s', label='颜色集合 s', fmt=lambda x: str(x), h=110),
        dict(type='calls', h=200),
    ],
    watch=[('node', lambda S: S['_inner'].get('node') and S['_inner']['node'].val, 'blue'), ('len(s)', lambda S: len(S['s']) if 's' in S else 0, 'green')],
    captions={
        's = set()': '建一个空的哈希集合：重复的颜色==自动去重==',
        'if node is None': lambda S, B, r: ('空节点 → 没有颜色，直接返回' if S.node is None else f'节点 `{S.node.val}` 非空，它的颜色要记下来'),
        6: '空节点，返回上一层',
        's.add': lambda S, B, r: (f'颜色 `{S.node.val}` 加入集合；已有过，集合不变 → `{sorted(S.s)}`' if S.node.val in B.s else f'颜色 `{S.node.val}` 是新颜色，加入集合 → `{sorted(S.s)}`'),
        'dfs(node.left)': '遍历左子树',
        'dfs(node.right)': '遍历右子树',
        'dfs(root)': '从根节点开始遍历（先序）',
        'return len(s)': '答案就是集合的大小 `len(s) = {len(s)}`',
    },
    cards=dict(
        one_liner='遍历整棵树，把颜色丢进哈希集合，数集合大小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一棵二叉树代表焰火，节点值是该位置的颜色',
                 '求焰火一共有多少种==不同==的颜色',
                 '本视频：`root = [1,3,2,1,null,2]` → 颜色 `1、2、3` 共 `3` 种'],
        quote='遍历的同时用哈希集合统计节点值。答案为哈希集合的大小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['递归遍历每个节点，空节点直接返回',
              '`s.add(node.val)`：集合自动去掉重复颜色',
              '最后 `len(s)` 就是不同颜色数'],
        summary=['时间 `O(n)`，空间 `O(n)`（集合 + 递归栈）',
                 '遍历顺序无所谓，先序、中序、后序都行',
                 '别用 `len(节点)` 代替 `len(集合)`：重复颜色只算一次',
                 '同类题见灵神的二叉树题单（遍历二叉树）'],
    ),
)
