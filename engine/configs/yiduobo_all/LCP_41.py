BOARD = ["OO.", "XOO", ".XX"]
CH = '.XO'


def _board(S):
    inner = S.get('_inner', {})
    if 'tmp' in S and S.get('tmp') is not None and 'tmp' in inner:
        return [[CH[v] for v in r] for r in S['tmp']]
    return [[CH[v] for v in r] for r in S['board_matrix']]


def _color(S, i, j, v):
    if v == 'X' and BOARD[i][j] == 'O':
        return 'orange'
    if v == 'X' and BOARD[i][j] == '.':
        return 'purple'
    return None


def _info(S):
    if 'q' in S and 'head' in S:
        return f"队列里一共 ==`{len(S['q'])}`== 枚：1 枚新放的黑棋 + 被翻转的 ==`{len(S['q']) - 1}`== 枚白棋"
    if 'res' in S:
        return f"目前最好成绩 `res = {S['res']}`"
    return ''


CONFIG = dict(
    num='LCP 41', title='黑白翻转棋', difficulty='Medium', category='模拟',
    author='yiduobo', technique='枚举落子点 · BFS 模拟连锁翻转',
    tags=[],
    code='''
class Solution(object):
    def flipChess(self, chessboard):

        res = 0
        n = len(chessboard)
        m = len(chessboard[0])
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]

        board_matrix = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if chessboard[i][j] == '.':
                    board_matrix[i][j] = 0
                elif chessboard[i][j] == 'X':
                    board_matrix[i][j] = 1
                else:
                    board_matrix[i][j] = 2

        res = 0
        for i in range(n):
            for j in range(m):
                if board_matrix[i][j] == 0:
                    tmp = [[board_matrix[x][y] for y in range(m)] for x in range(n)]
                    q = [[i, j]]
                    head = 0
                    tail = 1
                    vis = set([(i, j)])
                    while head < tail:
                        for x, y in q[head : tail]:
                            tmp[x][y] = 1
                        for nowx, nowy in q[head : tail]:
                            for index in range(8):
                                x = nowx + dx[index]
                                y = nowy + dy[index]
                                black_flag = False
                                while x >= 0 and x < n and y >= 0 and y < m:
                                    if tmp[x][y] == 0:
                                        break
                                    elif tmp[x][y] == 1:
                                        black_flag = True
                                        break
                                    else:
                                        x += dx[index]
                                        y += dy[index]
                                
                                if black_flag:
                                    tx = nowx + dx[index]
                                    ty = nowy + dy[index]
                                    while tx != x or ty != y:
                                        if (tx, ty) not in vis:
                                            q.append([tx, ty])
                                            vis.add((tx, ty))
                                        tx += dx[index]
                                        ty += dy[index]
                                
                        
                        head, tail = tail, len(q)

                    res = max(res, len(q) - 1)
        
        return res
''',
    call=f'Solution().flipChess({BOARD!r})',
    expect=2,
    skip=['n = len', 'm = len', 'dx = [', 'dy = [', 'board_matrix = [[0]', 'for i in range(n)', 'for j in range(m)',
          'board_matrix[i][j] =', 'if chessboard[i][j]', 'elif chessboard[i][j]', 'else:', 'for index in range(8)',
          'x = nowx', 'y = nowy', 'black_flag = False', 'while x >= 0', 'if tmp[x][y] == 0', 'elif tmp[x][y] == 1',
          'black_flag = True', 'break', 'x += dx', 'y += dy', 'while tx != x', 'tx += dx', 'ty += dy',
          'for nowx, nowy', 'for x, y in q[head', 'tmp[x][y] = 1', 'vis = set', 'head = 0', 'tail = 1'],
    views=[
        dict(type='grid', var=_board,
             label='棋盘（紫 = 新放的黑棋，橙 = 被翻转的白棋，蓝框 = 当前出队的黑棋，粉框 = 要翻转的格）', cell=90, h=300,
             color=_color,
             cursors=[('nowx', 'nowy', 'blue'), ('tx if _line in (38, 39, 40, 41, 42, 43) else None', 'ty', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S and S.get('q') else None,
             label='q（BFS 队列：新变黑的棋子；暗 = 已处理，head 指向下一轮起点）', cell=80,
             pointers={'head': 'blue', 'tail': 'pink'}, dim=lambda S, i, v: i < S.get('head', 0), h=240),
        dict(type='text', h=70, size=28, fn=_info),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('res', 'res', 'green')],
    max_steps=64,
    captions={
        4: '`res` 记录所有落子点里最多能翻几枚白棋；后面先把棋盘转成数字：空 0，黑 1，白 2',
        20: '棋盘转好了（看下面的棋盘）；`res` 清零，开始枚举每个空位作为第一枚黑棋的落点',
        'if board_matrix[i][j] == 0': lambda S, B, r: (f'`({S.i},{S.j})` 是空位 → ==在这里放第一枚黑棋==，开始 BFS' if S.board_matrix[S.i][S.j] == 0
                                                        else f'`({S.i},{S.j})` 已有棋子，跳过'),
        'tmp = [[': '复制一份棋盘 `tmp`，在副本上模拟，不影响下一个落子点',
        'q = [[i, j]]': '新放的黑棋 `({i},{j})` 入队：队列里装的都是“变黑的棋子”',
        'while head < tail': lambda S, B, r: (f'`head = {S.head} < tail = {S.tail}`：这一轮有 {S.tail - S.head} 枚新黑棋要向 8 个方向扩散'
                                              if S.head < S.tail else f'`head = {S.head} == tail`：没有新翻转的棋子了，这个落子点结束'),
        'if black_flag': lambda S, B, r: (
            (f'方向 `({S.dx[S.index]},{S.dy[S.index]})`：`({S.x},{S.y})` 紧挨着就是黑棋，中间没有白棋 → 没有可翻的'
             if (S.x, S.y) == (S.nowx + S.dx[S.index], S.nowy + S.dy[S.index]) else
             f'方向 `({S.dx[S.index]},{S.dy[S.index]})`：从 `({S.nowx},{S.nowy})` 走到 `({S.x},{S.y})` 遇到黑棋 → ==中间的白棋全部变色==')
            if S.black_flag else
            f'方向 `({S.dx[S.index]},{S.dy[S.index]})`：先碰到空格或边界，夹不住 → 不翻'),
        'tx = nowx': '从 `({nowx},{nowy})` 出发，把到 `({x},{y})` 之间的白棋依次入队',
        'if (tx, ty) not in vis': lambda S, B, r: (f'`({S.tx},{S.ty})` 还没加过 → 加入队列' if (S.tx, S.ty) not in S.vis
                                                   else f'`({S.tx},{S.ty})` 已经在队列里，不重复加'),
        'q.append': '`({tx},{ty})` 的白棋被翻转，入队：下一轮它也会向外扩散，==连锁翻转==',
        'vis.add': '记入 `vis`，避免重复',
        'head, tail = tail, len(q)': '这一轮处理完：新入队的 `{tail - head}` 枚成为下一轮 → `head = {head}`，`tail = {tail}`',
        'res = max(res, len(q) - 1)': lambda S, B, r: (f'队列里共 `{len(S.q)}` 枚，扣掉新放的黑棋，翻转了 `{len(S.q) - 1}` 枚；`res = {S.res}`'),
        'return res': '所有空位都试过，最多翻 `{res}` 枚',
    },
    cards=dict(
        one_liner='枚举落子点，再用 BFS 向 8 个方向扩散：夹住的白棋入队，变黑后继续扩散',
        complexity='时间约 `O((nm)^2 · max(n,m))`，空间 `O(nm)`',
        problem=['`n×m` 棋盘，黑 `X`、白 `O`、空位 `.`',
                 '落一枚黑棋，被黑棋夹住且中间无空位的白棋翻成黑，可连锁',
                 '本视频：`["OO.","XOO",".XX"]` → `2`'],
        quote='题目的数据规模很小，那么完全可以枚举放置第一个黑子的位置，然后从这个位置开始进行bfs，模拟整个棋盘的变化过程。',
        quote_src='—— yiduobo 题解原文',
        idea=['每一轮 BFS：对每枚新变黑的棋，沿 8 个方向一直走',
              '先遇到黑棋（中间没有空位）→ 两者之间的白棋全部变黑并入队',
              '先遇到空位或边界 → 这个方向什么也不翻；队列空了就结束'],
        summary=['`len(q) - 1` 就是翻转的白棋数（扣掉新放的那枚）',
                 '用 `vis` 避免同一枚白棋被重复入队',
                 '易错：只有「中间全是白棋、另一端是黑棋」才翻转，碰到空位要停',
                 '对比灵神：yiduobo 用 BFS 只处理新变黑的棋；灵神反复全盘扫描白棋直到稳定',
                 '代码未做修改（原文已可在 Python 3 运行）'],
    ),
)
