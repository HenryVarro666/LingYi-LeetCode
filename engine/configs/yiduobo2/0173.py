VALS = [7, 3, 15, None, None, 9, 20]
_ROOT = Tr(VALS)
ALL = sorted(v for v in VALS if v is not None)


def _stack_vals(S):
    return [n.val for n in (S.get('self.stack') or [])]


def _returned(S):
    """已经被 next() 返回过的值（BST 中序：比栈里最小值还小的都已访问）"""
    if 'root' in S:  # 还在 __init__
        return set()
    res = S.get('res')
    if res is not None:
        return {v for v in ALL if v < res.val}
    st = _stack_vals(S)
    if st:
        return {v for v in ALL if v < min(st)}
    return set(ALL)


def _color(S, n):
    res = S.get('res')
    if res is not None and n.val == res.val:
        return 'yellow'
    cur = S.get('root', S.get('now'))
    if cur is not None and n.val == cur.val:
        return 'blue'
    if n.val in _stack_vals(S):
        return 'purple'
    if n.val in _returned(S):
        return 'green'
    return None


def _out(S):
    got = sorted(_returned(S))
    if S.get('res') is not None and S['_line'] == 16:
        got.append(S['res'].val)
    return '已输出：' + ('`' + ' '.join(map(str, got)) + '`' if got else '（无）') + '　　中序遍历 = 从小到大'


def _w5(S, B, ret):
    if S.root is not None:
        return f'`root = {S.root.val}` 非空 → 入栈，继续往左走'
    return '左边走到头了：栈顶就是中序遍历的==第一个节点==，先停下来等 `next`'


def _w12(S, B, ret):
    if S.now is not None:
        return f'`now = {S.now.val}` 非空 → 入栈，继续往左'
    if S.res.right is None:
        return '`now` 为空，栈不变：新的栈顶就是下一个最小值'
    return '右子树的最左侧节点已入栈，停下来等下一个 `next`'


CONFIG = dict(
    num=173, title='二叉搜索树迭代器', difficulty='Medium', category='设计',
    author='yiduobo', technique='栈模拟中序遍历 · 走到最左就停下',
    tags=['面试经典150'],
    code='''
class BSTIterator(object):

    def __init__(self, root):
        self.stack = []
        while root:
            self.stack.append(root)
            root = root.left

    def next(self):
        res = self.stack.pop()
        now = res.right
        while now:
            self.stack.append(now)
            now = now.left

        return res.val

    def hasNext(self):
        if self.stack:
            return True

        return False
''',
    call='''it = BSTIterator(Tr([7, 3, 15, None, None, 9, 20]))
[it.next(), it.next(), it.hasNext(), it.next(), it.hasNext(), it.next(), it.hasNext(), it.next(), it.hasNext()]''',
    expect=[3, 7, True, 9, True, 15, True, 20, False],
    views=[
        dict(type='text', size=24, h=60,
             fn=lambda S: '操作：`next next hasNext next hasNext next hasNext next hasNext`'),
        dict(type='tree', var=lambda S: _ROOT, path=False, color=_color, h=330,
             label='BST（紫 = 在栈里，蓝 = 正在走，黄 = 本次返回，绿 = 已返回）'),
        dict(type='stack', var='self.stack', fmt=lambda n: str(n.val), font=30, h=130,
             label='stack（栈顶 = 下一个最小值）'),
        dict(type='text', size=28, fn=_out),
    ],
    watch=[('res', lambda S: S['res'].val, 'yellow'), ('now', lambda S: S['now'].val if S['now'] else None, 'blue'),
           ('栈大小', lambda S: len(S['self.stack']), 'purple')],
    captions={
        'self.stack = []': '栈只存==当前节点到最左侧的一条链==，规模最多是树高 `h`',
        5: _w5,
        'self.stack.append(root)': '`{root.val}` 入栈',
        'root = root.left': lambda S, B, r: (f'往左子树走：`root` → `{S.root.val}`' if S.root else f'`{B.root.val}` 没有左孩子'),
        'res = self.stack.pop()': '`next()`：弹出栈顶 `{res.val}`——它就是还没访问的节点里==最小的==',
        'now = res.right': lambda S, B, r: (f'回溯：进入 `{S.res.val}` 的右子树，从 `{S.now.val}` 开始找最左侧节点' if S.now
                                            else f'`{S.res.val}` 没有右子树 → 不用入栈'),
        12: _w12,
        'self.stack.append(now)': '沿途节点 `{now.val}` 入栈',
        'now = now.left': lambda S, B, r: (f'往左走：`now` → `{S.now.val}`' if S.now else f'`{B.now.val}` 没有左孩子'),
        'return res.val': lambda S, B, r: (f'返回 =={r}==；每个节点只入栈、出栈各一次 → 均摊 `O(1)`' if r in (3, 7)
                                           else f'返回 =={r}=='),
        'if self.stack': lambda S, B, r: (f'`hasNext()`：栈里还有 `{len(S.self.stack)}` 个节点 → 还有下一个' if S.self.stack
                                          else '`hasNext()`：栈空了 → 所有节点都访问完了'),
        'return True': '返回 `True`',
        'return False': '返回 `False`',
    },
    max_steps=70,
    cards=dict(
        one_liner='栈里只放“左链”：走到最左就停，next 时弹出再进右子树',
        complexity='`next` 均摊 `O(1)`，`hasNext` `O(1)`，空间 `O(h)`',
        problem=['实现 BST 的迭代器：`next()` 按==中序==（从小到大）返回下一个数，`hasNext()` 判断是否还有',
                 '要求 `next`/`hasNext` 均摊 `O(1)`，额外空间 `O(h)`（`h` 为树高）',
                 '示例：`[7,3,15,null,null,9,20]` → `3, 7, 9, 15, 20`'],
        quote='我们在这里==找到最左侧节点时就可以先停下来，等待next指令==。遇到next指令后弹出栈顶节点，然后执行回溯操作，即在栈顶节点的右子树中寻找最左侧节点并将沿途节点入栈。',
        quote_src='—— yiduobo 题解原文',
        idea=['初始化就把所有节点存下来要 `O(n)` 空间，不符合要求',
              '改成模拟递归：节点入栈、往左走；到最左侧就停，栈顶即最小值',
              '`next` 弹出栈顶，再把它右子树的左链入栈'],
        summary=['`next` 均摊 `O(1)`：每个节点只入栈一次、出栈一次；空间 `O(h)`',
                 '原文说“前序遍历”，代码实际做的是==中序遍历==（左 → 根 → 右），BST 的中序就是升序',
                 '易错：弹出节点后要处理它的==右子树==的整条左链，而不只是右孩子',
                 '原文为 Python 2 写法：只删去了文档字符串和 LeetCode 模板注释，逻辑未改'],
    ),
)
