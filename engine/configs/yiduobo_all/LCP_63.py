_ARR = ['右 →', '下 ↓', '左 ←', '上 ↑']


def _cell(S, i, j, v):
    if v == 'O':
        return 'green'
    if v == 'W':
        return 'pink'
    if v == 'E':
        return 'blue'
    return None


def _info(S):
    inn = S['_inner']
    if 'nowd' not in inn:
        return '`O` 洞（绿）、`W` 逆时针转向器（粉）、`E` 顺时针转向器（蓝）、`.` 空地'
    x, y, d = inn['nowx'], inn['nowy'], inn['nowd']
    return f"dfs 正在看 `({x},{y})`，以方向 =={_ARR[d]}== 到达；`f[{x}][{y}] = {S['f'][x][y]}`"


def _memo(S):
    f = S.get('f')
    if f is None:
        return ''
    rows = []
    for i, r in enumerate(f):
        for j, c in enumerate(r):
            for d, v in enumerate(c):
                if v is not None:
                    rows.append(f'`({i},{j}){"→↓←↑"[d]}`={v}')
    return '已记忆 `f[x][y][d]`：' + ('，'.join(rows) if rows else '（空）')


CONFIG = dict(
    num='LCP 63', title='弹珠游戏', difficulty='Medium', category='网格图',
    author='yiduobo', technique='枚举起点 + 记忆化搜索 f[x][y][d]',
    tags=['灵神核心路线', '灵神题单·网格图'],
    code='''
class Solution(object):
    def ballGame(self, num, plate):

        n = len(plate)
        m = len(plate[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        f = [[[None] * 4 for _ in range(m)] for _ in range(n)]
        res = []

        def dfs(nowx, nowy, nowd):
            if f[nowx][nowy][nowd] is not None:
                return f[nowx][nowy][nowd]

            if plate[nowx][nowy] == 'O':
                f[nowx][nowy][nowd] = 0
                return 0
                
            if plate[nowx][nowy] == '.':
                d = nowd
            elif plate[nowx][nowy] == 'E':
                d = (nowd + 1) % 4
            else:
                d = (nowd + 3) % 4
                
            x = nowx + dx[d]
            y = nowy + dy[d]
            if x < 0 or x == n or y < 0 or y == m:
                f[nowx][nowy][nowd] = num + 1
                return num + 1
            
            f[nowx][nowy][nowd] = dfs(x, y, d) + 1
            return f[nowx][nowy][nowd]

        for index in range(1, m - 1):
            if plate[0][index] == '.' and dfs(0, index, 1) <= num:
                res.append([0, index])
            if plate[n - 1][index] == '.' and dfs(n - 1, index, 3) <= num:
                res.append([n - 1, index])
        
        for index in range(1, n - 1):
            if plate[index][0] == '.' and dfs(index, 0, 0) <= num:
                res.append([index, 0])
            if plate[index][m - 1] == '.' and dfs(index, m - 1, 2) <= num:
                res.append([index, m - 1])
        
        return res
''',
    call='Solution().ballGame(4, ["..E.", ".EOW", "..W."])',
    expect=[[2, 1]],
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='grid', var='plate', label='plate（黄 = dfs 当前所在格）', cell=110, h=360,
             color=_cell, cursors=[(lambda S: S['_inner'].get('nowx'), lambda S: S['_inner'].get('nowy'), 'yellow')]),
        dict(type='text', fn=_memo, size=22, h=90),
        dict(type='calls', h=170, hide=('ballGame',)),
    ],
    watch=[('num', 'num', 'cyan'), ('res', 'res', 'green')],
    skip=['n = len', 'm = len', 'dx = [', 'dy = [', 'res = []', 'for index in range'],
    max_steps=70,
    captions={
        'f = [[[None]': '`f[x][y][d]` = 弹珠以方向 `d` 来到 `(x,y)` 后，==还要几步入洞==；`None` 表示没算过',
        'if f[nowx][nowy][nowd] is not None': lambda S, B, r: (f'`f[{S.nowx}][{S.nowy}][{S.nowd}] = {B.f[S.nowx][S.nowy][S.nowd]}`：这个状态算过了 → ==直接返回记忆值=='
                                                               if B.f[S.nowx][S.nowy][S.nowd] is not None
                                                               else f'`({S.nowx},{S.nowy})` 朝 {_ARR[S.nowd]} 还没算过，继续'),
        "== 'O'": lambda S, B, r: (f'`({S.nowx},{S.nowy})` 是洞' if S.plate[S.nowx][S.nowy] == 'O'
                                   else f'`({S.nowx},{S.nowy})` 是 `{S.plate[S.nowx][S.nowy]}`，不是洞'),
        'f[nowx][nowy][nowd] = 0': '入洞，还需 `0` 步：`f = 0`',
        "plate[nowx][nowy] == '.'": lambda S, B, r: ('是空地 `.`：方向不变' if S.plate[S.nowx][S.nowy] == '.' else '不是空地，看是不是转向器'),
        'd = nowd': lambda S, B, r: f'`d = nowd = {S.d}`：方向不变，仍然朝 {_ARR[S.d]}',
        "== 'E'": lambda S, B, r: ('是 `E`（顺时针转向器）' if S.plate[S.nowx][S.nowy] == 'E' else '不是 `E`，那只能是 `W`'),
        'd = (nowd + 1) % 4': lambda S, B, r: f'顺时针：方向下标 `+1` → `d = {S.d}`（=={_ARR[S.d]}==）',
        'd = (nowd + 3) % 4': lambda S, B, r: f'只剩 `W`（逆时针）：方向下标 `-1`，写成 `+3` 防负数 → `d = {S.d}`（=={_ARR[S.d]}==）',
        'x = nowx + dx[d]': lambda S, B, r: f'沿 =={_ARR[S.d]}== 前进一格，到 `({S.nowx + [0,1,0,-1][S.d]}, {S.nowy + [1,0,-1,0][S.d]})`',
        'y = nowy + dy[d]': '`y = {y}`',
        'if x < 0 or x == n': lambda S, B, r: (f'`({S.x},{S.y})` 出界 → 永远入不了洞，记为 `num + 1 = {S.num + 1}`'
                                                if (S.x < 0 or S.x == S.n or S.y < 0 or S.y == S.m)
                                                else f'`({S.x},{S.y})` 还在盘内，继续往下走'),
        'f[nowx][nowy][nowd] = num + 1': '`f[{nowx}][{nowy}][{nowd}] = {num + 1}`：==步数超限的哨兵值==',
        'f[nowx][nowy][nowd] = dfs(x, y, d) + 1': lambda S, B, r: (f'`f[{S.nowx}][{S.nowy}][{S.nowd}] = dfs({S.x},{S.y},{S.d}) + 1` = =={S.f[S.nowx][S.nowy][S.nowd]}==：下一格需要几步，再加这一步'
                                                                   if S.f[S.nowx][S.nowy][S.nowd] is not None else '递归：先去算下一格'),
        'return f[nowx][nowy][nowd]': '下一格的结果 `+ 1`：`f[{nowx}][{nowy}][{nowd}] = {f[nowx][nowy][nowd]}`，返回上一层',
        "plate[0][index] == '.'": lambda S, B, r: (f'上边入口 `(0,{S.index})`：空地才能打入，方向朝下；`dfs(...) <= num` 才算入洞' if S.plate[0][S.index] == '.'
                                                   else f'上边入口 `(0,{S.index})` 是 `{S.plate[0][S.index]}`，不能打入'),
        "plate[n - 1][index] == '.'": lambda S, B, r: (f'下边入口 `({S.n - 1},{S.index})`：空地才能打入，方向朝上' if S.plate[S.n - 1][S.index] == '.'
                                                       else f'下边入口 `({S.n - 1},{S.index})` 是 `{S.plate[S.n - 1][S.index]}`，不能打入'),
        "plate[index][0] == '.'": lambda S, B, r: (f'左边入口 `({S.index},0)`：空地才能打入，方向朝右' if S.plate[S.index][0] == '.'
                                                   else f'左边入口 `({S.index},0)` 是 `{S.plate[S.index][0]}`，不能打入'),
        "plate[index][m - 1] == '.'": lambda S, B, r: (f'右边入口 `({S.index},{S.m - 1})`：空地才能打入，方向朝左' if S.plate[S.index][S.m - 1] == '.'
                                                       else f'右边入口 `({S.index},{S.m - 1})` 是 `{S.plate[S.index][S.m - 1]}`，不能打入'),
        'res.append': '步数 `<= num`：这个入口能入洞，加入 `res`：`{res}`',
        'return res': '全部入口枚举完：`{res}`',
    },
    cards=dict(
        one_liner='把“到这里还要几步入洞”记成 f[x][y][d]，起点只看是否 ≤ num',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['弹珠盘 `plate`：`O` 洞、`W` 逆时针转向器、`E` 顺时针转向器、`.` 空地',
                 '只能在边缘空地（不含四角）、沿垂直于边缘的方向打入，最多前进 `num` 步',
                 '返回所有能让弹珠入洞的打入位置',
                 '本视频：`num = 4`，`plate = ["..E.",".EOW","..W."]` → `[[2,1]]`'],
        quote='当某个弹珠以方向d来到位置(x, y)时，其最终结局其实也已经固定死了，那么在这里完全可以使用f[x][y][d]记录弹珠以方向d来到(x, y)时，在多少步内可以落入洞中。',
        quote_src='—— yiduobo 题解原文',
        idea=['打入后路径固定，所以枚举每个起点，各自做记忆化搜索',
              '`f[x][y][d]` = 入洞所需步数；出界记 `num + 1`，表示“入不了洞”',
              '方向数组按右、下、左、上排：右转 `+1`，左转 `-1`（写成 `+3`）'],
        summary=['时间空间 `O(mn)`：状态（位置，方向）共 `4mn` 个，每个只算一次',
                 '哨兵值 `num + 1`：出界或超限时统一大于 `num`，最后只需比较 `<= num`',
                 '递归深度最多 `4mn`，大盘面时 Python 要注意递归上限',
                 '原文是 Python 2 风格，在 Python 3 下无需改动即可运行',
                 '对比灵神：他直接循环模拟、不记忆，因为不同入口的路径本来就不重叠'],
    ),
)
