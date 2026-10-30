CONFIG = dict(
    num=107, title='二叉树的层序遍历 II', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='BFS · 一个队列 + 反转答案',
    tags=[],
    code='''
class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []
        ans = []
        q = deque([root])
        while q:
            vals = []
            for _ in range(len(q)):
                node = q.popleft()
                vals.append(node.val)
                if node.left:  q.append(node.left)
                if node.right: q.append(node.right)
            ans.append(vals)
        return ans[::-1]
''',
    call='Solution().levelOrderBottom(Tr([3,9,20,None,None,15,7]))',
    expect=[[15, 7], [9, 20], [3]],
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前出队节点）', pointers={'node': 'blue'}, path=False, h=300),
        dict(type='queue', var='q', label='队列 q', fmt=lambda x: str(x.val), h=110),
        dict(type='array', var='vals', label='vals（当前层）', cell=72, h=120),
        dict(type='text', fn=lambda S: f"`ans = {S['ans']}`" if 'ans' in S else '', size=26, h=56),
    ],
    watch=[('node', lambda S: S['node'].val if S.get('node') else None, 'blue'), 'vals', ('ans', 'ans', 'green')],
    captions={
        'if root is None': '空树没有任何层 → 直接返回 `[]`',
        'q = deque': '队列里先放根节点：此时队列里恰好是第一层',
        'while q': '`q` 里装着==当前这一层==的所有节点；非空就继续处理一层',
        'vals = []': '开一个新的 `vals`，收集这一层的节点值',
        'for _ in range(len(q))': lambda S, B, r: (f'关键：进入循环时 `len(q) = {len(S.q)}`，==固定住本层节点个数==，后面入队的是下一层' if not S.vals else '本层还没数完 → 继续出队下一个；数完了就退出 for'),
        'node = q.popleft()': '本层队头出队：节点 `{node.val}`',
        'vals.append': '`{node.val}` 加入本层 → `{vals}`',
        'if node.left': lambda S, B, r: (f'`{S.node.val}` 有左儿子 `{S.node.left.val}` → 入队，留给下一层' if S.node.left else f'`{S.node.val}` 没有左儿子 → 跳过'),
        'if node.right': lambda S, B, r: (f'`{S.node.val}` 有右儿子 `{S.node.right.val}` → 入队，留给下一层' if S.node.right else f'`{S.node.val}` 没有右儿子 → 跳过'),
        'ans.append': '这一层处理完 → `vals = {vals}` 放进 `ans`（目前是自顶向下的顺序）',
        'return ans[::-1]': '题目要自底向上：把 `ans` 整体反转 → `{ret}`',
    },
    cards=dict(
        one_liner='先正常按层 BFS，最后把答案反转一下',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你二叉树根节点 `root`，返回节点值==自底向上==的层序遍历',
                 '即从叶子所在层到根所在层，逐层从左向右',
                 '示例：`[3,9,20,null,null,15,7]` → `[[15,7],[9,20],[3]]`'],
        quote='本题只需要在 102. 二叉树的层序遍历 的基础上，把答案反转即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['102 的做法：队列里每轮恰好装着一层，先数出 `len(q)` 再逐个出队',
              '出队的同时把左右儿子入队，它们就是下一层',
              '所有层收集完，`ans[::-1]` 得到自底向上的顺序'],
        summary=['时间 `O(n)`，空间 `O(n)`（满二叉树最后一层约 n/2 个节点在队列里）',
                 '易错：`range(len(q))` 只在循环开始时求值一次，所以层边界不会被新入队的节点破坏',
                 '易错：空树要先返回 `[]`，否则 `deque([None])` 会出错',
                 '方法一「两个数组」：用 `cur`/`nxt` 两个列表交替，思路相同'],
    ),
)
