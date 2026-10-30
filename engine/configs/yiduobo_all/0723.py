BOARD = [[3, 2, 4, 1], [2, 3, 3, 1], [4, 1, 1, 1], [2, 4, 3, 1]]


def _color(S, i, j, v):
    rp = S.get('remove_pos')
    if rp and (i, j) in rp:
        return 'red'
    if v == 0:
        return None
    return None


CONFIG = dict(
    num=723, title='粉碎糖果', difficulty='Medium', category='模拟',
    author='yiduobo', technique='暴力模拟：标记、消除、下落',
    tags=[],
    code='''
class Solution(object):
    def candyCrush(self, board):

        m = len(board)
        n = len(board[0])

        while True:
            remove_pos = set()

            for i in range(m):
                for j in range(n):
                    if j + 2 < n and board[i][j] > 0 and board[i][j] == board[i][j + 1] == board[i][j + 2]:
                        remove_pos.add((i, j))
                        remove_pos.add((i, j + 1))
                        remove_pos.add((i, j + 2))

                    if i + 2 < m and board[i][j] > 0 and board[i][j] == board[i + 1][j] == board[i + 2][j]:
                        remove_pos.add((i, j))
                        remove_pos.add((i + 1, j))
                        remove_pos.add((i + 2, j))

            if len(remove_pos) == 0:
                break

            for x, y in remove_pos:
                board[x][y] = 0

            for j in range(n):
                p = m - 1
                for i in range(m - 1, -1, -1):
                    if board[i][j] > 0:
                        board[p][j] = board[i][j]
                        if p > i:
                            board[i][j] = 0
                        p -= 1
                
                for i in range(p, -1, -1):
                    board[i][j] = 0

        return board
''',
    call='Solution().candyCrush([[3,2,4,1],[2,3,3,1],[4,1,1,1],[2,4,3,1]])',
    expect=[[3, 0, 0, 0], [2, 2, 4, 0], [4, 3, 3, 0], [2, 4, 3, 0]],
    views=[
        dict(type='text', fn=lambda S: ('' if 'remove_pos' not in S else f"本轮待消除的格子：`{len(S['remove_pos'])}` 个（红色）")),
        dict(type='grid', var='board', h=420, cell=96,
             cursors=[('i', 'j', 'yellow', '(i,j)')],
             color=lambda S, i, j, v: 'red' if S.get('remove_pos') and (i, j) in S['remove_pos'] and S['board'][i][j] != 0 else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'blue'), ('p', 'p', 'pink'), ('待消除', 'len(remove_pos)', 'orange')],
    captions={
        'remove_pos = set()': '新的一轮：先清空 `remove_pos`，用来收集这一轮要消除的格子',
        'j + 2 < n and': lambda S, B, r: (f"检查 `({S.i},{S.j})` 向右三连：`{S.board[S.i][S.j]}`，不越界且非 0 且三格相等 → ==成立==" if S.j + 2 < S.n and S.board[S.i][S.j] > 0 and S.board[S.i][S.j] == S.board[S.i][S.j + 1] == S.board[S.i][S.j + 2]
                                          else f"`({S.i},{S.j})` 向右凑不出三连"),
        'i + 2 < m and': lambda S, B, r: (f"检查 `({S.i},{S.j})` 向下三连 → ==成立=="  if S.i + 2 < S.m and S.board[S.i][S.j] > 0 and S.board[S.i][S.j] == S.board[S.i + 1][S.j] == S.board[S.i + 2][S.j]
                                          else f"`({S.i},{S.j})` 向下凑不出三连"),
        'remove_pos.add((i, j))': '三连：把这格加入 `remove_pos`（共 {len(remove_pos)} 格）',
        'remove_pos.add((i, j + 1))': '同一行的第二格也加入',
        'remove_pos.add((i, j + 2))': '同一行的第三格也加入',
        'remove_pos.add((i + 1, j))': '同一列的第二格也加入',
        'remove_pos.add((i + 2, j))': '同一列的第三格也加入',
        'len(remove_pos) == 0': lambda S, B, r: ('这一轮没有任何可消除的 → ==局面稳定，结束==' if len(S.remove_pos) == 0 else f'这一轮标出 `{len(S.remove_pos)}` 格 → 先消除，再下落，然后重来'),
        'board[x][y] = 0': '消除：`({x},{y})` 置 0（==先标记后统一消除，三连相交的格子才不会漏==）',
        'p = m - 1': '第 `{j}` 列下落：`p` 指向下一个该放糖果的位置（从最底部开始）',
        'if board[i][j] > 0': lambda S, B, r: (f"`board[{S.i}][{S.j}] = {S.board[S.i][S.j]}` 是糖果 → 落到 `p = {S.p}`" if S.board[S.i][S.j] > 0 else f"`({S.i},{S.j})` 是空格，跳过"),
        'board[p][j] = board[i][j]': '把糖果放到第 `{p}` 行',
        'if p > i': lambda S, B, r: ('糖果确实下落了 → 原位置清零' if S.p > S.i else '没有移动，原位置保留'),
        34: '糖果落到了下面 → 原位置 `({i},{j})` 清零',
        'p -= 1': '`p` 上移一格 → {p}',
        38: '`p` 以上（第 `{i}` 行）没有糖果可落 → 补 0',
        'return board': '稳定了，返回最终的 `board`',
    },
    skip=['m = len', 'n = len'],
    max_steps=88,
    cards=dict(
        one_liner='数据范围小：每轮先找出所有三连，再统一消除、下落，直到稳定',
        complexity='时间 `O((mn)^2)`，空间 `O(mn)`',
        problem=['`board[i][j]` 是糖果种类，`0` 表示空格',
                 '横向或纵向 3 个以上相同糖果就消除；消除后上方糖果下落；重复直到稳定',
                 '本视频：`4×4` 棋盘，最终 `[[3,0,0,0],[2,2,4,0],[4,3,3,0],[2,4,3,0]]`'],
        quote='没有什么特别好的思路，不过好在本题的数据范围很小，可以直接暴力处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['用集合 `remove_pos` 先记下一轮里所有该消除的格子，再统一置 0',
              '下落：每列从下往上扫，非 0 的值依次放到 `p`，`p` 以上补 0',
              '某一轮 `remove_pos` 为空就结束；每轮最坏 `O(mn)`，最多 `O(mn)` 轮'],
        summary=['时间 `O((mn)^2)`，空间 `O(mn)`',
                 '必须==先标记后消除==：边找边消会破坏相交的三连（如 L 形、T 形）',
                 '下落时 `p > i` 才需要把原位置清零，否则会把刚放的糖果擦掉',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
