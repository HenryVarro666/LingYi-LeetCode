CONFIG = dict(
    num=536, title='从字符串生成二叉树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='栈 + 假根节点',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def str2tree(self, s):

        if len(s) == 0:
            return None

        now = None
        stack = []
        now_root = None
        neg_delta = 1

        phead = TreeNode(0)
        now_root = phead
        s = '(' + s + ')'
        p = 0
        n = len(s)
        while p < n:
            if s[p] == '(':
                p += 1
                neg_delta = 1
                if s[p] == '-':
                    neg_delta = -1
                    p += 1
                now = 0
                while s[p] >= '0' and s[p] <= '9':
                    now = now * 10 + int(s[p])
                    p += 1
                
                node = TreeNode(now * neg_delta)
                if now_root.left is None:
                    now_root.left = node
                else:
                    now_root.right = node
                
                stack.append(now_root)
                now_root = node
            
            elif s[p] == ')':
                now_root = stack.pop()
                p += 1
        
        return phead.left
''',
    call="Solution().str2tree('4(2(3)(1))(6)')",
    expect=[4, 2, 6, 3, 1],
    result_fn=tree_list,
    views=[
        dict(type='string', var='s', label='字符串 s（两侧已补括号，p = 当前位置）', pointers={'p': 'blue'}, cell=54, h=160),
        dict(type='tree', label='二叉树（蓝 = now_root，从假根 0 开始）', var='phead', pointers={'now_root': 'blue'}, path=False, h=330),
        dict(type='stack', var='stack', label='stack（待返回的祖先）', fmt=lambda n: str(n.val), h=150),
    ],
    watch=[('p', 'p', 'blue'), ('now_root', 'now_root.val', 'cyan'), ('now', 'now', 'yellow'), ('len(stack)', lambda S: len(S['stack']), 'green')],
    captions={
        'len(s) == 0': '空字符串 → 空树',
        'phead = TreeNode': '先造一个==假根== `0`，真正的根会是它的左孩子',
        'now_root = phead': '`now_root` 表示「当前正在描述哪个节点」，从假根开始',
        "s = '(' + s": '两侧补一对括号：这样每个节点值前面都有一个 `(`，规律统一 → `s = {s}`',
        "if s[p] == '('": lambda S, B, r: ('遇到 `(`：后面一定是一个节点值，新建节点并挂到 `now_root` 下' if S.s[S.p] == '(' else '不是 `(`，看是不是 `)`'),
        'neg_delta = 1': '先假设是正数',
        "if s[p] == '-'": lambda S, B, r: '遇到 `-` → 是负数' if S.s[S.p] == '-' else '没有负号',
        'now = 0': '开始读数字',
        "while s[p] >= '0'": lambda S, B, r: (f'`s[{S.p}] = {S.s[S.p]}` 是数字 → 继续读' if S.s[S.p] >= '0' and S.s[S.p] <= '9' else f'`s[{S.p}] = {S.s[S.p]}` 不是数字 → 数字读完，`now = {S.now}`'),
        'now = now * 10': '`now = {B.now} * 10 + {s[p]} = =={now}==`',
        'node = TreeNode': '新建节点 `{node.val}`',
        'if now_root.left is None': lambda S, B, r: (f'`{S.now_root.val}` 还没有左孩子 → 新节点做左孩子' if S.now_root.left is None else f'`{S.now_root.val}` 已有左孩子 → 新节点做右孩子'),
        'now_root.left = node': '`{now_root.val}` 的左孩子 = `{node.val}`',
        'now_root.right = node': '`{now_root.val}` 的右孩子 = `{node.val}`',
        'stack.append': '接下来描述的是 `{node.val}` 的子树，先把 `{now_root.val}` 压栈，等 `)` 时回来',
        'now_root = node': '`now_root` 换成新节点 `{now_root.val}`，后面的括号描述它的孩子',
        "elif s[p] == ')'": '遇到 `)`：当前节点的描述结束',
        'now_root = stack.pop()': '弹栈，回到上一个节点 `now_root = {now_root.val}`',
        'return phead.left': '真根是假根的左孩子 → 返回 `{phead.left.val}`',
    },
    skip=['p += 1', 'neg_delta = 1', 'now = None', 'stack = []', 'now_root = None', 'p = 0', 'n = len(s)', 'while p < n'],
    max_steps=100,
    cards=dict(
        one_liner='括号对应进出子树：遇 `(` 建点压栈，遇 `)` 弹栈',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['字符串由整数和括号组成：`整数(左子树)(右子树)`',
                 '括号里是子树，先左后右，空子树省略括号；整数可为负',
                 '示例：`"4(2(3)(1))(6)"` → `[4,2,6,3,1]`'],
        quote='除根节点外，其他所有节点值的左侧必然存在一个左括号，同时左括号也不会嵌套出现，因此可以在s的两侧额外添加一对括号来适配这个规律。',
        quote_src='—— yiduobo 题解原文',
        idea=['两侧补括号 + 假根节点：根也变成「某节点的左孩子」，统一处理',
              '`(`：读数字建 `node`，挂到 `now_root` 的左（没有）或右，旧 `now_root` 压栈',
              '`)`：这个节点描述完，栈顶弹出作为新的 `now_root`'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '易错：负号要单独处理；数字可能多位',
                 '真根是假根的 `left`，不是假根本身',
                 '原文为 Python 2 风格，无需改动'],
    ),
)
