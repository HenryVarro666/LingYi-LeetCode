G = [[0, 0, 1, 0], [0, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0]]


def _color(S, i, j, v):
    if 'nowx' in S and 'h_flag' in S:
        x, y, h = S['nowx'], S['nowy'], S['h_flag']
        body = (x, y - 1) if h else (x - 1, y)
        if (i, j) == (x, y):
            return 'blue'
        if (i, j) == body:
            return 'cyan'
    if 'used_h' in S and (S['used_h'][i][j] or S['used_v'][i][j]):
        return 'green'
    return None


def _can(S, B, r):
    if S.h_flag:
        return None
    return None


def _state(S):
    if 'nowx' not in S:
        return ''
    h = '水平' if S['h_flag'] else '竖直'
    return f"正在扩展：蛇头 `({S['nowx']},{S['nowy']})`，==%s==；已走 `{S['step']}` 步" % h


CONFIG = dict(
    num=1210, title='穿过迷宫的最少移动次数', difficulty='Hard', category='网格图',
    author='yiduobo', technique='BFS · 蛇头坐标 + 水平/竖直',
    tags=['网格图 BFS', '难度分 2022'],
    code='''
class Solution(object):
    def minimumMoves(self, grid):

        n = len(grid)
        used_v = [[False] * n for _ in range(n)]
        used_h = [[False] * n for _ in range(n)]
        used_h[0][1] = True
        q = [[0, 1, 1]]
        l = 0
        r = 1
        step = 0
        while l < r:
            step += 1
            for nowx, nowy, h_flag in q[l : r]:
                l += 1
                if h_flag:
                    if nowy + 1 < n and grid[nowx][nowy + 1] == 0 and not used_h[nowx][nowy + 1]:
                        q.append([nowx, nowy + 1, h_flag])
                        used_h[nowx][nowy + 1] = True
                    if nowx + 1 < n and grid[nowx + 1][nowy] == 0 and grid[nowx + 1][nowy - 1] == 0:
                        if not used_h[nowx + 1][nowy]:
                            q.append([nowx + 1, nowy, h_flag])
                            used_h[nowx + 1][nowy] = True
                        if not used_v[nowx + 1][nowy - 1]:
                            q.append([nowx + 1, nowy - 1, 1 - h_flag])
                            used_v[nowx + 1][nowy - 1] = True
                    if used_h[n - 1][n - 1]:
                        return step
                else:
                    if nowx + 1 < n and grid[nowx + 1][nowy] == 0 and not used_v[nowx + 1][nowy]:
                        q.append([nowx + 1, nowy, h_flag])
                        used_v[nowx + 1][nowy] = True
                    if nowy + 1 < n and grid[nowx][nowy + 1] == 0 and grid[nowx - 1][nowy + 1] == 0:
                        if not used_v[nowx][nowy + 1]:
                            q.append([nowx, nowy + 1, h_flag])
                            used_v[nowx][nowy + 1] = True
                        if not used_h[nowx - 1][nowy + 1]:
                            q.append([nowx - 1, nowy + 1, 1 - h_flag])
                            used_h[nowx - 1][nowy + 1] = True

            l, r = r, len(q)

        return -1
''',
    call=f'Solution().minimumMoves({G})',
    expect=5,
    skip=['n = len', 'l = 0', 'r = 1', 'l += 1', 'step = 0', 'used_v = [[', 'used_h = [[', 'if h_flag:', 'else:'],
    max_steps=48,
    views=[
        dict(type='grid', var='grid', label='grid（1 = 障碍；蓝 = 蛇头，青 = 蛇尾；绿 = 蛇头到过的格子）', cell=88, h=370, color=_color),
        dict(type='text', fn=_state, size=28),
        dict(type='array', var=lambda S: [f"{a}{b}{'H' if c else 'V'}" for a, b, c in S['q']] if 'q' in S else None,
             label='q：蛇头 x y 加方向（H 水平 / V 竖直），暗 = 已处理', cell=76, h=150,
             dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('step', 'step', 'green'), ('l', 'l', 'blue'), ('r', 'r'), ('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue')],
    captions={
        'used_h[0][1] = True': '蛇头在 `(0,1)`、水平：==水平和竖直各用一张 used 表去重==，同一蛇头位置方向不同是不同状态',
        'q = [[0, 1, 1]]': '起点入队 `[x, y, h_flag]` = `[0, 1, 1]`：蛇头 `(0,1)`，`h_flag = 1` 表示水平',
        'while l < r': lambda S, B, r: (f'这一轮有 `{B.r - B.l}` 个状态 `[l, r) = [{B.l}, {B.r})`' if B.l < B.r else '队列空了：到不了 → 返回 -1'),
        'step += 1': '新一轮，走一步：`step` = {step}',
        'for nowx, nowy, h_flag': lambda S, B, r: f'取出状态：蛇头 `({S.nowx},{S.nowy})`，' + ('==水平==，蛇尾在左边' if S.h_flag else '==竖直==，蛇尾在上边'),
        'if nowy + 1 < n and grid[nowx][nowy + 1] == 0 and not used_h': lambda S, B, r: (
            f'水平向右：新蛇头 `({S.nowx},{S.nowy+1})` ' + ('出界' if S.nowy + 1 >= S.n else '是障碍' if S.grid[S.nowx][S.nowy + 1] else '已到过' if S.used_h[S.nowx][S.nowy + 1] else '可走') + ('，==不行==' if (S.nowy + 1 >= S.n or S.grid[S.nowx][S.nowy + 1] or S.used_h[S.nowx][S.nowy + 1]) else '，==入队==')),
        'q.append([nowx, nowy + 1, h_flag])': '向右一格入队 `({nowx},{nowy_p})`'.replace('{nowy_p}', '{nowy + 1}'),
        'if nowx + 1 < n and grid[nowx + 1][nowy] == 0 and grid[nowx + 1][nowy - 1] == 0': lambda S, B, r: (
            '向下一格：蛇头下 `(%d,%d)` 和蛇尾下 `(%d,%d)` ' % (S.nowx + 1, S.nowy, S.nowx + 1, S.nowy - 1) + (
                '都是空的 → ==能下移，也能顺时针旋转==' if (S.nowx + 1 < S.n and S.grid[S.nowx + 1][S.nowy] == 0 and S.grid[S.nowx + 1][S.nowy - 1] == 0) else '有障碍或出界 → 不能下移也不能旋转')),
        'if not used_h[nowx + 1][nowy]': '下移后仍水平，蛇头 `({nowx_p},{nowy})`：没到过才入队'.replace('{nowx_p}', '{nowx + 1}'),
        'if not used_v[nowx + 1][nowy - 1]': '顺时针旋转：蛇尾不动，蛇头从 `({nowx},{nowy})` 变到 `({nowx + 1},{nowy - 1})` 的竖直状态，没到过才入队',
        'if used_h[n - 1][n - 1]': lambda S, B, r: ('水平蛇头到了右下角 `(n-1,n-1)` → ==终点==' if S.used_h[S.n - 1][S.n - 1] else '右下角水平状态还没到过'),
        'if nowx + 1 < n and grid[nowx + 1][nowy] == 0 and not used_v': lambda S, B, r: (
            f'竖直向下：新蛇头 `({S.nowx+1},{S.nowy})` ' + ('出界' if S.nowx + 1 >= S.n else '是障碍' if S.grid[S.nowx + 1][S.nowy] else '已到过' if S.used_v[S.nowx + 1][S.nowy] else '可走')),
        'if nowy + 1 < n and grid[nowx][nowy + 1] == 0 and grid[nowx - 1][nowy + 1] == 0': lambda S, B, r: (
            '向右一列：蛇头右 `(%d,%d)` 和蛇尾右 `(%d,%d)` ' % (S.nowx, S.nowy + 1, S.nowx - 1, S.nowy + 1) + (
                '都是空的 → ==能右移，也能逆时针旋转==' if (S.nowy + 1 < S.n and S.grid[S.nowx][S.nowy + 1] == 0 and S.grid[S.nowx - 1][S.nowy + 1] == 0) else '有障碍或出界 → 不能右移也不能旋转')),
        'if not used_v[nowx][nowy + 1]': '右移后仍竖直，蛇头 `({nowx},{nowy + 1})`：没到过才入队',
        'if not used_h[nowx - 1][nowy + 1]': '逆时针旋转：蛇头变成 `({nowx - 1},{nowy + 1})` 的水平状态，没到过才入队',
        'l, r = r, len(q)': '一轮结束：`[l, r)` 切到新入队的状态 `[{l}, {r})`',
        'return step': '水平蛇头到了右下角，最少 ==`{step}`== 步',
        'return -1': '到不了 → `-1`',
    },
    cards=dict(
        one_liner='用蛇头坐标加水平/竖直标志做 BFS，两种方向各去重',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`n×n` 迷宫里长度 2 的蛇，从左上角水平出发，要到右下角（水平）',
                 '可以右移、下移；水平时可顺时针转，竖直时可逆时针转；不能压障碍',
                 '求最少移动次数，到不了返回 `-1`',
                 '本视频用 4×4 的小迷宫演示'],
        quote='蛇的状态可以是水平也可以是竖直，我们需要使用三元组(x, y, h_flag)来表示蛇当前的状态，表示蛇的头在(x, y)。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态 `(x, y, h_flag)`：蛇头位置加方向，水平时蛇尾在左，竖直时蛇尾在上',
              '水平：右移、下移（要检查蛇头、蛇尾下方都空）、旋转到竖直',
              '竖直：下移、右移（检查右侧两格）、旋转回水平；`used_h`、`used_v` 分开去重'],
        summary=['时间、空间都是 `O(n²)`',
                 '易错：下移、旋转都要检查蛇头和蛇尾下方（或右侧）两格都为空',
                 '`used_h`、`used_v` 必须分开，同一蛇头位置的两种方向是不同状态',
                 '对比灵神：灵神用蛇尾坐标 + 三个三元组统一六种移动，yiduobo 分水平、竖直逐一写',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改，仅删去空行里的空格'],
    ),
)
