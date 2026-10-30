BOARD = [['.', '.', '.', 'B', '.'],
         ['.', '.', 'W', 'B', '.'],
         ['B', 'W', 'W', '.', '.'],
         ['.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.']]


def _col(S, i, j, v):
    if v == 'B':
        return 'orange'
    if v == 'W':
        return 'cyan'
    return None


def _scan(S, B, r):
    x, y = S.nowx, S.nowy
    if not (0 <= x < S.m and 0 <= y < S.n):
        return '`(%d,%d)` 已出界 → 循环结束，这个方向没有同色端点' % (x, y)
    return '`(%d,%d)` 在棋盘内，继续扫描' % (x, y)


def _chk(S, B, r):
    c = S.board[S.nowx][S.nowy]
    if c == '.':
        return f'`({S.nowx},{S.nowy})` 是空格 → 停止，不可能成线'
    if c == S.color:
        return f'`({S.nowx},{S.nowy})` 与 color 同色 → 停止，==可能==成线（要看是否紧挨起点）'
    return f'`({S.nowx},{S.nowy})` 是异色，继续延伸'


CONFIG = dict(
    num=1958, title='检查操作是否合法', difficulty='Medium', category='模拟',
    author='yiduobo', technique='八方向延伸 + 判断是否相邻',
    tags=[],
    code='''
class Solution(object):
    def checkMove(self, board, rMove, cMove, color):

        dx = [-1, -1, 0, 1, 1, 1, 0, -1]
        dy = [0, 1, 1, 1, 0, -1, -1, -1]
        m = len(board)
        n = len(board[0])
        for index in range(8):
            nowx, nowy = rMove + dx[index], cMove + dy[index]
            flag = False
            while nowx >= 0 and nowx < m and nowy >= 0 and nowy < n:
                if board[nowx][nowy] == '.':
                    break
                if board[nowx][nowy] == color:
                    flag = True
                    break
                nowx += dx[index]
                nowy += dy[index]
            
            if flag and ((nowx != rMove + dx[index]) or (nowy != cMove + dy[index])):
                return True
        
        return False
''',
    call=f"Solution().checkMove({BOARD}, 2, 3, 'B')",
    expect=True,
    views=[
        dict(type='grid', var='board', h=420, cell=96, color=_col,
             cursors=[('rMove', 'cMove', 'yellow', '落子'), ('nowx', 'nowy', 'pink', '探')]),
        dict(type='text', fn=lambda S: (f"方向 {S['index']}：`({S['dx'][S['index']]},{S['dy'][S['index']]})`，flag = `{S['flag']}`" if 'flag' in S else '')),
    ],
    watch=['index', 'nowx', 'nowy', 'flag', 'color'],
    captions={
        'dx = [': '`dx`、`dy` 两个数组按顺序列出八个方向',
        'dy = [': '八个方向：上、右上、右、右下、下、左下、左、左上',
        'm = len': '行数 `m = {m}`',
        'n = len': '列数 `n = {n}`',
        'for index in range(8)': '第 `{index}` 个方向：`({dx[index]}, {dy[index]})`',
        'nowx, nowy =': '从落子点相邻的一格出发：`({nowx}, {nowy})`',
        'flag = False': '`flag` 记录这个方向是否停在同色格上',
        'while nowx >= 0': _scan,
        "== '.'": _chk,
        '== color:': _chk,
        'flag = True': '遇到同色 → `flag = True`，停止延伸',
        'break': '停止延伸',
        'nowx += dx': '沿方向前进：`nowx` → {nowx}',
        'nowy += dy': '沿方向前进：`nowy` → {nowy}',
        'if flag and': lambda S, B, r: (('`flag = False`：没停在同色格上 → 这个方向不成立') if not S.flag else ('停点 `(%d,%d)` 就是紧挨起点的格子 → 中间没有异色格，不成立' if (S.nowx == S.rMove + S.dx[S.index] and S.nowy == S.cMove + S.dy[S.index]) else '停点 `(%d,%d)` 不紧挨起点（距离 ≥ 2）→ 中间有异色格 → ==好线段==') % (S.nowx, S.nowy)),
        'return True': '存在好线段 → 返回 ==True==',
        'return False': '八个方向都没有 → 返回 False',
    },
    cards=dict(
        one_liner='向八个方向延伸，停在同色且不紧挨起点才算好线段',
        complexity='时间 `O(m+n)`，空间 `O(1)`',
        problem=['空格涂色 `color` 后，要成为某条好线段的端点',
                 '好线段：≥3 格，两端同色，中间全是异色，无空格',
                 '本视频用 5×5 小棋盘：落子 `(2,3)` 涂黑 → `true`；上方有紧挨的同色 `B`，不算'],
        quote='只有抵达同色色块这种情况才可能形成好线段。另一方面，好线段需要两端同色快之间必须存在一个异色色块，因此只需要判断停止的色块位置是否与起始位置相邻。',
        quote_src='—— yiduobo 题解原文',
        idea=['从落子点向八个方向延伸，遇到边界、空格、同色就停',
              '只有停在同色格上才可能成线',
              '再检查停点是否紧挨起点：紧挨说明中间没有异色格'],
        summary=['时间 `O(m+n)`，空间 `O(1)`',
                 '易错点：停在紧挨起点的同色格不算（中间没有异色）',
                 '易错点：遇到空格要立刻停止',
                 '原文为 Python 2 写法，代码无需改动（仅用 range）；对比灵神：灵神先要求第一步异色，yiduobo 最后比较停点位置'],
    ),
)
