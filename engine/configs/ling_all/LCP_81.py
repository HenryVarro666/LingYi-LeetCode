def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    t = S.get('t')
    cv.text((x0 + 18, y0 + 4), '线段树：每个结点 [l,r] 记录比特 0 / 1 穿过这段区间后变成什么（二进制，k 位）', 22, T['muted'], bold=True)
    if t is None or not hasattr(t, 't'):
        return
    kk = S.get('k', 3)
    nodes = [o for o in range(1, len(t.t)) if t.t[o].r > 0]
    if not nodes:
        return
    maxd = max(o.bit_length() - 1 for o in nodes)
    W = x1 - x0 - 40
    bw = min(260, W / (2 ** maxd) - 10)
    bh = 92
    gap = (y1 - y0 - 60 - bh * (maxd + 1)) / max(1, maxd)
    cur = S.get('o')
    pos = {}
    for o in nodes:
        d = o.bit_length() - 1
        px = x0 + 20 + (o - (1 << d) + 0.5) / (1 << d) * W
        py = y0 + 40 + d * (bh + min(gap, 70))
        pos[o] = (px, py)
    for o in nodes:
        if o >> 1 in pos:
            (px, py), (qx, qy) = pos[o], pos[o >> 1]
            cv.line([(qx, qy + bh), (px, py)], T['border'], 2)
    for o in nodes:
        px, py = pos[o]
        nd = t.t[o]
        hot = (o == cur)
        cv.rect((px - bw / 2, py, px + bw / 2, py + bh), fill=T['panel2'], r=10,
                outline=T['yellow'] if hot else T['border'], width=4 if hot else 1)
        cv.text((px, py + 8), f'[{nd.l},{nd.r}]', 22, T['yellow'] if hot else T['muted'], anchor='mt', bold=True)
        cv.text((px, py + 38), f"0 → {nd.to[0]:0{kk}b}", 22, T['cyan'], anchor='mt', mono=True)
        cv.text((px, py + 64), f"1 → {nd.to[1]:0{kk}b}", 22, T['pink'], anchor='mt', mono=True)


CONFIG = dict(
    num='LCP 81', title='与非的谜题', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='拆位 + 线段树维护「穿过」结果（Go 原文转写）',
    tags=['灵神题单', '线段树'],
    code='''
k = 0

class Node:
    def __init__(self):
        self.l = 0
        self.r = 0
        self.to = [0, 0]

class Seg:
    def __init__(self, size):
        self.t = [Node() for _ in range(size)]

    def set(self, o, val):
        self.t[o].to[1] = self.t[o].to[0] ^ val

    def maintain(self, o):
        a, b, c = self.t[o << 1].to, self.t[o << 1 | 1].to, [0, 0]
        for i in range(k):
            c[0] |= (b[a[0] >> i & 1] >> i & 1) << i
            c[1] |= (b[a[1] >> i & 1] >> i & 1) << i
        self.t[o].to = c

    def build(self, a, k, o, l, r):
        self.t[o].l, self.t[o].r = l, r
        self.t[o].to[0] = (1 << k) - 1
        if l == r:
            self.set(o, a[l - 1])
            return
        m = (l + r) >> 1
        self.build(a, k, o << 1, l, m)
        self.build(a, k, o << 1 | 1, m + 1, r)
        self.maintain(o)

    def update(self, o, i, val):
        if self.t[o].l == self.t[o].r:
            self.set(o, val)
            return
        m = (self.t[o].l + self.t[o].r) >> 1
        if i <= m:
            self.update(o << 1, i, val)
        else:
            self.update(o << 1 | 1, i, val)
        self.maintain(o)

class Solution:
    def getNandResult(self, K: int, arr: List[int], operations: List[List[int]]) -> int:
        global k
        ans = 0
        k = K
        t = Seg(len(arr) * 4)
        t.build(arr, k, 1, 1, len(arr))
        for op in operations:
            if op[0] == 0:
                t.update(1, op[1] + 1, op[2])
                continue
            to = t.t[1].to
            x, y = op[1], op[2]
            for i in range(k):
                res = 0
                yy = y >> i & 1
                y1 = to[yy] >> i & 1  # 穿过 arr 一次
                if y1 == yy:  # 不变
                    res = yy
                elif x == 1 or to[y1] >> i & 1 == y1:
                    # 只穿过一次，或者穿过两次和穿过一次相同
                    res = y1
                else:
                    res = yy ^ x % 2  # 奇变偶不变
                ans ^= res << i
        return ans
''',
    call='Solution().getNandResult(2, [1, 2], [[1, 2, 3], [0, 0, 3], [1, 2, 2]])',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=330),
    ],
    skip=['self.l = 0', 'self.r = 0', 'self.to = [0, 0]', 'self.t = [Node()', 'res = 0', 'self.set(o', 'self.update(o << 1', 'to = t.t[1].to', 'self.t[o].to = c', 'm = (', 'self.t[o].l, self.t[o].r = l, r'],
    watch=['x', 'y', 'i', 'res', ('ans', 'ans', 'green')],
    captions={
        't = Seg(len(arr) * 4)': '准备一棵线段树（数组存，结点 `o` 的左右儿子是 `2o`、`2o+1`）',
        't.build(arr': '建树：每个结点记 `to[0]`、`to[1]`——比特 0 / 1 穿过这段区间后的结果',
        '(1 << k) - 1': '`to[0] = 全 1`：比特 0 穿过任何数（NAND）都变成 1，k 位并行，所以是 k 个 1',
        'self.t[o].to[1] = self.t[o].to[0] ^ val': '比特 1 穿过 `val` 得 `~val`（k 位）：用 `to[0] ^ val` 算出来，即 `{self.t[o].to[1]}`',
        'l == r': lambda S, B, r: ('叶子：只有一个数 `arr[l-1]`' if S.l == S.r else '不是叶子，继续分成左右两半'),
        'self.build(a, k, o << 1, l': '先建左儿子 `[{l}, {m}]`',
        'self.build(a, k, o << 1 | 1': '再建右儿子 `[{m+1}, {r}]`',
        'self.maintain(o)': '左右儿子都好了 → 合并成父结点',
        'a, b, c = self.t': '合并：先穿过左儿子 `a`，再把结果穿过右儿子 `b`',
        'c[0] |=': '第 `{i}` 位：0 先穿过左儿子变成 `a[0]` 的这一位，再用这一位去查右儿子 `b`',
        'c[1] |=': '同理 1 穿过整段区间：`c[1]` 的第 `{i}` 位',
        'for op in operations': lambda S, B, r: ('所有操作处理完' if ('op' in B and B.op is S.op) else f'下一个操作 `{S.op}`：' + ('修改 `arr[x] = y`' if S.op[0] == 0 else '运算：把 `y` 穿过 `x` 遍 arr')),
        'if op[0] == 0': lambda S, B, r: ('`type = 0`：单点修改，线段树更新' if S.op[0] == 0 else '`type = 1`：运算操作，拆位查根结点'),
        't.update(1': '线段树单点修改，下标从 1 开始：`arr[{op[1]}] = {op[2]}`',
        'if i <= m': lambda S, B, r: ('目标在左半边，往左儿子走' if S.i <= S.m else '目标在右半边，往右儿子走'),
        'x, y = op[1], op[2]': '`to = 根结点的 to`：比特 0 / 1 穿过整个 arr 一次的结果 `{to}`；运算：`y = {y}` 穿过 arr `{x}` 遍',
        'y >> i & 1': '取 y 的第 `{i}` 位：`{yy}`',
        'y1 = to[yy]': '这个比特穿过 arr 一次后是 `{y1}`',
        'if y1 == yy': lambda S, B, r: (f'穿过一次没变（`{S.y1} == {S.yy}`）→ 无论穿过几次都不变' if S.y1 == S.yy else f'穿过一次变了（`{S.yy}` → `{S.y1}`）→ 看 x 和第二次穿过的结果'),
        'elif x == 1': lambda S, B, r: ('`x == 1` 只穿过一次，或者穿过两次和一次结果相同 → 之后固定为 `y1`' if (S.x == 1 or S.to[S.y1] >> S.i & 1 == S.y1) else '两次穿过会回到原来的数 → 要按 x 的奇偶性分类'),
        'res = yy': '`res = {res}`（不变）',
        'res = y1': '`res = {res}`（固定为穿过一次的结果）',
        'res = yy ^ x % 2': '来回翻转：x 为奇数翻转，偶数不变 → `res = {res}`',
        'ans ^= res << i': '第 `{i}` 位的结果放回 `ans`：`ans = {ans}`（各运算结果异或）',
        'return ans': '所有运算结果异或完毕，返回 `{ans}`',
    },
    cards=dict(
        one_liner='拆位后，每个比特「穿过」整个数组的结果用线段树维护',
        complexity='时间 `O(k(n + q log n))`，空间 `O(n)`',
        problem=['数组 `arr`（k 位二进制数）；`type=0` 把 `arr[x]` 改成 `y`',
                 '`type=1`：把 `y` 与整个 arr 做 `x` 遍 NAND（`y = y NAND arr[i % n]`）',
                 '所有 `type=1` 的结果异或起来就是答案',
                 '本视频：`k=2`，`arr=[1,2]`，`ops=[[1,2,3],[0,0,3],[1,2,2]]` → `2`'],
        quote='想象成 0 或者 1 从左到右「穿过」数组 arr，用线段树维护穿过某段区间后，这个比特如何变化。线段树合并区间：先变成穿过左儿子的结果，然后把这个结果穿过右儿子，得到穿过这段区间的结果。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按位拆开，每一位独立：比特 0 或 1 依次 NAND 过每个数',
              '结点记 `to[0]`、`to[1]`：0 / 1 穿过该区间后变成什么（k 位并行）',
              '查询：穿过一次不变 → 不变；`x=1` 或 穿两次同一次 → 取一次的结果；否则奇变偶不变'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(k(n + q log n))`，空间 `O(n)`',
                 '转写时 Go 里循环内的 `y := y >> i & 1`（遮蔽外层 y）改名为 `yy`，Go 的 `1<<k - 1` 要写成 `(1 << k) - 1`',
                 '易错：NAND 的 0 穿过任何数都变 1；合并时先左后右，顺序不能反'],
    ),
)
