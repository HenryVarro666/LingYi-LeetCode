def _nv(n):
    return '空' if n is None else str(n.val)


def _pos(S):
    if 'row' not in S or 'node' not in S:
        return ''
    n = S.get('node')
    if n is None:
        return f"走到空节点 `(row={S['row']}, col={S['col']})`：没有东西可记"
    return f"节点 `{n.val}` 在 `(row={S['row']}, col={S['col']})`；左儿子 `(row+1, col−1)`，右儿子 `(row+1, col+1)`"


def _ans(S):
    if 'ans' not in S:
        return ''
    return f"答案 `ans = {S['ans']}`"


def _cap_if(S, B, ret):
    if S.node is None:
        return '`node` 是空节点 → ==递归边界==，直接返回'
    return f'节点 `{S.node.val}` 非空 → 记录它的 `(row, val)`，再递归两个儿子'


CONFIG = dict(
    num=987, title='二叉树的垂序遍历', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='DFS 记录 (row, col, val) + 哈希表分组',
    tags=['灵神题单', '链表树与回溯', '难度分 1676'],
    code='''
class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        groups = defaultdict(list)
        def dfs(node: Optional[TreeNode], row: int, col: int):
            if node is None:
                return
            groups[col].append((row, node.val))  # col 相同的分到同一组
            dfs(node.left, row + 1, col - 1)
            dfs(node.right, row + 1, col + 1)
        dfs(root, 0, 0)

        ans = []
        for _, g in sorted(groups.items()):
            g.sort()  # 按照 row 排序，row 相同按照 val 排序
            ans.append([val for _, val in g])
        return ans
''',
    call='''s = Solution()
s.tree = Tr([1,2,3,None,6,5])
s.verticalTraversal(s.tree)''',
    expect=[[2], [1, 5, 6], [3]],
    max_steps=90,
    skip=[6],
    views=[
        dict(type='text', fn=_pos, size=24, h=56),
        dict(type='tree', label='二叉树（蓝 = 当前 node）', pointers={'node': 'blue'}, h=250),
        dict(type='map', var='groups', label='groups：col → [(row, val), ...]',
             fmt=lambda k, v: f'{k}: {v}', h=190),
        dict(type='text', fn=_ans, size=24, h=50),
        dict(type='calls', h=150, hide=('root',)),
    ],
    watch=[('node.val', lambda S: getattr(S.get('node'), 'val', None), 'blue'), ('row', lambda S: S['_inner'].get('row'), 'yellow'),
           ('col', lambda S: S['_inner'].get('col'), 'pink')],
    captions={
        'groups = defaultdict': '`groups` 的 key 是列号 `col`，value 是这一列里所有的 `(row, val)`',
        'if node is None': _cap_if,
        'groups[col].append': '把 `(row={row}, val={node.val})` 放进第 `{col}` 列：`groups[{col}] = {groups[col]}`',
        'dfs(node.left': lambda S, B, r: f'往左：`row + 1 = {B.row + 1}`，`col − 1 = {B.col - 1}`，进入 `{_nv(B.node.left)}`',
        'dfs(node.right': lambda S, B, r: f'往右：`row + 1 = {B.row + 1}`，`col + 1 = {B.col + 1}`，进入 `{_nv(B.node.right)}`',
        'dfs(root, 0, 0)': '根在 `(0, 0)`，开始 DFS 收集所有节点的行列',
        'ans = []': 'DFS 完成：`groups` 里已按列分好组。接下来按 col 从小到大取出',
        'for _, g in sorted': lambda S, B, r: (f'下一列 `col = {S._}`：`g = {S.g}`' if len(S.ans) < len(S.groups) else '所有列都处理完了'),
        'g.sort()': '`g` 按 `(row, val)` 排序：==row 小的在前，row 相同 val 小的在前== → `{g}`',
        'ans.append': '只保留 val：这一列的结果 `{ans[-1]}`',
        'return ans': '按列从左到右的结果：`{ans}`',
    },
    cards=dict(
        one_liner='DFS 带上行列坐标，按列分组，组内按 (row, val) 排序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['根在 `(0, 0)`，左儿子 `(row+1, col−1)`，右儿子 `(row+1, col+1)`',
                 '按列从左到右输出，每列里按 row 从上到下，同行同列按值从小到大',
                 '本视频：`root = [1,2,3,null,6,5]` → `[[2],[1,5,6],[3]]`'],
        quote='把 col 相同的分到同一组，每组只保留 val，每组的 val 按照 row 从小到大排序，row 相同的按照 val 从小到大排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['DFS 的参数除了 `node`，还带上 `row` 和 `col`：往下一层 `row + 1`，往左 `col − 1`，往右 `col + 1`',
              '哈希表 key 是 `col`，value 是 `(row, val)` 列表',
              '`(row, val)` 元组直接 `sort()`：先比 row，再比 val，正好是题目要求'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(n)`',
                 '易错：同一行同一列的节点（如 5 和 6，都在 (2, 0)）要按值排序：元组 row 在前 val 在后',
                 '其他写法：记录最小列号免去 key 排序；两个列表模拟双端队列；全部 `(col,row,val)` 丢进一个列表排序后分组',
                 '本视频选用写法一（哈希表 + `sorted(groups.items())`）'],
    ),
)
