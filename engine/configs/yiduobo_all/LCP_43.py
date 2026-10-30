NAMES = ['东', '南', '西', '北']
DIRS = ['W', '', '', 'W']


def _I(S):
    return S['_inner']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    I = S['_inner']
    ds = S['directions']
    pos = I.get('pos')
    cv.text((x0 + 18, y0 + 4), '四条车道（暗 = 已开走，黄框 = 这一秒要走的车）', 22, T['muted'], bold=True)
    rowh = (y1 - y0 - 50) / 4
    cell, gap = min(64, rowh - 14), 10
    cand = None
    if all(k in I for k in ('d0', 'd1', 'd2', 'd3', 'p0', 'p1', 'p2', 'p3')):
        cand = [I['p0'], I['p1'], I['p2'], I['p3']]
    for d in range(4):
        y = y0 + 48 + d * rowh
        cv.text((x0 + 24, y + cell / 2), NAMES[d], 30, T['text'], anchor='lm', bold=True)
        q = ds[d]
        if not q:
            cv.text((x0 + 100, y + cell / 2), '（没有车）', 22, T['dim'], anchor='lm')
            continue
        for j, ch in enumerate(q):
            X = x0 + 100 + j * (cell + gap)
            gone = pos is not None and j < pos[d]
            front = pos is not None and j == pos[d]
            moving = cand is not None and pos is not None and cand[d] == pos[d] + 1 and j == pos[d]
            fill = T['panel2']
            cv.rect((X, y, X + cell, y + cell), fill=fill, r=8,
                    outline=T['yellow'] if moving else (T['blue'] if front else T['border']), width=4 if (moving or front) else 1)
            cv.text((X + cell / 2, y + cell / 2), '去' + NAMES['ESWN'.index(ch)], 24,
                    T['dim'] if gone else T['text'], anchor='mm', bold=True)
        if pos is not None and pos[d] >= len(q):
            cv.text((x0 + 100 + len(q) * (cell + gap) + 10, y + cell / 2), '空了', 22, T['green'], anchor='lm', bold=True)


def _in_valid(S, B, r):
    pos = S.pos
    ps = [S.p0, S.p1, S.p2, S.p3]
    ds = [S.d0, S.d1, S.d2, S.d3]
    desc = '、'.join(NAMES[k] + ('停' if ps[k] == pos[k] else '去' + NAMES[ds[k]]) for k in range(4))
    if all(ps[k] == pos[k] for k in range(4)):
        return f'方案「{desc}」：谁都不走，不算一秒 → 不在 `valid`'
    if (S.d0, S.d1, S.d2, S.d3) in S.valid:
        return f'方案「{desc}」：路线不相交、也没有同进同出 → ==合法=='
    going = [ds[k] for k in range(4) if ps[k] != pos[k]]
    if len(going) != len(set(going)):
        return f'方案「{desc}」：两辆车开往同一个方向，同一秒只能驶入一辆 → ==不合法=='
    return f'方案「{desc}」：路线有交叉点 → ==不合法=='


def _combo(S):
    I = S['_inner']
    if 'pos' not in I:
        return ''
    if not all(k in I for k in ('d0', 'd1', 'd2', 'd3')):
        return f'`pos = {I["pos"]}`：各车道已经开走的车数'
    pos = I['pos']
    ps = [I['p0'], I['p1'], I['p2'], I['p3']]
    ds = [I['d0'], I['d1'], I['d2'], I['d3']]
    parts = []
    for k in range(4):
        parts.append(f'{NAMES[k]}' + ('停' if ps[k] == pos[k] else f'→{NAMES[ds[k]]}'))
    return '试这一秒的方案：`' + '　'.join(parts) + '`'


CONFIG = dict(
    num='LCP 43', title='十字路口的交通', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='记忆化搜索 · 预处理合法组合',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def trafficCommand(self, directions):

        max_l = [len(directions[0]), len(directions[1]), len(directions[2]), len(directions[3])]

        f = [[[[None] * (max_l[3] + 1) for _ in range(max_l[2] + 1)] for _ in range(max_l[1] + 1)] for _ in range(max_l[0] + 1)]

        """

                1       2

                    3

        4       5       6       7

            8               9

        10      11      12      13

                    14

                15      16

        """

        points_matrix = [[0,  0,  1,  0,  2,  0,  0],
                         [0,  0,  0,  3,  0,  0,  0],
                         [4,  0,  5,  0,  6,  0,  7],
                         [0,  8,  0,  0,  0,  9,  0],
                         [10, 0, 11,  0,  12, 0, 13],
                         [0,  0,  0, 14,  0,  0,  0],
                         [0,  0, 15,  0,  16, 0,  0]]

        start_coord = [[2, 6], [6, 4], [4, 0], [0, 2]]
        #dx和dy表示路线上坐标的变化
        #其中dx[0]、dy[0]表示东方的车辆路线，因此只需要考虑原地不动、左下、左、左上三个方向
        #另外三个方向的dx和dy也是一样
        dx = [[0, 1, 0, -1], [-1, 0, -1, -1], [0, 1, 0, -1], [1, 1, 1, 0]]
        dy = [[0, -1, -1, -1], [1, 0, -1, 0], [1, 1, 0, 1], [1, 0, -1, 0]]
        d_map = {'E': 0, 'S': 1, 'W': 2, 'N': 3}

        candidate_list = []
        for d in range(4):
            candidate_list.append([])
            candidate_list[-1].append([d, []])
            for target_d in range(4):
                if d == target_d:
                    continue
                
                x = start_coord[d][0] + dx[d][target_d]
                y = start_coord[d][1] + dy[d][target_d]
                used_points = []
                #将当前行进路线上经过的交叉点加入到used_points中
                while x >= 0 and x < 7 and y >= 0 and y < 7:
                    if points_matrix[x][y] > 0:
                        used_points.append(points_matrix[x][y])
                    x += dx[d][target_d]
                    y += dy[d][target_d]
                
                #candidate_list储存的是当前方向上，目的地为target_d时需要经过的交叉点集合used_points
                candidate_list[-1].append([target_d, used_points[:]])

        #valid储存合法的行车方案
        valid = set()

        #枚举四个方向上行车方案的组合
        for p0, used0 in candidate_list[0]:
            for p1, used1 in candidate_list[1]:
                for p2, used2 in candidate_list[2]:
                    for p3, used3 in candidate_list[3]:
                        #cnt记录经过交叉点的次数
                        cnt = {}
                        for p in used0:
                            cnt[p] = cnt.get(p, 0) + 1
                        for p in used1:
                            cnt[p] = cnt.get(p, 0) + 1
                        for p in used2:
                            cnt[p] = cnt.get(p, 0) + 1
                        for p in used3:
                            cnt[p] = cnt.get(p, 0) + 1

                        #cnt为空表示所有方向的车辆都在原地停留，这也是不合法的行动方案
                        if not cnt or max(cnt.values()) != 1:
                            continue
                        
                        valid.add((p0, p1, p2, p3))
        
        #记忆化搜索实现
        def dfs(pos, f):
            if f[pos[0]][pos[1]][pos[2]][pos[3]] is not None:
                return f[pos[0]][pos[1]][pos[2]][pos[3]]
            
            if pos == max_l:
                return 0
            
            candidate_list = []
            for d in range(4):
                candidate_list.append([])
                candidate_list[-1].append([pos[d], d])
                if pos[d] < max_l[d]:
                    target_d = d_map[directions[d][pos[d]]]
                    candidate_list[-1].append([pos[d] + 1, target_d])
            
            f[pos[0]][pos[1]][pos[2]][pos[3]] = sum(max_l) + 1
            for p0, d0 in candidate_list[0]:
                for p1, d1 in candidate_list[1]:
                    for p2, d2 in candidate_list[2]:
                        for p3, d3 in candidate_list[3]:
                            if (d0, d1, d2, d3) in valid:
                                f[pos[0]][pos[1]][pos[2]][pos[3]] = min(f[pos[0]][pos[1]][pos[2]][pos[3]], dfs([p0, p1, p2, p3], f) + 1)
            
            return f[pos[0]][pos[1]][pos[2]][pos[3]]
        
        return dfs([0, 0, 0, 0], f)
''',
    call=f'Solution().trafficCommand({DIRS})',
    expect=2,
    skip=[8, 39, 40] + list(range(26, 33)) + list(range(43, 63)) + list(range(65, 88)) + [96, 97, 98, 99, 100, 101, 102, 103, 105, 106, 107, 108],
    views=[
        dict(type='custom', draw=_draw, h=450),
        dict(type='text', fn=_combo, h=70),
        dict(type='calls', h=170, hide=('f',)),
    ],
    watch=[('pos', lambda S: S['_inner'].get('pos'), 'blue'), ('max_l', 'max_l', 'cyan'),
           ('f[pos]', lambda S: S['_inner']['f'][S['_inner']['pos'][0]][S['_inner']['pos'][1]][S['_inner']['pos'][2]][S['_inner']['pos'][3]] if 'pos' in S['_inner'] else None, 'green')],
    captions={
        'max_l = [': '东南西北各有 `{max_l}` 辆车；`pos` 记录各车道「已经开走几辆」，它就是 DP 状态',
        'f = [[[[None]': '`f[p0][p1][p2][p3]`：四维记忆表，`None` 表示还没算过',
        'start_coord': '预处理：把路口画成 `7×7` 矩阵，交叉点编号 1..16，四个方向的入口坐标是 `start_coord`',
        'dx = [': '`dx / dy`：每个方向有「停着」和三条路线（左转、直行、右转），沿路线走就得到经过的交叉点',
        'candidate_list = []': '对每个方向、每个目的地，沿路线走一遍，记下途经的交叉点（这段循环已折叠）',
        'valid = set()': '`valid`：路线两两不交叉、且至少有一辆在走的方案集合；256 种组合的枚举已折叠，下面直接用',
        'return dfs([0, 0, 0, 0], f)': '预处理完成，`valid` 里一共 `{len(valid)}` 种合法方案；从 `pos = [0,0,0,0]`（没有车开走）开始 `dfs`',
        'is not None': lambda S, B, r: (f'`f{S.pos}` 已经算过 → 直接返回，这就是记忆化' if S.f[S.pos[0]][S.pos[1]][S.pos[2]][S.pos[3]] is not None
                                        else f'`pos = {S.pos}`：还没算过，往下算'),
        'if pos == max_l': lambda S, B, r: (f'`pos = {S.pos}` == `max_l`：所有车都开走了，还需要 `0` 秒' if S.pos == S.max_l
                                            else f'`pos = {S.pos}`，`max_l = {S.max_l}`：还有车在等，枚举这一秒的走法'),
        'return 0': '没有剩余的车，==0 秒==',
        '= sum(max_l) + 1': '先把 `f[pos]` 设成「不可能」的大数 `{sum(max_l) + 1}`，后面用 `min` 取最优',
        'in valid': _in_valid,
        '= min(f[pos[0]]': lambda S, B, r: (f'选这个方案走 1 秒：`pos` 从 `{B.pos}` 变成 `[{B.p0}, {B.p1}, {B.p2}, {B.p3}]`，递归求剩下的最少秒数，再 `+ 1`'),
        'return f[pos[0]][pos[1]][pos[2]][pos[3]]': lambda S, B, r: (f'记忆命中，返回 `{r}`' if S._line == 91 else f'`pos = {S.pos}` 的车走完最少需要 =={r}== 秒'),
    },
    max_steps=60,
    max_events=200000,
    cards=dict(
        one_liner='状态 = 每条车道已开走几辆；每秒枚举「谁走」，只保留路线不交叉的组合',
        complexity='状态 `Π(len+1)`，每个状态枚举 `≤ 2^4` 种组合',
        problem=['十字路口四个方向（东南西北）各有一队车，每辆车有目的方向',
                 '每秒每条车道只能放走最前面一辆，且路线不能相交、不能同进同出',
                 '示例：`["W","N","ES","W"]` → `2`'],
        quote='题目非常贴心地把路口的图示给了出来，可以发现，在题目给出的图中，两条线路交叉的话必然存在某个交叉点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[p0][p1][p2][p3]`：四个方向分别开走 `p` 辆后，剩下的车走完最少几秒',
              '预处理：把路口画成 `7×7` 矩阵，每个交叉点编号；一辆车的路线 = 经过的编号集合',
              '四个方向的选择组合里，任何交叉点被走 2 次就不合法；其余存进 `valid`'],
        summary=['时间约 `O(Π(len+1) × 16)`，空间 `O(Π(len+1))`',
                 '全部都停着（`cnt` 为空）也算不合法，否则会无限递归',
                 '`dfs` 里先把 `f[pos]` 置成 `sum(max_l) + 1`，再取 min，起到「正在算」的标记',
                 '原文为 Python 2 风格，代码无需修改；视频中预处理的循环（256 种组合）已折叠，只演示 `dfs`'],
    ),
)
