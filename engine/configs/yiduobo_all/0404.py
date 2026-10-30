ADD = set()


def _walk(root):
    out, st, seen = [], [root], set()
    while st:
        n = st.pop()
        if n is None or n._uid in seen:
            continue
        seen.add(n._uid)
        out.append(n)
        st += [n.left, n.right]
    return out


def mark(fn, add=False):
    def cap(S, B, ret):
        if add:
            ADD.add(S.now._uid)
        for n in _walk(S.get('self.tree')):
            n._lf = n._uid in ADD
        return fn(S, B, ret) if callable(fn) else fn
    return cap


CONFIG = dict(
    num=404, title='左叶子之和', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='dfs · 带「是否左孩子」标记',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def sumOfLeftLeaves(self, root):

        return self.dfs(root, False)

    def dfs(self, now, left_flag):
        if not now:
            return 0

        if not now.left and not now.right:
            if left_flag:
                return now.val
            else:
                return 0

        else:
            return self.dfs(now.left, True) + self.dfs(now.right, False)
''',
    call='''s = Solution()
s.tree = Tr([3,9,20,None,None,15,7])
s.sumOfLeftLeaves(s.tree)''',
    expect=24,
    views=[
        dict(type='tree', var='self.tree', label='二叉树（蓝 = now，绿 = 已被累加的左叶子）', pointers={'now': 'blue'}, h=270,
             color=lambda S, n: 'green' if getattr(n, '_lf', False) else None),
        dict(type='text', fn=lambda S: f"`left_flag = {S['_inner'].get('left_flag')}`：{'now 是父节点的左孩子' if S['_inner'].get('left_flag') else 'now 是右孩子（或根）'}" if 'now' in S['_inner'] else '', size=26, h=56),
        dict(type='calls', h=230),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue'), ('left_flag', lambda S: S['_inner'].get('left_flag'), 'yellow')],
    captions={
        4: mark('从根出发：根没有父亲，==不是左孩子==，所以 `left_flag = False`'),
        7: mark(lambda S, B, r: ('`now` 为空 → 返回 `0`' if S.now is None else f'节点 `{S.now.val}` 非空，继续判断')),
        8: mark('空节点，返回 `0`'),
        10: mark(lambda S, B, r: (f'`{S.now.val}` 没有孩子 → 是叶子，还要看它是不是左孩子' if (not S.now.left and not S.now.right) else f'`{S.now.val}` 有孩子 → 不是叶子，分别递归左右孩子')),
        11: mark(lambda S, B, r: (f'`left_flag = True`：`{S.now.val}` 是左孩子 → ==左叶子== ' if S.left_flag else f'`left_flag = False`：`{S.now.val}` 是右孩子 → 不是左叶子')),
        12: mark(lambda S, B, r: f'左叶子！返回它的值 `{S.now.val}`', add=True),
        14: mark('右叶子，不算 → 返回 `0`'),
        17: mark(lambda S, B, r: f'`{B.now.val}` 有孩子：左孩子带标记 `True`、右孩子带标记 `False`，两边结果相加后返回'),
    },
    cards=dict(
        one_liner='dfs 时顺带传一个标记：我是不是左孩子',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['给定二叉树的根节点，求所有==左叶子==的值之和',
                 '左叶子 = 是父亲的左孩子，且自己没有孩子',
                 '本视频：`root = [3,9,20,null,null,15,7]` → `9 + 15 = 24`'],
        quote='一趟dfs，在过程中标记当前节点是否为其父亲节点的左孩子。其没有孩子节点，且左孩子标记为True，说明其为左叶子节点，那么返回当前节点的值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now, left_flag)`：往左走传 `True`，往右走传 `False`',
              '空节点返回 `0`；叶子看标记：左叶子返回自己的值，右叶子返回 `0`',
              '有孩子：返回左右孩子结果之和'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '根节点传 `False`：根即使是叶子也不算左叶子',
                 '对比灵神：灵神站在父节点看「左儿子是不是叶子」；yiduobo 站在孩子自己看「我是左孩子吗」',
                 '原文代码无需改动，已直接在 Python 3 运行'],
    ),
)
