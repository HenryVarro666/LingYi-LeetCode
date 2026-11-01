DIRS = 'ESWN'
NAMES = ['东', '南', '西', '北']
_I = lambda S: S['_inner']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    d = _I(S)
    ds = S['directions']
    pos = d.get('pos') or [0, 0, 0, 0]
    ps = [d.get('p0'), d.get('p1'), d.get('p2'), d.get('p3')]
    live = d.get('d3') is not None and None not in ps
    moving = {k for k in range(4) if live and ps[k] == pos[k] + 1}
    cv.text((x0 + 18, y0 + 4), '四个车道（左 = 最靠近路口；灰 = 已通过，黄框 = 队首，绿 = 本秒放行）', 22, T['muted'], bold=True)
    cell = 76
    sx = x0 + 150
    y = y0 + 60
    rowh = 92
    for k in range(4):
        Y = y + k * rowh
        cv.text((x0 + 24, Y + 34), f'{NAMES[k]} {DIRS[k]}', 30, T['text'], anchor='lm', bold=True)
        cv.text((x0 + 24 + 92, Y + 34), f'pos={pos[k]}', 22, T['dim'], anchor='lm', mono=True)
        for i, c in enumerate(ds[k]):
            X = sx + i * cell + 70
            passed = i < pos[k]
            head = i == pos[k]
            fill = (52, 60, 72) if passed else T['panel2']
            if head and k in moving:
                fill = T['green']
            cv.rect((X, Y, X + cell - 8, Y + 68), fill=fill, r=10, outline=T['yellow'] if head else T['border'], width=4 if head else 1)
            cv.text((X + (cell - 8) / 2, Y + 34), c, 34, T['bg'] if fill == T['green'] else (T['dim'] if passed else T['text']), anchor='mm', bold=True, mono=True)
        if k in moving:
            cv.text((sx + 70 + max(len(ds[k]), 1) * cell + 10, Y + 34), '→ 本秒放行', 24, T['green'], anchor='lm', bold=True)


def _txt(S):
    d = _I(S)
    if 'pos' not in d:
        return '`valid` = 预处理好的「可以同一秒通行的行动组合」；`f[pos]` = 剩余的车走完最少几秒'
    return f"状态 `pos = {d['pos']}`（东南西北已走掉的车数）"


CONFIG = dict(
    num='LCP 43', title='十字路口的交通', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='预处理路线交点 + 记忆化搜索',
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
    call='Solution().trafficCommand(["W", "N", "", ""])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='calls', h=150, hide=('trafficCommand',)),
    ],
    watch=[('pos', lambda S: S['_inner'].get('pos'), 'blue'), ('d0..d3', lambda S: (S['_inner'].get('d0'), S['_inner'].get('d1'), S['_inner'].get('d2'), S['_inner'].get('d3')) if S['_inner'].get('d3') is not None else None, 'orange')],
    skip=[8, 27, 28, 29, 30, 31, 32, 38, 39, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 96, 97, 98, 99, 102, 105, 106, 107, 108, 111],
    captions={
        'max_l = [': '每条车道的车数 `max_l = {max_l}`（东南西北）',
        'f = [[[[None]': '`f[a][b][c][d]`：东南西北各走掉 a、b、c、d 辆后，走完剩下的车最少几秒；`None` = 还没算',
        'points_matrix = [[': '把十字路口画成 7×7 点阵：数字 1-16 是各条路线可能相交的==交叉点==',
        'start_coord = ': '四个方向的起点坐标：东 `[2,6]`、南 `[6,4]`、西 `[4,0]`、北 `[0,2]`',
        'd_map = {': '方向字符 → 编号：`E=0, S=1, W=2, N=3`',
        'return dfs([0': lambda B, S, r: (f'预处理已跑完：沿每条路线走过的交叉点，同一交叉点被两辆车用到就冲突 → `valid` 里存了 `{len(S.valid)}` 种不冲突的行动组合。现在从 `pos = [0,0,0,0]` 开始搜'),
        'is not None': lambda B, S, r: ('这个状态算过 → 直接返回记忆值' if S.f[S.pos[0]][S.pos[1]][S.pos[2]][S.pos[3]] is not None else '这个状态还没算过'),
        'if pos == max_l': lambda B, S, r: ('所有车都走完了 → 还要 0 秒' if S.pos == S.max_l else f'`pos = {S.pos}`，还有车没走完'),
        'return 0': '没车了：`0` 秒',
        'if pos[d] < max_l[d]': lambda B, S, r: (f"`{['东','南','西','北'][S.d]}` 车道还有车 → 除了「停着」，还可以让队首车走" if S.pos[S.d] < S.max_l[S.d]
                                                else f"`{['东','南','西','北'][S.d]}` 车道没车了 → 只能「停着」"),
        'target_d = d_map': "`{['东','南','西','北'][d]}` 车道队首车开往 `{directions[d][pos[d]]}`（编号 {target_d}）：候选「走」= `[{pos[d] + 1}, {target_d}]`",
        '= sum(max_l) + 1': '先把当前状态记成「最坏」`sum(max_l)+1 = {sum(max_l) + 1}` 秒，再在下面取更小值',
        'in valid': lambda B, S, r: (f'这一秒的行动 `({S.d0}, {S.d1}, {S.d2}, {S.d3})`（等于自己的编号 = 停着）' + ('在 `valid` 里 → ==路线不冲突==' if (S.d0, S.d1, S.d2, S.d3) in S.valid else '不在 `valid` 里 → 冲突或全都不动，跳过')),
        'min(f[pos': lambda B, S, r: f'放行后进入 `[{B.p0}, {B.p1}, {B.p2}, {B.p3}]`：这个状态的答案 = `min(当前, dfs(新状态) + 1)`',
        'return f[pos[0]][pos[1]][pos[2]][pos[3]]': lambda B, S, r: f'`pos = {S.pos}` 最少需要 =={r}== 秒',
    },
    max_events=200000,
    max_steps=58,
    cards=dict(
        one_liner='先把「哪些行动能同一秒通行」预处理成集合，再对车道进度做记忆化搜索',
        complexity='状态 `O(n^4)`，每个状态枚举至多 `2^4` 种行动，用 `valid` 集合 `O(1)` 判断',
        problem=['十字路口四个方向（东南西北）各有一队车，`directions[i]` 记录每辆车要开往的方向',
                 '每秒各车道只能走队首一辆，且路线不能相交，求最少几秒走完',
                 '示例：`["W","N","ES","W"]` → `2`；本视频：`["W","N","",""]` → `2`'],
        quote='两条线路交叉的话必然存在某个交叉点……若某个交点被经过了多次，说明这个线路组合就是不行的。',
        quote_src='—— yiduobo 题解原文',
        idea=['把路口画成 7×7 点阵，给 16 个交叉点编号，从四个起点沿三个方向走，记下经过的交叉点',
              '四个方向各「停着」或「走」，用计数表判断交叉点有没有被重复占用，合法组合存进 `valid`',
              '`f[pos]`：各车道已走掉的车数为 `pos` 时的最少秒数，对每个合法行动 `+1` 递归取最小'],
        summary=['预处理一次，之后判断 `(d0,d1,d2,d3) in valid` 只要 `O(1)`',
                 '全部不动的组合 `cnt` 为空，被当作不合法；否则会原地踏步死循环',
                 '先把当前状态记成 `sum(max_l)+1` 再更新，避免写错初值',
                 '原文为 Python 2 风格，本题代码无需改动（仅删去了类型说明文档字符串）；预处理循环在视频里略去逐行动画，只展示结果',
                 '对比灵神：他把一辆车旋转到方向 0 来判断冲突，这里用交叉点计数'],
    ),
)
