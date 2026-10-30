CONFIG = dict(
    num=2641, title='二叉树的堂兄弟节点 II', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='BFS · 层和 减 兄弟和',
    tags=['灵神题单', '链表树与回溯', '难度分 1677'],
    code='''
class Solution:
    def replaceValueInTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        root.val = 0
        q = [root]
        while q:
            tmp = q
            q = []

            # 计算下一层的节点值之和
            next_level_sum = 0
            for node in tmp:
                if node.left:
                    q.append(node.left)
                    next_level_sum += node.left.val
                if node.right:
                    q.append(node.right)
                    next_level_sum += node.right.val

            # 再次遍历，更新下一层的节点值
            for node in tmp:
                children_sum = (node.left.val if node.left else 0) + \\
                               (node.right.val if node.right else 0)
                if node.left: node.left.val = next_level_sum - children_sum
                if node.right: node.right.val = next_level_sum - children_sum
        return root
''',
    call='Solution().replaceValueInTree(Tr([5,4,9,1,10,None,7]))',
    expect=[0, 0, 0, 7, 7, None, 11],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 node）', pointers={'node': 'blue'}, path=False, h=300),
        dict(type='array', var=lambda S: [n.val for n in S['tmp']] if S.get('tmp') else [], label='tmp（当前层）', cell=60, h=100),
        dict(type='array', var=lambda S: [n.val for n in S['q']], label='q（下一层）', cell=60, h=100),
        dict(type='text', fn=lambda S: (f"下一层总和 `next_level_sum = {S.get('next_level_sum')}`" + (f"，兄弟和 `children_sum = {S.get('children_sum')}`" if S.get('children_sum') is not None else '')), size=26, h=56),
    ],
    watch=[('node', lambda S: S['node'].val if S.get('node') else None, 'blue'), ('next_level_sum', 'next_level_sum', 'yellow'), ('children_sum', lambda S: S.get('children_sum'), 'pink')],
    captions={
        'root.val = 0': '根没有堂兄弟 → 直接置 `0`',
        'q = [root]': '`q` 放根：第一层',
        'while q': lambda S, B, r: ('还有一层 → 继续处理' if S.q else '没有下一层了，整棵树更新完毕'),
        'tmp = q': '`tmp` 是当前层，它的儿子就是下一层',
        'q = []': '`q` 清空，用来收集==下一层==',
        'next_level_sum = 0': '先第一遍：求出下一层所有节点值之和',
        'for node in tmp': lambda S, B, r: f'取出当前层节点 `{S.node.val}`',
        'next_level_sum += node.left.val': '左儿子 `{node.left.val}` 入队并计入下一层总和 → `next_level_sum = {next_level_sum}`',
        'next_level_sum += node.right.val': '右儿子 `{node.right.val}` 入队并计入下一层总和 → `next_level_sum = {next_level_sum}`',
        'children_sum =': '`{node.val}` 的左右儿子（互为兄弟）值之和：`children_sum = {children_sum}`',
        'if node.left: node.left.val': lambda S, B, r: (f'==堂兄弟之和 = 本层总和 − 兄弟和== = `{S.next_level_sum} - {S.children_sum}` = `{S.next_level_sum - S.children_sum}`，写进左儿子' if S.node.left else f'`{S.node.val}` 没有左儿子 → 不用改'),
        'if node.right: node.right.val': lambda S, B, r: (f'同样 `{S.next_level_sum} - {S.children_sum}` = `{S.next_level_sum - S.children_sum}`，写进右儿子' if S.node.right else f'`{S.node.val}` 没有右儿子 → 不用改'),
        'return root': '返回改好的树：每个节点都变成了堂兄弟之和',
    },
    skip=['if node.left:', 'if node.right:', '(node.right.val if node.right else 0)'],
    cards=dict(
        one_liner='堂兄弟之和 = 这一层总和 − 自己和兄弟的和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把每个节点的值换成它所有==堂兄弟==节点值的和',
                 '堂兄弟：深度相同、父节点不同',
                 '示例：`[5,4,9,1,10,null,7]` → `[0,0,0,7,7,null,11]`'],
        quote='对于一个节点 x 来说，它的所有堂兄弟节点值的和，等于 x 这一层的所有节点值之和减去 x 及其兄弟节点的值之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先遍历当前层，求下一层的总和 `next_level_sum`，并把下一层入队',
              '再遍历当前层：兄弟们的和 `children_sum` 来自同一个父亲',
              '左右儿子都改成 `next_level_sum - children_sum`'],
        result='运行结束，树变为 `[0,0,0,7,7,null,11]`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：必须先算完整层总和，再改值，否则会读到改过的值',
                 '易错：根没有堂兄弟，要先置 `0`；缺失的儿子按 `0` 处理',
                 '换个角度：「堂兄弟」就是同层中父亲不同的节点，层和减兄弟和即可'],
    ),
)
