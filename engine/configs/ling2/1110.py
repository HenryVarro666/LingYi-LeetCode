VALS = [1, 2, 3, 4, 5, 6, 7]
TO_DEL = [3, 5]


def nv(x):
    return '空' if x is None else f'`{x.val}`'


def _color(S, n):
    if n.val in TO_DEL:
        return 'red'
    if n._uid in {t._uid for t in (S.get('ans') or [])}:
        return 'green'
    return None


def _forest(ans):
    return '，'.join(str(tree_list(t)) for t in ans) if ans else '（空）'


def _if_none(S, B, ret):
    if B.node is None:
        return '空节点 → 返回 `None`'
    return f'节点 `{B.node.val}`：后序遍历，==先处理两个儿子==，再决定自己'


def _keep(S, B, ret):
    v = S.node.val
    if v not in S.s:
        return f'`{v}` 不在 `s` 里 → 不删，返回自己（父节点照常连着它）'
    return f'`{v}` 在 `s` 里 → ==要删掉它==；先看它的儿子'


def _kid(side, word):
    def cap(S, B, ret):
        ch = getattr(S.node, side)
        if ch is not None:
            return f'被删节点的{word}儿子 `{ch.val}` 没被删 → ==它是一棵树的根==，加入答案'
        return f'{word}儿子为空（或已被删），不用管'
    return cap


CONFIG = dict(
    num=1110, title='删点成林', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='后序遍历 · 返回值更新儿子',
    tags=['字节30天'],
    code='''
class Solution:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        ans = []
        s = set(to_delete)
        def dfs(node: Optional[TreeNode]) -> Optional[TreeNode]:
            if node is None: return None
            node.left = dfs(node.left)
            node.right = dfs(node.right)
            if node.val not in s: return node
            if node.left: ans.append(node.left)
            if node.right: ans.append(node.right)
            return None
        if dfs(root): ans.append(root)
        return ans
''',
    call=f'Solution().delNodes(Tr({VALS}), {TO_DEL})',
    result_fn=lambda a: [tree_list(t) for t in a],
    expect=[[6], [7], [1, 2, None, 4]],
    views=[
        dict(type='text', fn=lambda S: f"`ans` = {_forest(S['ans'])}" if 'ans' in S else '', h=56),
        dict(type='tree', h=400, pointers={'node': 'blue'}, color=_color,
             label='树 / 森林（红 = 要删除，绿 = 森林里某棵树的根）'),
        dict(type='calls', h=200, label='调用栈'),
    ],
    watch=[('node', 'node', 'blue'), 's', ('ans', lambda S: [t.val for t in S['ans']] if 'ans' in S else None, 'green')],
    captions={
        'ans = []': '`ans` 存森林里每棵树的根',
        's = set(to_delete)': '把 `to_delete` 丢进哈希集合 `s`，`O(1)` 判断要不要删',
        'if node is None': _if_none,
        'node.left = dfs(node.left)': lambda S, B, r: f'递归左儿子 {nv(B.node.left)}：==返回值就是新的左儿子==（被删则为 None）',
        'node.right = dfs(node.right)': lambda S, B, r: f'递归右儿子 {nv(B.node.right)}：返回值就是新的右儿子',
        'if node.val not in s': _keep,
        'if node.left: ans.append': _kid('left', '左'),
        'if node.right: ans.append': _kid('right', '右'),
        'return None': lambda S, B, r: f'`{S.node.val}` 被删 → 返回 `None`，父节点把这一侧置空',
        'if dfs(root)': '从根开始 DFS',
        'return ans': lambda S, B, r: f'根 `{VALS[0]}` 没被删，也加入答案 → 返回森林 {_forest(r)}',
    },
    cards=dict(
        one_liner='后序遍历：被删节点的没被删的儿子，就是新树的根',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['二叉树每个节点值都不同；删去值在 `to_delete` 里的节点，得到一个森林',
                 '返回森林中每棵树的根（顺序任意）',
                 '示例：`root = [1,2,3,4,5,6,7], to_delete = [3,5]`',
                 '→ `[[1,2,null,4],[6],[7]]`'],
        quote='如果当前节点被删除，但是左儿子（右儿子）没被删除，意味着==左儿子（右儿子）是一棵树的根节点==，加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['后序遍历：先用递归的返回值==更新左右儿子==（被删的儿子返回 `None`）',
              '当前节点被删：没被删的儿子加入答案，自己返回 `None`',
              '最后，如果根节点没被删，把根节点加入答案'],
        result='返回 `[[6],[7],[1,2,null,4]]` ✓（顺序任意）',
        summary=['时间 `O(n + m)`：每个节点恰好递归一次；`m` 是 `to_delete` 长度',
                 '为什么后序：先处理儿子，返回时父节点才能把被删的儿子置空',
                 '易错：别忘了最后检查根节点是否要加入答案',
                 '`to_delete` 转成集合，否则每次判断 `O(m)`'],
    ),
)
