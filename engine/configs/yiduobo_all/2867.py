N = 7
EDGES = [[1, 2], [2, 4], [4, 3], [4, 6], [3, 5], [6, 7]]
PRIMES = {2, 3, 5, 7}
POS = {1: (0.06, 0.5), 2: (0.27, 0.5), 4: (0.5, 0.5), 6: (0.73, 0.15), 7: (0.94, 0.15), 3: (0.73, 0.8), 5: (0.94, 0.8)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '树（粉 = 质数；非质数按所在连通块着色，旁边是块大小）', 22, T['muted'], bold=True)
    w, h = x1 - x0 - 120, y1 - y0 - 130
    P = {k: (x0 + 60 + v[0] * w, y0 + 75 + v[1] * h) for k, v in POS.items()}
    belong = S.get('belong') or {}
    plen = S.get('part_len') or {}
    cols = [T['cyan'], T['orange'], T['purple'], T['green']]
    phase2 = 'res' in S
    q = S.get('q') or []
    cur = S.get('x') if (phase2 and 'cnt' in S) or (not phase2 and 'head' in S and S.get('x') in P) else None
    for a, b in EDGES:
        cv.line([P[a], P[b]], T['border'], 4)
    for k, (px, py) in P.items():
        r = 30
        isp = k in PRIMES
        fill = T['pink'] if isp else T['panel2']
        tc = T['bg'] if isp else T['text']
        if k in belong:
            c = cols[belong[k] % 4]
            cv.d.ellipse((px - r - 6, py - r - 6, px + r + 6, py + r + 6), outline=c, width=4)
            cv.text((px, py + r + 12), '块%d · 大小 %d' % (belong[k], plen.get(belong[k], 0)), 20, c, anchor='mt', bold=True)
        cv.d.ellipse((px - r, py - r, px + r, py + r), fill=fill, outline=T['border'])
        if k == cur:
            cv.d.ellipse((px - r - 12, py - r - 12, px + r + 12, py + r + 12), outline=T['yellow'], width=5)
        cv.text((px, py), k, 30, tc, anchor='mm', bold=True)


def _t(S):
    if 'res' in S and 'cnt' in S:
        return f"质数 ==%d==：cnt = %d（先算上自己这一端），res = ==%d==" % (S['x'], S['cnt'], S['res'])
    if 'tot_part' in S and 'q' in S:
        return f"已找到 `{S['tot_part']}` 个合数连通块；队列 q = `{S['q']}`"
    return ''


CONFIG = dict(
    num=2867, title='统计树中的合法路径数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='筛质数 · BFS 合数连通块 · 枚举质数', tags=['数学算法', '链表树与回溯', '难度分 2428'],
    code='''
class Solution(object):
    def countPaths(self, n, edges):

        g = {x : set() for x in range(1, n + 1)}
        for x, y in  edges:
            g[x].add(y)
            g[y].add(x)

        prime = [True] * (n + 1)
        prime[1] = False
        p = 2
        while p * p <= n:
            if prime[p]:
                for x in range(p + p, n + 1, p):
                    prime[x] = False
            p += 1
        
        belong = {}
        part_len = {}
        tot_part = 0
        for x in range(1, n + 1):
            if not prime[x] and x not in belong:
                q = [x]
                belong[x] = tot_part
                part_len[tot_part] = 1
                head, tail = 0, 1
                while head < tail:
                    for x in q[head : tail]:
                        for y in g[x]:
                            if not prime[y] and y not in belong:
                                q.append(y)
                                belong[y] = tot_part
                                part_len[tot_part] += 1
                    
                    head, tail = tail, len(q)
                
                tot_part += 1
        
        res = 0
        for x in range(1, n + 1):
            if prime[x]:
                cnt = 1
                for y in g[x]:
                    if y in belong:
                        res += part_len[belong[y]] * cnt
                        cnt += part_len[belong[y]]
        
        return res
''',
    call='Solution().countPaths(%d, %r)' % (N, EDGES),
    expect=9,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='text', fn=_t, h=110),
    ],
    watch=[('x', 'x', 'pink'), ('cnt', 'cnt', 'cyan'), ('res', 'res', 'green')],
    skip=['g = {x', 5, 'g[x].add', 'g[y].add', 'prime = [True]', 'prime[1] = False', 'p = 2', 'p += 1', 'for x in range(p + p', 'belong = {}', 'part_len = {}',
          'tot_part = 0', 'q = [x]', 'part_len[tot_part] = 1', 'head, tail = 0, 1', 'head, tail = tail', 28, 29, 'res = 0'],
    max_steps=80,
    captions={
        'while p * p <= n': lambda S, B, r: (f'筛法：`p = {S.p}`，`p*p = {S.p * S.p}` ≤ `n = {S.n}` → 继续' if S.p * S.p <= S.n else f'`p*p = {S.p * S.p}` > `n` → 筛完，剩下的 True 就是质数'),
        'if prime[p]': lambda S, B, r: (f'`{S.p}` 是质数 → 划掉它的倍数' if S.prime[S.p] else f'`{S.p}` 已被划掉'),
        'prime[x] = False': '`{x}` 是 `{p}` 的倍数 → 不是质数',
        21: lambda S, B, r: ('合数连通块都找好了：`tot_part = %d`' % S.tot_part if getattr(B, 'x', None) == S.x and S.x == S.n else f'扫描 `x = {S.x}`'),
        22: lambda S, B, r: (f'`{S.x}` 是' + ('质数，不属于任何连通块 → 跳过' if S.prime[S.x] else ('合数，已在某个块里 → 跳过' if S.x in S.belong else '合数，还没分块 → ==新开一个连通块=='))),
        'belong[x] = tot_part': '`belong[{x}] = {tot_part}`：给这个合数标上块号',
        'while head < tail': lambda S, B, r: ('BFS 一圈一圈往外扩：`head < tail`，还有点没扩' if S.head < S.tail else 'BFS 这一块扩完了'),
        30: lambda S, B, r: (f'邻居 `{S.y}`：' + ('合数且没分过块 → ==并入当前块==' if (not S.prime[S.y] and S.y not in S.belong) else ('是质数，是块的边界' if S.prime[S.y] else '已经在块里了'))),
        'belong[y] = tot_part': '`belong[{y}] = {tot_part}`：`{y}` 和当前块是同一块',
        'q.append(y)': '`{y}` 入队',
        'part_len[tot_part] += 1': '块 `{tot_part}` 的大小 +1 = =={part_len[tot_part]}==',
        'tot_part += 1': '这一块扩完，大小 `{part_len[tot_part - 1]}`；下一块编号 `{tot_part}`',
        40: lambda S, B, r: ('每个点都枚举过了' if getattr(B, 'x', None) == S.x and S.x == S.n else f'枚举 `x = {S.x}`'),
        41: lambda S, B, r: (f'`{S.x}` 是质数：它当中间点' if S.prime[S.x] else f'`{S.x}` 不是质数，跳过'),
        'cnt = 1': '`cnt` 记已算过的块大小之和，初值 `1` 是“以质数自己为端点”的那条路径',
        43: lambda S, B, r: (f'质数 `{S.x}` 的邻居都看完了，`res = {S.res}`' if getattr(B, 'y', None) == S.y and S.y == list(S.g[S.x])[-1] else f'看邻居 `y = {S.y}`'),
        'if y in belong': lambda S, B, r: (f'`{S.y}` 是合数，属于块 `{S.belong[S.y]}`（大小 `{S.part_len[S.belong[S.y]]}`）' if S.y in S.belong else f'`{S.y}` 是质数，不在任何块里，跳过'),
        'res += part_len[belong[y]] * cnt': '这块 `{part_len[belong[y]]}` 个合数 × 之前的 `{B.cnt}` → `res` = =={res}==',
        'cnt += part_len[belong[y]]': '把这块的大小并入 `cnt` = =={cnt}==，给后面的块配对',
        'return res': '合法路径共 `{res}` 条',
    },
    cards=dict(
        one_liner='换成质数的视角：从质数出发，只经合数连通块，两块两两配对',
        complexity='时间 `O(n log log n)`，空间 `O(n)`',
        problem=['树的节点编号 `1..n`，路径 `(a, b)` 中恰好有一个质数编号才算合法',
                 '`(a, b)` 和 `(b, a)` 算同一条路径',
                 '本视频：`n = 7`，`edges = [[1,2],[2,4],[4,3],[4,6],[3,5],[6,7]]` → `9`'],
        quote='合数连通块指的是树中由若干个合数节点组成的连通分量，其中不能包含质数节点，那么合数连通块就可以通过类似 floodfill 的方式进行求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['先筛出 `1..n` 的质数，再用 BFS 把合数分成连通块，记下块号 `belong` 和大小 `part_len`',
              '合法路径 = 质数 + 两侧只经合数：从质数出发到一个块里的点，或两个不同块里的点配对',
              '枚举每个质数，`cnt` 从 `1` 开始（算上质数自己做端点），`res += 块大小 * cnt`，再 `cnt += 块大小`',
              '这样“后来的块”只和“先来的块”配对，不用最后再除以 2'],
        summary=['时间约 `O(n log log n)`（筛法）加 `O(n)`（BFS 和枚举），空间 `O(n)`',
                 '易错：`cnt` 初值是 `1`，漏了就少算“质数自己为端点”的路径',
                 '易错：质数邻居不在 `belong` 里，要用 `if y in belong` 过滤',
                 '原文是 Python 3 可直接运行的写法，没有改动',
                 '对比灵神：灵神在类外预处理质数、DFS 求块并缓存 `size`；yiduobo 在函数里筛，BFS 分块'],
    ),
)
