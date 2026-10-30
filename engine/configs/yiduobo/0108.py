class Ptr(str):
    """带标签的“表达式指针”：名字照常显示，取值时调用函数（这里只读当前这一层的局部变量）"""
    def __new__(cls, label, fn):
        o = str.__new__(cls, label)
        o.fn = fn
        return o

    def __call__(self, S):
        return self.fn(S)


def nv(x):
    return '空' if x is None else str(x.val)


def cap_eq(S, B, ret):
    if S.left == S.right:
        return f'`left == right == {S.left}`：==只有一个节点==，它自己就是要求的树'
    return f'区间 `[{S.left}, {S.right}]` 不止一个节点'


def cap_two(S, B, ret):
    if S.left == S.right - 1:
        return f'`[{S.left}, {S.right}]` 恰好==两个节点==：一个作根，另一个作孩子'
    return f'区间 `[{S.left}, {S.right}]` 超过两个节点 → 取正中间作根'


def cap_mid(S, B, ret):
    return f'`mid = ({S.left} + {S.right}) // 2 = {S.mid}`：正中间的 `{S.nums[S.mid]}` 作根'


CONFIG = dict(
    num=108, title='将有序数组转换为二叉搜索树', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='递归 · 一个 / 两个 / 多个节点分类讨论',
    code='''
class Solution(object):
    def sortedArrayToBST(self, nums):
        if not nums:
            return None

        return self.build(0, len(nums) - 1, nums)

    def build(self, left, right, nums):
        if left == right:
            return TreeNode(nums[left])

        if left == right - 1:
            root = TreeNode(nums[left])
            root.right = TreeNode(nums[right])
            return root

        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = self.build(left, mid - 1, nums)
        root.right = self.build(mid + 1, right, nums)
        return root
''',
    call='Solution().sortedArrayToBST([-10,-3,0,5,9,12])',
    expect=[0, -10, 9, None, -3, 5, 12],
    result_fn=tree_list,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前区间 [left, right]）',
             pointers={Ptr('mid', lambda S: S['_inner'].get('mid')): 'orange'},
             window=('left', 'right'), cell=72,
             dim=lambda S, i, v: 'left' in S and not (S['left'] <= i <= S['right'])),
        dict(type='tree', label='已建好的节点', h=270,
             pointers={Ptr('root', lambda S: S['_inner'].get('root')): 'blue'}),
        dict(type='calls', h=190),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', lambda S: S['_inner'].get('mid'), 'orange')],
    captions={
        'if not nums': '`nums` 非空',
        'return self.build': '用闭区间 `[0, len(nums) - 1]` 调用 `build`',
        'if left == right:': cap_eq,
        'return TreeNode(nums[left])': lambda S, B, ret: f'新建叶子 `{ret.val}` 返回',
        'if left == right - 1': cap_two,
        'root = TreeNode(nums[left])': lambda S, B, ret: f'两个节点的情况：左边的 `{S.root.val}` 作根……',
        'root.right = TreeNode(nums[right])': lambda S, B, ret: f'……右边的 `{S.root.right.val}` 作它的==右孩子==（作左孩子也可以）',
        'mid = (left + right)': cap_mid,
        'root = TreeNode(nums[mid])': lambda S, B, ret: f'新建根节点 `{S.root.val}`',
        'root.left = self.build': lambda S, B, ret: f'左边区间 `[{S.left}, {S.right}]` 递归建左子树',
        'root.right = self.build': lambda S, B, ret: f'左子树接好了；右边区间 `[{S.left}, {S.right}]` 递归建右子树',
        'return root': lambda S, B, ret: f'以 `{ret.val}` 为根的子树建好，返回',
    },
    cards=dict(
        one_liner='一个节点直接返回，两个节点一根一孩子，更多就取中间递归',
        complexity='时间 `O(n)`，空间 `O(log n)`（递归栈，不计答案）',
        problem=['`nums` 严格递增，把它转换成一棵==平衡==二叉搜索树',
                 '示例：`[-10,-3,0,5,9]` → `[0,-3,9,-10,null,5]`（答案不唯一）',
                 '本视频用 `[-10,-3,0,5,9,12]`，三种情况都会出现'],
        quote='对于一个节点的情况，这个节点就是要求的树。对于两个节点的情况，其中一个作为根，另一个作为左孩子或者右孩子都可以。对于超过两个节点的情况，==取正中间的节点作为根==……',
        quote_src='—— yiduobo 题解',
        idea=['`build(left, right, nums)` 处理闭区间，==只传下标，不切片==',
              '先把小规模情况（1 个、2 个节点）单独处理掉',
              '超过两个节点：`mid` 作根，`[left, mid-1]`、`[mid+1, right]` 递归'],
        result='运行结束，返回 `[0,-10,9,null,-3,5,12]`：两边高度差不超过 1 ✓',
        summary=['时间 `O(n)`：每个数建一个节点；只传下标，没有切片开销',
                 '两个节点时让右边的数当右孩子，所以 `-10` 下面挂 `-3`',
                 '易错：闭区间写法里左右子树是 `mid - 1` 和 `mid + 1`',
                 '原文为 Python 2：整除 `/` 已改为 `//`；删去 docstring'],
    ),
)
