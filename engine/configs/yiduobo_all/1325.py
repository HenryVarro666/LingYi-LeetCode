def nv(x):
    return '空' if x is None else str(x.val)


def cap_l(S, B, ret):
    n = S.now
    if n.left is None:
        return f'节点 `{n.val}` 没有左孩子 → 不用递归'
    return f'节点 `{n.val}` 有左孩子 `{n.left.val}` → 先递归处理它；返回 `True` 说明它被删了，就断开这条边'


def cap_r(S, B, ret):
    n = S.now
    if n.right is None:
        return f'节点 `{n.val}` 没有右孩子 → 不用递归'
    return f'节点 `{n.val}` 有右孩子 `{n.right.val}` → 先递归处理它；返回 `True` 就断开这条边'


def cap_ret(S, B, ret):
    n = S.now
    if ret:
        return f'节点 `{n.val}`：左右都空、值 `{n.val}` == target `{S.target}` → 它成了该删的叶子，返回 `True` 让父节点断开'
    if n.left is not None or n.right is not None:
        return f'节点 `{n.val}` 还有孩子，不是叶子 → 返回 `False`，保留'
    return f'节点 `{n.val}` 是叶子，但值 `{n.val}` ≠ target `{S.target}` → 返回 `False`，保留'


CONFIG = dict(
    num=1325, title='删除给定值的叶子节点', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='假根节点 + 后序 DFS（返回是否删除）',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def removeLeafNodes(self, root, target):

        p_root = TreeNode(0)
        p_root.left = root
        self.dfs(p_root, target)
    
        return p_root.left

    def dfs(self, now, target):
        if now.left is not None and self.dfs(now.left, target):
            now.left = None

        if now.right is not None and self.dfs(now.right, target):
            now.right = None

        return now.left is None and now.right is None and now.val == target
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,2,None,2,4])
s.removeLeafNodes(s.tree, 2)''',
    expect=[1, None, 3, None, 4],
    result_fn=tree_list,
    views=[
        dict(type='tree', label='二叉树（红 = 值等于 target 的节点；最上面的 0 是假根）', pointers={'now': 'blue'}, h=420,
             color=lambda S, n: 'red' if n.val == S.get('target') and n.val != 0 else None),
        dict(type='calls', h=200),
    ],
    watch=[('target', 'target', 'red'), ('now', lambda S: S['_inner'].get('now'), 'blue'),
           ('now.left', lambda S: nv(S['_inner'].get('now').left) if S['_inner'].get('now') else None),
           ('now.right', lambda S: nv(S['_inner'].get('now').right) if S['_inner'].get('now') else None)],
    captions={
        'p_root = TreeNode(0)': '删节点要改它父亲的指针，可是根没有父亲 → 先造一个==假根== `p_root`',
        'p_root.left = root': '把真正的 `root` 挂在假根的左边，这样根也能被「断开」',
        'self.dfs(p_root, target)': '从假根开始 dfs，所有节点都有父亲了',
        'if now.left is not None': cap_l,
        'now.left = None': '左孩子返回了 `True` → `now.left = None`，把这个叶子断开',
        'if now.right is not None': cap_r,
        'now.right = None': '右孩子返回了 `True` → `now.right = None`，把这个叶子断开',
        'return now.left is None': cap_ret,
        'return p_root.left': '假根的左边就是处理后的树，返回它（原根被删时这里是空）',
    },
    cards=dict(
        one_liner='先处理孩子再看自己：删完孩子，自己可能成了新叶子',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['删除所有值等于 `target` 的叶子节点',
                 '删完后父亲可能成为新叶子，如果值也是 `target` 也要删，直到没有为止',
                 '示例：`[1,2,3,2,null,2,4]`，`target=2` → `[1,null,3,null,4]`'],
        quote='若我们需要删除节点now，实际上我们需要执行的操作是将now的父亲节点在now的这一侧断开连接，于是我们需要先设置一个假根节点p_head',
        quote_src='—— yiduobo 题解原文',
        idea=['删除 = 在父亲那一侧把指针置 `None`，所以根也需要一个父亲：假根 `p_root`',
              '`dfs(now)` 先递归左右孩子，返回 `True` 就断开',
              '孩子处理完后，若 `now` 左右都空且值等于 `target`，返回 `True` 交给上一层'],
        summary=['时间 `O(n)`；空间 `O(h)`',
                 '易错：必须==先递归孩子再判断自己==（后序），这样新出现的叶子才能被一并删掉',
                 '根节点本身也可能被删，所以用假根，最后返回 `p_root.left`',
                 '原文代码未改动（本来就是 Python 3 可运行）'],
    ),
)
