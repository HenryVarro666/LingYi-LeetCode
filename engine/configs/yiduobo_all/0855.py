
def _occ(S):
    h = S.get('self.heap') or []
    N = S.get('self.N')
    occ = set()
    for l, r in h:
        if l >= 0:
            occ.add(l)
        if r < N:
            occ.add(r)
    return occ


def _dis(l, r, N):
    return r if l == -1 else (N - 1 - l if r == N else (r - l) // 2)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    N = S.get('self.N')
    cv.text((x0 + 18, y0 + 4), '考场座位（绿 = 有人，黄 = 正在拆分的区间，蓝 = 空）', 24, T['muted'], bold=True)
    if N is None:
        return
    occ = _occ(S)
    cell = min(64, (x1 - x0 - 40) / N)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * N) / 2
    y = y0 + 64
    L, R = S.get('left'), S.get('right')
    cur = None
    if '_line' in S and isinstance(L, int) and isinstance(R, int) and S.get('_inner', {}).get('left') is not None:
        cur = (L, R)
    for i in range(N):
        X = sx + i * cell
        inside = cur is not None and cur[0] < i < cur[1]
        fill = T['green'] if i in occ else (T['yellow'] if inside else T['panel2'])
        cv.rect((X + 3, y, X + cell - 3, y + cell - 6), fill=fill, r=8, outline=T['border'], width=1)
        cv.text((X + cell / 2, y + (cell - 6) / 2), '人' if i in occ else '', 28, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y + cell + 4), i, 20, T['dim'], anchor='mt', mono=True)
    # 区间：画在座位下面，每个 [l, r] 一条横线 + 它能提供的间隔
    h = S.get('self.heap') or []
    yy = y + cell + 56
    for k, (l, r) in enumerate(sorted(h, key=lambda p: p[0])):
        a = sx + (max(l, -0.5) + 0.5) * cell
        b = sx + (min(r, N - 0.5) + 0.5) * cell
        cv.line([(a, yy), (b, yy)], T['cyan'], 4)
        cv.text(((a + b) / 2, yy - 6), f'[{l},{r}] 间隔{_dis(l, r, N)}', 16, T['cyan'], anchor='mb')
        yy += 26


def _fmt(x):
    return f'[{x[0]},{x[1]}]'


def _node(S, i):
    return S['self.heap'][i]


CONFIG = dict(
    num=855, title='考场就座', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='堆维护空闲区间 + head/tail 字典定位',
    tags=['堆'],
    code='''
class ExamRoom(object):

    def __init__(self, N):
        self.heap = []
        self.N = N
        self.head_dict = {}
        self.tail_dict = {}

    def compare(self, x, y):
        l1, r1 = self.heap[x]
        l2, r2 = self.heap[y]
        if l1 == -1:
            dis1 = r1
        elif r1 == self.N:
            dis1 = self.N - 1 - l1
        else:
            dis1 = (r1 - l1) // 2
        
        if l2 == -1:
            dis2 = r2
        elif r2 == self.N:
            dis2 = self.N - 1 - l2
        else:
            dis2 = (r2 - l2) // 2
        
        if dis1 > dis2 or (dis1 == dis2 and l1 < l2):
            return True

        return False

    def swap(self, x, y):
        l1, r1 = self.heap[x]
        l2, r2 = self.heap[y]

        self.heap[x] = [l2, r2]
        self.heap[y] = [l1, r1]

        self.head_dict[l1] = y
        self.tail_dict[r1] = y
        self.head_dict[l2] = x
        self.tail_dict[r2] = x

    def push(self, left, right):
        self.heap.append([left, right])
        now = len(self.heap) - 1
        self.head_dict[left] = now
        self.tail_dict[right] = now
        while now != 0:
            if self.compare(now, (now - 1) // 2):
                self.swap(now, (now - 1) // 2)
                now = (now - 1) // 2
            else:
                break

    def pop(self, now):
        l, r = self.heap[now]
        self.swap(now, -1)
        self.heap.pop()
        self.head_dict.pop(l)
        self.tail_dict.pop(r)
        while now < len(self.heap):
            flag_l = flag_r = False
            if now + now + 1 < len(self.heap) and self.compare(now + now + 1, now):
                flag_l = True
            if now + now + 2 < len(self.heap) and self.compare(now + now + 2, now):
                flag_r = True
            if flag_l:
                if flag_r:
                    if self.compare(now + now + 1, now + now + 2):
                        self.swap(now, now + now + 1)
                        now = now + now + 1
                    else:
                        self.swap(now, now + now + 2)
                        now = now + now + 2
                else:
                    self.swap(now, now + now + 1)
                    now = now + now + 1
            elif flag_r:
                self.swap(now, now + now + 2)
                now = now + now + 2
            else:
                break

        return l, r

    def seat(self):
        if not self.heap:
            self.push(0, self.N)
            self.push(-1, 0)
            return 0
        
        left, right = self.pop(0)
        if left == -1:
            self.push(0, right)
            self.push(-1, 0)
            return 0
        elif right == self.N:
            self.push(left, self.N - 1)
            self.push(self.N - 1, self.N)
            return self.N - 1
        else:
            mid = (left + right) // 2
            self.push(left, mid)
            self.push(mid, right)
            return mid

    def leave(self, p):
        _, right = self.pop(self.head_dict[p])
        left, _ = self.pop(self.tail_dict[p])
        self.push(left, right)

''',
    call="""room = ExamRoom(10)
res = [room.seat(), room.seat(), room.seat()]
room.leave(4)
res""",
    expect=[0, 9, 4],
    skip=['l1, r1 = self.heap', 'l2, r2 = self.heap', 'dis1 = ', 'dis2 = ', 'if l1 == -1', 'elif r1 == self.N',
          'if l2 == -1', 'elif r2 == self.N', 'self.heap[x] = ', 'self.heap[y] = ', 'self.head_dict[l1]', 'self.tail_dict[r1]',
          'self.head_dict[l2]', 'self.tail_dict[r2]', 'self.heap = []', 'self.N = N', 'self.head_dict = {}', 'self.tail_dict = {}',
          'flag_l = flag_r = False', 'now = len(self.heap) - 1', 'self.head_dict[left] = now', 'self.tail_dict[right] = now',
          'self.swap(now, -1)', 'self.heap.pop()', 'self.head_dict.pop(l)', 'self.tail_dict.pop(r)', 'while now < len', 'if now + now + 1 <',
          'if now + now + 2 <', 'if flag_l', 'if flag_r', 'elif flag_r', 'break', 'return True', 'return False', 'while now != 0', 'if self.compare(now, (now - 1) // 2)', 'if self.compare(now + now + 1, now)'],
    max_steps=130,
    views=[
        dict(type='custom', draw=_draw, h=265),
        dict(type='heap', var='self.heap', label='self.heap 空闲区间', fmt=_fmt, top_color='yellow', h=150),
        dict(type='map', var='self.head_dict', label='head_dict（左端点 → 堆下标）', font=20, h=108),
        dict(type='map', var='self.tail_dict', label='tail_dict（右端点 → 堆下标）', font=20, h=108),
        dict(type='calls', label='正在执行', h=80),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('now', 'now', 'cyan'), ('p', 'p', 'orange')],
    captions={
        'dis1 > dis2 or': lambda S, B, ret: '比较两个区间的间隔 `{}` vs `{}`：大的更优先，相等取==左端点小==的'.format(S.dis1, S.dis2),
        'return True': '`x` 比 `y` 更优先 → 返回 True',
        'return False': '`x` 不比 `y` 优先 → 返回 False',
        'self.heap.append([left, right])': '新区间 `[{left}, {right}]` 放到堆末尾，登记 head_dict / tail_dict，再和父节点比较、向上调整',
        'now = len(self.heap) - 1': '新区间在堆中的下标 `now = {now}`',
        'self.head_dict[left] = now': '记住：以 `{left}` 为左端点的区间在堆里的位置 = `{now}`',
        'self.tail_dict[right] = now': '记住：以 `{right}` 为右端点的区间在堆里的位置 = `{now}`',
        'while now != 0': lambda S, B, ret: '还没到堆顶，继续比较父节点' if S.now != 0 else '已经到堆顶',
        'if self.compare(now, (now - 1) // 2)': lambda S, B, ret: '和父节点 `{}` 比：比它优先吗？'.format((S.now - 1) // 2),
        'self.swap(now, (now - 1) // 2)': '比父节点更优先 → 交换上移（swap 同时更新两个字典）',
        'now = (now - 1) // 2': '`now` 上移到 `{now}`',
        'l, r = self.heap[now]': '要删下标 `{now}` 的区间 `[{l}, {r}]`：先和堆尾交换再弹出，并从两个字典里删掉它，然后向下调整堆',
        'self.swap(now, -1)': '和堆尾交换，这样可以 `pop()` 掉末尾',
        'self.heap.pop()': '弹出堆尾（就是要删的区间）',
        'self.head_dict.pop(l)': '从 head_dict 删掉 `{l}`',
        'self.tail_dict.pop(r)': '从 tail_dict 删掉 `{r}`',
        'while now < len(self.heap)': '从 `now = {now}` 向下调整：换上来的堆尾可能不够优先',
        'if now + now + 1 < len(self.heap)': '左孩子比 `now` 更优先吗？`flag_l = {flag_l}`',
        'if now + now + 2 < len(self.heap)': '右孩子比 `now` 更优先吗？`flag_r = {flag_r}`',
        'return l, r': '返回被删区间 `[{l}, {r}]`',
        'if not self.heap': lambda S, B, ret: '考场空 → 第一个人坐 0 号' if not S['self.heap'] else '考场有人：取堆顶区间来拆',
        'self.push(0, self.N)': '区间 `[0, N]`：右边还有空位，之后坐 N−1',
        'self.push(-1, 0)': '区间 `[-1, 0]`：0 号坐了人，左边没有空位',
        'left, right = self.pop(0)': '弹出堆顶 = 能提供最大间隔的区间 `[{left}, {right}]`',
        'if left == -1': lambda S, B, ret: '左端是墙 `-1` → 坐 ==0 号==，间隔 = `right`' if S.left == -1 else '左端不是墙，再看右端',
        'elif right == self.N': lambda S, B, ret: '右端是墙 `N` → 坐 ==N−1 号==，间隔 = `N-1-left`' if S.right == S['self.N'] else '两端都是人 → 坐正中间',
        'self.push(0, right)': '拆成 `[0, {right}]`，再补上 `[-1, 0]`',
        'self.push(left, self.N - 1)': '拆成 `[{left}, N-1]`，再补上 `[N-1, N]`',
        'mid = (left + right) // 2': '坐正中间：`mid = ({left} + {right}) // 2` = =={mid}==',
        'self.push(left, mid)': '拆成两段：`[{B.left}, {mid}]` 和 `[{mid}, {B.right}]`',
        'self.push(mid, right)': '右半段 `[{mid}, {B.right}]`',
        'return mid': '这位同学坐 `{mid}` 号',
        'return 0': '坐 0 号',
        'return self.N - 1': '坐最后一个座位 `N-1`',
        'def leave': '',
        '_, right = self.pop(self.head_dict[p])': '座位 `{p}` 是某区间的左端：用 `head_dict[{p}]` 找到它并弹出，得到 `right = {right}`',
        'left, _ = self.pop(self.tail_dict[p])': '它同时是另一个区间的右端：用 `tail_dict[{p}]` 弹出，得到 `left = {left}`',
        'self.push(left, right)': '两段合并回 `[{left}, {right}]`（空位连成一片）',
    },
    cards=dict(
        one_liner='把空座位看成区间放进堆，坐人 = 拆区间，离开 = 合并区间',
        complexity='`seat` / `leave` 均 `O(log n)`',
        problem=['`ExamRoom(N)`：`N` 个座位，`seat()` 让新学生坐到离最近的人最远的位置（并列取编号最小）',
                 '`leave(p)`：`p` 号座位的学生离开',
                 '示例 `N = 10`：连续 `seat` 得 0、9、4，再 `leave(4)`'],
        quote='当前能提供最大间隔的区间[l ,r]就将被划分为[l, p]以及[p, r]两段……每离开一个学生，那么以离开的位置p为首尾的两端区间[l, p]以及[p, r]则会被重新合并为区间[l, r]。',
        quote_src='—— yiduobo 题解原文',
        idea=['区间 `[l, r]` 能提供的间隔：左墙 `-1` 看 `r`，右墙 `N` 看 `N-1-l`，否则 `(r-l)//2`',
              '堆按「间隔大、左端点小」排序，堆顶就是下一个座位所在的区间',
              'Python 的 heapq 不能删中间元素，所以手写堆，并用 `head_dict` / `tail_dict` 记住区间位置，离开时 `O(log n)` 找到并删除'],
        summary=['`seat` / `leave` 都是 `O(log n)`，空间 `O(n)`',
                 '易错：两端是墙时间隔的算法不同；并列时要选左端点小的',
                 '手写堆的 `swap` 必须同时更新 `head_dict` 与 `tail_dict`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（间隔、父节点下标、中点）'],
    ),
)
