def _q(S):
    q = S.get('q')
    if q is None:
        return ''
    h = S.get('head', 0)
    items = [f"{n.val}@{p}" for n, p in q]
    return '队列 `q`（节点值@垂直位置，已出队的灰掉）：' + ' '.join(('`%s`' % s) if i >= h else s for i, s in enumerate(items))


CONFIG = dict(
    num=314, title='二叉树的垂直遍历', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='BFS · 哈希表按列收集',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def verticalOrder(self, root):

        if not root:
            return []

        res = {}
        q = [[root, 0]]
        head, tail = 0, 1
        while head < tail:
            now, p = q[head]
            if p not in res:
                res[p] = []
            res[p].append(now.val)
            head += 1

            if now.left:
                q.append([now.left, p - 1])
                tail += 1
            if now.right:
                q.append([now.right, p + 1])
                tail += 1
        
        return [x[1] for x in sorted(res.items(), key=lambda d:d[0])]
''',
    call='Solution().verticalOrder(Tr([3,9,20,4,10,15,7]))',
    expect=[[4], [9], [3, 10, 15], [20], [7]],
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前出队节点）', pointers={'now': 'blue'}, path=False, h=330,
             color=lambda S, n: 'blue' if n is S.get('now') else None),
        dict(type='text', fn=_q, size=26, h=60),
        dict(type='map', var='res', label='res（垂直位置 → 该列节点值，按 BFS 顺序）', h=170,
             fmt=lambda k, v: f'{k} → {v}'),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') else None, 'blue'), ('p', 'p', 'yellow'), 'head', 'tail'],
    max_steps=110,
    captions={
        'if not root': '`root` 非空，继续；空树才直接返回 `[]`',
        'res = {}': '`res`：垂直位置 `p` → 这一列的节点值列表',
        'q = [[root, 0]]': '队列里存 `[节点, 垂直位置]`，根的位置是 `0`',
        'head, tail = 0, 1': '`head` 是队头、`tail` 是队尾：用下标当队列，不真正弹出',
        'while head < tail': lambda S, B, r: (f'队列里还有 `{S.tail - S.head}` 个节点没处理 → 继续' if S.head < S.tail
                                              else '队列空了，整棵树都访问过 → 退出循环'),
        'now, p = q[head]': '取出队头：节点 `{now.val}`，垂直位置 `p = {p}`',
        'if p not in res': lambda S, B, r: (f'`res` 里还没有第 `{S.p}` 列 → 先建一个空列表' if S.p not in B['res']
                                            else f'第 `{S.p}` 列已经有人了，直接追加'),
        'res[p] = []': '新开第 `{p}` 列',
        'res[p].append': '节点 `{now.val}` 放进第 `{p}` 列：`res[{p}] = {res[p]}`（BFS 先上后下、先左后右，追加顺序即答案顺序）',
        'head += 1': '队头后移，`{now.val}` 出队',
        'if now.left': lambda S, B, r: (f'`{B.now.val}` 有左孩子 `{B.now.left.val}` → 它在 `p - 1 = {B.p - 1}` 列'
                                        if B.now.left else f'`{B.now.val}` 没有左孩子'),
        'q.append([now.left': '左孩子 `{now.left.val}` 入队，位置 `{p} - 1 = {p - 1}`（向左一列）',
        'if now.right': lambda S, B, r: (f'`{B.now.val}` 有右孩子 `{B.now.right.val}` → 它在 `p + 1 = {B.p + 1}` 列'
                                         if B.now.right else f'`{B.now.val}` 没有右孩子'),
        'q.append([now.right': '右孩子 `{now.right.val}` 入队，位置 `{p} + 1 = {p + 1}`（向右一列）',
        'tail += 1': '队尾后移 → `tail = {tail}`',
        'return [x[1]': lambda S, B, r: f'按 key（列号）从小到大排序，取出各列的值 → =={r}==',
    },
    cards=dict(
        one_liner='BFS 时给每个节点记列号：往左减一，往右加一',
        complexity='时间 `O(n log n)`（最后对列号排序），空间 `O(n)`',
        problem=['给你一棵二叉树，返回它==从上到下、从左到右==的垂直遍历结果',
                 '同一列（垂直位置相同）的节点放在一起；同一行同一列时按从左到右',
                 '示例：`[3,9,20,4,10,15,7]` → `[[4],[9],[3,10,15],[20],[7]]`'],
        quote='向左子树走时，将这个垂直位置减去1，反之当向右子树走时，则将这个垂直位置加上1。在bfs过程中使用哈希表将所有节点按照其对应的垂直位置收集起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['根在第 `0` 列；左孩子 `p - 1`，右孩子 `p + 1`',
              'BFS 保证先上后下、同层先左后右 → 往列表里 `append` 的顺序就是答案顺序',
              '最后哈希表按 key 排序，列号从小到大输出'],
        summary=['时间 `O(n log n)`：BFS 是 `O(n)`，排序列号最多 `n` 个',
                 '易错：必须用 BFS（层序）；DFS 会打乱同一列上下的先后顺序',
                 '`head`/`tail` 下标模拟队列，不用 `pop(0)`',
                 '原文为 Python 2 风格，本视频无需改动即可在 Python 3 运行'],
    ),
)
