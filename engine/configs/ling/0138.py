import tracer as _tr


def _collect(S):
    nodes = {}

    def walk(v, d=0):
        if d > 30 or not isinstance(v, Node) or v._uid in nodes:
            return
        nodes[v._uid] = v
        walk(v.next, d + 1)
        walk(v.random, d + 1)
    for v in S.values():
        walk(v)
    return nodes


def _rl_view(ptrs, title, n):
    """138 专用：原链表在上排，拷贝节点在下排（正好在原节点正下方）；
    next 用灰色实线箭头，random 用紫色弧线（上排画在上方，下排画在下方）；本步改动的指针标黄。"""
    def place(S):
        nodes = _collect(S)
        org = _tr._origin
        pos = {u: org[u] for u in nodes if u in org}
        new = sorted(u for u in nodes if u not in org)
        for k, u in enumerate(new):
            pos[u] = (1, k + 1) if k < n else (1, 0)  # 第 n+1 个新节点是 dummy，放在下排最左
        return nodes, pos

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        nodes, pos = place(S)
        bnodes = _collect(B)
        gap = min(200, (x1 - x0 - 100) / (n + 1))
        nw, nh = min(70, gap * 0.5), 50
        rowy = [y0 + 175, y0 + 175 + min(190, (y1 - y0 - 330))]

        def xy(u):
            r, c = pos[u]
            return x0 + 50 + c * gap + nw / 2, rowy[r]

        def changed(u, attr):
            b = bnodes.get(u)
            return b is not None and getattr(getattr(b, attr), '_uid', None) != getattr(getattr(nodes[u], attr), '_uid', None)

        for u, nd in nodes.items():
            X, Y = xy(u)
            r, c = pos[u]
            for attr in ('next', 'random'):
                tg = getattr(nd, attr)
                ch = changed(u, attr)
                if tg is None:
                    if attr == 'next':
                        cv.text((X + nw / 2 + 6, Y), '∅', 22, T['yellow'] if ch else T['dim'], anchor='lm')
                    continue
                if tg._uid not in pos:
                    continue
                X2, Y2 = xy(tg._uid)
                r2, c2 = pos[tg._uid]
                if attr == 'random':
                    color, w = (T['yellow'], 3) if ch else (T['purple'], 2)
                    up = r == 0
                    sgn = 1 if c2 >= c else -1
                    p0 = (X + sgn * nw * 0.22, Y + (-nh / 2 if up else nh / 2))
                    p1 = (X2 - sgn * nw * 0.22, Y2 + (-nh / 2 - 3 if up else nh / 2 + 3))
                    lift = 34 + 12 * abs(c2 - c)
                    cv.arc_arrow(p0, p1, lift if up else -lift, color, w, 10)
                    continue
                color, w = (T['yellow'], 4) if ch else (T['muted'], 3)
                if r2 == r and c2 == c + 1:
                    cv.arrow((X + nw / 2 + 2, Y), (X2 - nw / 2 - 3, Y2), color, w, 12)
                elif r2 == r:
                    cv.arc_arrow((X, Y + nh / 2), (X2, Y2 + nh / 2 + 3), -(30 + 10 * abs(c2 - c)), color, w, 12)
                else:
                    down = r2 > r
                    s = 0 if c2 == c else (1 if c2 > c else -1)
                    p0 = (X + s * nw * 0.28, Y + (nh / 2 if down else -nh / 2))
                    p1 = (X2 - s * nw * 0.28, Y2 + (-nh / 2 - 3 if down else nh / 2 + 3))
                    cv.arrow(p0, p1, color, w, 12)
        hit = {}
        for name, c in (ptrs(S) if callable(ptrs) else ptrs).items():
            v = S.get(name)
            if isinstance(v, Node) and v._uid in pos:
                hit.setdefault(v._uid, []).append((name, T[c]))
        for u, nd in nodes.items():
            X, Y = xy(u)
            hs = hit.get(u, [])
            copy = pos[u][0] == 1
            fill = hs[0][1] if hs else ((40, 62, 58) if copy else T['panel2'])
            cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10,
                    outline=T['cyan'] if copy else T['border'], width=2)
            cv.text((X, Y), nd.val, 23, T['bg'] if hs else T['text'], anchor='mm', bold=True)
            for i, (name, cc) in enumerate(hs):
                if pos[u][1] == 0:  # 最左列：写在节点上方
                    cv.text((X, Y - nh / 2 - 4 - i * 24), name, 20, cc, anchor='mb', bold=True)
                else:  # 其余：写在节点左上方，避开中线上的箭头
                    cv.text((X - nw / 2 - 4, Y - 6 - i * 24), name, 20, cc, anchor='rb', bold=True)
        cv.text((x0 + 18, rowy[0] - nh / 2 - 92), '上排：原链表', 20, T['dim'])
        cv.text((x0 + 18, rowy[1] + nh / 2 + 70), '下排：新建的拷贝节点（青色边框）', 20, T['dim'])
        cv.text((x1 - 20, rowy[1] + nh / 2 + 70), '紫色弧线 = random', 20, T['purple'], anchor='ra')
    return draw


def _enc(head):
    out, x = [], head
    while x is not None and len(out) < 50:
        out.append(x)
        x = x.next
    idx = {id(v): i for i, v in enumerate(out)}
    return [[v.val, idx.get(id(v.random)) if v.random is not None else None] for v in out]


def _all_new(head):
    x = head
    while x is not None:
        if x._uid in _tr._origin:
            return False
        x = x.next
    return True


def _progress(S):
    nodes = _collect(S)
    d = S.get('dummy')
    N, R = 5, 4  # 示例 1：5 个节点，其中 4 个 random 非空
    copies = [v for u, v in nodes.items() if u not in _tr._origin and v is not d]
    nr = sum(1 for v in copies if v.random is not None)
    s = f'已复制 =={len(copies)}==/{N} 个　·　拷贝的 random 已连 =={nr}==/{R}'
    if d is not None:
        k, x = 0, d.next
        while x is not None and x._uid not in _tr._origin and k < 20:
            k, x = k + 1, x.next
        s += f'　·　新链表已摘出 =={k}==/{N}'
    return s


CONFIG = dict(
    num=138, title='随机链表的复制', difficulty='Medium', category='链表',
    author='灵茶山艾府', technique='交错链表（不用哈希表）',
    code="""
class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # 复制每个节点，把新节点直接插到原节点的后面
        cur = head
        while cur:
            cur.next = Node(cur.val, cur.next)
            cur = cur.next.next

        # 遍历交错链表中的原链表节点
        cur = head
        while cur:
            if cur.random:
                # 要复制的 random 是 cur.random 的下一个节点
                cur.next.random = cur.random.next
            cur = cur.next.next

        # 删除交错链表中的原链表节点，剩下的节点即为新链表
        cur = dummy = Node(0, head)
        while cur.next:
            # 删除原链表的节点，即当前节点的下一个节点
            # 如果要恢复原链表，见另一份代码【Python3 写法二】
            cur.next = cur.next.next
            cur = cur.next

        return dummy.next
""",
    # setup：按示例 1 手动建 Node 并接好 random；_origin 只用于布局（原节点放上排第 1..5 列）
    setup="""
import tracer
_vals, _rnd = [7, 13, 11, 10, 1], [None, 0, 4, 2, 0]
_ns = [Node(v) for v in _vals]
for _i in range(len(_ns) - 1):
    _ns[_i].next = _ns[_i + 1]
for _i, _r in enumerate(_rnd):
    if _r is not None:
        _ns[_i].random = _ns[_r]
for _i, _nd in enumerate(_ns):
    tracer._origin[_nd._uid] = (0, _i + 1)
head = _ns[0]
""",
    call='Solution().copyRandomList(head)',
    expect=[[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
    result_fn=_enc,
    check=_all_new,
    views=[
        dict(type='text', fn=_progress),
        dict(type='custom', draw=_rl_view({'cur': 'blue', 'dummy': 'cyan'}, '交错链表（灰色 = next，紫色 = random，黄色 = 这一步改的）', 5), h=560),
    ],
    watch=[('cur', 'cur', 'blue'), ('cur.next', 'cur.next'), ('cur.random', 'cur.random', 'purple')],
    captions={
        4: '第一轮：从 `head` 开始，给每个节点做一份拷贝',
        'cur.next = Node(cur.val, cur.next)': '新建 `{cur.val}′`，==直接插到== `{cur.val}` ==后面==：`{cur.val} → {cur.val}′ → 原来的下一个`',
        'cur = cur.next.next': lambda S, B, ret: '跳过刚插入的拷贝，`cur` → {}'.format(S.cur.val if S.cur else 'None（这一轮结束）'),
        'while cur:': lambda S, B, ret: '`cur` = {} 是原节点 → 处理它'.format(B.cur.val) if B.cur else '`cur` 为空 → 这一轮结束',
        10: '第二轮：遍历交错链表中的原节点，复制 random',
        'if cur.random:': lambda S, B, ret: ('`{}.random` = {} → 需要复制'.format(B.cur.val, B.cur.random.val) if B.cur.random
                                             else '`{}.random` 为空 → 拷贝的 random 也保持为空'.format(B.cur.val)),
        'cur.next.random = cur.random.next': '原节点的下一个就是它的拷贝：`{cur.val}′.random` = `{cur.random.val}` 的下一个 = =={cur.random.val}′==',
        'cur = dummy = Node(0, head)': '第三轮：哨兵 `dummy` 接在 `head` 前面，准备把原节点摘掉',
        'while cur.next:': lambda S, B, ret: '`cur.next` 不为空 → 继续' if B.cur.next else '`cur.next` 为空 → 摘完了',
        'cur.next = cur.next.next': lambda S, B, ret: '删掉原节点 `{}`：`cur.next` 跳过它，指向 `{}`'.format(
            B.cur.next.val, '{}′'.format(S.cur.next.val) if S.cur.next else 'None'),
        'cur = cur.next': lambda S, B, ret: '`cur` 前进到拷贝节点 `{}′`'.format(S.cur.val),
        'return dummy.next': '`dummy.next` 就是拷贝链表的头 `7′`',
    },
    cards=dict(
        one_liner='把拷贝插在原节点后面：原节点的下一个，就是它的拷贝',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['每个节点多一个 `random` 指针（写成 `[val, random 下标]`）',
                 '构造==深拷贝==：新节点的 `next`/`random` 只能指向新节点',
                 '示例：`[[7,null],[13,0],[11,4],[10,2],[1,0]]`'],
        quote='难道要用哈希表吗？不需要，我们可以把新链表和旧链表「混在一起」……如此一来，==原链表节点的下一个节点，就是其对应的新链表节点了！==',
        quote_src='—— 灵茶山艾府题解',
        idea=['难点：`X.random → Y` 时要找到 `Y` 的==拷贝== `Y′`，一般要哈希表',
              '交错链表 `1→1′→2→2′`：`Y′` ==就是== `Y.next`，不用哈希表',
              '`X.next.random = X.random.next`；最后删掉原节点，剩下 `1′→2′→…`'],
        summary=['三轮遍历：插入拷贝 → 复制 random → 分离；时间 `O(n)`，空间 `O(1)`',
                 '复制 random 必须单独一轮：第一轮时 `random` 指向的节点可能还没有拷贝',
                 '这份 Python 代码删掉原节点后，==原节点的 next 指向了拷贝==；题意要求不改原链表',
                 '写法二用 `tail` 构建新链表，同时 `cur.next = copy.next` 恢复原链表'],
    ),
)
