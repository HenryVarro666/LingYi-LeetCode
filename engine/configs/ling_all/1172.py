def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cap = S.get('self.capacity', 2)
    st = [list(c) for c in S.get('self.stacks', [])]
    old = [list(c) for c in B.get('self.stacks', [])]
    h = set(S.get('self.h', []))
    cv.text((x0 + 18, y0 + 4), 'stacks（从左到右编号，栈底在下；虚线框 = 容量）', 24, T['muted'], bold=True)
    cv.text((x0 + 18, y0 + 40), '绿 = 刚压入，青色「未满」= 下标在最小堆里', 20, T['cyan'], bold=True)
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
    author='灵茶山艾府', technique='栈列表 + 最小堆（懒删除）',
    tags=['栈', '懒删除堆', '设计', '难度分 2110'],
    code='''
class DinnerPlates:
    def __init__(self, capacity: int):
        self.capacity = capacity  # 栈的容量
        self.stacks = []  # 所有栈
        self.h = []  # 最小堆，保存未满栈的下标

    def push(self, val: int) -> None:
        if self.h and self.h[0] >= len(self.stacks):
            self.h = []  # 堆中都是越界下标，直接清空
        if self.h:  # 还有未满栈
            self.stacks[self.h[0]].append(val)  # 入栈
            if len(self.stacks[self.h[0]]) == self.capacity:  # 栈满了
                heappop(self.h)  # 从堆中去掉
        else:  # 所有栈都是满的
            self.stacks.append([val])  # 添加一个新的栈
            if self.capacity > 1:  # 新的栈没有满
                heappush(self.h, len(self.stacks) - 1)  # 入堆

    def pop(self) -> int:
        # 等价为 popAtStack 最后一个非空栈
        return self.popAtStack(len(self.stacks) - 1)

    def popAtStack(self, index: int) -> int:
        if index < 0 or index >= len(self.stacks) or len(self.stacks[index]) == 0:
            return -1  # 非法操作
        if len(self.stacks[index]) == self.capacity:  # 满栈
            heappush(self.h, index)  # 元素出栈后，栈就不满了，把下标入堆
        val = self.stacks[index].pop()
        while self.stacks and len(self.stacks[-1]) == 0:
            self.stacks.pop()  # 去掉末尾的空栈（懒删除，堆中下标在 push 时处理）
        return val
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
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='heap', var='self.h', label='self.h 最小堆（未满栈的下标）', top_color='cyan', h=120),
        dict(type='text', fn=lambda S: (f"堆顶 `{S['self.h'][0]}` ≥ `len(stacks) = {len(S['self.stacks'])}`：==越界的残留下标==" if S.get('self.h') and S['self.h'][0] >= len(S['self.stacks']) else ''), size=28, h=60),
    ],
    max_steps=84,
    watch=[('val', 'val', 'yellow'), ('index', 'index', 'blue'), ('h', 'self.h', 'cyan'), ('栈数', 'len(self.stacks)', 'green')],
    captions={
        'self.capacity = capacity': '每个栈最多放 `{capacity}` 个盘子',
        'self.stacks = []': '`stacks` 按编号存放所有栈',
        'self.h = []': '`h` 最小堆：==维护所有未满栈的下标==，堆顶就是最左边的未满栈',
        'if self.h and self.h[0] >=': lambda S, B, r: (
            '堆顶下标已经越界（右边的栈被删光了）→ 残留的下标无效，==整堆清空==（懒删除）'
            if S.self.h and S.self.h[0] >= len(S.self.stacks) else
            ('堆里有未满栈，下标合法' if S.self.h else '堆为空：所有栈都是满的')),
        'self.h = []': lambda S, B, r: ('堆里都是越界下标，清空' if S.self.h == [] and B.get('self.h') else '`h` 最小堆：==维护所有未满栈的下标==，堆顶就是最左边的未满栈'),
        'if self.h:': lambda S, B, r: (f'有未满栈：最左的是栈 `{S.self.h[0]}`' if S.self.h else '没有未满栈 → 只能开新栈'),
        'self.stacks[self.h[0]].append(val)': '`{val}` 压入最左未满栈 `{self.h[0]}`',
        'if len(self.stacks[self.h[0]]) == self.capacity': lambda S, B, r: (
            f'栈 `{S.self.h[0]}` 现在 `{len(S.self.stacks[S.self.h[0]])}` 个，容量 `{S.self.capacity}` → ' + ('满了' if len(S.self.stacks[S.self.h[0]]) == S.self.capacity else '还没满')),
        'heappop(self.h)': '栈满了，不再「未满」→ 弹出堆顶 `{B.self.h[0]}`',
        'self.stacks.append([val])': '所有栈都满：右边新开一个栈，放入 `{val}`',
        'if self.capacity > 1': lambda S, B, r: ('容量 > 1，新栈还有空位 → 下标入堆' if S.self.capacity > 1 else '容量为 1，新栈一放就满 → 不入堆'),
        'heappush(self.h, len(self.stacks) - 1)': '新栈下标 `{len(self.stacks) - 1}` 入堆：`h = {self.h}`',
        'return self.popAtStack': 'pop 等价于对==最后一个栈==做 `popAtStack`',
        'if index < 0 or': lambda S, B, r: ('下标越界或栈为空 → 返回 -1' if (S.index < 0 or S.index >= len(S.self.stacks) or len(S.self.stacks[S.index]) == 0) else f'栈 `{S.index}` 合法且非空，可以弹'),
        'if len(self.stacks[index]) == self.capacity': lambda S, B, r: (
            f'栈 `{S.index}` 是满栈 → 弹出后会变成未满，要把下标 `{S.index}` 放进堆' if len(S.self.stacks[S.index]) == S.self.capacity
            else f'栈 `{S.index}` 本来就不满，下标已经在堆里 → 不用管'),
        'heappush(self.h, index)': '下标 `{index}` 入堆：`h = {self.h}`',
        'val = self.stacks[index].pop()': '弹出栈 `{index}` 的栈顶：`{val}`',
        'while self.stacks and': lambda S, B, r: ('末尾栈空了 → 继续删' if S.self.stacks and len(S.self.stacks[-1]) == 0 else '末尾栈非空（或没有栈了）→ 停止'),
        'self.stacks.pop()': '删掉末尾空栈：==堆里的旧下标不管==，等下次 push 发现越界再清',
        'return val': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='与其找第一个未满栈，不如用最小堆维护所有未满栈',
        complexity='每次操作均摊 `O(log q)`，空间 `O(q)`',
        problem=['无限多个栈排成一排，容量都是 `capacity`',
                 '`push`：放进==最左边未满==的栈；`pop`：弹最右非空栈的栈顶；`popAtStack(i)`：弹栈 `i`',
                 '本视频：容量 2，`push 1..5`，再穿插若干弹出 → `[2, 5, 4, 7, 6]`'],
        quote='与其维护第一个未满栈，不如维护所有未满栈。……最小堆，就你了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`stacks` 列表存所有栈，`pop` 就是 `popAtStack(len(stacks) - 1)`',
              '最小堆 `h` 存未满栈的下标：`push` 看堆顶；栈满了就弹出；满栈被弹后下标入堆',
              '末尾栈删掉时不去堆里找下标，==懒删除==：下次 `push` 见堆顶越界就整堆清空'],
        summary=['时间：均摊 `O(log q)`，空间 `O(q)`',
                 '易错：`popAtStack` 只有从满栈弹时才入堆，否则下标会重复',
                 '易错：删掉末尾空栈要用 `while`，中间的空栈保留位置不动',
                 '易错：`capacity == 1` 时新栈一放就满，不能入堆',
                 '思考题：`pushAtStack(index, val)` 作者留给读者'],
    ),
)
