def _inf(S):
    if 'now' not in S:
        return '节点值 ==等于所有后代节点值之和== 时计数（叶子的后代和为 0）'
    return '后序：先拿到左右子树和 `s`，再和自己的值比较；相等 `res` +1'


CONFIG = dict(
    num=1973, title='值等于子节点之和的节点数量', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='后序 dfs · 返回子树和',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def equalToDescendants(self, root):

        global res
        res = 0

        def dfs(now):
            s = 0
            if now.left:
                s += dfs(now.left)
            if now.right:
                s += dfs(now.right)

            global res
            if s == now.val:
                res += 1

            return s + now.val

        dfs(root)
        return res
''',
    call='Solution().equalToDescendants(Tr([10,3,4,2,1]))',
    expect=2,
    views=[
        dict(type='text', fn=_inf, size=26, h=60),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=320),
        dict(type='text', fn=lambda S: (f"本层 `s`（后代和）= {S['_inner']['s']}，`now.val` = {S['now'].val}" if 's' in S['_inner'] and 'now' in S else ''), size=26, h=60),
        dict(type='calls', h=240),
    ],
    watch=[('now', 'now.val', 'blue'), ('s', lambda S: S['_inner'].get('s'), 'cyan')],
    captions={
        'res = 0': '`res` 计数，`global` 让 dfs 里也能修改',
        's = 0': '`s` 累计 `{now.val}` 的所有后代节点值之和，先清零',
        's += dfs(now.left)': '递归左孩子 `{B.now.left.val}`：它返回整棵左子树的和，累加进 `s`',
        's += dfs(now.right)': '递归右孩子 `{B.now.right.val}`：它返回的整棵右子树的和也累加进 `s`',
        'if s == now.val': lambda S, B, r: (f'`s = {S.s}` == `now.val = {S.now.val}` → ==满足条件==' if S.s == S.now.val
                                           else f'`s = {S.s}` != `now.val = {S.now.val}` → 不计数'),
        'res += 1': '后代和等于自己 → `res` 加 1',
        'return s + now.val': lambda S, B, r: f'返回给父节点的是整棵子树的和：`{S.s} + {S.now.val}` = =={r}=='
                                              '（父亲要的是包含 now 在内的和）',
        'dfs(root)': '从根开始后序 dfs',
        'return res': '一共 `{ret}` 个节点满足',
    },
    skip=['global res'],
    cards=dict(
        one_liner='后序 dfs：先拿到左右子树和，再和自己比',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['给你一棵二叉树的根 `root`',
                 '统计节点值==等于所有后代节点值之和==的节点个数',
                 '没有后代时，后代之和视为 `0`',
                 '本视频：`root = [10,3,4,2,1]` → `2`（节点 10 和 3）'],
        quote='对于当前节点now，先递归求解now的左右孩子节点，并取得左右子树中所有节点值之和，若左右子树节点之和恰好等于now.val，那么就更新答案，然后将返回左右节点值之和再加上now.val提供给上层的节点使用。',
        quote_src='—— yiduobo 题解原文',
        idea=['典型的子树节点和问题：一趟后序 dfs 就够',
              '`s` 是左右子树之和（不含自己），`s == now.val` 就计数',
              '返回值要把自己的值加上，这样父节点拿到的才是完整子树和'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：返回 `s` 而不是 `s + now.val`，父节点就少算了孩子的值',
                 '叶子的 `s = 0`，只有叶子值恰为 0 才计数',
                 '用 `global res` 累计，赋值前要在函数内声明',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
