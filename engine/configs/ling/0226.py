# ---- 标注“已翻转完”的子树：caption 回调里记录返回过的节点，tree 视图用 color 把它们涂绿
DONE = set()


def _walk_all(S):
    out, st, seen = [], [v for v in S.values() if isinstance(v, TreeNode)], set()
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        out.append(n)
        st += [n.left, n.right]
    return out


def track(fn, key=None):
    def cap(S, B, ret):
        if key and S.get(key) is not None:
            DONE.add(S[key]._uid)
        for n in _walk_all(S):
            n._d = n._uid in DONE
        return fn(S, B, ret) if callable(fn) else fn
    return cap


class Ptr(str):
    """tree 视图的指针名会直接画出来：用可调用的 str 子类做“带标签的条件指针”"""
    def __new__(cls, label, fn):
        o = str.__new__(cls, label)
        o.fn = fn
        return o

    def __call__(self, S):
        return self.fn(S)


def detached(name):
    def fn(S):
        x = S.get(name)
        if not isinstance(x, TreeNode):
            return None
        reach = {n._uid for n in _walk_all({'t': S.get('self.tree')})}
        return x if x._uid not in reach else None
    return fn


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if S.root is None:
        return '空节点：翻转后还是空 → 递归边界'
    return f'节点 `{S.root.val}` 非空 → 先把左右子树分别翻转'


def cap_l(S, B, ret):
    if S.root is None:
        return f'`{B.root.val}` 的左子树为空，递归进去直接返回 `None`'
    return f'翻转左子树：递归 `invertTree({S.root.val})`，==相信它返回翻转好的左子树=='


def cap_r(S, B, ret):
    if B.left is None and S.root is None:
        return f'`{B.root.val}` 左右都为空，右边同样直接返回 `None`'
    return f'左子树已翻转好，存在 `left = {nv(B.left)}`；再翻转右子树 `invertTree({nv(S.root)})`'


def cap_swap1(S, B, ret):
    if S.left is None and S.right is None:
        return f'`{S.root.val}` 是叶子：交换两个空儿子，等于没变'
    return (f'交换左右儿子：`root.left = right`（{nv(S.right)}）。'
            f'此刻原左子树==只靠变量 left 记着==，所以要先存下来再交换')


def cap_swap2(S, B, ret):
    if S.left is None and S.right is None:
        return f'`root.right = left`，叶子 `{S.root.val}` 完成'
    return f'`root.right = left`（{nv(S.left)}）→ 节点 `{S.root.val}` 的左右儿子==交换完成=='


CONFIG = dict(
    num=226, title='翻转二叉树', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='递归 · 先翻转子树再交换',
    code='''
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        left = self.invertTree(root.left)  # 翻转左子树
        right = self.invertTree(root.right)  # 翻转右子树
        root.left = right  # 交换左右儿子
        root.right = left
        return root
''',
    call='''s = Solution()
s.tree = Tr([4,2,7,1,3])
s.invertTree(s.tree)''',
    expect=[4, 7, 2, None, None, 3, 1],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（绿 = 这棵子树已翻转完）', pointers={'root': 'blue', Ptr('left（暂存）', detached('left')): 'green'}, h=400,
             color=lambda S, n: 'green' if getattr(n, '_d', False) else None),
        dict(type='calls', h=230),
    ],
    watch=[('root', 'root', 'blue')],
    captions={
        'if root is None': track(cap_if),
        'return None': track('返回 `None`'),
        'left = self': track(cap_l),
        'right = self': track(cap_r),
        'root.left = right': track(cap_swap1),
        'root.right = left': track(cap_swap2),
        'return root': track(lambda S, B, ret: f'以 `{S.root.val}` 为根的子树==翻转完毕==，把它返回给上一层', key='root'),
    },
    cards=dict(
        one_liner='根的左右儿子交换，左右子树内部交给递归',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
        problem=['给你二叉树的根 `root`，把它==左右镜像翻转==，返回根节点',
                 '示例：`[4,2,7,1,3,6,9]` → `[4,7,2,9,6,3,1]`',
                 '本视频用更小的 `[4,2,7,1,3]` → `[4,7,2,null,null,3,1]`'],
        quote='对于根节点，它的左右==儿子==必须交换；对于根节点的左右==子树==，也需要翻转其内部节点。这是一个和原问题相似的子问题，可以用递归解决。',
        quote_src='—— 灵茶山艾府题解「要点」',
        idea=['区分「儿子」和「子树」：交换儿子是本层的事，翻转子树交给递归',
              '写法一：先拿到翻转好的 `left`、`right`，再交换',
              '边界：空节点直接返回 `None`'],
        result='运行结束：`[4,2,7,1,3]` 翻转成 `[4,7,2,null,null,3,1]` ✓',
        summary=['时间 `O(n)`：每个节点递归一次；空间 `O(n)`：最坏退化成链',
                 '易错：交换前要==先存下两棵子树==，否则 `root.left` 被覆盖后原左子树就找不到了',
                 '灵神写法二：先交换左右儿子，再递归翻转两棵子树',
                 'Python 还可以用同时赋值一行写完，省掉 `left`/`right` 变量'],
    ),
)
