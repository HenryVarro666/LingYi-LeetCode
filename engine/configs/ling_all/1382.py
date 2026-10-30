def _arr(S):
    a = S.get('nums')
    if isinstance(a, list):
        return a
    a = S.get('ans')
    return a if isinstance(a, list) else []


def _info(S):
    I = S['_inner']
    if 'left' in I and 'right' in I and 'nums' in S:
        l, r = I['left'], I['right']
        if l == r:
            return f'区间 `nums[{l}:{r}]` 为空 → 返回 `None`'
        m = I.get('m', (l + r) // 2)
        return f'区间 `nums[{l}:{r}]`，中点 `m = ({l} + {r}) // 2 = {m}` → 根 =={S["nums"][m]}=='
    if 'nums' in S:
        return '中序遍历得到递增数组 `nums`，接着把它转成平衡 BST'
    return '第一步：中序遍历，把节点值按 左 → 根 → 右 收集到 `ans`'


CONFIG = dict(
    num=1382, title='将二叉搜索树变平衡', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='中序遍历 + 有序数组建平衡 BST',
    tags=['链表树与回溯', '二叉树'],
    code='''
class Solution:
    # 94. 二叉树的中序遍历
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            dfs(node.left)        # 左
            ans.append(node.val)  # 根（这行代码移到前面就是前序，移到后面就是后序）
            dfs(node.right)       # 右

        ans = []
        dfs(root)
        return ans

    # 108. 将有序数组转换为二叉搜索树
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        # 把 nums[left:right] 转成平衡二叉搜索树
        def dfs(left: int, right: int) -> Optional[TreeNode]:
            if left == right:
                return None
            m = (left + right) // 2
            return TreeNode(nums[m], dfs(left, m), dfs(m + 1, right))

        return dfs(0, len(nums))

    def balanceBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        nums = self.inorderTraversal(root)
        return self.sortedArrayToBST(nums)
''',
    call='''s = Solution()
s.tree = Tr([1, None, 2, None, 3, None, 4])
tree_list(s.balanceBST(s.tree))''',
    expect=[3, 2, 4, 1],
    views=[
        dict(type='text', fn=_info, size=24, h=56),
        dict(type='tree', var='self.tree', label='原 BST（蓝 = node，退化成一条链）', pointers={'node': 'blue'}, path=False, h=230),
        dict(type='array', var=_arr, label='ans / nums（亮 = 当前区间 [left, right)，绿 = 中点 m）', pointers={'m': 'orange'}, cell=72, h=165,
             dim=lambda S, i, v: 'left' in S['_inner'] and 'right' in S['_inner'] and not (S['_inner']['left'] <= i < S['_inner']['right']),
             color=lambda S, i, v: 'green' if S['_inner'].get('m') == i else None),
        dict(type='calls', h=170),
    ],
    watch=[('node', lambda S: getattr(S['_inner'].get('node'), 'val', None), 'blue'), ('left', lambda S: S['_inner'].get('left'), 'blue'), ('right', lambda S: S['_inner'].get('right'), 'pink'), ('m', lambda S: S['_inner'].get('m'), 'orange')],
    captions={
        'nums = self.inorderTraversal': '第一步：中序遍历原树 → 因为是 BST，==遍历结果天然递增，无需排序==',
        'if node is None': '`node` {"是空节点 → 到头了，返回" if node is None else "不为空 → 先左、再根、后右"}',
        'dfs(node.left)': '先递归左子树（`node = {node.val}` 的左边都更小）',
        'ans.append(node.val)': '左子树走完，轮到根：`node.val = {node.val}` 加入 `ans` → `{ans}`',
        'dfs(node.right)': '最后递归右子树（比 `{node.val}` 大的都在这里）',
        'ans = []': '`ans` 收集遍历到的节点值',
        'dfs(root)': '从根开始中序遍历',
        'return ans': lambda S, B, r: f'中序遍历完成：`ans = {r}`，已经是递增数组',
        'return self.sortedArrayToBST': '第二步：用递增数组 `nums` 建平衡 BST',
        'if left == right': '`nums[{left}:{right}]` {"为空 → 递归边界，返回 None" if left == right else "还有元素 → 取中点当根"}',
        'm = (left + right) // 2': '取中点 `m = ({left} + {right}) // 2` = =={m}==：左右各分一半，==高度差不超过 1==',
        'return TreeNode': '`nums[{B.m}] = {nums[B.m]}` 做根：先建左半 `nums[{B.left}:{B.m}]`，再建右半 `nums[{B.m + 1}:{B.right}]`',
        'return dfs(0, len(nums))': '整个数组 `nums[0:{len(nums)}]` 建树：根是中点',
        'return None': '空区间没有节点 → `None`',
    },
    skip=['def ', 'return nums'],
    cards=dict(
        one_liner='BST 的中序遍历是有序数组；每次取中点当根，就是平衡树',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你一棵二叉搜索树，返回一棵节点值相同的==平衡== BST',
                 '平衡：每个节点两棵子树的高度差不超过 `1`',
                 '本视频：`[1,null,2,null,3,null,4]`（一条链）→ `[3,2,4,1]`'],
        quote='由于输入的是一棵二叉搜索树，节点值满足 左子树 < 根 < 右子树，所以通过一次中序遍历，把遍历到的节点值添加到一个数组中，可以直接得到一个递增数组，无需排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['拆成两道老题：94 中序遍历 + 108 有序数组转 BST',
              '中序遍历 BST ==天然有序==，不用再排序',
              '`nums[left:right]` 取中点 `m` 做根，左右两半各建子树，高度差 ≤ 1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '本视频用的是「写法二」：下标区间 `dfs(left, right)`，==避免切片复制==',
                 '写法一用 `nums[:m]` / `nums[m+1:]` 切片，每层复制 `O(n)`，总共 `O(n log n)`',
                 '易错：区间是左闭右开，`left == right` 才为空；右半从 `m + 1` 开始'],
    ),
)
