RECTS = [[0, 0, 2, 2], [1, 1, 3, 2]]
W, H = 3, 2


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '扫描线从左往右：蓝框 = 矩形，绿 = 已统计的面积，黄线 = 当前 x', 22, T['muted'], bold=True)
    cell = min((x1 - x0 - 160) / W, (y1 - y0 - 110) / H, 120)
    ox, oy = x0 + 70, y1 - 50
    P = lambda x, y: (ox + x * cell, oy - y * cell)
    for k in range(W + 1):
        cv.line([P(k, 0), P(k, H)], T['border'], 1)
        cv.text((P(k, 0)[0], oy + 8), k, 18, T['dim'], anchor='mt')
    for k in range(H + 1):
        cv.line([P(0, k), P(W, k)], T['border'], 1)
        cv.text((ox - 10, P(0, k)[1]), k, 18, T['dim'], anchor='rm')
    lx = S.get('last_x')
    if lx is not None:
        for i in range(W):
            if i < lx:
                for j in range(H):
                    if any(r[0] <= i < r[2] and r[1] <= j < r[3] for r in RECTS):
                        a, b = P(i, j + 1), P(i + 1, j)
                        cv.rect((a[0] + 1, a[1] + 1, b[0] - 1, b[1] - 1), fill=T['green'], alpha=140)
    for r in RECTS:
        a, b = P(r[2], r[3]), P(r[0], r[1])
        cv.rect((a[0] if a[0] < b[0] else b[0], P(r[0], r[3])[1], max(a[0], b[0]), P(r[0], r[1])[1]), outline=T['blue'], width=4)
    if 'x' in S and 'y1' in S:
        c = T['red'] if S['delta'] < 0 else T['orange']
        cv.line([P(S['x'], 0), P(S['x'], H)], T['yellow'], 4)
        cv.text((P(S['x'], H)[0], P(0, H)[1] - 10), f"x={S['x']}", 22, T['yellow'], anchor='mb', bold=True)
        rm = S.get('re_mapping_dict') or {}
        a, b = rm.get(S['y1']), rm.get(S['y2'])
        if a is not None and b is not None:
            cv.line([P(S['x'], a), P(S['x'], b)], c, 9)


def _nodes(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '线段树 f[node]：覆盖次数（node 管的 y 下标区间）', 22, T['muted'], bold=True)
    f, cnt = S.get('f'), S.get('cnt')
    if f is None or cnt is None:
        return
    y = y0 + 44

    def walk(now, l, r, d):
        nonlocal y
        if l > r or now > 6:
            return
        cv.text((x0 + 24 + d * 36, y), f'f[{now}]  管 [{l},{r}]  = {f[now]}', 22, T['yellow'] if f[now] > 0 else T['text'], mono=True)
        y += 32
        if l < r:
            m = (l + r) // 2
            walk(now * 2 + 1, l, m, d + 1)
            walk(now * 2 + 2, m + 1, r, d + 1)
    walk(0, 0, cnt - 1, 0)


CONFIG = dict(
    num=850, title='矩形面积 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按 x 扫描 + y 离散化 + 线段树',
    tags=['常用数据结构', '难度分 2236'],
    code='''
class Solution(object):
    def rectangleArea(self, rectangles):

        line_list = []
        height_list = []
        mapping_dict = {}
        re_mapping_dict = {}
        for x1, y1, x2, y2 in rectangles:
            height_list.append(y1)
            height_list.append(y2)

        cnt = 0
        now = None
        for index, height in enumerate(sorted(height_list)):
            if height != now:
                mapping_dict[height] = cnt
                re_mapping_dict[cnt] = height
                cnt += 1
                now = height
        
        for x1, y1, x2, y2 in rectangles:
            line_list.append([x1, mapping_dict[y1], mapping_dict[y2], 1])
            line_list.append([x2, mapping_dict[y1], mapping_dict[y2], -1])
        
        mod = 10 ** 9 + 7
        line_list = sorted(line_list, key=lambda d:d[0])
        last_x = line_list[0][0]
        f = [0] * 1024
        res = 0
        self.put(0, 0, cnt - 1, line_list[0][1], line_list[0][2] - 1, line_list[0][3], f)
        for x, y1, y2, delta in line_list[1:]:
            if x != last_x:
                res = (res + (x - last_x) * self.get(0, 0, cnt - 1, f, re_mapping_dict)) % mod
                last_x = x
            self.put(0, 0, cnt - 1, y1, y2 - 1, delta, f)

        return res

    def put(self, now, left, right, i, j, delta, f):
        if i > j:
            return
        if left == i and right == j:
            f[now] += delta
        else:
            mid = (left + right) // 2
            if j <= mid:
                self.put(now + now + 1, left, mid, i, j, delta, f)
            elif i > mid:
                self.put(now + now + 2, mid + 1, right, i, j, delta, f)
            else:
                self.put(now + now + 1, left, mid, i, mid, delta, f)
                self.put(now + now + 2, mid + 1, right, mid + 1, j, delta, f)
        
    def get(self, now, left, right, f, re_mapping_dict):
        if left > right:
            return 0
        if f[now] > 0:
            return re_mapping_dict[right + 1] - re_mapping_dict[left]
        elif left == right:
            return 0
        else:
            mid = (left + right) // 2
            return self.get(now + now + 1, left, mid, f, re_mapping_dict) + self.get(now + now + 2, mid + 1, right, f, re_mapping_dict)
''',
    call='Solution().rectangleArea([[0,0,2,2],[1,1,3,2]])',
    expect=5,
    skip=['last_x = x', 'elif left == right', 'if x != last_x', 'last_x = line_list[0][0]', 'line_list = []', 'height_list = []', 'mapping_dict = {}', 're_mapping_dict = {}', 'for x1, y1, x2, y2 in rectangles',
          'res = 0', 'f = [0] * 1024', 'if left > right', 'if i > j', 'mid = (left + right)', 'height_list.append', 'mapping_dict[height] = cnt', 're_mapping_dict[cnt] = height', 'now = height', 'now = None',
          'mod = ', 'for index, height', 'if height != now', 'cnt += 1', 'cnt = 0', 'line_list.append'],
    max_steps=110,
    views=[
        dict(type='text', fn=lambda S: ('y 离散化：`' + str(S['mapping_dict']) + '`（y 值 → 排名）') if S.get('mapping_dict') else '', size=24, h=50),
        dict(type='custom', draw=_draw, h=270),
        dict(type='custom', draw=_nodes, h=260),
    ],
    watch=[('x', 'x', 'yellow'), ('last_x', 'last_x', 'cyan'), ('delta', 'delta', 'orange'), ('res', 'res', 'green')],
    captions={
        'line_list = sorted': 'y 先==离散化==成排名 `{mapping_dict}`（最多 400 个）；每个矩形拆成左边 `+1`、右边 `-1` 两个事件，按 x 排序：`{line_list}`',
        'last_x = line_list[0][0]': '`last_x` 记录上一个事件的 x，两个 x 之间是一条竖带：起点 `{last_x}`',
        'self.put(0, 0, cnt - 1, line_list[0][1]': '先处理第一个事件：把 y 区间 `[{line_list[0][1]}, {line_list[0][2]-1}]` 的覆盖次数 `+{line_list[0][3]}`（叶子 `i` 表示排名 `i` 到 `i+1` 之间那一段，所以右端是 `y2-1`）',
        'for x, y1, y2, delta in line_list[1:]': lambda S, B, r: ('事件都处理完了：最后一条竖带已经结算' if B.get('x') == S.x and B.get('y1') == S.y1 and B.get('delta') == S.delta else None) or (f'取下一个事件：`x = {S.x}`，y 排名区间 `[{S.y1}, {S.y2})`，`delta = {S.delta}`。' + (f'`x` 和上一个 x 相同，竖带宽 0' if S.x == S.last_x else f'它和 `last_x = {S.last_x}` 之间是一条宽 `{S.x - S.last_x}` 的竖带，==先结算竖带，再处理事件==')),
        'res = (res +': lambda S, B, r: f'竖带面积 = 宽 `{B.x - B.last_x}` × 这时被覆盖的 y 总长，调用 `get` 来算',
        'self.put(0, 0, cnt - 1, y1, y2 - 1, delta, f)': '竖带结算完：`res = {res}`，`last_x` 前进到 `{last_x}`。再把事件的 y 区间 `[{y1}, {y2 - 1}]` 覆盖次数 ==加 `{delta}`==（左边 +1，右边 −1）',
        'left == i and right == j': lambda S, B, r: (f'节点 `[{B.left}, {B.right}]` 刚好等于要改的区间 → ==直接记在这个节点上==，不往下拆' if (B.left == B.i and B.right == B.j) else f'节点 `[{B.left}, {B.right}]` 比要改的区间 `[{B.i}, {B.j}]` 大 → 继续往下拆'),
        'f[now] += delta': '`f[{now}]` += `{delta}` → =={f[now]}==（这个节点整段的覆盖次数）',
        'if j <= mid': lambda S, B, r: (f'`j = {B.j} ≤ mid = {B.mid}`：区间全在==左半边==' if B.j <= B.mid else f'`j = {B.j} > mid = {B.mid}`：不只在左半边'),
        'elif i > mid': lambda S, B, r: (f'`i = {B.i} > mid = {B.mid}`：区间全在==右半边==' if B.i > B.mid else f'`i = {B.i} ≤ mid = {B.mid}`：区间==跨过了中点=='),
        47: '递归左孩子 `f[{B.now + B.now + 1}]`',
        49: '递归右孩子 `f[{B.now + B.now + 2}]`',
        51: '跨中点：左半边那一段 `[{B.i}, {B.mid}]` 给左孩子',
        52: '右半边那一段 `[{B.mid + 1}, {B.j}]` 给右孩子',
        'if f[now] > 0': lambda S, B, r: (f'`f[{B.now}] = {B.f[B.now]} > 0`：节点 `[{B.left}, {B.right}]` ==整段都被覆盖==' if B.f[B.now] > 0 else f'`f[{B.now}] = 0`：这个节点本身没被整段覆盖'),
        'return re_mapping_dict[right + 1]': '覆盖长度取真实坐标：`y[{right + 1}] − y[{left}]` = `{re_mapping_dict[right + 1]} − {re_mapping_dict[left]}` = =={ret}==',
        'elif left == right': lambda S, B, r: ('叶子且没被覆盖 → 长度 `0`' if B.left == B.right else '不是叶子，累加两个孩子'),
        'return 0': '叶子且没被覆盖：没有矩形盖住这一段 → `0`',
        'return self.get(now + now + 1': '节点 `[{B.left}, {B.right}]` 没被整段覆盖：覆盖长度 = 左孩子 + 右孩子',
        'return res': '所有竖带结算完，面积 `{ret}`（再取模）',
    },
    cards=dict(
        one_liner='按 x 扫描，每条竖带的面积 = 宽度 × 这时被覆盖的 y 总长',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给出若干轴对齐矩形，求覆盖的==总面积==（重叠只算一次），对 `10^9+7` 取模',
                 '示例：`[[0,0,2,2],[1,0,2,3],[1,0,3,1]]` → `6`',
                 '本视频用 `[[0,0,2,2],[1,1,3,2]]` → `5`'],
        quote='可以按照x轴进行分段……每一段的面积则取决于所有矩形在当前x轴区间上生效的纵坐标区间之和。……面积的计算实际上是某种动态区间合并的问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['x 方向的分段就是排序后相邻的事件；每段面积 = `delta_x × 覆盖的 y 长度`',
              '矩形左边加入 y 区间，右边去掉；y 先离散化成 `0 ~ 399`',
              '线段树 `f` 记录每个节点整段被覆盖的次数；`get` 遇到 `f > 0` 的节点直接返回整段长度'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`put` 的区间是 `[y1, y2-1]`：叶子 `i` 管 `y[i]` 到 `y[i+1]` 这一段',
                 '不需要下推：加、减在同一个节点上成对出现，`f[now] > 0` 就表示整段有盖',
                 '原文为 Python 2 写法，`put`/`get` 里的 `mid = (left + right) / 2` 已改为 `//`',
                 '对比灵神：灵神按 y 扫描，用 Lazy 线段树维护最小覆盖次数；这里按 x 扫描，用「不下传」的覆盖计数'],
    ),
)
