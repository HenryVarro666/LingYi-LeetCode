CONFIG = dict(
    num=1028, title='从先序遍历还原二叉树', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='栈维护当前路径',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def recoverFromPreorder(self, S):

        stack = []
        l = len(S)
        now = 0

        while now < l:
            level = 0
            while now < l and S[now] == '-':
                level += 1
                now += 1
            
            num = 0
            while now < l and S[now] != '-':
                num = num * 10 + ord(S[now]) - 48
                now += 1

            while level < len(stack):
                stack.pop()
            
            node = TreeNode(num)
            if len(stack) > 0:
                if stack[-1].left is None:
                    stack[-1].left = node
                else:
                    stack[-1].right = node
            
            stack.append(node)
        
        return stack[0]
''',
    call="Solution().recoverFromPreorder('1-2--3--4-5')",
    expect=[1, 2, 5, 3, 4],
    result_fn=tree_list,
    views=[
        dict(type='string', var='S', label='先序字符串 S（now 指向正在读的位置）', pointers={'now': 'blue'}, cell=60, h=130),
        dict(type='text', fn=lambda S: f"当前节点：深度 `level = {S['level']}`，值 `num = {S['num']}`" if 'num' in S and 'level' in S else '', size=26, h=56),
        dict(type='tree', label='二叉树（黄圈 = 栈中节点）', var='stack', pointers={'node': 'blue'}, path=False, h=300),
        dict(type='stack', var='stack', label='stack（根 → 当前路径）', fmt=lambda n: str(n.val), h=170),
    ],
    watch=[('now', 'now', 'blue'), 'level', 'num', ('len(stack)', lambda S: len(S['stack']), 'green')],
    captions={
        'stack = []': '`stack` 保存「根到当前节点」的路径，栈的长度就是路径深度',
        'level = 0': '新读一个节点：先数前面有几个 `-`，那就是它的深度',
        "S[now] == '-'": lambda S, B, r: f"`S[{S.now if 'now' in S else 0}]` 是 `-` → 深度 +1" if S.now < len(S.S) and S.S[S.now] == '-' else '没有更多 `-` 了，深度读完',
        'level += 1': '深度 `level = {level}`',
        'num = num * 10': '读入一位数字，`num = {B.num} * 10 + 新数字 = =={num}==`',
        'while level < len(stack)': lambda S, B, r: (f'`level = {S.level} < len(stack) = {len(S.stack)}`：栈顶不是它的祖先，其子树已遍历完 → 弹出' if S.level < len(S.stack) else ('`stack` 为空，还没有父节点' if not S.stack else f'`level = {S.level}` 不小于 `len(stack) = {len(S.stack)}` → 栈顶就是它的父节点')),
        'stack.pop()': '弹出栈顶，`len(stack) = {len(stack)}`',
        'node = TreeNode': '新建节点 `{num}`',
        'if len(stack) > 0': lambda S, B, r: ('栈非空 → 栈顶 `%d` 是父节点' % S.stack[-1].val) if S.stack else '栈为空 → 它是整棵树的根',
        'if stack[-1].left is None': lambda S, B, r: ('父节点还没有左孩子 → 先挂左边' if S.stack[-1].left is None else '父节点已有左孩子 → 挂到右边'),
        'stack[-1].left = node': '`{stack[-1].val}` 的左孩子 = `{node.val}`',
        'stack[-1].right = node': '`{stack[-1].val}` 的右孩子 = `{node.val}`',
        'stack.append': '`{node.val}` 入栈，它成为下一个节点的候选父节点',
        'return stack[0]': '栈底永远是根节点 `{stack[0].val}`，返回它',
    },
    skip=['now += 1', 'stack = []', 'l = len(S)', 'now = 0', 'num = 0'],
    max_steps=100,
    cards=dict(
        one_liner='用栈保存当前路径：栈长 = 深度，弹到比自己浅就是父亲',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['先序遍历：每个节点前有 `D` 条短划线，`D` 是它的深度，根深度为 0',
                 '只有一个子节点时，保证它是==左孩子==',
                 '示例：`"1-2--3--4-5"` → `[1,2,5,3,4]`'],
        quote='对于一个位于第k层的节点而言：其父节点必然是离该节点最近，且先序遍历在其之前的第k - 1层的节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先序遍历是 dfs 序，用栈维护「根到当前」的路径',
              '新节点深度 `level`：把栈弹到只剩 `level` 个，栈顶就是父亲',
              '父亲没有左孩子就挂左边，否则挂右边'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：数字可能不止一位，要逐位累加；深度要先读 `-` 再读数字',
                 '`while level < len(stack)`：深度相同的栈顶是兄弟，也要弹出',
                 '原文为 Python 2 风格，无需改动'],
    ),
)
