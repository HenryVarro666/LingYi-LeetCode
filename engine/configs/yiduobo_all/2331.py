def nv(x):
    return '空' if x is None else str(x.val)


CONFIG = dict(
    num=2331, title='计算布尔二叉树的值', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='递归 · 后序求值',
    tags=['二叉树', '自底向上 DFS', '难度分 1304'],
    code='''
class Solution(object):
    def evaluateTree(self, root):

        def dfs(now):
            if now.left:
                if now.val == 2:
                    return dfs(now.left) or dfs(now.right)
                else:
                    return dfs(now.left) and dfs(now.right)
            else:
                return now.val == 1

        return dfs(root)
''',
    call='''s = Solution()
s.tree = Tr([3,2,2,1,0,0,1])
s.evaluateTree(s.tree)''',
    expect=True,
    views=[
        dict(type='tree', var='self.tree', label='布尔树（2 = OR，3 = AND，0/1 = 叶子；蓝 = now）', pointers={'now': 'blue'}, h=330),
        dict(type='text', fn=lambda S: ('当前节点：' + ({0: '叶子 0 = False', 1: '叶子 1 = True', 2: 'OR 节点', 3: 'AND 节点'}[S['_inner']['now'].val] if 'now' in S['_inner'] else '')), size=26, h=60),
        dict(type='calls', h=220, hide=('self',)),
    ],
    watch=[('now', lambda S: nv(S['_inner'].get('now')), 'blue')],
    captions={
        'def dfs': '`dfs(now)`：返回以 `now` 为根的子树的布尔值',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有孩子 → 是运算节点，先算左右孩子的值再运算' if S.now.left
                                        else f'`{S.now.val}` 没有孩子 → 是==叶子==，值就是它自己'),
        'if now.val == 2': lambda S, B, r: ('值为 `2` → ==OR==：左右有一个真就行' if S.now.val == 2 else '值不是 `2`（是 `3`）→ ==AND==：左右都真才行'),
        'return dfs(now.left) or': 'OR 节点 `{B.now.val}`：先递归左孩子 `{B.now.left.val}`，==左边为真就短路==，不必再算右边；左边为假才算右孩子 `{B.now.right.val}`',
        'return dfs(now.left) and': 'AND 节点 `{B.now.val}`：先递归左孩子 `{B.now.left.val}` 再递归右孩子 `{B.now.right.val}`，两个都为真才为真（左边为假会短路）',
        'return now.val == 1': '叶子 `{now.val}`：`{now.val} == 1` → ==`{ret}`==',
        'return dfs(root)': lambda S, B, r: ('从根出发：`dfs(root)`' if r is None else f'根节点算出来的就是整棵树的值：=={r}=='),
    },
    skip=['else:'],
    cards=dict(
        one_liner='叶子直接取值，运算节点先算两个孩子再 and / or',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['完整二叉树：叶子是 `0`（False）或 `1`（True）',
                 '非叶子是 `2`（OR）或 `3`（AND），对两个孩子的值做运算',
                 '本视频：`[3,2,2,1,0,0,1]` → `True`'],
        quote='若now不是叶子节点，那么先递归求解now.left和now.right，然后根据now.val选择与运算或者或运算。',
        quote_src='—— yiduobo 题解原文',
        idea=['从根递归：叶子（没有 `left`）返回 `now.val == 1`',
              '非叶子：`val == 2` 用 `or`，否则用 `and`',
              '先有孩子的结果才能算自己 → ==后序==，自底向上'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '完整二叉树要么 0 个孩子要么 2 个，所以只判断 `now.left` 就能区分叶子',
                 '`or` / `and` 有短路：OR 左边为真就不再算右边；AND 左边为假同理',
                 '原文为 Python 2 风格（`class Solution(object)`），代码没有改动'],
    ),
)
