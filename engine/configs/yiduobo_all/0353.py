W, H, FOOD = 3, 2, [[1, 2], [0, 1]]


def _board(S):
    if 'self.snake' not in S or 'self.h' not in S:
        return None
    w, h, food, score = S['self.w'], S['self.h'], S['self.food'], S['self.score']
    g = [[''] * w for _ in range(h)]
    for k in range(score, len(food)):
        x, y = food[k]
        g[x][y] = '食' if k == score else '食·'
    body = S['self.snake'][min(S['self.left'], len(S['self.snake']) - 1):]
    for x, y in body:
        g[x][y] = '蛇'
    if body:
        x, y = body[-1]
        g[x][y] = '头'
    return g


def _color(S, i, j, v):
    return {'头': 'green', '蛇': 'blue', '食': 'orange', '食·': None}.get(v)


def _body_txt(S):
    if 'self.snake' not in S or 'self.left' not in S:
        return ''
    body = [tuple(p) for p in S['self.snake'][min(S['self.left'], len(S['self.snake']) - 1):]]
    return f"队列（蛇尾 → 蛇头）：`{body}`　得分 =={S['self.score']}==　`used` = `{sorted(S['self.used'])}`"


CONFIG = dict(
    num=353, title='贪吃蛇', difficulty='Medium', category='设计',
    author='yiduobo', technique='队列 + 哈希集合',
    code='''
class SnakeGame(object):

    def __init__(self, width, height, food):
        self.w = width
        self.h = height
        self.score = 0
        self.food = food[:]
        self.used = set()
        self.used.add(0)
        self.snake = [[0, 0]]
        self.left = 0
        self.right = 1
        self.dx = {'L': 0, 'R': 0, 'U': -1, 'D': 1}
        self.dy = {'L': -1, 'R': 1, 'U': 0, 'D': 0}

    def move(self, direction):
        head_x, head_y = self.snake[-1]
        head_x += self.dx[direction]
        head_y += self.dy[direction]
        if head_x < 0 or head_y < 0 or head_x == self.h or head_y == self.w:
            return -1

        if self.score < len(self.food) and self.food[self.score][0] == head_x and self.food[self.score][1] == head_y:
            self.score += 1
            self.snake.append([head_x, head_y])
            self.right += 1
            self.used.add(head_x * self.w + head_y)
        else:
            tail_x, tail_y = self.snake[self.left]
            self.left += 1
            self.used.remove(tail_x * self.w + tail_y)
            if head_x * self.w + head_y in self.used:
                return -1
            self.snake.append([head_x, head_y])
            self.right += 1
            self.used.add(head_x * self.w + head_y)

        return self.score
''',
    call='''g = SnakeGame(3, 2, [[1, 2], [0, 1]])
[g.move(d) for d in 'RDRULU']''',
    expect=[0, 0, 1, 1, 2, -1],
    views=[
        dict(type='grid', var=_board, label='棋盘 2×3（绿 = 蛇头，蓝 = 蛇身，橙 = 下一个食物）', cell=130, h=330, color=_color),
        dict(type='text', fn=_body_txt, size=26, h=110),
        dict(type='calls', h=100),
    ],
    watch=[('方向', 'direction', 'blue'), 'head_x', 'head_y', ('score', 'self.score', 'green'), ('left', 'self.left', 'cyan')],
    skip=['self.w = width', 'self.h = height', 'self.right = 1', 'self.dx =', 'self.dy =', 'self.right += 1',
          'self.used = set()', 'self.left = 0'],
    captions={
        'self.score = 0': '`score` 既是得分，也是==下一个食物在 food 里的下标==',
        'self.food = food[:]': '复制食物列表：`{self.food}`',
        'self.used.add(0)': '`used` 集合记录蛇占的格子，编号 = `x * w + y`；起点 (0,0) 编号 0',
        'self.snake = [[0, 0]]': '`snake` 当队列用：队尾（末尾）是蛇头，`left` 指向蛇尾',
        'head_x, head_y = self.snake[-1]': '== move({direction}) ==：先取蛇头 `({head_x}, {head_y})`',
        'head_x += self.dx': '按方向 `{direction}` 算出新蛇头的行：`head_x = {head_x}`',
        'head_y += self.dy': '新蛇头的列：`head_y = {head_y}` → 目标格 `({head_x}, {head_y})`',
        'if head_x < 0': lambda S, B, r: ('目标格 `({}, {})` 出了棋盘 → 撞墙'.format(S.head_x, S.head_y) if (S.head_x < 0 or S.head_y < 0 or S.head_x == S.self.h or S.head_y == S.self.w)
                                          else '目标格 `({}, {})` 在棋盘内，没撞墙'.format(S.head_x, S.head_y)),
        'return -1': '游戏结束，返回 `-1`',
        'if self.score < len(self.food)': lambda S, B, r: ('目标格正好是下一个食物 `{}` → ==吃到食物=='.format(S.self.food[B.self.score]) if r_eat(S, B)
                                                           else '目标格不是食物 → 正常前进'),
        'self.score += 1': '吃到食物：`score` → `{self.score}`',
        'self.snake.append([head_x, head_y])': '新蛇头入队：`({head_x}, {head_y})`',
        'self.used.add(head_x * self.w + head_y)': '新蛇头占用的格子编号 `{head_x * self.w + head_y}` 加入 `used`',
        'tail_x, tail_y = self.snake[self.left]': '没吃到食物：蛇尾 `({tail_x}, {tail_y})` 要离开',
        'self.left += 1': '蛇尾出队，`left` → {self.left}',
        'self.used.remove': '把蛇尾格子 `{tail_x * self.w + tail_y}` 从 `used` 删掉：==必须先走尾，再判断撞自己==',
        'if head_x * self.w + head_y in self.used': lambda S, B, r: ('新蛇头格子 `{}` 还在 `used` 里 → ==撞到自己=='.format(S.head_x * S.self.w + S.head_y) if (S.head_x * S.self.w + S.head_y) in S.self.used
                                                                    else '新蛇头格子 `{}` 不在 `used` 里 → 安全'.format(S.head_x * S.self.w + S.head_y)),
        'return self.score': '本次移动后得分 `{ret}`',
    },
    cards=dict(
        one_liner='蛇尾先出队、蛇头再入队，吃到食物时蛇尾不动',
        complexity='每次 `move` 时间 `O(1)`，空间 `O(蛇长 + 食物数)`',
        problem=['设计贪吃蛇 `SnakeGame(width, height, food)`，蛇从 `(0,0)` 出发',
                 '`move(direction)` 沿 U/D/L/R 前进一格，返回当前得分',
                 '撞墙或撞到自己返回 `-1`；吃到食物蛇身变长、得分 +1',
                 '示例：宽 3 高 2，食物 `[[1,2],[0,1]]`，走 `RDRULU` → `[0,0,1,1,2,-1]`'],
        quote='蛇尾离开所在单元格，然后蛇头来到新的单元格，恰好是符合队列先进先出的概念的，因此可以尝试使用一个队列来维护蛇现在占据的单元格。',
        quote_src='—— yiduobo 题解原文',
        idea=['队尾 = 蛇头：用队尾加方向就能算出下一格',
              '吃到食物：只入队蛇头，蛇尾==不出队==（蛇变长）',
              '否则蛇尾先出队，再用哈希集合 `used` 判断新蛇头是否撞自己'],
        summary=['每次 `move` 都是 `O(1)`：队列首尾操作 + 集合查询',
                 '易错：==先移除蛇尾，再判断撞自己==，否则蛇头追着蛇尾走会被误判',
                 '`score` 同时是下一个食物的下标，不用额外指针',
                 '格子编号 `x * w + y`，保证集合里的元素唯一'],
    ),
)


def r_eat(S, B):
    o = B.self
    return o.score < len(o.food) and o.food[o.score][0] == S.head_x and o.food[o.score][1] == S.head_y
