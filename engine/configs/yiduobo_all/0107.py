def _lv(S):
    return f"层号 `level = {S['_inner'].get('level')}`" if 'level' in S['_inner'] else ''


CONFIG = dict(
    num=107, title='二叉树的层序遍历 II', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='DFS 带层号 · 最后 reverse',
    tags=[],
    code='''
class Solution(object):
    def levelOrderBottom(self, root):

        res = []

        self.dfs(root, 1, res)
        res.reverse()
        return res

    def dfs(self, now, level, res):
        if now is None:
            return 

        if level > len(res):
            res.append([])
        res[level - 1].append(now.val)
        if now.left:
            self.dfs(now.left, level + 1, res)
        if now.right:
            self.dfs(now.right, level + 1, res)
''',
    call='Solution().levelOrderBottom(Tr([3,9,20,None,None,15,7]))',
    expect=[[15, 7], [9, 20], [3]],
    views=[
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=290),
        dict(type='text', fn=lambda S: f"`res = {S['res']}`" if 'res' in S['_inner'] else '', size=26, h=56),
        dict(type='calls', h=200, hide=('res',)),
    ],
    watch=[('now', lambda S: S['_inner']['now'].val if S['_inner'].get('now') else None, 'blue'),
           ('level', lambda S: S['_inner'].get('level'), 'yellow')],
    captions={
        'res = []': '`res[i]` 存第 `i+1` 层的节点值',
        'self.dfs(root, 1, res)': '从根出发 DFS，根在第 `1` 层，边走边把值放进对应层',
        'if now is None': lambda S, B, r: '空节点 → 直接返回' if S.now is None else f'`{S.now.val}` 非空 → 处理它',
        'if level > len(res)': lambda S, B, r: (f'`level = {S.level}` > `len(res) = {len(S.res)}`：==第一次到达这一层== → 先新开一个空列表'
                                              if S.level > len(S.res) else f'`level = {S.level}` ≤ `len(res) = {len(S.res)}`：这一层已经有列表了'),
        'res.append([])': '新开第 `{level}` 层的列表 → `res = {res}`',
        'res[level - 1].append': '`{now.val}` 放进第 `{level}` 层 → `res = {res}`',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左儿子 → 层号 +1 递归' if S.now.left else f'`{S.now.val}` 没有左儿子'),
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右儿子 → 层号 +1 递归' if S.now.right else f'`{S.now.val}` 没有右儿子'),
        'self.dfs(now.left': lambda S, B, r: f'进入左儿子，层号 `{S.level}`',
        'self.dfs(now.right': lambda S, B, r: f'进入右儿子，层号 `{S.level}`',
        'res.reverse()': 'DFS 先左后右，每层内部已是从左到右；整体 ==reverse== 得到自底向上 → `{res}`',
        'return res': '返回 `{ret}`',
    },
    skip=['return \n'],
    cards=dict(
        one_liner='用 DFS 带着层号走，按层号分桶，最后整体 reverse',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你二叉树根节点 `root`，返回节点值==自底向上==的层序遍历',
                 '示例：`[3,9,20,null,null,15,7]` → `[[15,7],[9,20],[3]]`'],
        quote='与102题一样，这里求出层次遍历之后将结果reverse即可。当然在过程中使用栈来做也行。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文没有用队列，而是 ==先序 DFS + 层号==：`level > len(res)` 说明第一次到这层，新开一个列表',
              '先左后右访问，所以同一层的值天然是从左到右',
              '102 的答案算出来后 `res.reverse()`，就是 107'],
        summary=['时间 `O(n)`，空间 `O(n)`（递归栈最坏 `O(n)`）',
                 '易错：层号从 1 开始，所以下标是 `level - 1`',
                 '易错：`level > len(res)` 才新开列表，用 `==` 在先序里同样成立',
                 '对比灵神：灵神用 BFS 队列逐层处理；这里用 DFS 按层号分桶，结果一样'],
    ),
)
