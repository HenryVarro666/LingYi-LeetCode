ROOM = [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
DN = ['向右', '向下', '向左', '向上']


def _dir(S):
    if 'nowd' not in S:
        return ''
    return (f"位置 `({S['nowx']},{S['nowy']})`，朝向 =={DN[S['nowd']]}==（`nowd = {S['nowd']}`），"
            f"已清扫 =={S['res']}== 格")


def _if(S, B, r):
    x, y = S.x, S.y
    m, n = len(S.room), len(S.room[0])
    if x < 0 or y < 0 or x >= m or y >= n:
        return f'前方 `({x},{y})` 出界 → ==右转 90 度=='
    if S.room[x][y] == 1:
        return f'前方 `({x},{y})` 是障碍物 → ==右转 90 度=='
    return f'前方 `({x},{y})` 是空格子 → 前进'


def _vis(S, B, r):
    p, d = S.vis[S.nowx][S.nowy], S.nowd
    if p & (1 << d) == 0:
        return f'`vis[{S.nowx}][{S.nowy}] = {p}`，没有朝{DN[d]}来过 → ==新状态==，继续'
    return f'`vis[{S.nowx}][{S.nowy}] = {p}`，已经朝{DN[d]}来过 → ==状态重复==，之后只会循环'


CONFIG = dict(
    num=2061, title='扫地机器人清扫过的空间个数', difficulty='Medium', category='网格图',
    author='yiduobo', technique='模拟 + 位置/方向状态去重',
    tags=[],
    code='''
class Solution(object):
    def numberOfCleanRooms(self, room):

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        
        m = len(room)
        n = len(room[0])
        vis = [[0] * n for _ in range(m)]

        nowx, nowy, nowd = 0, 0, 0
        vis[0][0] = 1
        res = 1
        while True:
            x = nowx + dx[nowd]
            y = nowy + dy[nowd]
            if x < 0 or y < 0 or x >= m or y >= n or room[x][y] == 1:
                nowd = (nowd + 1) % 4
            else:
                nowx, nowy = x, y
            
            if vis[nowx][nowy] & (1 << nowd) == 0:
                if vis[nowx][nowy] == 0:
                    res += 1
                vis[nowx][nowy] |= (1 << nowd)
            else:
                break

        return res
''',
    call=f'Solution().numberOfCleanRooms({ROOM})',
    expect=7,
    skip=['dx = [', 'dy = [', 'm = len', 'n = len', 'x = nowx', 'y = nowy'],
    views=[
        dict(type='text', fn=_dir),
        dict(type='grid', var='room', label='room（黑 = 障碍 1；绿 = 清扫过；蓝框 = 机器人）', cell=100, h=330,
             color=lambda S, i, j, v: ('green' if 'vis' in S and S['vis'][i][j] else None),
             cursors=[('nowx', 'nowy', 'blue')]),
        dict(type='grid', var='vis', label='vis（位掩码：bit0 向右 / bit1 向下 / bit2 向左 / bit3 向上）', cell=100, h=330,
             color=lambda S, i, j, v: 'yellow' if v else None,
             cursors=[('nowx', 'nowy', 'blue')]),
    ],
    watch=[('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue'), ('nowd', 'nowd', 'pink'), ('res', 'res', 'green')],
    captions={
        'vis = [[0]': '`vis[x][y]` 是 4 位二进制：记录从哪几个方向到过 `(x, y)`',
        'nowx, nowy, nowd = 0, 0, 0': '机器人从 `(0, 0)` 出发，朝向 `0` = 向右',
        'vis[0][0] = 1': '起点已经朝右到过：`vis[0][0] = 1`',
        'res = 1': '起点本身算清扫过一格：`res = 1`',
        'while True': '机器人不会自己停 → 靠“状态重复”来判断结束',
        'if x < 0 or y < 0': _if,
        'nowd = (nowd + 1) % 4': lambda S, B, r: f'撞到墙或障碍：右转，`nowd = {S.nowd}`（朝{DN[S.nowd]}），位置不动',
        'nowx, nowy = x, y': '前方可走：前进到 `({nowx},{nowy})`，朝向不变',
        'if vis[nowx][nowy] & (1 << nowd) == 0': _vis,
        'if vis[nowx][nowy] == 0': lambda S, B, r: ('`vis` 为 0：这个格子==从没来过== → 清扫数 +1' if S.vis[S.nowx][S.nowy] == 0
                                                    else f'`vis = {S.vis[S.nowx][S.nowy]}`：格子来过（换了个方向），不重复计数'),
        'res += 1': '新格子：`res` → =={res}==',
        '|= (1 << nowd)': '记下状态：`vis[{nowx}][{nowy}] = {vis[nowx][nowy]}`',
        'break': '回到了走过的（位置, 方向）→ 从此无限循环，停止模拟',
        'return res': '一共清扫了 `{res}` 个格子',
    },
    cards=dict(
        one_liner='机器人一直走：状态 = 位置 + 方向，重复就停',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`room[i][j]`：`0` 是空格子，`1` 是障碍物，机器人从 `(0,0)` 朝右出发',
                 '前方是空格子就前进，撞墙或障碍物就==原地右转 90 度==，永远不会停',
                 '求它清扫过的不同格子数',
                 '示例：`[[0,0,0],[1,1,0],[0,0,0]]` → `7`'],
        quote='除了常规的二维空间位置信息外，机器人自身还具备一个方向信息，因此需要将这三个信息综合起来进行去重，接下来就只需要模拟机器人的行动，直到再次走到一个之前出已经现过的状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，直接模拟机器人的每一步',
              '光看位置去重不够：同一格朝不同方向，后续路线不同 → 状态是 ==(x, y, 方向)==',
              '用 `vis[x][y]` 的 4 个二进制位，记录四个方向有没有来过'],
        summary=['时间 `O(mn)`：状态数最多 `4mn`，每个状态至多出现一次',
                 '易错：计数要看 `vis == 0`（格子第一次到），而不是状态是否新',
                 '易错：撞墙右转后，也要把新朝向在当前格登记一次',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
