CONFIG = dict(
    num='LCP 44', title='开幕式焰火', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS 遍历 + 哈希表',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def numColor(self, root):

        color_set = set()
        q = [root]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            color_set.add(now.val)
            head += 1
            if now.left:
                q.append(now.left)
                tail += 1
            if now.right:
                q.append(now.right)
                tail += 1
        
        return len(color_set)
''',
    call='''s = Solution()
s.tree = Tr([1,3,2,1,None,2])
s.numColor(s.tree)''',
    expect=3,
    views=[
        dict(type='tree', var='self.tree', label='焰火二叉树（蓝 = now，绿 = 已出队处理）', pointers={'now': 'blue'}, path=False, h=240,
             color=lambda S, n: 'green' if 'q' in S and any(x._uid == n._uid for x in S['q'][:S['head']]) else None),
        dict(type='array', var=lambda S: [x.val for x in S['q']] if 'q' in S else [], label='队列 q（head = 队头，tail = 队尾后一位）',
             pointers={'head': 'blue', 'tail': 'pink'}, cell=70, h=130),
        dict(type='set', var='color_set', label='color_set', fmt=lambda x: str(x), h=100),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('now', lambda S: S['now'].val if S.get('now') is not None else None, 'yellow'), ('颜色数', lambda S: len(S['color_set']) if 'color_set' in S else 0, 'green')],
    captions={
        'color_set = set()': '`color_set`：哈希表，记录出现过的颜色',
        'q = [root]': '队列里先放进根节点；用 `head`、`tail` 当队头队尾',
        'head, tail = 0, 1': '`head = 0`，`tail = 1`：队列里有 `tail - head` 个待处理节点',
        'while head < tail': lambda S, B, r: (f'`head = {S.head} < tail = {S.tail}`：队列里还有节点 → 继续' if S.head < S.tail else f'`head = {S.head} == tail = {S.tail}`：队列空了，整棵树遍历完'),
        'now = q[head]': '取队头节点 `now = {now.val}`',
        'color_set.add': lambda S, B, r: (f'颜色 `{S.now.val}` 已经在表里，不变' if S.now.val in B.color_set else f'颜色 `{S.now.val}` 第一次出现 → 记入 `color_set` = `{sorted(S.color_set)}`'),
        'head += 1': '`now` 处理完，队头后移：`head` → {head}',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 入队' if S.now.left else f'`{S.now.val}` 没有左孩子'),
        'q.append(now.left)': '左孩子 `{now.left.val}` 入队',
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 入队' if S.now.right else f'`{S.now.val}` 没有右孩子'),
        'q.append(now.right)': '右孩子 `{now.right.val}` 入队',
        'tail += 1': '队尾后移：`tail` → {tail}',
        'return len': '哈希表长度即答案：`{len(color_set)}`',
    },
    cards=dict(
        one_liner='BFS 走遍整棵树，哈希表的长度就是颜色种数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树的每个节点值代表一种颜色',
                 '计算整棵树一共有多少种不同的颜色',
                 '本视频：`root = [1,3,2,1,null,2]` → `3`'],
        quote='直接bfs遍历整棵树，使用哈希表记录树中的所有节点值。遍历完成后，哈希表的长度即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['用列表 `q` 加上 `head`、`tail` 两个下标，手写队列',
              '每取出一个节点：值记进 `color_set`，非空孩子入队',
              '队列空了就遍历完，答案 `len(color_set)`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`q` 只增不删，用 `head` 移动代替出队，省去 `pop(0)` 的 `O(n)` 开销',
                 '对比灵神：灵神递归 DFS，yiduobo 用 BFS；结果一样，只是遍历顺序不同',
                 '入队前判断 `if now.left`，所以队列里不会有空节点'],
    ),
)
