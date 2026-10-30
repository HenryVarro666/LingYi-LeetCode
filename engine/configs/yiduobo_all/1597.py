def _forest(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '节点栈里的子树（从左到右 = 栈底到栈顶；黄 = 刚合成的新根）', 24, T['muted'], bold=True)
    roots = list(S['node_stack'])
    inner = S['_inner']
    for k in ('x', 'y', 'node'):
        v = inner.get(k)
        if isinstance(v, TreeNode) and not any(v is r for r in roots):
            roots.append(v)

    def kids(nd):
        return [c for c in (nd.left, nd.right) if c is not None]

    seen = set()

    def mark(nd):
        for c in kids(nd):
            seen.add(id(c))
            mark(c)
    for r in roots:
        mark(r)
    roots = [r for r in roots if id(r) not in seen]
    if not roots:
        return

    def leaves(nd):
        ks = kids(nd)
        return 1 if not ks else sum(leaves(c) for c in ks)

    def depth(nd):
        return 1 + max([depth(c) for c in kids(nd)] or [0])
    total = sum(leaves(r) for r in roots) + 0.6 * (len(roots) - 1)
    unit = min(90, (x1 - x0 - 60) / total)
    dmax = max(depth(r) for r in roots)
    dy = min(90, (y1 - y0 - 90) / max(1, dmax - 1)) if dmax > 1 else 0
    rad = 26
    newest = S['node_stack'][-1] if S['node_stack'] else None
    pos = {}
    cur = x0 + 30 + ((x1 - x0 - 60) - total * unit) / 2

    def place(nd, d, left):
        ks = kids(nd)
        if not ks:
            pos[id(nd)] = (left + unit / 2, y0 + 70 + d * dy)
            return left + unit
        xs = []
        for c in ks:
            left = place(c, d + 1, left)
            xs.append(pos[id(c)][0])
        pos[id(nd)] = (sum(xs) / len(xs), y0 + 70 + d * dy)
        return left

    def draw_edges(nd):
        for c in kids(nd):
            cv.line([pos[id(nd)], pos[id(c)]], T['border'], 3)
            draw_edges(c)

    def draw_nodes(nd):
        X, Y = pos[id(nd)]
        hot = nd is newest and nd.left is not None
        cv.d.ellipse((X - rad, Y - rad, X + rad, Y + rad), fill=(70, 60, 30) if hot else T['panel2'],
                     outline=T['yellow'] if hot else T['border'], width=3 if hot else 2)
        cv.text((X, Y), nd.val, 26, T['text'], anchor='mm', bold=True)
        for c in kids(nd):
            draw_nodes(c)
    for r in roots:
        cur = place(r, 0, cur) + 0.6 * unit
    for r in roots:
        draw_edges(r)
    for r in roots:
        draw_nodes(r)


CONFIG = dict(
    num=1597, title='根据中缀表达式构造二叉表达式树', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='双栈：节点栈 + 运算符栈',
    tags=['常用数据结构', '链表树与回溯'],
    setup='Node = TreeNode',
    code='''
class Solution(object):
    def expTree(self, s):

        node_stack = []
        op_stack = []
        n = len(s)
        p = 0

        def calc():
            y, x = node_stack.pop(), node_stack.pop()
            op = op_stack.pop()

            node = Node(op)
            node.left = x
            node.right = y
            node_stack.append(node)

        while p < n:
            if '0' <= s[p] <= '9':
                start = p
                while p < n and '0' <= s[p] <= '9':
                    p += 1
                
                node = Node(s[start : p])
                node_stack.append(node)

            elif s[p] == '+' or s[p] == '-':
                while op_stack and op_stack[-1] != '(' and op_stack[-1] != ')':
                    calc()
                
                op_stack.append(s[p])
                p += 1
            
            elif s[p] == '*' or s[p] == '/':
                while op_stack and (op_stack[-1] == '*' or op_stack[-1] == '/'):
                    calc()
                
                op_stack.append(s[p])
                p += 1
            
            elif s[p] == '(':
                op_stack.append(s[p])
                p += 1
            else:
                while op_stack[-1] != '(':
                    calc()

                op_stack.pop()
                p += 1

        while op_stack:
            calc()

        return node_stack[-1]
''',
    call='Solution().expTree("2*(3+4)-6/2")',
    expect=['-', '*', '/', '2', '+', '6', '2', None, None, '3', '4'],
    result_fn=tree_list,
    views=[
        dict(type='string', var='s', label='表达式 s（蓝箭头 = 当前字符 p）', cell=56, h=190, pointers={'p': 'blue'},
             dim=lambda S, i, v: i < S['p']),
        dict(type='stack', var='node_stack', label='node_stack（子树的根，栈顶在右）', h=130, font=28,
             fmt=lambda nd: nd.val),
        dict(type='stack', var='op_stack', label='op_stack（运算符栈）', h=130, font=28),
        dict(type='custom', draw=_forest, h=300),
    ],
    watch=[('p', 'p', 'blue'), ('node_stack', lambda S: [x.val for x in S['node_stack']], 'green'), ('op_stack', 'op_stack', 'pink')],
    skip=['while p < n and', 'n = len(s)', 'start = p', 'p += 1', 'while p < n:', 'y, x = node_stack.pop()', 'op = op_stack.pop()', 'node.left = x'],
    captions={
        'node_stack = []': '和 772 同一套双栈，但数值栈里放的不是数，而是==子树的根节点==',
        'op_stack = []': '运算符栈和 772 完全一样',
        'p = 0': '`p` 从左往右扫描',
        "if '0' <= s[p] <= '9'": lambda S, B, r: (f'`s[{S.p}] = "{S.s[S.p]}"` 是数字 → 读完整个数，建一个叶子节点' if '0' <= S.s[S.p] <= '9'
                                                   else f'`s[{S.p}] = "{S.s[S.p]}"` 不是数字 → 看运算符或括号'),
        'while p < n and': lambda S, B, r: (f'`s[{S.p}]` 还是数字 → 继续' if S.p < S.n and '0' <= S.s[S.p] <= '9' else '数字读完，`s[start:p]` 是完整的数'),
        'node = Node(s[start': '建叶子节点 `Node("{node.val}")`',
        "elif s[p] == '+'": lambda S, B, r: (f'`s[{S.p}] = "{S.s[S.p]}"` 是 `+` / `-` → 栈里（到 `(` 为止）的运算都可以==建成子树==了'
                                              if S.s[S.p] in '+-' else f'`"{S.s[S.p]}"` 不是加减 → 看乘除'),
        "while op_stack and op_stack[-1] != '('": lambda S, B, r: (
            f'栈顶 `{S.op_stack[-1]}` 不是括号 → 先 `calc()`：把它和栈顶两个子树合成一棵' if S.op_stack and S.op_stack[-1] not in '()'
            else '栈空或栈顶是 `(` → 停，不越过括号'),
        "elif s[p] == '*'": lambda S, B, r: (f'`s[{S.p}] = "{S.s[S.p]}"` 是 `*` / `/`' if S.s[S.p] in '*/' else f'`"{S.s[S.p]}"` 不是乘除 → 看括号'),
        "while op_stack and (op_stack[-1] == '*'": lambda S, B, r: (
            f'栈顶 `{S.op_stack[-1]}` 也是乘除 → 先 `calc()`' if S.op_stack and S.op_stack[-1] in '*/'
            else '栈顶不是乘除 → 新的乘除可以压着它，先不建树'),
        'calc()': lambda S, B, r: (f'`calc()`：运算符 `{B.op_stack[-1]}` 当根，栈顶两棵子树当左右孩子'
                                    if S._line != 0 and B.op_stack else '`calc()` 合并子树'),
        'node = Node(op)': '运算符 `{op}` 变成新节点',
        'node.right = y': '`left = {x.val}` 子树（先入栈的），`right = {y.val}` 子树（后入栈的）',
        'node_stack.append(node)': lambda S, B, r: (f'叶子 `{S.node.val}` 入节点栈' if S.node.left is None else f'新子树（根 `{S.node.val}`）压回节点栈，等价于 772 里把结果压回数值栈'),
        'op_stack.append(s[p])': '运算符 `{s[p]}` 入栈：`{op_stack}`（右子树还没读到）',
        "elif s[p] == '('": lambda S, B, r: (f'`s[{S.p}]` 是 `(`，直接入栈' if S.s[S.p] == '(' else f'`s[{S.p}]` 只剩 `)`'),
        'while op_stack[-1] != ': lambda S, B, r: (f'遇到 `)`：栈顶 `{S.op_stack[-1]}` → 一路 `calc()` 到 `(`' if S.op_stack[-1] != '(' else '栈顶是 `(` → 括号内已合成一棵子树'),
        'op_stack.pop()': '弹出 `(`',
        'while op_stack:': lambda S, B, r: (f'扫完后栈里还剩 `{S.op_stack}` → 继续 `calc()`' if S.op_stack else '运算符栈空：节点栈只剩一个根'),
        'return node_stack[-1]': '节点栈里唯一的根就是整棵表达式树的根 `{ret.val}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='和 772 一样的双栈，只是“算出结果”改成“造出节点”',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给只含 `+ - * /`、括号和数字的中缀表达式 `s`',
                 '构造二叉表达式树：叶子是数字，内部节点是运算符',
                 '中序遍历该树要还原原表达式；本视频：`"2*(3+4)-6/2"`'],
        quote='对于题目中给出的表达式，如果其部分前缀可以进行计算，那么就可以将其做成一颗树，使用树的根节点来代替这部分前缀参与后续的运算。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 772 的方式扫描，只是 `calc()` 不再做运算',
              '`calc()` 弹两个子树 `x`、`y` 和一个运算符，造节点 `op` 并接成 `op.left=x, op.right=y`',
              '新的子树根压回节点栈，代替这段前缀参与后续运算'],
        result='树根是 `-`：左 `2*(3+4)`，右 `6/2` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：弹出顺序是先 `y`（右）后 `x`（左）',
                 '括号不进树，只影响运算符栈何时合并',
                 '这里用 `TreeNode(val)` 代替 `Node(val)`，原题的 `Node` 类需有 `left/right`，字段相同',
                 '原文已是 Python 3 可运行写法，无需改动；对照 772 的数值栈版本'],
    ),
)
