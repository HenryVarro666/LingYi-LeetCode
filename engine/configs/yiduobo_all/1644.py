_SETUP = '''
def find(n, v):
    if n is None:
        return None
    if n.val == v:
        return n
    return find(n.left, v) or find(n.right, v)
'''


def _lca(S):
    p, q = S['p'], S['q']

    def has(n, t):
        return n is not None and (n is t or has(n.left, t) or has(n.right, t))
    n = S['root']
    while True:
        if has(n.left, p) and has(n.left, q):
            n = n.left
        elif has(n.right, p) and has(n.right, q):
            n = n.right
        else:
            return n


def _in(n, t):
    return n is not None and (n is t or _in(n.left, t) or _in(n.right, t))


def _cap_right(S, B, r):
    n = S['_inner']['now']
    if _in(n.left, _lca(S)):
        return '==答案已经在左子树里找到了== → `res` 非空，右边不用再搜'
    return '答案还没找到' + (f'，`{_v(n)}` 有右儿子 → 进入' if n.right else '，没有右儿子 → 跳过')


def _v(n):
    return 'None' if n is None else str(n.val)


CONFIG = dict(
    num=1644, title='二叉树的最近公共祖先II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='自顶向下 dfs 计数',
    tags=['灵神题单', '链表树与回溯'],
    setup=_SETUP,
    code='''
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):

        global res
        res = None

        def dfs(now):
            global res

            cnt = 0

            if res is None and now.left:
                cnt += dfs(now.left)
            
            if res is None and now.right:
                cnt += dfs(now.right)
            
            if now == p or now == q:
                cnt += 1
            
            if res is None and cnt == 2:
                res = now

            return cnt

        dfs(root)
        return res
''',
    call='root0 = Tr([3,5,1,6,2,0,8,None,None,7,4])\nSolution().lowestCommonAncestor(root0, find(root0, 7), find(root0, 4)).val',
    expect=2,
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"当前子树根 `now = {_v(S['_inner'].get('now'))}`，命中数 `cnt = {S['_inner'].get('cnt')}`" if 'now' in S['_inner'] else '目标：p = 7，q = 4（保证都存在）')),
        dict(type='tree', label='二叉树（蓝 = now，目标 7、4）', pointers={'now': 'blue', 'p': 'pink', 'q': 'pink'}, h=360,
             color=lambda S, n: 'pink' if n is S.get('p') or n is S.get('q') else None),
        dict(type='text', size=24, h=56, fn=lambda S: '`res` 是全局变量，一旦被赋值，后面的 dfs 都会被剪枝跳过'),
        dict(type='calls', h=200),
    ],
    watch=[('now', lambda S: _v(S['_inner'].get('now')), 'blue'), ('cnt', lambda S: S['_inner'].get('cnt'), 'yellow')],
    captions={
        'res = None': '`res` 存最终答案，先置空；==第一次出现 cnt == 2 就是最深的公共祖先==',
        'cnt = 0': '新的一层：`cnt` 统计 `now` 这棵子树里命中 p 或 q 的个数，从 0 开始',
        'cnt += dfs(now.left)': lambda S, B, r: f'左子树返回命中数 `{S["_inner"]["cnt"]}`，累加到 `cnt`',
        'cnt += dfs(now.right)': lambda S, B, r: f'右子树返回命中数，`cnt` = `{S["_inner"]["cnt"]}`',
        'if res is None and now.left': lambda S, B, r: '答案还没找到' + (f'，`{_v(S["_inner"]["now"])}` 有左儿子 → 进入' if S["_inner"]["now"].left else '，没有左儿子 → 跳过'),
        'if res is None and now.right': _cap_right,
        'if now == p or now == q': lambda S, B, r: f'`{_v(S["_inner"]["now"])}` 自己是目标吗？' + ('是 → `cnt` 再加 1' if S["_inner"]["now"] is S.get('p') or S["_inner"]["now"] is S.get('q') else '不是'),
        'cnt += 1': '`now` 自己就是 p 或 q：`cnt = {cnt}`',
        'if res is None and cnt == 2': lambda S, B, r: (f'`cnt = 2`：p、q 都在这棵子树里，但更深的 `{_lca(S).val}` 已经抢先记了答案 → 这里不再更新' if S['_inner']['cnt'] == 2 and S['_inner']['now'] is not _lca(S) else f'`cnt = 2`：这棵子树里 ==p、q 都有了== → 公共祖先') if S['_inner']['cnt'] == 2 else f'`cnt = {S["_inner"]["cnt"]}` 不到 2 → 还不是公共祖先',
        'res = now': '首次凑齐 2 个目标：`res = {now.val}`，dfs 是先处理孩子再判断，所以这就是==最深==的公共祖先',
        'return cnt': '把 `cnt = {cnt}` 返回给父节点，让它知道这棵子树里命中了几个',
        'return res': '`res = {ret.val}` 就是最近公共祖先',
    },
    cards=dict(
        one_liner='自顶向下 dfs，数子树里命中几个目标，首次凑齐 2 个就是答案',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给二叉树 `root` 和两个节点 `p`、`q`，求它们的最近公共祖先',
                 '与 236 不同：==p、q 不一定都在树中==，不在就返回 `null`',
                 '节点只有左右孩子指针，没有父指针',
                 '示例：树 `[3,5,1,6,2,0,8,null,null,7,4]`，`p=7, q=4` → `2`'],
        quote='若最终的cnt等于2，且当前还没有找到答案，那么答案就是当前节点now。',
        quote_src='—— yiduobo 知乎题解',
        idea=['没有父指针，只能从 root 往下 dfs',
              '`cnt` = 当前子树里命中 p、q 的个数：左 + 右 + 自己',
              '后序：先递归孩子，孩子里先凑齐就先赋值，所以 `res` 是最深的那个',
              '`res` 一旦非空，后面的 dfs 全部跳过'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '`cnt == 2` 才记答案，所以 p、q 有一个不在树里时返回 `None`（这正是 II 与 236 的区别）',
                 '`global res` 用来在嵌套函数间共享答案，`res is None` 是提前剪枝的开关',
                 '同类题：1650（有父指针）、1676（多个目标）、1740（求距离）'],
    ),
)
