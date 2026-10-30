G = [[0, 0, 1, 0], [0, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0]]


def _body(S, x, y, s):
    return [(x, y), (x + s, y + (s ^ 1))]


def _color(S, i, j, v):
    if 'X' not in S:
        return None
    if 'x' in S and S['_line'] >= 12:
        if (i, j) in _body(S, S['x'], S['y'], S['s']):
            return 'pink'
    if (i, j) in _body(S, S['X'], S['Y'], S['S']):
        return 'blue'
    return None


def _check(S, B, ret):
    x, y, s, x2, y2 = S.x, S.y, S.s, S.x2, S.y2
    n = S.n
    if x2 >= n or y2 >= n:
        return f'蛇头 `({x2},{y2})` 出界 → 不行'
    if (x, y, s) in S.vis:
        return f'状态 `({x},{y},{s})` 访问过 → 不行'
    if S.g[x][y] or S.g[x2][y2]:
        return f'蛇身 `({x},{y})`、`({x2},{y2})` 压到障碍 → 不行'
    if s != S.S and S.g[x + 1][y + 1]:
        return f'旋转还要 `({x+1},{y+1})` 为空，但它是障碍 → 不行'
    return f'蛇尾 `({x},{y})` 蛇头 `({x2},{y2})`：不出界、没访问过、没压障碍 → ==这一步合法=='


CONFIG = dict(
    num=1210, title='穿过迷宫的最少移动次数', difficulty='Hard', category='网格图',
    author='灵茶山艾府', technique='BFS · 三元组统一六种移动',
    tags=['网格图 BFS', '难度分 2022'],
    code='''
class Solution:
    def minimumMoves(self, g: List[List[int]]) -> int:
        step, n = 1, len(g)
        vis = {(0, 0, 0)}
        q = [(0, 0, 0)]  # 初始位置
        while q:
            tmp = q
            q = []
            for X, Y, S in tmp:
                for t in (X + 1, Y, S), (X, Y + 1, S), (X, Y, S ^ 1):  # 直接把移动后的位置算出来
                    x, y, s = t
                    x2, y2 = x + s, y + (s ^ 1)  # 蛇头
                    if x2 < n and y2 < n and t not in vis and \\
                       g[x][y] == 0 and g[x2][y2] == 0 and (s == S or g[x + 1][y + 1] == 0):
                        if x == n - 1 and y == n - 2:  # 此时蛇头一定在 (n-1,n-1)
                            return step
                        vis.add(t)
                        q.append(t)
            step += 1
        return -1
''',
    call=f'Solution().minimumMoves({G})',
    expect=5,
    skip=['g[x][y] == 0 and', 'tmp = q'],
    max_steps=56,
    views=[
        dict(type='grid', var='g', label='迷宫（黑 1 = 障碍；蓝 = 正在扩展的蛇；粉 = 移动后的候选）', cell=88, h=380, color=_color),
        dict(type='text', fn=lambda S: (f"状态 `(X,Y,S)` = `({S['X']},{S['Y']},{S['S']})` → 候选 `(x,y,s)` = `({S['x']},{S['y']},{S['s']})`，蛇头 `({S['x2']},{S['y2']})`" if 'x2' in S else (f"正在扩展 `({S['X']},{S['Y']},{S['S']})`" if 'X' in S else '')), size=28),
        dict(type='array', var=lambda S: [''.join(map(str, t)) for t in S['q']] if 'q' in S else None,
             label='q：下一层的状态（x y s 连写）', cell=70, h=150),
    ],
    watch=['step', ('X', 'X', 'blue'), ('Y', 'Y', 'blue'), ('S', 'S', 'blue'), ('len(vis)', 'len(vis)', 'green')],
    captions={
        'step, n = 1': '`step` 从 1 开始：第一层扩展出来的状态就是走了 1 步；`n = {n}`',
        'vis = {': '`vis` 记录状态 `(蛇尾x, 蛇尾y, 方向s)`：==s=0 水平，s=1 竖直==',
        'q = [(0, 0, 0)]': '起点：蛇尾 `(0,0)`，水平 → `(0,0,0)`',
        'while q': lambda S, B, r: (f'这一层有 `{len(B.q)}` 个状态，继续 BFS' if B.q else 'q 空了：没有路 → 返回 -1'),
        'tmp = q': '`tmp` 取走当前层，`q` 换成空表装下一层——==层数就是步数==',
        'q = []': '`q` 清空，下一层的状态装这里',
        'for X, Y, S in tmp': '取出状态 `({X},{Y},{S})`',
        'for t in': '==六种移动合成三种==：下移 `(X+1,Y,S)`、右移 `(X,Y+1,S)`、旋转 `(X,Y,S^1)`',
        'x, y, s = t': '候选状态 `t = ({x},{y},{s})`',
        'x2, y2 = ': '蛇头 `(x+s, y+(s^1))` = `({x2},{y2})`',
        'if x2 < n': _check,
        'if x == n - 1': lambda S, B, r: ('蛇尾到了 `(n-1,n-2)` 水平 → ==终点==' if (S.x == S.n - 1 and S.y == S.n - 2) else f'蛇尾 `({S.x},{S.y})` 还不是终点 `({S.n-1},{S.n-2})`'),
        'vis.add': '标记 `{t}` 已访问，BFS 先到的就是最短，不会再来',
        'q.append': '`{t}` 进入下一层',
        'step += 1': '这一层扩展完，`step` → {step}',
        'return step': '蛇到终点，最少 ==`{step}`== 步',
        'return -1': '所有状态都试过，到不了 → `-1`',
    },
    cards=dict(
        one_liner='把方向当第三维，六种移动压成三个三元组',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`n×n` 网格里有一条长度 2 的蛇，从左上角水平出发，要到右下角（水平）',
                 '可以右移、下移，水平时可顺时针旋转，竖直时可逆时针旋转，障碍不能压',
                 '求最少移动次数，到不了返回 `-1`',
                 '本视频用 4×4 的小迷宫演示'],
        quote='无论是水平状态还是竖直状态：向下移动：x 增加 1；向右移动：y 增加 1；旋转：s 切换，可以用异或运算解决。',
        quote_src='—— 灵茶山艾府题解',
        idea=['用 `(x, y, s)` 表示蛇尾位置和方向，BFS 求最短路',
              '三个三元组：下移、右移、旋转，水平竖直共用一份代码',
              '蛇头 `(x+s, y+(s^1))`；旋转时还要检查 `(x+1,y+1)` 为空'],
        summary=['时间、空间都是 `O(n²)`：每个状态至多入队一次',
                 '终点判断放在入队前：蛇尾到 `(n-1,n-2)` 时蛇头一定在 `(n-1,n-1)`',
                 '易错：旋转要多查 `(x+1,y+1)`；蛇头坐标别算反',
                 '同类题：1926 迷宫中离入口最近的出口（一般网格 BFS）'],
    ),
)
