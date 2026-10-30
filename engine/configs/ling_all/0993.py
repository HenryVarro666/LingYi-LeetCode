def _nv(n):
    return '无' if n is None else str(n.val)


CONFIG = dict(
    num=993, title='二叉树的堂兄弟节点', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS · 记录深度与父节点',
    tags=['灵神题单', '链表树与回溯', '难度分 1288'],
    code='''
class Solution:
    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        ans = False
        depth = father = None
        def dfs(node: Optional[TreeNode], fa: Optional[TreeNode], d: int) -> bool:
            nonlocal ans, depth, father
            if node is None or depth and d > depth:
                return False
            if node.val == x or node.val == y:  # 找到 x 或 y
                if depth:  # 之前找到 x y 其中一个
                    ans = depth == d and father != fa
                    return True  # 表示 x 和 y 都找到
                depth, father = d, fa  # 之前没找到，记录信息
            return dfs(node.left, node, d + 1) or dfs(node.right, node, d + 1)
        dfs(root, None, 1)
        return ans
''',
    call='Solution().isCousins(Tr([1,2,3,None,4,None,5]), 5, 4)',
    expect=True,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前 node，黄圈 = 递归路径）', pointers={'node': 'blue', 'father': 'pink'},
             color=lambda S, n: 'green' if n.val in (4, 5) else None, h=300),
        dict(type='text', fn=lambda S: f"已记录：`depth = {S.get('depth')}`，`father = {_nv(S.get('father'))}`    答案 `ans = {S.get('ans')}`", size=26, h=56),
        dict(type='calls', h=230, hide=('root',)),
    ],
    watch=[('node', lambda S: S['_inner'].get('node').val if S['_inner'].get('node') else None, 'blue'),
           ('d', lambda S: S['_inner'].get('d'), 'yellow'),
           ('depth', 'depth'), ('father', lambda S: _nv(S.get('father')), 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = False': '`ans` 记录最终结果，默认 `False`',
        'depth = father': '`depth`、`father` 用来记下==先找到的那个==节点的深度和父节点',
        'dfs(root, None, 1)': '从根出发 DFS：根的父节点是 `None`，深度记为 `1`',
        'if node is None or depth and d > depth': lambda S, B, r: (
            '空节点 → 返回 `False`，回到上一层' if S['_inner'].get('node') is None
            else (f'已找到一个，且当前深度 `{S.d}` > `depth = {S.depth}` → ==更深的点不可能是堂兄弟==，剪枝返回' if S.depth and S.d > S.depth
                  else f'节点 `{S["_inner"]["node"].val}`（深度 {S.d}）不用剪枝，继续')),
        'if node.val == x or node.val == y': lambda S, B, r: (
            f'节点 `{S.node.val}` 是 x 或 y → ==找到了=={"（第二个）" if S.depth and S.depth else "（第一个）"}' if S.node.val in (4, 5)
            else f'节点 `{S.node.val}` 既不是 `x` 也不是 `y` → 继续往下找'),
        'if depth:': lambda S, B, r: ('之前已找到过一个 → 现在 x、y 都找到了，可以判断了' if B.depth else '之前没找到过 → 这是第一个，先记录它'),
        'ans = depth == d': '同深度？`depth = {depth}`，`d = {d}`；父节点不同？`{_nv(father)}` ≠ `{_nv(B.node and fa)}` → ans = =={ans}==',
        'return True': '两个都找到了 → 返回 `True`，一路向上提前结束，不再搜别的子树',
        'depth, father = d, fa': '第一个目标：记下深度 `depth = {d}`，父节点 `father = {_nv(fa)}`',
        'return dfs(node.left': lambda S, B, r: ('左子树搜完返回 `False`（没找齐）→ 继续搜右子树' if r is False else ('递归返回 `True`：x、y 都找齐了 → 逐层向上传递，不再搜别处' if r is True else '先搜左子树，没找齐再搜右子树；`d + 1` 表示儿子深一层')),
        'return ans': '返回 `ans = {ret}`：5 和 4 都在深度 3，父节点分别是 3 和 2，==深度同、父不同== → 堂兄弟',
    },
    skip=['nonlocal'],
    cards=dict(
        one_liner='DFS 记下先找到的节点的深度和父亲，找到第二个时一比就知道',
        complexity='时间 `O(n)`，空间 `O(n)`（递归栈）',
        problem=['二叉树节点值互不相同，给定两个值 `x` 和 `y`',
                 '深度相同、但父节点不同，才是==堂兄弟==',
                 '示例：`root = [1,2,3,null,4,null,5]`，`x = 5`，`y = 4` → `true`'],
        quote='DFS 传入三个参数：当前节点 node、父节点 fa、深度 d。如果之前找到 x 或 y，那么现在 x 和 y 都找到了。如果 depth = d 且 father ≠ fa，说明是堂兄弟节点。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 时把「父节点」和「深度」当参数往下传',
              '遇到 x 或 y：第一次只记录 `depth, father`；第二次就能直接比较',
              '写法三再加两处优化：已找到一个后不递归更深的点，找齐后提前返回'],
        result='运行结束，返回 `True`',
        summary=['时间 `O(n)`，空间 `O(n)`（链状树时递归栈最深）',
                 '易错：根的深度设为 `1`，这样 `depth` 非空判断（`if depth`）不会因为 0 出错',
                 '易错：比较的是父==节点==而不是父节点的值（本题值唯一，两者等价）',
                 '写法一、二：没有剪枝或只提前返回；写法三（本视频）三处优化最彻底'],
    ),
)
