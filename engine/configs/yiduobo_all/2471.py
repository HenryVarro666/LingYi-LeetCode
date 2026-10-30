CONFIG = dict(
    num=2471, title='逐层排序二叉树所需的最少操作数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='层序遍历 + 逐个换到目标位',
    tags=['链表树与回溯', '难度分 1635'],
    code='''
class Solution(object):
    def minimumOperations(self, root):

        res = 0
        q = [root]
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            head, tail = tail, len(q)
            v = [q[index].val for index in range(head, tail)]
            target = {}
            for index, num in enumerate(sorted(v)):
                target[num] = index

            for index in range(len(v)):
                while index != target[v[index]]:
                    target_pos = target[v[index]]
                    v[index], v[target_pos] = v[target_pos], v[index]
                    res += 1

        return res
''',
    call='''root = Tr([1,4,3,7,6,8,5])
Solution().minimumOperations(root)''',
    expect=3,
    views=[
        dict(type='tree', var='root', label='二叉树', path=False, h=220,
             color=lambda S, nd: 'yellow' if ('q' in S and 'head' in S and any(x is nd for x in S['q'][S['head']:S['tail']])) else None),
        dict(type='array', var='v', label='v：本层节点值（正在被换位）', pointers={'index': 'blue'}, h=170,
             color=lambda S, i, x: 'green' if 'target' in S and S['target'].get(x) == i else None),
        dict(type='map', var='target', label='target：值 → 排好序后应在的位置', h=130, fmt=lambda k, x: f'{k} → {x}'),
    ],
    watch=[('res', 'res', 'green'), ('head', 'head', 'cyan'), ('tail', 'tail', 'orange'), ('index', 'index', 'blue')],
    captions={
        'res = 0': '`res` 统计总交换次数；交换的是节点==值==，所以可以一层一层单独算',
        'q = [root]': '`q` 当层序遍历的队列，`[head, tail)` 是当前这一层',
        'head, tail = 0, 1': '第一层只有根：`head = 0, tail = 1`',
        'while head < tail': lambda S, B, r: (f'这一层 `[{S.head}, {S.tail})` 非空，继续处理' if S.head < S.tail else '下面没有新节点了 → 结束'),
        'for now in': '遍历当前层，把它们的孩子加到 `q` 末尾',
        'q.append(now.left)': '左儿子 `{now.left.val}` 入队（下一层）',
        'q.append(now.right)': '右儿子 `{now.right.val}` 入队（下一层）',
        'head, tail = tail': '队列里新加的就是下一层：`head = {head}, tail = {tail}`',
        'v = [q[index]': '收集这一层的节点值：`v = {v}`',
        'target = {}': '`target` 记录每个值排序后的目标位置',
        'target[num] = index': '排序后第 `{index}` 小的是 `{num}` → 它应该放在位置 `{index}`',
        'for index in range': '检查位置 `index = {index}`',
        'while index != target': lambda S, B, r: (f'位置 {S.index} 上的值 `{S.v[S.index]}` 应在 `{S.target[S.v[S.index]]}` ≠ {S.index} → 还要换' if S.index != S.target[S.v[S.index]] else f'位置 {S.index} 上的值 `{S.v[S.index]}` 已经在目标位置，看下一个'),
        'target_pos = target': '当前值要去的位置 `target_pos = {target_pos}`',
        'v[index], v[target_pos]': '把它和 `target_pos` 上的值交换：`v = {v}`',
        'res += 1': '换了一次：`res = {res}`',
        'return res': '全部层处理完，最少共 `{res}` 次交换',
    },
    cards=dict(
        one_liner='每层把值一个个换到它的目标位，换几次记几次',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['在==同一层==任意交换两个节点的值，使每层都严格递增',
                 '求最少操作次数，节点值互不相同',
                 '本视频：`[1,4,3,7,6,8,5]` → `3`'],
        quote='题目中的操作是交换节点的值而不是节点本身，这也就意味着上层节点交换值之后并不会影响下层节点的顺序，因此在这里就可以从上到下进行层序遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['层序遍历（`head/tail` 划出每一层），每层单独算',
              '本层值排序，用 `target` 记下每个值的目标位置',
              '一趟遍历：位置 `index` 上的值不在目标位，就把它换到目标位，直到当前位置正确'],
        summary=['时间 `O(n log n)`：排序；空间 `O(n)`',
                 '每次交换至少让一个值到位，所以次数就是最少的（等价于置换环 大小−1）',
                 '易错：`q[head:tail]` 遍历时 `q` 会变长，切片已取好所以安全',
                 '原文代码在 Python 3 下可直接运行，无需改动',
                 '对比灵神：灵神用置换环计数，yiduobo 直接模拟换位'],
    ),
)
