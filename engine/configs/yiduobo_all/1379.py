CONFIG = dict(
    num=1379, title='找出克隆二叉树中的相同节点', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='只遍历克隆树 · BFS 比较值',
    tags=['二叉树', '自底向上 DFS'],
    code='''
class Solution(object):
    def getTargetCopy(self, original, cloned, target):

        if original == target:
            return cloned

        q = [cloned]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            if now.left:
                q.append(now.left)
                r += 1
                if now.left.val == target.val:
                    return q[-1]
            
            if now.right:
                q.append(now.right)
                r += 1
                if now.right.val == target.val:
                    return q[-1]
''',
    call='''s = Solution()
s.o = Tr([7,4,3,None,None,6,19])
s.c = Tr([7,4,3,None,None,6,19])
s.getTargetCopy(s.o, s.c, s.o.right.right)''',
    expect=19,
    result_fn=lambda n: n.val,
    views=[
        dict(type='tree', var='self.o', label='original（橙 = target）', pointers={'target': 'orange'}, path=False, h=230),
        dict(type='tree', var='self.c', label='cloned（蓝 = now，只在这棵树里 BFS）', pointers={'now': 'blue'}, path=False, h=250),
        dict(type='array', var='q', label='队列 q（数组 + l/r 下标）', pointers={'l': 'blue'}, cell=72, h=130),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('now', 'now.val', 'blue'), ('target', 'target.val', 'orange')],
    captions={
        'if original == target': '先看根：`original == target`？根就是 target 的话直接返回 `cloned`；这里不是，往下 BFS',
        'q = [cloned]': '只遍历克隆树：队列里先放入 `cloned`（根）',
        'l = 0': '`l` 是队头下标，不用 pop，直接移动下标',
        'r = 1': '`r` 是队尾下标（队列里已有元素个数）',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：队列里还有没处理的节点' if S.l < S.r else '队列空了'),
        'now = q[l]': '取队头 `{now.val}`，下面看它的两个孩子',
        'l += 1': '队头出队：`l` → {l}',
        'q.append(now.left)': '左孩子 `{now.left.val}` 入队',
        'q.append(now.right)': '右孩子 `{now.right.val}` 入队',
        'r += 1': '入队了一个节点：`r` → {r}',
        'now.left.val == target.val': lambda S, B, r: (f'左孩子值 `{S.now.left.val}` == `target.val` `{S.target.val}` → ==就是它=='
                                                      if S.now.left.val == S.target.val
                                                      else f'左孩子值 `{S.now.left.val}` ≠ `{S.target.val}` → 继续'),
        'now.right.val == target.val': lambda S, B, r: (f'右孩子值 `{S.now.right.val}` == `target.val` `{S.target.val}` → ==就是它=='
                                                        if S.now.right.val == S.target.val
                                                        else f'右孩子值 `{S.now.right.val}` ≠ `{S.target.val}` → 继续'),
        'return q[-1]': '`q[-1]` 刚入队的就是它 → 返回克隆树里值为 `{q[-1].val}` 的节点',
    },
    cards=dict(
        one_liner='树里值互不相同：在克隆树里 BFS，碰到值等于 target.val 的就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`（队列）',
        problem=['给原树 `original`、克隆树 `cloned` 和原树中的节点 `target`',
                 '返回 `cloned` 中与 `target` 相同的节点',
                 '本视频：`[7,4,3,null,null,6,19]`，target = 值为 `19` 的节点'],
        quote='由于树中每个节点的值都不一样，因此只要在bfs过程中遇到一个值等于target.val的节点，那么该节点就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['值唯一 → 不必管 `original`，只在 `cloned` 上按层找值',
              '用数组 `q` 当队列，`l` 队头、`r` 队尾，不弹出元素',
              '孩子入队的同时就判断：值相同立刻返回 `q[-1]`'],
        summary=['时间 `O(n)`，空间 `O(n)`；BFS 找得早，层数浅时更快',
                 '前提：节点值互不相同；有重复值就要像进阶那样两棵树同步 BFS',
                 '根要单独判断（`original == target`），因为循环只检查孩子',
                 '对比灵神：灵神两棵树同步 DFS、比较节点本身，重复值也成立'],
    ),
)
