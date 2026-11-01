BOARD = ["OO.", "XOO", ".XX"]


def _board(S):
    g = S['g']
    inner = S.get('_inner', {})
    if 'flip' not in inner:
        g2 = S.get('g2')
        if g2 and all(isinstance(r, list) for r in g2):
            return g2
    return [list(r) if isinstance(r, str) else r for r in g]


def _color(S, i, j, v):
    if v == 'X' and BOARD[i][j] == 'O':
        return 'orange'
    if v == 'X' and BOARD[i][j] == '.':
        return 'purple'
    return None


def _info(S):
    inner = S.get('_inner', {})
    if 'flip' in inner:
        return f"本轮已翻转 ==`{S['cnt']}`== 枚白棋，这一遍扫描 `flip = {S['flip']}`"
    if 'ans' in S:
        return f"目前最好成绩 `ans = {S['ans']}`"
    return ''


CONFIG = dict(
    num='LCP 41', title='黑白翻转棋', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='枚举落子点 · 反复扫描翻转（Go 原文转写）',
    tags=[],
    code='''
dir8 = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

class Solution:
    def cntFlip(self, g: List[List[str]]) -> int:
        cnt = 0
        n, m = len(g), len(g[0])
        while True:  # 不断循环，直到无法翻转白棋
            flip = False
            for i, row in enumerate(g):
                for j, ch in enumerate(row):
                    if ch != 'O':
                        continue
                    # 对于每个白棋，检查行、列或对角线中是否存在两端均有黑棋，且中间没有空白
                    for k, d in enumerate(dir8[:4]):
                        # 检查一个方向
                        x, y = i, j
                        while True:
                            if x < 0 or x >= n or y < 0 or y >= m or g[x][y] == '.':
                                break
                            if g[x][y] == 'X':
                                break
                            x, y = x + d[0], y + d[1]
                        if x < 0 or x >= n or y < 0 or y >= m or g[x][y] == '.':
                            continue
                        # 检查相反的另一方向
                        d = dir8[k + 4]
                        x, y = i, j
                        while True:
                            if x < 0 or x >= n or y < 0 or y >= m or g[x][y] == '.':
                                break
                            if g[x][y] == 'X':
                                break
                            x, y = x + d[0], y + d[1]
                        if x < 0 or x >= n or y < 0 or y >= m or g[x][y] == '.':
                            continue
                        # 将其翻转为黑棋
                        g[i][j] = 'X'
                        flip = True
                        cnt += 1
                        break
            if not flip:
                return cnt

    def flipChess(self, g: List[str]) -> int:
        ans = 0
        g2 = [None] * len(g)
        for i, row in enumerate(g):
            for j, ch in enumerate(row):
                if ch == '.':
                    for k, r in enumerate(g):
                        g2[k] = list(r)
                    g2[i][j] = 'X'  # 放上黑棋
                    cnt = self.cntFlip(g2)
                    if cnt > ans:
                        ans = cnt
        return ans
''',
    call=f'Solution().flipChess({BOARD!r})',
    expect=2,
    skip=['n, m = len(g)', 'g2 = [None]', 'for k, r in enumerate(g)', 'g2[k] = list(r)', 'for i, row in enumerate(g)',
          'for j, ch in enumerate(row)', 'x, y = ', 'while True:', 'break', 'if x < 0 or x >= n', 'if g[x][y] ==', 'for k, d in enumerate',
          'flip = False', 'continue'],
    views=[
        dict(type='grid', var=_board, label='棋盘（紫 = 新放的黑棋，橙 = 被翻转的白棋，蓝框 = 当前格，粉框 = 正在探的格）', cell=96, h=420,
             color=_color,
             cursors=[('i', 'j', 'blue'), ('x if _line in (26, 37) else None', 'y', 'pink')]),
        dict(type='text', h=70, size=28, fn=_info),
    ],
    watch=[('cnt', 'cnt', 'orange'), ('flip', 'flip'), ('ans', 'ans', 'green'), ('d', 'd', 'pink')],
    max_steps=64,
    captions={
        'ans = 0': '`ans` 记录所有落子点里最多能翻几枚白棋',
        'for i, row in enumerate(g)': lambda S, B, r: (
            '枚举每个格子，只在空格 `.` 放黑棋试一试' if 'cnt' not in S.get('_inner', {}) or 'flip' not in S.get('_inner', {})
            else f'扫描第 `{S.i}` 行'),
        'if ch == \'.\'': lambda S, B, r: (f'`({S.i},{S.j})` 是空格 → ==在这里放黑棋==试试' if S.ch == '.'
                                          else f'`({S.i},{S.j})` 已经有棋，跳过'),
        'g2[i][j] = ': '在 `({i},{j})` 放上黑棋（对 g 的副本操作，不影响下一次枚举）',
        'cnt = self.cntFlip(g2)': '放好黑棋后，反复翻转到不能翻为止，数一共翻了几枚',
        'if cnt > ans': lambda S, B, r: (f'翻了 `{S.cnt}` 枚 > 当前最好 `{S.ans}` → 更新答案' if S.cnt > S.ans
                                         else f'翻了 `{S.cnt}` 枚，不比当前最好 `{S.ans}` 多'),
        'ans = cnt': '`ans = {ans}`',
        'return ans': '所有空格都试过，最多翻 `{ans}` 枚',
        'cnt = 0': '`cnt` 统计这个落子点翻转的白棋总数',
        'while True': '==不断循环，直到无法翻转白棋==：翻转出的新黑棋可能让别的白棋也被夹住',
        'if ch != \'O\'': lambda S, B, r: (f'`({S.i},{S.j})` 是 `{S.ch!r}`，不是白棋，跳过' if S.ch != 'O'
                                          else f'`({S.i},{S.j})` 是白棋 → 检查四条线能不能被夹住'),
                'if x < 0 or x >= n': lambda S, B, r: (f'`({S.x},{S.y})` 越界或是空格 → 这一侧夹不住' if (S.x < 0 or S.x >= S.n or S.y < 0 or S.y >= S.m or S.g[S.x][S.y] == '.')
                                               else f'`({S.x},{S.y})` 是 `{S.g[S.x][S.y]}`，没有断开，继续'),
        'continue': lambda S, B, r: ('这条线有一端没有黑棋（或中间有空格）→ 换下一个方向，对应原文 `continue outer`'
                                    if 'flip' in S else '不是白棋，看下一个格子'),
        'd = dir8[k + 4]': '一个方向走到 `({x},{y})` 碰到黑棋，没被空格隔开 → 再往==相反方向== `d = {d}` 检查另一端',
        'g[i][j] = \'X\'': '`({i},{j})` 的某条线两端都有黑棋、中间没有空格 → ==翻成黑棋==',
        'flip = True': '这一遍发生了翻转，扫完后还要再来一遍',
        'cnt += 1': '累计翻转 `cnt = {cnt}`',
        'if not flip': lambda S, B, r: ('这一遍一枚都没翻 → 局面稳定，结束' if not S.flip
                                        else '这一遍有翻转，新的黑棋可能夹住别的白棋 → 再扫一遍'),
        'return cnt': '这个落子点一共翻转 `{cnt}` 枚',
    },
    cards=dict(
        one_liner='枚举每个空格放黑棋，然后反复扫描：被黑棋夹住的白棋就翻转，直到稳定',
        complexity='时间约 `O((nm)^2 · max(n,m))`，空间 `O(nm)`',
        problem=['`n×m` 棋盘，黑棋 `X`、白棋 `O`、空位 `.`',
                 '落下一枚黑棋，行、列、对角线上被两端黑棋夹住且中间无空位的白棋会被翻转，可连锁',
                 '本视频：`["OXO","OO.",".OX"]` → `2`'],
        quote='枚举每个空格放上黑棋后，能翻转多少白棋，然后就是一些实现细节了，具体见代码注释。',
        quote_src='—— 灵茶山艾府题解',
        idea=['棋盘最大 `8×8`，空格最多 64 个：直接枚举落子点',
              '`cntFlip`：循环扫描所有白棋，四个方向（共 8 个方向成对）检查两端是否都有黑棋',
              '一遍扫描中只要翻了棋就再来一遍，直到 `flip = False`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`continue outer` 改成「循环结束后再判断一次越界/空格」，`dir8` 结构体改为元组，`[]byte` 改为字符列表）',
                 '每次枚举前要重新拷贝棋盘，否则上一次的翻转会污染下一次',
                 '易错：只有「两端都有黑棋且中间没有空格」才翻转；只一端有黑棋不行',
                 '翻转后必须再来一遍：新黑棋可能让别的白棋被夹住'],
    ),
)
