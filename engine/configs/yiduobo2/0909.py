BOARD = [[-1, -1, -1], [-1, 2, -1], [-1, -1, 9]]
N = len(BOARD)


def _cell(sq):
    rr, cc = divmod(sq - 1, N)
    c = cc if rr % 2 == 0 else N - 1 - cc
    return N - 1 - rr, c


def _num(i, j):
    return (N - i - 1) * N + (N - j if i % 2 == N % 2 else j + 1)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cell = 140
    gx, gy = x0 + 30, y0 + 46
    line = S.get('_line')
    scanning = line is not None and line <= 13
    cv.text((x0 + 18, y0 + 4), '棋盘（黄框 = 正在看的格子；深绿 = used；蓝 = 当前 now）', 24, T['muted'], bold=True)
    used = S.get('used') or set()
    cur = None
    if scanning and 'j' in S:
        cur = _num(S['i'], S['j'])
    elif line in (25, 26, 27, 28, 29, 30) and isinstance(S.get('next'), int):
        cur = S['next']
    now = S.get('now') if not scanning else None
    jump = S.get('jump') or {}
    for sq in range(1, N * N + 1):
        r, c = _cell(sq)
        X, Y = gx + c * cell, gy + r * cell
        fill = T['blue'] if sq == now else ((30, 70, 45) if sq in used else T['panel2'])
        cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=fill, r=12,
                outline=T['yellow'] if sq == cur else T['border'], width=5 if sq == cur else 1)
        cv.text((X + 14, Y + 10), sq, 30, T['bg'] if sq == now else T['text'], bold=True)
        if sq in jump:
            v = jump[sq]
            cv.text((X + cell - 12, Y + cell - 12), f'→{v}', 22, T['green'] if v > sq else T['red'], anchor='rb', bold=True)
        if scanning:
            cv.text((X + cell - 12, Y + 12), f'[{r}][{c}]', 18, T['dim'], anchor='ra', mono=True)
    for sq, v in jump.items():
        r, c = _cell(sq)
        r2, c2 = _cell(v)
        p0 = (gx + c * cell + cell / 2, gy + r * cell + cell / 2)
        p1 = (gx + c2 * cell + cell / 2, gy + r2 * cell + cell / 2 + (14 if v < sq else 0))
        cv.arrow(p0, p1, T['green'] if v > sq else T['red'], 5, 18)
    px = gx + N * cell + 50
    cv.text((px, gy), f'jump = {jump}', 24, T['code'], mono=True)
    q = S.get('q')
    if q is None:
        if scanning and 'i' in S:
            same = S['i'] % 2 == N % 2
            cv.text((px, gy + 60), f'第 i = {S["i"]} 行：i % 2 与 n % 2 ' + ('一致' if same else '不一致'), 22, T['text'])
            cv.text((px, gy + 92), '→ 这一行' + ('从右往左编号' if same else '从左往右编号'), 22,
                    T['orange'] if same else T['text'], bold=True)
        return
    cv.text((px, gy + 60), f'step = {S.get("step", 0)}', 30, T['orange'], bold=True)
    cv.text((px, gy + 120), 'q（[l, r) 是这一轮）', 24, T['muted'], bold=True)
    l, r = S.get('l', 0), S.get('r', 1)
    for k, v in enumerate(q):
        X = px + k * 62
        inr = l <= k < r
        on = v == now and inr
        cv.rect((X, gy + 156, X + 56, gy + 212), fill=T['blue'] if on else T['panel2'], r=8,
                outline=T['cyan'] if inr else T['border'], width=3 if inr else 1)
        cv.text((X + 28, gy + 184), v, 26, T['bg'] if on else T['text'], anchor='mm', bold=True)
        cv.text((X + 28, gy + 218), k, 16, T['dim'], anchor='mt', mono=True)


def _cap_cell(S, B, ret):
    i, j = S.i, S.j
    v = S.board[i][j]
    if v == -1:
        return f'`board[{i}][{j}] = -1`：没有蛇梯'
    return f'`board[{i}][{j}] = {v}`：有蛇梯 → 算出这个格子的编号'


def _cap_par(S, B, ret):
    i = S.i
    if i % 2 == N % 2:
        return f'`i % 2 = {i % 2}` 与 `n % 2 = {N % 2}` ==一致== → 这一行从右往左排（逆序）'
    return f'`i % 2 = {i % 2}` 与 `n % 2 = {N % 2}` 不一致 → 这一行从左往右排（顺序）'


def _cap_next(S, B, ret):
    nx, b = S.next, B.next
    if nx != b:
        kind = '==梯子==' if nx > b else '==蛇=='
        return f'`{b}` 在 jump 里：是{kind}，跳到 `{nx}`'
    return f'`{nx}` 没有蛇梯，就停在 `{nx}`'


CONFIG = dict(
    num=909, title='蛇梯棋', difficulty='Medium', category='图论',
    author='yiduobo', technique='先建跳跃表，再 BFS',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def snakesAndLadders(self, board):
        jump = {}
        n = len(board)
        for i in range(n):
            for j in range(n):
                if board[i][j] != -1:
                    now = (n - i - 1) * n
                    if i % 2 == n % 2:
                        now += n - j
                    else:
                        now += j + 1
                    jump[now] = board[i][j]

        q = [1]
        l = 0
        r = 1
        used = set([1])
        step = 0
        while l < r:
            step += 1
            for now in q[l : r]:
                for next in range(now + 1, now + 7):
                    if next <= n * n:
                        next = jump.get(next, next)
                        if next not in used:
                            used.add(next)
                            q.append(next)
                            if next == n * n:
                                return step
            l, r = r, len(q)

        return -1
''',
    call=f'Solution().snakesAndLadders({BOARD})',
    expect=1,
    skip=['for i in range(n)', 'for j in range(n)', 'n = len(board)', 'else:', 'l = 0', 'r = 1'],
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('now', 'now', 'blue'), ('next', lambda S: S.get('next'), 'yellow'), ('step', 'step', 'orange'), ('used', 'used', 'green')],
    captions={
        'jump = {}': '`jump`：蛇 / 梯子的起点编号 → 目的地编号',
        'if board[i][j] != -1': _cap_cell,
        'now = (n - i - 1) * n': '第 `i = {i}` 行下面还有 `{n - i - 1}` 整行 → 先数 `{now}` 个格子',
        'if i % 2 == n % 2': _cap_par,
        'now += n - j': '逆序：`now += n − j = {n - j}` → 编号 =={now}==',
        'now += j + 1': '顺序：`now += j + 1 = {j + 1}` → 编号 =={now}==',
        'jump[now] = board[i][j]': '记下 `jump[{now}] = {jump[now]}`',
        'q = [1]': '棋盘扫完，开始 BFS：队列从 `1` 出发',
        'used = set([1])': '`used` 记录到达过的格子；`l`、`r` 框出这一轮的队列区间',
        'step = 0': '`step` = 已经掷了几次骰子',
        'while l < r': lambda S, B, r: f'`l = {S.l} < r = {S.r}`：这一轮还有格子要扩展',
        'step += 1': '这一轮扩展出来的格子都要多掷一次：`step = {step}`',
        'for now in q[l : r]': '扩展这一轮的格子 `now = {now}`',
        'for next in range': lambda S, B, r: f'掷出 `{S.next - S.now}` 点：`next = {S.next}`',
        'if next <= n * n': lambda S, B, r: (f'`{S.next} ≤ {N * N}`，没出界' if S.next <= N * N else '出界'),
        'next = jump.get(next, next)': _cap_next,
        'if next not in used': lambda S, B, r: (f'`{S.next}` 没到过' if S.next not in S.used else f'`{S.next}` 已经到过 → 跳过'),
        'used.add(next)': '`{next}` 第一次到达 → 加入 used',
        'q.append(next)': '入队，下一轮从它出发',
        'if next == n * n': lambda S, B, r: (f'`{S.next}` 就是终点 `{N * N}`！' if S.next == N * N else f'`{S.next}` 不是终点'),
        'return step': '入队时就发现到达终点 → 返回 =={ret}==',
        'l, r = r, len(q)': '这一轮结束，`[l, r)` 移到新入队的部分',
    },
    cards=dict(
        one_liner='先把棋盘翻译成「编号 → 跳到哪」的字典，再从 1 开始一轮一轮 BFS',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`n × n` 棋盘从左下角开始==蛇形==编号 `1 ~ n²`，起点在 `1`',
                 '每回合掷骰到 `curr+1 ~ curr+6`；落在蛇/梯子起点就==传送一次==',
                 '求到达 `n²` 的最少掷骰次数，到不了返回 `-1`',
                 '本视频：3×3 棋盘，`3` 有梯子到 `9`，`5` 有蛇到 `2` → 答案 `1`'],
        quote='对于某一行某一列，若==当前行的奇偶性与n的奇偶性一致，那么说明当前行为逆序排列==，否则为顺序排列。……使用一个跳跃dict将其储存起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `i` 行下面有 `n−i−1` 整行：编号从 `(n−i−1)·n` 开始数',
              '行的奇偶性与 n 一致就逆序（`+ n − j`），否则顺序（`+ j + 1`）',
              'BFS：每轮 `step + 1`，`next` 先查 jump 再判 used；==入队时==发现终点就返回'],
        result='掷到 3 爬梯子直达 9：最少 `1` 次',
        summary=['时间 `O(n^2)`（每个格子入队一次，枚举 6 个点数），空间 `O(n^2)`',
                 '易错：最底下一行（i = n−1）一定是从左往右，奇偶性要和 n 比，不是和 0 比',
                 '技巧：入队时判断终点，比出队时判断少扩展一轮',
                 '对比灵神：不建字典，每次用 `divmod` 把编号换算回行列',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
