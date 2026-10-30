def nv(x):
    return '空' if x is None else str(x.val)


def cap_base(S, B, ret):
    if S.original is None:
        return '`original` 是空节点 → 这条路走到头了，返回 `cloned`（也是空）'
    if S.original is S.target:
        return f'`original is target`：==比较的是节点本身，不是值== → 找到了，返回克隆树的同位置节点 `{S.cloned.val}`'
    return f'`original` = {S.original.val} 不是 `target`（{S.target.val}）→ 继续往下找'


def cap_left(S, B, ret):
    return f'左右子树里各走一步：原树 `{nv(B.original)}` 与克隆树 `{nv(B.cloned)}` ==同步下去==；左边找到就用左边，否则找右边'


CONFIG = dict(
    num=1379, title='找出克隆二叉树中的相同节点', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='两棵树同步 DFS',
    tags=['二叉树', '自底向上 DFS'],
    code='''
class Solution:
    def getTargetCopy(self, original: TreeNode, cloned: TreeNode, target: TreeNode) -> TreeNode:
        if original is None or original is target:
            return cloned
        return self.getTargetCopy(original.left, cloned.left, target) or \\
               self.getTargetCopy(original.right, cloned.right, target)
''',
    call='''s = Solution()
s.o = Tr([7,4,3,None,None,6,19])
s.c = Tr([7,4,3,None,None,6,19])
s.getTargetCopy(s.o, s.c, s.o.right.left)''',
    expect=6,
    result_fn=lambda n: n.val,
    views=[
        dict(type='tree', var='self.o', label='original（黄圈 = 当前递归路径，橙 = target）',
             pointers={'original': 'blue', 'target': 'orange'}, h=250),
        dict(type='tree', var='self.c', label='cloned（和 original 同步走）', pointers={'cloned': 'green'}, h=250),
        dict(type='calls', h=200),
    ],
    watch=[('original', lambda S: S['_inner'].get('original').val if S['_inner'].get('original') is not None else None, 'blue'),
           ('target', 'target.val', 'orange')],
    captions={
        'original is None or': cap_base,
        'return cloned': lambda S, B, r: ('空节点：返回 `cloned`，也就是 `None`，上一层的 `or` 会继续找右边' if S.cloned is None
                                          else f'`return cloned`：这个克隆节点（值 `{S.cloned.val}`）就是答案'),
        'self.getTargetCopy(original.left': '左子树的递归结果：两棵树同步走左儿子；==非空 = target 在左边==，`or` 短路直接返回；为空就去找右边',
        'self.getTargetCopy(original.right': '左边没找到 → 递归右子树；题目保证 target 一定存在，右边的返回值直接返回',
    },
    cards=dict(
        one_liner='原树和克隆树同步 DFS，原树碰到 target 时，克隆树走到的就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`（最坏退化成链的递归栈）',
        problem=['给原树 `original`、克隆树 `cloned` 和原树中的节点 `target`',
                 '返回 `cloned` 中与 `target` ==位置相同==的那个节点',
                 '本视频：`[7,4,3,null,null,6,19]`，target = 值为 `6` 的节点 → 返回克隆树的 `6`'],
        quote='注：由于我们比较的是节点而不是节点值（例如 C++ 比较的是地址），所以下面的代码也适用于树中有值相同节点的情况（本题的进阶问题）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两棵树==同形==，所以同时往左、同时往右，走到的位置始终对应',
              '`original is target`：比较的是节点对象，不看值 → 重复值也不怕',
              '左边返回非空 = 找到了；否则答案一定在右边'],
        summary=['时间 `O(n)`，空间 `O(n)`：最坏树成链，递归栈 n 层',
                 '易错：别写成 `original.val == target.val`，那样处理不了进阶（值重复）',
                 '`or` 的短路：左边找到就不会再进右边；空节点返回 `cloned`（也是空）',
                 '题解称之为先序遍历：先判断当前节点，再递归左右'],
    ),
)
