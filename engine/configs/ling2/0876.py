VALS = [1, 2, 3, 4, 5, 6]


def _chain(S):
    out, cur = [], S.get('head')
    while cur is not None and len(out) < 20:
        out.append(cur)
        cur = cur.next
    return out


def _idx(nodes, v):
    for k, nd in enumerate(nodes):
        if nd is v:
            return k
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '链表（最右边的 ∅ 是最后一个节点的下一个：None）', 24, T['muted'], bold=True)
    nodes = _chain(S)
    if not nodes:
        return
    n = len(nodes)
    gap = min(140, (x1 - x0 - 80) / (n + 1))
    nw, nh = min(80, gap * 0.6), 64
    left = x0 + (x1 - x0 - gap * (n + 1)) / 2 + (gap - nw) / 2
    Y = y0 + (y1 - y0) / 2 + 30

    def X(k):
        return left + k * gap + nw / 2
    ptrs = [('slow', 'green', '乌龟 slow'), ('fast', 'pink', '兔子 fast')]
    at = {}
    for name, c, disp in ptrs:
        if name not in S:
            continue
        k = n if S[name] is None else _idx(nodes, S[name])
        if k is not None:
            at.setdefault(k, []).append((disp, T[c]))
    for k in range(n):
        if k + 1 < n:
            cv.arrow((X(k) + nw / 2, Y), (X(k + 1) - nw / 2 - 2, Y), T['muted'], 3, 12)
        else:
            cv.arrow((X(k) + nw / 2, Y), (X(n) - nw / 2 - 2, Y), T['dim'], 2, 10)
    mid = n // 2
    for k in range(n + 1):
        hs = at.get(k, [])
        fill = hs[0][1] if hs else T['panel2']
        if k == n:
            cv.rect((X(k) - nw / 2, Y - nh / 2, X(k) + nw / 2, Y + nh / 2), fill=fill if hs else T['bg'], r=10,
                    outline=T['dim'], width=2)
            cv.text((X(k), Y), '∅', 30, T['bg'] if hs else T['dim'], anchor='mm', bold=True)
        else:
            cv.rect((X(k) - nw / 2, Y - nh / 2, X(k) + nw / 2, Y + nh / 2), fill=fill, r=10,
                    outline=T['yellow'] if (k == mid and S.get('_line') == 7) else T['border'],
                    width=4 if (k == mid and S.get('_line') == 7) else 2)
            cv.text((X(k), Y), str(nodes[k].val), 30, T['bg'] if hs else T['text'], anchor='mm', bold=True)
            cv.text((X(k), Y + nh / 2 + 10), f'第{k + 1}个', 18, T['dim'], anchor='mt')
        for r, (disp, c) in enumerate(hs):
            yy = Y - nh / 2 - 10 - r * 46
            cv.tri_down(X(k), yy, 9, c)
            cv.text((X(k), yy - 12), disp, 22, c, anchor='mb', bold=True)


def _race(S):
    nodes = _chain(S)
    if 'slow' not in S or not nodes:
        return '龟兔赛跑：兔子的速度是乌龟的 ==2 倍=='
    k = _idx(nodes, S['slow'])
    f = len(nodes) if S['fast'] is None else _idx(nodes, S['fast'])
    return f'乌龟走了 `{k}` 步，兔子走了 `{f}` 步 = ==2 × {k}=='


def _trail(S, who):
    nodes = _chain(S)
    if who not in S or not nodes:
        return ''
    if who == 'slow':
        k = _idx(nodes, S['slow'])
        seq = [str(nodes[i].val) for i in range(k + 1)]
        return '乌龟轨迹：`' + ' → '.join(seq) + '`（每次 1 步）'
    f = len(nodes) if S['fast'] is None else _idx(nodes, S['fast'])
    seq = [str(nodes[i].val) if i < len(nodes) else '∅' for i in range(0, f + 1, 2)]
    return '兔子轨迹：`' + ' → '.join(seq) + '`（每次 2 步）'


def _while_cap(S, B, ret):
    f = B.fast
    if f is not None and f.next is not None:
        return f'`fast = {f.val}`，`fast.next = {f.next.val}` 都不为空 → 兔子还能走两步，继续'
    if f is None:
        return '`fast` 已经是 ==None==（最后一个节点的下一个）→ `n` 为偶数，停止'
    return f'`fast.next` 为空：兔子站在==最后一个节点== → `n` 为奇数，停止'


def _fast_cap(S, B, ret):
    f = S.fast
    return f'兔子走两步：`fast` → `{f.val}`' if f is not None else '兔子走两步：`fast` → ==None==（越过了最后一个节点）'


CONFIG = dict(
    num=876, title='链表的中间结点', difficulty='Easy', category='链表',
    author='灵茶山艾府', technique='快慢指针（龟兔赛跑）',
    tags=['字节30天'],
    code='''
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next  # 乌龟走一步
            fast = fast.next.next  # 兔子走两步
        return slow  # 兔子到达终点时，乌龟走了一半，在中间位置
''',
    call=f'Solution().middleNode(L({VALS}))',
    result_fn=list_vals,
    expect=[4, 5, 6],
    views=[
        dict(type='text', h=60, fn=_race, size=28),
        dict(type='custom', draw=_draw, h=380),
        dict(type='text', h=50, fn=lambda S: _trail(S, 'slow'), size=26),
        dict(type='text', h=50, fn=lambda S: _trail(S, 'fast'), size=26),
    ],
    watch=[('slow（乌龟）', 'slow', 'green'), ('fast（兔子）', 'fast', 'pink')],
    captions={
        'slow = fast = head': '乌龟 `slow` 和兔子 `fast` 同时从 `head` 出发',
        'while fast and fast.next': _while_cap,
        'slow = slow.next': '乌龟走一步：`slow` → `{slow.val}`',
        'fast = fast.next.next': _fast_cap,
        'return slow': '兔子到达终点时，乌龟走了一半：返回 =={ret.val}==（6 个节点，返回第二个中间结点）',
    },
    cards=dict(
        one_liner='兔子速度是乌龟的两倍：兔子到终点时，乌龟恰好在中间',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你单链表的头结点 `head`，返回链表的==中间结点==',
                 '如果有两个中间结点，==返回第二个==',
                 '示例：`[1,2,3,4,5]` → `3`；`[1,2,3,4,5,6]` → `4`（本视频）'],
        quote='龟兔赛跑。如果兔子速度恰好比乌龟速度快一倍，那么==当兔子到达终点时，乌龟走了一半==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个指针都从 `head` 出发：快指针每次走两步，慢指针每次走一步',
              '快指针移动到==最后一个节点==，或==最后一个节点的下一个（空节点）==时停止',
              '只需遍历一次，不用先求链表长度'],
        after=[dict(heading='为什么停下时 slow 恰好在中间？', lines=[
            '`n` 为奇数：快指针停在最后一个节点，移动了 `floor(n/2)` 次',
            '慢指针停在第 `1 + floor(n/2)` 个节点，例如 `n = 5` 停在第 3 个',
            '`n` 为偶数：快指针停在空节点，移动 `n/2` 次，慢指针停在第 `1 + n/2` 个',
            '例如 `n = 6` 停在第 4 个——正好是题目要的==第二个==中间结点'])],
        result='运行结束，返回结点 `4`（链表 `[4,5,6]`），和示例 2 一致',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环条件 `fast and fast.next` 缺一不可：分别对应偶数和奇数长度',
                 '==不用判断 slow==：乌龟走的都是兔子走过的路',
                 '同类：141 环形链表、142 环形链表 II、234 回文链表都用快慢指针'],
    ),
)
