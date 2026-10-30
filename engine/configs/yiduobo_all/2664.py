_cur = lambda S: S['_inner'].get('nowx')
_curY = lambda S: S['_inner'].get('nowy')


def _try(S, B, r):
    I = S['_inner']
    x, y, d = I['x'], I['y'], I['d']
    m, n = S['m'], S['n']
    if not (0 <= x < m and 0 <= y < n):
        return f'第 `{d}` 个方向落脚 `({x},{y})`：==出界== → 换下一个方向'
    v = S['mat'][x][y]
    if v is not None:
        return f'落脚 `({x},{y})` 已经走过（第 `{v}` 步）→ 换下一个方向'
    return f'落脚 `({x},{y})` 在界内且没走过 → ==可以走=='


CONFIG = dict(
    num=2664, title='巡逻的骑士', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='暴力回溯（8 方向枚举）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def tourOfKnight(self, m, n, r, c):

        dx = [1, 2, 2, 1, -1, -2, -2, -1]
        dy = [2, 1, -1, -2, -2, -1, 1, 2]

        def dfs(level, nowx, nowy):
            if level == m * n:
                return True
            
            for d in range(8):
                x = nowx + dx[d]
                y = nowy + dy[d]
                if x >= 0 and x < m and y >= 0 and y < n and mat[x][y] is None:
                    mat[x][y] = mat[nowx][nowy] + 1
                    if dfs(level + 1, x, y):
                        return True
                    mat[x][y] = None
            
            return False

        mat = [[None] * n for _ in range(m)]
        mat[r][c] = 0
        dfs(1, r, c)

        return mat
''',
    call='Solution().tourOfKnight(3, 4, 1, 0)',
    expect=[[7, 10, 5, 2], [0, 3, 8, 11], [9, 6, 1, 4]],
    skip=['dx = [', 'dy = [', 'x = nowx', 'y = nowy', 'for d in range(8)', 17],
    max_steps=66,
    views=[
        dict(type='grid', var=lambda S: [[('' if v is None else v) for v in row] for row in S['mat']] if 'mat' in S else None,
             label='mat（数字 = 第几步到达；蓝框 = 骑士当前位置，粉框 = 正在试的落脚点）', cell=104, h=330,
             color=lambda S, i, j, v: 'green' if v != '' else None,
             cursors=[(_cur, _curY, 'blue'),
                      (lambda S: S['_inner'].get('x') if S['_line'] in (14,) else None, lambda S: S['_inner'].get('y'), 'pink')]),
        dict(type='calls', h=200),
    ],
    watch=[('level', lambda S: S['_inner'].get('level'), 'blue'), ('d', lambda S: S['_inner'].get('d'), 'pink'),
           ('x', lambda S: S['_inner'].get('x')), ('y', lambda S: S['_inner'].get('y'))],
    captions={
        'mat = [[None]': '`mat` 记录每格是第几步到达，`None` = ==还没走过==',
        'mat[r][c] = 0': '起点 `({r},{c})` 记为第 `0` 步',
        'dfs(1, r, c)': '从起点开始回溯：`level` = 已经走过的格子数，走满 `m*n` 格才算成功',
        'if level == m * n:': lambda S, B, r: (f'`level = {S._inner["level"]} == {S.m * S.n}`：==走完整个棋盘== → 返回 True'
                                              if S._inner['level'] == S.m * S.n
                                              else f'`level = {S._inner["level"]} < {S.m * S.n}`：还没走满，继续枚举 8 个落脚点'),
        'if x >= 0 and x < m': _try,
        'mat[x][y] = mat[nowx][nowy] + 1': lambda S, B, r: f'落脚 `({S._inner["x"]},{S._inner["y"]})` 标记为第 `{S.mat[S._inner["x"]][S._inner["y"]]}` 步，==占用格子==',
        'if dfs(level + 1, x, y)': '带着新位置往下一层搜索，==成功就一路返回 True==',
        9: '走满了，成功！返回 True，上面每一层都会直接返回 True，==不撤销，保留 mat==',
        'mat[x][y] = None': lambda S, B, r: f'这条路走不通 → ==撤销==：`({S._inner["x"]},{S._inner["y"]})` 还原为 None，试下一个方向',
        'return False': '8 个方向都试完仍不行 → 返回 False，==回到上一层换方向==',
        'return mat': '`mat` 里就是巡游路线：每格的数字是到达的步数',
    },
    cards=dict(
        one_liner='每步枚举 8 个落脚点，走不通就撤销重来',
        complexity='时间 `O(8^(mn))`（剪枝后远小于此），空间 `O(mn)`',
        problem=['`m × n` 的棋盘，骑士从 `(r, c)` 出发，按“日”字走，每格恰好经过一次',
                 '返回 `mat`：`mat[i][j]` 是到达 `(i, j)` 的步数（起点为 0）',
                 '本视频：`3 × 4`，起点 `(1, 0)`'],
        quote='直接使用暴力搜索回溯进行求解。具体来说，就是每一轮都枚举8个目标落脚点，若落脚点合法，同时之前没有被访问过，那么就从这个落脚点继续向后执行搜索回溯。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dx`、`dy` 两个数组列出骑士的 8 种走法', '落脚点界内且 `mat` 为 None（没走过）才能走', '递归后失败就把格子改回 None，再试下一个方向'],
        summary=['时间指数级，题目保证数据规模很小，暴力回溯即可',
                 '`mat` 同时承担“走过的步数”和“是否访问过”两个作用',
                 '成功时 `dfs` 直接返回 True，不撤销，保留结果',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
