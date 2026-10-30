G = [[1, 2], [0, 2], [0, 1]]
NN = len(G)
POS = {0: (0.5, 0.1), 1: (0.12, 0.85), 2: (0.88, 0.85)}
WHO = {0: '', 1: '鼠', 2: '猫'}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    win = S.get('winner')
    if win is None:
        return
    deg = S.get('deg')
    cm, cc, ct = S.get('mouse'), S.get('cat'), S.get('turn')
    line = S.get('_line', 0)
    in_loop = 'pre_turn' in S and line >= 44
    pm, pc, pt = S.get('pre_mouse'), S.get('pre_cat'), S.get('pre_turn')
    # ---- 左：图
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
    if cm is not None and cc is not None and 'turn' in S:
        for who, node, c in (('鼠', cm, T['green']), ('猫', cc, T['orange'])):
            px, py = pts[node]
            dx = -16 if who == '鼠' else 16
            cv.rect((px + dx - 17, py - 52, px + dx + 17, py - 24), fill=c, r=8)
            cv.text((px + dx, py - 38), who, 20, T['bg'], anchor='mm', bold=True)
        cv.text((x0 + 18, y0 + 100 + 3 * 76 + 150), f"当前取出：鼠 {cm}，猫 {cc}，轮到{'猫' if ct else '鼠'}", 24, T['yellow'], bold=True)
    # ---- 右：winner 两张表
    cw = 76
    for k in (0, 1):
        gx = x0 + gw + 50 + k * (cw * (NN - 1) + 70)
        gy = y0 + 100
        cv.text((gx - 30, y0 + 4), f"winner[鼠][猫][{k}]", 20, T['text'], bold=True, mono=True)
        cv.text((gx - 30, y0 + 36), f"轮到{'猫' if k else '鼠'}移动", 20, T['muted'])
        for c in range(1, NN):
            cv.text((gx + (c - 1) * cw + cw / 2, gy - 6), f'猫{c}', 18, T['orange'], anchor='mb', bold=True)
        for r in range(NN):
            cv.text((gx - 8, gy + r * cw + cw / 2), f'鼠{r}', 18, T['green'], anchor='rm', bold=True)
            for c in range(1, NN):
                v = win[r][c][k]
                X, Y = gx + (c - 1) * cw, gy + r * cw
                fill = T['green'] if v == 1 else T['orange'] if v == 2 else T['panel2']
                changed = B.get('winner') is not None and B['winner'][r][c][k] != v
                cur = (r, c, k) == (cm, cc, ct) and 'turn' in S and line >= 40
                pre = in_loop and (r, c, k) == (pm, pc, pt)
                oc = T['yellow'] if (cur or changed) else T['pink'] if pre else T['border']
                cv.rect((X + 2, Y + 2, X + cw - 2, Y + cw - 2), fill=fill, r=6, outline=oc, width=4 if (cur or changed or pre) else 1)
                cv.text((X + cw / 2, Y + cw / 2 - 4), WHO[v] if v else '?', 26, T['bg'] if v else T['dim'], anchor='mm', bold=True)
                if deg is not None and not v:
                    cv.text((X + cw - 6, Y + cw - 4), f'd{deg[r][c][k]}', 15, T['muted'], anchor='rb', mono=True)
    ly = y0 + 100 + NN * cw + 24
    for k, t_ in enumerate(['绿 = 鼠赢，橙 = 猫赢，? = 未定 / 平局', 'dN = 还剩 N 种走法没被判输', '黄框 = 刚取出 / 刚标记，粉框 = 上一状态']):
        cv.text((x0 + gw + 20, ly + k * 30), t_, 20, T['muted'])
    cv.text((x0 + gw + 20, ly + 100), '猫列只画 1、2：猫不能进洞 0', 20, T['dim'])


def _who(t):
    return '猫' if t else '鼠'


def _cap_if(S, B, ret):
    pm, pc, pt, win = S.pre_mouse, S.pre_cat, S.pre_turn, S.win
    key = f'(鼠{pm}, 猫{pc}, 轮到{_who(pt)})'
    tail = '（鼠已在洞里还轮到鼠，这种状态不会真正出现，不影响答案）' if pm == 0 and pt == 0 else ''
    pre = f'上一个状态 {key}：'
    if pt == win - 1:
        return (pre + f'上一步是{_who(pt)}动，而这个状态{WHO[win]}赢：{_who(pt)}==直接走过来就赢=='
                f'（情况{"一" if pt == 0 else "二"}）→ 标记 {key} 为{WHO[win]}赢')
    d = S.deg[pm][pc][pt]
    if d == 0:
        return (pre + f'这条路对{_who(pt)}是输的，`deg` 减 1 → ==0==：所有走法都通向{WHO[win]}赢 → 判{WHO[win]}赢'
                f'（情况{"三" if pt == 0 else "四"}）' + tail)
    return pre + f'这条路对{_who(pt)}是输的，只能排除一种走法：`deg` 减 1 → {d}，还有别的走法，先不下结论'


CONFIG = dict(
    num=913, title='猫和老鼠', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='逆向拓扑排序 · 从终局倒推博弈',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2800'],
    code='''
class Solution:
    def catMouseGame(self, g: List[List[int]]) -> int:
        HOLE = 0
        n = len(g)
        deg = [[[0, 0] for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(1, n):
                deg[i][j][0] = len(g[i])
                deg[i][j][1] = len(g[j])
            # 对于猫来说，所有连到洞的边都不能走
            for j in g[HOLE]:
                deg[i][j][1] -= 1

        winner = [[[0, 0] for _ in range(n)] for _ in range(n)]
        q = deque()
        for i in range(1, n):
            winner[HOLE][i][1] = 1  # 鼠到达洞中（此时轮到猫移动），鼠获胜
            winner[i][i][0] = winner[i][i][1] = 2  # 猫和鼠出现在同一个节点，无论轮到谁移动，都是猫获胜
            q.append((HOLE, i, 1))  # 从终点开始倒推
            q.append((i, i, 0))
            q.append((i, i, 1))

        # 获取 (mouse, cat, turn) 的上个状态（值尚未确定）
        def get_pre_states() -> List[Tuple[int, int]]:
            if turn:  # 当前轮到猫移动，枚举上一轮鼠的位置
                return [(pre_mouse, cat) for pre_mouse in g[mouse] if winner[pre_mouse][cat][0] == 0]
            # 当前轮到鼠移动，枚举上一轮猫的位置，注意猫无法移动到洞中
            return [(mouse, pre_cat) for pre_cat in g[cat] if pre_cat != HOLE and winner[mouse][pre_cat][1] == 0]

        # 减少上个状态的度数
        def dec_deg_to_zero() -> bool:
            deg[pre_mouse][pre_cat][pre_turn] -= 1
            return deg[pre_mouse][pre_cat][pre_turn] == 0

        while q:
            mouse, cat, turn = q.popleft()
            win = winner[mouse][cat][turn]  # 最终谁赢了
            pre_turn = turn ^ 1
            for pre_mouse, pre_cat in get_pre_states():
                # 情况一：如果上一回合鼠从 pre 移动到 cur，最终鼠赢，那么标记 pre 状态的 winner = 鼠
                # 情况二：如果上一回合猫从 pre 移动到 cur，最终猫赢，那么标记 pre 状态的 winner = 猫
                # 情况三：如果上一回合鼠从 pre 移动到 cur，最终猫赢，那么待定，直到我们发现从 pre 出发能到达的状态都是猫赢，那么标记 pre 状态的 winner = 猫
                # 情况四：如果上一回合猫从 pre 移动到 cur，最终鼠赢，那么待定，直到我们发现从 pre 出发能到达的状态都是鼠赢，那么标记 pre 状态的 winner = 鼠
                if pre_turn == win - 1 or dec_deg_to_zero():
                    winner[pre_mouse][pre_cat][pre_turn] = win
                    q.append((pre_mouse, pre_cat, pre_turn))  # 继续倒推

        # 鼠在节点 1，猫在节点 2，当前轮到鼠移动
        return winner[1][2][0]  # 返回最终谁赢了（或者平局）
''',
    call=f'Solution().catMouseGame({G})',
    expect=1,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=['mouse', 'cat', 'turn', 'win', 'pre_mouse', 'pre_cat', 'pre_turn'],
    skip=['for j in range(1, n)', 'deg[i][j][0]', 'deg[i][j][1]', 'for j in g[HOLE]', 'for i in range(n)',
          'winner[HOLE][i][1]', 'winner[i][i][0]', 'q.append((HOLE', 'q.append((i, i', 'q.append((pre_mouse',
          'return [(', 'deg[pre_mouse][pre_cat][pre_turn]', 'def get_pre_states', 'def dec_deg', 'if turn:', 'while q', 'pre_turn = turn ^ 1', 'for pre_mouse, pre_cat in get_pre_states()'],
    max_steps=100,
    captions={
        'HOLE = 0': '节点 `0` 是洞；鼠从 `1` 出发先走，猫从 `2` 出发，猫不能进洞',
        'n = len(g)': '图有 `{n}` 个节点',
        'deg = [[[0, 0]': '`deg[i][j][k]`：状态（鼠 i，猫 j，轮到 k）还剩几种走法（出度），后面用来判断「所有走法都输」',
        'winner = [[[0, 0]': '`winner[i][j][k]`：0 = 未定或平局，1 = 鼠赢，2 = 猫赢',
        'q = deque()': '队列放「已经确定结果」的状态，从它们倒推',
        'for i in range(1, n)': lambda S, B, r: ('终点都标好了，队列里有 6 个确定的状态' if S.i == B.get('i') else
                                                  f'终点 `i = {S.i}`：鼠在洞、轮到猫 → ==鼠赢==；猫鼠同在节点 `{S.i}` → ==猫赢==，都入队'),
        'XXX': '终点 `i = {i}`：鼠在洞、轮到猫 → ==鼠赢==；猫鼠同在节点 `{i}` → ==猫赢==，都入队',
        'mouse, cat, turn = q.popleft()': lambda S, B, r: f'队列里取出已确定的状态：鼠在 `{S.mouse}`，猫在 `{S.cat}`，轮到{_who(S.turn)}（还剩 {len(S.q)} 个待处理）',
        'win = winner[mouse][cat][turn]': lambda S, B, r: f'这个状态的结果：=={WHO[S.win]}赢==；倒推它的上一个状态，上一步轮到{_who(S.turn ^ 1)}',
        'if pre_turn == win - 1': _cap_if,
        'winner[pre_mouse][pre_cat][pre_turn] = win': lambda S, B, r: f'标记（鼠{S.pre_mouse}，猫{S.pre_cat}，轮到{_who(S.pre_turn)}）= =={WHO[S.win]}赢==，并入队，继续往前倒推',
        'return winner[1][2][0]': lambda S, B, r: ('队列空了，倒推结束。`winner[1][2][0] = 1`：鼠在 1、猫在 2、轮到鼠 → ==鼠赢==' if r == 1 else f'`winner[1][2][0] = {r}` → {"猫赢" if r == 2 else "平局"}'),
    },
    cards=dict(
        one_liner='从终局倒推：能确定谁赢的状态一圈圈往回扩',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['无向图上，鼠从 1 先走，猫从 2 后走，节点 0 是洞，猫不能进洞',
                 '鼠到洞 → 鼠赢；猫鼠同点 → 猫赢；状态重复 → 平局',
                 '返回 1（鼠赢）/ 2（猫赢）/ 0（平局）。本视频：`g=[[1,2],[0,2],[0,1]]` → `1`'],
        quote='从起点出发，是不好解决的。……正难则反，从终点开始==倒推==，能否得到一个鼠在节点 1，猫在节点 2，当前轮到鼠移动的状态？',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 =（鼠位置，猫位置，轮到谁），终点是确定的：鼠在洞 / 猫鼠同点',
              '倒推四种情况：上一步的人一步走到赢家状态 → 必赢；否则要等「所有走法都通向对方赢」才判输',
              '「所有走法都输」用拓扑排序的度数 `deg` 来数；最后没被标记的是平局'],
        summary=['时间 `O(n^3)`：`n^2` 个状态，每个状态枚举 `O(n)` 个相邻状态；空间 `O(n^2)`',
                 '易错：猫不能进洞，所以 `deg[i][j][1]` 要减去洞的连边，倒推时也要排除 `pre_cat == HOLE`',
                 '易错：`pre_turn == win - 1` 表示「上一步的玩家恰好是赢家」，其余情况只能减度数',
                 '同类题：1728 猫和老鼠 II（同一套思路，换成网格）'],
    ),
)
