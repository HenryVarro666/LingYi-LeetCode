G = [[1, 0, 0], [0, 0, 0], [0, 0, 1]]


def _color(S, i, j, v):
    q = S.get('q')
    if q is None or 'l' not in S or 'r' not in S:
        return 'green' if G[i][j] == 1 else None
    if G[i][j] == 1:
        return 'green'
    if [i, j] in q[S['r']:]:
        return 'cyan'
    if [i, j] in q[S['l']:S['r']]:
        return 'yellow'
    if v == 1:
        return 'blue'
    return None


def _txt(S):
    if 'res' not in S or 'l' not in S:
        return ''
    if S['l'] >= S['r']:
        return f"BFS 结束：一共扩散了 `res = {S['res']}` 轮，最后一轮什么也没扩到，所以答案是 ==`{S['res'] - 1}`=="
    return f"第 ==`{S['res']}`== 轮扩散：当前层有 `{S['r'] - S['l']}` 个格子（黄），新加入下一层的（青）"


CONFIG = dict(
    num=1162, title='地图分析', difficulty='Medium', category='网格图',
    author='yiduobo', technique='多源 BFS · 按层染色',
    tags=['灵神题单·网格图'],
    code='''
class Solution(object):
    def maxDistance(self, grid):
        
        q = []
        n = len(grid)
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    q.append([i, j])
        
        l = 0
        r = len(q)
        if r == 0 or r == n * n:
            return -1
        res = 0
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            res += 1
            for nowx, nowy in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < n and y >= 0 and y < n and grid[x][y] == 0:
                        q.append([x, y])
                        grid[x][y] = 1
            
            l, r = r, len(q)

        return res - 1
''',
    call='Solution().maxDistance([[1, 0, 0], [0, 0, 0], [0, 0, 1]])',
    expect=2,
    skip=['dx = [', 'dy = [', 'n = len', 'for index in range(4)', 'x = nowx', 'y = nowy', 'for i in range(n)',
          'for j in range(n)', 'q = []'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', cell=100, h=400, color=_color,
             label='grid（绿 = 原来的陆地 1，黄 = 本轮正在扩散的格子，青 = 本轮新染的，蓝 = 更早染的）',
             cursors=[('nowx', 'nowy', 'blue'), ('x if _line in (21, 22) else None', 'y', 'pink')]),
        dict(type='text', fn=_txt, h=70, size=30),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        'if grid[i][j] == 1': lambda S, B, rt: (f'`grid[{B.i}][{B.j}] = 1`：陆地 ==作为 BFS 起点==，入队'
                                                if B.grid[B.i][B.j] == 1 else f'`grid[{B.i}][{B.j}] = 0`：海洋，跳过'),
        'l = 0': '`l = 0`：当前这一层在 `q[l:r]`',
        'r = len(q)': '`r = len(q)` = {r}：第 0 层 = 所有陆地',
        'if r == 0 or': lambda S, B, rt: ('没有陆地 或 全是陆地：没有符合要求的海洋 → 返回 -1' if (S.r == 0 or S.r == S.n * S.n)
                                          else f'陆地 `{S.r}` 个，海洋 `{S.n * S.n - S.r}` 个：都有，继续'),
        'res = 0': '`res` 记录扩散了多少轮',
        'while l < r': lambda S, B, rt: (f'`l = {B.l} < r = {B.r}`：这一层还有 `{B.r - B.l}` 个格子 → 扩散一轮'
                                         if B.l < B.r else f'`l == r`：这一轮什么也没扩到，BFS 结束'),
        'res += 1': '开始第 `{res}` 轮：所有当前层格子同时向四周扩一格，==轮数就是到陆地的距离==',
        'for nowx, nowy in q[l : r]': lambda S, B, rt: (1 / 0 if 'nowx' in B and (B.nowx, B.nowy) == (S.nowx, S.nowy)
                                                        else f'取当前层的格子 `({S.nowx},{S.nowy})`'),
        'if x >= 0 and x < n': lambda S, B, rt: (f'邻居 `({B.x},{B.y})` 越界' if not (0 <= B.x < B.n and 0 <= B.y < B.n)
                                                 else (f'邻居 `({B.x},{B.y})` 是海洋 0 → ==染成 1，加入下一层=='
                                                       if B.grid[B.x][B.y] == 0 else
                                                       f'邻居 `({B.x},{B.y})` 已经是 1（陆地或更早染的）→ 不重复入队')),
        'q.append': '`({x},{y})` 入队：它离最近陆地的距离 = ==第 {res} 轮==',
        'grid[x][y] = 1': '就地改成 1 当访问标记',
        'l, r = r, len(q)': '这一层处理完：`l, r = {l}, {r}`，下一层 = `q[{l}:{r}]`',
        'return res - 1': '最后一轮没有扩出新格子，所以多算了一轮：答案 `res - 1` = =={res - 1}==',
    },
    cards=dict(
        one_liner='把所有陆地当起点同时 BFS，扩散的轮数就是最远距离',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`n × n` 的 `grid`，`0` 是海洋，`1` 是陆地',
                 '找一个海洋格子，使它到==最近陆地==的曼哈顿距离==最大==，返回这个距离',
                 '没有海洋或没有陆地，返回 `-1`',
                 '本视频：3×3，左上、右下各一块陆地 → `2`'],
        quote='我们可以从所有的1开始进行bfs染色，每一轮将相邻的格子中的0变成1，同时将其加入bfs队列中，那么最终bfs的轮次就是要求的最远距离。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐个海洋找最近陆地太慢，反过来：==陆地一起向外扩散==',
              '每轮把相邻的 0 染成 1 并入队，第 k 轮染到的格子距离正好是 k',
              '最后一轮染到的格子最远；`l、r` 圈出队列里的“当前层”'],
        summary=['时间 `O(n²)`，每个格子最多入队一次',
                 '先判断 `-1`：没有陆地或全是陆地',
                 '易错：循环结束时多数了一轮空扩散，所以返回 `res - 1`',
                 '原文已是 Python 3 可运行的写法，代码未改'],
    ),
)
