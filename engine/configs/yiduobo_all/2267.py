GRID = [['(', ')', ')'], ['(', '(', ')']]


def _f(S):
    if 'f' not in S:
        return None
    return [[('{' + ','.join(map(str, sorted(s))) + '}') if s else '∅' for s in row] for row in S['f']]


def _col(S, i, j, v):
    if 'f' not in S:
        return None
    if 'i' in S and (i, j) == (S['i'], S['j']):
        return 'blue'
    if S['f'][i][j]:
        return 'green'
    return None


CONFIG = dict(
    num=2267, title='检查是否有合法括号字符串路径', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='网格 DP · f[i][j] 存可能的剩余左括号集合',
    tags=['网格图', '动态规划', '难度分 2085'],
    code='''
class Solution(object):
    def hasValidPath(self, grid):

        m = len(grid)
        n = len(grid[0])
        f = [[set() for j in range(n)] for i in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '(':
                    delta = 1
                else:
                    delta = -1
                
                if i == 0:
                    if j == 0:
                        if delta == -1:
                            return False
                        else:
                            f[i][j].add(1)
                    else:
                        for cnt in list(f[i][j - 1]):
                            if 0 <= cnt + delta <= m + n - i - j:
                                f[i][j].add(cnt + delta)
                elif j == 0:
                    for cnt in list(f[i - 1][j]):
                        if 0 <= cnt + delta <= m + n - i - j:
                            f[i][j].add(cnt + delta)
                else:
                    for cnt in list(f[i - 1][j]):
                        if 0 <= cnt + delta <= m + n - i - j:
                            f[i][j].add(cnt + delta)
                    
                    for cnt in list(f[i][j - 1]):
                        if 0 <= cnt + delta <= m + n - i - j:
                            f[i][j].add(cnt + delta)

        return 0 in f[-1][-1]
''',
    call=f'Solution().hasValidPath({GRID})',
    expect=True,
    skip=['m = len', 'n = len', 'f = [[', 'delta = 1', 'delta = -1'],
    views=[
        dict(type='grid', var='grid', cell=96, h=210, label='grid（蓝 = 正在算的格子）',
             color=lambda S, i, j, v: 'blue' if 'i' in S and (i, j) == (S['i'], S['j']) else None),
        dict(type='grid', var=_f, cell=96, h=250, label='f[i][j]：以该格为终点的路径，可能剩余的左括号数（绿 = 已算出非空）',
             color=_col, cursors=[('i', 'j', 'yellow')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('delta', 'delta', 'green'),
           ('f[i][j]', lambda S: sorted(S['f'][S['i']][S['j']]) if 'i' in S and 'delta' in S else None, 'cyan')],
    captions={
        9: lambda S, B, r: f"`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` → delta = =={'+1' if S.grid[S.i][S.j] == '(' else '−1'}==（左括号 +1，右括号 −1）",
        'f = [[set()': '`f[i][j]` 是集合：存==所有可能==的剩余左括号数（不是只留最大值）',
        'if delta == -1': lambda S, B, r: ('起点是 `)`，一开始右括号就多了 → 直接 False' if S.delta == -1
                                           else '起点是 `(`，可以继续'),
        'f[i][j].add(1)': '起点是 `(` → 剩余左括号 1 个：`f[0][0] = {1}`',
        'for cnt in list(f[i][j - 1])': '从==左边==格子 `({i},{j - 1})` 走来：它的剩余数集合是 `{sorted(f[i][j - 1])}`，逐个取出 `cnt`',
        'for cnt in list(f[i - 1][j])': '从==上边==格子 `({i - 1},{j})` 走来：它的剩余数集合是 `{sorted(f[i - 1][j])}`，逐个取出 `cnt`',
        'if 0 <= cnt + delta <= m + n - i - j': lambda S, B, r: (
            f'`cnt + delta = {S.cnt} + {S.delta} = {S.cnt + S.delta}`，在 `[0, {S.m + S.n - S.i - S.j}]` 内 → 保留'
            if 0 <= S.cnt + S.delta <= S.m + S.n - S.i - S.j
            else f'`cnt + delta = {S.cnt + S.delta}` 不在 `[0, {S.m + S.n - S.i - S.j}]`：'
                 + ('小于 0 → 右括号太多，丢弃' if S.cnt + S.delta < 0 else '太大，后面消不完 → 丢弃')),
        'f[i][j].add(cnt + delta)': '`f[{i}][{j}]` 加入 `{cnt + delta}` → `{sorted(f[i][j])}`',
        'return 0 in f[-1][-1]': lambda S, B, r: f'终点集合 `{sorted(B.f[-1][-1])}`：包含 0 吗？=={r}=='
    },
    cards=dict(
        one_liner='f[i][j] 记下到这格所有可能的“剩余左括号数”，终点有 0 就行',
        complexity='时间 `O(mn(m+n))`，空间 `O(mn(m+n))`',
        problem=['`m×n` 括号网格，从左上走到右下，只能向下或向右',
                 '路径上拼出的括号串必须==合法==，问是否存在',
                 '本视频：2×3 网格 → `true`'],
        quote='将状态改成f[i][j]表示以(i, j)为终点的路径，在括号抵消后所有可能的剩余左括号数目的集合。',
        quote_src='—— yiduobo 题解原文',
        idea=['只留“最大剩余数”不行：它可能到终点还有多余的 `(`',
              '所以状态是==集合==：到 `(i,j)` 能剩下 `k` 个左括号吗？',
              '转移像“矩阵最长路径”：从上、左两格的集合各加 `delta` 得到当前格',
              '终点集合里有 `0` → 存在合法路径'],
        summary=['时间 `O(mn(m+n))`，状态最多 `mn × (m+n)` 个',
                 '剪枝：剩余数不能为负，也不能超过 `m+n-i-j`（后面格子不够消）',
                 '易错：必须保留所有可能值，只留最大值会漏答案',
                 '对比灵神：灵神 DFS + 记忆化只访问可达状态；这里是正向 DP 全表',
                 '原文已是 Python 3 可运行的写法，代码未改'],
    ),
)
