_SETUP = '''
def _link(n, par=None):
    if n is None:
        return
    n.parent = par
    _link(n.left, n)
    _link(n.right, n)


def find(n, v):
    if n is None:
        return None
    if n.val == v:
        return n
    return find(n.left, v) or find(n.right, v)
'''


def _root(S):
    n = S.get('q') or S.get('p')
    while n is not None and n.parent is not None:
        n = n.parent
    return n


def _v(n):
    return 'None' if n is None else str(n.val)


CONFIG = dict(
    num=1650, title='二叉树的最近公共祖先III', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='祖先路径 + 集合',
    tags=['灵神题单', '链表树与回溯'],
    setup=_SETUP,
    code='''
class Solution(object):
    def lowestCommonAncestor(self, p, q):

        node_set = set()
        while p:
            node_set.add(p)
            p = p.parent
        
        while q not in node_set:
            q = q.parent
        
        return q
''',
    call='root0 = Tr([3,5,1,6,2,0,8,None,None,7,4])\n_link(root0)\nSolution().lowestCommonAncestor(find(root0, 7), find(root0, 6)).val',
    expect=5,
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: (f"p 沿 parent 向上：`p = {_v(S.get('p'))}`；`q = {_v(S.get('q'))}`" if 'node_set' in S else '')),
        dict(type='tree', var=_root, label='二叉树（蓝 = p，粉 = q，绿 = 已在 node_set 中）', pointers={'p': 'blue', 'q': 'pink'}, path=False, h=330,
             color=lambda S, n: 'green' if n in S.get('node_set', ()) else None),
        dict(type='set', var=lambda S: {n.val for n in S['node_set']} if 'node_set' in S else None, label='node_set（p 的祖先路径，显示节点值）', h=130),
    ],
    watch=[('p', lambda S: _v(S.get('p')), 'blue'), ('q', lambda S: _v(S.get('q')), 'pink'), ('|node_set|', lambda S: len(S.get('node_set', ())), 'green')],
    captions={
        'node_set = set()': '准备一个集合 `node_set`，记录 p 一路向上走过的所有节点',
        'while p:': lambda S, B, r: (f'`p = {_v(S["p"])}` 不为空 → 还没越过根，继续' if S.get('p') is not None else '`p` 变成 None：已经越过根节点，p 的祖先链记录完了'),
        'node_set.add(p)': '把 `{p.val}` 记进集合，现在集合有 `{len(node_set)}` 个节点',
        'p = p.parent': lambda S, B, r: f'`p` 沿父指针上移：`{_v(B.p)}` → `{_v(S["p"])}`',
        'while q not in node_set': lambda S, B, r: (f'`q = {_v(S["q"])}` 在 p 的祖先链里吗？不在 → 继续往上' if S['q'] not in S['node_set'] else f'`q = {_v(S["q"])}` 在 p 的祖先链里 → ==这就是第一个公共祖先=='),
        'q = q.parent': lambda S, B, r: f'`q` 沿父指针上移：`{_v(B.q)}` → `{_v(S["q"])}`',
        'return q': '`q = {q.val}` 是 q 的祖先链上第一个出现在 p 的祖先链里的节点 → 最近公共祖先',
    },
    cards=dict(
        one_liner='p 沿父指针走到根记下路径，q 往上走，第一个撞上的节点就是答案',
        complexity='时间 `O(h)`，空间 `O(h)`',
        problem=['给两个节点 `p`、`q`，每个节点有 `val`、`left`、`right`、==`parent`== 指针',
                 '求它们的最近公共祖先（节点自己也算自己的祖先）',
                 '示例：树 `[3,5,1,6,2,0,8,null,null,7,4]`，`p=7, q=6` → `5`'],
        quote='从p开始不断向上迭代直到来到根节点为止，同时使用一个集合记录这个路径上的所有节点。接下来从q开始不断向上迭代，首次出现在集合中的节点即为最终答案。',
        quote_src='—— yiduobo 知乎题解',
        idea=['有了父指针，就不用从根往下搜了',
              '第一步：p 一路爬到根，把经过的节点都放进 `node_set`',
              '第二步：q 一路往上爬，第一次碰到集合里的节点就停下',
              '该节点同时在 p 和 q 的祖先链上，而且离 q 最近 → 最近公共祖先'],
        summary=['时间 `O(h)`，空间 `O(h)`（`h` 为树高）',
                 '集合里存的是节点对象，不是 `val`；`q` 自己在集合里时直接返回自己',
                 '第一个 while 条件是 `p` 不为空：根的 `parent` 是 `None`，循环到此结束',
                 '同类：链表相交（160）用双指针可以做到 `O(1)` 空间',
                 '原文开头的 `Node` 类是题目模板注释，已删去；视频里的 parent 指针由 setup 补上'],
    ),
)
