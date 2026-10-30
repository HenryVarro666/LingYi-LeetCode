def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cap = S.get('self.capacity', 2)
    st = [list(c) for c in S.get('self.stacks', [])]
    old = [list(c) for c in B.get('self.stacks', [])]
    h = set(S.get('self.heap', []))
    cv.text((x0 + 18, y0 + 4), 'stacks（从左到右编号，栈底在下；虚线框 = 容量）', 24, T['muted'], bold=True)
    cv.text((x0 + 18, y0 + 40), '绿 = 刚压入，青色「未满」= 下标在 heap 里', 20, T['cyan'], bold=True)
    if not st:
        cv.text((x0 + 18, y0 + 100), '（stacks 是空的，一个栈都没有）', 24, T['dim'])
        return
    n = len(st)
    cw = min(130, (x1 - x0 - 60) / max(n, 4))
    ch = 52
    base = y1 - 70
    sx = x0 + 30
    for k, col in enumerate(st):
        X = sx + k * cw
        cv.rect((X + 4, base - cap * ch, X + cw - 4, base), outline=T['border'], width=2, r=8)
        for j, v in enumerate(col):
            fresh = j == len(col) - 1 and (k >= len(old) or len(col) > len(old[k]))
            cv.rect((X + 8, base - (j + 1) * ch + 4, X + cw - 8, base - j * ch - 2), fill=T['green'] if fresh else (62, 70, 84), r=8)
            cv.text((X + cw / 2, base - j * ch - ch / 2 + 1), v, 28, T['bg'] if fresh else T['text'], anchor='mm', bold=True)
        cv.text((X + cw / 2, base + 8), f'栈 {k}', 22, T['text'], anchor='mt', bold=True)
        if k in h:
            cv.text((X + cw / 2, base + 36), '未满', 20, T['cyan'], anchor='mt', bold=True)
        elif len(col) == cap:
            cv.text((X + cw / 2, base + 36), '满', 20, T['dim'], anchor='mt')


CONFIG = dict(
    num=1172, title='餐盘栈', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='栈列表 + 非满栈下标堆',
    tags=['栈', '堆', '设计', '难度分 2110'],
    code='''
class DinnerPlates(object):

    def __init__(self, capacity):
        self.stacks = []
        self.heap = []
        self.capacity = capacity

    def push(self, val):

        if not self.heap:
            self.stacks.append([])
            self.stacks[-1].append(val)
            p = len(self.stacks) - 1
        else:
            p = heapq.heappop(self.heap)
            if len(self.stacks) - 1 < p:
                self.stacks.append([])
            self.stacks[p].append(val)

        if len(self.stacks[p]) < self.capacity:
            heapq.heappush(self.heap, p)

    def pop(self):

        while self.stacks and len(self.stacks[-1]) == 0:
            self.stacks.pop()
        
        if not self.stacks:
            return -1
        
        p = len(self.stacks) - 1
        if len(self.stacks[p]) == self.capacity:
            heapq.heappush(self.heap, p)

        return self.stacks[p].pop()

    def popAtStack(self, index):

        if len(self.stacks) - 1 < index:
            return -1
        
        if not self.stacks[index]:
            return -1
        
        if len(self.stacks[index]) == self.capacity:
            heapq.heappush(self.heap, index)
        
        return self.stacks[index].pop()
''',
    call='''D = DinnerPlates(2)
r = []
for v in [1, 2, 3, 4, 5]:
    D.push(v)
r.append(D.popAtStack(0))
D.push(20)
r.append(D.popAtStack(2))
r.append(D.pop())
D.push(6)
D.push(7)
r.append(D.pop())
r.append(D.pop())
r''',
    expect=[2, 5, 4, 7, 6],
    max_steps=90,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='heap', var='self.heap', label='self.heap 最小堆（未满栈的下标）', top_color='cyan', h=120),
        dict(type='text', fn=lambda S: (f"堆顶 `{S['self.heap'][0]}` > 最后一个栈下标 `{len(S['self.stacks']) - 1}`：==这个栈已被 pop 删掉，要重新建=="
                                        if S.get('self.heap') and S['self.heap'][0] > len(S['self.stacks']) - 1 else ''), size=28, h=60),
    ],
    watch=[('val', 'val', 'yellow'), ('p', 'p', 'blue'), ('index', 'index', 'blue'), ('heap', 'self.heap', 'cyan'), ('栈数', 'len(self.stacks)', 'green')],
    captions={
        'self.stacks = []': '`stacks` 按编号存放所有栈',
        'self.heap = []': '`heap` 最小堆：==存所有未满栈的下标==，堆顶是最左的未满栈',
        'self.capacity = capacity': '每个栈最多 `{capacity}` 个',
        'if not self.heap': lambda S, B, r: ('堆为空：没有未满栈' if not S.self.heap else f'堆顶是 `{S.self.heap[0]}`，有未满栈'),
        'self.stacks.append([])': '末尾新开一个空栈',
        'self.stacks[-1].append(val)': '`{val}` 放进新栈',
        'p = len(self.stacks) - 1': '`p = {p}`：最后一个栈的下标',
        'p = heapq.heappop(self.heap)': '取出堆顶 `p = {p}`：==最左的未满栈==（先取出来，装完再决定要不要放回）',
        'if len(self.stacks) - 1 < p': lambda S, B, r: (f'`p = {S.p}` 超过了最后一个栈的下标 `{len(S.self.stacks) - 1}`：这个栈已被删掉 → 重新建一个' if len(S.self.stacks) - 1 < S.p else f'栈 `{S.p}` 还在 → 直接用'),
        'self.stacks[p].append(val)': '`{val}` 压入栈 `{p}`：`{self.stacks[p]}`',
        'if len(self.stacks[p]) < self.capacity': lambda S, B, r: (
            f'栈 `{S.p}` 有 `{len(S.self.stacks[S.p])}` 个 < 容量 `{S.self.capacity}` → 仍未满，下标放回堆' if len(S.self.stacks[S.p]) < S.self.capacity
            else f'栈 `{S.p}` 满了 → 不放回堆'),
        'heapq.heappush(self.heap, p)': '下标 `{p}` 放回堆：`heap = {self.heap}`',
        'while self.stacks and': lambda S, B, r: ('末尾栈是空的 → 删掉，继续看前一个' if S.self.stacks and len(S.self.stacks[-1]) == 0 else '末尾栈非空（或没有栈）→ 停止'),
        'self.stacks.pop()': '删掉末尾空栈',
        'if not self.stacks': lambda S, B, r: ('所有栈都空了 → 返回 -1' if not S.self.stacks else '还有非空栈'),
        'p = len(self.stacks) - 1': '`p = {p}`：最后一个栈的下标',
        'if len(self.stacks[p]) == self.capacity': lambda S, B, r: (
            f'栈 `{S.p}` 是满栈 → 弹出后变未满，下标 `{S.p}` 要入堆' if len(S.self.stacks[S.p]) == S.self.capacity else f'栈 `{S.p}` 本来就不满，下标已在堆里'),
        'return self.stacks[p].pop()': '弹出栈 `{p}` 的栈顶，返回 `{ret}`',
        'if len(self.stacks) - 1 < index': lambda S, B, r: ('`index` 超过栈数 → 返回 -1' if len(S.self.stacks) - 1 < S.index else f'栈 `{S.index}` 存在'),
        'if not self.stacks[index]': lambda S, B, r: ('栈 `' + str(S.index) + '` 是空的 → 返回 -1' if not S.self.stacks[S.index] else '栈非空，可以弹'),
        'if len(self.stacks[index]) == self.capacity': lambda S, B, r: (
            f'栈 `{S.index}` 是满栈 → 弹出后变未满，下标要入堆' if len(S.self.stacks[S.index]) == S.self.capacity else f'栈 `{S.index}` 本来就不满，下标已在堆里'),
        'heapq.heappush(self.heap, index)': '下标 `{index}` 入堆：`heap = {self.heap}`',
        'return self.stacks[index].pop()': '弹出栈 `{index}` 的栈顶，返回 `{ret}`',
        'return -1': '非法操作，返回 `-1`',
    },
    cards=dict(
        one_liner='用堆记住所有未满栈的下标，堆顶就是 push 的目标',
        complexity='每次操作 `O(log q)`，空间 `O(q)`',
        problem=['一排栈，容量都是 `capacity`',
                 '`push` 进最左未满栈；`pop` 弹最右非空栈；`popAtStack(i)` 弹栈 `i`',
                 '本视频：容量 2，`push 1..5` 再穿插弹出 → `[2, 5, 4, 7, 6]`'],
        quote='push操作要求我们在任意时刻都可以很快得知当前编号最小的非满栈的下标，那么一个自然的想法就是使用一个堆来维护所有非满栈的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pop`、`popAtStack` 都容易：list 末尾检查、按下标弹',
              '`push` 取堆顶 `p` 放进去，装完还没满就把 `p` 放回堆',
              '`pop` 从满栈弹出、`popAtStack` 从满栈弹出后，栈变未满 → 下标入堆'],
        summary=['时间：`O(log q)`/次，空间 `O(q)`',
                 '易错：只有「满 → 未满」那一刻才把下标入堆，否则堆里会重复',
                 '易错：`pop` 会删掉末尾空栈，堆里可能残留越界下标，`push` 里用 `len(stacks) - 1 < p` 兜底重建',
                 '原文已是 Python 3 可运行，未做修改（`heapq` 已由引擎注入）',
                 '对比灵神：灵神堆中残留越界下标时整堆清空；yiduobo 每次取出堆顶再判断'],
    ),
)
