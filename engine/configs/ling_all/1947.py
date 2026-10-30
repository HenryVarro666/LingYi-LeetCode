_INF = 10 ** 9


def _fmt(v):
    return '∞' if v >= _INF else ('-∞' if v <= -_INF else str(v))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    wt = S.get('wt')
    if not wt:
        return
    m = len(wt) - 1
    la, lb, sl = S.get('la'), S.get('lb'), S.get('slack')
    match, vb = S.get('match'), S.get('vb')
    cur_i, cur_y = S.get('i'), S.get('y')
    x = S.get('x') if 'nextY' in S else None
    cv.text((x0 + 18, y0 + 4), '兼容性矩阵 wt（行 = 学生 x，列 = 导师 y）；la / lb = 顶标，slack = 列上的最小松弛', 21, T['muted'], bold=True)
    cell = min(120, (x1 - x0 - 330) / m)
    sx, sy = x0 + 230, y0 + 100
    for j in range(1, m + 1):
        cv.text((sx + (j - 0.5) * cell, sy - 14), f'导师{j}', 22, T['blue'] if vb and vb[j] else T['muted'], anchor='mb', bold=True)
    for i in range(1, m + 1):
        Y = sy + (i - 1) * cell
        hot = (x == i)
        cv.text((sx - 130, Y + cell / 2), f'学生{i}', 22, T['pink'] if hot else (T['yellow'] if cur_i == i else T['muted']), anchor='rm', bold=True)
        if la:
            cv.text((sx - 12, Y + cell / 2), f'la={_fmt(la[i])}', 20, T['cyan'], anchor='rm', bold=True)
        for j in range(1, m + 1):
            X = sx + (j - 1) * cell
            w = wt[i][j]
            matched = match is not None and match[j] == i
            tight = la is not None and lb is not None and la[i] + lb[j] == w
            fill = T['green'] if matched else T['panel2']
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=fill, r=10,
                    outline=T['yellow'] if tight and la else T['border'], width=4 if tight and la else 1)
            cv.text((X + cell / 2, Y + cell / 2), w, 34, T['bg'] if matched else T['text'], anchor='mm', bold=True)
    yb = sy + m * cell + 12
    if lb:
        cv.text((sx - 12, yb + 14), '列顶标 lb', 20, T['cyan'], anchor='rm', bold=True)
        for j in range(1, m + 1):
            cv.text((sx + (j - 0.5) * cell, yb + 14), _fmt(lb[j]), 24, T['cyan'], anchor='mm', bold=True)
    if sl and vb:
        cv.text((sx - 12, yb + 50), 'slack', 20, T['orange'], anchor='rm', bold=True)
        for j in range(1, m + 1):
            cv.text((sx + (j - 0.5) * cell, yb + 50), _fmt(sl[j]) if not vb[j] else '·', 24, T['orange'], anchor='mm', bold=True)
    if match:
        cv.text((sx - 12, yb + 90), '匹配 match', 20, T['green'], anchor='rm', bold=True)
        for j in range(1, m + 1):
            cv.text((sx + (j - 0.5) * cell, yb + 90), f'学生{match[j]}' if match[j] else '—', 22, T['green'] if match[j] else T['dim'], anchor='mm', bold=True)


CONFIG = dict(
    num=1947, title='最大兼容性评分和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='KM 算法（最大权二分图匹配）（Go 原文转写）',
    tags=['灵神题单·动态规划', '灵神题单·图论算法', '难度分 1704'],
    code='''
inf = int(1e9)


def KuhnMunkres(wt: List[List[int]]) -> int:
    sum = 0
    match = [0] * len(wt)  # 右部点匹配了哪一个左部点
    la = [0] * len(wt)
    for i, row in enumerate(wt):
        la[i] = -inf
        for v in row:
            if v > la[i]:
                la[i] = v
    lb = [0] * len(wt)
    slack = [0] * len(wt)
    for i in range(1, len(wt)):
        vb = [False] * len(wt)
        for j in range(1, len(wt)):
            slack[j] = inf
        last = [0] * len(wt)  # 右部点在交错树中的上一个右部点，用于倒推得到交错路
        y = 0
        match[0] = i  # 一开始假设有一条 i-0 的匹配
        while True:
            vb[y] = True
            x, nextY = match[y], 0
            delta = inf
            for j in range(1, len(wt)):
                if not vb[j]:
                    d = la[x] + lb[j] - wt[x][j]
                    if d < slack[j]:
                        slack[j] = d
                        last[j] = y
                    if slack[j] < delta:
                        delta = slack[j]
                        nextY = j
            # 当 delta=0 时，相当于沿着相等子图向下搜索一层
            # 当 delta>0 时，相当于直接回到最小边（新加入相等子图的边）处开始搜索
            if delta > 0:
                for j in range(len(wt)):
                    if vb[j]:
                        la[match[j]] -= delta
                        lb[j] += delta
                    else:
                        slack[j] -= delta
            y = nextY
            if match[y] == 0:
                break
        # 倒推更新增广路
        while y > 0:
            match[y] = match[last[y]]
            y = last[y]
    for w in range(1, len(wt)):
        sum += wt[match[w]][w]
    return sum


class Solution:
    def maxCompatibilitySum(self, students: List[List[int]], mentors: List[List[int]]) -> int:
        m = len(students)
        wt = [None] * (m + 1)
        wt[0] = [0] * (m + 1)
        for i in range(len(wt[0])):
            wt[0][i] = -inf
        for i, st in enumerate(students):
            wt[i + 1] = [0] * (m + 1)
            wt[i + 1][0] = -inf
            for j, mt in enumerate(mentors):
                for k, v in enumerate(st):
                    if v == mt[k]:
                        wt[i + 1][j + 1] += 1
        return KuhnMunkres(wt)
''',
    call='Solution().maxCompatibilitySum([[0,1,1],[1,1,0]], [[1,0,0],[1,1,0]])',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: (f"`x = {S['x']}`（学生），`nextY = {S['nextY']}`，`delta = {_fmt(S['delta'])}`" if 'delta' in S and 'nextY' in S and S.get('x') is not None else ''), h=60, size=26),
    ],
    skip=['sum = 0', 'match = [0]', 'la = [0]', 'for i, row', 'slack = [0]', 'm = len', 'wt = [None]', 'wt[0] = ', 'for i in range(len(wt[0]))', 'wt[0][i]',
          'for i, st', 'wt[i + 1]', 'for j, mt', 'for k, v', 'if v == mt', 'vb = [False]', 'last = [0]', 'for v in row', 'la[i] = -inf', 'if v > la[i]', 'la[i] = v',
          'slack[j] = d', 'last[j] = y', 'delta = slack[j]', 'nextY = j', 'break', 'while True', 17, 18, 'for j in range(len(wt))', 'if vb[j]:', 'delta = inf', 'if not vb[j]', 'vb[y] = True', 'for w in range(1', 'y = 0', 'while y > 0'],
    max_steps=85,
    watch=['i', 'y', 'x', 'delta', ('sum', 'sum', 'green')],
    captions={
        'return KuhnMunkres(wt)': '先算好兼容性矩阵 `wt`（第 0 行 / 第 0 列是占位，值 `-inf`），再交给 KM 算法求最大权匹配',
        'lb = [0]': '顶标初始化：`la[x]` = 这一行的最大权 `{la[1:]}`，`lb` 全 0，保证 `la[x] + lb[y] >= wt[x][y]`',
        'for i in range(1, len(wt))': lambda S, B, r: f'逐个加入左部点（学生）`{S.i}`，为它找增广路' if B.get('i') != S.i else '所有学生都匹配完了',
        'slack[j] = inf': '`slack[j]`：交错树到右部点 `j` 的最小松弛，先设为 `inf`',
        'y = 0': '`y` 是当前右部点，从虚拟点 `0` 出发',
        'match[0] = i': '从右部点 `y = 0`（虚拟点）出发：先假设学生 `{i}` 匹配了它，这样就能从学生 `{i}` 开始搜',
        'x, nextY': '右部点 `{y}` 进入交错树（`vb[{y}] = True`）；`x = match[{y}] = {x}` 是和它匹配的学生，从 `x` 向外找边，`delta` 记最小松弛',
        'd = la[x]': '未访问的右部点 `{j}`：`d = la[{x}] + lb[{j}] − wt[{x}][{j}]` = =={d}==（0 = 相等边）',
        'if d < slack[j]': lambda S, B, r: (f'`{S.d} < slack[{S.j}]` → 更新 `slack[{S.j}] = {S.d}`，并记录来路 `last[{S.j}] = {S.y}`' if S.d < S.slack[S.j] else f'`{S.d}` 不比 `slack[{S.j}] = {_fmt(S.slack[S.j])}` 小，不用更新'),
        'if slack[j] < delta': lambda S, B, r: (f'`slack[{S.j}] = {_fmt(S.slack[S.j])}` < `delta = {_fmt(S.delta)}` → 它是目前最小松弛，`delta = {_fmt(S.slack[S.j])}`，候选 `nextY = {S.j}`' if S.slack[S.j] < S.delta else f'`slack[{S.j}] = {_fmt(S.slack[S.j])}` 不比 `delta` 小'),
        'if delta > 0': lambda S, B, r: (f'`delta = {S.delta}` > 0：相等子图里走不动 → 调整顶标让一条新边进入相等子图' if S.delta > 0 else '`delta = 0`：沿相等子图直接走到下一层'),
        'la[match[j]] -= delta': '树内的学生顶标 `la` 减 `delta`',
        'lb[j] += delta': '树内的右部点顶标 `lb` 加 `delta`（保持树内的边仍然相等）',
        'slack[j] -= delta': '树外的右部点 `slack` 同步减 `delta`',
        'y = nextY': '走到右部点 `y = {y}`',
        'if match[y] == 0': lambda S, B, r: (f'`match[{S.y}] = 0`：右部点 `{S.y}` 还没人匹配 → 找到增广路，跳出循环' if S.match[S.y] == 0 else f'`{S.y}` 已匹配学生 `{S.match[S.y]}` → 继续沿交错树往下搜'),
        'match[y] = match[last[y]]': '沿 `last` 倒推：`match[{y}] = match[last[{y}]]` = 学生 `{match[y]}`，把路上的匹配逐个换过去',
        'y = last[y]': '回到来路的上一个右部点 `y = {y}`',
        'sum += wt[match[w]][w]': '导师 `{w}` 配学生 `{match[w]}`，加上 `wt = {wt[match[w]][w]}` → `sum = {sum}`',
        'return sum': '最大兼容性评分和 `{sum}`',
    },
    cards=dict(
        one_liner='学生和导师是二分图，兼容性是边权：KM 算法求最大权完美匹配',
        complexity='KM `O(m³)`，建矩阵 `O(m² n)`，空间 `O(m²)`',
        problem=['`m` 名学生、`m` 名导师，各自回答 `n` 个 0/1 问题',
                 '配对的评分 = 两人答案相同的题数，求一一配对后的最大评分和',
                 '本视频：2 名学生、2 名导师，每人 3 道题（原示例 3 人 → `8`）'],
        quote='先算出 `wt[i+1][j+1]` 兼容性评分，再调用 `KuhnMunkres(wt)` 求最大权匹配。',
        quote_src='—— 灵茶山艾府题解代码（原文只有 Go 代码）',
        idea=['`wt[x][y]` 是学生 x 与导师 y 的评分，`la`、`lb` 是顶标，始终满足 `la[x] + lb[y] >= wt[x][y]`',
              '只走「相等」的边（`la + lb == wt`）找增广路；走不动就用最小松弛 `delta` 调整顶标',
              '找到增广路后沿 `last` 倒推翻转匹配，最后累加匹配边的权值'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`for ; y > 0; y = last[y]` 写成 `while y > 0`）',
                 '第 0 行 / 第 0 列是占位（`-inf`），`match[0]` 借给虚拟点，下标从 1 开始',
                 '时间 `O(m³ + m² n)`，空间 `O(m²)`；`m, n <= 8` 时状压 DP 也能做',
                 '树内的左部点 `la -= delta`、右部点 `lb += delta`，树外只减 `slack`'],
    ),
)
