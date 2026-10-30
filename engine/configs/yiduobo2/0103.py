def nv(x):
    return '空' if x is None else str(x.val)


def tree_color(S, n):
    seen = {v for row in S.get('res', []) for v in row}
    return 'green' if n.val in seen else None


def row_color(S, i, j, v):
    if 'index' in S:  # 反转阶段：已反转的行标橙（本例每层从左到右是递增的，反转后变成递减）
        row = S['res'][i]
        if row != sorted(row):
            return 'orange'
        return 'yellow' if i == S['index'] else None
    if 'now' in S and S['now'] is not None and v == S['now'].val:
        return 'green'
    return None


def cap_len(S, B, ret):
    if S.level > len(S.res):
        return f'`level = {S.level} > len(res) = {len(S.res)}` → ==第一次来到第 {S.level} 层==，先开一个新列表'
    return f'`level = {S.level} ≤ len(res) = {len(S.res)}` → 第 {S.level} 层的列表已经有了'


def cap_put(S, B, ret):
    i = S.level - 1
    return f'把 `{S.now.val}` 放进第 {S.level} 层的末尾：`res[{i}] = {S.res[i]}`'


def cap_lif(S, B, ret):
    if S.now.left:
        return f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → ==先往左==递归'
    return f'`{S.now.val}` 没有左孩子'


def cap_rif(S, B, ret):
    if S.now.right:
        return f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 再往右递归'
    return f'`{S.now.val}` 没有右孩子 → 这一层递归结束，回溯'


def cap_for(S, B, ret):
    if 'index' not in B:
        return f'DFS 结束，普通层序遍历 `res = {S.res}`；==第二步==：从 `index = 0` 开始逐层检查'
    if S.index != B.index:
        return f'检查下一层：`index = {S.index}`，`level_res = {S.level_res}`'
    return '每一层都检查完了'


def cap_odd(S, B, ret):
    if S.index % 2 == 1:
        return f'`index = {S.index}` 是==奇数== → 这一层要从右往左，需要反转'
    return f'`index = {S.index}` 是偶数 → 保持从左往右，不动'


def stage(S):
    if 'index' in S:
        return '第二步：==奇数层原地 `reverse()`==（index 从 0 开始）'
    if 'now' in S:
        return f"第一步：普通层序遍历（DFS 带层级），当前 `level = {S['level']}`"
    return '第一步：先求普通的层序遍历'


CONFIG = dict(
    num=103, title='二叉树的锯齿形层序遍历', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='DFS 记录层级 · 再反转奇数层',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def zigzagLevelOrder(self, root):
        res = []

        self.dfs(root, 1, res)

        for index, level_res in enumerate(res):
            if index % 2 == 1:
                level_res.reverse()
        return res

    def dfs(self, now, level, res):
        if now is None:
            return
        if level > len(res):
            res.append([])
        res[level - 1].append(now.val)
        if now.left:
            self.dfs(now.left, level + 1, res)
        if now.right:
            self.dfs(now.right, level + 1, res)
''',
    call='Solution().zigzagLevelOrder(Tr([1,2,3,4,None,None,5]))',
    expect=[[1], [3, 2], [4, 5]],
    views=[
        dict(type='text', h=50, fn=stage, size=26),
        dict(type='tree', label='二叉树（绿 = 已加入 res）', pointers={'now': 'blue'}, h=230, color=tree_color),
        dict(type='calls', h=185, hide=('res',)),
        dict(type='table', var='res', label='res（第 i 行 = 第 i+1 层，橙 = 已反转）', h=190, cell=52,
             rows=lambda S: [str(i) for i in range(len(S.get('res', [])))], color=row_color),
    ],
    watch=[('now', 'now', 'blue'), ('level', 'level', 'yellow'), ('index', 'index', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res[i]` 存第 `i+1` 层的节点值，先为空',
        'self.dfs(root, 1, res)': '第一步：从根开始搜索，==根在第 1 层==',
        'if now is None': lambda S, B, ret: f'`now = {nv(S.now)}`，`level = {S.level}`：节点非空，处理它',
        'if level > len(res)': cap_len,
        'res.append([])': lambda S, B, ret: f'`res` 末尾加一个空列表 → 现在有 {len(S.res)} 层',
        'res[level - 1].append': cap_put,
        'if now.left': cap_lif,
        'self.dfs(now.left': lambda S, B, ret: f'递归左孩子 `{S.now.val}`，层级 `+1` → `level = {S.level}`',
        'if now.right': cap_rif,
        'self.dfs(now.right': lambda S, B, ret: f'递归右孩子 `{S.now.val}`，层级 `+1` → `level = {S.level}`',
        'for index, level_res': cap_for,
        'if index % 2 == 1': cap_odd,
        'level_res.reverse()': lambda S, B, ret: f'原地反转：`res[{S.index}]` → =={S.level_res}==（`level_res` 和 `res[{S.index}]` 是同一个列表）',
        'return res': lambda S, B, ret: f'返回锯齿形结果 `{ret}`',
    },
    cards=dict(
        one_liner='先用 DFS 求出普通层序遍历，再把奇数层反过来',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈，不计答案）',
        problem=['给你二叉树的根 `root`，返回节点值的==锯齿形层序遍历==',
                 '先从左往右，下一层从右往左，层与层之间交替进行',
                 '本视频：`[1,2,3,4,null,null,5]` → `[[1],[3,2],[4,5]]`'],
        quote='同样是搜索回溯并记录下当前的层级来求出层次遍历。由于题目要求的是锯齿形的层次遍历，那么==只需要将层次遍历中的奇数层反过来==即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['完全复用 102 题：`dfs(now, level, res)` 带着层级往下走',
              '第一次到某层（`level > len(res)`）就开新列表；==先左后右==保证层内从左到右',
              '最后只对 `index` 为奇数的层调用 `reverse()`'],
        result='运行结束，返回 `[[1],[3,2],[4,5]]`：只有第 2 层（index 1）被反转',
        summary=['时间 `O(n)`：DFS 一遍 + 反转总长 `n`；空间 `O(h)`',
                 '易错：`index` 从 0 开始，==第 2 层对应 index 1==，所以反转 `index % 2 == 1`',
                 '`res[level - 1]`：层级从 1 开始而下标从 0 开始',
                 '对比灵神：BFS 每层收集完立刻 `vals[::-1]`；yiduobo 先全部收集再统一反转',
                 '原文为 Python 2 风格，仅删去 docstring 和 TreeNode 定义注释，其余照搬'],
    ),
)
