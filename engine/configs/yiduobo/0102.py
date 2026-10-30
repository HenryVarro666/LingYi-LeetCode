def nv(x):
    return '空' if x is None else str(x.val)


def tree_color(S, n):
    seen = {v for row in S.get('res', []) for v in row}
    return 'green' if n.val in seen else None


def cap_len(S, B, ret):
    if len(S.res) < S.level:
        return f'`len(res) = {len(S.res)} < level = {S.level}` → ==第一次来到第 {S.level} 层==，先开一个新列表'
    return f'`len(res) = {len(S.res)} ≥ level = {S.level}` → 第 {S.level} 层的列表已经有了'


def cap_put(S, B, ret):
    i = S.level - 1
    return f'把 `{S.now.val}` 放进第 {S.level} 层的末尾：`res[{i}] = {S.res[i]}`'


def cap_lif(S, B, ret):
    if S.now.left:
        return f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 先往左递归'
    return f'`{S.now.val}` 没有左孩子'


def cap_rif(S, B, ret):
    if S.now.right:
        return f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 再往右递归'
    return f'`{S.now.val}` 没有右孩子 → 这一层递归结束，回溯'


CONFIG = dict(
    num=102, title='二叉树的层序遍历', difficulty='Medium', category='二叉树',
    author='yiduobo', technique='DFS · 记录层级',
    code='''
class Solution(object):
    def levelOrder(self, root):
        res = []

        self.dfs(root, 1, res)
        return res

    def dfs(self, now, level, res):
        if now is None:
            return

        if len(res) < level:
            res.append([])
        res[level - 1].append(now.val)
        if now.left:
            self.dfs(now.left, level + 1, res)
        if now.right:
            self.dfs(now.right, level + 1, res)
''',
    call='Solution().levelOrder(Tr([1,2,3,4,None,None,5]))',
    expect=[[1], [2, 3], [4, 5]],
    views=[
        dict(type='tree', label='二叉树（绿 = 已加入 res）', pointers={'now': 'blue'}, h=255, color=tree_color),
        dict(type='calls', h=190),
        dict(type='table', var='res', label='res（第 i 行 = 第 i+1 层）', h=200, cell=52,
             rows=lambda S: [f'L{i + 1}' for i in range(len(S.get('res', [])))],
             color=lambda S, i, j, v: 'green' if 'now' in S and S['now'] is not None and v == S['now'].val else None),
    ],
    watch=[('now', 'now', 'blue'), ('level', 'level', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res[i]` 存第 `i+1` 层的节点值，先为空',
        'self.dfs(root, 1, res)': '从根开始搜索，==根在第 1 层==',
        'if now is None': lambda S, B, ret: f'`now = {nv(S.now)}`，`level = {S.level}`：节点非空，处理它',
        'if len(res) < level': cap_len,
        'res.append([])': lambda S, B, ret: f'`res` 末尾加一个空列表 → 现在有 {len(S.res)} 层',
        'res[level - 1].append': cap_put,
        'if now.left': cap_lif,
        'self.dfs(now.left': lambda S, B, ret: f'递归左孩子 `{S.now.val}`，层级 `+1` → `level = {S.level}`',
        'if now.right': cap_rif,
        'self.dfs(now.right': lambda S, B, ret: f'递归右孩子 `{S.now.val}`，层级 `+1` → `level = {S.level}`',
        'return res': lambda S, B, ret: f'搜索结束，返回 `{ret}`',
    },
    cards=dict(
        one_liner='DFS 时带上层级 level，碰到节点就放进第 level 层的列表',
        complexity='时间 `O(n)`，空间 `O(h)`（递归栈，不计答案）',
        problem=['给你二叉树的根 `root`，返回节点值的==层序遍历==',
                 '即逐层地、从左到右访问所有节点',
                 '本视频：`[1,2,3,4,null,null,5]` → `[[1],[2,3],[4,5]]`'],
        quote='从根节点开始往下搜索回溯，==在搜索过程中记录下当前的层级==，然后每碰到一个节点就将其加入到当前层级的list中即可。',
        quote_src='—— yiduobo 题解',
        idea=['不用队列：`dfs(now, level, res)` 带着层级往下走',
              '第一次到达某一层时（`len(res) < level`）给它开一个新列表',
              '==先左后右==递归，所以每层列表里的顺序天然是从左到右'],
        result='运行结束，返回 `[[1],[2,3],[4,5]]`：DFS 先访问了 4 再访问 3，但各层内顺序仍正确',
        summary=['时间 `O(n)`；空间 `O(h)`，`h` 为树高',
                 '访问顺序是前序 `1,2,4,3,5`，不是层序；靠 `level` 下标把值放对位置',
                 '易错：`res[level - 1]`，层级从 1 开始而下标从 0 开始',
                 '原文为 Python 2 风格，仅删去 docstring 和定义注释，其余照搬'],
    ),
)
