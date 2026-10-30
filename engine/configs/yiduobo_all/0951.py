def nv(x):
    return '空' if x is None else str(x.val)


def cap_head(S, B, ret):
    a, b = S.root1, S.root2
    if a is None and b is None:
        return '两边都是空树 → 一致，返回 `True`'
    if a is None or b is None:
        return f'一边是空、一边是 `{nv(a) if b is None else nv(b)}` → 形状对不上，返回 `False`'
    return f'比较 `check({a.val}, {b.val})`：两棵子树能否通过翻转变成一样'


CONFIG = dict(
    num=951, title='翻转等价二叉树', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='递归 · 不翻转 / 翻转两种配对',
    tags=['二叉树', '递归'],
    code='''
class Solution(object):
    def flipEquiv(self, root1, root2):

        return self.check(root1, root2)
    
    def check(self, root1, root2):
        if not root1:
            if not root2:
                return True
            return False
        elif not root2:
            return False
        
        if root1.val != root2.val:
            return False

        if self.check(root1.left, root2.left) and self.check(root1.right, root2.right):
            return True
        
        if self.check(root1.left, root2.right) and self.check(root1.right, root2.left):
            return True
    
        return False
''',
    call='''s = Solution()
s.a = Tr([1,2,3,4,5])
s.b = Tr([1,3,2,None,None,5,4])
s.flipEquiv(s.a, s.b)''',
    expect=True,
    views=[
        dict(type='tree', var='self.a', label='root1 树（蓝 = root1）', pointers={'root1': 'blue'}, h=210),
        dict(type='tree', var='self.b', label='root2 树（粉 = root2）', pointers={'root2': 'pink'}, h=210),
        dict(type='calls', h=270, hide=('self',)),
    ],
    watch=[('root1', lambda S: nv(S['_inner'].get('root1')), 'blue'), ('root2', lambda S: nv(S['_inner'].get('root2')), 'pink')],
    captions={
        4: '`f[root1, root2]`：能否通过翻转某些节点的左右子树，让两棵树完全一致',
        7: cap_head,
        8: '`root1` 是空：`root2` 也是空才一致',
        9: '两边都空 → 一致，`True`',
        10: '`root1` 是空而 `root2` 不空 → 形状对不上，`False`',
        11: '`root1` 非空：`root2` 若是空 → 形状对不上',
        12: '`root1` 非空而 `root2` 是空 → `False`',
        14: lambda S, B, r: (f'根的值不同 `{S.root1.val} ≠ {S.root2.val}` → 不可能一致' if S.root1.val != S.root2.val
                             else f'根的值相同 `{S.root1.val} = {S.root2.val}` → 再看孩子能否配上'),
        15: '值不同：无论怎么翻转都不可能一致 → `False`',
        17: '==不翻转==：左配左、右配右，`f[left1,left2]` 且 `f[right1,right2]` 都为真才行',
        18: '`{root1.val}`：不翻转的配对成立 → ==这两棵子树翻转等价==，`True`',
        20: '==翻转 root1==（两树同时翻转等于没翻，只翻一边）：左配右、右配左，两个都要为真',
        21: '`{root1.val}`：翻转后的配对成立 → ==翻转等价==，`True`',
        23: '`{root1.val}` 不翻转、翻转两种配对都失败 → `False`',
    },
    cards=dict(
        one_liner='把「整棵树能否翻转一致」拆成子树的同一个问题：配对分翻转或不翻转',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈）',
        problem=['翻转操作：选任意节点，交换它的左右子树',
                 '给两棵二叉树 `root1`、`root2`，判断能否经若干次翻转让两棵树==完全一致==',
                 '本视频：`[1,2,3,4,5]` 与 `[1,3,2,null,null,5,4]` → `True`'],
        quote='若以left1和left2满足f[left1, left2] = true，同时right1和right2满足f[right1, right2] = true，那么就有f[root1, root2]为true。另外，我们也可以对root1和root2进行翻转操作……',
        quote_src='—— yiduobo 题解原文',
        idea=['设 `f[root1, root2]` 表示两树能否翻转一致，先比根的值，不等直接 `False`',
              '不翻转：左配左、右配右；翻转：左配右、右配左，两种配对任何一种成立即可',
              '两树同时翻转等于没翻转，所以只需考虑翻转 `root1` 一边'],
        summary=['时间 `O(n)`：每对节点最多比较常数次；空间 `O(h)`',
                 '先处理空节点：两个都空 `True`，只有一个空 `False`，再比值',
                 '易错：节点值互不相同，所以值相等时才会进入配对；两种配对要用 `and` 连接',
                 '原文为 Python 2 风格（`class Solution(object)`），代码没有改动'],
    ),
)
