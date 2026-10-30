POS = [(3, 3), (1, 1)]
NAMES = ['象A', '象B']
COLS = ['blue', 'pink', 'green', 'purple']


def _sim(final):
    """和 check 一样逐秒模拟：返回 (秒数, 格子) 或 None"""
    cur = [list(p) for p in POS]
    t = 0
    while any(cur[k] != list(final[k]) for k in range(len(POS))):
        t += 1
        seen = {}
        for k in range(len(POS)):
            for a in (0, 1):
                if cur[k][a] != final[k][a]:
                    cur[k][a] += 1 if cur[k][a] < final[k][a] else -1
            key = tuple(cur[k])
            if key in seen:
                return t, key
            seen[key] = k
    return None


def _desc(p, k):
    return '原地不动' if list(p) == list(POS[k]) else f'走到 ({p[0]}, {p[1]})'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    now = S.get('now') or []
    cv.text((x0 + 18, y0 + 4), '棋盘（箭头 = 选好的目的地，红叉 = 逐秒模拟时的冲突）', 22, T['muted'], bold=True)
    cell = min((x1 - x0 - 330) / 8, (y1 - y0 - 100) / 8, 70)
    sx, sy = x0 + 70, y0 + 72
    for r in range(8):
        for c in range(8):
            X, Y = sx + c * cell, sy + r * cell
            cv.rect((X, Y, X + cell, Y + cell), fill=T['panel2'] if (r + c) % 2 == 0 else (30, 36, 46), outline=T['border'])
    for k in range(8):
        cv.text((sx + k * cell + cell / 2, sy - 6), k + 1, 17, T['dim'], anchor='mb', mono=True)
        cv.text((sx - 8, sy + k * cell + cell / 2), k + 1, 17, T['dim'], anchor='rm', mono=True)

    def ctr(p):
        return sx + (p[1] - 1) * cell + cell / 2, sy + (p[0] - 1) * cell + cell / 2

    full = len(now) == len(POS)
    bad = _sim(now) if full else None
    for k, p in enumerate(now):
        a, b = ctr(POS[k]), ctr(p)
        col = T['yellow'] if k == len(now) - 1 else T[COLS[k]]
        if list(p) != list(POS[k]):
            cv.arrow(a, b, col, 6, 14)
        cv.rect((b[0] - cell * 0.2, b[1] - cell * 0.2, b[0] + cell * 0.2, b[1] + cell * 0.2), outline=col, width=4, r=5)
    for k, p in enumerate(POS):
        X, Y = ctr(p)
        cv.rect((X - cell * 0.36, Y - cell * 0.36, X + cell * 0.36, Y + cell * 0.36), fill=T[COLS[k]], r=cell * 0.2)
        cv.text((X, Y), '象', 24, T['bg'], anchor='mm', bold=True)
    if bad:
        X, Y = ctr(bad[1])
        cv.line([(X - 14, Y - 14), (X + 14, Y + 14)], T['red'], 6)
        cv.line([(X - 14, Y + 14), (X + 14, Y - 14)], T['red'], 6)
    tx = sx + 8 * cell + 36
    cv.text((tx, sy), '各棋子选的目的地', 22, T['muted'], bold=True)
    for k in range(len(POS)):
        yy = sy + 40 + k * 70
        cv.rect((tx, yy, tx + 18, yy + 18), fill=T[COLS[k]], r=4)
        cv.text((tx + 28, yy - 4), f'{NAMES[k]} {POS[k]}', 22, T['text'], bold=True)
        cv.text((tx + 28, yy + 24), _desc(now[k], k) if k < len(now) else '尚未选择', 20, T['text'] if k < len(now) else T['dim'])
    if full:
        yy = sy + 40 + 2 * 70
        cv.text((tx, yy), '逐秒模拟 check：', 22, T['yellow'], bold=True)
        cv.text((tx, yy + 32), f'第 {bad[0]} 秒同在 {bad[1]}' if bad else '全程没有重叠', 21, T['red'] if bad else T['green'], bold=True)


def _chk(S, B, r):
    now = S.now
    bad = _sim(now)
    if bad:
        return f'`check`：两枚象逐秒各走一步，第 =={bad[0]}== 秒同时到 `{bad[1]}` → ==重叠，返回 False==，这个组合不计数'
    return '`check`：逐秒模拟到两枚象都到达目的地，==从未同格== → 返回 True'


CONFIG = dict(
    num=2056, title='棋盘上有效移动组合的数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举所有目的地组合 + 逐秒模拟',
    tags=['灵神题单·常用数据结构', '灵神题单·链表树与回溯', '难度分 2611'],
    code='''
class Solution(object):
    def countCombinations(self, pieces, positions):

        dx = {}
        dy = {}

        dx[0] = [1, 0, -1, 0]
        dy[0] = [0, -1, 0, 1]

        dx[1] = [1, 1, 0, -1, -1, -1, 0, 1]
        dy[1] = [0, -1, -1, -1, 0, 1, 1, 1]

        dx[2] = [1, -1, -1, 1]
        dy[2] = [-1, -1, 1, 1]

        final_target = []
        n = len(pieces)

        for index in range(n):
            final_target.append([])
            final_target[-1].append(positions[index])
            if pieces[index] == "rook":
                type = 0
            elif pieces[index] == "queen":
                type = 1
            else:
                type = 2
            
            for d in range(len(dx[type])):
                nowx, nowy = positions[index]
                while True:
                    nowx += dx[type][d]
                    nowy += dy[type][d]
                    if nowx == 0 or nowy == 0 or nowx == 9 or nowy == 9:
                        break
                    final_target[-1].append([nowx, nowy])
        
        self.res = 0
        self.dfs(0, n, [], final_target, positions)
        return self.res

    def check(self, n, origin, final):
        at_pos = 0
        nowx = []
        nowy = []
        for index in range(n):
            if origin[index][0] == final[index][0] and origin[index][1] == final[index][1]:
                at_pos += 1
            nowx.append(origin[index][0])
            nowy.append(origin[index][1])
        
        while at_pos < n:
            used = set()
            at_pos = 0
            for index in range(n):
                at_pos_flag = True

                if nowx[index] != final[index][0]:
                    at_pos_flag = False
                    if nowx[index] > final[index][0]:
                        nowx[index] -= 1
                    else:
                        nowx[index] += 1

                if nowy[index] != final[index][1]:
                    at_pos_flag = False
                    if nowy[index] > final[index][1]:
                        nowy[index] -= 1
                    else:
                        nowy[index] += 1
                
                if at_pos_flag:
                    at_pos += 1

                key = (nowx[index] - 1) * 8 + nowy[index]
                if key not in used:
                    used.add(key)
                else:
                    return False
        
        return True

    def dfs(self, level, n, now, final_target, positions):
        if level == n:
            if self.check(n, positions, now):
                self.res += 1
            return

        for pos in final_target[level]:
            now.append(pos)
            self.dfs(level + 1, n, now, final_target, positions)
            now.pop()
''',
    call="Solution().countCombinations(['bishop', 'bishop'], [[3, 3], [1, 1]])",
    expect=60,
    skip=['dx[', 'dy[', 'dx = {}', 'dy = {}', 'final_target[-1].append', 'final_target.append([])', 'if origin[', 'if pieces[index]', 'elif pieces', 'else:', 'type = ',
          'for d in range', 'nowx, nowy', 'while True', 'nowx +=', 'nowy +=', 'if nowx == 0', 'break', 'for index in range(n):',
          'at_pos', 'nowx', 'nowy', 'used', 'key', 'return False', 'return True', 'now.append(pos)', 'now.pop()',
          'if level == n', 87],
    max_steps=42, max_events=400000,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='calls', h=120, hide=('final_target', 'positions')),
    ],
    watch=['level', ('res', 'self.res', 'green')],
    captions={
        'final_target = []': '先算出每枚棋子所有的目的地：==原地不动 + 每个方向走到边界前的每一格==',
        'n = len(pieces)': '`n = {n}`',
        'self.res = 0': lambda S, B, r: f'目的地都算好了：象A 有 `{len(S.final_target[0])}` 个，象B 有 `{len(S.final_target[1])}` 个，组合最多 `{len(S.final_target[0]) * len(S.final_target[1])}` 种',
        'self.dfs(0, n': '从第 0 枚棋子开始枚举目的地组合',
        'return self.res': '有效组合共 =={ret}== 个',
        'for pos in final_target[level]': lambda S, B, r: (f'枚举{NAMES[S.level]}的目的地：`pos = {S.pos}`' if B.get('pos') != S.pos or B.get('level') != S.level
                                                          else f'{NAMES[S.level]}的目的地都试完了，回到上一层'),
        'self.dfs(level + 1': lambda S, B, r: (f'{NAMES[B.level]}去 `{B.pos}`，再枚举{NAMES[B.level + 1]}的目的地' if B.level + 1 < S.n
                                              else f'{NAMES[B.level]}去 `{B.pos}`，所有棋子的目的地都定好了'),
        'if self.check(': _chk,
        'self.res += 1': '这个组合有效 → `res` = =={self.res}==',
    },
    cards=dict(
        one_liner='目的地最多几十个，枚举所有组合，再逐秒模拟判冲突',
        complexity='时间 `O(M^n × n × L)`，空间 `O(n × M)`',
        problem=['8×8 棋盘上最多 4 个棋子（车 / 后 / 象），每个棋子选一个方向和步数，==同时==每秒走一步',
                 '任意时刻两个棋子占同一格就==无效==；可以原地不动',
                 '示例：`["rook"]` `[[1,1]]` → `15`；本视频用两个象 `(3,3)`、`(1,1)` → `60`'],
        quote='因此可以先计算出每颗棋子的所有的目的地，然后枚举每一种组合，最后的组合总数也就不到30^4。对于枚举到的最终情况，则可以从起始状况一步一步开始模拟，判断在棋子移动的过程中是否会出现棋子在某一时刻走到同一位置引起冲突的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['只记==目的地==，不记方向和步数：目的地列表 = 原地 + 各方向的每一格',
              '`dfs` 逐个棋子选目的地，选满 `n` 个才调用 `check`',
              '`check` 每秒让每个棋子往目的地走一步（x、y 各 ±1 或不动），用 `used` 集合判断同一秒有没有两个棋子同格',
              '所有棋子都到达目的地且没有重叠才算有效'],
        summary=['时间约 `O(M^n × n × 8)`：`M ≤ 28`，`n ≤ 4`，量级几十万次模拟',
                 '易错：到达目的地的棋子==停在原地继续占格子==，所以 `check` 要一直模拟到全部到达',
                 '目的地相同的组合在第一秒到终点前就会被发现冲突，不会漏掉',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神边枚举边用 `is_valid` 剪枝，yiduobo 先选满再整体验证；视频里 `check` 内部没有逐行展示'],
    ),
)
