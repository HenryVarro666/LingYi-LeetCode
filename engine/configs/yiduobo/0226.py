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
    if S.now is None:
        return '`now` 为空 → 原样返回（空树翻转后还是空树）'
    return f'`now = {S.now.val}` 非空 → 先递归翻转它的左子树和右子树'


def cap_l(S, B, ret):
    if S.now is None:
        return f'`{B.now.val}` 没有左子树 → `dfs(None)` 直接返回'
    return f'递归翻转左子树 `dfs({S.now.val})`，结果记为 `left_tree`'


def cap_r(S, B, ret):
    if S.now is None:
        return f'`left_tree = {nv(B.left_tree)}`；`{B.now.val}` 没有右子树 → `dfs(None)` 直接返回'
    if B.left_tree is None:
        return f'`{B.now.val}` 的左子树为空；再递归翻转右子树 `dfs({S.now.val})`'
    return f'`left_tree = {B.left_tree.val}` 已翻转好；再递归翻转右子树 `dfs({S.now.val})`'


def cap_swap1(S, B, ret):
    if S.left_tree is None and S.right_tree is None:
        return f'`{S.now.val}` 是叶子：左右都是空，互换等于没变'
    if S.left_tree is None:
        return f'左右子树互换（第 1 步）：`now.left = right_tree`（{nv(S.right_tree)}），右子树搬到左边'
    return (f'左右子树互换（第 1 步）：`now.left = right_tree`（{nv(S.right_tree)}），'
            f'原左子树还在 ==left_tree== 里')


def cap_swap2(S, B, ret):
    if S.left_tree is None and S.right_tree is None:
        return f'`now.right = left_tree`，叶子 `{S.now.val}` 完成'
    return f'互换（第 2 步）：`now.right = left_tree`（{nv(S.left_tree)}）→ ==以 {S.now.val} 为根的子树翻转完成=='


CONFIG = dict(
    num=226, title='翻转二叉树', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='递归 · 后序翻转',
    code='''
class Solution(object):
    def invertTree(self, root):
        return self.dfs(root)

    def dfs(self, now):
        if not now:
            return now

        left_tree = self.dfs(now.left)
        right_tree = self.dfs(now.right)
        now.left = right_tree
        now.right = left_tree
        return now
''',
    call='''s = Solution()
s.tree = Tr([4,2,7,None,3])
s.invertTree(s.tree)''',
    expect=[4, 7, 2, None, None, 3],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（绿 = 这棵子树已翻转完）',
             pointers={'now': 'blue', Ptr('left_tree（暂存）', detached('left_tree')): 'green'}, h=400,
             color=lambda S, n: 'green' if getattr(n, '_d', False) else None),
        dict(type='calls', h=230),
    ],
    watch=[('now', 'now', 'blue')],
    captions={
        'return self.dfs': track('`invertTree` 只是入口：把根交给 `dfs(now)`'),
        'if not now': track(cap_if),
        7: track('返回 `None`'),
        13: track(lambda S, B, ret: f'返回 `{S.now.val}`：以它为根的子树==已经翻转好==', key='now'),
        'left_tree = self': track(cap_l),
        'right_tree = self': track(cap_r),
        'now.left = right_tree': track(cap_swap1),
        'now.right = left_tree': track(cap_swap2),
    },
    cards=dict(
        one_liner='先翻转左右子树，再把两棵子树互换',
        complexity='时间 `O(n)`（每个节点只访问一次），空间 `O(h)`',
        problem=['给你二叉树的根 `root`，把它==左右镜像翻转==，返回根节点',
                 '示例：`[4,2,7,1,3,6,9]` → `[4,7,2,9,6,3,1]`',
                 '本视频用 `[4,2,7,null,3]` → `[4,7,2,null,null,3]`'],
        quote='对于树中某个节点，==先递归翻转其左子树和右子树，然后将左右子树互换==，就完成了以该节点为根的子树的翻转了。',
        quote_src='—— yiduobo 题解',
        idea=['`dfs(now)`：把以 `now` 为根的子树翻转好，并返回 `now`',
              '顺序是「左、右、再处理自己」——典型的==后序遍历==',
              '每个节点只会访问一次 → 时间 `O(n)`'],
        result='运行结束：`[4,2,7,null,3]` 翻转成 `[4,7,2,null,null,3]` ✓',
        summary=['时间 `O(n)`，空间 `O(h)`（`h` 为树高）',
                 '易错：互换前要用 `left_tree`/`right_tree` ==先存好两棵子树==',
                 'yiduobo 提到迭代也可以做（BFS/栈逐个交换），他选了递归',
                 '原文为 Python 2 风格，仅删去 docstring 和定义注释，其余照搬'],
    ),
)
