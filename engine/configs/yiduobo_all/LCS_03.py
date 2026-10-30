G0 = ['1133', '1233', '1101']


def _col(S, i, j, v):
    b = S.get('belong')
    if b is None or b[i][j] is None:
        return None
    return 'red' if b[i][j] in S['near_part'] else 'green'


def _nb(S, B, r):
    x, y = S.x, S.y
    m, n = B.m, B.n
    k = B.part_cnt
    if x < 0 or x == m or y < 0 or y == n:
        return f'`({x},{y})` 在==界外== → 块 {k} 贴边界，记入 `near_part`'
    c = B.grid[x][y]
    if c == '0':
        return f'`({x},{y})` 是走廊 → 块 {k} 贴走廊，记入 `near_part`'
    if c != B.grid[B.i][B.j]:
        return f'`({x},{y})` 是别的数字 `{c}` → 不属于本块，不扩展'
    if B.belong[x][y] is not None:
        return f'`({x},{y})` 同数字但已在块里 → 不重复入队'
    return f'`({x},{y})` 同数字且没处理过 → ==入队==并标上块编号 {k}'


CONFIG = dict(
    num='LCS 03', title='主题空间', difficulty='Medium', category='网格图',
    author='yiduobo', technique='floodfill（BFS）标记连通块',
    tags=['灵神核心路线', '灵神题单·网格图'],
    code='''
class Solution(object):
    def largestArea(self, grid):

        m = len(grid)
        n = len(grid[0])

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        belong = [[None] * n for _ in range(m)]
        part_cnt = 0
        part_len = []
        near_part = set()

        for i in range(m):
            for j in range(n):
                if grid[i][j] != '0' and belong[i][j] is None:
                    belong[i][j] = part_cnt
                    q = [[i, j]]
                    head, tail = 0, 1
                    while head < tail:
                        nowx, nowy = q[head]
                        head += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x < 0 or x == m or y < 0 or y == n or grid[x][y] == '0':
                                near_part.add(part_cnt)
                            elif grid[x][y] == grid[i][j] and belong[x][y] is None:
                                belong[x][y] = part_cnt
                                q.append([x, y])
                                tail += 1

                    part_cnt += 1
                    part_len.append(tail)

        res = 0
        for index, length in enumerate(part_len):
            if index not in near_part:
                res = max(res, length)

        return res
''',
    call=f'Solution().largestArea({G0})',
    expect=1,
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'belong = [[', 'part_cnt = 0', 'part_len = []', 'near_part = set',
          'if grid[i][j] != ', 'for index, length in enumerate', 'head += 1', 'while head < tail', 'elif grid[x][y] ==', 'belong[x][y] = part_cnt', 'near_part.add', 'for index in range(4)', 'x = nowx', 'y = nowy', 'q.append', 'tail += 1', 'for i in range', 'for j in range',
          'res = 0', 'part_cnt += 1', 'head, tail = 0, 1', 'q = [[i, j]]'],
    max_steps=100,
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已归块；红 = 贴走廊/边界的块；黄框 = 起点；蓝框 = 出队；粉框 = 邻居）', cell=84, h=300,
             color=_col, cursors=[('i', 'j', 'yellow'), ('nowx', 'nowy', 'blue'),
                                  ('x if _line == 27 else None', 'y', 'pink')]),
        dict(type='array', var=lambda S: [f'块{k}:{l}' for k, l in enumerate(S['part_len'])] if S.get('part_len') else None,
             label='part_len（各连通块大小）', cell=96, h=120),
        dict(type='text', fn=lambda S: ('贴走廊或边界的块：`' + str(sorted(S['near_part'])) + '`') if 'near_part' in S else '', size=30, h=50),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail'), ('part_cnt', 'part_cnt'), ('res', 'res', 'green')],
    captions={
        'if grid[i][j] != ': lambda S, B, r: (
            f'`({S.i},{S.j})` 是数字 `{S.grid[S.i][S.j]}` 且没处理过 → 新连通块 `{S.part_cnt}`，从这里 BFS'
            if S.grid[S.i][S.j] != '0' and B.belong[S.i][S.j] is None else f'`({S.i},{S.j})` 是走廊或已处理过 → 跳过'),
        'belong[i][j] = part_cnt': '扫描到 `({i},{j})`：数字 `{grid[i][j]}` 且没处理过 → ==新连通块 {part_cnt}==，起点打上编号，从这里 BFS',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：队列不空，继续扩展' if B.head < B.tail
                                              else f'`head == tail`：这个块扩展完，大小 `tail` = =={B.tail}=='),
        'nowx, nowy = q[head]': '出队 `({nowx},{nowy})`，看四个邻居',
        'if x < 0 or x == m': _nb,
                'part_len.append': '队列空了，块 `{part_cnt - 1}` 扩展完，大小 `tail` = =={tail}==：`part_len = {part_len}`',
        'if index not in near_part': lambda S, B, r: (
            f'块 `{S.index}`（大小 {S.length}）贴走廊或边界 → 不满足要求' if S.index in S.near_part
            else f'块 `{S.index}`（大小 {S.length}）不贴走廊也不贴边界 → 候选'),
        'res = max': '`res = max({B.res}, {length}) = {res}`：用这个候选块更新答案',
        'return res': '最大且不与走廊相邻的主题空间面积 =={res}==',
    },
    cards=dict(
        one_liner='floodfill 求每块同数字区域，再挑不贴走廊的最大块',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`grid` 中 `0` 是走廊，相同数字相连成一个主题空间',
                 '要找一个==不与走廊相邻==、也不在边界上的主题空间',
                 '返回满足条件的最大面积，没有则返回 `0`',
                 '示例：`["1133","1233","1101"]` → `1`'],
        quote='若在遍历过程中来到了边界，或者与0相邻，那么说明当前的连通块与走廊相邻。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每格，遇到没处理的非 0 格就 BFS，只扩展数字相同的格子',
              'BFS 途中碰到边界或 `0`，就把这块编号加入 `near_part`',
              '最后在不属于 `near_part` 的块里取最大面积'],
        summary=['时间 `O(mn)`：每个格子最多入队一次',
                 '易错：BFS 只扩展与起点数字相同的格子，碰到别的数字什么也不做',
                 '块的大小直接用 `tail`，因为每个入队的格子都计入',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
