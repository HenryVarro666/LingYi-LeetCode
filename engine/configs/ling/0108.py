ORIG = [-10, -3, 0, 5, 9]   # 示例输入；切片里的数互不相同，可以反查它在原数组里的位置


def off(S):
    nums = S.get('nums')
    return ORIG.index(nums[0]) if nums else None


def win_r(S):
    o = off(S)
    return None if o is None else o + len(S['nums']) - 1


def nv(x):
    return '空' if x is None else str(x.val)


def cap_if(S, B, ret):
    if not S.nums:
        return '`nums` 是空数组 → 递归边界'
    return f'`nums = {S.nums}` 非空'


def cap_m(S, B, ret):
    n = len(S.nums)
    tail = '（偶数长度取正中间==右边==那个）' if n % 2 == 0 else ''
    return f'`m = {n} // 2 = {S.m}`：正中间的 `{S.nums[S.m]}` 当根{tail}'


def cap_l(S, B, ret):
    if not S.nums:
        return '左边没有数了（`nums[:m] = []`）→ 左儿子是空节点'
    return f'左边 `nums[:m] = {S.nums}` 转成平衡 BST，作为左儿子：==和原问题相似的子问题=='


def cap_r(S, B, ret):
    if not S.nums:
        return f'左儿子 = {nv(B.left)}；右边也没有数了（`nums[m + 1:] = []`）→ 右儿子为空'
    return f'左子树建好（根 {nv(B.left)}）；右边 `nums[m + 1:] = {S.nums}` 递归建右子树'


def cap_ret(S, B, ret):
    return f'新建节点 `{ret.val}`：左儿子 {nv(S.left)}，右儿子 {nv(S.right)}，返回给上一层'


CONFIG = dict(
    num=108, title='将有序数组转换为二叉搜索树', difficulty='Easy', category='二叉树',
    author='灵茶山艾府', technique='递归 · 取中间为根（切片写法）',
    code='''
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        m = len(nums) // 2
        left = self.sortedArrayToBST(nums[:m])
        right = self.sortedArrayToBST(nums[m + 1:])
        return TreeNode(nums[m], left, right)
''',
    call='Solution().sortedArrayToBST([-10,-3,0,5,9])',
    expect=[0, -3, 9, -10, None, 5],
    result_fn=tree_list,
    views=[
        dict(type='array', var=lambda S: ORIG, label='nums（框 = 当前这一层的切片，橙 = 正中间）',
             window=(off, win_r), cell=80,
             color=lambda S, i, v: 'orange' if (off(S) is not None and i == off(S) + len(S['nums']) // 2) else None,
             dim=lambda S, i, v: off(S) is None or not (off(S) <= i <= win_r(S))),
        dict(type='tree', label='已建好的节点（子树自底向上拼起来）', h=290),
        dict(type='calls', h=200),
    ],
    watch=[('nums', 'nums'), ('m', lambda S: S['_inner'].get('m'), 'orange')],
    captions={
        'if not nums': cap_if,
        'return None': '空数组 → 返回 `None`（空节点）',
        'm = len(nums)': cap_m,
        'left = self': cap_l,
        'right = self': cap_r,
        'return TreeNode': cap_ret,
    },
    cards=dict(
        one_liner='正中间的数当根，左右两半递归建左右子树',
        complexity='时间 `O(n log n)`（切片复制），空间 `O(n)`',
        problem=['`nums` 严格递增，把它转换成一棵==平衡==二叉搜索树',
                 '示例：`[-10,-3,0,5,9]` → `[0,-3,9,-10,null,5]`',
                 '答案不唯一，`[0,-10,5,null,-3,null,9]` 也对'],
        quote='答案由三部分组成：根节点 nums[2]=0；把左边的 [-10,-3] 转换成平衡二叉搜索树，作为答案的左儿子；把右边的 [5,9] 转换成平衡二叉搜索树，作为答案的右儿子。',
        quote_src='—— 灵茶山艾府题解',
        idea=['根取正中间：左右两半个数差不超过 1 → ==平衡==',
              '左半边都比根小、右半边都比根大 → ==二叉搜索树==',
              '左右两半是==和原问题相似的子问题==，递归边界是空数组'],
        result='运行结束，返回 `[0,-3,9,-10,null,5]`：每个节点都是它那段切片的正中间',
        summary=['切片写法时间 `O(n log n)`：每层复制 `O(n)`，共 `O(log n)` 层',
                 '灵神写法二：`dfs(left, right)` 只传下标，避免切片，时间 `O(n)`',
                 '`n` 为偶数时取 `n // 2`（正中间右边），取左边那个也对',
                 '易错：右半边是 `nums[m + 1:]`，别把根 `nums[m]` 再放进去'],
    ),
)
