def _v(n):
    return 'None' if n is None else str(n.val)


CONFIG = dict(
    num=998, title='最大二叉树 II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归复制 + 插入右链',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def insertIntoMaxTree(self, root, val):
        if val > root.val:
            res = TreeNode(val)
            res.left = self.dfs(root, 0)
        else:
            res = self.dfs(root, val)

        return res

    def dfs(self, now, val):
        ret = TreeNode(now.val)
        if now.left:
            ret.left = self.dfs(now.left, 0)
        if now.right:
            if now.right.val < val:
                ret.right = TreeNode(val)
                ret.right.left = self.dfs(now.right, 0)
            else:
                ret.right = self.dfs(now.right, val)
        elif val > 0:
            ret.right = TreeNode(val)

        return ret
''',
    call='''s = Solution()
s.tree = Tr([5, 2, 4, None, 1])
tree_list(s.insertIntoMaxTree(s.tree, 3))''',
    expect=[5, 2, 4, None, 1, None, 3],
    views=[
        dict(type='text', fn=lambda S: f"插入值 `val = {S['_inner'].get('val')}`；`val = 0` 表示「已经插入过 / 只是复制」" if 'now' in S['_inner'] else '原树 A（5 是根）；要把 `val = 3` 追加到 B 的最右边', size=24, h=56),
        dict(type='tree', var='self.tree', label='原树 A（蓝 = now，递归复制它）', pointers={'now': 'blue'}, h=300),
        dict(type='calls', h=230),
    ],
    watch=[('now', lambda S: getattr(S['_inner'].get('now'), 'val', None), 'blue'), ('val', lambda S: S['_inner'].get('val'), 'yellow'), ('ret', lambda S: getattr(S['_inner'].get('ret'), 'val', None), 'green')],
    captions={
        'if val > root.val': '`val = {val}` 和根 `{root.val}` 比：根更大 → ==val 不是最大值，只能插到右边==',
        'res = TreeNode(val)': '`val` 比根还大 → 它是 B 的最大值，==做新根==，原树整体当左子树',
        'res.left = self.dfs(root, 0)': '`val = 0` 表示不再插入：把原树完整复制成 `res` 的左子树',
        'res = self.dfs(root, val)': '`val` 小于根 → 根不变，沿右侧找位置，带着 `val` 递归复制',
        'ret = TreeNode(now.val)': '复制当前节点 `{now.val}` 得到 `ret`：这里有大前提 `now.val > val`',
        'ret.left = self.dfs(now.left, 0)': '`now` 的左侧和 A 完全一致 → 直接复制左子树（`val = 0`）',
        'if now.right.val < val': '右儿子 `{now.right.val}` 与 `val = {val}` 比：{"右儿子更小 → val 应该插在它上面" if now.right.val < val else "右儿子更大 → val 还要往右子树里找"}',
        'ret.right = TreeNode(val)': '`val = {val}` 变成 `ret` 的新右儿子',
        'ret.right.left = self.dfs(now.right, 0)': '原来的右子树整体挂到新节点 `{val}` 的左边（复制，`val = 0`）',
        'ret.right = self.dfs(now.right, val)': '右儿子更大 → 子问题：以右儿子为根，继续插入 `val = {val}`',
        'elif val > 0': '右边为空：`val = {val}` ' + '{"> 0，还没插入 → ==新建它做右儿子==" if val > 0 else "= 0，已经插过了 → 无事可做"}',
        'return ret': lambda S, B, r: f'复制完成，返回以 `{r.val}` 为根的新子树',
        'return res': lambda S, B, r: '得到新树：3 挂在 4 的右边，因为 B 的末尾是 3',
    },
    cards=dict(
        one_liner='val 在 B 的最右边：比根大就当新根，否则沿右侧找位置',
        complexity='时间 `O(n)`（整棵树被复制一遍），空间 `O(h)` 递归栈',
        problem=['最大树：根是最大值，左子树来自最大值左边，右子树来自右边',
                 '给你最大树 `root`（由数组 A 构造），把 `val` ==追加到 A 末尾== 得到 B，返回 B 对应的最大树',
                 '本视频：`root = [5,2,4,null,1]`，`val = 3` → `[5,2,4,null,1,null,3]`'],
        quote='当val大于root.val时，说明此时val是B中的最大值，因此应该构造值为val的节点node作为新的根节点，同时递归复制树root作为node的左子树。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`val` 小于根：设当前节点 `now`，复制 `now`；左侧与 A 一致，直接复制',
              '右侧 = A 的右侧 + val，是同样的子问题：右儿子比 `val` 小就把 `val` 插在这里，否则继续递归',
              '`dfs(now, 0)` 的 `0` 表示 val 已经用掉，只复制；右侧为空且 `val > 0` 就新建它'],
        summary=['时间 `O(n)`、空间 `O(h)`：这个写法把树完整复制了一遍，没有改原树',
                 '易错：`val` 为 0 当作「不再插入」的哨兵，题目 `val >= 1` 所以安全',
                 '右侧为空的边界：`elif val > 0` 才新建节点',
                 '原文为 Python 2 风格：删去了函数开头的空白行（代码本身未改）'],
    ),
)
