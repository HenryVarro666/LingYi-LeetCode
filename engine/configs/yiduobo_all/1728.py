GRID = ['MCF']
CAT_J, MOUSE_J = 1, 2
NC = len(GRID[0])
FOOD = GRID[0].index('F')


def _who_move(r):
    return '鼠' if r == 1 else '猫'


def _res(node):
    """node.win_state 是对「当前行动方」而言；转成谁赢"""
    ws = node.win_state
    if ws is None:
        return None
    mover = '鼠' if node.m_round == 1 else '猫'
    other = '猫' if mover == '鼠' else '鼠'
    return mover if ws else other


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nd = S.get('node_dict')
    cv.text((x0 + 18, y0 + 2), f'地图 "{GRID[0]}"：M 鼠（跳 {MOUSE_J}）  C 猫（跳 {CAT_J}）  F 食物', 22, T['muted'], bold=True)
    cw0 = min(110, (x1 - x0 - 40) / NC)
    for c in range(NC):
        ch = GRID[0][c]
        X = x0 + 18 + c * cw0
        food = ch == 'F'
        cv.rect((X + 3, y0 + 40, X + cw0 - 3, y0 + 100), fill=T['yellow'] if food else T['panel2'], outline=T['border'], r=10)
        cv.text((X + cw0 / 2, y0 + 70), {'F': '食物 F', 'M': '鼠 M', 'C': '猫 C'}.get(ch, ch), 24, T['bg'] if food else T['text'], anchor='mm', bold=True)
        cv.text((X + cw0 / 2, y0 + 108), str(c), 16, T['dim'], anchor='mt', mono=True)
    if nd is None:
        return
    line = S.get('_line', 0)
    node, pre = S.get('node'), S.get('pre_node')
    live_node = node is not None and line >= 104
    live_pre = pre is not None and line >= 104
    cw = 70
    y = y0 + 150
    tabs = [(1, '鼠先行动的状态'), (0, '猫先行动的状态')]
    for k, (rd, sub) in enumerate(tabs):
        gx = x0 + 70 + k * (cw * NC + 90)
        cv.text((gx - 52, y), sub, 22, T['text'], bold=True)
        gy = y + 70
        for c in range(NC):
            cv.text((gx + c * cw + cw / 2, gy - 6), f'猫{c}', 18, T['orange'], anchor='mb', bold=True)
        for r in range(NC):
            cv.text((gx - 8, gy + r * cw + cw / 2), f'鼠{r}', 18, T['green'], anchor='rm', bold=True)
            for c in range(NC):
                X, Y = gx + c * cw, gy + r * cw
                nobj = nd.get((0, r, 0, c, rd))
                if nobj is None:
                    cv.rect((X + 2, Y + 2, X + cw - 2, Y + cw - 2), fill=(30, 34, 40), r=6, outline=T['border'])
                    continue
                res = _res(nobj)
                fill = T['green'] if res == '鼠' else T['orange'] if res == '猫' else T['panel2']
                bnd = B.get('node_dict')
                bn = bnd.get((0, r, 0, c, rd)) if bnd else None
                changed = bn is not None and bn.win_state != nobj.win_state
                is_cur = live_node and node is nobj
                is_pre = live_pre and pre is nobj
                oc = T['yellow'] if (is_cur or changed) else T['pink'] if is_pre else T['border']
                cv.rect((X + 2, Y + 2, X + cw - 2, Y + cw - 2), fill=fill, r=6, outline=oc, width=4 if (is_cur or changed or is_pre) else 1)
                cv.text((X + cw / 2, Y + cw / 2 - 4), res if res else '?', 26, T['bg'] if res else T['dim'], anchor='mm', bold=True)
                if res is None and nobj.out_d:
                    cv.text((X + cw - 6, Y + cw - 4), f'd{nobj.out_d}', 15, T['muted'], anchor='rb', mono=True)
    ly = y + 70 + NC * cw + 14
    cv.text((x0 + 18, ly), '绿 = 鼠赢，橙 = 猫赢，? = 未定，dN = out_d：还剩 N 种走法没被判输', 19, T['muted'])
    cv.text((x0 + 18, ly + 28), '黄框 = 正在处理的节点，粉框 = 它的前一状态；深色格 = 不存在（食物 / 抓到后无需再走）', 19, T['muted'])
    if 'round' in S:
        cv.text((x0 + 18, ly + 62), f"BFS 第 {S['round']} 轮", 22, T['cyan'], bold=True)


def _cap_node(S, B, r):
    nd = S.node
    bn = B.get('node')
    if bn is not None and (bn.mx, bn.my, bn.cx, bn.cy, bn.m_round) == (nd.mx, nd.my, nd.cx, nd.cy, nd.m_round):
        return '这一轮队列里的节点都处理完了'
    res = _res(nd)
    return f'处理节点：鼠 `{nd.my}`，猫 `{nd.cy}`，{_who_move(nd.m_round)}先动 → =={res}赢=='


CONFIG = dict(
    num=1728, title='猫和老鼠 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='五元组状态 · 终局倒推 BFS',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2849'],
    code='''
class Node(object):

    def __init__(self, mx, my, cx, cy, m_round):
        self.mx = mx
        self.my = my
        self.cx = cx
        self.cy = cy
        self.m_round = m_round
        self.out_d = 0
        self.g = set()
        self.win_state = None

class Solution(object):
    def canMouseWin(self, grid, catJump, mouseJump):

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '#':
                    continue
                if grid[i][j] == 'C':
                    cx = i
                    cy = j
                elif grid[i][j] == 'M':
                    mx = i
                    my = j
                elif grid[i][j] == 'F':
                    fx = i
                    fy = j
                
        cnt = 0
        node_dict = {}
        for x1 in range(m):
            for y1 in range(n):
                if grid[x1][y1] == '#': #必须是合法单元格
                    continue
                for x2 in range(m):
                    for y2 in range(n):
                        if grid[x2][y2] == '#':
                            continue
                        if x1 == fx and y1 == fy and x2 == fx and y2 == fy: #不会同时出现在食物所在的位置
                            continue

                        if x1 == fx and y1 == fy: #老鼠在上一次操作之后到达了食物，因此只需要记录轮到猫行动的这个状态
                            node_dict[(x1, y1, x2, y2, 0)] = Node(x1, y1, x2, y2, 0)
                        elif x2 == fx and y2 == fy: #猫在上一次操作之后到达了食物，因此只需要记录轮到老鼠行动的这个状态
                            node_dict[(x1, y1, x2, y2, 1)] = Node(x1, y1, x2, y2, 1)
                        elif x1 == x2 and y1 == y2: #猫在上一操作之后抓到了老鼠，因此只需要记录轮到老鼠行动的这个状态
                            node_dict[(x1, y1, x2, y2, 1)] = Node(x1, y1, x2, y2, 1)
                        else:
                            node_dict[(x1, y1, x2, y2, 0)] = Node(x1, y1, x2, y2, 0)
                            node_dict[(x1, y1, x2, y2, 1)] = Node(x1, y1, x2, y2, 1)
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        #预处理pre_state以及out_d
        for node in node_dict.values():
            if node.mx == fx and node.my == fy: #无需考察老鼠吃到食物的下一个状态
                continue
            if node.cx == fx and node.cy == fy: #无需考察猫吃到食物的下一个状态
                continue
            if node.mx == node.cx and node.my == node.cy: #无需考察猫逮到老鼠的下一个状态
                continue

            if node.m_round == 1:
                step_range = mouseJump
                nowx, nowy = node.mx, node.my
            else:
                step_range = catJump
                nowx, nowy = node.cx, node.cy
            
            for index in range(4):
                for l in range(1, step_range + 1):
                    x = dx[index] * l + nowx
                    y = dy[index] * l + nowy

                    if x < 0 or x == m or y < 0 or y == n or grid[x][y] == '#':
                        break
                    if node.m_round == 1:
                        if x == node.cx and y == node.cy: #当前是老鼠行动，老鼠不可能走到猫所在的位置
                            continue
                        next_node = node_dict[(x, y, node.cx, node.cy, 0)]
                    else:
                        next_node = node_dict[(node.mx, node.my, x, y, 1)]
                    
                    node.out_d += 1
                    next_node.g.add(node)

            node.out_d += 1

            node_dict[(node.mx, node.my, node.cx, node.cy, 1 - node.m_round)].g.add(node)
        
        q = []
        for node in node_dict.values():
            if (node.mx == fx and node.my == fy) or (node.cx == fx and node.cy == fy) or (node.mx == node.cx and node.my == node.cy): #三种终局状态均设置为必败
                node.win_state = False
                q.append(node)
        
        l = 0
        r = len(q)
        round = 0
        while l < r and round < 1000:
            round += 1
            for node in q[l : r]:
                if not node.win_state: #当前状态必败，那么上一个状态必胜
                    for pre_node in node.g:
                        if pre_node.win_state is None:
                            pre_node.win_state = True
                            q.append(pre_node)
                else:
                    for pre_node in node.g:
                        pre_node.out_d -= 1
                        if pre_node.out_d == 0: #所有可到达的状态都是必胜，那么必败
                            pre_node.win_state = False
                            q.append(pre_node)
            
            l, r = r, len(q)
        
        if node_dict[(mx, my, cx, cy, 1)].win_state:
            return True
        
        return False
''',
    call=f'Solution().canMouseWin({GRID}, {CAT_J}, {MOUSE_J})',
    expect=True,
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=['round', 'l', 'r'],
    skip=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 95, 96, 97, 98, 99, 101, 102, 103, 107, 110, 112, 116, 117],
    max_steps=60,
    captions={
        'node_dict = {}': '先扫描地图记下 M、C、F 的位置；`node_dict` 存全部状态（鼠位置，猫位置，轮到谁）对应的 `Node`',
        'q = []': '节点已建好：每个节点的 `out_d` = 当前行动方的走法数（含原地不动），`g` = 能走到它的前一状态',
        'l = 0': '终局状态（鼠到食物、猫到食物、猫抓到鼠）都设为 ==必败==（对即将行动的一方）并入队，从它们倒推',
        'round += 1': '第 `{round}` 轮 BFS：处理这一层队列 `q[{l}:{r}]` 里的节点',
        'for node in q[l : r]': _cap_node,
        'if not node.win_state': lambda S, B, r: ('这个状态对行动方 ==必败==：谁能走到它，谁就能赢 → 它的前一状态都标成 ==必胜==' if not S.node.win_state
                                                else '这个状态对行动方 ==必胜==：谁走到它都是送分，只能把前一状态的 `out_d` 减 1'),
        'if pre_node.win_state is None': lambda S, B, r: (f'前一状态：鼠 `{S.pre_node.my}`，猫 `{S.pre_node.cy}`，{_who_move(S.pre_node.m_round)}先动：' +
                                                          ('还没确定' if S.pre_node.win_state is None else '已经确定，跳过')),
        'pre_node.win_state = True': '能走到对方必败的状态 → 这个前一状态对行动方 ==必胜==（`win_state = True`），入队',
        'pre_node.out_d -= 1': lambda S, B, r: f'走到「必胜」状态是死路，排除一种走法：`out_d` = {S.pre_node.out_d}',
        'if pre_node.out_d == 0': lambda S, B, r: ('`out_d` 减到 ==0==：所有走法都通向对方必胜 → 这个前一状态必败' if S.pre_node.out_d == 0
                                                   else f'还剩 `{S.pre_node.out_d}` 种走法，先不下结论'),
        'pre_node.win_state = False': '全部走法都输 → `win_state = False`（必败），入队继续倒推',
        'l, r = r, len(q)': '这一轮处理完，下一轮处理新加入的节点：`l = {l}`，`r = {r}`（队列空就结束）',
        'if node_dict[(mx, my, cx, cy, 1)]': lambda S, B, r: ('倒推结束。看起点（鼠 `{0}`，猫 `{1}`，鼠先动）：`win_state = {2}` → 鼠赢'.format(S.my, S.cy, S.node_dict[(S.mx, S.my, S.cx, S.cy, 1)].win_state)),
        'return True': '起点对鼠先动 ==必胜== → 返回 `True`',
    },
    cards=dict(
        one_liner='五元组表示状态，从三种终局往前一轮一轮推',
        complexity='时间 `O(m^2n^2(m+n))`，空间 `O(m^2n^2)`',
        problem=['网格里有鼠 M、猫 C、食物 F、墙 #；鼠先走，轮流跳，最远 `mouseJump` / `catJump` 格，可以原地不动',
                 '猫抓到鼠 / 猫先到食物 → 猫赢；鼠先到食物 → 鼠赢；老鼠 1000 步内吃不到 → 猫赢',
                 '本视频：地图 `MCF`，`catJump=1, mouseJump=2` → `true`'],
        quote='对于这类有向图无环图中路径有关的问题……一般的做法是先确定出所有的终局状态，然后从这些状态往前倒推。……由于存在步数的限制，因此对于环中的状态，也都是老鼠输。',
        quote_src='—— yiduobo 题解原文',
        idea=['状态 = (鼠位置, 猫位置, 轮到谁)，每个状态存「对当前行动方是否必胜」`win_state`',
              '终局：鼠到食物、猫到食物、猫抓到鼠，对即将行动的一方都是==必败==',
              '倒推：能走到「对方必败」→ 必胜；全部走法都走到「对方必胜」→ 必败（`out_d` 数到 0）。没确定的当作鼠输'],
        summary=['时间 `O(m^2n^2(m+n))`，空间 `O(m^2n^2)`',
                 '`win_state` 是对「当前行动方」说的：鼠先动的节点 True = 鼠赢；猫先动的节点 True = 猫赢',
                 '易错：不要忘了「原地不动」也是一种走法，所以每个节点 `out_d` 要额外加 1；鼠不能走到猫所在的格子（会被抓）',
                 '步数限制靠 `round < 1000` 实现；环里没被确定的状态最后都按「鼠输」处理',
                 '对比灵神：灵神把本题化成 913 的图模型，用 `deg` 倒推；yiduobo 直接为每个状态建 `Node`，思路一致'],
    ),
)
