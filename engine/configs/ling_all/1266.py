P = [[1, 1], [3, 4], [-1, 0], [2, -2]]


def _rows(S, pts):
    out = []
    for k, p in enumerate(pts):
        out.append(f'P{k}')
    return out


def _cell(S, r, c, v):
    if 'x1' not in S:
        return None
    pts = S['points']
    for k in range(len(pts) - 1):
        if pts[k] == [S['x1'], S['y1']] and pts[k + 1] == [S['x2'], S['y2']]:
            if r == k:
                return 'blue'
            if r == k + 1:
                return 'pink'
    return None


def _text(S):
    if 'x1' not in S:
        return '相邻两点之间的最少时间 = `max(|dx|, |dy|)`（切比雪夫距离）'
    dx, dy = abs(S['x1'] - S['x2']), abs(S['y1'] - S['y2'])
    return f'`dx = {dx}`，`dy = {dy}`：斜着走 `{min(dx, dy)}` 秒 + 直走 `{abs(dx - dy)}` 秒 = ==`{max(dx, dy)}`== 秒'


CONFIG = dict(
    num=1266, title='访问所有点的最小时间', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='相邻点切比雪夫距离求和',
    tags=['曼哈顿距离与切比雪夫距离', '难度分 1303'],
    code='''
class Solution:
    def minTimeToVisitAllPoints(self, points: List[List[int]]) -> int:
        ans = 0
        for (x1, y1), (x2, y2) in pairwise(points):
            ans += max(abs(x1 - x2), abs(y1 - y2))
        return ans
''',
    call=f'Solution().minTimeToVisitAllPoints({P!r})',
    expect=10,
    views=[
        dict(type='table', var='points', label='points（蓝 = 起点，粉 = 终点，必须按顺序访问）', h=330, cell=80,
             rows=lambda S: [f'P{k}' for k in range(len(S['points']))], cols=['x', 'y'], color=_cell),
        dict(type='text', fn=_text, size=26, h=70),
    ],
    watch=[('x1,y1', '(x1, y1)', 'blue'), ('x2,y2', '(x2, y2)', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计总时间',
        'for (x1, y1)': lambda S, B, r: ('所有相邻点对都处理完，循环结束' if B.get('x1') == S.x1 and B.get('y2') == S.y2 and B.get('ans') == S.ans and S.ans > 0 else f'取相邻两点：从 `({S.x1}, {S.y1})` 走到 `({S.x2}, {S.y2})`，==按数组顺序==访问'),
        'ans += max': '斜着走一秒能同时缩小 dx、dy，所以 `max({abs(x1-x2)}, {abs(y1-y2)})` = {max(abs(x1-x2), abs(y1-y2))} 秒 → `ans` = =={ans}==',
        'return ans': '所有相邻点对累加完，答案 =={ret}==',
    },
    cards=dict(
        one_liner='斜着走最划算：两点耗时 = max(|dx|, |dy|)',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['平面上有 `n` 个点，每秒可横走、竖走或斜走一格',
                 '必须按数组顺序访问，求最少总时间',
                 '示例：`[[1,1],[3,4],[-1,0]]` → `7`'],
        quote='所以当 d_x 和 d_y 都大于 0 时，使用对角线移动是最优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dx`、`dy` 都 > 0 时，对角线一秒同时减 1，最划算',
              '先斜走 `min(dx, dy)` 秒，剩下的直走，共 `max(dx, dy)` 秒',
              '这就是两点的切比雪夫距离；相邻点对累加即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '必须按顺序访问，所以只累加相邻点对，不能重排',
                 '另有一行写法：`sum(max(...) for ... in pairwise(points))`',
                 '同类：曼哈顿距离与切比雪夫距离题单（§7.3）'],
    ),
)
