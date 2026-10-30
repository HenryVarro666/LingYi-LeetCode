def _cmp(side):
    def f(S, B, ret):
        n = B.now
        c = getattr(n, side)
        word = '左' if side == 'left' else '右'
        if c is None:
            return f'`{n.val}` 没有{word}孩子 → 无需检查'
        if c.val != n.val:
            return f'{word}孩子 `{c.val}` != 当前 `{n.val}` → ==值不一致，直接返回 False=='
        return f'{word}孩子 `{c.val}` == 当前 `{n.val}` → 值一致，还要继续检查它的子树'
    return f


CONFIG = dict(
    num=965, title='单值二叉树', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='DFS · 逐个比对孩子',
    tags=['灵神核心路线', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def isUnivalTree(self, root):
        return self.dfs(root)

    def dfs(self, now):
        if now.left:
            if now.left.val != now.val or (not self.dfs(now.left)):
                return False

        if now.right:
            if now.right.val != now.val or (not self.dfs(now.right)):
                return False

        return True
''',
    call='Solution().isUnivalTree(Tr([1,1,1,1,1,1,2]))',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: f"当前节点 `{S['now'].val}`，要求它的孩子都等于 `{S['now'].val}`" if 'now' in S else '单值树：所有节点的值都相同', size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=320),
        dict(type='calls', h=240),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') and S['_inner']['now'].val, 'blue')],
    captions={
        'return self.dfs(root)': '从根节点开始 DFS',
        'if now.left:': '`{now.val}` 有左孩子吗？{"有，去比较" if now.left else "没有，跳过"}',
        'if now.left.val': _cmp('left'),
        'if now.right:': '`{now.val}` 有右孩子吗？{"有，去比较" if now.right else "没有，跳过"}',
        'if now.right.val': _cmp('right'),
        'return False': '发现不一致 → ==返回 False==，上层的 `not self.dfs(...)` 为真，一路返回 False',
        'return True': '`{now.val}` 的孩子和子树都与它相同 → 返回 True',
    },
    cards=dict(
        one_liner='每个节点只和自己的孩子比较，传递下去就是全树相等',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['如果二叉树每个节点都具有相同的值，它就是==单值二叉树==',
                 '给定根节点 `root`，是单值树返回 `true`，否则返回 `false`',
                 '示例：`[1,1,1,1,1,1,2]` → 最右下角是 `2` → `false`'],
        quote='对于每个节点，若其存在孩子节点那么就判断孩子节点的值是否与该节点的值一致即可。',
        quote_src='—— yiduobo 题解',
        idea=['相等有传递性：父 == 子，子 == 孙，整棵树就都相等',
              '所以每个节点只看自己的左右孩子是否和自己相等',
              '孩子值相同还不够，还要递归检查孩子的子树；任何一处失败立刻返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(h)` 递归栈；遇到不一致会提前结束',
                 '易错：先判断孩子存在（`if now.left`），再取 `.val`，否则空指针',
                 '`or` 短路：孩子值不同时不会再递归下去',
                 '原文为 Python 2 风格，只删去了空行，代码可直接在 Python 3 运行'],
    ),
)
