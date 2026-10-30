CONFIG = dict(
    num=993, title='二叉树的堂兄弟节点', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='层序遍历 · 记录父节点',
    tags=['灵神题单', '链表树与回溯', '难度分 1288'],
    code='''
class Solution(object):
    def isCousins(self, root, x, y):

        if root.val == x or root.val == y:
            return False

        fa_x = fa_y = 0
        q = [root]
        l = 0
        r = 1
        while l < r:
            for now in q[l : r]:
                if now.left:
                    q.append(now.left)
                    if now.left.val == x:
                        fa_x = now.val
                    if now.left.val == y:
                        fa_y = now.val
                if now.right:
                    q.append(now.right)
                    if now.right.val == x:
                        fa_x = now.val
                    if now.right.val == y:
                        fa_y = now.val
            
            if fa_x or fa_y:
                return fa_x and fa_y and fa_x != fa_y
            
            l, r = r, len(q)
''',
    call='Solution().isCousins(Tr([1,2,3,None,4,None,5]), 5, 4)',
    expect=True,
    views=[
        dict(type='tree', label='二叉树（蓝 = now，绿 = x / y）', pointers={'now': 'blue'}, path=False,
             color=lambda S, n: 'green' if n.val in (4, 5) else None, h=300),
        dict(type='array', var=lambda S: [n.val for n in S['q']], label='q（l..r-1 是当前层）',
             pointers={'l': 'blue'}, window=('l', 'r - 1'), cell=72, h=175),
        dict(type='text', fn=lambda S: f"`fa_x = {S.get('fa_x')}`（x 的父亲）    `fa_y = {S.get('fa_y')}`（y 的父亲）", size=26, h=56),
    ],
    watch=['l', 'r', ('now', lambda S: S['now'].val if S.get('now') else None, 'blue'), ('fa_x', 'fa_x', 'pink'), ('fa_y', 'fa_y', 'pink')],
    captions={
        'if root.val == x': '根没有父节点，也就没有堂兄弟 → 若 x 或 y 是根，直接返回 `False`；这里不是',
        'fa_x = fa_y = 0': '`fa_x`、`fa_y` 记录 x、y 的父节点值，0 表示还没遇到',
        'q = [root]': '`q` 当队列：`q[l:r]` 恰好是当前这一层，先放入根',
        'while l < r': '`q[l:r]` 非空 → 还有一层要处理（当前层下标 `{l}` 到 `{r-1}`）',
        'for now in q': '逐个取出当前层的节点 `{now.val}`，看它的儿子里有没有 x 或 y',
        'if now.left:': lambda S, B, r: (f'`{S.now.val}` 有左儿子 `{S.now.left.val}` → 入队，作为下一层' if S.now.left else f'`{S.now.val}` 没有左儿子 → 跳过'),
        'if now.right:': lambda S, B, r: (f'`{S.now.val}` 有右儿子 `{S.now.right.val}` → 入队，作为下一层' if S.now.right else f'`{S.now.val}` 没有右儿子 → 跳过'),
        'if now.left.val == x': '左儿子 `{now.left.val}` 等于 x（`{x}`）？ → 成立则 x 的父亲就是 `{now.val}`',
        'if now.left.val == y': '左儿子 `{now.left.val}` 等于 y（`{y}`）？ → 成立则 y 的父亲就是 `{now.val}`',
        'if now.right.val == x': '右儿子 `{now.right.val}` 等于 x（`{x}`）？ → 成立则 x 的父亲就是 `{now.val}`',
        'if now.right.val == y': '右儿子 `{now.right.val}` 等于 y（`{y}`）？ → 成立则 y 的父亲就是 `{now.val}`',
        'fa_x = now.val': '找到 x：它的父亲是 `{now.val}` → `fa_x = {fa_x}`',
        'fa_y = now.val': '找到 y：它的父亲是 `{now.val}` → `fa_y = {fa_y}`',
        'if fa_x or fa_y': lambda S, B, r: (f'这一层处理完：`fa_x = {S.fa_x}`，`fa_y = {S.fa_y}` → 至少一个出现了，==答案在这层就能定，不必再往下=={chr(10) if False else ""}' if (S.fa_x or S.fa_y) else '这一层处理完：`fa_x`、`fa_y` 都还是 0 → x、y 都不在下一层，继续看更深的层'),
        'return fa_x and fa_y': lambda S, B, r: f'两个同层出现（都非 0）且父亲 `{S.fa_x}` ≠ `{S.fa_y}` → 返回 `{r}`；若只出现一个，说明深度不同，返回假值',
        'l, r = r, len(q)': '这层没有 x、y → 进入下一层：`l = {l}`，`r = {r}`',
    },
    cards=dict(
        one_liner='深度相同 → 层序遍历；这一层同时遇到 x、y 且父亲不同',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二叉树节点值互不相同，给定两个值 `x` 和 `y`',
                 '深度相同、父节点不同才是==堂兄弟==',
                 '示例：`root = [1,2,3,null,4,null,5]`，`x = 5`，`y = 4` → `true`'],
        quote='注意到深度相同这一条件，很自然想到利用层序遍历来处理。当处理完某一层时，若某个节点已经被处理过：若另一个节点还没有被处理，说明两个节点深度不同，返回false。',
        quote_src='—— yiduobo 题解',
        idea=['深度相同这个条件，直接对应「层序遍历」',
              '处理每个节点时，看儿子是不是 x 或 y，并记下父亲 `fa_x`、`fa_y`',
              '一层处理完：两者都出现且父亲不同 → 真；只出现一个（深度不同）或父亲相同 → 假'],
        result='运行结束，返回 `True`',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：根节点没有父亲，要先特判；否则 `fa_x` 为 0 会被误当成「未出现」',
                 '易错：父亲值 0 作为「未出现」，依赖节点值 >= 1（题目保证 1 到 100）',
                 '对比灵神：灵神用 DFS 记深度和父亲，yiduobo 用 BFS 让「同一层」自然成立'],
    ),
)
