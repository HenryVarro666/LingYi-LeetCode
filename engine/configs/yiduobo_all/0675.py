FOREST = [[1, 0, 3], [2, 0, 4], [5, 6, 7]]


def _color(S, i, j, v):
    if 'rnd' not in S or 'used' not in S:
        return None
    if (i, j) == (S.get('next_x'), S.get('next_y')):
        return 'pink'
    if S['used'][i][j] == S['rnd'] + 1:
        return 'green'
    return None


def _txt(S):
    if 'next_x' not in S:
        return ''
    return (f"第 `{S['rnd'] + 1}` 棵：从 `({S['start_x']},{S['start_y']})` 走到高 `{S['height']}` 的树 `({S['next_x']},{S['next_y']})`，"
            f"本轮 BFS 层数 `{S.get('step', 0)}`，累计 ==`{S['res']}`==")


CONFIG = dict(
    num=675, title='为高尔夫比赛砍树', difficulty='Hard', category='网格图',
    author='yiduobo', technique='按高度排序 + 多轮 BFS',
    tags=[],
    code='''
class Solution(object):
    def cutOffTree(self, forest):

        m = len(forest)
        n = len(forest[0])

        pos_list = []
        for i in range(m):
            for j in range(n):
                if forest[i][j] > 1:
                    pos_list.append([i, j, forest[i][j]])
        
        start_x, start_y = 0, 0
        used = [[0] * n for _ in range(m)]
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        res = 0
        for rnd, [next_x, next_y, height] in enumerate(sorted(pos_list, key=lambda d:d[2])):
            q = [[start_x, start_y]]
            used[start_x][start_y] = rnd + 1
            l = 0
            r = 1
            step = 0
            while l < r:
                step += 1
                for index in range(l, r):
                    nowx, nowy = q[index]
                    for direct in range(4):
                        x = nowx + dx[direct]
                        y = nowy + dy[direct]
                        if x >= 0 and x < m and y >= 0 and y < n and forest[x][y] > 0 and used[x][y] < rnd + 1:
                            used[x][y] = rnd + 1
                            if x == next_x and y == next_y:
                                res += step
                                break
                            q.append([x, y])

                    if used[next_x][next_y] == rnd + 1:
                        break

                if used[next_x][next_y] == rnd + 1:
                    break

                l, r = r, len(q)
            
            if used[next_x][next_y] != rnd + 1:
                return -1

            start_x, start_y = next_x, next_y

        return res
''',
    call=f'Solution().cutOffTree({FOREST})',
    expect=12,
    skip=['m = len', 'n = len', 'pos_list = []', 'for i in range(m)', 'for j in range(n)', 'pos_list.append',
          'used = [[', 'dx = [', 'dy = [', 'res = 0', 'l = 0', 'r = 1', 'step = 0', 'for direct in range(4)',
          'x = nowx', 'y = nowy', 'q.append', 'if forest[i][j] > 1', 'break', 'for index in range(l, r)'],
    max_steps=80,
    views=[
        dict(type='grid', var='forest', label='forest（0 障碍；粉 = 目标树；绿 = 本轮到过）', cell=100, h=330,
             color=_color, cursors=[('start_x', 'start_y', 'orange'), ('nowx', 'nowy', 'blue')]),
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var=lambda S: [f'{a}{b}' for a, b in S['q']] if 'q' in S else None,
             label='q：本轮 BFS 队列（x y 连写）', cell=70, h=140,
             dim=lambda S, i, v: i < S.get('l', 0)),
    ],
    watch=[('res', 'res', 'green'), ('rnd', 'rnd', 'orange'), ('step', 'step', 'blue'), ('height', 'height', 'pink')],
    captions={
        'start_x, start_y = 0, 0': '起点 `(0, 0)`',
        'for rnd, [next_x': '==按高度从矮到高==砍：第 `{rnd + 1}` 棵在 `({next_x},{next_y})`，高 `{height}`',
        'q = [[start_x, start_y]]': '这一轮从当前位置 `({start_x},{start_y})` 做 BFS 找下一棵树',
        'used[start_x][start_y] = rnd + 1': '`used` 记「第几轮访问过」：用轮号当标记，==不用每轮重置==',
        'while l < r': lambda S, B, r: (f'当前层有 `{B.r - B.l}` 个格子，继续' if B.l < B.r else '队列空了'),
        'step += 1': '往外扩一层，距离 `step` = {step}',
        'nowx, nowy = q[index]': '取出 `({nowx},{nowy})`，看它的四个邻居',
        'if x >= 0 and x < m': lambda S, B, r: (
            f'`({S.x},{S.y})` 出界' if not (0 <= S.x < S.m and 0 <= S.y < S.n) else
            f'`({S.x},{S.y})` 是障碍 → 不走' if S.forest[S.x][S.y] == 0 else
            f'`({S.x},{S.y})` 本轮已访问 → 不走' if S.used[S.x][S.y] >= S.rnd + 1 else
            f'`({S.x},{S.y})` 可走'),
        'used[x][y] = rnd + 1': '标记 `({x},{y})` 本轮已访问',
        'if x == next_x and y == next_y': lambda S, B, r: ('==找到目标树== → 本轮结束' if (S.x == S.next_x and S.y == S.next_y) else f'`({S.x},{S.y})` 不是目标 `({S.next_x},{S.next_y})`，入队'),
        'res += step': '这棵树的最短距离就是 `step = {step}`，累计 `res` = =={res}==',
        'if used[next_x][next_y] == rnd + 1:': lambda S, B, r: ('目标已被访问到 → ==跳出==，不用再扫' if S.used[S.next_x][S.next_y] == S.rnd + 1 else '目标还没访问到 → 继续'),
        'l, r = r, len(q)': '这层扩完，下一层是 `[{l}, {r})`',
        'if used[next_x][next_y] != rnd + 1': lambda S, B, r: ('目标没访问到 → ==砍不到这棵树，返回 -1==' if S.used[S.next_x][S.next_y] != S.rnd + 1 else '本轮到达了目标，继续下一棵'),
        'start_x, start_y = next_x, next_y': '砍倒这棵树，==下一轮从这里出发==：`({start_x},{start_y})`',
        'return -1': '有树够不到 → `-1`',
        'return res': '全部砍完，总步数 `{res}`',
    },
    cards=dict(
        one_liner='树必须从矮到高砍，所以相邻两棵之间各做一次 BFS',
        complexity='时间 `O((mn)²)`，空间 `O(mn)`',
        problem=['`m × n` 的森林：`0` 是障碍，`1` 是平地，大于 1 是一棵树（数值是高度）',
                 '从 `(0,0)` 出发，==必须按树高从小到大==砍，砍完该格变平地',
                 '求砍完所有树的最少步数，有树够不到返回 `-1`',
                 '本视频：`[[1,0,3],[2,0,4],[5,6,7]]` → `12`'],
        quote='直接按题目要求，按树的高度排序，每一轮做一次bfs是比较直观的做法。',
        quote_src='—— yiduobo 题解原文',
        idea=['先收集所有树并按高度排序，砍树顺序就固定了',
              '每相邻两棵树做一次 BFS，路径长度累加',
              '`used[x][y] = 轮号` 当 visited，省得每轮重新清零'],
        summary=['时间 `O((mn)²)`：最多 mn 棵树，每次 BFS `O(mn)`',
                 '易错：起点 `(0,0)` 若是树，排序后第一棵路程可能是 0',
                 '`used` 用轮号标记，所以判断是 `used[x][y] < rnd + 1`',
                 '作者也提到没找到更好的优化，这里是最朴素的多轮 BFS',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改'],
    ),
)
