CONFIG = dict(
    num=99, title='恢复二叉搜索树', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='Morris 中序 + 找逆序对', tags=[],
    code='''
class Solution(object):
    def recoverTree(self, root):

        first = None
        second = None
        last = None
        now = root

        while now:
            if now.left:
                rightest = now.left
                while rightest.right and rightest.right != now:
                    rightest = rightest.right

                if rightest.right is None:
                    rightest.right = now
                    now = now.left
                else:
                    rightest.right = None
                    if last and last.val > now.val:
                        second = now
                        if first is None:
                            first = last
                    last = now
                    now = now.right
            else:
                if last and last.val > now.val:
                    second = now
                    if first is None:
                        first = last
                last = now
                now = now.right

        tmp = first.val
        first.val = second.val
        second.val = tmp

        return root
''',
    call='Solution().recoverTree(Tr([4,5,6,1,3,2]))',
    expect=[4, 2, 6, 1, 3, 5],
    result_fn=tree_list,
    views=[
        dict(type='tree', var='root', label='树（蓝 = now，粉 = last，黄 = first/second）',
             pointers={'now': 'blue', 'last': 'pink', 'rightest': 'cyan'}, h=380, path=False),
        dict(type='text', fn=lambda S: f"`first = {S['first'].val if S.get('first') else None}`，`second = {S['second'].val if S.get('second') else None}`" if 'first' in S else '', size=28, h=56),
    ],
    watch=[('now', 'now.val if now else None', 'blue'), ('last', 'last.val if last else None', 'pink'),
           ('first', 'first.val if first else None', 'yellow'), ('second', 'second.val if second else None', 'orange')],
    captions={
        'first = None': '`first`：第一处逆序里较大的那个（应该被换走的）',
        'second = None': '`second`：最后一处逆序里较小的那个',
        'last = None': '`last`：中序遍历时上一个访问的节点',
        'now = root': '`now` 从根出发，用 ==左子树最右节点== 的办法做 O(1) 空间中序遍历',
        'while now:': lambda S, B, r: ('`now` 不为空，继续遍历' if S.now else '遍历结束，两个错位节点已找到'),
        'if now.left:': lambda S, B, r: (f'`{S.now.val}` 有左子树 → 先找它左子树的最右节点' if S.now.left else f'`{S.now.val}` 没有左子树 → 直接访问它'),
        'rightest = now.left': '`rightest` 从左儿子 `{rightest.val}` 开始，一路向右',
        'while rightest.right': lambda S, B, r: ('`rightest.right` 存在且不是 `now` → 继续向右' if S.rightest.right and S.rightest.right != S.now else '到头了（或已指回 `now`）'),
        'rightest = rightest.right': '`rightest` 右移到 `{rightest.val}`',
        'if rightest.right is None': lambda S, B, r: ('第一次到这里：左子树还没遍历 → 建立线索' if S.rightest.right is None else '`rightest.right` 已经指回 `now` → 左子树遍历完了'),
        'rightest.right = now': '线索：让 `{rightest.val}` 的右指针指回 `{now.val}`，走完左子树能回来',
        'now = now.left': '进入左子树，`now = {now.val}`',
        'rightest.right = None': '左子树已访问完 → 拆掉线索，恢复原树',
        'if last and last.val > now.val': lambda S, B, r: (f'`last = {S.last.val} > now = {S.now.val}`：==中序出现逆序== ' if S.last and S.last.val > S.now.val else (f'`last = {S.last.val} < now = {S.now.val}`：升序正常' if S.last else '还没有上一个节点，不比较')),
        'second = now': '逆序的后者：`second = {now.val}`（每出现一次逆序就更新）',
        'if first is None': lambda S, B, r: ('这是第一次逆序 → 记下 `first`' if S.first is None else '`first` 已经记过了，不再改'),
        'first = last': '逆序的前者：`first = {last.val}`',
        'last = now': '访问完毕：`last = {now.val}`',
        'now = now.right': '去右边（或沿线索回到上层）：`now = {now.val if now else None}`',
        'tmp = first.val': '遍历完了：`first = {first.val}`，`second = {second.val}`，把两个值互换',
        'first.val = second.val': '`first` 改成 `second` 的值 `{first.val}`',
        'second.val = tmp': '`second` 改成原来 first 的值 `{second.val}` → 树恢复',
        'return root': '恢复后的树',
    },
    cards=dict(
        one_liner='BST 的中序应当升序，找到被交换的那两个逆序位置再换回来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二叉搜索树中==恰有两个节点的值被错误交换==', '不改变结构，恢复这棵树',
                 '本视频：`[4,5,6,1,3,2]`，中序 `1,5,3,4,2,6`，换回 `5` 和 `2`'],
        quote='于是，可以通过一次扫描，记录下两次逆序的位置，就能确定具体的m和n是多少了。',
        quote_src='—— yiduobo 题解原文',
        idea=['正常 BST 中序严格递增；交换两个值后会出现 ==1 或 2 处逆序==',
              '第一次逆序记 `first = last`，之后每次逆序都更新 `second = now`',
              '题目要求常数空间：用左子树最右节点做线索（Morris），不用递归和数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：相邻交换只有一处逆序，所以 `second` 每次都更新，`first` 只在第一次记',
                 '易错：`first`、`second` 是节点，最后交换的是它们的值',
                 'Morris 遍历会临时改 `right` 指针，必须拆掉线索，否则树里有环',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
