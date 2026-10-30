GRID = ["@a.", "#A#", "#b#"]


def _keys(S):
    if 'now_state' not in S or 'key_num' not in S:
        return ''
    ks = [chr(97 + k) for k in range(S['key_num']) if S['now_state'] >> k & 1]
    return f"当前出队状态：位置 `({S['nowx']},{S['nowy']})`，已持钥匙 ==" + (' '.join(ks) if ks else '无') + f"==（二进制 `{S['now_state']:0{S['key_num']}b}`），第 `{S['step']}` 轮"


def _cur(S, i, j, v):
    if 'nowx' in S and (i, j) == (S['nowx'], S['nowy']):
        return 'blue'
    if 'used' in S and any(S['used'][i][j]) and v != '#':
        return None
    return None


CONFIG = dict(
    num=864, title='获取所有钥匙的最短路径', difficulty='Hard', category='网格图',
    author='yiduobo', technique='状态压缩 BFS（位置 + 钥匙集合）',
    tags=['灵神题单·网格图', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def shortestPathAllKeys(self, grid):

        m = len(grid)
        n = len(grid[0])
        max_key = 'a'
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '@':
                    start_x = i
                    start_y = j
                elif grid[i][j] != '#' and grid[i][j] != '.':
                    if grid[i][j] > max_key:
                        max_key = grid[i][j]
        
        key_num = ord(max_key) - 96
        used = [[[False] * (1 << key_num) for _ in range(n)] for _ in range(m)]
        used[start_x][start_y][0] = True
        q = [[start_x, start_y, 0]]
        l = 0
        r = 1
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        step = 0
        while l < r:
            step += 1
            for nowx, nowy, now_state in q[l:r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] != '#':
                        if grid[x][y] == '.' or grid[x][y] == '@':
                            if not used[x][y][now_state]:
                                q.append([x, y, now_state])
                                used[x][y][now_state] = True
                        elif grid[x][y] >= 'a' and grid[x][y] <= max_key:
                            state = now_state | (1 << (ord(grid[x][y]) - 97))
                            if state == (1 << key_num) - 1:
                                return step
                            if not used[x][y][state]:
                                q.append([x, y, state])
                                used[x][y][state] = True
                        elif (now_state & (1 << (ord(grid[x][y]) - 65))) and not used[x][y][now_state]:
                                q.append([x, y, now_state])
                                used[x][y][now_state] = True

            l, r = r, len(q)
        
        return -1
''',
    call=f'Solution().shortestPathAllKeys({GRID})',
    expect=3,
    views=[
        dict(type='text', fn=_keys, h=60),
        dict(type='grid', var='grid', cursors=[('nowx', 'nowy', 'blue', '出队'), ('x', 'y', 'yellow', '邻居')],
             color=lambda S, i, j, v: ('green' if v in 'abcdefghijklmnopqrstuvwxyz' else 'orange' if v.isupper() else 'pink' if v == '@' else None) if isinstance(v, str) else None,
             h=330),
        dict(type='queue', var='q', fmt=lambda e: f'({e[0]},{e[1]}):{e[2]:b}', label='q（位置:钥匙二进制）', h=110),
    ],
    watch=[('step', 'step', 'yellow'), ('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue'), ('now_state', 'now_state', 'green'), ('l', 'l'), ('r', 'r')],
    skip=['for i in range(m)', 'for j in range(n)', "if grid[i][j] == '@'", "elif grid[i][j] !=", 'if grid[i][j] > max_key', 'start_x = i', 'start_y = j', 'dx = [', 'dy = [', 'l = 0', 'r = 1', 'for index in range(4)', 'x = nowx', 'y = nowy', 'm = len', 'n = len'],
    max_steps=110,
    captions={
        "max_key = 'a'": '`max_key`：先设为 `a`，扫描网格找出最大的钥匙字母，就知道一共有几把钥匙',
        'max_key = grid': '扫描完网格：最大钥匙是 `{max_key}`，起点在 `({start_x},{start_y})`',
        'key_num = ': '钥匙数 `key_num = {key_num}`：最多 6 把 → 用 ==二进制位表示持有哪些钥匙==',
        'used = [[[': '`used[x][y][state]`：站在 `(x,y)`、手里钥匙集合为 `state` 的状态是否访问过。==位置相同、钥匙不同算不同状态==',
        'used[start_x][start_y][0] = True': '起点入队：位置 `({start_x},{start_y})`，钥匙集合 `0`（一把都没有）',
        'q = [[start_x': '队列 `q` 放 `[x, y, 钥匙集合]`',
        'step += 1': '==BFS 一层 = 走一步==：现在处理第 `{step}` 轮的所有状态',
        'for nowx, nowy, now_state in q[l:r]': '遍历当前层 `q[{l}:{r}]`：处理位置 `({nowx},{nowy})`、钥匙 `{now_state:b}` 的状态（取完则这一层结束）',
        "if x >= 0 and x < m": lambda S, B, r: (f"邻居 `({S.x},{S.y})` 在界内且不是墙 → 继续判断" if (0 <= S.x < S.m and 0 <= S.y < S.n and S.grid[S.x][S.y] != '#') else f"邻居 `({S.x},{S.y})` 越界或是墙 → 不能走"),
        "if grid[x][y] == '.'": lambda S, B, r: (f"邻居是空地 `{S.grid[S.x][S.y]}`，无需特殊处理" if S.grid[S.x][S.y] in '.@' else f"邻居是 `{S.grid[S.x][S.y]}`，不是空地"),
        'if not used[x][y][now_state]': lambda S, B, r: ('这个（位置, 钥匙）状态没来过 → 入队' if not S.used[S.x][S.y][S.now_state] else '这个（位置, 钥匙）状态已访问过 → ==BFS 最先到达的一定最短==，不再入队'),
        "elif grid[x][y] >= 'a'": lambda S, B, r: (f"邻居 `{S.grid[S.x][S.y]}` 是钥匙" if 'a' <= S.grid[S.x][S.y] <= S.max_key else f"邻居 `{S.grid[S.x][S.y]}` 是门"),
        'state = now_state |': '捡起钥匙 `{grid[x][y]}`：用 `|` 把对应位置 1 → `state = {state:b}`',
        'if state == (1 << key_num) - 1': lambda S, B, r: (f"`state = {S.state:b}` 等于全 1 `{(1 << S.key_num) - 1:b}` → ==钥匙集齐=={'' }" if S.state == (1 << S.key_num) - 1 else f"`state = {S.state:b}`，还没集齐 `{(1 << S.key_num) - 1:b}`"),
        'used[x][y][now_state] = True': '标记 `({x},{y})` + 钥匙 `{now_state:b}` 已访问，状态入队，下一轮再扩展',
        'used[x][y][state] = True': '标记 `({x},{y})` + 新钥匙集合 `{state:b}` 已访问（同一格、钥匙变多是新状态）',
        'return step': '集齐所有钥匙，当前 BFS 轮次 `{step}` 就是最短步数',
        'elif (now_state & (1 << (ord(grid[x][y]) - 65)))': lambda S, B, r: (f"邻居是门 `{S.grid[S.x][S.y]}`：检查钥匙集合 `{S.now_state:b}` 里有没有对应的钥匙 `{S.grid[S.x][S.y].lower()}`，且这个状态没访问过"),
        'l, r = r, len(q)': '这一层处理完，下一层是 `q[{l}:{r}]`：`l, r = {l}, {r}`',
        'return -1': '队列耗尽仍没集齐钥匙 → 无解 `-1`',
    },
    cards=dict(
        one_liner='把「位置 + 持有哪些钥匙」当成一个状态来做 BFS',
        complexity='时间 `O(m·n·2^k)`，空间 `O(m·n·2^k)`（k 为钥匙数 ≤ 6）',
        problem=['网格里 `@` 起点，`.` 空地，`#` 墙，小写字母是钥匙，大写字母是对应的门',
                 '每步上下左右走一格；==有钥匙才能过门==，求集齐所有钥匙的最少步数，不行返回 `-1`',
                 '本视频示例：`["@a.","#A#","#b#"]` → `3`'],
        quote='钥匙最多只有6把，因此可以使用状态压缩，即2^k来表示是否获取到第k把钥匙。配合当前坐标，就可以表示现在处于迷宫的哪个位置，手中有哪几把钥匙了。',
        quote_src='—— yiduobo 题解原文',
        idea=['普通 BFS 只记位置不够：同一格带着不同钥匙，后面能走的路不同',
              '状态 = `(x, y, 钥匙二进制)`，`used[x][y][state]` 去重',
              '碰到钥匙用 `|` 加进状态，碰到门用 `&` 检查；某一轮集齐全部钥匙，轮次就是答案'],
        summary=['每个状态只入队一次，状态总数 `m·n·2^k`，时间空间同阶',
                 '易错点：门要用 `ord(c) - 65` 对应钥匙位，钥匙用 `ord(c) - 97`',
                 '易错点：捡钥匙后状态变了，要用新 `state` 去重；`step` 按层累加，不是按出队次数',
                 '原文本身已是 Python 3 可运行的写法，代码未做修改'],
    ),
)
