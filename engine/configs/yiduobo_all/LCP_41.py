BOARD = ['XO.', 'OOX', '.XO']


def _show(S):
    t = S.get('tmp') if isinstance(S.get('tmp'), list) else S.get('board_matrix')
    if not isinstance(t, list):
        return [list(r) for r in BOARD]
    return [['.XO'[v] for v in r] for r in t]


def _color(S, i, j, v):
    return {'X': 'blue', 'O': 'pink'}.get(v)


def _q(S):
    q = S.get('q')
    return [f'{a},{b}' for a, b in q] if isinstance(q, list) else None


CONFIG = dict(
    num='LCP 41', title='黑白翻转棋', difficulty='Medium', category='网格图',
    author='yiduobo', technique='枚举落子点 + BFS 模拟连锁翻转',
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
    call=f'Solution().flipChess({BOARD})',
    expect=2,
    max_steps=56,
    skip=['res = 0', 'n = len', 'm = len', 'dx = [', 'dy = [', 'board_matrix = [[0]', 'for i in range', 'for j in range',
          'board_matrix[i][j] =', 'if chessboard', 'elif chessboard', 'else:', 'head = 0', 'tail = 1', 'vis = set',
          'for x, y in q', 'tmp[x][y] = 1', 'for nowx', 'for index in range(8)', 'x = nowx', 'y = nowy',
          'black_flag = False', 'x += dx', 'y += dy', 'tx = nowx', 'ty = nowy', 'tx += dx', 'ty += dy',
          'q.append', 'vis.add', 'while x >=', 'while tx', 'if tmp[x][y] == 0', 'elif tmp[x][y] == 1',
          'black_flag = True', 'break', 'if (tx, ty) not in vis'],
    views=[
        dict(type='grid', var=_show, label='棋盘（蓝 X = 黑棋，粉 O = 白棋；黄框 = 本次落子，橙框 = 正在扩展的黑子）',
             cell=110, h=420, color=_color,
             cursors=[('i', 'j', 'yellow'), ('nowx', 'nowy', 'orange')]),
        dict(type='array', var=_q, label='q：本次落子后被翻转的棋子（q[0] 是落子点）', cell=80, h=170),
    ],
    watch=[('落子 i,j', "(i, j) if 'i' in locals() else ''", 'yellow'), ('head', 'head', 'blue'), ('tail', 'tail', 'pink'),
           ('res', 'res', 'green')],
    captions={
        'if board_matrix[i][j] == 0': lambda S, B, r: (
            f'`({S.i},{S.j})` 是空位 → ==试着在这里落黑子=='
            if S.board_matrix[S.i][S.j] == 0 else f'`({S.i},{S.j})` 已有棋子，跳过'),
        'tmp = [[board_matrix': '复制一份棋盘 `tmp`，在副本上模拟，不破坏原棋盘',
        'q = [[i, j]]': '落子点 `({i},{j})` 入队，BFS 开始：队列里的每个黑子都要往 8 个方向找「被夹住的白子」',
        'if black_flag': lambda S, B, r: (
            (f'沿方向 `({B.dx[B.index]},{B.dy[B.index]})` 走到黑子 `({B.x},{B.y})`，中间 `{max(abs(B.x - B.nowx), abs(B.y - B.nowy)) - 1}` 枚白子全被夹住 → ==翻转并入队==，它们下一轮也是黑子'
             if max(abs(B.x - B.nowx), abs(B.y - B.nowy)) > 1 else
             f'方向 `({B.dx[B.index]},{B.dy[B.index]})` 紧挨着黑子，中间没有白子 → 无可翻')
            if B.black_flag else
            f'方向 `({B.dx[B.index]},{B.dy[B.index]})`：先遇到空格或出界 → 不翻'),
        'head, tail = tail, len(q)': lambda S, B, r: (
            f'这一层处理完：新翻转的 `{S.tail - S.head}` 枚白子变成黑子，==继续作为新的黑子扩展=='
            if S.tail > S.head else '没有新翻转的棋子了，BFS 结束'),
        'res = max(res, len(q) - 1)': '落在 `({i},{j})` 共翻转 `{len(q) - 1}` 枚白子（q 去掉落子点）：`res = max({B.res}, {len(q) - 1}) = {res}`',
        'return res': '最多翻转 `{res}` 枚白棋',
    },
    cards=dict(
        one_liner='棋盘很小：枚举落子点，再用 BFS 模拟连锁翻转',
        complexity='时间 `O((nm)² · 8)` 量级，空间 `O(nm)`',
        problem=['棋盘上 `X` 黑、`O` 白、`.` 空；黑子落下后，与另一黑子在行、列或对角线上==夹住==的白子（中间无空格）都会翻成黑',
                 '翻转后新黑子还能继续夹住别的白子，==连锁翻转==',
                 '求放一枚黑子最多翻转多少白子',
                 '示例：`[".X.", ".O.", "XO."]` → `2`；本视频：`["XO.","OOX",".XO"]` → `2`'],
        quote='完全可以枚举放置第一个黑子的位置，然后从这个位置开始进行bfs，模拟整个棋盘的变化过程。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每个空位：复制棋盘，落子，然后 BFS',
              'BFS 每一轮：当前黑子往 8 个方向走，直到碰到另一个黑子',
              '中途遇到空格或出界，该方向不翻；否则中间所有白子入队，下一轮它们也是黑子'],
        summary=['时间：空位数 ≤ `nm`，每个空位 BFS 最多处理 `nm` 个黑子 × 8 方向 × 长度 `≤ max(n,m)`',
                 '`vis` 防止同一枚白子重复入队；答案是 `len(q) - 1`（不含落子点本身）',
                 '易错：遇到空格要 `break`，不能把空格后面的棋子算进去',
                 '原文为 Python 2 风格，代码在 Python 3 下可直接运行，未做修改'],
    ),
)
