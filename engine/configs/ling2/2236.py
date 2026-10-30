TREE = [21, 9, 12, 4, 5, 2, 10, None, None, None, None, None, None, 3, 7]   # 节点值互不相同


def _pre(vals):
    """层序列表 -> 先序遍历的节点值"""
    kids = {}
    nodes = [(0, vals[0])]
    q, idx = [0], 1
    pos = {0: vals[0]}
    while q and idx < len(vals):
        p = q.pop(0)
        for side in (0, 1):
            if idx < len(vals) and vals[idx] is not None:
                kids.setdefault(p, [None, None])[side] = idx
                pos[idx] = vals[idx]
                q.append(idx)
            idx += 1
    out = []

    def go(i):
        if i is None:
            return
        out.append(pos[i])
        k = kids.get(i, [None, None])
        go(k[0])
        go(k[1])
    go(0)
    return out


PRE = _pre(TREE)
L_RET = 5


def _vals(nd):
    return set() if nd is None else {nd.val} | _vals(nd.left) | _vals(nd.right)


def _color(S, nd):
    cur = S.get('root')
    if cur is None:
        return None
    if PRE.index(nd.val) < PRE.index(cur.val):
        return 'green'
    line = S.get('_line')
    if nd.val == cur.val and line in (4, 5):
        return 'green'
    stage = getattr(cur, '_stage', 0) if line == 5 else 0
    if stage >= 1 and nd.val in _vals(cur.left):
        return 'green'
    if stage >= 2 and nd.val in _vals(cur.right):
        return 'green'
    return None


_seen = {}   # 同一个节点第几次停在这行（递归返回后 Python 会再次报告这一行）


def _leaf(S, B, r):
    if B.root.val == PRE[0]:
        _seen.clear()   # 从根重新开始（保证重复构建时计数正确）
    if B.root.left is None and B.root.right is None:
        return f'`{B.root.val}` 没有儿子 → ==叶子==，递归边界'
    return f'`{B.root.val}` 有两个儿子，不是叶子'


def _ret5(S, B, r):
    nd = B.root
    k = _seen.get(nd._uid, 0)
    _seen[nd._uid] = k + 1
    S['root']._stage = k   # 记在这一步的快照节点上，供画图时区分「刚检查 / 左子树已通过 / 整棵通过」
    if k == 0:
        if nd.val == nd.left.val + nd.right.val:
            return f'`{nd.val} == {nd.left.val} + {nd.right.val}` 成立 → `and` 继续：==先递归左儿子== `{nd.left.val}`'
        return f'`{nd.val} ≠ {nd.left.val} + {nd.right.val}` → `and` 短路，直接返回 `False`'
    if k == 1:
        return f'左子树 `{nd.left.val}` 返回 `True` → 再递归右儿子 `{nd.right.val}`'
    return f'右子树 `{nd.right.val}` 也返回 `True` → `{nd.val}` 这棵子树==全部满足==，返回 `True`'


def _text(S):
    r = S.get('root')
    if r is None:
        return ''
    if r.left is None and r.right is None:
        return f'`{r.val}` 是叶子：不用判断'
    ok = r.val == r.left.val + r.right.val
    return f"`{r.val}` 和儿子之和 `{r.left.val} + {r.right.val} = {r.left.val + r.right.val}` → {'==相等==' if ok else '不相等'}"


CONFIG = dict(
    num=2236, title='判断根结点是否等于子结点之和', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='扩展到 n 个节点：递归判断',
    tags=['List.md'],
    code='''
class Solution:
    def checkTree(self, root: Optional[TreeNode]) -> bool:
        if root.left is None and root.right is None:  # 递归边界：判断 root 是否为叶子节点
            return True
        return root.val == root.left.val + root.right.val and \\
               self.checkTree(root.left) and self.checkTree(root.right)
''',
    call=f'Solution().checkTree(Tr({TREE}))',
    expect=True,
    skip=[6],
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='tree', label='二叉树（绿 = 已检查通过）', h=420, pointers={'root': 'blue'}, color=_color),
        dict(type='calls', h=150),
    ],
    watch=[('root', 'root', 'blue')],
    captions={
        'if root.left is None and root.right is None': _leaf,
        'return True': '叶子无需判断，返回 `True`',
        'return root.val == root.left.val': _ret5,
    },
    cards=dict(
        one_liner='本题 3 个节点直接比较；n 个节点时递归：自己对、左右子树也都对',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['二叉树==恰好 3 个节点==：根、左儿子、右儿子',
                 '根的值等于两个儿子的值之和 → `true`，否则 `false`',
                 '示例：`[10,4,6]` → `true`；`[5,3,1]` → `false`',
                 '原题一行就够：`root.val == root.left.val + root.right.val`'],
        before=[dict(heading='扩展：如果有 n 个节点？', lines=[
            '每个节点有 0 或 2 个儿子（`n ≥ 3`）',
            '判断：除了叶子，是否==每个节点==的值都等于左右儿子之和',
            '本视频：9 个节点的树，每个非叶节点都满足 → `true`'])],
        quote='如果当前节点是叶子节点，直接返回 true……否则，如果当前节点的节点值不等于其儿子的节点值之和，返回 false。否则，==递归左右儿子==，如果它们都返回 true，那么当前节点返回 true',
        quote_src='—— 灵茶山艾府题解：扩展：如果有 n 个节点要怎么做？',
        idea=['递归边界：叶子 → `True`',
              '先判断自己：`root.val == 左 + 右`',
              '再用 `and` 连接左右子树的递归结果，任何一处不满足就短路返回 `False`'],
        summary=['原题只有 3 个节点：一行 `return root.val == …` 即可',
                 '扩展版时间 `O(n)`：每个节点恰好递归一次；空间 `O(n)` 递归栈',
                 '`and` 短路：自己不满足时，不会再递归儿子',
                 '练习：100. 相同的树、101. 对称二叉树、110. 平衡二叉树'],
    ),
)
