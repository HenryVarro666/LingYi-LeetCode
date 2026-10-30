import math

NUMS = [3, 1, 3, 4, 2]
PTRS = [('slow', 'blue'), ('fast', 'pink')]


def _layout(nums, box):
    """从 0 出发的 ρ 形：尾巴横排，环画成圆；其余节点放在右下角"""
    x0, y0, x1, y1 = box
    seq, seen = [], {}
    u = 0
    while u not in seen:
        seen[u] = len(seq)
        seq.append(u)
        u = nums[u]
    tail, cyc = seq[:seen[u]], seq[seen[u]:]
    pos = {}
    gap = 160
    cy = y0 + 70 + (y1 - y0 - 140) / 2
    for k, v in enumerate(tail):
        pos[v] = (x0 + 90 + k * gap, cy)
    L = len(cyc)
    R = max(80, 45 * L)
    cx = x0 + 90 + len(tail) * gap + R
    for k, v in enumerate(cyc):
        a = math.pi + 2 * math.pi * k / L
        pos[v] = (cx + R * math.cos(a), cy - R * math.sin(a))
    rest = [v for v in range(len(nums)) if v not in pos]
    for k, v in enumerate(rest):
        pos[v] = (x1 - 90 - k * 110, y1 - 60)
    return pos


def _graph(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums') or NUMS
    cv.text((x0 + 18, y0 + 4), '0 到 n 视为 n+1 个点，x → nums[x] 建有向边', 24, T['muted'], bold=True)
    pos = _layout(nums, (x0, y0 + 20, x1, y1))
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
    phase2 = S.get('_line', 0) >= 11
    for v, (X, Y) in pos.items():
        hit = [(n, c) for n, c in PTRS if S.get(n) == v]
        fill = T[hit[0][1]] if hit else T['panel2']
        cv.d.ellipse((X - r, Y - r, X + r, Y + r), fill=fill, outline=T['border'], width=2)
        cv.text((X, Y), str(v), 28, T['bg'] if hit else T['text'], anchor='mm', bold=True)
        for k, (n, c) in enumerate(hit):
            label = 'fast(从0)' if (n == 'fast' and phase2) else n
            cv.text((X, Y + r + 6 + k * 26), label, 22, T[c], anchor='mt', bold=True)


CONFIG = dict(
    num=287, title='寻找重复数', difficulty='Medium', category='技巧',
    author='yiduobo', technique='有向图找入环点 · 快慢指针',
    code='''
class Solution(object):
    def findDuplicate(self, nums):
        fast = 0
        slow = 0
        while True:
            fast = nums[nums[fast]]
            slow = nums[slow]
            if fast == slow:
                break

        fast = 0
        while fast != slow:
            fast = nums[fast]
            slow = nums[slow]

        return fast
''',
    call=f'Solution().findDuplicate({NUMS})',
    expect=3,
    skip=['while True'],
    views=[
        dict(type='array', var='nums', label='nums', h=215, cell=90,
             pointers={'slow': 'blue', 'fast': 'pink'}),
        dict(type='custom', draw=_graph, h=400),
    ],
    watch=[('slow', 'slow', 'blue'), ('fast', 'fast', 'pink')],
    captions={
        'fast = 0': lambda S, B, ret: ('把 0 视为链表头：快指针 `fast = 0`' if 'slow' not in B
                                       else '第二阶段：`fast` 回到 0，之后改为==每次走一步=='),
        'slow = 0': '慢指针 `slow = 0`',
        'fast = nums[nums[fast]]': '快指针走两步：`fast {B.fast} → {B.nums[B.fast]} → {fast}`',
        7: '慢指针走一步：`slow {B.slow} → {slow}`',
        14: 'slow 也走一步：`{B.slow} → {slow}`',
        'if fast == slow': lambda S, B, ret: (f'`fast == slow == {S.slow}` → ==相遇==' if S.fast == S.slow
                                              else f'`fast = {S.fast} ≠ slow = {S.slow}`，继续'),
        'break': '相遇点一定在环上，第一阶段结束',
        'while fast != slow': lambda S, B, ret: (f'`fast = {B.fast} ≠ slow = {B.slow}` → 各走一步' if B.fast != B.slow
                                                 else f'`fast == slow == {B.slow}` → 这就是==入环的节点=='),
        'fast = nums[fast]': 'fast 走一步：`{B.fast} → {fast}`',
        'return fast': '入环节点 = 被两条边指向的点 = 重复数 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='0 到 n 当成节点，x → nums[x] 连边，答案就是入环的节点',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['长度 `n+1` 的数组，数字都在 `[1, n]` 内，只有==一个数重复==（可能多次）',
                 '要求：==不修改==数组，只用 `O(1)` 额外空间',
                 '示例：`[1,3,4,2,2]` → `2`，`[3,1,3,4,2]` → `3`'],
        quote='将0到n视为n + 1个点，然后在这些点之间，通过x到nums[x]的对应关系建立有向边，最终可以得到一张有向有环图，而题目此时就变成了==找到入环的节点==。',
        quote_src='—— yiduobo 题解',
        idea=['这其实就是 142 题环形链表：==如法炮制==',
              '将 0 视为链表头，快指针每次两步、慢指针每次一步，直到相遇',
              '再让一个指针从 0 出发，两者每次各走一步，相遇处就是入环节点'],
        result='入环节点是 `3` → 重复数为 `3` ✓（节点 1 自成一环，从 0 出发走不到）',
        summary=['时间 `O(n)`，空间 `O(1)`，没有改动原始数组',
                 '第二阶段复用了 `fast` 变量：从 0 出发，==每次只走一步==',
                 '为什么从 0 出发：没有 `nums[x] = 0`，0 一定在环外，像链表头',
                 '原文为 Python 2 写法：仅删去文档字符串，逻辑未改'],
    ),
)
