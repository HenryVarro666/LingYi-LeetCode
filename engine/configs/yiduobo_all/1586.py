def _in(S):
    return list(S.get('self.inorder') or [])


def _stk(S):
    return [n.val for n in (S.get('self.stack') or [])]


def _ccol(S, n):
    if n in (S.get('self.stack') or []):
        return 'yellow'
    if n.val in (S.get('self.inorder') or []):
        return 'green'
    return None


def _cap_next(S, B, r):
    s = S.self
    if B['self.p'] == len(B['self.inorder']):
        return f'`p = {B["self.p"]}` 等于记录数组长度 → 要往前走一个新节点：栈顶 `{S.self.stack[-1].val if s.stack else None}` 就是下一个'
    return f'`p = {B["self.p"]}` 还没到记录数组末尾 → 这是 ==prev 之后的 next==，直接读记录'


CONFIG = dict(
    num=1586, title='二叉搜索树迭代器 II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='栈模拟中序 · 数组记录支持 prev',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class BSTIterator(object):

    def __init__(self, root):
        self.inorder = []
        self.stack = []
        self.p = 0
        self.add_left(root)

    def add_left(self, now):
        while now:
            self.stack.append(now)
            now = now.left

    def hasNext(self):
        return self.p < len(self.inorder) or len(self.stack) > 0

    def next(self):
        if self.p == len(self.inorder):
            self.inorder.append(self.stack[-1].val)
            node = self.stack.pop()
            self.add_left(node.right)

        res = self.inorder[self.p]
        self.p += 1
        
        return res

    def hasPrev(self):
        return self.p > 1

    def prev(self):
        self.p -= 1
        return self.inorder[self.p - 1]
''',
    call='''tree_root = Tr([7, 3, 15, None, None, 9, 20])
it = BSTIterator(tree_root)
out = []
out.append(it.next())
out.append(it.next())
out.append(it.prev())
out.append(it.next())
out.append(it.hasNext())
out.append(it.next())
out.append(it.hasPrev())
out.append(it.prev())
out''',
    expect=[3, 7, 3, 7, True, 9, True, 7],
    views=[
        dict(type='tree', var='tree_root', label='BST（黄 = 在栈里，绿 = 已访问并记录）', path=False, h=250,
             color=_ccol),
        dict(type='array', var=_in, label='self.inorder（已访问的中序记录）', h=170, pointers={'self.p': 'blue'}),
        dict(type='stack', var=_stk, label='self.stack（从下到上；栈顶 = 下一个）', h=120),
        dict(type='calls', h=130),
    ],
    watch=[('p', 'self.p', 'blue'),
           ('out', 'out', 'green')],
    max_steps=120,
    captions={
        'self.inorder = []': '`inorder`：把 `next` 走过的节点值记下来，==`prev` 直接读它==',
        'self.stack = []': '`stack`：从根往左走的路径，栈顶就是下一个要访问的节点',
        'self.p = 0': '`p`：当前位置（已返回了几个数）',
        'self.add_left(root)': '先把根沿左链全部压栈：栈顶是最小的节点',
        'while now': lambda S, B, r: (f'节点 `{S.now.val}` 存在 → 压栈并继续往左' if S.now else '走到空 → 左链压完了'),
        'self.stack.append(now)': '`{now.val}` 入栈',
        'now = now.left': '往左孩子走',
        'return self.p < len': lambda S, B, r: f'`p = {S.self.p} < len(inorder) = {len(S.self.inorder)}`（还能重放记录）或 栈非空（还有新节点）→ =={r}==',
        'if self.p == len(self.inorder)': lambda S, B, r: ('`p` 等于记录长度 → 要往前走新节点，取栈顶' if S.self.p == len(S.self.inorder)
                                                          else '`p` 小于记录长度 → ==prev 之后的 next==，直接读记录'),
        'self.inorder.append': '栈顶 `{self.stack[-1].val}` 就是中序的下一个 → 记进 `inorder`，以后 prev 直接读',
        'node = self.stack.pop()': '弹出栈顶 `{node.val}`',
        'self.add_left(node.right)': lambda S, B, r: f'后继在右子树的最左：对 `node.right` 做一次 add_left（右孩子为空则什么也不压）',
        'res = self.inorder[self.p]': '返回值 = `inorder[{p}]` = `{res}`'.replace('{p}', '{self.p}'),
        'self.p += 1': '`p` 前进到 `{self.p}`',
        'return res': '`next` 返回 `{res}`',
        'return self.p > 1': lambda S, B, r: f'`p = {S.self.p} > 1` → =={r}==：当前数前面还有数，才能 prev',
        'self.p -= 1': '`p` 后退到 `{self.p}`',
        'return self.inorder[self.p - 1]': '`prev` 返回 `inorder[{self.p} - 1]` = =={ret}==（`p` = 已走过的个数，回退一格后当前数是 `inorder[p-1]`）',
    },
    cards=dict(
        one_liner='next 时顺手记录，prev 就只是在记录里往回读',
        complexity='`next` 均摊 `O(1)`，`prev`/`hasNext`/`hasPrev` 均 `O(1)`；空间 `O(n)`',
        problem=['实现 BST 迭代器：`next()`、`hasNext()`、`prev()`、`hasPrev()`',
                 '`next` 按中序向后走，`prev` 往回走（指针在第一个数之前也能 `hasPrev` 判断）',
                 '示例：`next,next,prev,next` → `3,7,3,7`'],
        quote='由于prev操作总是发生在next操作之后，那么如果在执行next操作时顺便将遍历到的节点记录下来，对于prev操作就可以直接通过这个记录下来的数组得到了。',
        quote_src='—— yiduobo 题解原文',
        idea=['不预先遍历：用栈保存“还没访问的左链”，栈顶就是后继',
              '后继三种情况：已记录过（读记录）、有右孩子（右子树最左）、否则栈顶祖先',
              '访问右孩子时只需对它 `add_left`，栈里剩下的就是更上层祖先'],
        summary=['`next` 均摊 `O(1)`：每个节点最多进栈出栈一次；空间 `O(n)`',
                 '易错：`p` 表示已返回个数，`prev` 返回的是 `inorder[p-1]`（先 `p -= 1`）',
                 '易错：`next` 要先判断 `p == len(inorder)`，否则是 prev 之后的重放，不能再弹栈',
                 '原文为 Python 2 风格，本视频无需改动即可在 Python 3 运行'],
    ),
)
