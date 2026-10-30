def _colq(S):
    m = S.get('m')
    if m is None or 'col_q' not in S or m >= len(S['col_q']):
        return []
    return list(S['col_q'][m])


def _diag(S):
    d = S.get('diag_q')
    return list(d) if d is not None else []


def _fcolor(S, r, c, v):
    i, m = S.get('i'), S.get('m')
    if i is None or m is None or 'f' not in S:
        return None
    if r == i and c == m:
        return 'yellow'
    n = len(S['piles'])
    if r > i and S.get('_line', 0) >= 26 and i + 2 * m < n:
        if c == m and r <= i + m:
            return 'blue'
        if m < c <= 2 * m and r == i + c:
            return 'pink'
    return None


def _fml(S):
    i, m = S.get('i'), S.get('m')
    if i is None or m is None:
        return '`f[i][m]`：从第 i 堆开始、当前 M=m，先手最多拿到的石子数；`s` = 后缀和'
    n = len(S['piles'])
    if i + 2 * m >= n:
        return f'`i + 2m = {i + 2 * m} ≥ {n}`：==可以全拿== → `f[{i}][{m}] = s = {S["s"]}`'
    return f'`f[{i}][{m}] = s − min( 列窗口 f[i+1..i+m][{m}] ， 斜窗口 f[i+x][x], x=m+1..2m )`'


def _cap_coldrop(S, B, ret):
    q = S.q
    return f'列窗口是 `[i+1, i+m]` = `[{S.i + 1}, {S.i + S.m}]`，队首 `{q[0]}`：' + ('==出窗，弹出==' if q[0] > S.i + S.m else '还在窗口内，保留')


def _cap_diag_front(S, B, ret):
    d = S.diag_q
    return f'斜向窗口的 x 范围是 `[m+1, 2m]` = `[{S.m + 1}, {2 * S.m}]`，队首 `x={d[0]}`：' + ('==x ≤ m，出窗，弹出==' if d[0] <= S.m else '在窗口内，保留')


def _cap_f(S, B, ret):
    n = len(S.piles)
    return (f'`f[{S.i}][{S.m}] = s − min(f[{S.q[0]}][{S.m}], f[{S.i + S.diag_q[0]}][{S.diag_q[0]}])` '
            f'= {S.s} − min({S.f[S.q[0]][S.m]}, {S.f[S.i + S.diag_q[0]][S.diag_q[0]]}) = =={S.f[S.i][S.m]}==')


CONFIG = dict(
    num=1140, title='石子游戏 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='博弈 DP · 单调队列优化', tags=['动态规划', '数学算法', '难度分 2035'],
    code='''
class Solution:
    def stoneGameII(self, piles: list[int]) -> int:
        n = len(piles)
        f = [[0] * (n + 1) for _ in range(n)]
        col_q = [deque() for _ in range(n + 1)]  # 每列的滑动窗口最小值（窗口向上滑动）

        s = 0
        for i in range(n - 1, -1, -1):
            s += piles[i]
            diag_q = deque()  # 斜向的滑动窗口最小值（窗口向右下滑动）
            for m in range(1, i // 2 + 2):
                if i + m * 2 >= n:  # 全拿
                    f[i][m] = s
                    continue

                # f[i+1][m] 进入列窗口
                q = col_q[m]
                while q and f[q[-1]][m] >= f[i + 1][m]:
                    q.pop()
                q.append(i + 1)

                # 队首离开列窗口
                if q[0] > i + m:
                    q.popleft()

                # f[i+m*2-1][m*2-1] 和 f[i+m*2][m*2] 进入斜向窗口
                for x in range(m * 2 - 1, m * 2 + 1):
                    while diag_q and f[i + diag_q[-1]][diag_q[-1]] >= f[i + x][x]:
                        diag_q.pop()
                    diag_q.append(x)

                # 队首离开斜向窗口
                if diag_q[0] <= m:
                    diag_q.popleft()

                f[i][m] = s - min(f[q[0]][m], f[i + diag_q[0]][diag_q[0]])

        return f[0][1]
''',
    call='Solution().stoneGameII([2, 7, 9, 4, 4])',
    expect=10,
    skip=['col_q = [deque()', 'diag_q = deque()', 'continue', 'for m in range', 'for x in range', 'n = len', 's = 0', 'f = [[0]'],
    max_steps=90,
    views=[
        dict(type='text', fn=_fml, size=24, h=50),
        dict(type='array', var='piles', label='piles', h=110, cell=70,
             color=lambda S, k, v: 'blue' if S.get('i') is not None and k == S['i'] else None),
        dict(type='table', var='f', label='f[i][m]（行 i，列 m）', h=360, cell=60, rows=lambda S: list(range(len(S['piles']))), cols=lambda S: list(range(len(S['piles']) + 1)), color=_fcolor,
             cursors=[('i', 'm', 'yellow', '')]),
        dict(type='queue', var=_colq, label='列队列 col_q[m]（存行号 i）', h=125, fmt=lambda j: f'{j}'),
        dict(type='queue', var=_diag, label='斜队列 diag_q（存 x）', h=125, fmt=lambda j: f'{j}'),
    ],
    watch=[('i', 'i', 'blue'), ('m', 'm', 'pink'), ('s', 's', 'green')],
    captions={
        'for i in range(n - 1': '`i` 从后往前：`f[i][·]` 依赖 `f[i+x][·]`',
        's += piles[i]': '`s` = 从第 `{i}` 堆到最后的石子总和（后缀和）= =={s}==',
        'for m in range': '`m` 只需枚举到 `i//2+1`，更大的 M 不可能出现',
        'if i + m * 2 >= n': lambda S, B, r: (f'`i + 2m = {S.i + 2 * S.m}` ' + ('≥' if S.i + 2 * S.m >= len(S.piles) else '<') + f' `n = {len(S.piles)}` → ' + ('可以全拿' if S.i + 2 * S.m >= len(S.piles) else '不能全拿，要比较各种拿法')),
        'f[i][m] = s\n': '',
        'q = col_q[m]': '取第 `m` 列的单调队列：对固定 `m`，窗口 `f[i+1..i+m][m]` 的最小值',
        'while q and f[q[-1]][m]': lambda S, B, r: (f'列队列为空，无需弹出' if not S.q else f'队尾 `f[{S.q[-1]}][{S.m}]` = {S.f[S.q[-1]][S.m]} ' + ('≥' if S.f[S.q[-1]][S.m] >= S.f[S.i + 1][S.m] else '<') + f' 新来的 `f[{S.i + 1}][{S.m}]` = {S.f[S.i + 1][S.m]} → ' + ('==更靠前又不更小，永远用不上==，弹出' if S.f[S.q[-1]][S.m] >= S.f[S.i + 1][S.m] else '保留')),
        'q.append(i + 1)': '`f[{i+1}][{m}]` 入列队列 → `q = {list(q)}`',
        'if q[0] > i + m': _cap_coldrop,
        'for x in range': '`x` 依次取 `2m-1`、`2m`：`f[i+x][x]` 依次进入斜向窗口',
        'while diag_q and': lambda S, B, r: (f'斜队列为空，无需弹出' if not S.diag_q else f'队尾 `f[{S.i + S.diag_q[-1]}][{S.diag_q[-1]}]` = {S.f[S.i + S.diag_q[-1]][S.diag_q[-1]]} ' + ('≥' if S.f[S.i + S.diag_q[-1]][S.diag_q[-1]] >= S.f[S.i + S.x][S.x] else '<') + f' 新来的 `f[{S.i + S.x}][{S.x}]` = {S.f[S.i + S.x][S.x]} → ' + ('弹出' if S.f[S.i + S.diag_q[-1]][S.diag_q[-1]] >= S.f[S.i + S.x][S.x] else '保留')),
        'diag_q.append(x)': '`x = {x}` 入斜队列 → `{list(diag_q)}`',
        'if diag_q[0] <= m': _cap_diag_front,
        'f[i][m] = s - min': _cap_f,
        'return f[0][1]': 'Alice 从 `i=0, M=1` 出发，先手最多拿 `f[0][1]` = =={ret}==',
    },
    cards=dict(
        one_liner='拿 X 堆 = 对手在剩下的局面里少拿：用「总数 − 对手最优」做博弈 DP',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['石子排成一行，轮流拿走前 `X` 堆（`1 ≤ X ≤ 2M`），然后 `M = max(M, X)`，Alice 先手',
                 '双方都最优，求 Alice 最多拿多少',
                 '示例：`[2,7,9,4,4]` → `10`'],
        quote='剩余石子的总数 - 对手拿走的石子总数 = 当前玩家拿走的石子总数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][m] = s[i] − min f[i+x][max(m,x)]`，对手拿得越少我拿得越多',
              '`max(m,x)` 分两段：`x ≤ m` 时是同一列 `f[·][m]` 的滑动窗口最小值',
              '`x > m` 时是斜向 `f[i+x][x]` 的滑动窗口最小值：各用一个单调队列'],
        after=[dict(heading='灵神的几种写法', lines=['先是记忆化搜索 `dfs(i, M)`，`O(n³)`', '再 1:1 翻译成递推 `f`', '最后用两个单调队列把枚举 X 的一层循环去掉'])],
        summary=['时间 `O(n²)`：每个 `f[i][m]` 至多进出两个队列各一次',
                 '`i + 2m ≥ n` 时全拿，直接 `f = s`',
                 '`m` 的上界是 `i//2 + 1`，`f` 的列开到 `n+1` 以放下边界',
                 '倒序遍历 `i`：状态来自更大的 `i`'],
    ),
)
