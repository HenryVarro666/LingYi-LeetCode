CONFIG = dict(
    num=1080, title='根到叶路径上的不足节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='递归 · 递归时减 limit',
    tags=['灵神题单', '链表树与回溯', '难度分 1805'],
    code='''
class Solution:
    def sufficientSubset(self, root: Optional[TreeNode], limit: int) -> Optional[TreeNode]:
        limit -= root.val
        if root.left is None and root.right is None:  # root 是叶子
            # 如果 limit > 0 说明从根到叶子的路径和小于 limit，删除叶子，否则不删除
            return None if limit > 0 else root
        if root.left: root.left = self.sufficientSubset(root.left, limit)
        if root.right: root.right = self.sufficientSubset(root.right, limit)
        # 如果有儿子没被删除，就不删 root，否则删 root
        return root if root.left or root.right else None
''',
    call='Solution().sufficientSubset(Tr([1,2,-3,-5,None,4,None]), -1)',
    expect=[1, None, -3, 4],
    result_fn=tree_list,
    views=[
        dict(type='text', fn=lambda S: f"剩余 `limit = {S['_inner']['limit']}`（已减去路径上的值）" if 'limit' in S['_inner'] else '', size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = root，黄圈 = 递归路径）', pointers={'root': 'blue'}, h=360),
        dict(type='calls', h=240, hide=()),
    ],
    watch=[('root', lambda S: S['_inner'].get('root').val if S['_inner'].get('root') else None, 'blue'),
           ('limit', lambda S: S['_inner'].get('limit'), 'yellow')],
    captions={
        'limit -= root.val': '`limit = {B.limit} - {root.val} = {limit}`：==把路径和折进 limit==，剩下还要凑 `{limit}`',
        'root.left is None and root.right is None': lambda S, B, r: (f'`{S.root.val}` 是叶子' if S.root.left is None and S.root.right is None else f'`{S.root.val}` 不是叶子 → 先处理儿子'),
        'return None if limit > 0': lambda S, B, r: (f'叶子：`limit = {S.limit} > 0` → 路径和不够 → ==删除叶子==，返回 None' if S.limit > 0 else f'叶子：`limit = {S.limit} ≤ 0` → 路径和够了 → ==保留==，返回自己'),
        'if root.left:': lambda S, B, r: (f'左儿子 `{B.root.left.val}`：递归后用返回值替换它，被删则变 None' if B.root.left else '没有左儿子 → 跳过'),
        'if root.right:': lambda S, B, r: (f'右儿子 `{B.root.right.val}`：同样用递归结果替换' if B.root.right else '没有右儿子 → 跳过'),
        'return root if root.left or root.right': lambda S, B, r: (f'`{S.root.val}` 至少有一个儿子留下 → ==不删==' if (S.root.left or S.root.right) else f'`{S.root.val}` 的儿子全被删 → 所有路径都不足 → ==删除自己==，返回 None'),
    },
    max_steps=80,
    cards=dict(
        one_liner='非叶节点被删，当且仅当它的所有儿子都被删',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['删除所有「不足节点」：经过它的每条根到叶路径和都 `< limit`',
                 '返回删除后的二叉树根',
                 '本视频：`[1,2,-3,-5,null,4,null]`，`limit = -1`',
                 '答案：`[1,null,-3,4]`'],
        quote='要删除非叶节点 node，==当且仅当 node 的所有儿子都被删除==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['叶子：根到它只有一条路径，和 `< limit` 就删',
              '非叶节点有儿子保留，就不能删（反证法）',
              '为了直接调用原函数，不加参数，而是每往下一层就 `limit -= root.val`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：不足节点看的是==根到叶子==的路径和，不是到中间节点的和',
                 '删除后中间节点仍然是中间节点，不会变成叶子',
                 '`limit > 0` 表示路径和仍小于原 limit，叶子要删',
                 '同类题：1123 / 865 的有递有归'],
    ),
)
