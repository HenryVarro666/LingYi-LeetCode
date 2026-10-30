import tracer as _tr


def _ll_view(ptrs, title='链表', hide=(), new_row=None):
    """自绘单链表：节点按输入位置固定不动；相邻的正向 next 画直箭头，
    其余（跨越 / 反向）画在节点下方的弧线；指针名写在节点上方；本步改动的 next 标黄。"""
    def collect(S):
        nodes = {}

        def walk(v, d=0):
            if isinstance(v, (list, tuple)) and d < 2:
                for y in v:
                    walk(y, d + 1)
            while isinstance(v, (ListNode, Node)) and v._uid not in nodes:
                nodes[v._uid] = v
                v = v.next
        for k, v in S.items():
            if k not in hide:
                walk(v)
        return nodes

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        nodes, bnodes = collect(S), collect(B)
        org = _tr._origin
        base = max([r for r, c in org.values()] + [-1]) + 1
        pos = {u: org[u] for u in nodes if u in org}
        for k, u in enumerate(sorted(u for u in nodes if u not in org)):
            pos[u] = new_row(k, base) if new_row else (base, k)
        allp = list(org.values()) + list(pos.values())
        R = max(r for r, c in allp) + 1
        C = max(c for r, c in allp) + 1
        gap = min(150, (x1 - x0 - 100) / C)
        nw, nh = min(74, gap * 0.56), 50
        top = y0 + 112
        rowh = min(170, (y1 - top - nh - 50) / max(1, R - 1)) if R > 1 else 0
        top += max(0, ((y1 - y0) - (112 + nh + 140 + (R - 1) * rowh)) / 2)

        def xy(u):
            r, c = pos[u]
            return x0 + 50 + c * gap + nw / 2, top + nh / 2 + r * rowh

        links = {}
        for u, nd in nodes.items():
            if nd.next is not None and nd.next._uid in pos:
                links[pos[u]] = pos[nd.next._uid]
        for u, nd in nodes.items():
            X, Y = xy(u)
            r, c = pos[u]
            nx = nd.next
            bn = bnodes.get(u)
            ch = bn is not None and getattr(bn.next, '_uid', None) != getattr(nx, '_uid', None)
            lc, lw = (T['yellow'], 4) if ch else (T['muted'], 3)
            if nx is None:
                busy = links.get((r, c + 1)) == (r, c)  # 右边邻居有箭头指回来，∅ 挪到上方
                cv.text((X + nw / 2 + 8, Y - (22 if busy else 0)), '∅', 24, T['yellow'] if ch else T['dim'], anchor='lm')
                continue
            if nx._uid not in pos:
                continue
            X2, Y2 = xy(nx._uid)
            r2, c2 = pos[nx._uid]
            both = links.get((r2, c2)) == (r, c)
            if r2 == r and c2 == c + 1:
                dy = -9 if both else 0
                cv.arrow((X + nw / 2 + 2, Y + dy), (X2 - nw / 2 - 3, Y2 + dy), lc, lw, 12)
            elif r2 == r and c2 == c - 1:
                dy = 9 if both else 0
                cv.arrow((X - nw / 2 - 2, Y + dy), (X2 + nw / 2 + 3, Y2 + dy), lc, lw, 12)
            elif r2 == r:
                fwd = c2 > c
                s = nw * 0.2
                p0 = (X + (s if fwd else -s), Y + nh / 2 + 2)
                p1 = (X2 - (s if fwd else -s), Y2 + nh / 2 + 4)
                cv.arc_arrow(p0, p1, -(26 + 15 * abs(c2 - c) + (0 if fwd else 14)), lc, lw, 12)
            else:
                down = r2 > r
                p0 = (X, Y + (nh / 2 if down else -nh / 2))
                p1 = (X2, Y2 - (nh / 2 + 3 if down else -nh / 2 - 3))
                cv.arrow(p0, p1, lc, lw, 12)
        hit = {}
        for k, (name, c) in enumerate(ptrs.items()):
            v = S.get(name.split('.')[0])
            for a in name.split('.')[1:]:
                v = getattr(v, a, None)
            if isinstance(v, (ListNode, Node)) and v._uid in pos:
                hit.setdefault(v._uid, []).append((name, T[c]))
        for u, nd in nodes.items():
            X, Y = xy(u)
            hs = hit.get(u, [])
            fill = hs[0][1] if hs else T['panel2']
            cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10, outline=T['border'], width=2)
            cv.text((X, Y), nd.val, 25, T['bg'] if hs else T['text'], anchor='mm', bold=True)
            for i, (name, cc) in enumerate(hs):
                cv.text((X, Y - nh / 2 - 6 - i * 25), name, 21, cc, anchor='mb', bold=True)
        nones = [n for n in ptrs if n in S and S[n] is None]
        if nones:
            cv.text((x1 - 20, y0 + 6), '  '.join(f'{n}=None' for n in nones), 20, T['muted'], anchor='ra', mono=True)
    return draw


def _groups(S):
    d = S.get('dummy')
    if d is None:
        return ''
    out, x, seen = [], d.next, set()
    while x is not None and id(x) not in seen and len(out) < 12:
        seen.add(id(x)); out.append(str(x.val)); x = x.next
    s = '从 `dummy` 往后读：' + ' → '.join(out) + ' → ∅'
    if 'n' in S and 'last_tail' in S:
        s += f'　　剩余未处理 `n` = {S["n"]}'
    return s


CONFIG = dict(
    num=25, title='K 个一组翻转链表', difficulty='Hard', category='链表',
    author='灵茶山艾府', technique='分组反转 + 哨兵节点',
    code="""
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # 统计节点个数
        n = 0
        cur = head
        while cur:
            n += 1
            cur = cur.next

        # last_tail 是上一组翻转后的尾节点
        last_tail = dummy = ListNode(next=head)

        # k 个一组处理
        while n >= k:
            n -= k

            pre = None
            cur = last_tail.next
            for _ in range(k):  # 同 92 题
                nxt = cur.next
                cur.next = pre  # 每次循环只修改一个 next，方便大家理解
                pre = cur
                cur = nxt

            # 请结合视频中的图理解
            # 翻转后：
            # pre 是当前组的头节点
            # cur 是下一组的起始节点
            # last_tail 是上一组的尾节点
            # last_tail.next 是当前组的尾节点
            tail = last_tail.next
            tail.next = cur  # 当前组的尾节点指向下一组的起始节点
            last_tail.next = pre  # 上一组的尾节点指向当前组的头节点
            last_tail = tail

        return dummy.next
""",
    # setup 只做布局：把运行中创建的第一个节点（dummy）放在第 0 行最左边，原链表整体右移一格
    setup="""
import tracer, itertools
head = L([1,2,3,4,5])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
""",
    call='Solution().reverseKGroup(head, 2)',
    expect=[2, 1, 4, 3, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_groups),
        dict(type='custom', draw=_ll_view({'last_tail': 'purple', 'pre': 'pink', 'cur': 'blue', 'nxt': 'green', 'tail': 'orange', 'dummy': 'cyan'},
                                          title='链表（黄色 = 这一步改的 next）'), h=430),
    ],
    watch=['n', ('last_tail', 'last_tail', 'purple'), ('pre', 'pre', 'pink'), ('cur', 'cur', 'blue'), ('nxt', 'nxt', 'green')],
    skip=['n += 1', 'cur = cur.next'],  # 计数循环只保留 while 行
    captions={
        'n = 0': '先数一数有多少个节点：决定能分出几个完整的组',
        'cur = head': '`cur` 从头开始数',
        'while cur:': lambda S, B, ret: ('数到第 {} 个节点 `{}`'.format(S.n + 1, B.cur.val) if B.cur
                                         else '数完了：一共 `n` = {} 个节点'.format(S.n)),
        'last_tail = dummy': '哨兵 `dummy` 当作“上一组的尾巴” `last_tail`：第一组也能统一处理',
        'while n >= k': lambda S, B, ret: ('剩余 `{}` ≥ `k` = {} → 还能凑出完整一组，翻转它'.format(B.n, S.k) if B.n >= S.k
                                           else '剩余 `{}` < `k` → ==不足一组，保持原样==，结束'.format(B.n)),
        'n -= k': '这一组用掉 `k` 个：剩余 `n` = {n}',
        'pre = None': '组内反转同 206/92 题：`pre` 从空开始',
        'cur = last_tail.next': '`cur` = 这一组的第一个节点 `{cur.val}`（`last_tail` 的下一个）',
        'for _ in range(k)': lambda S, B, ret: ('组内第 {} 次：反转一根 next'.format(S._ + 1) if '_' not in B or S._ != B._
                                               else '这一组 `k` 个节点都反转完了'),
        'nxt = cur.next': lambda S, B, ret: '先存下 `nxt` = {}：改完 `cur.next` 就找不到它了'.format(S.nxt.val if S.nxt else 'None'),
        'cur.next = pre': lambda S, B, ret: '`{}.next` 改成 `pre`（{}）：这一根箭头反向'.format(S.cur.val, S.pre.val if S.pre else 'None'),
        'pre = cur': '`pre` 前进到 `{pre.val}`',
        'cur = nxt': lambda S, B, ret: '`cur` 前进到 {}'.format(S.cur.val if S.cur else 'None'),
        'tail = last_tail.next': '反转后：`pre`={pre.val} 是组头，`cur` 是下一组起点；`last_tail.next`（`{tail.val}`）==变成了组尾==',
        'tail.next = cur': lambda S, B, ret: '组尾 `{}` 接上下一组的起点 `{}`'.format(S.tail.val, S.cur.val if S.cur else 'None'),
        'last_tail.next = pre': lambda S, B, ret: '上一组的尾巴 `{}` 接上这一组的新头 `{}`'.format(
            'dummy' if S.last_tail is S.dummy else S.last_tail.val, S.pre.val),
        'last_tail = tail': '`last_tail` 移到这一组的尾巴 `{last_tail.val}`，准备处理下一组',
        'return dummy.next': '返回 `dummy.next`',
    },
    cards=dict(
        one_liner='组内照抄反转链表，组间用 last_tail 把首尾接好',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每 `k` 个节点一组翻转，返回修改后的链表',
                 '最后剩余不足 `k` 个的节点==保持原有顺序==；只能改指针',
                 '示例：`[1,2,3,4,5], k = 2` → `[2,1,4,3,5]`'],
        quote='翻转后：pre 是当前组的头节点，cur 是下一组的起始节点，last_tail 是上一组的尾节点，last_tail.next 是当前组的尾节点。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['先数出 `n`：每处理一组 `n -= k`，`n < k` 就停，剩下的不动',
              '组内用 206 题的 `pre/cur/nxt` 反转 `k` 次',
              '反转后原组头变==组尾==：组尾接 `cur`，`last_tail` 接 `pre`，再移动 `last_tail`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '前置题：206 反转链表、92 反转链表 II；本题 = 92 题重复做',
                 '易错：先取 `tail = last_tail.next`，再改 `last_tail.next`',
                 '写法二不先数 `n`：每组先试探走 `k` 步，不足 `k` 个就直接返回'],
    ),
)
