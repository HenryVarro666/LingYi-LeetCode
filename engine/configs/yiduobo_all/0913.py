G = [[1, 2], [0, 2], [0, 1]]
NN = len(G)
POS = {0: (0.5, 0.1), 1: (0.12, 0.85), 2: (0.88, 0.85)}
WHO = {0: '', 1: '鼠', 2: '猫'}
LOOP0 = 42   # 'for last in graph' 所在行之后才画粉框（见下方 --steps 里的行号）


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    mouse, cat = S.get('mouse'), S.get('cat')
    if mouse is None or cat is None:
        return
    om, oc_ = S.get('oud_mouse'), S.get('oud_cat')
    line = S.get('_line', 0)
    live = 'now' in S and 36 <= line <= 62
    ci, cj, cn = S.get('i'), S.get('j'), S.get('now')
    last = S.get('last')
    gw = 250
    cv.text((x0 + 18, y0 + 4), '图（蓝 = 洞）', 22, T['muted'], bold=True)
    pts = {k: (x0 + 40 + v[0] * (gw - 80), y0 + 90 + v[1] * (gw - 110)) for k, v in POS.items()}
    for a in range(NN):
        for b in G[a]:
            if a < b:
                cv.line([pts[a], pts[b]], T['border'], 4)
    for k, (px, py) in pts.items():
        cv.rect((px - 24, py - 24, px + 24, py + 24), fill=T['panel2'], outline=T['blue'] if k == 0 else T['border'], width=4 if k == 0 else 1, r=24)
        cv.text((px, py), k, 26, T['text'], anchor='mm', bold=True)
    if live:
        for who, node, c in (('鼠', ci, T['green']), ('猫', cj, T['orange'])):
            px, py = pts[node]
            dx = -16 if who == '鼠' else 16
            cv.rect((px + dx - 17, py - 52, px + dx + 17, py - 24), fill=c, r=8)
            cv.text((px + dx, py - 38), who, 20, T['bg'], anchor='mm', bold=True)
        cv.text((x0 + 18, y0 + 100 + 3 * 76 + 150), f"当前取出：鼠 {ci}，猫 {cj}，{'鼠先动' if cn == 1 else '猫先动'}", 24, T['yellow'], bold=True)
    cw = 76
    tabs = [('mouse[鼠][猫]', mouse, om, '鼠先行动的结果'), ('cat[鼠][猫]', cat, oc_, '猫先行动的结果')]
    for k, (title, tab, oud, sub) in enumerate(tabs):
        gx = x0 + gw + 50 + k * (cw * (NN - 1) + 70)
        gy = y0 + 100
        cv.text((gx - 30, y0 + 4), title, 20, T['text'], bold=True, mono=True)
        cv.text((gx - 30, y0 + 36), sub, 20, T['muted'])
        for c in range(1, NN):
            cv.text((gx + (c - 1) * cw + cw / 2, gy - 6), f'猫{c}', 18, T['orange'], anchor='mb', bold=True)
        for r in range(NN):
            cv.text((gx - 8, gy + r * cw + cw / 2), f'鼠{r}', 18, T['green'], anchor='rm', bold=True)
            for c in range(1, NN):
                v = tab[r][c]
                X, Y = gx + (c - 1) * cw, gy + r * cw
                fill = T['green'] if v == 1 else T['orange'] if v == 2 else T['panel2']
                bt = B.get('mouse' if k == 0 else 'cat')
                changed = bt is not None and bt[r][c] != v
                cur = live and (r, c) == (ci, cj) and ((k == 0 and cn == 1) or (k == 1 and cn == 2))
                pre = False
                if live and last is not None and line >= LOOP0:
                    if cn == 1 and k == 1 and (r, c) == (ci, last):
                        pre = True
                    if cn == 2 and k == 0 and (r, c) == (last, cj):
                        pre = True
                oc = T['yellow'] if (cur or changed) else T['pink'] if pre else T['border']
                cv.rect((X + 2, Y + 2, X + cw - 2, Y + cw - 2), fill=fill, r=6, outline=oc, width=4 if (cur or changed or pre) else 1)
                cv.text((X + cw / 2, Y + cw / 2 - 4), WHO[v] if v else '?', 26, T['bg'] if v else T['dim'], anchor='mm', bold=True)
                if oud is not None and not v and oud[r][c]:
                    cv.text((X + cw - 6, Y + cw - 4), f'd{oud[r][c]}', 15, T['muted'], anchor='rb', mono=True)
    ly = y0 + 100 + NN * cw + 24
    for k, t_ in enumerate(['绿 = 鼠赢，橙 = 猫赢，? = 未定 / 平局', 'dN = oud 计数：还剩 N 种走法没被判输', '黄框 = 刚取出 / 刚标记，粉框 = 上一状态']):
        cv.text((x0 + gw + 20, ly + k * 30), t_, 20, T['muted'])
    cv.text((x0 + gw + 20, ly + 100), '猫列只画 1、2：猫不能进洞 0', 20, T['dim'])


CONFIG = dict(
    num=913, title='猫和老鼠', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='已知终局倒推 · 类拓扑排序 BFS',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2800'],
    code='''
class Solution(object):
    def catMouseGame(self, graph):

        zero_connect = set()
        for x in graph[0]:
            zero_connect.add(x)

        n = len(graph)
        mouse = [[0] * n for _ in range(n)]
        cat = [[0] * n for _ in range(n)]
        oud_mouse = [[0] * n for _ in range(n)]
        oud_cat = [[0] * n for _ in range(n)]

        q = []
        for i in range(n):
            for j in range(1, n):
                if i == 0:
                    mouse[i][j] = 1
                    cat[i][j] = 1
                    q.append([i, j, 1])
                    q.append([i, j, 2])
                elif i == j:
                    mouse[i][j] = 2
                    cat[i][j] = 2
                    q.append([i, j, 1])
                    q.append([i, j, 2])
                else:
                    oud_mouse[i][j] = len(graph[i])
                    oud_cat[i][j] = len(graph[j])
                    if j in zero_connect:
                        oud_cat[i][j] -= 1

        l = 0
        r = len(q)
        while l < r:
            i, j, now = q[l]
            l += 1
            if now == 1:
                for last in graph[j]:
                    if last == 0:
                        continue
                    if cat[i][last] == 0:
                        if mouse[i][j] == 2:
                            cat[i][last] = 2
                            q.append([i, last, 2])
                            r += 1
                        elif mouse[i][j] == 1:
                            oud_cat[i][last] -= 1
                            if oud_cat[i][last] == 0:
                                cat[i][last] = 1
                                q.append([i, last, 2])
                                r += 1
            else:
                for last in graph[i]:
                    if mouse[last][j] == 0:
                        if cat[i][j] == 1:
                            mouse[last][j] = 1
                            q.append([last, j, 1])
                            r += 1
                        elif cat[i][j] == 2:
                            oud_mouse[last][j] -= 1
                            if oud_mouse[last][j] == 0:
                                mouse[last][j] = 2
                                q.append([last, j, 1])
                                r += 1

        return mouse[1][2]
''',
    call=f'Solution().catMouseGame({G})',
    expect=1,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['i', 'j', 'now', 'last', 'l', 'r'],
    skip=['zero_connect.add', 'for x in graph[0]', 'for i in range(n)', 'for j in range(1, n)', 'if i == 0', 'elif i == j', 'mouse[i][j] = ', 'cat[i][j] = ',
          'q.append([i, j', 'oud_mouse[i][j] = ', 'oud_cat[i][j] = ', 'if j in zero_connect', 'oud_cat[i][j] -= 1', 'else:',
          'while l < r', 'l += 1', 'if now == 1', 'for last in graph', 'if last == 0', 'continue', 'r += 1', 'q.append([i, last', 'q.append([last, j',
          'r = len(q)', 'mouse = [[0]', 'cat = [[0]', 'oud_mouse = [[0]'],
    max_steps=100,
    captions={
        'zero_connect = set()': '`zero_connect`：和洞（节点 0）相连的节点，猫不能走进洞，要从猫的走法里扣掉',
        'oud_cat = [[0]': '`mouse[i][j]`：鼠在 i、猫在 j、==鼠先动==的结果；`cat[i][j]`：==猫先动==的结果；0 = 未定',
        'n = len(graph)': '建四张 n×n 的表：`mouse` / `cat` 存结果，`oud_mouse` / `oud_cat` 存「还剩几种没被判输的走法」，数到 0 就说明走哪都输',
        'q = []': '队列里放已经确定结果的状态，格式 `[鼠, 猫, 1=鼠表 / 2=猫表]`',
        'l = 0': '先把终局放进队列：鼠在洞（0, j）→ ==鼠赢==；鼠猫同点（i, i）→ ==猫赢==；其余状态记下走法数 `oud`',
        'i, j, now = q[l]': lambda S, B, r: (f'取出确定的状态：鼠 `{S.i}`，猫 `{S.j}`，{"==鼠先动==" if S.now == 1 else "==猫先动=="}，'
                                             f'结果 =={WHO[S.mouse[S.i][S.j] if S.now == 1 else S.cat[S.i][S.j]]}赢==（队尾 `r = {S.r}`）'),
        'if cat[i][last] == 0': lambda S, B, r: (f'它的上一步：猫从 `{S.last}` 走到 `{S.j}`，对应状态 `cat[{S.i}][{S.last}]`（猫先动）' +
                                                  ('，还没确定 → 往下判断' if S.cat[S.i][S.last] == 0 else '，已经确定 → 跳过')),
        'if mouse[i][j] == 2': lambda S, B, r: ('现在的状态是==猫赢==：上一步猫走过来就能赢' if S.mouse[S.i][S.j] == 2 else '现在的状态不是猫赢，继续看是不是鼠赢'),
        'cat[i][last] = 2': '`cat[{i}][{last}] = 2`：猫先动、走到 `{j}` 就赢 → ==猫赢==（入队）',
        'elif mouse[i][j] == 1': '现在的状态是==鼠赢==：猫走到这里是一条死路，只能把走法数减 1',
        'oud_cat[i][last] -= 1': '猫在 `{last}` 的一条路被排除：`oud_cat[{i}][{last}]` = {oud_cat[i][last]}',
        'if oud_cat[i][last] == 0': lambda S, B, r: ('走法数减到 ==0==：猫往哪走都输 → 判鼠赢' if S.oud_cat[S.i][S.last] == 0 else f'还剩 `{S.oud_cat[S.i][S.last]}` 种走法，先不下结论'),
        'cat[i][last] = 1': '`cat[{i}][{last}] = 1`：猫所有走法都让鼠赢 → ==鼠赢==（入队）',
        'if mouse[last][j] == 0': lambda S, B, r: (f'它的上一步：鼠从 `{S.last}` 走到 `{S.i}`，对应状态 `mouse[{S.last}][{S.j}]`（鼠先动）' +
                                                    ('，还没确定 → 往下判断' if S.mouse[S.last][S.j] == 0 else '，已经确定 → 跳过')),
        'if cat[i][j] == 1': lambda S, B, r: ('现在的状态是==鼠赢==：上一步鼠走过来就能赢' if S.cat[S.i][S.j] == 1 else '现在的状态不是鼠赢，继续看是不是猫赢'),
        'mouse[last][j] = 1': '`mouse[{last}][{j}] = 1`：鼠先动、走到 `{i}` 就赢 → ==鼠赢==（入队）',
        'elif cat[i][j] == 2': '现在的状态是==猫赢==：鼠走到这里是死路，只能把走法数减 1',
        'oud_mouse[last][j] -= 1': '鼠在 `{last}` 的一条路被排除：`oud_mouse[{last}][{j}]` = {oud_mouse[last][j]}',
        'if oud_mouse[last][j] == 0': lambda S, B, r: ('走法数减到 ==0==：鼠往哪走都输 → 判猫赢' if S.oud_mouse[S.last][S.j] == 0 else f'还剩 `{S.oud_mouse[S.last][S.j]}` 种走法，先不下结论'),
        'mouse[last][j] = 2': '`mouse[{last}][{j}] = 2`：鼠所有走法都让猫赢 → ==猫赢==（入队）',
        'return mouse[1][2]': lambda S, B, r: f'队列处理完。`mouse[1][2] = {r}`：鼠在 1、猫在 2、鼠先动 → ' + ('==鼠赢==' if r == 1 else '猫赢' if r == 2 else '平局'),
    },
    cards=dict(
        one_liner='先写下确定的终局，再倒着推出其他状态',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['无向图上，鼠从 1 先走，猫从 2 后走，节点 0 是洞，猫不能进洞',
                 '鼠到洞 → 鼠赢；猫鼠同点 → 猫赢；重复局面 → 平局。返回 1 / 2 / 0',
                 '本视频：`graph=[[1,2],[0,2],[0,1]]`，答案 `1`'],
        quote='由于题目中可能出现平局状态，……因此使用普通的bfs会出现死循环的情况。不过既然我们知道了一些确定的值，那么我们可以换一种思路，从这些确定的值开始==倒推==，这就联想到了某种类似拓扑排序的做法。',
        quote_src='—— yiduobo 题解原文',
        idea=['两张表：`mouse[i][j]` 鼠先动，`cat[i][j]` 猫先动。`mouse[0][x]`、`cat[0][x]` 鼠赢，`mouse[x][x]`、`cat[x][x]` 猫赢',
              '取出确定的状态，枚举它的「上一步」：上一步的人一步走过来就赢 → 直接判赢',
              '否则只是排除一条路：`oud` 减 1，减到 0 才说明所有走法都输'],
        summary=['时间 `O(n^3)`，空间 `O(n^2)`；没被标记的状态就是平局',
                 '易错：猫不能进洞，`oud_cat` 初值要减去和洞相连的路，倒推时 `last == 0` 要跳过',
                 '`now == 1` 对应「鼠先动」的表，`now == 2` 对应「猫先动」的表，别搞反',
                 '对比灵神：灵神把鼠猫两张表合成一个三维 `winner`，yiduobo 分成 `mouse` / `cat` 两个二维表，思路相同'],
    ),
)
