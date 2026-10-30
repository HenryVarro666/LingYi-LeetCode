def _while(S, B, r):
    now = S.now
    if now is None:
        return '`now` 走到空节点：树里==没有== `val`，循环结束'
    if now.val == S.val:
        return f'`now.val = {now.val}` 等于 `val` → ==找到了==，循环结束'
    return f'`now.val = {now.val}` ≠ `val = {S.val}`，继续往下找'


def _cmp(S, B, r):
    v = S.now.val
    if v < S.val:
        return f'`{v} < {S.val}`：左子树全都比 `{v}` 小，==不可能有 {S.val}== → 去右子树'
    return f'`{v} > {S.val}`：右子树全都比 `{v}` 大，==不可能有 {S.val}== → 去左子树'


def _info(S):
    if 'val' not in S:
        return '二叉搜索树：左子树 < 根 < 右子树'
    return f"查找 `val = {S['val']}`：每一步只走一边，另一边整棵子树被排除"


CONFIG = dict(
    num=700, title='二叉搜索树中的搜索', difficulty='Easy', category='二叉树与回溯',
    author='yiduobo', technique='BST 迭代查找',
    tags=['labuladong', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def searchBST(self, root, val):

        now = root
        while now and now.val != val:
            if now.val < val:
                now = now.right
            else:
                now = now.left

        return now
''',
    setup='root = Tr([8,4,12,2,6,10,14,1,3])',
    call='''a = Solution().searchBST(root, 3)
b = Solution().searchBST(root, 11)
(tree_list(a), b)''',
    expect=([3], None),
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='tree', label='BST（蓝 = now，绿 = 目标值所在节点）', pointers={'now': 'blue'}, path=False, h=470,
             color=lambda S, node: 'green' if 'val' in S and node.val == S['val'] else None),
    ],
    watch=[('val', 'val', 'green'), ('now.val', lambda S: S['now'].val if S.get('now') else None, 'blue')],
    captions={
        'now = root': '从根节点出发：`now = {now.val}`，要找 `val = {val}`',
        'while now and now.val != val': _while,
        'if now.val < val': _cmp,
        'now = now.right': lambda S, B, r: f'`now` → 右儿子 ' + (f'`{S.now.val}`' if S.now else '==空=='),
        'now = now.left': lambda S, B, r: f'`now` → 左儿子 ' + (f'`{S.now.val}`' if S.now else '==空=='),
        'return now': lambda S, B, r: (f'返回节点 `{r.val}`（以它为根的子树）' if r else '返回 `None`：没找到'),
    },
    cards=dict(
        one_liner='比根小往左、比根大往右，每步排除一整棵子树',
        complexity='时间 `O(h)`（h 为树高），空间 `O(1)`',
        problem=['给你二叉搜索树的根 `root` 和整数 `val`',
                 '找到值等于 `val` 的节点，返回==以它为根的子树==；不存在返回 `null`',
                 '本视频：在 `[8,4,12,2,6,10,14,1,3]` 里先找 `3`，再找 `11`'],
        quote='若now.val小于val，说明now的左子树中所有的节点的值都小于val，因此我们需要在now的右子树now.right中继续查找',
        quote_src='—— yiduobo 题解原文',
        idea=['`now.val == val`：`now` 就是答案',
              '`now.val < val`：左子树更小，==只能在右边==；反之只能在左边',
              '走到空节点还没找到，说明不存在，循环自然结束返回 `None`'],
        summary=['时间 `O(h)`：平衡时 `O(log n)`，退化成链时 `O(n)`；迭代写法空间 `O(1)`',
                 '循环条件 `now and now.val != val`：==先判空再取 val==，顺序不能反',
                 '找到和找不到都统一 `return now`，不用分开写',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未改动'],
    ),
)
