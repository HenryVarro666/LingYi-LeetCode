def _tcolor(S, node):
    q, l, r = S.get('q'), S.get('l'), S.get('r')
    if q is None or l is None:
        return None
    layer = [x.val for x in q[l:r]]
    if node.val in layer:
        return 'orange'
    if node.val in (S.get('used') or ()):
        return 'green'
    return None


def _fa(S):
    fa = S.get('fa')
    if fa is None:
        return None
    return {k: (v.val if v is not None else None) for k, v in fa.items()}


def _v(x):
    return 'None' if x is None else x.val


def _cap_fa(S, B, r):
    f = S.fa[S.now.val]
    if f is None:
        return f'`{S.now.val}` 是根，没有父节点'
    if f.val in B.used:
        return f'父节点 `{f.val}` 已经访问过 → 跳过'
    return f'==往上走==：父节点 `{f.val}` 没访问过 → 入队'


def _cap_child(side, word):
    def f(S, B, r):
        ch = getattr(S.now, side)
        if ch is None:
            return f'`{S.now.val}` 没有{word}孩子'
        if ch.val in B.used:
            return f'{word}孩子 `{ch.val}` 已经访问过 → 跳过'
        return f'{word}孩子 `{ch.val}` 没访问过 → 入队'
    return f


CONFIG = dict(
    num=863, title='二叉树中所有距离为K的结点', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS 记父节点 + BFS',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def distanceK(self, root, target, K):

        fa = {root.val:None}
        self.dfs(root, fa)
        q = [target]
        l = 0
        r = 1
        used = set([target.val])
        
        dis = 0
        while l < r:
            if dis == K:
                return [x.val for x in q[l:r]]
            dis += 1
            for now in q[l:r]:
                if fa[now.val] is not None and fa[now.val].val not in used:
                    q.append(fa[now.val])
                    used.add(fa[now.val].val)
                if now.left is not None and now.left.val not in used:
                    q.append(now.left)
                    used.add(now.left.val)
                if now.right is not None and now.right.val not in used:
                    q.append(now.right)
                    used.add(now.right.val)

            l, r = r, len(q)
            
        
        return []

    def dfs(self, now, fa):
        if now.left:
            fa[now.left.val] = now
            self.dfs(now.left, fa)
        if now.right:
            fa[now.right.val] = now
            self.dfs(now.right, fa)
''',
    call='root = Tr([3,5,1,6,2,None,8,None,None,7,4])\nSolution().distanceK(root, root.left, 2)',
    expect=[1, 7, 4],
    skip=['if now.left:', 'if now.right:', 'l = 0', 'r = 1', 'q.append(', 'self.dfs(now.left', 'self.dfs(now.right'],
    views=[
        dict(type='tree', var='root', label='树（粉 = target，蓝 = now；橙 = 当前这一层，绿 = 已访问）',
             pointers={'target': 'pink', 'now': 'blue'}, color=_tcolor, path=False, h=370),
        dict(type='map', var=_fa, label='fa：子节点值 → 父节点值', h=120),
        dict(type='array', var=lambda S: [x.val for x in S['q']] if 'q' in S else None,
             label='q（暗 = 之前的层，[l, r) = 当前这一层）', cell=80, h=180,
             pointers={'l': 'blue', 'r': 'pink'}, dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('dis', 'dis', 'green'), ('K', 'K', 'yellow'), ('now', lambda S: _v(S.get('now')), 'blue'),
           ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'fa = {root.val:None}': '`fa` 记录每个节点的父节点，根 `{root.val}` 没有父节点',
        'self.dfs(root, fa)': '先 DFS 一遍整棵树，把父节点都记下来',
        'fa[now.left.val] = now': '`{now.left.val}` 的父节点是 `{now.val}`',
        'fa[now.right.val] = now': '`{now.right.val}` 的父节点是 `{now.val}`',
        'q = [target]': '父节点记好了 → 从 `target = {target.val}` 开始 BFS，==把树当成无向图==',
        'used = set([target.val])': '`used` 防止走回头路（例如从父节点再走回孩子）',
        'dis = 0': '`dis` = 当前这一层到 target 的距离',
        'while l < r': lambda S, B, r: (f'这一层 `q[{S.l}:{S.r}]` 不空' if S.l < S.r else '队列空了，距离 K 处没有节点'),
        'if dis == K': lambda S, B, r: (f'`dis = {S.dis} == K` → ==这一层就是答案==' if S.dis == S.K
                                        else f'`dis = {S.dis} < K = {S.K}`，继续往外扩一层'),
        'return [x.val': '距离为 `{K}` 的节点：`{ret}`',
        'dis += 1': '扩展出的下一层距离为 `{dis}`',
        'for now in q[l:r]': lambda S, B, r: (f'这一层处理完了' if 'now' in B and B.now.val == S.now.val
                                             else f'取出 `{S.now.val}`：看它的==父节点==和左右孩子'),
        'if fa[now.val] is not None': _cap_fa,
        'if now.left is not None': _cap_child('left', '左'),
        'if now.right is not None': _cap_child('right', '右'),
        'used.add(fa[now.val].val)': '`{fa[now.val].val}` 进入下一层，`used` 记下它',
        'used.add(now.left.val)': '`{now.left.val}` 进入下一层，`used` 记下它',
        'used.add(now.right.val)': '`{now.right.val}` 进入下一层，`used` 记下它',
        'l, r = r, len(q)': '这一层结束：`l, r = {l}, {r}`',
    },
    cards=dict(
        one_liner='先记下每个节点的父节点，再从 target 往三个方向 BFS K 层',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给二叉树根 `root`、树中节点 `target` 和整数 `K`（节点值互不相同）',
                 '返回所有与 `target` 距离为 `K` 的节点值，顺序任意',
                 '本视频：`[3,5,1,6,2,null,8,null,null,7,4]`，`target = 5`，`K = 2` → `[1,7,4]`'],
        quote='首先从root开始，对整棵树进行一趟dfs，记录下每个节点的父节点是什么。接下来从target开始进行bfs，每次扩展的节点除了孩子节点之外，==还需要额外考察当前节点的父亲节点==。',
        quote_src='—— yiduobo 题解原文',
        idea=['二叉树只能往下走；记下父节点后，每个节点就有==父、左、右==三个邻居',
              '从 target 做 BFS，`used` 防止走回头路',
              '第 K 轮扩展到的那一层就是答案'],
        summary=['时间、空间 `O(n)`：DFS 一遍 + BFS 一遍',
                 '`fa` 和 `used` 用节点值作键，依赖==节点值互不相同==',
                 '易错：不记 `used` 的话，从父节点会走回 target，距离算错',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
