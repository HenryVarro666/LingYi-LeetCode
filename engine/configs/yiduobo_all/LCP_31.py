MAZE = [['.##', '#.#', '#..'], ['.#.', '###', '##.'], ['.##', '###', '##.'], ['.##', '##.', '.#.'], ['.##', '.##', '...']]
_SN = {0: '两张卷轴都在', 1: '临时卷轴已用', 2: '永久卷轴已用', 3: '两张卷轴都已用'}


def _board(S):
    I = S['_inner']
    t = I.get('nowt', S.get('nowt'))
    if t is None or 'maze' not in S:
        return None
    return [list(r) for r in S['maze'][t]]


def _col(S, i, j, v):
    I = S['_inner']
    if 'nowx' in I and (i, j) == (I['nowx'], I['nowy']):
        return 'blue'
    if 'x' in I and S.get('_line') in range(24, 40) and (i, j) == (I['x'], I['y']):
        return 'pink'
    return 'red' if v == '#' else None


def _lab(S):
    I = S['_inner']
    t = I.get('nowt')
    return f'时刻 {t} 的地形（蓝 = 小力，粉 = 要走去的格子，红 = 陷阱 #，出口在右下角）' if t is not None else '地形'


def _state(S):
    I = S['_inner']
    if 'nowt' not in I:
        return ''
    return f"状态 `(t={I['nowt']}, 位置=({I['nowx']},{I['nowy']}), s={I['nows']})`：=={_SN[I['nows']]}=="


def _try(S, B, ret):
    I = S['_inner']
    x, y, t, m, n = I['x'], I['y'], I['nowt'], S['m'], S['n']
    if not (0 <= x < m and 0 <= y < n):
        return f'`({x},{y})` 出界，这个方向不行'
    stay = ' （原地挂机）' if (x, y) == (I['nowx'], I['nowy']) else ''
    return f'下一时刻 `{t + 1}` 想去 `({x},{y})`{stay}，那时它是 `{S["maze"][t + 1][x][y]}`'


def _free(S, B, ret):
    I = S['_inner']
    x, y, t = I['x'], I['y'], I['nowt']
    return f'`maze[{t + 1}][{x}][{y}]` 是空地，直接走过去，卷轴状态 `s = {I["nows"]}` 不变，递归进入时刻 {t + 1}'


def _temp(S, B, ret):
    I = S['_inner']
    ok = I['nows'] in (0, 2)
    return ('那一格是陷阱：先试 ==临时卷轴==（只管下一时刻），`s + 1` 表示临时卷轴用掉了' if ok
            else '那一格是陷阱，但临时卷轴已经用过，这条路走不了')


CONFIG = dict(
    num='LCP 31', title='变换的迷宫', difficulty='Hard', category='网格图',
    author='yiduobo', technique='记忆化搜索 · 状态 (t, x, y, 卷轴)',
    tags=['网格图'],
    code='''
class Solution(object):
    def escapeMaze(self, maze):

        t = len(maze)
        m = len(maze[0])
        n = len(maze[0][0])
        
        f = [[[[None] * 4 for k in range(n)] for j in range(m)] for i in range(t)]

        dx = [1, 0, -1, 0, 0]
        dy = [0, 1, 0, -1, 0]

        def dfs(nowt, nowx, nowy, nows, f):
            if f[nowt][nowx][nowy][nows] is None:
                if nowx == m - 1 and nowy == n - 1:
                    return True

                f[nowt][nowx][nowy][nows] = False

                if nowt == t - 1:
                    return False
                
                
                for index in range(5):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        if maze[nowt + 1][x][y] == '.':
                            if dfs(nowt + 1, x, y, nows, f):
                                return True
                        else:
                            if nows == 0 or nows == 2:
                                if dfs(nowt + 1, x, y, nows + 1, f):
                                    return True
                
                            if nows < 2:
                                for nextt in range(nowt + 1, t):
                                    if dfs(nextt, x, y, nows + 2, f):
                                        return True
            
            return False
        
        

        return dfs(0, 0, 0, 0, f)
''',
    call=f'Solution().escapeMaze({MAZE})',
    expect=True,
    skip=['t = len', 'm = len', 'n = len', 'f = [[[[None]', 'dx = [', 'dy = [', 'def dfs', 'for index in range(5)',
          'x = nowx', 'y = nowy', 'if x >= 0 and x < m', 'if nowx == m - 1 and nowy == n - 1', 'for nextt in range', 'return False'],
    max_steps=110,
    views=[
        dict(type='grid', var=_board, label='当前时刻 nowt 的地形 maze[nowt]（蓝 = 小力，粉 = 要去的格子，红 = 陷阱 #，出口在右下角）', cell=110, h=250, color=_col),
        dict(type='text', fn=_state, size=26, h=60),
        dict(type='calls', h=200, hide=('f',)),
    ],
    watch=[('nowt', "_inner.get('nowt')", 'blue'), ('s', "_inner.get('nows')", 'orange'), ('x', "_inner.get('x')"), ('y', "_inner.get('y')")],
    captions={
        'if f[nowt][nowx][nowy][nows] is None': lambda S, B, r: ('这个状态没算过，往下展开' if B.f[S.nowt][S.nowx][S.nowy][S.nows] is None
                                                                else '这个状态以前算过（且失败了）→ 直接返回 False，不重复搜索'),
        'if nowx == m - 1 and nowy == n - 1': lambda S, B, r: ('到出口了 → 返回 ==True==' if (S.nowx, S.nowy) == (S.m - 1, S.n - 1)
                                                                else f'还没到出口 `({S.m - 1},{S.n - 1})`，继续'),
        'f[nowt][nowx][nowy][nows] = False': '==先标记为 False==：这个状态一旦展开就不用再展开第二次',
        'if nowt == t - 1': lambda S, B, r: ('时间到了（最后一个时刻）还没到出口 → False' if S.nowt == S.t - 1
                                              else f'还剩时间（现在 `t={S.nowt}`，最后是 `{S.t - 1}`），继续尝试 5 个动作'),
        "if maze[nowt + 1][x][y] == '.'": lambda S, B, r: (f'下一时刻想去 `({S.x},{S.y})`，那时是空地 → ==直接走过去==' if S.maze[S.nowt + 1][S.x][S.y] == '.'
                                                           else f'下一时刻想去 `({S.x},{S.y})`，那时是陷阱 `#` → 得用卷轴'),
        'if dfs(nowt + 1, x, y, nows, f)': _free,
        'if nows == 0 or nows == 2': _temp,
        'if dfs(nowt + 1, x, y, nows + 1, f)': '临时卷轴只管一个时刻：踩着陷阱走过去，`s` 变成 `{B.nows + 1}`，进入时刻 {B.nowt + 1}',
        'if nows < 2': lambda S, B, r: ('永久卷轴还没用 → 可以用：它让这格永久变空地' if S.nows < 2
                                        else '永久卷轴已经用过了，不能再用'),
        'if dfs(nextt, x, y, nows + 2, f)': '==永久卷轴==：这格永久变空地，小力可以在这里==挂机到任意时刻 `{nextt}`==，`s` 变成 `{B.nows + 2}`',
        'return True': lambda S, B, r: ('到出口 `(%d,%d)` 了 → 返回 ==True==' % (S.m - 1, S.n - 1) if (S.nowx, S.nowy) == (S.m - 1, S.n - 1) else '下一层找到出路，一路返回 ==True=='),
        'return dfs(0, 0, 0, 0, f)': '从时刻 0、起点 `(0,0)`、没用过卷轴开始搜',
    },
    cards=dict(
        one_liner='把卷轴使用情况压进状态，永久卷轴 = 在原地挂机',
        complexity='时间 `O(t·m·n·4·t)`，空间 `O(t·m·n)`',
        problem=['迷宫地形随时间 `t` 变化，每刻可上下左右走一步或原地不动',
                 '有两张卷轴：==临时消除术==（只管下一时刻）、==永久消除术==（一直有效）',
                 '问：能否在 `t` 个时刻内、不踩陷阱到达右下角出口',
                 '本视频用 5 个时刻、3×3 的小迷宫，答案 True（必须用永久卷轴）'],
        quote='使用永久卷轴相当于提供了一种待在(cx, cy)一直挂机的选项，这样一来就没有必要在状态中储存(cx, cy)了。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态 `f[t][x][y][s]`，`s` 用两位二进制记录两张卷轴是否用过',
              '永久卷轴会改地图，但只用来「在该格挂机」就够了：用的那一刻，枚举后面挂机到哪个时刻 `nextt`',
              '记忆化搜索：状态先标 False 再展开，同一状态不会算两遍'],
        summary=['状态数 `t·m·n·4`，每个永久卷轴状态再枚举挂机时刻，共 `O(t²·m·n)` 量级',
                 '易错：走到出口要先于「时间到」的判断；陷阱格只有用卷轴才能进入',
                 '`s = 0/1/2/3` 分别表示都没用 / 只用临时 / 只用永久 / 都用了',
                 '原文为 Python 2 风格，代码未做改动（直接是 Python 3 可运行）'],
    ),
)
