PAR = {}   # uid -> (父节点, 'L'/'R')，第一次看到整棵树时记下来，用于字幕和路径显示


def _learn(node):
    if PAR or node is None:
        return
    st = [node]
    while st:
        n = st.pop()
        for side, ch in (('L', n.left), ('R', n.right)):
            if ch is not None:
                PAR[ch._uid] = (n, side)
                st.append(ch)


def _path(node):
    out = []
    while node is not None:
        out.append(node.val)
        node = PAR.get(node._uid, (None, ''))[0]
    return out[::-1]


def _info(S):
    r = S.get('root')
    if r is None:
        return '从 `targetSum = 22` 出发，==每往下走一步就减去节点值==，到叶子时看是否恰好减到 0'
    p = ' → '.join(map(str, _path(r)))
    return f"当前路径 `{p}`，剩余 `targetSum = {S['targetSum']}`"


def _cap_none(S, B, ret):
    _learn(B.root)
    r = B.root
    if r is None:
        return '空节点：这里没有路径 → 返回 False'
    if PAR.get(r._uid, (None, ''))[1] == 'R':
        return f'左子树没找到（返回 False）→ `or` 继续递归==右子树==：来到 `{r.val}`'
    return f'来到节点 `{r.val}`（不是空节点），剩余目标 `targetSum = {B.targetSum}`'


def _cap_leaf(S, B, ret):
    r = S.root
    if r.left is None and r.right is None:
        return f'`{r.val}` 没有儿子，是==叶子== → 看 targetSum 是否恰好减到 0'
    return f'`{r.val}` 不是叶子 → 继续往下递归，把 `targetSum = {S.targetSum}` 传下去'


def _cap_leaf_ret(S, B, ret):
    if ret:
        return f'叶子 `{S.root.val}`：`targetSum == 0` → ==找到了==！返回 True'
    return f'叶子 `{S.root.val}`：`targetSum = {S.targetSum} ≠ 0` → 这条路不行，返回 False'


def _cap_rec(S, B, ret):
    l = B.root.left
    return (f'先递归左子树 `{l.val if l else None}`，带着 `targetSum = {B.targetSum}`；'
            f'左边返回 True 就==不用看右边==（`or` 短路）')


CONFIG = dict(
    num=112, title='路径总和', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='递归 · 倒着减小 targetSum',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        targetSum -= root.val
        if root.left is None and root.right is None:  # root 是叶子
            return targetSum == 0
        return self.hasPathSum(root.left, targetSum) or self.hasPathSum(root.right, targetSum)
''',
    call='Solution().hasPathSum(Tr([5,4,8,11,None,13,4,7,2,None,None,None,1]), 22)',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = 当前 root）', pointers={'root': 'blue'}, h=400),
        dict(type='calls', h=210),
    ],
    watch=[('root', 'root.val', 'blue'), ('targetSum', lambda S: S['_inner'].get('targetSum'), 'yellow')],
    captions={
        'if root is None': _cap_none,
        'targetSum -= root.val': '减去当前节点值：`targetSum = {B.targetSum} - {root.val} = =={targetSum}==`',
        'if root.left is None and root.right is None': _cap_leaf,
        'return targetSum == 0': _cap_leaf_ret,
        'return self.hasPathSum': _cap_rec,
    },
    cards=dict(
        one_liner='从 targetSum 开始，沿路减去节点值，到叶子恰好为 0 就找到了',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['给你二叉树的根 `root` 和整数 `targetSum`',
                 '判断是否存在==根节点到叶子节点==的路径，路径上节点值之和等于 `targetSum`',
                 '示例：`root = [5,4,8,11,null,13,4,7,2,null,null,null,1]`',
                 '`targetSum = 22` → `true`（`5 + 4 + 11 + 2 = 22`）'],
        quote='我们可以从 targetSum=22 开始，==不断地减去路径上的节点值==，如果走到叶子节点发现 targetSum=0，就说明我们找到了一条符合题目要求的路径。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「倒着减小」让我们可以==直接递归调用 hasPathSum==，不用额外的辅助函数',
              '空节点返回 False；叶子节点判断 `targetSum == 0`',
              '否则：左子树找到就返回 True，否则返回右子树的结果'],
        result='返回 `True`：路径 `5 → 4 → 11 → 2` 的和恰好是 22 ✓',
        summary=['时间 `O(n)`；空间 `O(n)`：树退化成链时递归栈深度为 n',
                 '易错：必须在==叶子==处判断，不能在空节点处判断 0（单孩子节点会误判）',
                 '`or` 短路：左边找到就不再递归右边',
                 '同类：113 路径总和 II（记录路径）、437 路径总和 III（前缀和）'],
    ),
)
