CONFIG = dict(
    num=513, title='找树左下角的值', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='BFS · 先右后左，最后出队的就是答案',
    tags=[],
    code='''
class Solution:
    def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
        q = deque([root])
        while q:
            node = q.popleft()
            if node.right: q.append(node.right)
            if node.left:  q.append(node.left)
        return node.val
''',
    call='Solution().findBottomLeftValue(Tr([1,2,3,4,None,5,6,None,None,7]))',
    expect=7,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前出队节点）', pointers={'node': 'blue'}, path=False, h=330),
        dict(type='queue', var='q', label='队列 q（队头在左）', fmt=lambda x: str(x.val), h=120),
    ],
    watch=[('node', lambda S: S['node'].val if S.get('node') else None, 'blue'), ('q', lambda S: [x.val for x in S['q']])],
    captions={
        'q = deque': '队列放入根节点 `{q[0].val}`',
        'while q': lambda S, B, r: (f'队列非空（还有 `{len(S.q)}` 个节点）→ 继续出队' if S.q else '队列空了 → 整棵树 BFS 完毕，`node` 停在最后一个出队的节点'),
        'node = q.popleft()': '队头出队：`node = {node.val}`',
        'if node.right': lambda S, B, r: (f'`{S.node.val}` 有右儿子 `{S.node.right.val}` → ==先==入队' if S.node.right else f'`{S.node.val}` 没有右儿子 → 跳过'),
        'if node.left': lambda S, B, r: (f'`{S.node.val}` 有左儿子 `{S.node.left.val}` → ==后==入队，它排在同层右边节点的后面' if S.node.left else f'`{S.node.val}` 没有左儿子 → 跳过'),
        'return node.val': '最后一个出队的节点 `{node.val}`：最底层、且同层里==最靠左== → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='BFS 时先入右儿子再入左儿子，最后出队的就是左下角',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定二叉树根节点 `root`，找出==最底层最左边==节点的值',
                 '示例：`[1,2,3,4,null,5,6,null,null,7]` → `7`（最后一层只有 7）'],
        quote='BFS 这棵二叉树，先把右儿子入队，再把左儿子入队，这样最后一个出队的节点就是左下角的节点了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['普通 BFS 按层、每层从左到右出队，最后出队的是右下角',
              '把入队顺序改成 ==先右后左==：每层从右到左出队',
              '于是整个队列的最后一个出队节点 = 最底层的最左节点'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '不需要记录层号，也不需要按层分批：只要入队顺序对，最后一个出队的就是答案',
                 '易错：`return node.val` 用的是循环结束后 `node` 的值，题目保证至少有一个节点',
                 '对比常规做法：按层遍历并记录每层第一个节点，写起来更长'],
    ),
)
