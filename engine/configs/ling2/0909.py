BOARD = [[-1, -1, -1], [-1, 2, -1], [-1, -1, 9]]
N = len(BOARD)


def _cell(sq):
    rr, cc = divmod(sq - 1, N)
    c = cc if rr % 2 == 0 else N - 1 - cc
    return N - 1 - rr, c


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cell = 140
    gx, gy = x0 + 30, y0 + 46
    cv.text((x0 + 18, y0 + 4), '棋盘（蓝 = 当前 x，黄框 = 掷到的 y，深绿 = 已访问）', 24, T['muted'], bold=True)
    vis = S.get('vis') or []
    x, y = S.get('x'), S.get('y')
    line = S.get('_line')
    cur_y = y if line in (18, 22) else None
    for sq in range(1, N * N + 1):
        r, c = _cell(sq)
        X, Y = gx + c * cell, gy + r * cell
        seen = sq < len(vis) and vis[sq]
        fill = T['blue'] if sq == x else ((30, 70, 45) if seen else T['panel2'])
        cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=fill, r=12,
                outline=T['yellow'] if sq == cur_y else T['border'], width=5 if sq == cur_y else 1)
        cv.text((X + 14, Y + 10), sq, 30, T['bg'] if sq == x else T['text'], bold=True)
        v = BOARD[r][c]
        if v != -1:
            cv.text((X + cell - 12, Y + cell - 12), f'→{v}', 22, T['green'] if v > sq else T['red'], anchor='rb', bold=True)
    for sq in range(1, N * N + 1):
        r, c = _cell(sq)
        v = BOARD[r][c]
        if v != -1:
            r2, c2 = _cell(v)
            p0 = (gx + c * cell + cell / 2, gy + r * cell + cell / 2)
            p1 = (gx + c2 * cell + cell / 2, gy + r2 * cell + cell / 2 + (14 if v < sq else 0))
            cv.arrow(p0, p1, T['green'] if v > sq else T['red'], 5, 18)
    # 右侧：BFS 队列
    px = gx + N * cell + 50
    cv.text((px, gy), f'step = {S.get("step", 0)}', 30, T['orange'], bold=True)
    for k, (name, arr, col) in enumerate((('tmp（本轮）', S.get('tmp'), T['blue']), ('q（下一轮）', S.get('q'), T['purple']))):
        Y = gy + 70 + k * 120
        cv.text((px, Y), name, 24, T['muted'], bold=True)
        if arr is None:
            continue
        for i, v in enumerate(arr):
            X = px + i * 62
            on = name.startswith('tmp') and v == x
            cv.rect((X, Y + 36, X + 56, Y + 92), fill=col if on else T['panel2'], r=8, outline=col, width=2)
            cv.text((X + 28, Y + 64), v, 26, T['bg'] if on else T['text'], anchor='mm', bold=True)
        if not arr:
            cv.text((px, Y + 64), '空', 24, T['dim'], anchor='lm')


def _cap_nxt(S, B, ret):
    y = S.y
    rr, cc = divmod(y - 1, N)
    c = cc if rr % 2 == 0 else N - 1 - cc
    v = S.nxt
    dest = v if v > 0 else y
    seen = S.vis[dest]
    kind = '==梯子==' if v > y else '==蛇=='
    if S.step > 0:
        return f'掷到 `{y}`' + (f' → {kind}到 `{v}`' if v > 0 else '') + ('：已访问，跳过' if seen else '：==新格子==')
    where = f'`divmod({y}-1, {N}) = ({rr},{cc})`' + ('，奇数行从右到左 → `c = ' + str(c) + '`' if rr % 2 else '')
    tail = '，==已经访问过== → 跳过（防止绕圈）' if seen else ''
    if v < 0:
        return f'掷到 `{y}`：{where}，`board[{-1 - rr}][{c}] = -1` 没有蛇梯 → 停在 `{y}`{tail}'
    return f'掷到 `{y}`：{where}，`board[{-1 - rr}][{c}] = {v}` 是{kind} → 传送到 `{v}`{tail}'


def _cap_vis(S, B, ret):
    if S.step == 0 and sum(S.vis) == 2:
        return f'`{S.nxt}` 第一次到达 → 标记 `vis[{S.nxt}]`，加入下一轮队列 `q`（掷 `step + 1` 次到达）'
    return f'`{S.nxt}` 第一次到达 → 标记 vis，入队 `q`'


CONFIG = dict(
    num=909, title='蛇梯棋', difficulty='Medium', category='图论',
    author='灵茶山艾府', technique='BFS（双列表），vis 防环',
    tags=['面试经典150'],
    code='''
class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        vis = [False] * (n * n + 1)
        vis[1] = True  # 题目保证起点没有蛇梯，不写也可以
        q = [1]  # 起点
        step = 0
        while q:
            tmp = q
            q = []
            for x in tmp:
                if x == n * n:  # 终点
                    return step
                for y in range(x + 1, min(x + 6, n * n) + 1):
                    r, c = divmod(y - 1, n)
                    if r % 2:
                        c = n - 1 - c  # 奇数行从右到左
                    nxt = board[-1 - r][c]
                    if nxt < 0:
                        nxt = y
                    if not vis[nxt]:
                        vis[nxt] = True  # 有环的情况下，避免死循环
                        q.append(nxt)
            step += 1
        return -1  # 无法到达终点
''',
    call=f'Solution().snakesAndLadders({BOARD})',
    expect=1,
    skip=['for y in range', 'r, c = divmod', 'if r % 2', 'c = n - 1 - c', 'if nxt < 0', 'nxt = y', 'if not vis[nxt]',
          'q.append(nxt)', 'q = []', 'n = len(board)'],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('step', 'step', 'orange'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('nxt', 'nxt')],
    captions={
        'vis = [False]': '`vis[i]`：编号 i 是否已经到达过（`n² = {n * n}` 个格子）',
        'vis[1] = True': '起点 `1` 标记为已访问',
        'q = [1]': '队列从起点 `1` 开始：掷 0 次就在 1',
        'step = 0': '`step`：当前这一轮是掷了几次骰子',
        'while q': lambda S, B, r: f'队列非空：开始第 `{S.step}` 轮（这一轮的格子都是掷 {S.step} 次能到的）',
        'tmp = q': '`tmp` = 这一轮要扩展的格子 `{tmp}`，`q` 清空用来收集下一轮',
        'for x in tmp': lambda S, B, r: (f'取出 `x = {S.x}`' if B.get('x') != S.get('x') else '这一轮的格子都扩展完了'),
        'if x == n * n': lambda S, B, r: (f'`x = {S.x}` 就是终点 `{N * N}`！' if S.x == N * N
                                          else f'`x = {S.x}` 不是终点 → 枚举骰子点数 `{S.x + 1}` ~ `{min(S.x + 6, N * N)}`'),
        'return step': '到达终点，最少掷 =={ret}== 次',
        'nxt = board[-1 - r][c]': _cap_nxt,
        'vis[nxt] = True': _cap_vis,
        'step += 1': '这一轮扩展完，`step` → {step}',
    },
    cards=dict(
        one_liner='把格子当成图的节点，掷骰子是边：BFS 的轮数就是最少掷骰次数',
        complexity='时间 `O(6 n^2)`，空间 `O(n^2)`',
        problem=['`n × n` 棋盘从左下角开始==蛇形==编号 `1 ~ n²`，起点在 `1`',
                 '每回合掷骰到 `curr+1 ~ curr+6`；落在蛇/梯子起点就==传送一次==',
                 '求到达 `n²` 的最少掷骰次数，到不了返回 `-1`',
                 '本视频：3×3 棋盘，`3` 有梯子到 `9`，`5` 有蛇到 `2` → 答案 `1`'],
        quote='假设当前在编号 x，那么可以移动到 [x+1, min(x+6, n²)] 中的编号 y。如果编号 y 对应的 board[r][c] > 0，那么继续移动到编号 board[r][c]。如果==无法到达终点（有环）==，返回 -1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['编号减一再算：`y−1` 在倒数第 `r = (y−1) // n` 行，余数 `(y−1) % n`',
              '`r` 是奇数时这一行==从右往左==，列号要翻转成 `n−1−c`',
              'BFS 双列表：`tmp` 是这一轮，`q` 收集下一轮；`vis` 防止蛇造成死循环'],
        result='掷到 3 爬梯子直达 9：最少 `1` 次',
        summary=['时间 `O(6 n^2)`：每个格子出队一次，枚举 6 个点数；空间 `O(n^2)`',
                 '易错：行号是从==下往上==数的，用 `board[-1 - r]`',
                 '易错：传送只发生一次，落点就算是另一条蛇梯的起点也不再继续',
                 '易错：`vis` 标记的是传送后的落点 `nxt`，不是 `y`'],
    ),
)
