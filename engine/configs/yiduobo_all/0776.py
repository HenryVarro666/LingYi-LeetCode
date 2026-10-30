def _v(n):
    return 'None' if n is None else str(n.val)


CONFIG = dict(
    num=776, title='拆分二叉搜索树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归切分',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def splitBST(self, root, target):

        def dfs(now):
            if now is None:
                left = None
                right = None
            elif now.val == target:
                left = now
                right = now.right
                now.right = None
            elif now.val > target:
                left, right = dfs(now.left)
                now.left = right
                right = now
            else:
                left, right = dfs(now.right)
                now.right = left
                left = now
            
            return [left, right]

        return dfs(root)
''',
    call='Solution().splitBST(Tr([4, 2, 6, 1, 3, 5, 7]), 3)',
    expect=[[2, 1, 3], [4, None, 6, 5, 7]],
    result_fn=lambda r: [tree_list(r[0]), tree_list(r[1])],
    views=[
        dict(type='tree', label='二叉搜索树（蓝 = now；断开 / 重连会实时变化）', pointers={'now': 'blue'}, h=330),
        dict(type='text', fn=lambda S: f"本层结果：`left = {_v(S['_inner'].get('left'))}`（≤ target 的一半），`right = {_v(S['_inner'].get('right'))}`（> target 的一半）" if 'left' in S['_inner'] else '', size=24, h=60),
        dict(type='calls', h=200),
    ],
    watch=[('now', lambda S: _v(S['_inner'].get('now')), 'blue'), ('target', 'target', 'yellow'),
           ('left', lambda S: _v(S['_inner'].get('left')), 'green'), ('right', lambda S: _v(S['_inner'].get('right')), 'pink')],
    captions={
        'return dfs(root)': '从根开始递归切分，返回 `[left, right]`',
        'if now is None': lambda S, B, r: '`now` 为空 → 没有东西可切，返回两个空' if S.now is None else '`now` 不为空，继续判断',
        'left = None': '空节点：`left` 和 `right` 都是空',
        'elif now.val == target': lambda S, B, r: f'`now.val = {S.now.val}`，和 `target = {S.target}` ' + ('==相等== → 就是要找的节点' if S.now.val == S.target else '不相等'),
        'now.right = None': '把 `now` 和右子树断开，`now.right = None`',
        'elif now.val > target': lambda S, B, r: (f'`now.val = {S.now.val}` > `target = {S.target}` → target 在左子树，先去切 `now.left`' if S.now.val > S.target else f'`now.val = {S.now.val}` < `target = {S.target}` → target 在右子树，先去切 `now.right`'),
        'left, right = dfs(now.left)': lambda S, B, r: f'左子树切好了：`left = {_v(S.left)}`，`right = {_v(S.right)}`',
        'now.left = right': lambda S, B, r: f'切出的右半部分（> target）接回来当 `now.left`：`{S.now.val}.left = {_v(S.now.left)}`',
        'right = now': lambda S, B, r: f'`now` 连同它的右子树都 > target，所以它是 ==右半部分的根==：`right = {S.right.val}`',
        'left, right = dfs(now.right)': lambda S, B, r: f'右子树切好了：`left = {_v(S.left)}`，`right = {_v(S.right)}`',
        'now.right = left': lambda S, B, r: f'切出的左半部分（≤ target）接回来当 `now.right`：`{S.now.val}.right = {_v(S.now.right)}`',
        'left = now': lambda S, B, r: (f'`now` 及它的左子树都 ≤ target → `left = {S.left.val}`' if S.now.val == S.target else f'`now` 连同它的左子树都 ≤ target，所以它是 ==左半部分的根==：`left = {S.left.val}`'),
        'right = now.right': lambda S, B, r: f'`now.right` 里的值全都 > target → `right = {_v(S.right)}`',
        'return [left, right]': lambda S, B, r: f'返回这一层的切分结果：`left = {_v(S.left)}`，`right = {_v(S.right)}`',
    },
    cards=dict(
        one_liner='target 在哪边，就先切哪边，再把切出来的一半接回去',
        complexity='时间 `O(h)`，空间 `O(h)`',
        problem=['给二叉搜索树 `root` 和整数 `target`，拆成两棵树',
                 '一棵所有值 `≤ target`，另一棵所有值 `> target`；尽量保留原来的结构',
                 '示例：`root = [4,2,6,1,3,5,7]`，`target = 3` → `[[2,1,3],[4,null,6,null,null,5,7]]`'],
        quote='题目要求尽量保留原树的结构，那么节点now而言，若target位于其左子树中，那么应当将now.left先进行切分，然后将切分得到的右半部分作为新的now.left。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now.val == target`：`now` 带左子树归左半，`now.right` 整体归右半，断开',
              '`now.val > target`：先切左子树，右半部分接回 `now.left`，`now` 成为右半部分的根',
              '`now.val < target`：与上面对称，切右子树，左半部分接回 `now.right`'],
        summary=['时间 `O(h)`，只沿一条路径下去；空间 `O(h)`',
                 '易错：返回 `[left, right]` 时，`left` 是 ≤ target 的一半',
                 '`now.right = None` 一定要断开，否则两棵树还连在一起',
                 '原文为 Python 2 风格，无需改动'],
    ),
)
