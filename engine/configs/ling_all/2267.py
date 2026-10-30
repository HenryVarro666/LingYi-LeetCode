GRID = [['(', ')', '(', '('], ['(', '(', ')', '('], ['(', '(', '(', ')']]

_X = lambda S: S['_inner'].get('x')
_Y = lambda S: S['_inner'].get('y')


def _txt(S):
    I = S['_inner']
    if 'c' not in I or 'x' not in I:
        return ''
    x, y, c = I['x'], I['y'], I['c']
    m, n = S['m'], S['n']
    need = m - x + n - y - 1
    return f'状态 `(x,y,c) = ({x},{y},{c})`：未匹配左括号 ==`{c}`==；后面还剩 `{need}` 格，最多能消掉 `{need}` 个'


CONFIG = dict(
    num=2267, title='检查是否有合法括号字符串路径', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='网格 DFS + 记忆化（状态 x,y,c）',
    tags=['网格图', '动态规划', '难度分 2085'],
    code='''
class Solution:
    def hasValidPath(self, grid: List[List[str]]) -> bool:
        m, n = len(grid), len(grid[0])
        if (m + n) % 2 == 0 or grid[0][0] == ')' or grid[-1][-1] == '(':
            return False

        @cache  # 效果类似 vis 数组
        def dfs(x: int, y: int, c: int) -> bool:
            if c > m - x + n - y - 1:  # 剪枝：即使后面都是 ')' 也不能把 c 减为 0
                return False
            if x == m - 1 and y == n - 1:  # 终点
                return c == 1  # 上面提前判断了，终点一定是 ')'

            c += 1 if grid[x][y] == '(' else -1
            if c < 0:  # 右括号比左括号还多
                return False
            return x < m - 1 and dfs(x + 1, y, c) or \\
                   y < n - 1 and dfs(x, y + 1, c)

        return dfs(0, 0, 0)  # 起点
''',
    call=f'Solution().hasValidPath({GRID})',
    expect=True,
    skip=['m, n = len'],
    max_steps=56,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='grid', var='grid', cell=100, h=330, label='grid（蓝框 = 当前 dfs 所在格子）',
             color=lambda S, i, j, v: ('blue' if (i, j) == (_X(S), _Y(S)) else None),
             cursors=[(_X, _Y, 'blue')]),
        dict(type='calls', h=300),
    ],
    watch=[('x', _X, 'blue'), ('y', _Y, 'pink'), ('c', lambda S: S['_inner'].get('c'), 'green')],
    captions={
        'if (m + n) % 2 == 0': lambda S, B, r: (
            f'路径长度 `m+n-1 = {B.m + B.n - 1}` 必须是偶数，起点不能是 `)`，终点不能是 `(` → 都满足，开始搜索'),
        'if c > m - x + n - y - 1': lambda S, B, r: (
            f'`c = {B.c}` 比剩余格数 `{B.m - B.x + B.n - B.y - 1}` 还大 → 后面全是 `)` 也消不完，==剪枝返回 False=='
            if B.c > B.m - B.x + B.n - B.y - 1
            else f'`c = {B.c}` ≤ 剩余格数 `{B.m - B.x + B.n - B.y - 1}`：还有希望消完，继续'),
        'if x == m - 1 and y == n - 1': lambda S, B, r: (
            f'到终点 `({B.x},{B.y})`：必须 `c == 1`（再被终点的 `)` 消掉就是 0）' if (B.x == B.m - 1 and B.y == B.n - 1)
            else f'`({B.x},{B.y})` 还不是终点，继续走'),
        'return c == 1': lambda S, B, r: f'`c = {B.c}`，`c == 1` → =={r}==',
        'c += 1 if': lambda S, B, r: (f'`grid[{S.x}][{S.y}] = (` → 未匹配的左括号 +1：`c` = =={S.c}==' if S.grid[S.x][S.y] == '('
                                      else f'`grid[{S.x}][{S.y}] = )` → 消掉一个左括号：`c` = =={S.c}=='),
        'if c < 0': lambda S, B, r: (f'`c = {S.c} < 0`：右括号比左括号还多，这条路不合法 → 返回 False' if S.c < 0
                                     else f'`c = {S.c} ≥ 0`：前缀合法，继续往下/往右走'),
        17: lambda S, B, r: ('优先往下 `dfs(x+1, y, c)`（要 `x < m - 1`）；子调用返回 True 就一路向上返回 True'),
        18: '不能再往下（到底了 / 下面已失败）→ 换往右：`dfs(x, y+1, c)`，带上更新后的 `c`',
        'return dfs(0, 0, 0)': lambda S, B, r: ('从起点 `(0,0)` 出发，初始 `c = 0`' if r is None else f'搜索结束 → =={r}=='),
    },
    cards=dict(
        one_liner='用 c 记录未匹配的左括号数：一路 ≥ 0，到终点恰好 1',
        complexity='时间 `O(mn(m+n))`，空间 `O(mn(m+n))`',
        problem=['`m×n` 括号网格，从左上走到右下，每次只能向下或向右',
                 '路径上的字符拼成的括号串必须==合法==',
                 '存在合法路径返回 `true`',
                 '本视频：3×4 网格 → `true`'],
        quote='所以如果 dfs(x,y,c) 最后返回的是 false，那后续访问同一个状态（再次调用 dfs(x,y,c)），仍然会得到 false。因此没必要重复访问同一个状态。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`c` = 尚未匹配的左括号个数：`(` 加一，`)` 减一',
              '任意时刻 `c ≥ 0`（右括号不能比左括号多），终点前 `c = 1`',
              '状态 `(x,y,c)`：DFS 找到路径就返回；`@cache` 保证每个状态只算一次',
              '路径长度固定为 `m+n-1`，必须是偶数，还能提前剪枝'],
        summary=['时间 `O(mn(m+n))`：状态 `(x,y,c)` 最多 `mn(m+n)/2` 个，每个至多访问一次',
                 '剪枝 1：`m+n` 为偶数、起点是 `)`、终点是 `(` 直接 False',
                 '剪枝 2：`c > 剩余格数` 时后面全是 `)` 也消不完',
                 '灵神提醒：DFS 只访问可达状态，比递推快 10 倍以上',
                 '易错：终点处判断 `c == 1`，因为终点本身的 `)` 还没被减'],
    ),
)
