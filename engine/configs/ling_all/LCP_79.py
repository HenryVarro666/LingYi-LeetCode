def _vis_cells(S):
    return {(i, j) for i, j, k in S.get('vis', ())}


def _color(S, i, j, v):
    if 'vis' not in S or 'k' not in S:
        return None
    if (i, j) == (S['i'], S['j']):
        return 'yellow'
    if any((a, b) == (i, j) and kk == S['k'] for a, b, kk in S['vis']):
        return 'blue'
    return None


CONFIG = dict(
    num='LCP 79', title='提取咒文', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='BFS · 状态 (i,j,k)', tags=[],
    code='''
class Solution:
    def extractMantra(self, matrix: List[str], mantra: str) -> int:
        m, n = len(matrix), len(matrix[0])
        q = [(0, 0, 0)]
        vis = {q[0]}
        step = 1
        while q:
            tmp = q
            q = []
            for i, j, k in tmp:
                if matrix[i][j] == mantra[k]:  # 可以提取
                    if k == len(mantra) - 1:  # 下一步就是终点，直接返回
                        return step
                    p = (i, j, k + 1)
                    if p not in vis:
                        vis.add(p)
                        q.append(p)
                # 枚举周围四个格子
                for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
                    if 0 <= x < m and 0 <= y < n:
                        p = (x, y, k)
                        if p not in vis:
                            vis.add(p)
                            q.append(p)
            step += 1
        return -1
''',
    call='Solution().extractMantra(["sd","ep"], "speed")',
    expect=10,
    views=[
        dict(type='text', fn=lambda S: (f"BFS 第 =={S['step']}== 层（已用 {S['step'] - 1} 次操作），队列里 {len(S['tmp'] if 'tmp' in S else S['q'])} 个状态" if 'step' in S else '')),
        dict(type='grid', var='matrix', h=250, cursors=[('i', 'j', 'yellow', '')], color=_color, label='matrix（黄 当前格，蓝 已访问格）'),
        dict(type='string', var='mantra', h=170, pointers={'k': 'pink'}, label='mantra（k = 当前要提取的字母）'),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), ('k', 'k', 'pink'), ('step', 'step', 'green'), ('len(vis)', 'len(vis)', 'orange')],
    captions={
        'm, n = len': '矩阵 `{m}` 行 `{n}` 列',
        'q = [(0, 0, 0)]': '起点状态 `(0,0,0)`：在左上角，==要去提取== `mantra[0]`',
        'vis = {q[0]}': '`vis` 记录访问过的状态 `(i,j,k)`：同一格、同一进度不重复走',
        'step = 1': '`step` 从 1 开始：把「提取」的那一步也算上',
        'while q': lambda S, B, r: f'队列里还有 {len(S.q)} 个状态 → 继续扩展一层',
        'q = []': '新开一个空队列 `q` 装下一层状态',
        'tmp = q': '这一层的状态交给 `tmp`，新一层写进新的 `q`',
        'for i, j, k in tmp': '取出状态：位置 `({i},{j})`，要提取 `mantra[{k}]` = `{mantra[k]}`',
        'if matrix[i][j] == mantra[k]': '`matrix[{i}][{j}] = {matrix[i][j]!r}`，`mantra[{k}] = {mantra[k]!r}` → {"==相同，可以提取==" if matrix[i][j] == mantra[k] else "不同，只能移动"}',
        'if k == len(mantra) - 1': '`k = {k}`，是最后一个字母吗？{f"==是==：提取它就完成，这次提取是第 `{step}` 次操作" if k == len(mantra) - 1 else "不是，继续"}',
        'return step': 'BFS 按层推进，最先到达终点的层数就是最少操作数 → =={step}==',
        'p = (i, j, k + 1)': '提取后进入状态 `{p}`：位置不变，进度 +1',
        'p = (x, y, k)': '移动到 `({x},{y})`，进度不变：状态 `{p}`',
        'if p not in vis': lambda S, B, r: f'状态 `{S.p}` {"已访问过 → 跳过" if S.p in S.vis else "==没访问过=="}',
        'vis.add(p)': '标记已访问：`vis` 现有 {len(vis)} 个状态',
        'q.append(p)': '加入下一层队列，`q` 长度 = {len(q)}',
        'for x, y in': '枚举 `({i},{j})` 的上下左右四个邻居',
        'if 0 <= x < m': lambda S, B, r: f'邻居 `({S.x},{S.y})` {"在矩阵内" if 0 <= S.x < S.m and 0 <= S.y < S.n else "越界 → 跳过"}',
        'step += 1': '这一层全部处理完，操作次数 +1：`step` → =={step}==',
        'return -1': '队列空了仍没提取完 → `-1`',
    },
    cards=dict(
        one_liner='把「位置 + 提取进度」当成一个状态，BFS 找最短操作数',
        complexity='时间 `O(mnl)`，空间 `O(mnl)`',
        problem=['矩阵里每格一个小写字母，提取装置从左上角出发，上下左右移动算一次操作，提取算一次操作',
                 '要按顺序取出 `mantra` 的每个字母，求最少操作次数，取不出返回 `-1`',
                 '示例：`["sd","ep"]`，`"speed"` → `10`'],
        quote='状态为 (i,j,k)，表示当前位置在 (i,j)，要去提取 mantra[k]。初始状态：(0,0,0)。终点为 k=l。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个状态走一步（移动或提取）代价都是 1 → ==无权最短路，用 BFS==',
              '移动：`(i,j,k) → (x,y,k)`；提取：格子字母等于 `mantra[k]` 时 `→ (i,j,k+1)`',
              '提取最后一个字母那一步直接返回 `step`，不用再入队'],
        summary=['时间 `O(mnl)`：状态数 `m·n·l`，每个状态枚举 5 种转移',
                 '空间 `O(mnl)`，`vis` 要记三元组，只记位置会错',
                 '`step` 从 1 开始，因为返回时「提取最后一个字母」这一步还没加上',
                 '矩阵里缺某个字母时，BFS 走完所有状态队列才空，返回 `-1`'],
    ),
)
