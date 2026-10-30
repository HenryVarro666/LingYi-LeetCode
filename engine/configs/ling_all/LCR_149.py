def _done(S, n):
    ans, vals = S.get('ans'), S.get('vals')
    if ans is not None and n.val in ans + (vals or []):
        return 'green'
    return None


def _txt(S):
    q = S.get('q')
    if q is None:
        return '一层一层地处理：每轮先数清队列里有几个节点，就是这一层'
    return f'队列里 `{len(q)}` 个节点 = 当前这一层；已收集的答案 `{S.get("ans", [])}`'


CONFIG = dict(
    num='LCR 149', title='彩灯装饰记录 I', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='BFS · 一个队列，按层遍历',
    tags=[],
    code='''
class Solution:
    def decorateRecord(self, root: TreeNode) -> List[int]:
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
            ans.extend(vals)
        return ans
''',
    call='''s = Solution()
s.tree = Tr([8,17,21,18,None,None,6])
s.decorateRecord(s.tree)''',
    expect=[8, 17, 21, 18, 6],
    skip=['for _ in range(len(q))'],
    views=[
        dict(type='tree', label='二叉树（绿 = 已取出）', pointers={'node': 'blue'}, h=340, path=False, color=_done),
        dict(type='queue', var='q', label='队列 q（左 = 队头）', fmt=lambda x: str(x.val), h=115),
        dict(type='array', var='vals', label='vals（本层）', h=135, cell=64),
        dict(type='array', var='ans', label='ans', h=135, cell=64),
    ],
    watch=[('node', lambda S: S.get('node').val if S.get('node') else None, 'blue')],
    captions={
        'if root is None': lambda S, B, ret: '空树没有彩灯，直接返回 `[]`' if S.root is None else '`root` 不为空，开始按层遍历',
        'ans = []': '`ans` 存最终的答案（所有层摊平）',
        'q = deque([root])': '队列先放入根节点 `{root.val}`：第 0 层',
        'while q': lambda S, B, ret: (f'队列非空 → 开始处理新的一层' if S.q else '队列空了，所有层都处理完'),
        'vals = []': '`vals` 收集这一层：此时队列里正好是==这一层的全部节点==，共 `{len(q)}` 个',
        'node = q.popleft()': '队头出队：节点 `{node.val}`',
        'vals.append(node.val)': '把 `{node.val}` 记入本层 `vals` → `{vals}`',
        'if node.left': lambda S, B, ret: (f'左儿子 `{S.node.left.val}` 存在 → ==入队==，留给下一层' if S.node.left else f'`{S.node.val}` 没有左儿子，不入队'),
        'if node.right': lambda S, B, ret: (f'右儿子 `{S.node.right.val}` 存在 → ==入队==，留给下一层' if S.node.right else f'`{S.node.val}` 没有右儿子，不入队'),
        'ans.extend(vals)': '这一层处理完（循环次数是==进入时的队列长度==，新入队的不算）：`ans` += `{vals}` → `{ans}`',
        'return ans': '按层、从左到右，返回 `{ans}`',
    },
    cards=dict(
        one_liner='每轮循环只处理「进来时队列里有的那些」，恰好就是一层',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['按从==左到右==、==一层一层==的顺序返回二叉树各节点的值',
                 '示例：`root = [8,17,21,18,null,null,6]`',
                 '输出：`[8,17,21,18,6]`'],
        quote='满二叉树（每一层都填满）最后一层有大约 n/2 个节点，因此队列中最多有 O(n) 个元素，所以空间复杂度是 O(n) 的。',
        quote_src='—— 灵茶山艾府题解复杂度分析（方法二）',
        idea=['用 `deque` 当队列：先进先出，上一层的节点排在下一层前面',
              '每轮先固定 `len(q)`，就是==当前层的节点数==；循环里新入队的是下一层',
              '出队一个，就把它的左、右儿子依次入队，保证从左到右'],
        summary=['时间 `O(n)`：每个节点入队、出队各一次；空间 `O(n)`：满二叉树最后一层约 `n/2` 个',
                 '易错：`range(len(q))` 只在循环开始时求值一次，所以层与层不会混',
                 '方法一「两个数组」：`cur` 存本层、`nxt` 存下一层，每层结束 `cur = nxt`',
                 '本题只要平铺的列表，所以用 `ans.extend(vals)`；分层结果则 `ans.append(vals)`'],
    ),
)
