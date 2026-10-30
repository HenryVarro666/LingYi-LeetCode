GRID = ['MCF']
CAT_J, MOUSE_J = 1, 2
WHO = {0: '', 1: '鼠', 2: '猫'}
NC = len(GRID[0])


def _who(t):
    return '猫' if t else '鼠'


def _strip(cv, S, T, x0, y0, w, mouse=None, cat=None):
    cw = min(110, (w - 20) / NC)
    for c in range(NC):
        ch = GRID[0][c]
        X = x0 + c * cw
        food = ch == 'F'
        cv.rect((X + 3, y0 + 40, X + cw - 3, y0 + 40 + 70), fill=T['yellow'] if food else T['panel2'], outline=T['border'], r=10)
        cv.text((X + cw / 2, y0 + 40 + 35), {'F': '食物 F', 'M': '鼠 M', 'C': '猫 C'}.get(ch, ch), 24, T['bg'] if food else T['text'], anchor='mm', bold=True)
        cv.text((X + cw / 2, y0 + 40 + 84), str(c), 16, T['dim'], anchor='mt', mono=True)
        if mouse == c:
            cv.rect((X + 10 - 2, y0 + 8, X + 10 + 38, y0 + 38), fill=T['green'], r=8)
            cv.text((X + 29, y0 + 23), '鼠', 22, T['bg'], anchor='mm', bold=True)
        if cat == c:
            cv.rect((X + cw - 48, y0 + 8, X + cw - 8, y0 + 38), fill=T['orange'], r=8)
            cv.text((X + cw - 28, y0 + 23), '猫', 22, T['bg'], anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), f'地图 "{GRID[0]}"：M 鼠（跳 {MOUSE_J}）  C 猫（跳 {CAT_J}）  F 食物 = 洞', 22, T['muted'], bold=True)
    win = S.get('winner')
    cm, cc, ct = S.get('mouse'), S.get('cat'), S.get('turn')
    line = S.get('_line', 0)
    live = win is not None and cm is not None and 'turn' in S and 34 <= line <= 55
    _strip(cv, S, T, x0 + 18, y0 + 34, x1 - x0 - 36, cm if live else None, cc if live else None)
    # 邻接表
    gm, gc = S.get('g_mouse'), S.get('g_cat')
    y = y0 + 190
    if gm is not None and win is None:
        cv.text((x0 + 18, y), '建好的图（从格子 v 一步能到哪些格子，包含原地不动）', 22, T['muted'], bold=True)
        for k, (nm, g, c) in enumerate((('鼠 g_mouse', gm, T['green']), ('猫 g_cat', gc, T['orange']))):
            for v in range(NC):
                txt = f'{nm}[{v}] = {g[v]}'
                cv.text((x0 + 28, y + 38 + k * (NC * 30 + 8) + v * 30), txt, 21, c, mono=True)
        y += 38 + 2 * (NC * 30 + 8) + 12
    if win is None:
        return
    cw = 70
    pre_m, pre_c, pre_t = S.get('pre_mouse'), S.get('pre_cat'), S.get('pre_turn')
    for k in (0, 1):
        gx = x0 + 70 + k * (cw * NC + 90)
        cv.text((gx - 52, y), f'winner[鼠][猫][{k}]  {"鼠" if k == 0 else "猫"}先动', 20, T['text'], bold=True, mono=True)
        gy = y + 66
        for c in range(NC):
            cv.text((gx + c * cw + cw / 2, gy - 6), f'猫{c}', 18, T['orange'], anchor='mb', bold=True)
        for r in range(NC):
            cv.text((gx - 8, gy + r * cw + cw / 2), f'鼠{r}', 18, T['green'], anchor='rm', bold=True)
            for c in range(NC):
                v = win[r][c][k]
                X, Y = gx + c * cw, gy + r * cw
                fill = T['green'] if v == 1 else T['orange'] if v == 2 else T['panel2']
                bw = B.get('winner')
                changed = bw is not None and bw[r][c][k] != v
                cur = live and (r, c, k) == (cm, cc, ct)
                pre = live and 'pre_turn' in S and line >= 44 and (r, c, k) == (pre_m, pre_c, pre_t)
                oc = T['yellow'] if (cur or changed) else T['pink'] if pre else T['border']
                cv.rect((X + 2, Y + 2, X + cw - 2, Y + cw - 2), fill=fill, r=6, outline=oc, width=4 if (cur or changed or pre) else 1)
                cv.text((X + cw / 2, Y + cw / 2 - 4), WHO[v] if v else '?', 26, T['bg'] if v else T['dim'], anchor='mm', bold=True)
                dg = S.get('deg')
                if dg is not None and not v:
                    cv.text((X + cw - 6, Y + cw - 4), f'd{dg[r][c][k]}', 15, T['muted'], anchor='rb', mono=True)
    ly = y + 66 + NC * cw + 14
    cv.text((x0 + 18, ly), '绿 = 鼠赢，橙 = 猫赢，? = 未定 / 平局，dN = 还剩 N 种走法没被判输', 19, T['muted'])
    cv.text((x0 + 18, ly + 28), '黄框 = 刚取出 / 刚标记，粉框 = 上一状态', 19, T['muted'])


def _cap_if(S, B, ret):
    pm, pc, pt, win = S.pre_mouse, S.pre_cat, S.pre_turn, S.win
    pre = f'上一个状态 (鼠{pm}, 猫{pc}, 轮到{_who(pt)})：'
    if pt == win - 1:
        return pre + f'上一步是{_who(pt)}动，而这个状态{WHO[win]}赢：{_who(pt)}==直接走过来就赢== → 标记为{WHO[win]}赢'
    d = S.deg[pm][pc][pt]
    if d == 0:
        return pre + f'这条路对{_who(pt)}是输的，`deg` 减 1 → ==0==：所有走法都通向{WHO[win]}赢 → 判{WHO[win]}赢'
    return pre + f'这条路对{_who(pt)}是输的，只能排除一种走法：`deg` 减 1 → {d}，先不下结论'


CONFIG = dict(
    num=1728, title='猫和老鼠 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='复用 913：网格建图 + 逆向拓扑排序',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2849'],
    code='''
class Solution:
    # 913. 猫和老鼠
    def catMouseGame(self, g_mouse: List[List[int]], g_cat: List[List[int]], mouse_start: int, cat_start: int, hole: int) -> int:
        n = len(g_mouse)
        deg = [[[0, 0] for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                deg[i][j][0] = len(g_mouse[i])
                deg[i][j][1] = len(g_cat[j])

        winner = [[[0, 0] for _ in range(n)] for _ in range(n)]
        q = deque()
        for i in range(n):
            winner[hole][i][1] = 1  # 鼠到达洞中（此时轮到猫移动），鼠获胜
            winner[i][hole][0] = 2  # 猫到达洞中（此时轮到鼠移动），猫获胜
            winner[i][i][0] = winner[i][i][1] = 2  # 猫和鼠出现在同一个节点，无论轮到谁移动，都是猫获胜
            q.append((hole, i, 1))  # 从终点开始倒推
            q.append((i, hole, 0))
            q.append((i, i, 0))
            q.append((i, i, 1))

        # 获取 (mouse, cat, turn) 的上个状态（值尚未确定）
        def get_pre_states() -> List[Tuple[int, int]]:
            if turn:  # 当前轮到猫移动，枚举上一轮鼠的位置
                return [(pre_mouse, cat) for pre_mouse in g_mouse[mouse] if winner[pre_mouse][cat][0] == 0]
            # 当前轮到鼠移动，枚举上一轮猫的位置
            return [(mouse, pre_cat) for pre_cat in g_cat[cat] if winner[mouse][pre_cat][1] == 0]

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
                    q.append((pre_mouse, pre_cat, pre_turn))

        # 鼠在节点 mouse_start，猫在节点 cat_start，当前轮到鼠移动
        return winner[mouse_start][cat_start][0]  # 返回最终谁赢了（或者平局）

    def canMouseWin(self, grid: List[str], catJump: int, mouseJump: int) -> bool:
        DIRS = (0, -1), (0, 1), (-1, 0), (1, 0)  # 左右上下
        m, n = len(grid), len(grid[0])
        # 鼠和猫分别建图
        g_mouse = [[] for _ in range(m * n)]
        g_cat = [[] for _ in range(m * n)]
        for i, row in enumerate(grid):
            for j, c in enumerate(row):
                if c == '#':  # 墙
                    continue
                if c == 'M':  # 鼠的位置
                    mx, my = i, j
                elif c == 'C':  # 猫的位置
                    cx, cy = i, j
                elif c == 'F':  # 食物（洞）的位置
                    fx, fy = i, j
                v = i * n + j  # 二维坐标 (i,j) 映射为一维坐标 v
                for dx, dy in DIRS:  # 枚举左右上下四个方向
                    for k in range(mouseJump + 1):  # 枚举跳跃长度
                        x, y = i + k * dx, j + k * dy
                        if not (0 <= x < m and 0 <= y < n and grid[x][y] != '#'):  # 出界或者遇到墙
                            break
                        g_mouse[v].append(x * n + y)  # 连边
                    for k in range(catJump + 1):  # 枚举跳跃长度
                        x, y = i + k * dx, j + k * dy
                        if not (0 <= x < m and 0 <= y < n and grid[x][y] != '#'):  # 出界或者遇到墙
                            break
                        g_cat[v].append(x * n + y)  # 连边

        # 判断是否鼠赢
        return self.catMouseGame(g_mouse, g_cat, mx * n + my, cx * n + cy, fx * n + fy) == 1
''',
    call=f'Solution().canMouseWin({GRID}, {CAT_J}, {MOUSE_J})',
    expect=True,
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=['mouse', 'cat', 'turn', 'win', 'pre_mouse', 'pre_cat', 'pre_turn'],
    skip=["DIRS =", "m, n =", "g_cat = [[]", "for i, row", "for j, c in", "if c == '#'", "continue", "if c == 'M'", "elif c ==", "mx, my", "cx, cy", "fx, fy",
          "for dx, dy", "for k in", "x, y =", "if not (", "break", ".append(x * n + y)",
          'deg[i][j][0]', 'deg[i][j][1]', 'for i in range(n)', 'for j in range(n)', 'winner[hole][i][1]', 'winner[i][hole][0]', 'winner[i][i][0]',
          'q.append((hole', 'q.append((i, hole', 'q.append((i, i', 'q.append((pre_mouse', 'return [(', 'deg[pre_mouse]', 'def get_pre', 'def dec_deg',
          'if turn:', 'while q', 'pre_turn = turn ^ 1', 'for pre_mouse, pre_cat in get_pre_states()', 'win = winner[mouse][cat][turn]'],
    max_steps=42,
    captions={
        'g_mouse = [[]': '鼠、猫各建一张图：`g[v]` 是从格子 `v`（编号 = 行×列数+列）一步能跳到的格子；遇墙或出界就停',
        'v = i * n + j': lambda S, B, r: f'格子 `{S.v}`（`{S.c}`）：枚举左右上下四个方向、跳 `0..jump` 格，都连边（跳 0 格 = 原地不动，每个方向都会加一次）',
        'return self.catMouseGame': lambda S, B, r: ('图建好了。鼠能跳 2 格：`g_mouse[0]` 里有 `1` 和 `2`，==可以跳过猫直接到食物 2==；猫只能跳 1 格。原地不动每个方向都连了一次，所以后面会重复遇到同一个状态，不影响结果。开始倒推' if 'winner' not in S else '返回 `winner == 1` 的判断结果'),
        'n = len(g_mouse)': '节点就是格子，共 `{n}` 个；食物当作洞：`hole = {hole}`，鼠起点 `{mouse_start}`，猫起点 `{cat_start}`',
        'deg = [[[0, 0]': '`deg[i][j][k]`：状态（鼠 i，猫 j，轮到 k）的走法数 = 当前玩家所在格的出边数（本题猫也能进洞，不用扣）',
        'winner = [[[0, 0]': '`winner`：0 = 未定或平局，1 = 鼠赢，2 = 猫赢',
        'q = deque()': '先标终局并入队：鼠在洞（轮到猫）→ ==鼠赢==；猫在洞（轮到鼠）→ ==猫赢==；猫鼠同格 → ==猫赢==',
        'mouse, cat, turn = q.popleft()': lambda S, B, r: f'取出已确定的状态：鼠 `{S.mouse}`，猫 `{S.cat}`，轮到{_who(S.turn)}，结果 =={WHO[S.winner[S.mouse][S.cat][S.turn]]}赢==（队里还剩 {len(S.q)} 个）；去找它的上一个状态',
        'win = winner[mouse][cat][turn]': lambda S, B, r: f'这个状态的结果：=={WHO[S.win]}赢==；倒推它的上一个状态，上一步轮到{_who(S.turn ^ 1)}',
        'if pre_turn == win - 1': _cap_if,
        'winner[pre_mouse][pre_cat][pre_turn] = win': lambda S, B, r: f'标记（鼠{S.pre_mouse}，猫{S.pre_cat}，轮到{_who(S.pre_turn)}）= =={WHO[S.win]}赢==，并入队',
        'return winner[mouse_start]': lambda S, B, r: ('队列空了。鼠起点 `{0}`、猫起点 `{1}`、轮到鼠：`winner = 1` → ==鼠赢=='.format(S.mouse_start, S.cat_start) if r == 1 else f'`winner = {r}`'),
    },
    cards=dict(
        one_liner='和 913 同一套倒推，只是先把网格拆成「鼠图」和「猫图」',
        complexity='时间 `O(m^2·n^2·(m+n))`，空间 `O(m^2·n^2)`',
        problem=['网格里有鼠 M、猫 C、食物 F、墙 #；鼠先走，两人轮流跳，最远 `mouseJump` / `catJump` 格，可以原地不动',
                 '猫抓到鼠或先吃到食物 → 猫赢；鼠先吃到食物 → 鼠赢；1000 步内吃不到 → 猫赢',
                 '本视频：地图 `MCF`，`catJump=1, mouseJump=2` → `true`（鼠可以跳过猫）'],
        quote='本题思路一样，为了复用 913 题的代码，需要做一些预处理和修改：把二维坐标映射为一维坐标……鼠和猫分别建图 gMouse 和 gCat……913 题猫不能进洞，但本题可以（把食物当作洞）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['格子 `(i,j)` 映射成编号 `i·n+j`，鼠、猫各建一张图：能跳到的格子（含原地）都连边',
              '食物当作洞：鼠到洞 → 鼠赢；猫到洞 → 猫赢；同格 → 猫赢',
              '之后和 913 完全一样：从终局倒推，`deg` 数到 0 才判输'],
        summary=['时间 `O(m^2n^2(m+n))`，空间 `O(m^2n^2)`',
                 '「1000 步」可以当平局：`2mn << 1000`，超过说明局面在兜圈',
                 '易错：建图时枚举 `k` 要从 0 开始（原地不动），遇墙立刻 `break`；鼠可以跳过猫，所以不判断猫的位置',
                 '本题猫也能进洞，所以 `winner[i][hole][0] = 2` 要额外初始化'],
    ),
)
