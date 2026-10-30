BOARD = [['E', 'E', 'E'], ['E', 'E', 'M']]


def _near(S, B, r):
    a, b = B.near_x, B.near_y
    if not (0 <= a < len(B.board) and 0 <= b < len(B.board[0])):
        return f'邻居 `({a},{b})` 越界，不算'
    if B.board[a][b] == 'M':
        return f'邻居 `({a},{b})` 是地雷 → `cnt` 变成 =={B.cnt + 1}=='
    return f'邻居 `({a},{b})` 不是地雷，`cnt` 不变'


def _enq(S, B, r):
    a, b = B.near_x, B.near_y
    if not (0 <= a < len(B.board) and 0 <= b < len(B.board[0])):
        return f'邻居 `({a},{b})` 越界，不入队'
    if B.used[a][b]:
        return f'邻居 `({a},{b})` 已经入过队了，不重复加入'
    if B.board[a][b] != 'E':
        return f'邻居 `({a},{b})` 不是未翻开的 `E`，不入队'
    return f'邻居 `({a},{b})` 是没翻开且没入过队的 `E` → ==入队==，`used` 标记'


def _col(S, i, j, v):
    if v == 'M':
        return 'red'
    if v == 'B':
        return 'green'
    if v in '12345678' and v != '':
        return 'cyan'
    return None


CONFIG = dict(
    num=529, title='扫雷游戏', difficulty='Medium', category='网格图',
    author='yiduobo', technique='BFS 逐格翻开',
    tags=['灵神核心路线', '灵神题单·网格图'],
    code='''
class Solution(object):
    def updateBoard(self, board, click):

        x = click[0]
        y = click[1]
        if board[x][y] == 'M':
            board[x][y] = 'X'
        else:
            dx = [0, 1, 1, 1, 0, -1, -1, -1]
            dy = [1, 1, 0, -1, -1, -1, 0, 1]
            used = [[False] * len(board[0]) for _ in range(len(board))]
            q = [(x, y)]
            l = 0
            r = 1
            while l < r:
                x, y = q[l]
                l += 1
                cnt = 0
                for index in range(8):
                    near_x = x + dx[index]
                    near_y = y + dy[index]
                    if near_x >= 0 and near_x < len(board) and near_y >= 0 and near_y < len(board[0]) and board[near_x][near_y] == 'M':
                        cnt += 1

                if cnt > 0:
                    board[x][y] = str(cnt)
                else:
                    board[x][y] = 'B'
                    for index in range(8):
                        near_x = x + dx[index]
                        near_y = y + dy[index]
                        if near_x >= 0 and near_x < len(board) and near_y >= 0 and near_y < len(board[0]) and not used[near_x][near_y] and board[near_x][near_y] == 'E':
                            q.append((near_x, near_y))
                            used[near_x][near_y] = True
                            r += 1

        return board
''',
    call=f'Solution().updateBoard({BOARD}, [0, 0])',
    expect=[['B', '1', 'E'], ['B', '1', 'M']],
    skip=['dx = [', 'dy = [', 'l = 0', 'r = 1', 'l += 1', 'for index in range(8)',
          'near_x = x', 'near_y = y', 'q.append', 'r += 1', 'used[near_x][near_y] = True'],
    max_steps=90,
    views=[
        dict(type='grid', var='board', label='board（蓝框 = 出队格，粉框 = 邻居）', cell=100, h=300,
             color=_col, cursors=[('x', 'y', 'blue'), ('near_x if _line in (22, 23, 32) else None', 'near_y', 'pink')]),
        dict(type='array', var=lambda S: [f'{a},{b}' for a, b in S['q']] if 'q' in S else None,
             label='q（暗 = 已出队，l 指向下一个出队的）', cell=80, pointers={'l': 'blue'},
             dim=lambda S, i, v: i < S.get('l', 0), h=190),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r'), ('cnt', 'cnt', 'yellow')],
    captions={
        'x = click[0]': '点击位置 `({click[0]},{click[1]})`',
        "if board[x][y] == 'M'": lambda S, B, r: ('点到地雷 → 直接爆炸' if S.board[S.x][S.y] == 'M' else f'`board[{S.x}][{S.y}]` 是 `{S.board[S.x][S.y]}`，不是地雷 → 开始 BFS 翻开'),
        'used = [[False]': '`used` 标记哪些格子已经入过队，避免重复加入',
        'q = [(x, y)]': '点击的格子作为 BFS 起点入队（`l` 队首，`r` 队尾）',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队列不空，继续翻开' if B.l < B.r else f'`l == r = {B.r}`：队列空了，翻开结束'),
        'x, y = q[l]': '出队 `({x},{y})`：先数周围八个格子里有几颗雷',
        'cnt = 0': '`cnt` 清零，准备统计地雷数',
        'and board[near_x][near_y] == \'M\'': _near,
        'cnt += 1': '又发现一颗雷：`cnt = {cnt}`',
        'if cnt > 0': lambda S, B, r: (f'周围有 `{S.cnt}` 颗雷 → 这格显示数字，不再往外扩' if S.cnt > 0 else '周围一颗雷都没有 → 标成空白 `B`，并把周围没翻开的格子加入队列'),
        'board[x][y] = str(cnt)': '`({x},{y})` 翻开，显示数字 `{board[x][y]}`',
        "board[x][y] = 'B'": '`({x},{y})` 翻开成空白 `B`',
        'and not used[near_x][near_y]': _enq,
        'return board': '队列空了，返回翻开后的 `board`',
    },
    cards=dict(
        one_liner='数周围八格的雷：有雷就显示数字，没雷就标空白并向外扩',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`E` 未翻开的空格，`M` 地雷，`B` 已翻开的空白，数字 = 周围地雷数',
                 '点击一个位置，按规则更新面板：点到雷变 `X`',
                 '否则翻开：周围有雷显示数字；没雷变 `B` 并继续翻开周围',
                 '示例：`[[E,E,E],[E,E,M]]`，点击 `(0,0)` → `[[B,1,E],[B,1,M]]`'],
        quote='若地雷数量大于0，那么将其标记为对应的数量，继续bfs。若地雷的数量等于0，那么将其标记为E，同时将周围八个格子中，没有被翻开且不在队列中的格子加入到队列尾部。',
        quote_src='—— yiduobo 题解原文（空白格在代码里标成 B）',
        idea=['出队一格，先数八邻域里的地雷数 `cnt`',
              '`cnt > 0`：写成数字，停在这里，不再扩散',
              '`cnt == 0`：写成 `B`，把没翻开且没入队的 `E` 邻居加入队尾',
              '`used` 防止同一个格子被重复入队'],
        summary=['时间 `O(mn)`：每格最多入队一次，每次看 8 个邻居',
                 '易错：只有 `cnt == 0` 才向外扩，数字格不扩',
                 '入队时就标 `used`，否则同一格会被多个邻居重复加入',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
