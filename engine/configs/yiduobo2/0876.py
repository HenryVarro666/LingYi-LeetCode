VALS = [1, 2, 3, 4, 5]


def _chain(S):
    """phead（若已创建）+ 原链表"""
    out = []
    ph = S.get('phead')
    if ph is not None:
        out.append(ph)
    cur = S.get('head')
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
    cv.text((x0 + 18, y0 + 4), '链表（灰框 0 = 哑节点 phead）', 24, T['muted'], bold=True)
    nodes = _chain(S)
    if not nodes:
        return
    has_ph = S.get('phead') is not None
    n = len(nodes)
    gap = min(140, (x1 - x0 - 80) / (n + 1))
    nw, nh = min(80, gap * 0.6), 64
    left = x0 + (x1 - x0 - gap * (n + 1)) / 2 + (gap - nw) / 2
    Y = y0 + (y1 - y0) / 2 + 40

    def X(k):
        return left + k * gap + nw / 2
    ptrs = [('one_step', 'green', '慢 one_step'), ('two_step', 'pink', '快 two_step')]
    at = {}
    for name, c, disp in ptrs:
        if name not in S or S[name] is None:
            continue
        k = _idx(nodes, S[name])
        if k is not None:
            at.setdefault(k, []).append((disp, T[c]))
    for k in range(n):
        nd = nodes[k]
        if k + 1 < n and nd.next is nodes[k + 1]:
            cv.arrow((X(k) + nw / 2, Y), (X(k + 1) - nw / 2 - 2, Y), T['muted'], 3, 12)
        elif k + 1 == n:
            cv.text((X(k) + nw / 2 + 10, Y), '∅', 26, T['dim'], anchor='lm')
    done = S.get('_line') in (9, 12)  # break / return
    for k in range(n):
        hs = at.get(k, [])
        dummy = has_ph and k == 0
        fill = hs[0][1] if hs else ((26, 30, 37) if dummy else T['panel2'])
        mid = done and nodes[k] is S.get('one_step')
        cv.rect((X(k) - nw / 2, Y - nh / 2, X(k) + nw / 2, Y + nh / 2), fill=fill, r=10,
                outline=T['yellow'] if mid else (T['dim'] if dummy else T['border']), width=4 if mid else 2)
        cv.text((X(k), Y), str(nodes[k].val), 30, T['bg'] if hs else (T['muted'] if dummy else T['text']),
                anchor='mm', bold=True)
        cv.text((X(k), Y + nh / 2 + 10), 'phead' if dummy else f'第{k if has_ph else k + 1}个', 18, T['dim'], anchor='mt')
        for r, (disp, c) in enumerate(hs):
            r = 1 if disp.startswith('快') else 0  # 快指针的名字放高一行，避免和相邻的慢指针挤在一起
            yy = Y - nh / 2 - 10 - r * 46
            cv.tri_down(X(k), yy, 9, c)
            cv.text((X(k), yy - 12), disp, 22, c, anchor='mb', bold=True)


def _info(S):
    nodes = _chain(S)
    if 'one_step' not in S or S.get('phead') is None:
        return '先在链表头前面放一个==哑节点== `phead`'
    a, b = _idx(nodes, S['one_step']), _idx(nodes, S['two_step'])
    return f'从 `phead` 算起：慢指针走了 `{a}` 步，快指针走了 `{b}` 步'


def _look(S):
    t = S.get('two_step')
    if t is None:
        return ''
    a = t.next
    b = a.next if a is not None else None
    v = lambda x: 'None' if x is None else str(x.val)
    if a is None:
        return '快指针后面：`two_step.next = None` → 不够两步'
    return f'快指针后面：`two_step.next = {v(a)}`，`two_step.next.next = {v(b)}`' + (' → ==不够两步==' if b is None else '')


def _if_cap(S, B, ret):
    t = S.two_step
    name = '在 phead' if t is S.phead else f'= {t.val}'
    if t.next is None:
        return f'`two_step` {name} 的下一个就是空 → 快指针到末尾了，==停=='
    if t.next.next is None:
        return f'`two_step` {name} 后面只剩 `{t.next.val}` 一个节点 → 走不了两步，==停=='
    return f'`two_step` {name}，后面还有 `{t.next.val}`、`{t.next.next.val}` 两个节点 → 快指针可以继续'


CONFIG = dict(
    num=876, title='链表的中间结点', difficulty='Easy', category='链表',
    author='yiduobo', technique='哑节点 + 快慢指针',
    tags=['字节30天'],
    code='''
class Solution(object):
    def middleNode(self, head):
        phead = ListNode(0)
        phead.next = head
        one_step = two_step = phead
        while True:
            one_step = one_step.next
            if two_step.next is None or two_step.next.next is None:
                break
            two_step = two_step.next.next

        return one_step
''',
    call=f'Solution().middleNode(L({VALS}))',
    result_fn=list_vals,
    expect=[3, 4, 5],
    views=[
        dict(type='text', h=60, fn=_info, size=27),
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', h=60, fn=_look, size=26),
    ],
    watch=[('one_step（慢）', 'one_step', 'green'), ('two_step（快）', 'two_step', 'pink')],
    captions={
        'phead = ListNode(0)': '新建一个==哑节点== `phead`（值为 0）',
        'phead.next = head': '`phead.next = head`：哑节点接在原链表头的前面',
        'one_step = two_step = phead': '慢指针 `one_step`、快指针 `two_step` 都从 ==phead== 出发',
        'while True': '`while True`：新的一轮（只靠 `break` 退出）',
        'one_step = one_step.next': '每轮==先让慢指针走一步==：`one_step` → `{one_step.val}`',
        'if two_step.next is None': _if_cap,
        'break': '跳出循环：此时慢指针恰好停在中间节点',
        'two_step = two_step.next.next': '快指针走两步：`two_step` → `{two_step.val}`',
        'return one_step': '返回 `one_step` → 中间节点 =={ret.val}==',
    },
    cards=dict(
        one_liner='快指针每轮走两步、慢指针走一步，快指针到末尾时慢指针恰好在中间',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你单链表的头结点 `head`，返回链表的==中间结点==',
                 '如果有两个中间结点，==返回第二个==',
                 '示例：`[1,2,3,4,5]` → `3`（本视频）；`[1,2,3,4,5,6]` → `4`'],
        quote='维护一组快慢指针，其中快指针每轮往后走两个节点，而慢指针则是往后走一个节点，那么==当快指针在走到链表末尾时，慢指针就恰好走到中间节点了==。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素做法：先遍历一趟求长度 `l`，再从头走 `l/2` 步——要==两次遍历==',
              '快慢指针只需==一次遍历==',
              '实现细节：两指针从哑节点 `phead` 出发，每轮慢指针先走，再检查快指针能否走两步'],
        after=[dict(heading='哑节点 + “先走慢指针”', lines=[
            '从 `phead` 出发相当于从“第 0 个节点”出发，慢指针走 `k` 步就停在第 `k` 个节点',
            '奇数 `n = 5`：快指针停在第 4 个，慢指针走 3 步 → 第 3 个',
            '偶数 `n = 6`：快指针停在第 6 个，慢指针走 4 步 → 第 4 个，即==第二个中间结点=='])],
        result='运行结束，返回结点 `3`（链表 `[3,4,5]`），和示例 1 一致',
        summary=['时间 `O(n)`：只遍历一次；空间 `O(1)`',
                 '循环里==先移动慢指针，再判断==快指针能否走两步，顺序不能换',
                 '对比灵神：灵神从 `head` 出发、用 `while fast and fast.next`，不需要哑节点',
                 '原文为 Python 2 风格，只删去了 docstring 和 ListNode 定义注释，代码未改'],
    ),
)
