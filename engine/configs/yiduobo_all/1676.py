_SETUP = '''
def find(n, v):
    if n is None:
        return None
    if n.val == v:
        return n
    return find(n.left, v) or find(n.right, v)
'''


def _in(n, t):
    return n is not None and (n is t or _in(n.left, t) or _in(n.right, t))


def _lca(S):
    nodes = S['nodes']
    n = S['root']
    while True:
        for ch in (n.left, n.right):
            if ch is not None and all(_in(ch, t) for t in nodes):
                n = ch
                break
        else:
            return n


def _v(n):
    return 'None' if n is None else str(n.val)


def _cap_right(S, B, r):
    n = S['_inner']['now']
    if _in(n.left, _lca(S)):
        return '==答案已经在左子树里找到了== → `res` 非空，右边不用再搜'
    return '答案还没找到' + (f'，`{_v(n)}` 有右儿子 → 进入' if n.right else '，没有右儿子 → 跳过')


def _cap_hit(S, B, r):
    n = S['_inner']['now']
    if n.val in S['v_set']:
        return f'`{n.val}` 在目标集合 `v_set` 里 → 命中，`cnt` 加 1'
    return f'`{n.val}` 不在 `v_set` 里 → 不加'


def _cap_full(S, B, r):
    c, n = S['_inner']['cnt'], S['_inner']['now']
    k = len(S['v_set'])
    if c < k:
        return f'`cnt = {c}`，还差 `{k - c}` 个目标 → 这棵子树还不是答案'
    if n is _lca(S):
        return f'`cnt = {c} == len(v_set) = {k}`：目标全在这棵子树里，而且是第一次凑齐 → ==公共祖先=='
    return f'`cnt = {c}` 也凑齐了，但更深的 `{_lca(S).val}` 已经先记了答案 → 不再更新'


CONFIG = dict(
    num=1676, title='二叉树的最近公共祖先IV', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='自顶向下 dfs 计数 + 哈希集合',
    tags=['灵神题单', '链表树与回溯'],
    setup=_SETUP,
    code='''
class Solution(object):
    def lowestCommonAncestor(self, root, nodes):

        global res
        res = None

        v_set = set()
        for node in nodes:
            v_set.add(node.val)
        

        def dfs(now):
            global res

            cnt = 0
            if res is None and now.left:
                cnt += dfs(now.left)
            
            if res is None and now.right:
                cnt += dfs(now.right)
            
            if now.val in v_set:
                cnt += 1
            
            if res is None and len(v_set) == cnt:
                res = now
            
            return cnt
            

        dfs(root)
        return res
''',
    call='root0 = Tr([3,5,1,6,2,0,8,None,None,7,4])\nSolution().lowestCommonAncestor(root0, [find(root0, 7), find(root0, 4), find(root0, 6)]).val',
    expect=5,
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"当前子树根 `now = {_v(S['_inner'].get('now'))}`，命中数 `cnt = {S['_inner'].get('cnt')}`" if 'now' in S['_inner'] else '目标节点：7、4、6')),
        dict(type='tree', label='二叉树（蓝 = now，粉 = 目标节点）', pointers={'now': 'blue'}, h=330,
             color=lambda S, n: 'pink' if n.val in S.get('v_set', ()) or (S.get('v_set') is None and n in S.get('nodes', ())) else None),
        dict(type='set', var='v_set', label='v_set（目标节点的 val）', fmt=lambda x: str(x), h=100),
        dict(type='calls', h=190, hide=('nodes',)),
    ],
    watch=[('now', lambda S: _v(S['_inner'].get('now')), 'blue'), ('cnt', lambda S: S['_inner'].get('cnt'), 'yellow'), ('目标数', lambda S: len(S['v_set']) if 'v_set' in S else '', 'pink')],
    captions={
        'res = None': '`res` 存最终答案，先置空',
        'v_set = set()': '`val` 互不相同，所以可以用 `val` 的集合判断“是不是目标”',
        'v_set.add': '目标 `{node.val}` 记进 `v_set` → `{v_set}`',
        'cnt = 0': '新的一层：`cnt` 统计 `now` 这棵子树里命中的目标数，从 0 开始',
        'cnt += dfs(now.left)': lambda S, B, r: f'左子树返回命中数，`cnt = {S["_inner"]["cnt"]}`',
        'cnt += dfs(now.right)': lambda S, B, r: f'右子树返回命中数，`cnt = {S["_inner"]["cnt"]}`',
        'if res is None and now.left': lambda S, B, r: '答案还没找到' + (f'，`{_v(S["_inner"]["now"])}` 有左儿子 → 进入' if S["_inner"]["now"].left else '，没有左儿子 → 跳过'),
        'if res is None and now.right': _cap_right,
        'if now.val in v_set': _cap_hit,
        'cnt += 1': '`cnt = {cnt}`',
        'if res is None and len(v_set) == cnt': _cap_full,
        'res = now': '首次凑齐全部目标：`res = {now.val}`。孩子先于自己判断，所以它是==最深==的',
        'return cnt': '把 `cnt = {cnt}` 返回给父节点',
        'return res': '`res = {ret.val}` 就是所有目标节点的最近公共祖先',
    },
    cards=dict(
        one_liner='和 II 一样的 dfs 计数，只是把“等于 2”换成“等于目标总数”',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给二叉树 `root` 和一组节点 `nodes`（都在树中，`val` 互不相同）',
                 '求这些节点的最近公共祖先',
                 '示例：树 `[3,5,1,6,2,0,8,null,null,7,4]`，`nodes=[7,4,6]` → `5`'],
        quote='从根节点向下进行dfs，计算当前子树内命中目标节点的数目，而其中最深的且命中了所有目标节点的子树树根即为最终答案。',
        quote_src='—— yiduobo 知乎题解',
        idea=['沿用 1644：`cnt` 是子树里命中目标的个数',
              '目标变多了，先把它们的 `val` 放进集合 `v_set`，判断命中就是 `now.val in v_set`',
              '`len(v_set) == cnt` 说明全部目标都在这棵子树里',
              '孩子先递归，所以第一个凑齐的就是最深的'],
        summary=['时间 `O(n)`，空间 `O(n)`（集合 + 递归栈）',
                 '依赖 `val` 互不相同这个条件，才能用 `val` 代替节点判断',
                 '判断是 `len(v_set) == cnt`，不是写死的 2',
                 '同类题：236、1644（两个节点）、1650（有父指针）',
                 '`global res` 在嵌套函数里共享答案，`res is None` 用来剪枝'],
    ),
)
