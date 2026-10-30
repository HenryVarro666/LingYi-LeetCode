N, M = 2, 2


def _coords():
    cl = [(0, i) for i in range(M)] + [(i, M) for i in range(N)] + [(N, i) for i in range(M, 0, -1)] + [(i, 0) for i in range(N, 0, -1)]
    return cl


def _cur(S):
    p, pos, P = S.get('p'), S.get('pos'), S.get('self.path')
    if P is None or not isinstance(p, int) or not isinstance(pos, int) or p >= len(P):
        return None
    return p, pos % len(P[p]), P[p]


def _draw_box(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '黑盒：绿 = 已打开，黄 = 当前光路，橙圈 = 当前节点', 22, T['muted'], bold=True)
    cl = _coords()
    cell = min((x1 - x0 - 200) / M, (y1 - y0 - 150) / N, 120)
    ox = x0 + (x1 - x0 - cell * M) / 2
    oy = y0 + 84 + ((y1 - y0 - 150) - cell * N) / 2

    def pt(h):
        x, y = cl[h]
        return ox + y * cell, oy + x * cell

    cv.rect((ox, oy, ox + cell * M, oy + cell * N), outline=T['border'], width=3)
    cur = _cur(S)
    openset = S.get('self.open_index') or set()
    if cur:
        p, pos, path = cur
        cyc = p not in (S.get('self.corner_path') or ())
        pts = [pt(v // 2) for v in path]
        segs = list(zip(pts, pts[1:] + ([pts[0]] if cyc else [])))
        for a, b in segs:
            cv.line([a, b], T['yellow'], 4)
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            dx, dy = b[0] - a[0], b[1] - a[1]
            d = max(1e-6, (dx * dx + dy * dy) ** 0.5)
            cv.arrow((mx - dx / d * 14, my - dy / d * 14), (mx + dx / d * 14, my + dy / d * 14), T['yellow'], 4, 12)
    for h in range(len(cl)):
        X, Y = pt(h)
        x, y = cl[h]
        on = h in openset
        cv.rect((X - 11, Y - 11, X + 11, Y + 11), fill=T['green'] if on else T['panel2'], outline=T['muted'], width=2, r=11)
        lx = X + (-30 if y == 0 else 30 if y == M else 0)
        ly = Y + (-26 if x == 0 else 26 if x == N else 0)
        if (x in (0, N)) and (y in (0, M)):
            lx, ly = X + (-30 if y == 0 else 30), Y + (-26 if x == 0 else 26)
        cv.text((lx, ly), h, 22, T['green'] if on else T['text'], anchor='mm', bold=True)
    if cur:
        p, pos, path = cur
        X, Y = pt(path[pos] // 2)
        cv.rect((X - 19, Y - 19, X + 19, Y + 19), outline=T['orange'], width=5, r=19)


def _arr(name, n=15):
    def f(S):
        P = S.get('p')
        A = S.get(name)
        if not isinstance(P, int) or not A or P >= len(A):
            return None
        return ['-' if v is None else v for v in A[P][:n]]
    return f


def _pathv(S):
    c = _cur(S)
    if not c:
        return None
    p, pos, path = c
    return path * (1 if p in S['self.corner_path'] else 2)



CONFIG = dict(
    num='LCP 27', title='黑盒光线反射', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='光路预处理 + 线段树维护最近的打开孔',
    tags=[],
    code='''
class BlackBox(object):

    def __init__(self, n, m):
        
        #coord_list记录的是盒子上各个点的下标到矩形二维下标的映射
        coord_list = []
        for index in range(m):
            coord_list.append([0, index])
        for index in range(n):
            coord_list.append([index, m])
        for index in range(m, 0, -1):
            coord_list.append([n, index])
        for index in range(n, 0, -1):
            coord_list.append([index, 0])

        #coord_map是coord_list的逆向映射
        coord_map = {}
        for index, coord in enumerate(coord_list):
            coord_map[(coord[0], coord[1])] = index
        
        #path和belong分别记录每条光路，以及每个编码后的节点位于哪条光路的第几个节点
        self.path = []
        self.belong = {}

        #get_path的作用是从编码后的节点now开始寻找光路
        def get_path(now):
            self.path.append([now])
            self.belong[now] = [len(self.path) - 1, 0]
            while True:
                direct = now % 2
                now //= 2
                x, y = coord_list[now]
                if x == 0:
                    if direct == 0:
                        #当x和direct都等于0时，表示从盒子上边往右下方向前进
                        #通过二维坐标计算最多可前进的距离dis
                        dis = min(m - y, n)
                        #dx和dy表示原始坐标x和y更新的方向
                        dx, dy = 1, 1
                    else:
                        #direct为1表示从盒子上边往左下方向前进
                        dis = min(y, n)
                        dx, dy = 1, -1
                elif y == m:
                    if direct == 0:
                        #右边往左上
                        dis = min(x, m)
                        dx, dy = -1, -1
                    else:
                        #右边往左下
                        dis = min(n - x, m)
                        dx, dy = 1, -1
                elif x == n:
                    if direct == 0:
                        #下边往左上
                        dis = min(y, n)
                        dx, dy = -1, -1
                    else:
                        #下边往右上
                        dis = min(m - y, n)
                        dx, dy = -1, 1
                else:
                    if direct == 0:
                        #左边往右下
                        dis = min(n - x, m)
                        dx, dy = 1, 1
                    else:
                        #左边往右上
                        dis = min(x, m)
                        dx, dy = -1, 1

                #计算下一个节点的坐标，然后得到其在盒子上对应的节点
                x += dis * dx
                y += dis * dy
                next = coord_map[(x, y)]
                if next == 0 or next == m or next == m + n or next == m + m + n:
                    #如果来到了一个角落上的节点，说明这是一条走到头的单链光路，更新后直接退出
                    if next == m or next == m + m + n:
                        next += next + 1
                    else:
                        next += next
                    self.path[-1].append(next)
                    break
                
                #否则对下一个节点进行编码
                elif direct == 0:
                    next += next + 1
                else:
                    next += next
                
                #若下一个编码后节点被访问过，说明这是一条走完了一遍的环形光路，直接退出
                if next in self.belong:
                    break
                #否则更新belong和path，然后继续往下走
                self.belong[next] = [len(self.path) - 1, len(self.path[-1])]
                self.path[-1].append(next)
                now = next
        
        #首先计算从四个角出发的单链光路
        get_path(0)
        get_path(m + m + 1)
        get_path(m + n + m + n)
        get_path(m + n + m + m + n + m + 1)
        #接下来计算环形光路
        for index in range((m + n) * 4):
            if index in (1, m + m, m + n + m + n + 1, m + n + m + m + n + m):
                continue
            if index not in self.belong:
                get_path(index)
        p1 = self.belong[0][0]
        p2 = self.belong[m + m + 1][0]
        p3 = self.belong[m + n + m + n][0]
        p4 = self.belong[m + n + m + m + n + m + 1][0]
        #corner_path记录单链光路在path数组中的下标
        self.corner_path = set([p1, p2, p3, p4])

        self.f = []
        self.l_max = []
        for index, p in enumerate(self.path):
            if index in self.corner_path:
                #初始化线段树需要的空间
                self.f.append([0] * (len(p) * 4))
                self.l_max.append([None] * (len(p) * 4))
            else:
                #环形光路需要双倍
                self.f.append([0] * (len(p) * 8))
                self.l_max.append([None] * (len(p) * 8))

        #open_index记录当前盒子上有哪些节点被打开了
        self.open_index = set()

    def insert(self, p, pos, delta):
        def put(now, left, right, pos, delta, f, l_max):
            f[now] += delta
            if left == right:
                if f[now] > 0:
                    l_max[now] = pos
                else:
                    l_max[now] = None
                return
            
            mid = (left + right) >> 1
            if pos <= mid:
                put(now + now + 1, left, mid, pos, delta, f, l_max)
            else:
                put(now + now + 2, mid + 1, right, pos, delta, f, l_max)
            
            if f[now + now + 1] > 0:
                l_max[now] = l_max[now + now + 1]
            elif f[now + now + 2] > 0:
                l_max[now] = l_max[now + now + 2]
            else:
                l_max[now] = None

        #单链光路只需要更新其在path中的位置
        if p in self.corner_path:
            left, right = 0, len(self.path[p]) - 1
            put(0, left, right, pos, delta, self.f[p], self.l_max[p])
        #环形光路需要更新原始位置和复制后位置两个地方
        else:
            left, right = 0, len(self.path[p]) * 2 - 1
            put(0, left, right, pos, delta, self.f[p], self.l_max[p])
            pos += len(self.path[p])
            put(0, left, right, pos, delta, self.f[p], self.l_max[p])

    def query(self, p, pos):
        if p in self.corner_path:
            left, right = 0, len(self.path[p]) - 1
        else:
            left, right = 0, len(self.path[p]) * 2 - 1
        
        def get(now, left, right, pos, f, l_max):
            if left == pos:
                return l_max[now]
            
            mid = (left + right) >> 1
            if pos <= mid:
                res = get(now + now + 1, left, mid, pos, f, l_max)
                if res is None:
                    return l_max[now + now + 2]
                else:
                    return res
            else:
                return get(now + now + 2, mid + 1, right, pos, f, l_max)

        index = get(0, left, right, pos + 1, self.f[p], self.l_max[p])

        #index为空说明后续行进路线上没有被打开的节点，此时光线会原路返回
        if index is None:
            return pos
        #如果是某个复制后的节点被打开，需要将其下标还原成原数组中的下标
        elif index >= len(self.path[p]):
            return index - len(self.path[p])
        else:
            return index

    def open(self, index, direction):
        #尚未打开则打开节点，并更新线段树
        if index not in self.open_index:
            #遍历光路的方向
            for direct in range(2):
                index_with_direct = index + index + direct
                if index_with_direct in self.belong:
                    p, pos = self.belong[index_with_direct]
                    self.insert(p, pos, 1)
                    #单链的两侧是角落节点，但角落节点只有一种表示法，所以需要借助另一侧的角落节点完成两条光路上的更新
                    if p in self.corner_path and pos == 0:
                        p, _ = self.belong[self.path[p][-1]]
                        pos = len(self.path[p]) - 1
                        self.insert(p, pos, 1)

            self.open_index.add(index)

        if direction == 1:
            index += index + 1
        else:
            index += index
        p, pos = self.belong[index]

        return self.path[p][self.query(p, pos)] // 2

    def close(self, index):
        #关闭节点，更新线段数
        for direct in range(2):
            index_with_direct = index + index + direct
            if index_with_direct in self.belong:
                p, pos = self.belong[index_with_direct]
                self.insert(p, pos, -1)
                #单链节点两侧更新
                if p in self.corner_path and pos == 0:
                    p, _ = self.belong[self.path[p][-1]]
                    pos = len(self.path[p]) - 1
                    self.insert(p, pos, -1)
        self.open_index.remove(index)
''',
    setup='''bb = BlackBox(2, 2)
bb.open(1, -1)''',
    call='bb.open(3, 1)',
    expect=1,
    max_steps=75,
    skip=['mid = (left + right)', 'if pos <= mid', 'if f[now + now + 1] > 0', 'elif f[now + now + 2] > 0',
          'if f[now] > 0', 'put(now + now', 'if p in self.corner_path and pos == 0', 'if left == right',
          'else:', 'self.open_index.add', 'index_with_direct in self.belong', 'if direction == 1',
          'for direct in range(2)', 'index_with_direct = index + index + direct', 'self.insert(p, pos, 1)',
          'if p in self.corner_path:', 140, 'p, pos = self.belong[index]', 'return l_max[now]', 'return l_max[now + now + 2]',
          'if index is None'],
    views=[
        dict(type='custom', draw=_draw_box, h=420),
        dict(type='array', var=_pathv, label='当前光路（编码=孔号×2+方向，环复制两遍）', cell=60, h=130,
             color=lambda S, i, v: 'pink' if i == S.get('pos') else None),
        dict(type='array', var=_arr('self.f'), label='线段树 f：区间内打开的孔数（蓝 = now）', cell=56, h=130,
             color=lambda S, i, v: 'blue' if i == S.get('now') else None),
        dict(type='array', var=_arr('self.l_max'), label='线段树 l_max：区间内最靠左的打开位置（-=无）', cell=56, h=130,
             color=lambda S, i, v: 'blue' if i == S.get('now') else None),
    ],
    watch=[('index', 'index', 'yellow'), ('p', 'p', 'blue'), ('pos', 'pos', 'pink'), ('now', 'now'), ('delta', 'delta')],
    captions={
        'if index not in self.open_index': lambda S, B, r: (
            f'`{S.index}` 号孔还没打开过 → 先把它登记进它所在光路的线段树'
            if S.index not in S.get('self.open_index', ()) else f'`{S.index}` 号孔已经打开过，不用重复登记'),
        'p, pos = self.belong[index_with_direct]': '孔有两个方向：编码 `孔号×2+方向` = `{index_with_direct}`，查 `belong` → 第 `{p}` 条光路第 `{pos}` 位，去更新它',
        'index += index': '入射孔 + 方向 `{direction}` 编码成节点 `{index}`，光线从它出发',
        'p, pos = self.belong[index]': '入射节点在第 `{p}` 条光路的第 `{pos}` 个位置，光线从这里出发',
        'self.query(p, pos)': lambda S, B, r: (
            '沿光路往后，==第一个打开的孔==在哪？' if r is None else f'光线最终从 =={r} 号孔== 射出'),
        'left, right = 0, len(self.path[p]) - 1': '单链光路：线段树区间 `[0, {right}]`',
        'left, right = 0, len(self.path[p]) * 2 - 1': '第 `{p}` 条是==环形光路==：复制两遍，区间 `[0, {right}]`，绕回的孔也排在后面',
        'put(0, left, right, pos, delta': '自顶向下更新位置 `{pos}`',
        'pos += len(self.path[p])': '复制的那份也要更新：位置 `{pos}`',
        'f[now] += delta': '区间 `[{left}, {right}]`：`f[{now}]` → `{f[now]}`',
        'l_max[now] = pos': '叶子：记下位置 `l_max[{now}] = {pos}`',
        'l_max[now] = l_max[now + now + 1]': '左半区有孔 → 取左边：`l_max[{now}] = {l_max[now]}`',
        'l_max[now] = l_max[now + now + 2]': '左半区没有 → 取右边：`l_max[{now}] = {l_max[now]}`',
        'index = get(0, left, right, pos + 1': '从==下一个位置== `{B.pos + 1}` 往后找最靠左的打开孔',
        'if left == pos': lambda S, B, r: (
            f'区间 `[{S.left}, {S.right}]` 的左端就是 `{S.pos}` → 这一段的 `l_max[{S.now}] = {S.l_max[S.now]}` 就是答案'
            if S.left == S.pos else f'区间 `[{S.left}, {S.right}]` 左端不是 `{S.pos}` → 继续拆成两半'),
        'res = get(now + now + 1': 'pos 在左半区：先递归问左半区',
        'if res is None': lambda S, B, r: (
            f'左半区没有已打开的孔 → 答案是右半区整体的 `l_max[{S.now + S.now + 2}] = {S.l_max[S.now + S.now + 2]}`'
            if S.res is None else f'左半区找到了 `{S.res}` → 直接返回它'),
        'return get(now + now + 2': 'pos 在右半区：只需要问右半区',
        'return l_max[now + now + 2]': '返回右半区最靠左的已打开位置 `{ret}`',
        'return l_max[now]': '返回这一段最靠左的已打开位置 `{ret}`',
        'return res': '把找到的位置 `{ret}` 往上返回',
        'if index is None': lambda S, B, r: (
            '后面没有打开的孔 → 光线原路返回' if S.index is None
            else f'找到下一个打开的孔，位置 `{S.index}`'),
        'elif index >= len(self.path[p])': lambda S, B, r: (
            f'`{S.index} ≥ 光路长度 {len(S["self.path"][S.p])}` → 它在复制出来的那一份里，要减去光路长度还原'
            if S.index >= len(S['self.path'][S.p]) else f'`{S.index}` 在原光路范围内，直接用'),
        'return index - len(self.path[p])': '还原成原光路的位置：`{ret}`',
        'return index': '位置 `{ret}`',
        'return pos': '原路返回，位置 `{ret}`',
    },
    cards=dict(
        one_liner='把光路拆成单链和环，再用线段树找“光路上最近的打开孔”',
        complexity='预处理 `O(n+m)`，每次 open/close `O(log(n+m))`',
        problem=['`n×m` 的黑盒，四周有 `2(n+m)` 个孔，光线斜着射入、遇壁反射',
                 '`open(index, direction)`：打开 `index` 号孔并从它射入光线，返回==光线从哪个已打开的孔射出==',
                 '`close(index)`：关闭 `index` 号孔',
                 '本视频：`2×2` 的盒子，先 `open(1, -1)`（视频外已执行），再 `open(3, 1)` → `1`'],
        quote='将direction为-1时光路上的节点设置为原始节点编号乘以2，将direction为1时光路上的节点设置为原始节点编号乘以2之后加1。',
        quote_src='—— yiduobo 题解原文',
        idea=['把孔看成图的点、光路看成边：图里只有两条单链（端点是四个角）和若干个环',
              '每条光路按方向拆成两份，节点编码 = `孔号×2 + 方向`，`belong` 哈希表能直接查到“在哪条光路第几位”',
              '问题变成：这条光路上，我之后第一个已打开的孔？线段树维护 `f`（个数）和 `l_max`（最左位置）',
              '环要复制成两遍：绕一圈回来之前也能碰到前面的孔'],
        before=[dict(heading='预处理：本例的光路（构造函数在视频外已运行）',
                     lines=['`2×2` 的盒子有 8 个孔，两条对角线单链 `0↔4`、`2↔6`',
                            '剩下的孔 `1、3、5、7` 组成一个环，顺逆时针各一份',
                            '`path[4] = [2, 7, 10, 15]`，`path[5] = [3, 14, 11, 6]`',
                            '`open_index` 记录哪些孔是开着的，线段树 `f`、`l_max` 一开始全是空'])],
        summary=['预处理 `O(n+m)` 个孔；每次 `open`/`close` 只更新常数条光路的线段树，`O(log(n+m))`',
                 '环形光路复制两遍：打开/关闭时要更新原位置和复制位置，查询结果 `≥` 光路长度要减回来',
                 '单链的角落只有一种编码，所以 `pos == 0` 时还要去另一条光路更新（本例未触发）',
                 '没有后续打开的孔时，光线原路返回：`query` 返回自己的位置',
                 '原文为 Python 2 写法，`now /= 2` 已改为 `now //= 2`，最后的 `/ 2` 已改为 `// 2`；构造函数在视频外运行'],
    ),
)
