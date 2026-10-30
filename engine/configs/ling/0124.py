def _cap_l(S, B, ret):
    kid = S.get('node')
    return f'先求 `{B["node"].val}` 左子树的==最大链和==' + ('（左边是空的）' if kid is None else f'（从 `{kid.val}` 往下）')


def _cap_r(S, B, ret):
    kid = S.get('node')
    return (f'左子树最大链和 `sum_l = {B["sum_l"]}`；再求右子树' + ('（空的）' if kid is None else f'（从 `{kid.val}` 往下）'))


def _cap_ans(S, B, ret):
    l, r, v = S['sum_l'], S['sum_r'], S['node'].val
    tot = l + v + r
    old = B['ans']
    old_s = '-inf' if old == float('-inf') else str(old)
    up = '==更新==' if S['ans'] != old else '不变'
    return f'假设路径在 `{v}` ==拐弯==：左链 + 自己 + 右链 = `{l} + {v} + {r} = {tot}`，`ans = max({old_s}, {tot})` → {up} `{S["ans"]}`'


def _cap_ret(S, B, ret):
    l, r, v = S['sum_l'], S['sum_r'], S['node'].val
    x = max(l, r) + v
    head = f'往上只能带==一条==链：`max({l}, {r}) + {v} = {x}`'
    if x < 0:
        return head + '，==是负数，接上反而更小== → 返回 `0`（不要这条链）'
    return head + f'，返回 `{ret}`'


CONFIG = dict(
    num=124, title='二叉树中的最大路径和', difficulty='Hard', category='二叉树',
    author='灵茶山艾府', technique='树形 DP：返回最大链和，在拐点更新答案',
    code='''
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        ans = -inf

        def dfs(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0  # 没有节点，和为 0
            sum_l = dfs(node.left)  # 左子树最大链和
            sum_r = dfs(node.right)  # 右子树最大链和
            nonlocal ans
            ans = max(ans, sum_l + node.val + sum_r)  # 左链 + node + 右链 = 路径
            return max(max(sum_l, sum_r) + node.val, 0)  # 当前子树最大链和（注意这里和 0 取最大值了）

        dfs(root)
        return ans
''',
    call='Solution().maxPathSum(Tr([-10,9,20,None,None,15,-7]))',
    expect=35,
    views=[
        dict(type='text', fn=lambda S: (f"拐弯路径 = `sum_l + node.val + sum_r` = `{S['sum_l']} + {S['node'].val} + {S['sum_r']}` = =={S['sum_l'] + S['node'].val + S['sum_r']}=="
                                        if S.get('node') is not None and 'sum_r' in S and 'sum_l' in S else '')),
        dict(type='tree', pointers={'node': 'blue'}, h=400),
        dict(type='calls', h=180),
    ],
    watch=[('sum_l', 'sum_l', 'cyan'), ('sum_r', 'sum_r', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'ans = -inf': '`ans = -inf`：节点值可能全是负数，不能初始化成 0',
        'return 0': '空节点：没有链，链和为 `0`',
        'sum_l = dfs': _cap_l,
        'sum_r = dfs': _cap_r,
        'ans = max(': _cap_ans,
        'return max(max(': _cap_ret,
        'dfs(root)': '从根开始 DFS：每个节点都当一次「拐点」',
        'return ans': '所有拐点里最大的路径和：返回 =={ret}==',
    },
    skip=['if node is None'],
    max_steps=60,
    cards=dict(
        one_liner='dfs 返回往下的最大链和，在每个节点「拐弯」拼出路径更新答案',
        complexity='时间 `O(n)`，空间 `O(h)`（h 为树高）',
        problem=['路径：沿着边走、每个节点最多一次、==至少一个节点==，不一定经过根',
                 '求所有路径中节点值之和的最大值',
                 '示例：`root = [-10,9,20,null,null,15,-7]` → `35`（`15→20`）'],
        quote='==链==：从下面的某个节点到当前节点的路径，把链的节点值之和作为 dfs 的返回值，如果是负数则返回 0。==直径==：由两条（或者一条）链拼成的路径，假设直径在这里「拐弯」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(node)` 返回往下的==最大链和==；负数就返回 0，即不要这条链（同 53 题）',
              '在 `node` 拐弯：`sum_l + node.val + sum_r` 是一条完整路径，更新 `ans`',
              '⚠ dfs 返回的是==链==的和，不是==路径==（直径）的和'],
        summary=['时间 `O(n)`，空间 `O(h)` 的递归栈',
                 '易错：`ans` 初始化为 `-inf`；全是负数时答案就是最大的那个节点值',
                 '易错：往上返回时只能选一条链 `max(sum_l, sum_r)`，不能两边都带',
                 '同一套「直径 DP」：543 二叉树的直径、2246 相邻字符不同的最长路径'],
    ),
)
