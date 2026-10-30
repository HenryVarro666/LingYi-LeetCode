CONFIG = dict(
    num='LCR 045', title='找树左下角的值', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='BFS · 先右后左，最后一个出队的就是答案',
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
        dict(type='queue', var='q', label='队列 q（队头在左；先进右儿子、再进左儿子）', fmt=lambda x: str(x.val), h=120),
        dict(type='text', size=28, h=60,
             fn=lambda S: f"当前出队 `{S['node'].val}`；它之后还有 `{len(S['q'])}` 个节点没出队" if S.get('node') is not None and 'q' in S else ''),
    ],
    watch=[('node', lambda S: S['node'].val if S.get('node') else None, 'blue'), ('队长', lambda S: len(S['q']) if 'q' in S else None)],
    captions={
        'q = deque': '队列先放根节点，开始 BFS',
        'while q': lambda S, B, r: (f'队列还有 `{len(S.q)}` 个节点 → 继续' if S.q else '队列空了：所有节点都出过队，最后出队的节点还留在 `node` 里'),
        'node = q.popleft()': '队头出队：节点 `{node.val}`（BFS 按层从上到下依次出队）',
        'if node.right': lambda S, B, r: (f'`{S.node.val}` 有右儿子 `{S.node.right.val}` → ==先==入队' if S.node.right else f'`{S.node.val}` 没有右儿子 → 跳过'),
        'if node.left': lambda S, B, r: (f'`{S.node.val}` 有左儿子 `{S.node.left.val}` → ==后==入队：同一层里左边的排在后面' if S.node.left else f'`{S.node.val}` 没有左儿子 → 跳过'),
        'return node.val': '最后一个出队的节点 = ==最底层、最左边==的节点 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='BFS 时先入右儿子再入左儿子，最后一个出队的就是左下角',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定二叉树根节点 `root`，找出==最底层最左边==节点的值',
                 '示例：`[2,1,3]` → `1`',
                 '本视频：`[1,2,3,4,null,5,6,null,null,7]` → `7`'],
        quote='q = deque([root])；while q: node = q.popleft()；先 append(node.right)，再 append(node.left)；循环结束 return node.val。',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['BFS 按层出队，最后一层一定最后出队',
              '每个节点都先入右儿子、后入左儿子 → 同一层里==从右往左==出队',
              '所以整棵树最后出队的节点，就是最底层最左边的那个，不需要记录层数'],
        summary=['时间 `O(n)`，空间 `O(n)`：满二叉树最后一层约 `n/2` 个节点在队列里',
                 '易错：入队顺序别写反；先左后右得到的是最底层最右边',
                 '题目保证至少一个节点，所以 `node` 一定被赋过值',
                 '常规写法要记录每层第一个节点；这里借入队顺序省掉了层数'],
    ),
)
