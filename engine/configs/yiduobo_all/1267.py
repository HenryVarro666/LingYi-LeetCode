GRID = [[1, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 0, 0]]


def _c(S, i, j, v):
    if 'row' not in S or not v:
        return None
    if S['_line'] < 16:
        return None
    return 'red' if S['row'][i] == 1 and S['col'][j] == 1 else 'green'


CONFIG = dict(
    num=1267, title='统计参与通信的服务器', difficulty='Medium', category='网格图',
    author='yiduobo', technique='行列计数 · 逆向排除',
    tags=[],
    code='''
class Solution(object):
    def countServers(self, grid):

        m = len(grid)
        n = len(grid[0])
        row = [0] * m
        col = [0] * n
        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j]:
                    row[i] += 1
                    col[j] += 1
                    res += 1

        for i in range(m):
            for j in range(n):
                if grid[i][j] and row[i] == 1 and col[j] == 1:
                    res -= 1
        
        return res
''',
    call=f'Solution().countServers({GRID})',
    expect=4,
    views=[
        dict(type='grid', var='grid', cursors=[('i', 'j', 'yellow', '(i,j)')], color=_c, h=330, cell=80),
        dict(type='array', var='row', label='row（每行服务器数）', pointers={'i': 'blue'}, h=130, cell=70),
        dict(type='array', var='col', label='col（每列服务器数）', pointers={'j': 'pink'}, h=130, cell=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    skip=['m = len', 'n = len', 'row = [0]', 'col = [0]'],
    captions={
        'res = 0': '`res` 先记录所有服务器数，后面再减掉孤立的',
        'if grid[i][j]:': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = 1`：这里有服务器，统计它所在的行和列' if S.grid[S.i][S.j] else f'`grid[{S.i}][{S.j}] = 0`：没有服务器，跳过'),
        'row[i] += 1': '第 `{i}` 行服务器数 → =={row[i]}==',
        'col[j] += 1': '第 `{j}` 列服务器数 → =={col[j]}==',
        'res += 1': '服务器总数 `res` = {res}',
        'if grid[i][j] and row[i] == 1': lambda S, B, r: (
            f'`({S.i},{S.j})` 行内 {S.row[S.i]} 台、列内 {S.col[S.j]} 台：行列都只有它自己 → ==孤立=='
            if S.grid[S.i][S.j] and S.row[S.i] == 1 and S.col[S.j] == 1 else
            (f'`({S.i},{S.j})` 行内 {S.row[S.i]} 台、列内 {S.col[S.j]} 台：至少有一个同伴 → 能通信'
             if S.grid[S.i][S.j] else f'`({S.i},{S.j})` 没有服务器，跳过')),
        'res -= 1': '孤立的服务器不能通信，去掉：`res` → =={res}==',
        'return res': '剩下的都能通信，共 `{res}` 台',
    },
    max_steps=110,
    cards=dict(
        one_liner='逆向思考：找出行列上都只有自己的孤立服务器，总数减去它们',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['网格里 `1` 是服务器，同一行或同一列的服务器可以互相通信',
                 '统计至少能和另一台服务器通信的服务器数量',
                 '示例：`[[1,0,0,1],[0,0,1,0],[0,0,1,0],[0,1,0,0]]` → `4`'],
        quote='对于某台服务器，若其不能与其他服务器通信，那么这台服务器的行和列上必然只有这一台服务器',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：数每行、每列各有几台服务器，同时累计总数 `res`',
              '第二趟：某台服务器若 `row[i] == 1` 且 `col[j] == 1`，就是孤立的',
              '总数减去孤立台数，就是答案'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`',
                 '易错：孤立要同时满足行和列都只有 1 台；只满足一个仍能通信',
                 '原文用数组 `row`/`col` 计数（文中称哈希表）；代码无需改动即可在 Python 3 运行'],
    ),
)
