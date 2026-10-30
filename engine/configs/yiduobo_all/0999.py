BOARD = [list(r) for r in ['........', '...p....', '...p....', 'pp.R.pB.', '........', '...B....', '...p....', '........']]


def _color(S, i, j, v):
    if v == 'R':
        return 'blue'
    if v == 'p':
        return 'pink'
    if v == 'B':
        return 'purple'
    return None


def _stop(S, B, r):
    x, y = S.x, S.y
    d = '右下左上'[S.index]
    if not (0 <= x < 8 and 0 <= y < 8):
        return f'往{d}走到 `({x},{y})`：==出界==，探索结束'
    c = S.board[x][y]
    if c == '.':
        return f'往{d}走到 `({x},{y})` 是空格 → 继续往{d}'
    return f'往{d}走到 `({x},{y})` 是 `{c}` → ==碰到棋子==，停下'


def _end(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < 8 and 0 <= y < 8):
        return f'是因为出界停的，不是碰到 `p` → `res` 不变 = {S.res}'
    c = S.board[x][y]
    if c == 'p':
        return f'是因为碰到卒 `p` 停的 → 能吃，`res` = =={S.res + 1}=='
    return f'碰到的是象 `B`，吃不了 → `res` 不变 = {S.res}'


CONFIG = dict(
    num=999, title='可以被一步捕获的棋子数', difficulty='Easy', category='模拟',
    author='yiduobo', technique='从 R 出发向四个方向探索',
    tags=[],
    code='''
class Solution(object):
    def numRookCaptures(self, board):

        for i in range(8):
            flag = False
            for j in range(8):
                if board[i][j] == 'R':
                    flag = True
                    break
            if flag:
                break
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        res = 0
        for index in range(4):
            x = i + dx[index]
            y = j + dy[index]
            while x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == '.':
                x += dx[index]
                y += dy[index]
            
            if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == 'p':
                res += 1
        
        return res
''',
    call=f'Solution().numRookCaptures({BOARD})',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: ('白车在 `(%d,%d)`，现在探索第 %d 个方向：==%s==' % (S['i'], S['j'], S['index'] + 1, '右下左上'[S['index']])) if 'index' in S else ('逐行逐列扫描，找到 `R`（蓝）' if 'dx' not in S else '找到了车 `(%d,%d)`；`dx, dy` 给出右、下、左、上四个方向' % (S['i'], S['j']))),
        dict(type='grid', var='board', cursors=[('x', 'y', 'yellow', '(x,y)')], color=_color, h=520, cell=62),
    ],
    watch=['i', 'j', 'index', 'x', 'y', ('res', 'res', 'green')],
    skip=['for j in range(8)', "if board[i][j] == 'R'", 'flag = False', 'if flag', 'break', 'dx = [', 'dy = ['],
    captions={
        'for i in range(8)': '按行扫描：第 `{i}` 行',
        'flag = True': '`board[{i}][{j}]` 就是 `R`，==车的位置找到了==，`flag` 通知外层循环也退出',
        'res = 0': '`res` 统计能吃到的卒数',
        'for index in range(4)': lambda S, B, r: ('四个方向都试完了' if 'index' in B and S.index == B.index else f'换方向：`index = {S.index}`，`(dx, dy) = ({S.dx[S.index]}, {S.dy[S.index]})`'),
        'x = i + dx[index]': '`x = i + dx[index]` = {x}：行号往 dx 方向挪一格',
        'y = j + dy[index]': '`y = j + dy[index]` = {y}：从车旁边第一格出发 `({x}, {y})`',
        'while x >= 0': _stop,
        'x += dx[index]': '空格不挡路，`x += dx[index]` → {x}',
        'y += dy[index]': '`y += dy[index]` → {y}，来到 `({x}, {y})`，回头再判断',
        "board[x][y] == 'p'": _end,
        'res += 1': '`res` = =={res}==',
        'return res': '四个方向探索完，能吃 `{res}` 个卒',
    },
    cards=dict(
        one_liner='从 R 出发，四个方向走到头，看是怎么停下的',
        complexity='时间 `O(1)`（棋盘固定 8×8），空间 `O(1)`',
        problem=['`8×8` 棋盘上有一个白车 `R`，可能有白象 `B`、黑卒 `p`',
                 '车只能直走，不能穿过棋子；求一步内能吃掉的卒数',
                 '本视频示例：右、上方向能吃到卒，下方被象挡 → `3`'],
        quote='比较基础的题目，从R的位置开始向四个方向探索，直到走出边界或者碰到棋子。若某个方向上是因为碰到棋子p结束，那么就将答案加1。',
        quote_src='—— yiduobo 题解原文',
        idea=['两层循环找 `R`：找到后用 `flag` 连续 `break` 两层，`i, j` 保持为车的位置',
              '`dx`、`dy` 数组表示四个方向，每个方向先迈一步再 `while` 走',
              '循环结束时看停下的格子：是 `p` 才加一，出界或象都不加'],
        summary=['时间 `O(1)`，扫描最多 64 格，每个方向最多 8 步',
                 '易错：`while` 之后必须再判一次边界，才能访问 `board[x][y]`',
                 '`flag` 是为了跳出两层循环，此时 `i, j` 恰好是车的坐标',
                 '对比灵神：灵神用 `enumerate` 扫描，yiduobo 用 `flag + break`，方向表也不同'],
    ),
)
