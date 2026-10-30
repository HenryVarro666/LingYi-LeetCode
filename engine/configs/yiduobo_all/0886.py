import math

N0 = 5
DISLIKES = [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]]
POS = {k: (0.5 + 0.46 * math.sin(2 * math.pi * k / 5), 0.52 - 0.46 * math.cos(2 * math.pi * k / 5)) for k in range(5)}
FILL = {None: None, 0: 'cyan', 1: 'orange'}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('g')
    if g is None:
        return
    color = S.get('color') or [None] * N0
    side = min(x1 - x0 - 440, y1 - y0 - 70)
    R = 32

    def P(u):
        fx, fy = POS[u]
        return x0 + 70 + fx * side, y0 + 35 + fy * side

    x, y = S['_inner'].get('x'), S['_inner'].get('y')
    in_dfs = 'now' in S['_inner']
    cur = (x, y) if in_dfs and isinstance(y, int) and y in g.get(x, ()) else None
    for u, vs in g.items():
        for v in vs:
            if u > v:
                continue
            hot = cur is not None and set(cur) == {u, v}
            c = T['muted']
            if hot:
                c = T['red'] if color[u] is not None and color[u] == color[v] else T['yellow']
            cv.line([P(u), P(v)], c, 7 if hot else 3)
    for u in range(N0):
        X, Y = P(u)
        f = FILL.get(color[u])
        on = in_dfs and u == x
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T[f] if f else T['panel2'],
                     outline=T['yellow'] if on else T['border'], width=6 if on else 2)
        cv.text((X, Y), u, 28, T['bg'] if f else T['text'], anchor='mm', bold=True)
    lx = x0 + 70 + side + 100
    items = [('None 无色', None), ('0 第一组', 'cyan'), ('1 第二组', 'orange')]
    for k, (name, f) in enumerate(items):
        yy = y0 + 50 + k * 50
        cv.d.ellipse((lx, yy, lx + 28, yy + 28), fill=T[f] if f else T['panel2'], outline=T['border'])
        cv.text((lx + 42, yy + 14), name, 22, T['muted'], anchor='lm')
    cv.text((lx, y0 + 50 + 3 * 50 + 4), '点号 = 人的编号 − 1', 20, T['dim'])
    cv.text((lx, y0 + 50 + 3 * 50 + 36), '黄圈 = 当前点 x，黄边 = x–y', 20, T['dim'])
    cv.text((lx, y0 + 50 + 3 * 50 + 68), '红边 = 同色冲突', 20, T['dim'])


def _y(S, B, ret):
    y, x = B.y, B.x
    cy = B.color[y]
    if cy is None:
        return f'`{y}` 无色 → 染成 `1 - {B.now} = {1 - B.now}`，然后从 {y} 递归染色'
    return f'`{y}` 已有颜色 `{cy}`，再看是否和 {x} 同色'


def _eq(S, B, ret):
    y, x = B.y, B.x
    if B.color[y] == B.color[x]:
        return f'`color[{y}] == color[{x}] == {B.color[x]}`：讨厌的两人==被迫同组== → 不是二分图'
    return f'`color[{y}] = {B.color[y]}` ≠ `color[{x}] = {B.color[x]}` → 跳过 {y}'


CONFIG = dict(
    num=886, title='可能的二分法', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='建图 + 01 染色 DFS',
    tags=['labuladong', '灵神题单·图论算法', '难度分 1795'],
    code='''
class Solution(object):
    def possibleBipartition(self, N, dislikes):

        g = {}
        for x, y in dislikes:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        color = [None] * N
        for x in range(N):
            if color[x] is None:
                color[x] = 0
                if not self.dfs(x, 0, g, color):
                    return False

        return True

    def dfs(self, x, now, g, color):
        for y in g.get(x, set()):
            if color[y] is None:
                color[y] = 1 - now
                if not self.dfs(y, 1 - now, g, color):
                    return False
            elif color[y] == color[x]:
                return False

        return True
''',
    call=f'Solution().possibleBipartition({N0}, {DISLIKES})',
    expect=False,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var=lambda S: ['-' if v is None else v for v in S['color']] if 'color' in S else None,
             label='color（None 无色 / 0 / 1）', cell=80, h=150,
             color=lambda S, i, v: FILL.get(S['color'][i])),
        dict(type='calls', h=150, hide=('g', 'color', 'dislikes')),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'yellow'), ('y', lambda S: S['_inner'].get('y')), 'now'],
    skip=['y -= 1', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()'],
    captions={
        'g = {}': '每个人看成一个点，讨厌关系连边：`g` 存每个点的邻居集合',
        'for x, y in dislikes': lambda S, B, r: (f'`[{S.x}, {S.y}]` 互相讨厌 → 连一条边' if 'x' not in B or (B.x, B.y) != (S.x, S.y)
                                                 else '边都连好了：问题转化为==判断二分图=='),
        'x -= 1': '编号改成从 0 开始：`{x}` 和 `{y - 1}`',
        'g[x].add(y)': '`g[{x}]` 加入 {y}',
        'g[y].add(x)': '`g[{y}]` 加入 {x}：无向边，两边都加',
        'color = [None] * N': '`color` 全为 `None`：所有人==都还没分组==',
        'for x in range(N)': lambda S, B, r: f'看第 {S.x} 个点',
        'if color[x] is None': lambda S, B, r: (f'{S.x} 无色 → 新连通块' if B.color[S.x] is None else f'{S.x} 已染色，跳过'),
        'color[x] = 0': '`color[{x}] = 0`：起点染成 0',
        'if not self.dfs(x, 0, g, color)': '从 {x} 开始递归染色',
        'for y in g.get(x, set())': lambda S, B, r: (f'枚举 {S.x} 连接的点 `y = {S.y}`'
                                                     if 'y' in S['_inner'] and ('y' not in B or B.y != S.y or B.x != S.x)
                                                     else f'{S.x} 的邻居都处理完了'),
        'if color[y] is None': _y,
        'color[y] = 1 - now': '`color[{y}] = 1 - {now} = {color[y]}`：和 {x} 分到==不同组==',
        'if not self.dfs(y, 1 - now, g, color)': '递归 `dfs({B.y}, {1 - B.now})`',
        'elif color[y] == color[x]': _eq,
        31: '同色冲突 → 返回 `False`',
        29: '下层返回 `False`，继续向上传递',
        20: '`dfs` 返回 `False` → ==无法分成两组==',
    },
    max_steps=75,
    cards=dict(
        one_liner='人看成点、讨厌关系看成边，问题就变成判断二分图',
        complexity='时间 `O(N + E)`，空间 `O(N + E)`',
        problem=['`N` 个人（编号 1..N）分成两组，`[a, b]` 表示 a、b ==不能同组==',
                 '能分成两组返回 `true`，否则 `false`',
                 '本视频：`N = 5`，`[[1,2],[2,3],[3,4],[4,5],[1,5]]` → `false`'],
        quote='把题目中的每个人看做图中的点，然后在存在dislike关系的两个人之间连上一条边，那么问题就转化成了==判断这个图是否为二分图==。',
        quote_src='—— yiduobo 题解原文',
        idea=['二分图判定的经典做法：==01 染色==',
              '邻居无色 → 染成 `1 - now` 并递归；同色 → 返回 false；异色 → 跳过',
              '注意 yiduobo 是==先给邻居染色再递归==，dfs 本身不染当前点'],
        summary=['时间 `O(N + E)`：每个点只染一次色',
                 '易错：编号从 1 开始，建图时先减 1；无向边要双向加',
                 '没出现在 dislikes 里的人用 `g.get(x, set())` 处理',
                 '五个人围成一圈是==奇环==，01 染色必然冲突',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
