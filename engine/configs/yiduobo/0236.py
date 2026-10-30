import views as V


def tree_view(**spec):
    """迭代写法没有递归路径：画树时不传调用栈参数，避免把 root/p/q 误标成"递归路径" """
    def draw(cv, S, B, box, T):
        V.v_tree(cv, spec, {'_S': S, '_B': B, '_frames': [dict(args=[], locals=S)]}, box, 0, {})
    return dict(type='custom', draw=draw, h=spec.get('h', 380))


def _v(x):
    return 'None' if x is None else str(x.val)


def _in_set(S, n):
    return n._uid in {x._uid for x in (S.get('father_set') or ())}


def _cap_child(side, word):
    def f(S, B, ret):
        nd = B['now']
        ch = getattr(nd, side)
        if ch is not None:
            return f'`{nd.val}` 有{word}儿子 `{ch.val}` → 记下它的父亲，并放进队列'
        return f'`{nd.val}` 没有{word}儿子'
    return f


def _cap_while_q(S, B, ret):
    q = B['q']
    if _in_set(B, q):
        return f'`{q.val}` ==在 father_set 里== → 它就是 p、q 的最近公共祖先'
    return f'`{q.val}` 不在 p 的祖先集合里 → 继续往上找'


CONFIG = dict(
    num=236, title='二叉树的最近公共祖先', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='BFS 记父节点 + 祖先集合',
    code='''
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        father = {root:None}
        queue = [root]
        l = 0
        r = 1
        while l < r:
            now = queue[l]
            l += 1
            if now.left:
                father[now.left] = now
                queue.append(now.left)
                r += 1
            if now.right:
                father[now.right] = now
                queue.append(now.right)
                r += 1

        father_set = set()
        while p:
            father_set.add(p)
            p = father[p]

        while q not in father_set:
            q = father[q]

        return q
''',
    call='''root = Tr([3,5,1,6,2,None,None,None,None,None,4])
p = root.left.left
q = root.left.right.right
Solution().lowestCommonAncestor(root, p, q)''',
    result_fn=lambda x: x.val,
    expect=5,
    views=[
        dict(type='array', var=lambda S: [n.val for n in S['queue']] if 'queue' in S else None,
             label='queue（BFS 队列，l 指向下一个要出队的）', cell=60, pointers={'l': 'blue'}),
        dict(type='map', var=lambda S: {k.val: (v.val if v else None) for k, v in S['father'].items()} if 'father' in S else None,
             label='father（节点 → 父节点）', h=110, fmt=lambda k, v: f'{k}→{v}'),
        dict(type='set', var=lambda S: {x.val for x in S['father_set']} if 'father_set' in S else None,
             label='father_set（p 和它的所有祖先）', h=100),
        tree_view(label='二叉树（橙 = p 的祖先集合）', h=300,
                  pointers={'now': 'blue', 'p': 'green', 'q': 'pink'}, color=lambda S, n: 'orange' if _in_set(S, n) else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('p', 'p', 'green'), ('q', 'q', 'pink')],
    captions={
        'father = {root:None}': '`father[x]` 记录 x 的父节点；根没有父亲：`father[{root.val}] = None`',
        'queue = [root]': '用数组当队列做 BFS，`l`/`r` 是队首和队尾（左闭右开）',
        'while l < r': lambda S, B, ret: (f'`l = {B["l"]} < r = {B["r"]}`：队列里还有节点' if B['l'] < B['r']
                                          else f'`l == r = {B["r"]}`：所有节点都遍历完，父节点表建好了'),
        'now = queue[l]': '取出队首 `{now.val}`',
        'if now.left': _cap_child('left', '左'),
        'father[now.left] = now': '记下 `{now.left.val}` 的父亲是 `{now.val}`：`father[{now.left.val}] = {now.val}`',
        'if now.right': _cap_child('right', '右'),
        'father[now.right] = now': '记下 `{now.right.val}` 的父亲是 `{now.val}`：`father[{now.right.val}] = {now.val}`',
        'father_set = set()': '第二步：把 ==root 到 p 路径上的所有节点== 放进集合',
        'while p:': lambda S, B, ret: (f'`p = {B["p"].val}` 不为空，继续往上' if B['p'] is not None else '`p` 走到了根的上面（None）→ 集合建好了'),
        'father_set.add(p)': '`{p.val}` 是 p 的祖先（包括 p 自己）→ 放进 `father_set`',
        'p = father[p]': lambda S, B, ret: f'沿着父指针往上：`p` → `{_v(S["p"])}`',
        'while q not in father_set': _cap_while_q,
        'q = father[q]': '`q` 往上走一步 → `{q.val}`',
        'return q': '从 q 往上第一个落在集合里的节点就是 LCA：返回 =={ret.val}==',
    },
    skip=['l += 1', 'r += 1', 'queue.append', 'l = 0', 'r = 1'],
    max_steps=60,
    cards=dict(
        one_liner='先记下每个节点的父亲，再把 p 的祖先放进集合，q 往上找第一个在集合里的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定二叉树和其中两个节点 `p`、`q`，找它们的==最近公共祖先==（LCA）',
                 'LCA：是 p、q 的祖先且深度尽量大；==一个节点也可以是它自己的祖先==',
                 '示例：`root = [3,5,1,6,2,null,null,null,null,null,4]`',
                 '`p = 6`，`q = 4` → 最近公共祖先是 `5`'],
        quote='我们将==root到p路径上的所有节点存到set中==，然后反过来==从q到root逐个节点遍历==，若当前节点出现在set中，那么就是p和q的最近公共祖先了。',
        quote_src='—— yiduobo 知乎题解',
        idea=['BFS 一遍，用 `father` 记录每个节点的父节点，这样就能从任何节点==往上走==',
              '从 p 一路往上走到根，路上的节点（p 的所有祖先）放进 `father_set`',
              '从 q 往上走，==第一个出现在集合里==的节点就是最近公共祖先'],
        summary=['时间 `O(n)`，空间 `O(n)`（`father` 字典 + 队列 + 集合）',
                 '易错：`father_set` 要包含 p 自己，因为 p 可能就是 q 的祖先',
                 '对比灵神的递归写法：不用理解「候选项」，但要多存一张父节点表',
                 '原文为 Python 2 风格（类型说明写在文档字符串里），已删去文档字符串，代码未改'],
    ),
)
