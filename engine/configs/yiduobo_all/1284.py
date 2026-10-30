def _mat(cv, x, y, cs, val, m, n, title, color, T, diff=None):
    cv.text((x + n * cs / 2, y - 8), title, 22, color, anchor='mb', bold=True)
    for i in range(m):
        for j in range(n):
            p = i * n + j
            on = (val >> p) & 1
            X, Y = x + j * cs, y + i * cs
            if diff is not None:
                fill = T['yellow'] if (diff >> p) & 1 else T['panel2']
                tc = T['bg'] if (diff >> p) & 1 else T['dim']
            else:
                fill = color if on else T['panel2']
                tc = T['bg'] if on else T['dim']
            cv.rect((X + 3, Y + 3, X + cs - 3, Y + cs - 3), fill=fill, r=8, outline=T['border'])
            cv.text((X + cs / 2, Y + cs / 2), on if diff is None else ('翻' if (diff >> p) & 1 else ''), 30, tc, anchor='mm', bold=True, mono=True)
    cv.text((x + n * cs / 2, y + m * cs + 8), format(val, '0%db' % (m * n)), 22, T['text'], anchor='mt', mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'm' not in S or 'n' not in S:
        cv.text((x0 + 18, y0 + 4), '用二进制数表示矩阵：第 p = i×n+j 位 = mat[i][j]', 24, T['muted'], bold=True)
        return
    m, n = S['m'], S['n']
    cs = 70
    cv.text((x0 + 18, y0 + 4), '矩阵状态（蓝 = 1，灰 = 0；黄 = 这次翻转会动到的格子）', 22, T['muted'], bold=True)
    ys = y0 + 80
    w = n * cs
    gap = (x1 - x0 - 3 * w) / 4
    xs = [x0 + gap + k * (w + gap) for k in range(3)]
    if 'now' in S:
        _mat(cv, xs[0], ys, cs, S['now'], m, n, 'now（当前状态）', T['blue'], T)
    if 'next' in S and 'near' in S and S.get('_line') is not None and 'for near in near_list' in B.get('_src', 'for near in near_list') or True:
        if 'next' in S and 'near' in S and 'now' in S and 'used' in S:
            _mat(cv, xs[1], ys, cs, S['near'], m, n, 'near（翻转掩码）', T['yellow'], T, diff=S['near'])
            _mat(cv, xs[2], ys, cs, S['next'], m, n, 'next = now ^ near', T['green'], T)
            cv.text((xs[1] - gap / 2, ys + m * cs / 2), '^', 40, T['muted'], anchor='mm', bold=True)
            cv.text((xs[2] - gap / 2, ys + m * cs / 2), '=', 40, T['muted'], anchor='mm', bold=True)
    if 'used' in S and 'res' in S:
        seen = sum(1 for v in S['used'] if v)
        cv.text((x0 + 18, ys + m * cs + 52), f"BFS 第 {S['res']} 层 · used 已见 {seen}/{len(S['used'])} 个状态 · 目标：状态 0（全零）", 22, T['text'], bold=True)


CONFIG = dict(
    num=1284, title='转化为全零矩阵的最少翻转次数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='状态压缩 + BFS',
    tags=['灵神题单', '图论算法'],
    code='''
class Solution(object):
    def minFlips(self, mat):

        near_list = []
        m = len(mat)
        n = len(mat[0])
        now = 0
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                p = i * n + j
                if mat[i][j]:
                    now |= (1 << p)
                near = (1 << p)
                for index in range(4):
                    x = i + dx[index]
                    y = j + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        near_p = x * n + y
                        near |= (1 << near_p)
                near_list.append(near)
        
        if now == 0:
            return 0

        q = [now]
        l = 0
        r = 1
        used = [False] * (1 << (m * n))
        used[now] = True
        res = 0
        while l < r:
            res += 1
            for now in q[l : r]:
                for near in near_list:
                    next = now ^ near
                    if not used[next]:
                        used[next] = True
                        q.append(next)
        
            if used[0]:
                return res

            l, r = r, len(q)

        return -1
''',
    call='Solution().minFlips([[1,1],[0,0]])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var=lambda S: [format(v, '0%db' % (S['m'] * S['n'])) for v in S['q']] if 'q' in S and 'm' in S else [], label='BFS 队列 q（二进制状态）', cell=90, h=150),
        dict(type='array', var=lambda S: S['near_list'] if 'near_list' in S else [], label='near_list：翻转每个格子的异或掩码', cell=70, h=150),
    ],
    watch=['now', 'res', 'l', 'r'],
    skip=['dx = ', 'dy = ', 'near_p = ', 'x = i + dx', 'y = j + dy', 'for index in range', 'if x >= 0', 'if mat[i][j]', 'for i in range', 'for j in range', 'near = (1 << p)', 'near_list.append', 'l, r = r, len(q)', 'used[next] = True', 'for now in q', 'res += 1'],
    max_steps=80,
    captions={
        'p = i * n + j': '格子 `({i},{j})` 对应二进制第 `p = {p}` 位',
        'now |= (1 << p)': '`mat[{i}][{j}] = 1` → 把第 {p} 位置 1，`now` = `{now}`',
        'near = (1 << p)': '先放自己这一位：翻格子本身',
        'near |= (1 << near_p)': '再加上邻居这一位：翻格子时邻居一起翻 → `near` = `{near}`',
        'near_list.append': '格子 `({i},{j})` 的翻转掩码 = `{near}`，存入 `near_list`',
        'if now == 0': '`now = {now}`：已经是全零就不用翻 → 否则开始 BFS',
        'q = [now]': '起点：初始状态入队',
        'used = [False]': '状态只有 `2^(m*n)` = {1 << (m*n)} 种，开 `used` 记录哪些状态见过',
        'used[now] = True': '起点标记为已访问',
        'res += 1': '开始第 `{res}` 层：每个状态各翻一次格子（一步操作）',
        'for now in q[l : r]': '取出这一层的状态 `now` = `{now}`',
        'next = now ^ near': '翻转 = 异或：`{B.now} ^ {near}` = `{next}`',
        'if not used[next]': lambda S, B, r: (f'状态 `{S.next}` 没见过 → 新状态，入队' if not S.used[S.next] else f'状态 `{S.next}` 见过了 → 更多步数到达它没有意义，丢弃'),
        'used[next] = True': '标记 `{next}` 已访问，保证每个状态只入队一次',
        'q.append(next)': '`{next}` 入队，下一层再展开',
        'if used[0]': lambda S, B, r: ('`used[0]` 为真：全零状态已经到达 → 当前层数就是最少翻转次数' if S.used[0] else '`used[0]` 还是假：全零还没出现，继续下一层'),
        'l, r = r, len(q)': '下一层的范围：`q[{l}:{r}]` 就是刚入队的那批状态',
        'return res': '全零在第 `{res}` 层出现 → 最少翻转 =={res}== 次',
    },
    cards=dict(
        one_liner='矩阵只有 2^(m·n) 种状态：翻转 = 异或，BFS 找全零',
        complexity='时间 `O(2^(mn) · mn)`，空间 `O(2^(mn))`',
        problem=['`mat` 是 0/1 矩阵，一步可以翻转一个格子及其上下左右的邻居',
                 '求把矩阵变成全零的==最少步数==，不可能返回 `-1`',
                 '示例：`[[0,0],[0,1]]` → `3`；本视频：`[[1,1],[0,0]]` → `2`'],
        quote='矩阵最多只有9个格子，同时取值只能是0或者1，那么最多也就只有2^(m * n)种不同的状态。',
        quote_src='—— yiduobo 题解原文',
        idea=['把矩阵压成一个整数，第 `i*n+j` 位 = `mat[i][j]`',
              '预处理每个格子的翻转掩码 `near`，翻转 = `now ^ near`',
              '每步代价都是 1 → 从初始状态 BFS，==第一次碰到 0 的层数==就是答案'],
        summary=['时间 `O(2^(mn) · mn)`，空间 `O(2^(mn))`',
                 '初始就是全零要先 `return 0`，否则 BFS 层数会多算 1',
                 '`used` 保证每个状态只入队一次；翻同一格两次等于没翻，所以不会漏最优解',
                 '原文已是 Python 3 可运行写法，代码逐字照搬',
                 '同类题：01 矩阵 / 滑动谜题等「状态压缩 + BFS」'],
    ),
)
