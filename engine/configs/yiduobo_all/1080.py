CONFIG = dict(
    num=1080, title='根到叶路径上的不足节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='递归 · 返回子树最大路径和',
    tags=['灵神题单', '链表树与回溯', '难度分 1805'],
    code='''
class Solution(object):
    def sufficientSubset(self, root, limit):

        max_s = self.dfs(root, 0, limit)
        if max_s < limit:
            return None
        else:
            return root
    
    def dfs(self, now, s, limit):
        s += now.val
        if not now.left:
            if not now.right:
                return s
            else:
                max_r = self.dfs(now.right, s, limit)
                if max_r < limit:
                    now.right = None
                return max_r
        elif not now.right:
            max_l = self.dfs(now.left, s, limit)
            if max_l < limit:
                now.left = None
            return max_l
        else:
            max_l = self.dfs(now.left, s, limit)
            max_r = self.dfs(now.right, s, limit)
            if max_l < limit:
                now.left = None
            if max_r < limit:
                now.right = None
            return max(max_l, max_r)
''',
    call='Solution().sufficientSubset(Tr([1,2,-3,-5,None,4,None]), -1)',
    expect=[1, None, -3, 4],
    result_fn=tree_list,
    views=[
        dict(type='text', fn=lambda S: f"路径和 `s = {S['_inner']['s']}`，`limit = {S['limit']}`" if 's' in S['_inner'] else '', size=26, h=56),
        dict(type='tree', label='二叉树（蓝 = now）', pointers={'now': 'blue'}, h=360),
        dict(type='calls', h=240, hide=()),
    ],
    watch=[('now', lambda S: S['_inner'].get('now').val if S['_inner'].get('now') else None, 'blue'),
           ('s', lambda S: S['_inner'].get('s'), 'yellow'), ('limit', 'limit', 'orange')],
    captions={
        'max_s = self.dfs': '从根出发，`s = 0`：带着「根到当前节点的路径和」往下走',
        'if max_s < limit': lambda S, B, r: (f'整棵树最大路径和 `{S.max_s} < {S.limit}` → 根也不足，返回 None' if S.max_s < S.limit else f'整棵树最大路径和 `{S.max_s} ≥ {S.limit}` → ==保留根=='),
        's += now.val': '`s = {B.s} + {now.val} = {s}`：根到 `{now.val}` 的路径和',
        12: lambda S, B, r: (f'`{S.now.val}` 没有左儿子' if not S.now.left else f'`{S.now.val}` 有左儿子 `{S.now.left.val}`'),
        13: lambda S, B, r: ('也没有右儿子 → ==叶子==' if not S.now.right else f'只有右儿子 `{S.now.right.val}` → 只往右递归'),
        20: lambda S, B, r: ('有左儿子，没有右儿子 → 只往左递归' if not S.now.right else '左右儿子都有 → 两边都要递归'),
        'return s': '叶子：直接返回路径和 `{s}`，==这条路径的总和==',
        'max_r = self.dfs': '先递归右子树，拿到它的最大路径和',
        'max_l = self.dfs': '先递归左子树，拿到它的最大路径和',
        'if max_r < limit': lambda S, B, r: (f'右子树最大路径和 `{S.max_r} < {S.limit}` → 右子树全不足 → ==删掉右孩子==' if S.max_r < S.limit else f'右子树最大路径和 `{S.max_r} ≥ {S.limit}` → 保留'),
        'if max_l < limit': lambda S, B, r: (f'左子树最大路径和 `{S.max_l} < {S.limit}` → 左子树全不足 → ==删掉左孩子==' if S.max_l < S.limit else f'左子树最大路径和 `{S.max_l} ≥ {S.limit}` → 保留'),
        'now.right = None': '删除右孩子：`now.right = None`',
        'now.left = None': '删除左孩子：`now.left = None`',
        'return max_r': '只有一个孩子：返回它的最大路径和 `{max_r}`',
        'return max_l': '只有一个孩子：返回它的最大路径和 `{max_l}`',
        'return max(max_l, max_r)': '返回两边较大者 `max({max_l}, {max_r}) = {ret}`：==子树里最好的一条路径==',
    },
    max_steps=80,
    cards=dict(
        one_liner='先求子树最大路径和，小于 limit 的孩子直接剪掉',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['删除所有「不足节点」：经过它的每条根到叶路径和都 `< limit`',
                 '返回删除后的二叉树根',
                 '本视频：`[1,2,-3,-5,null,4,null]`，`limit = -1`',
                 '答案：`[1,null,-3,4]`'],
        quote='对于当前节点，我们需要先分别递归求出其左子树和右子树中路径和的最大值，若左子树的路径和最大值小于limit，那么将当前节点的左孩子删去。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs` 带着 `s`（根到当前的和），返回「以 now 为根的子树」里最大的根到叶路径和',
              '最大的都 `< limit` → 这棵子树所有路径都不足 → 父节点把它剪掉',
              '叶子直接返回 `s`；只有一个孩子时分情况处理，避免访问空节点'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：只有一个孩子时，不能对 None 递归，也不能把缺失的孩子当作 0',
                 '根自己也要判断：`max_s < limit` 返回 None',
                 '对比灵神：灵神每层减 limit，叶子判 `limit > 0`；yiduobo 向上返回最大路径和再比较',
                 '原文可直接在 Python 3 运行，代码未改'],
    ),
)
