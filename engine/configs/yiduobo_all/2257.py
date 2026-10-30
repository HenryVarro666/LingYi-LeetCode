GUARDS = [[1, 0]]
WALLS = [[1, 1], [0, 2]]


def _fl(S, B, r):
    # 缩进更深的 flag = False 是遇到墙时那一句
    src = CONFIG['code'].strip('\n').split('\n')
    deep = len(src[S['_line'] - 1]) - len(src[S['_line'] - 1].lstrip()) > 16
    if deep:
        return f"`({S['x']},{S['y']})` 是墙：`flag = False`，警卫的视线被挡住"
    return '新一趟扫描：`flag` = ==最近的特殊格子是不是警卫==，一开始没遇到'


def _color(S, i, j, v):
    return {1: 'purple', 2: 'blue', 3: 'orange'}.get(v)


CONFIG = dict(
    num=2257, title='统计网格图中没有被保卫的格子数', difficulty='Medium', category='网格图',
    author='yiduobo', technique='四个方向各扫一遍，记最近的特殊格子',
    tags=[],
    code='''
class Solution(object):
    def countUnguarded(self, m, n, guards, walls):

        f = [[0] * n for _ in range(m)]

        for x, y in walls:
            f[x][y] = 1

        for x, y in guards:
            f[x][y] = 2
        
        for x in range(m):
            flag = False
            for y in range(n):
                if f[x][y] == 1:
                    flag = False
                elif f[x][y] == 2:
                    flag = True
                elif flag:
                    f[x][y] = 3

            flag = False
            for y in range(n - 1, -1, -1):
                if f[x][y] == 1:
                    flag = False
                elif f[x][y] == 2:
                    flag = True
                elif flag:
                    f[x][y] = 3
        
        for y in range(n):
            flag = False
            for x in range(m):
                if f[x][y] == 1:
                    flag = False
                elif f[x][y] == 2:
                    flag = True
                elif flag:
                    f[x][y] = 3
            
            flag = False
            for x in range(m - 1, -1, -1):
                if f[x][y] == 1:
                    flag = False
                elif f[x][y] == 2:
                    flag = True
                elif flag:
                    f[x][y] = 3

        res = 0
        for x in range(m):
            for y in range(n):
                if f[x][y] == 0:
                    res += 1

        return res
''',
    call='Solution().countUnguarded(3, 3, %r, %r)' % (GUARDS, WALLS),
    expect=4,
    skip=['if f[x][y] == 1', 'elif f[x][y] == 2', 'for x, y in walls', 'for x, y in guards', 'for x in range', 'for y in range', 'res = 0', 'f[x][y] = 1', 'f[x][y] = 2'],
    max_steps=120,
    views=[
        dict(type='grid', var='f', label='f（紫=墙 蓝=警卫 橙=被保卫 空白=暂未保卫；黄框=当前格）', cell=110, color=_color,
             cursors=[('x', 'y', 'yellow')], h=420),
        dict(type='text', fn=lambda S: ('`flag = %s`：本行（列）中，当前方向上最近的特殊格子%s' % (S['flag'], '是==警卫==' if S['flag'] else '是墙，或还没遇到')) if 'flag' in S and S['_line'] >= 12 and S['_line'] <= 52 else '', size=28, h=60),
    ],
    watch=[('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('flag', 'flag', 'blue'), ('res', 'res', 'green')],
    captions={
        'f = [[0]': '`f`：0 = 普通格子，1 = 墙，2 = 警卫，3 = 被保卫的普通格子',
        'flag = False': _fl,
        'if f[x][y] == 1': lambda S, B, r: ('`({0},{1})` 是墙 → 最近的特殊格子变成墙，`flag = False`（视线被挡住）'.format(S.x, S.y) if S.f[S.x][S.y] == 1
                                            else '`({0},{1})` 不是墙'.format(S.x, S.y)),
        'elif f[x][y] == 2': lambda S, B, r: ('`({0},{1})` 是警卫 → 它成了最近的特殊格子，`flag = True`'.format(S.x, S.y) if S.f[S.x][S.y] == 2
                                              else '`({0},{1})` 不是警卫，是普通格子'.format(S.x, S.y)),
        'elif flag': lambda S, B, r: (f'`({S.x},{S.y})` 是普通格子，最近的特殊格子是警卫 → ==被保卫==' if S.flag else f'`({S.x},{S.y})` 是普通格子，最近的特殊格子是墙或没有 → 不保护'),
        'f[x][y] = 3': '`({x},{y})` 标记为 3：被保卫',
        'flag = True': '`({x},{y})` 是警卫：`flag = True`，它成了最近的特殊格子',
        'if f[x][y] == 0': lambda S, B, r: ('`({0},{1})` 仍是 0 → 四个方向都没人保卫它，`res + 1`'.format(S.x, S.y) if S.f[S.x][S.y] == 0
                                            else '`({0},{1})` 不是 0（墙、警卫或被保卫），不计'.format(S.x, S.y)),
        'res += 1': '`res` → {res}',
        'return res': '没被保卫的普通格子共 `{res}` 个',
    },
    cards=dict(
        one_liner='四个方向各扫一遍：只看最近的特殊格子是警卫还是墙',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 网格里有警卫和墙；警卫能看见上下左右、直到被墙或警卫挡住',
                 '求既不是墙也不是警卫、且没被任何警卫看到的格子数',
                 '本视频：`3×3`，警卫 `[1,0]`，墙 `[1,1] [0,2]` → `4`'],
        quote='如果某个方向上最近的特殊单元格是警卫，那么这个单元格就可以被这个警卫保护。反过来，如果四个方向上最近的特殊单元格都是墙，或者一直到边界都没有特殊单元格，那么这个普通单元格就不会被保卫。',
        quote_src='—— yiduobo 题解原文',
        idea=['墙和警卫叫==特殊格子==，其余是普通格子',
              '从左到右扫一行，`flag` 记最近的特殊格子是否为警卫：普通格子遇到 `flag = True` 就被保护',
              '同理再从右到左、从上到下、从下到上各扫一遍，共 4 遍，每遍 `O(mn)`'],
        summary=['时间 `O(mn)`（4 遍扫描 + 1 遍统计），空间 `O(mn)`',
                 '易错：每扫一行（列）、每换一个方向，`flag` 都要重置为 False',
                 '易错：遇到墙要把 `flag` 置 False，墙会挡住警卫的视线',
                 '对比灵神：他从警卫出发沿射线标记，这里是每个格子问最近的特殊格子是谁',
                 '原文为 Python 2 风格，代码无需改动，直接运行'],
    ),
)
