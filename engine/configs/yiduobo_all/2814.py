LAND = [['D', '.', '*'], ['.', '.', 'S']]


def _color(S, i, j, v):
    if 'person_pos' not in S:
        return None
    if [i, j] in S['person_pos']:
        return 'green'
    if [i, j] in S['water_pos']:
        return 'blue'
    if v == 'D':
        return 'orange'
    return None


CONFIG = dict(
    num=2814, title='避免淹死并到达目的地的最短时间', difficulty='Hard', category='网格图',
    author='yiduobo', technique='水与人双 BFS（水先扩展）',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def minimumSeconds(self, land):

        m = len(land)
        n = len(land[0])

        person_pos = []
        water_pos = []
        for i in range(m):
            for j in range(n):
                if land[i][j] == 'S':
                    person_pos.append([i, j])
                elif land[i][j] == '*':
                    water_pos.append([i, j])

        person_head, person_tail = 0, len(person_pos)
        water_head, water_tail = 0, len(water_pos)
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        res = 0
        while person_head < person_tail:
            res += 1

            for nowx, nowy in water_pos[water_head : water_tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if x >= 0 and x < m and y >= 0 and y < n and land[x][y] == '.':
                        land[x][y] = '*'
                        water_pos.append([x, y])
            
            water_head, water_tail = water_tail, len(water_pos)

            for nowx, nowy in person_pos[person_head : person_tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if x >= 0 and x < m and y >= 0 and y < n and (land[x][y] == '.' or land[x][y] == 'D'):
                        if land[x][y] == 'D':
                            return res
                        land[x][y] = '*'
                        person_pos.append([x, y])
            
            person_head, person_tail = person_tail, len(person_pos)
        
        return -1
''',
    call=f'Solution().minimumSeconds({LAND})',
    expect=3,
    skip=['m = len', 'n = len', 'person_pos = []', 'water_pos = []', 'for i in range(m)', 'for j in range(n)', "if land[i][j] == 'S'", "elif land[i][j] == '*'",
          'dx = [', 'dy = [', 'for d in range(4)', 'x = nowx', 'y = nowy', 'person_pos.append([x, y])', 'water_pos.append([x, y])',
          'person_head, person_tail = 0', 'water_head, water_tail = 0'],
    max_steps=80,
    views=[
        dict(type='grid', var='land', label='land（绿 = 人走过/所在，蓝 = 水，橙 = 终点 D）', cell=120, h=470,
             color=_color, cursors=[('nowx', 'nowy', 'yellow'), ('x if _line in (29, 30, 39, 40) else None', 'y', 'pink')]),
        dict(type='text', fn=lambda S: f"第 `{S['res']}` 秒：先水扩展，再人扩展" if 'res' in S else ''),
    ],
    watch=[('res', 'res', 'green'), 'person_head', 'person_tail', 'water_head', 'water_tail'],
    captions={
        'person_pos.append([i, j])': '`({i},{j})` 是人的起点 `S`：记入 `person_pos`，BFS 从这里出发',
        'water_pos.append([i, j])': '`({i},{j})` 是水 `*`：记入 `water_pos`，它们是第 0 秒的水头',
        "== '.':": lambda S, B, r: (f'水看 `({S.x},{S.y})`：棋盘内的空地 → ==淹没它==' if (0 <= S.x < S.m and 0 <= S.y < S.n and S.land[S.x][S.y] == '.') else f'水看 `({S.x},{S.y})`：越界、石头、已淹或终点，水进不去'),
        "or land[x][y] == 'D')": lambda S, B, r: (f'人看 `({S.x},{S.y})`：棋盘内的空地或终点 → ==可以走==' if (0 <= S.x < S.m and 0 <= S.y < S.n and S.land[S.x][S.y] in '.D') else f'人看 `({S.x},{S.y})`：越界、石头，或已被水淹/走过 → 不能走'),
        'while person_head < person_tail': lambda S, B, r: (
            f'人这一层还有 `{S.person_tail - S.person_head}` 个位置能出发 → 继续' if S.person_head < S.person_tail
            else '人已无路可走（队列空）→ 退出，返回 `-1`'),
        'res += 1': '新的一秒：==先让水扩展，再让人走==。`res = {res}`',
        'for nowx, nowy in water_pos': '水的这一层：从 `({nowx},{nowy})` 向四周漫',
        "land[x][y] = '*'": lambda S, B, r: (f'`({S.x},{S.y})` 被淹没，标成 `*`' if S._line < 33
                                             else f'人走到 `({S.x},{S.y})` 并标成 `*`：水以后不会再让人回头走，也防重复入队'),
        'water_head, water_tail = water_tail': '水这一层扩完：下一层从 `water_head = {water_head}` 开始',
        'for nowx, nowy in person_pos': '人的这一层：从 `({nowx},{nowy})` 向四周走',
        "if land[x][y] == 'D'": lambda S, B, r: (f'`({S.x},{S.y})` 就是终点 `D` → ==人在第 {S.res} 秒到达==，直接返回'
                                                 if S.land[S.x][S.y] == 'D' else f'`({S.x},{S.y})` 是空地，不是终点 → 人走过去'),
        'person_head, person_tail = person_tail': '人这一层走完：下一层从 `person_head = {person_head}` 开始',
        'return -1': '人被水困住，到不了终点 → `-1`',
        'return res': '先扩水再走人，人踏进 `D` 时水还没淹到：答案 `{res}` 秒',
    },
    cards=dict(
        one_liner='水和人同时 BFS：每一秒先让水漫，再让人走',
        complexity='时间 `O(m × n)`，空间 `O(m × n)`',
        problem=['`land` 里 `.` 空地，`X` 石头，`*` 水，`S` 人起点，`D` 终点',
                 '每秒水向四邻的空地扩散，人也可走到相邻空地；==水淹过的格子人不能进==，终点水不会淹',
                 '本视频：`[["D",".","*"],[".",".","S"]]` → `3`'],
        quote='让水和人同时开始执行bfs，每一轮先让水进行扩展，然后人再进行扩展，直到人走到目的地或者无路可走为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['`water_pos`、`person_pos` 各是一个数组队列，`head:tail` 是当前层',
              '==水先扩展==：这样人只会走到「这一秒水没淹到」的格子',
              '人走过的格子也写成 `*`，等于不让人走回头路'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '顺序不能反：先扩水再走人，否则人会踏进这一秒刚被淹的格子',
                 '人走到 `D` 直接返回 `res`，水不会淹终点所以不用先判水',
                 '人的队列走空还没到 `D` 就返回 `-1`；代码会改写 `land`',
                 '原文是 Python 2 风格的类，代码无需修改；与「火势蔓延」同类'],
    ),
)
