def _text(S):
    r = S.get('root')
    if r is None:
        return ''
    ok = r.val == r.left.val + r.right.val
    return (f"`root.val = {r.val}`，`root.left.val + root.right.val = {r.left.val} + {r.right.val} = {r.left.val + r.right.val}`"
            f" → {'==相等==' if ok else '不相等'}")


CONFIG = dict(
    num=2236, title='判断根结点是否等于子结点之和', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='直接比较三个节点',
    tags=['List.md'],
    code='''
class Solution(object):
    def checkTree(self, root):
        return root.val == root.left.val + root.right.val
''',
    call='''s = Solution()
a = s.checkTree(Tr([10, 4, 6]))
b = s.checkTree(Tr([5, 3, 1]))
(a, b)''',
    expect=(True, False),
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='tree', label='本次调用的树（孩子：绿 = 和等于 root，红 = 不等）', h=420, pointers={'root': 'blue'}, path=False,
             color=lambda S, nd: (('green' if S['root'].val == S['root'].left.val + S['root'].right.val else 'red')
                                  if 'root' in S and nd is not S['root'] else None)),
    ],
    watch=[('root.val', 'root.val', 'blue'), ('root.left.val', 'root.left.val'), ('root.right.val', 'root.right.val')],
    captions={
        'return root.val == root.left.val + root.right.val': lambda S, B, r: (
            f'示例{"一" if B.root.val == 10 else "二"}：`{B.root.val} == {B.root.left.val} + {B.root.right.val}` → 返回 `{r}`'
            + ('，==相等==' if r else '，不相等')),
    },
    cards=dict(
        result='两个示例分别返回 `True`、`False` ✓',
        one_liner='树的结构固定：直接比较 root.val 和两个孩子之和',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['二叉树==恰好 3 个节点==：根、左子节点、右子节点',
                 '如果根的值等于两个子节点值之和，返回 `true`，否则返回 `false`',
                 '示例 1：`root = [10,4,6]` → `true`（10 = 4 + 6）',
                 '示例 2：`root = [5,3,1]` → `false`（5 ≠ 3 + 1）',
                 '本视频把两个示例都跑一遍'],
        quote='由于==题目保证了树的结构与样例一致==，因此可以放心使用root.left和root.right来找到左右孩子，接下来判断root.val是否等于……就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目保证左右孩子都存在 → `root.left`、`root.right` 不会是 `None`',
              '一行表达式：`root.val == root.left.val + root.right.val`',
              '比较的结果本身就是布尔值，直接返回'],
        after=[dict(heading='为什么可以不判空？', lines=[
            '题目保证树只有根、左、右三个节点',
            '所以 `root.left`、`root.right` 一定存在，可以直接取 `.val`',
            '原文：「感觉跟上一题是一起来的」（2235. 两整数相加，同样是送分题）'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '比较结果本身就是布尔值，直接 `return` 即可',
                 '对比灵神：灵神还给出了 n 个节点时的递归扩展',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
