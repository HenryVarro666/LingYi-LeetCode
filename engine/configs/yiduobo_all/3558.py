_EDGES = [[1, 2], [1, 3], [3, 4], [3, 5], [4, 6], [6, 7], [6, 8]]
_POS = {1: (1.5, 0), 2: (0.5, 1), 3: (2.5, 1), 4: (1.9, 2), 5: (3.1, 2), 6: (1.9, 3), 7: (1.3, 4), 8: (2.5, 4)}
_LVL = ['purple', 'blue', 'cyan', 'green', 'orange']


_ST = {'first': True}


def _pop_cap(S):
    _ST['first'] = True
    return f'取出队首 `x = {S.x}`（层级 `{S.level[S.x]}`），去看它的邻居 `{S.g[S.x]}`'


def _for_cap(S, B):
    if _ST['first']:
        _ST['first'] = False
        return f'看 `{S.x}` 的第一个邻居 `{S.y}`'
    if S.y == B.y:
        return f'`{S.x}` 的邻居都看完了，回到 `while`'
    return f'看 `{S.x}` 的下一个邻居 `{S.y}`'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    level = S.get('level') or []
    q = list(S.get('q') or [])
    cur = S.get('x') if S.get('_line') in (15, 16, 17, 18, 19) else None
    width, height = x1 - x0 - 120, y1 - y0 - 80
    sx = x0 + 60 + width * 0.1
    sw = width * 0.8 / 3.1
    sy, sh = y0 + 70, (height - 30) / 4.1
    P = lambda v: (sx + _POS[v][0] * sw, sy + _POS[v][1] * sh)
    cv.text((x0 + 18, y0 + 4), '树：圆内 = 编号，旁边 Lk = 层级 level；黄框 = 正在取出的 x，白框 = 在队列里', 22, T['muted'], bold=True)
    for a, b in _EDGES:
        done = len(level) > max(a, b) and level[a] is not None and level[b] is not None
        cv.line([P(a), P(b)], T['text'] if done else T['border'], 3)
    for v in _POS:
        X, Y = P(v)
        lv = level[v] if len(level) > v else None
        fill = T[_LVL[lv % 5]] if lv is not None else T['panel2']
        cv.rect((X - 24, Y - 24, X + 24, Y + 24), fill=fill, r=24, outline=T['border'])
        cv.text((X, Y - 2), v, 26, T['bg'] if lv is not None else T['text'], anchor='mm', bold=True)
        if lv is not None:
            cv.text((X + 30, Y + 20), f'L{lv}', 20, T[_LVL[lv % 5]], anchor='lm', bold=True)
        if v == cur:
            cv.rect((X - 31, Y - 31, X + 31, Y + 31), outline=T['yellow'], width=5, r=31)
        elif v in q:
            cv.rect((X - 31, Y - 31, X + 31, Y + 31), outline=T['text'], width=2, r=31)


CONFIG = dict(
    num=3558, title='给边赋权值的方案数 I', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='BFS 求层级 + 快速幂 2^(cnt-1)',
    tags=['自底向上 DFS', '组合计数', '难度分 1845'],
    code='''
class Solution(object):
    def assignEdgeWeights(self, edges):
        
        n = len(edges) + 1
        g = [[] for _ in range(n + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        level = [None] * (n + 1)
        q = deque()
        q.append(1)
        level[1] = 0
        while q:
            x = q.popleft()
            for y in g[x]:
                if level[y] is None:
                    q.append(y)
                    level[y] = level[x] + 1
        
        mod = 10 ** 9 + 7
        def quick_pow(p):
            if p == 0:
                return 1
            if p == 1:
                return 2
            
            v = quick_pow(p // 2)
            v = v * v % mod
            if p & 1:
                v = v * 2 % mod
            return v

        return quick_pow(max(level[1:]) - 1)
''',
    call=f'Solution().assignEdgeWeights({_EDGES})',
    expect=8,
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='queue', var='q', label='队列 q', h=90),
        dict(type='calls', h=110),
    ],
    watch=['x', 'y', ('mod', 'mod', 'dim'), ('p', 'p', 'blue'), ('v', 'v', 'green')],
    skip=['n = len', 'g = [[]', 'for x, y in edges', 'g[x].append', 'g[y].append', 'def quick_pow', 'mod = 10', 'level = [None]', 'q = deque', 'q.append(y)'],
    captions={
        'q = deque': '用队列做 BFS，从 1 号节点往外一层一层扩展',
        'q.append(1)': '1 号节点入队',
        'level[1] = 0': '根的层级是 `0`：以后 `max(level)` 就是最深节点离根的边数 `cnt`（level[0] 没用）',
        'while q': lambda S, B, r: (f'队列里还有 `{len(S.q)}` 个节点 → 继续' if S.q else '队列空了：所有节点的层级都定了'),
        'x = q.popleft': lambda S, B, r: _pop_cap(S),
        'for y in g[x]': lambda S, B, r: _for_cap(S, B),
        'if level[y] is None': lambda S, B, r: (f'`level[{S.y}]` 还是 None → 第一次到达，是孩子' if S.level[S.y] is None else f'`level[{S.y}]` = {S.level[S.y]} 已经有了（是父节点）→ 跳过'),
        'level[y] = level[x] + 1': '`{y}` 已入队；孩子的层级 = 父亲 + 1：`level[{y}] = {level[x]} + 1` = =={level[y]}==',
        'if p == 0': '`p = {p}`：是 0 吗？{"是 → 直接返回 `2^0 = 1`" if p == 0 else "不是 → 继续往下"}',
        'if p == 1': '`p = {p}`：是 1 吗？{"是 → 直接返回 `2^1 = 2`" if p == 1 else "不是 → 继续往下"}',
        'return 1': '`2^0 = 1`，返回 =={ret}==',
        'return 2': '`2^1 = 2`，返回 =={ret}==',
        'v = quick_pow(p // 2)': '`2^{B.p}` = (`2^{B.p // 2}`)²，`p` 为奇数时再 ×2：先递归求 `quick_pow({B.p // 2})`',
        'v = v * v': '平方：`v = {B.v} × {B.v}` = =={v}==',
        'if p & 1': lambda S, B, r: (f'`p = {S.p}` 是奇数（`p & 1` = 1）→ 还要再乘一个 2' if S.p & 1 else f'`p = {S.p}` 是偶数 → 不用再乘 2'),
        'v = v * 2': '补一个 2：`v = {B.v} × 2` = =={v}==',
        'return v': '`quick_pow({p})` 返回 =={ret}==',
        'return quick_pow': '`cnt = max(level[1:]) = {max(level[1:])}`，奇数个 1 的选法共 `2^(cnt-1)` = `2^{max(level[1:]) - 1}`：交给快速幂',
    },
    max_steps=90,
    cards=dict(
        one_liner='BFS 数出最深层级 cnt，答案就是 2^(cnt-1)，用快速幂算',
        complexity='时间 `O(n + log n)`，空间 `O(n)`',
        problem=['以 1 为根的树，每条边权设为 `1` 或 `2`',
                 '求从根到最深节点路径上，边权和为==奇数==的赋值方案数（模 `10^9+7`）',
                 '本视频：8 个节点，最深路径 1→3→4→6→7 共 `4` 条边 → 答案 `2^3 = 8`'],
        quote='为了使得边权之和为奇数，那么就需要从cnt中选出奇数条边赋值为1，其余的边赋值为2……答案就是2^(cnt - 1)，那么在这里只需使用快速幂计算2^(cnt - 1)就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一步：从 1 号做 `BFS`，`level` 记录每个节点的层级，`max(level)` 就是 `cnt`',
              '第二步：`cnt` 条边里选奇数条设为 1：`C(cnt,1)+C(cnt,3)+…`',
              '用 `C(m,n) = C(m-1,n-1) + C(m-1,n)` 拆开，恰好拼成 `C(cnt-1, 0..cnt-1)` 的和 = `2^(cnt-1)`',
              '第三步：快速幂，`p` 为奇数时多乘一个 2'],
        summary=['时间 `O(n)`（BFS）+ `O(log n)`（快速幂），空间 `O(n)`',
                 '用 BFS 而不是递归 DFS，不怕 `n = 10^5` 时递归太深',
                 '`quick_pow(p)` 的参数是 `cnt − 1`，不是 `cnt`',
                 '对比灵神：他用 DFS 求最大深度、内置 `pow` 取模幂；这里是 BFS + 手写快速幂',
                 '原文为 Python 2 写法，`max(level)` 里有 `level[0] = None`，Python 3 无法比较，已改为 `max(level[1:])`'],
    ),
)
