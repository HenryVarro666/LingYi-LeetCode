CONFIG = dict(
    num=2583, title='二叉树中的第 K 大层和', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='BFS 求层和 · 排序取第 k 大',
    tags=['灵神题单', '链表树与回溯', '难度分 1374'],
    code='''
class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        a = []
        q = [root]
        while q:
            s = 0
            tmp = q
            q = []
            for node in tmp:
                s += node.val
                if node.left:  q.append(node.left)
                if node.right: q.append(node.right)
            a.append(s)
        if k > len(a):
            return -1
        a.sort()
        return a[-k]
''',
    call='Solution().kthLargestLevelSum(Tr([5,8,9,2,1,3,7,4,6]), 2)',
    expect=13,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 node）', pointers={'node': 'blue'}, path=False, h=290),
        dict(type='array', var=lambda S: [n.val for n in S['tmp']] if S.get('tmp') else [], label='tmp（当前层）', cell=60, h=100),
        dict(type='array', var=lambda S: [n.val for n in S['q']], label='q（下一层）', cell=60, h=100),
        dict(type='array', var='a', label='a（每层的层和）', cell=72, h=110),
    ],
    watch=[('node', lambda S: S['node'].val if S.get('node') else None, 'blue'), ('s', 's', 'yellow'), ('k', 'k')],
    captions={
        'a = []': '`a` 用来保存每一层的节点值之和',
        'q = [root]': '`q` 先放根节点：它就是第一层',
        'while q': lambda S, B, r: (f'`q` 里有 `{len(S.q)}` 个节点（一整层）→ 处理这一层' if S.q else '`q` 空了 → 所有层都处理完，`a` 里是每层的层和'),
        's = 0': '新的一层，层和 `s` 从 0 开始累加',
        'tmp = q': '`tmp` 拿走当前层，下面用 `tmp` 遍历',
        'q = []': '`q` 清空，专门收集==下一层==的节点（双数组 BFS）',
        'for node in tmp': '取出当前层的节点 `{node.val}`',
        's += node.val': '`s = {B.s} + {node.val} = {s}`：把它加进层和',
        'if node.left': lambda S, B, r: (f'`{S.node.val}` 有左儿子 `{S.node.left.val}` → 放入 `q`，留给下一层' if S.node.left else f'`{S.node.val}` 没有左儿子 → 跳过'),
        'if node.right': lambda S, B, r: (f'`{S.node.val}` 有右儿子 `{S.node.right.val}` → 放入 `q`，留给下一层' if S.node.right else f'`{S.node.val}` 没有右儿子 → 跳过'),
        'a.append(s)': '这一层累加完 → 层和 `{s}` 记入 `a = {a}`',
        'if k > len(a)': lambda S, B, r: (f'`k = {S.k}` 大于层数 `{len(S.a)}` → 不够 k 层，返回 -1' if S.k > len(S.a) else f'层数 `{len(S.a)}` ≥ `k = {S.k}` → 一定存在第 k 大，不用返回 -1'),
        'a.sort()': '升序排序：`a = {a}`，第 k 大就是倒数第 k 个',
        'return a[-k]': '`a[-{k}] = {ret}` 就是第 {k} 大的层和',
    },
    skip=['return -1'],
    cards=dict(
        one_liner='BFS 逐层求和，把层和排序，倒数第 k 个就是答案',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给你二叉树 `root` 和正整数 `k`，层和是同一层节点值之和',
                 '返回第 `k` 大的层和（可重复），少于 `k` 层返回 `-1`',
                 '示例：`[5,8,9,2,1,3,7,4,6]`，`k = 2` → 层和 5、17、13、10 → `13`'],
        quote='首先，利用 BFS，可以得到二叉树每一层的节点值之和，本文用双数组实现。BFS 的同时，把每一层的节点值之和保存到一个列表 a 中，把 a 排序后就可以得到第 k 大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['双数组 BFS：`tmp` 是当前层，`q` 收集下一层',
              '遍历 `tmp` 时累加 `s`，每层结束把 `s` 放进 `a`',
              '最后判断层数够不够，够就排序取 `a[-k]`'],
        summary=['时间 `O(n log n)`（排序）；改用快速选择可到 `O(n)`；空间 `O(n)`',
                 '易错：层数不足 `k` 时要返回 `-1`，要在取 `a[-k]` 之前判断',
                 '易错：层和可能很大，但 Python 不会溢出；其他语言要用 64 位整数',
                 '对比：另一种常见写法是用大小为 k 的小顶堆，空间只需 `O(k)`（层数的另外一份）'],
    ),
)
