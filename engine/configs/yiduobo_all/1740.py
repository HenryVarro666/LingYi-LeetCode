_SETUP = '''
def find(n, v):
    if n is None:
        return None
    if n.val == v:
        return n
    return find(n.left, v) or find(n.right, v)
'''


def find(n, v):
    if n is None:
        return None
    if n.val == v:
        return n
    return find(n.left, v) or find(n.right, v)


def _in(n, t):
    return n is not None and (n is t or _in(n.left, t) or _in(n.right, t))


def _lca(S):
    p, q = find(S['root'], S['p']), find(S['root'], S['q'])
    n = S['root']
    while True:
        for ch in (n.left, n.right):
            if ch is not None and _in(ch, p) and _in(ch, q):
                n = ch
                break
        else:
            return n


def _v(n):
    return 'None' if n is None else str(n.val)


def _I(S):
    return S['_inner']


def _found_before_right(S):
    n = _I(S)['now']
    return _in(n.left, _lca(S))


def _cap_left(S, B, r):
    n = _I(S)['now']
    return ('`res == 0`，答案还没找到' + (f'，`{n.val}` 有左儿子 → 先递归求它到目标的距离' if n.left else f'，`{n.val}` 没有左儿子 → `l_dis = None`'))


def _cap_right(S, B, r):
    n = _I(S)['now']
    if _found_before_right(S):
        return '==左子树里已经算出了答案（`res != 0`）== → 右边不用再搜，`r_dis = None`'
    return '`res == 0`，答案还没找到' + (f'，`{n.val}` 有右儿子 → 递归求距离' if n.right else f'，`{n.val}` 没有右儿子 → `r_dis = None`')


def _cap_ifl(S, B, r):
    d = _I(S)['l_dis']
    return f'左边有目标：`l_dis` 再加上这条边 → `{d}`' if d is not None else '左边没有目标，`l_dis` 保持 None'


def _cap_ifr(S, B, r):
    d = _I(S)['r_dis']
    return f'右边有目标：`r_dis` 再加上这条边 → `{d}`' if d is not None else '右边没有目标，`r_dis` 保持 None'


def _cap_branch(S, B, r):
    i = _I(S)
    l, rr = i['l_dis'], i['r_dis']
    if l or rr:
        return f'`l_dis = {l}`，`r_dis = {rr}`：至少一边有目标，需要判断 `now` 是不是 LCA'
    return f'`l_dis = {l}`，`r_dis = {rr}`：两边都没有目标，看 `now` 自己是不是目标'


CONFIG = dict(
    num=1740, title='找到二叉树中的距离', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='dfs 返回到目标的距离，LCA 处求和',
    tags=['灵神题单', '链表树与回溯'],
    setup=_SETUP,
    code='''
class Solution(object):
    def findDistance(self, root, p, q):

        if p == q:
            return 0
        
        global res
        res = 0

        def dfs(now):
            global res

            if res == 0 and now.left:
                l_dis = dfs(now.left)
            else:
                l_dis = None
            
            if res == 0 and now.right:
                r_dis = dfs(now.right)
            else:
                r_dis = None

            if l_dis is not None:
                l_dis += 1
            if r_dis is not None:
                r_dis += 1

            if l_dis or r_dis:
                if l_dis and r_dis:
                    if res == 0:
                        res = l_dis + r_dis
                    return None

                elif now.val == p or now.val == q:
                    if res == 0:
                        if l_dis:
                            res = l_dis
                        else:
                            res = r_dis
                    
                    return None
                
                else:
                    if l_dis:
                        return l_dis
                    else:
                        return r_dis
            
            elif now.val == p or now.val == q:
                return 0

            return None

        dfs(root)
        return res
''',
    call='root = Tr([3,5,1,6,2,0,8,None,None,7,4])\nSolution().findDistance(root, 6, 4)',
    expect=3,
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"`now = {_v(_I(S).get('now'))}`，`l_dis = {_I(S).get('l_dis')}`，`r_dis = {_I(S).get('r_dis')}`" if 'now' in _I(S) else '目标：p = 6，q = 4，求它们之间的边数')),
        dict(type='tree', label='二叉树（蓝 = now，粉 = 目标 6 与 4）', pointers={'now': 'blue'}, h=330,
             color=lambda S, n: 'pink' if n.val in (S.get('p'), S.get('q')) else None),
        dict(type='text', size=24, h=56, fn=lambda S: '`dfs` 返回“到目标的距离”（没有目标就返回 None）；两边都有时在这里求和'),
        dict(type='calls', h=190),
    ],
    watch=[('now', lambda S: _v(_I(S).get('now')), 'blue'), ('l_dis', lambda S: _I(S).get('l_dis'), 'yellow'), ('r_dis', lambda S: _I(S).get('r_dis'), 'yellow')],
    captions={
        'if p == q': '`p = {p}`，`q = {q}`：两个目标不同 → 继续（相同的话距离直接是 0）',
        'res = 0': '`res` 存答案，0 表示“还没找到 LCA”',
        'if res == 0 and now.left': _cap_left,
        'if res == 0 and now.right': _cap_right,
        'l_dis = dfs(now.left)': lambda S, B, r: f'左子树返回 `l_dis = {_I(S)["l_dis"]}`（到目标的距离，None 表示左边没有目标）',
        'r_dis = dfs(now.right)': lambda S, B, r: f'右子树返回 `r_dis = {_I(S)["r_dis"]}`',
        'l_dis = None': '没有左孩子（或答案已出）→ `l_dis = None`',
        'r_dis = None': '没有右孩子（或答案已出）→ `r_dis = None`',
        'if l_dis is not None': _cap_ifl,
        'if r_dis is not None': _cap_ifr,
        'l_dis += 1': '左子树里有目标：多经过 `now → 左孩子` 这条边，`l_dis` 加 1 → `{l_dis}`',
        'r_dis += 1': '右子树里有目标：多经过 `now → 右孩子` 这条边，`r_dis` 加 1 → `{r_dis}`',
        'if l_dis or r_dis': _cap_branch,
        'if l_dis and r_dis': lambda S, B, r: ('两边都有目标 → `now` 就是 ==LCA==' if _I(S)['l_dis'] and _I(S)['r_dis'] else '不是两边都有目标 → 看 `now` 自己是不是目标'),
        30: '答案还没记录过（`res == 0`）→ 可以记',
        31: lambda S, B, r: f'两边到目标的距离相加：`{_I(S)["l_dis"]} + {_I(S)["r_dis"]} = =={_I(S)["l_dis"] + _I(S)["r_dis"]}==`，这就是两点距离',
        32: 'LCA 已经处理完，返回 None，让上面的节点不再把它当目标',
        34: lambda S, B, r: ('`now` 自己是目标，另一个目标在它的一侧子树里 → `now` 就是 LCA' if _I(S)['now'].val in (S['p'], S['q']) else '`now` 不是目标 → 它只是路过，把距离往上传'),
        35: '答案还没记录过 → 可以记',
        36: lambda S, B, r: f'目标在左边：距离 = `l_dis = {_I(S)["l_dis"]}`' if _I(S)['l_dis'] else '目标在右边，距离取 `r_dis`',
        37: lambda S, B, r: f'`now` 是目标，另一个目标在左子树：距离就是 `l_dis = {_I(S)["l_dis"]}`',
        39: lambda S, B, r: f'`now` 是目标，另一个目标在右子树：距离就是 `r_dis = {_I(S)["r_dis"]}`',
        41: '这个 LCA 已处理完，返回 None',
        44: lambda S, B, r: '目标在左边 → 返回 `l_dis`' if _I(S)['l_dis'] else '目标在右边 → 返回 `r_dis`',
        49: lambda S, B, r: ('两边都没有目标，但 `now` 自己是目标 → 距离从 0 开始往上传' if _I(S)['now'].val in (S['p'], S['q']) else '两边都没有目标，`now` 也不是目标'),
        52: '这棵子树里没有目标（或答案已算出）→ 返回 None',
        50: '`now` 自己是目标，到目标的距离为 0，往上传',
        'return l_dis': '`now` 不是 LCA，把到目标的距离 `{ret}` 往上传',
        'return r_dis': '`now` 不是 LCA，把到目标的距离 `{ret}` 往上传',
        'return res': '`res = {ret}`：6 → 5 → 2 → 4，共 3 条边',
    },
    skip=['if l_dis is not None', 'if r_dis is not None'],
    cards=dict(
        one_liner='dfs 返回“到目标的距离”，两边都有目标的节点就是 LCA，距离相加',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['给二叉树 `root` 和两个节点的值 `p`、`q`',
                 '返回这两个节点之间的距离（路径上的边数）',
                 '`p` 和 `q` 可能相同，此时距离为 0',
                 '示例：树 `[3,5,1,6,2,0,8,null,null,7,4]`，`p=6, q=4` → `3`'],
        quote='在这里维护的不再是子树中目标节点的数量，而是到目标节点的距离。……某个节点的左右子树返回的到目标节点的距离都不为空，或者其中一方不为空同时当前节点是p或q之一，那么该节点就是LCA。',
        quote_src='—— yiduobo 知乎题解',
        idea=['距离 = p 到 LCA + q 到 LCA，所以仍然是找 LCA 的 dfs',
              '和 1644 不同：dfs 返回的是“到目标的距离”，往上每走一层加 1',
              '两边都返回距离 → 当前节点就是 LCA，`res = l_dis + r_dis`',
              '一边有距离且自己是目标 → 距离就是那一边的值'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '`p == q` 要单独处理，直接返回 0',
                 '返回 0 表示“自己就是目标”，所以代码里判断 `l_dis or r_dis` 用的是真假，0 被当作假',
                 '`res == 0` 表示还没算出答案，一旦算出，后面的 dfs 都被剪枝跳过',
                 '同类题：1644、1650、1676（最近公共祖先系列）'],
    ),
)
