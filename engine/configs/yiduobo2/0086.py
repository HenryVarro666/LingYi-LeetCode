# ---- 自定义链表视图：上排 = left 部分（< x，哨兵 left_head 开头）+ 尚未扫描的节点，下排 = right 部分（≥ x）
# ---- 节点按"属于哪一部分"动态排位，箭头画的是真实的 next 指针；这一步刚改过的 next 画成黄色
import tracer

VALS = [1, 4, 3, 2, 5, 2]
X = 3


def _chain(start, stop):
    out, cur = [], start
    while cur is not None and len(out) < 20:
        out.append(cur)
        if stop is not None and cur is stop:
            break
        cur = cur.next
    return out


def _all(S):
    seen, out = set(), []
    for v in S.values():
        cur = v if isinstance(v, ListNode) else None
        while cur is not None and cur._uid not in seen:
            seen.add(cur._uid)
            out.append(cur)
            cur = cur.next
    return out


def _bnext(B):
    """执行前每个节点 next 指向谁（uid）"""
    return {n._uid: (n.next._uid if n.next else None) for n in _all(B)}


def draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    LH, RH = S.get('left_head'), S.get('right_head')
    if LH is None:
        cv.text((x0 + 18, y0 + 10), '（哨兵节点尚未创建）', 24, T['dim'])
        return
    ln, rn = S.get('left_now'), S.get('right_now')
    rowL = _chain(LH, ln if ln is not None else LH)
    rowR = _chain(RH, rn if rn is not None else RH) if RH is not None else []
    if ln is None:
        rowL = [LH]
    if rn is None:
        rowR = [RH] if RH is not None else []
    placed = {n._uid for n in rowL + rowR}
    rest = sorted([n for n in _all(S) if n._uid not in placed and n._uid in tracer._origin],
                  key=lambda n: tracer._origin[n._uid][1])
    lab_w = 150
    ncol = max(len(rowL) + len(rest) + 0.5, len(rowR), 7.5)
    gap = min(125, (x1 - x0 - lab_w - 40) / ncol)
    nw, nh = min(66, gap * 0.6), 50
    ya, yb = y0 + 110, y0 + 330
    pos = {}
    for c, n in enumerate(rowL):
        pos[n._uid] = (x0 + lab_w + c * gap + nw / 2, ya)
    for c, n in enumerate(rest):
        pos[n._uid] = (x0 + lab_w + (len(rowL) + 0.5 + c) * gap + nw / 2, ya)
    for c, n in enumerate(rowR):
        pos[n._uid] = (x0 + lab_w + c * gap + nw / 2, yb)
    cv.text((x0 + 18, ya), '< x 部分', 24, T['blue'], anchor='lm', bold=True)
    cv.text((x0 + 18, yb), '≥ x 部分', 24, T['pink'], anchor='lm', bold=True)
    if rest:
        X0 = pos[rest[0]._uid][0] - nw / 2 - 8
        X1 = pos[rest[-1]._uid][0] + nw / 2 + 8
        cv.rect((X0, ya - nh / 2 - 14, X1, ya + nh / 2 + 14), outline=T['dim'], width=2, r=12)
        cv.text(((X0 + X1) / 2, ya + nh / 2 + 20), '尚未扫描', 20, T['muted'], anchor='mt')
    bn = _bnext(B)
    nodes = {n._uid: n for n in _all(S)}
    for uid, n in nodes.items():
        if uid not in pos:
            continue
        X, Y = pos[uid]
        m = n.next
        changed = uid in bn and bn[uid] != (m._uid if m else None)
        c = T['yellow'] if changed else T['muted']
        if m is None or m._uid not in pos:
            cv.text((X + nw / 2 + 6, Y), '∅', 22, T['yellow'] if changed else T['dim'], anchor='lm')
            continue
        X2, Y2 = pos[m._uid]
        if abs(Y2 - Y) < 1 and X2 > X:
            cv.arrow((X + nw / 2, Y), (X2 - nw / 2 - 2, Y2), c, 4 if changed else 3, 12)
        elif abs(Y2 - Y) < 1:
            cv.arc_arrow((X, Y - nh / 2), (X2, Y2 - nh / 2), 40, c, 3, 11)
        else:
            sy = 1 if Y2 > Y else -1
            cv.arrow((X + nw * 0.25, Y + sy * nh / 2), (X2 - nw * 0.15, Y2 - sy * (nh / 2 + 2)), c, 4 if changed else 3, 12)
    hits = {}
    for name, cc in (('left_now', T['blue']), ('right_now', T['pink'])):
        v = S.get(name)
        if isinstance(v, ListNode):
            hits.setdefault(v._uid, []).append((name, cc))
    done_l = {n._uid for n in rowL[1:]}
    done_r = {n._uid for n in rowR[1:]}
    for uid, n in nodes.items():
        if uid not in pos:
            continue
        X, Y = pos[uid]
        dummy = n is LH or n is RH
        fill = T['panel'] if dummy else (mix(T['blue'], T['panel2'], 0.55) if uid in done_l else
                                         mix(T['pink'], T['panel2'], 0.55) if uid in done_r else T['panel2'])
        hs = hits.get(uid, [])
        cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10,
                outline=hs[0][1] if hs else T['border'], width=4 if hs else 2)
        cv.text((X, Y), '哨' if dummy else n.val, 22 if dummy else 26, T['muted'] if dummy else T['text'], anchor='mm', bold=True)
        if dummy:
            cv.text((X, Y + nh / 2 + 6), 'left_head' if n is LH else 'right_head', 17, T['dim'], anchor='mt', mono=True)
        for r, (name, cc) in enumerate(hs):
            cv.text((X, Y - nh / 2 - 6 - r * 24), name, 20, cc, anchor='mb', bold=True)


def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _if(S, B, ret):
    v = B.left_now.next.val
    if v >= S.x:
        return f'下一个节点 `{v} ≥ x = {S.x}` → 要把它==摘下来，接到 right 部分=='
    return f'下一个节点 `{v} < x = {S.x}` → 无事发生，留在 left 部分'


def _while(S, B, ret):
    nx = B.left_now.next
    if nx is not None:
        return f'`left_now` 后面还有节点 `{nx.val}` → 继续扫描'
    return '`left_now.next` 为空：所有节点都扫描完了'


CONFIG = dict(
    num=86, title='分隔链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='两个哨兵 · 把 ≥x 的节点摘到 right 链',
    tags=['List.md', '面试经典150'],
    code='''
class Solution(object):
    def partition(self, head, x):
        left_head = ListNode(0)
        right_head = ListNode(0)
        left_head.next = head

        left_now = left_head
        right_now = right_head

        while left_now.next:
            if left_now.next.val >= x:
                right_now.next = left_now.next
                right_now = right_now.next
                left_now.next = right_now.next
            else:
                left_now = left_now.next

        left_now.next = right_head.next
        right_now.next = None
        return left_head.next
''',
    call=f'Solution().partition(L({VALS}), {X})',
    expect=[1, 2, 2, 4, 3, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: f"`x = {X}`：小于 x 留在上排，≥ x 摘到下排，==两部分各自保持原顺序=="),
        dict(type='custom', draw=draw, h=480),
    ],
    watch=[('left_now', 'left_now', 'blue'), ('right_now', 'right_now', 'pink'),
           ('left_now.next', lambda S: S['left_now'].next if S.get('left_now') else None), 'x'],
    captions={
        'left_head = ListNode(0)': '`left_head`：哨兵，next 指向 head，表示==小于 x 的部分==',
        'right_head = ListNode(0)': '`right_head`：另一个哨兵，起始为空，表示==大于等于 x 的部分==',
        'left_head.next = head': '`left_head.next = head`：一开始整条链都挂在 left 后面，等待扫描',
        'left_now = left_head': '`left_now`：left 部分的末尾，从哨兵开始',
        'right_now = right_head': '`right_now`：right 部分的末尾',
        'while left_now.next': _while,
        'if left_now.next.val >= x': _if,
        'right_now.next = left_now.next': lambda S, B, r: f'把 `{S.right_now.next.val}` 接到 right 部分末尾（黄色箭头）',
        'right_now = right_now.next': lambda S, B, r: f'`right_now` 后移到 `{S.right_now.val}`，right 部分变长',
        'left_now.next = right_now.next': lambda S, B, r: (f'left 跳过 `{S.right_now.val}`：`left_now.next` 改指 '
                                                           + (f'`{S.left_now.next.val}`' if S.left_now.next else '`None`')
                                                           + '，摘除完成；==left_now 不动=='),
        'left_now = left_now.next': lambda S, B, r: f'`left_now` 后移到 `{S.left_now.val}`，left 部分变长',
        'left_now.next = right_head.next': lambda S, B, r: (f'把 right 部分整体接到 left 末尾：`{S.left_now.val}` → '
                                                            + (f'`{S.left_now.next.val}`' if S.left_now.next else '`None`')),
        'right_now.next = None': lambda S, B, r: (f'`{S.right_now.val}` 原来还指着 '
                                                  + (f'`{B.right_now.next.val}`' if B.right_now.next else '`None`')
                                                  + ' → ==必须断开==，否则会成环/多出节点'),
        'return left_head.next': '返回 `left_head.next`（跳过哨兵）',
    },
    cards=dict(
        one_liner='扫描时把 ≥x 的节点摘下来接到 right 链，最后 left 尾接 right 头',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给链表 `head` 和值 `x`，让所有 ==小于 x== 的节点排在 ==大于或等于 x== 的节点之前',
                 '两部分内部都要==保持原来的相对顺序==',
                 '示例：`head = [1,4,3,2,5,2], x = 3` → `[1,2,2,4,3,5]`'],
        quote='若当前节点存在next，且next.val小于x，那么无事发生，继续往后扫描left。否则==将next接在right部分==，然后继续扫描left。',
        quote_src='—— yiduobo 题解',
        idea=['`left_head` → head：小于 x 的部分；`right_head` 起始为空：≥ x 的部分',
              '看的是 `left_now.next`（下一个），这样摘除时手里有前驱，能直接跳过它',
              '摘走节点后 `left_now` 不动，下一轮继续看新的 `left_now.next`'],
        summary=['时间 `O(n)`，空间 `O(1)`：只改指针，不新建节点（两个哨兵除外）',
                 '易错：最后要 `right_now.next = None`，否则 right 末尾还指着旧节点',
                 '易错：摘除后不要移动 `left_now`，否则会漏看节点',
                 '常见写法是建两条新链分别尾插；yiduobo 是在原链上“摘”',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串和节点定义注释'],
    ),
)
