import views as V


def tree_view(**spec):
    """BFS 没有递归：画树时不传调用栈参数，避免把 root 误标成"递归路径" """
    def draw(cv, S, B, box, T):
        V.v_tree(cv, spec, {'_S': S, '_B': B, '_frames': [dict(args=[], locals=S)]}, box, 0, {})
    return dict(type='custom', draw=draw, h=spec.get('h', 380))


def _uids(S, name):
    return {n._uid for n in (S.get(name) or [])}


def _node_color(S, n):
    if n.val in (S.get('ans') or []):
        return 'orange'
    if n._uid in _uids(S, 'nxt'):
        return 'green'
    if n._uid in _uids(S, 'cur'):
        return 'blue'
    return None


def _vals(name):
    return lambda S: [n.val for n in S[name]] if S.get(name) is not None else None


def _cap_for(S, B, ret):
    a, b = S.get('node'), B.get('node')
    if a is not None and (b is None or a._uid != b._uid):
        return f'从左到右取出本层的节点 `{a.val}`'
    return '本层节点都看完了，`for` 循环结束'


def _cap_child(side, word):
    def f(S, B, ret):
        nd = B['node']
        ch = getattr(nd, side)
        if ch is not None:
            return f'`{nd.val}` 有{word}儿子 `{ch.val}` → 放进下一层 `nxt`'
        return f'`{nd.val}` 没有{word}儿子，跳过'
    return f


def _spine(root):
    out = set()
    while root is not None:
        out.add(root._uid)
        root = root.right
    return out


def _cap_append(S, B, ret):
    last = S['cur'][-1]
    s = f'`cur[-1]` ==是这一层最右边的节点==，从右边只能看到它 → `ans` 加入 `{last.val}`'
    if last._uid not in _spine(S['root']):
        s += f'（`{last.val}` 在==左子树==里，但这一层没有比它更靠右的）'
    return s


CONFIG = dict(
    num=199, title='二叉树的右视图', difficulty='Medium', category='二叉树',
    author='灵茶山艾府', technique='BFS 层序遍历，取每层最后一个',
    code='''
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        ans = []
        cur = [root]
        while cur:
            ans.append(cur[-1].val)
            nxt = []
            for node in cur:
                if node.left:  nxt.append(node.left)
                if node.right: nxt.append(node.right)
            cur = nxt
        return ans
''',
    call='Solution().rightSideView(Tr([1,2,3,None,5,None,4,6]))',
    expect=[1, 3, 4, 6],
    views=[
        dict(type='array', var=_vals('cur'), label='cur（当前层，从左到右）', cell=60,
             color=lambda S, i, v: 'orange' if i == len(S['cur']) - 1 else 'blue'),
        dict(type='array', var='ans', label='ans（右视图）', cell=60, color=lambda S, i, v: 'orange'),
        tree_view(label='二叉树（蓝 = 当前层 cur，绿 = 下一层 nxt，橙 = 右视图）', h=400,
                  pointers={'node': 'pink'}, color=_node_color),
    ],
    watch=[('node', 'node', 'pink'), ('nxt', _vals('nxt'), 'green'), ('ans', 'ans', 'orange')],
    captions={
        'if root is None': '根不为空，开始一层一层地 BFS',
        'ans = []': '`ans` 用来存每一层最右边的节点值',
        'cur = [root]': '第一层只有根：`cur = [{root.val}]`',
        'while cur:': lambda S, B, ret: (f'`cur` 里有 {len(B["cur"])} 个节点 → 处理这一层' if B['cur']
                                         else '`cur` 为空 → 所有层都处理完了'),
        'ans.append(cur[-1].val)': _cap_append,
        'nxt = []': '准备收集下一层：`nxt = []`',
        'for node in cur': _cap_for,
        'if node.left:': _cap_child('left', '左'),
        'if node.right:': _cap_child('right', '右'),
        'cur = nxt': lambda S, B, ret: (f'进入下一层：`cur = nxt`，共 {len(S["cur"])} 个节点' if S['cur']
                                         else '`nxt` 是空的：下面没有节点了'),
        'return ans': '每层最右的节点连起来就是右视图：返回 =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='一层一层地遍历，每层最后一个节点就是从右边看到的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['站在二叉树的==右侧==，从上到下返回你能看到的节点值',
                 '每一层只能看到==最右边==的那个节点（不一定是右儿子！）',
                 '示例：`root = [1,2,3,null,5,null,4,6]` → `[1,3,4,6]`'],
        quote='套用 102 题的 ==BFS 模板==，把==每一层的最后一个节点值==保存到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cur` 存当前层的节点（从左到右），`cur[-1]` 就是这一层最右边的',
              '遍历 `cur`，把左右儿子按顺序放进 `nxt`，再令 `cur = nxt` 进入下一层',
              '注意：最右边的节点可能来自==左子树==（如本例的 `6`）'],
        summary=['时间 `O(n)`：每个节点只进一次列表；空间 `O(n)`：最宽的一层约 `n/2` 个节点',
                 '易错：先放左儿子再放右儿子，`cur[-1]` 才是最右的；反过来放就取 `cur[0]`',
                 '易错：右视图≠一路向右走，左子树更深时也能被看到',
                 '方法二 DFS：先递归右子树，某个深度==首次到达==的节点就在右视图中'],
    ),
)
