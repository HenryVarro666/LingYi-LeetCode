CONFIG = dict(
    num=1305, title='两棵二叉搜索树中的所有元素', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='中序遍历 + 二路归并', tags=[],
    code='''
class Solution(object):
    def getAllElements(self, root1, root2):

        arr1 = []
        arr2 = []
        self.dfs(root1, arr1)
        self.dfs(root2, arr2)
        res = []
        i = 0
        j = 0
        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                res.append(arr1[i])
                i += 1
            else:
                res.append(arr2[j])
                j += 1

        if i < len(arr1):
            res.extend(arr1[i:])
        else:
            res.extend(arr2[j:])

        return res

    def dfs(self, now, arr):
        if not now:
            return
        self.dfs(now.left, arr)
        arr.append(now.val)
        self.dfs(now.right, arr)
''',
    call='Solution().getAllElements(Tr([2,1,4]), Tr([1,0,3]))',
    expect=[0, 1, 1, 2, 3, 4],
    views=[
        dict(type='tree', var='root1', label='root1', pointers={'now': 'blue'}, h=190),
        dict(type='tree', var='root2', label='root2', pointers={'now': 'blue'}, h=190),
        dict(type='array', var='arr1', label='arr1（root1 的中序）', pointers={'i': 'blue'}, cell=64, h=90),
        dict(type='array', var='arr2', label='arr2（root2 的中序）', pointers={'j': 'pink'}, cell=64, h=90),
        dict(type='array', var='res', label='res（归并结果）', cell=64, h=90),
        dict(type='calls', h=150, hide=('arr',)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'arr1 = []': '`arr1` 存 root1 的中序遍历',
        'arr2 = []': '`arr2` 存 root2 的中序遍历',
        'self.dfs(root1': '对 root1 做中序遍历：BST 的中序天然升序',
        'self.dfs(root2': '对 root2 同样做中序遍历',
        'self.dfs(now.left': '先递归左子树（左-根-右）',
        'arr.append': '左边都访问完了 → 轮到根：`{now.val}` 追加到数组，现在 `{arr}`',
        'self.dfs(now.right': '最后递归右子树',
        'i = 0': '`i` 指向 arr1 的队头',
        'j = 0': '`j` 指向 arr2 的队头',
        'res = []': '两个升序数组，准备二路归并',
        'while i < len': lambda S, B, r: (f'`i = {S.i} < {len(S.arr1)}` 且 `j = {S.j} < {len(S.arr2)}`：两边都还有数 → 继续比' if S.i < len(S.arr1) and S.j < len(S.arr2) else '有一边用完了 → 结束归并'),
        'if arr1[i] < arr2[j]': '比较两个队头 `{arr1[i]}` 和 `{arr2[j]}`：' + '{"arr1 的更小" if arr1[i] < arr2[j] else "arr2 的不更大"}',
        'res.append(arr1[i])': '小的先放：`{arr1[i]}` 进 `res` → `{res}`',
        'i += 1': 'arr1 的指针后移：`i = {i}`',
        'res.append(arr2[j])': '小的先放：`{arr2[j]}` 进 `res` → `{res}`',
        'j += 1': 'arr2 的指针后移：`j = {j}`',
        'if i < len(arr1)': lambda S, B, r: ('arr1 还有剩余 → 整段接到后面' if S.i < len(S.arr1) else 'arr1 已用完 → 剩下的只可能在 arr2'),
        'res.extend(arr1[i:])': '剩下的本来就升序，直接接上 → `{res}`',
        'res.extend(arr2[j:])': '剩下的本来就升序，直接接上 → `{res}`',
        'return res': '合并完成：`{ret}`',
    },
    skip=['if not now:'],
    cards=dict(
        one_liner='BST 中序遍历天然升序，两个升序数组二路归并',
        complexity='时间 `O(m+n)`，空间 `O(m+n)`',
        problem=['给两棵二叉搜索树 `root1`、`root2`', '返回两棵树中==所有整数按升序排序==的列表',
                 '本视频：`[2,1,4]` 和 `[1,0,3]` → `[0,1,1,2,3,4]`'],
        quote='二叉搜索树的中序遍历是天然按升序排列的，那么一个自然的想法就是分别对两棵树执行中序遍历，就可以得到两个升序的数组。接下来对这两个数组执行二路归并即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先各自中序遍历：左 - 根 - 右，得到两个升序数组', '再用两个指针 `i`、`j` 比较队头，小的先进 `res`', '一边用完后，另一边剩下的直接接上'],
        summary=['时间 `O(m+n)`，空间 `O(m+n)`',
                 '相等时取 `arr2` 的，不影响结果',
                 '循环结束后只有一个数组有剩余，`extend` 切片接上即可',
                 '原文为 Python 2 风格，代码无需改动（只去掉了行尾空白）'],
    ),
)
