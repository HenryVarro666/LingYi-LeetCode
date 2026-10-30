import math

NUMS = [1, 3, 4, 2, 2]
PTRS = [('slow', 'blue'), ('fast', 'pink'), ('head', 'green')]


def _layout(nums, box):
    """从 0 出发的 ρ 形：尾巴横排，环画成圆；其余节点放在底部一行"""
    x0, y0, x1, y1 = box
    seq, seen = [], {}
    u = 0
    while u not in seen:
        seen[u] = len(seq)
        seq.append(u)
        u = nums[u]
    tail, cyc = seq[:seen[u]], seq[seen[u]:]
    pos = {}
    gap = 150
    cy = y0 + 70 + (y1 - y0 - 140) / 2
    for k, v in enumerate(tail):
        pos[v] = (x0 + 80 + k * gap, cy)
    L = len(cyc)
    R = max(80, 40 * L)
    ex = x0 + 80 + len(tail) * gap
    cx = ex + R
    for k, v in enumerate(cyc):
        a = math.pi + 2 * math.pi * k / L
        pos[v] = (cx + R * math.cos(a), cy - R * math.sin(a))
    rest = [v for v in range(len(nums)) if v not in pos]
    for k, v in enumerate(rest):
        pos[v] = (x1 - 80 - k * 110, y1 - 50)
    return pos, cyc[0]


def _graph(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums') or NUMS
    cv.text((x0 + 18, y0 + 4), '把下标看成节点：i → nums[i]（同 142 环形链表）', 24, T['muted'], bold=True)
    pos, entry = _layout(nums, (x0, y0 + 20, x1, y1))
    r = 30
    edges = {(i, nums[i]) for i in range(len(nums))}
    for i in range(len(nums)):
        j = nums[i]
        (ax, ay), (bx, by) = pos[i], pos[j]
        if i == j:
            cv.d.arc((ax - 22, ay - r - 40, ax + 22, ay - r + 4), 200, 340, fill=T['muted'], width=3)
            cv.tri_down(ax + 16, ay - r - 2, 8, T['muted'])
            continue
        d = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        off = 9 if (j, i) in edges else 0
        px, py = -uy * off, ux * off
        cv.arrow((ax + ux * r + px, ay + uy * r + py), (bx - ux * (r + 4) + px, by - uy * (r + 4) + py), T['muted'], 3, 13)
    indeg = [0] * len(nums)
    for v in nums:
        indeg[v] += 1
    for v, (X, Y) in pos.items():
        hit = [(n, c) for n, c in PTRS if S.get(n) == v]
        fill = T[hit[0][1]] if hit else T['panel2']
        cv.d.ellipse((X - r, Y - r, X + r, Y + r), fill=fill, outline=T['yellow'] if indeg[v] > 1 else T['border'],
                     width=4 if indeg[v] > 1 else 2)
        cv.text((X, Y), str(v), 28, T['bg'] if hit else T['text'], anchor='mm', bold=True)
        for k, (n, c) in enumerate(hit):
            cv.text((X, Y + r + 6 + k * 26), n, 22, T[c], anchor='mt', bold=True)
        if indeg[v] > 1:
            cv.text((X, Y - r - 6), f'入度 {indeg[v]}', 20, T['yellow'], anchor='mb', bold=True)


def _slow_cap(S, B, ret):
    if 'head' in S:
        return f'slow 走一步：`{B.slow} → {S.slow}`'
    return f'slow 走一步：`{B.slow} → {S.slow}`（`slow = slow.next`）'


CONFIG = dict(
    num=287, title='寻找重复数', difficulty='Medium', category='技巧',
    author='灵茶山艾府', technique='基环树 · 快慢指针（同 142）',
    code='''
# 代码逻辑同 142. 环形链表 II
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = 0  # 0 一定不在环上，适合作为起点
        while True:
            slow = nums[slow]  # 等价于 slow = slow.next
            fast = nums[nums[fast]]  # 等价于 fast = fast.next.next
            if fast == slow:  # 快慢指针移动到同一个节点
                break

        head = 0  # 再用一个指针，从起点出发
        while slow != head:
            slow = nums[slow]
            head = nums[head]
        return slow  # 入环口即重复元素
''',
    call=f'Solution().findDuplicate({NUMS})',
    expect=2,
    skip=['while True'],
    views=[
        dict(type='array', var='nums', label='nums（下标 i 指向 nums[i]）', h=215, cell=90,
             pointers={'slow': 'blue', 'fast': 'pink', 'head': 'green'}),
        dict(type='custom', draw=_graph, h=400),
    ],
    watch=[('slow', 'slow', 'blue'), ('fast', 'fast', 'pink'), ('head', 'head', 'green')],
    captions={
        'slow = fast = 0': '第一阶段：`nums[i] ≥ 1`，没有边指向 0 → ==0 一定不在环上==，从 0 出发（相当于链表头）',
        'slow = nums[slow]': _slow_cap,
        'fast = nums[nums[fast]]': 'fast 走两步：`{B.fast} → {B.nums[B.fast]} → {fast}`（`fast = fast.next.next`）',
        'if fast == slow': lambda S, B, ret: (f'`fast == slow == {S.slow}` → ==相遇==' if S.fast == S.slow
                                              else f'`fast = {S.fast} ≠ slow = {S.slow}`，继续'),
        'break': '快慢指针在环上相遇，第一阶段结束',
        'head = 0': '第二阶段：再用一个指针 `head` 从起点 0 出发',
        'while slow != head': lambda S, B, ret: (f'`slow = {B.slow} ≠ head = {B.head}` → 两个指针各走一步' if B.slow != B.head
                                                 else f'`slow == head == {B.slow}` → 在==入环口==相遇'),
        'head = nums[head]': 'head 走一步：`{B.head} → {head}`',
        'return slow': '入环口 = 入度大于 1 的节点 = 重复元素 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='把 i → nums[i] 看成链表，重复数就是入环口',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['长度 `n+1` 的数组，数字都在 `[1, n]` 内，只有==一个数重复==（可能多次）',
                 '要求：==不修改==数组，只用 `O(1)` 额外空间',
                 '示例：`[1,3,4,2,2]` → `2`，`[3,1,3,4,2]` → `3`'],
        quote='每个节点的入度，就是这个节点在 nums 中的出现次数。重复元素的入度大于 1……从节点 0 出发，进入基环，==基环的入环口，就是入度大于 1 的节点==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['连边 `i → nums[i]`：`n+1` 个点 `n+1` 条边，出度都是 1 → ==内向基环森林==',
              '`nums[i] ≥ 1` → 节点 0 入度为 0，不在环上；从 0 出发的形状和 142 题一样',
              '对应关系：`node.next` ↔ `nums[i]`，头节点 ↔ `0`，入环口 ↔ 重复元素'],
        result='入环口是 `2` → 重复数为 `2` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`，没有修改数组',
                 '易错：必须从节点 ==0== 出发；从别的点出发可能根本走不到入环口',
                 '`nums[i] < n+1`，所以 `nums[i]` 作为下标不会越界',
                 '进阶：`n+1` 个球放进 `n` 个抽屉，必有重复（抽屉原理）'],
    ),
)
