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


def _chains(S):
    names = ['start', 'last_one'] if 'last_one' in S and S.get('cnt') else ['new_head']
    parts = []
    for name in names:
        v = S.get(name)
        if v is None:
            continue
        chain, x, k = [f'{name}({v.val})'], v.next, 0
        while x is not None and k < 4:
            chain.append(str(x.val))
            x, k = x.next, k + 1
        chain.append('∅' if x is None else '…')
        parts.append(' → '.join(chain))
    return '　|　'.join(parts)


CONFIG = dict(
    num=25, title='K 个一组翻转链表', difficulty='Hard', category='链表',
    author='yiduobo', technique='计数分组 + 逐个插到 right 前',
    code="""
class Solution(object):
    def reverseKGroup(self, head, k):
        new_head = ListNode(0)
        new_head.next = head

        left = new_head
        now = head
        cnt = 0
        start = None
        while now:
            cnt += 1
            if cnt == 1:
                start = now
                now = now.next
            elif cnt == k:
                right = now.next
                left.next = now
                left = start
                last_one = right
                while start != now:
                    tmp = start
                    start = start.next
                    tmp.next = last_one
                    last_one = tmp
                now = start.next
                start.next = last_one
                cnt = 0
            else:
                now = now.next

        return new_head.next
""",
    # setup 只做布局：把运行中创建的第一个节点（假头）放在第 0 行最左边，原链表整体右移一格
    setup="""
import tracer, itertools
head = L([1,2,3,4,5])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
""",
    call='Solution().reverseKGroup(head, 3)',
    expect=[3, 2, 1, 4, 5],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_chains),
        dict(type='custom', draw=_ll_view({'left': 'purple', 'start': 'blue', 'now': 'pink', 'right': 'green',
                                           'last_one': 'orange', 'tmp': 'red', 'new_head': 'cyan'},
                                          title='链表（最左边是假头 new_head；黄色 = 这一步改的 next）'), h=430),
    ],
    watch=['cnt', ('start', 'start', 'blue'), ('now', 'now', 'pink'), ('last_one', 'last_one', 'orange')],
    captions={
        'new_head = ListNode(0)': '增加一个假头 `new_head`：用来充当前 `k` 个节点的 `left`',
        'new_head.next = head': '假头接在原链表前面',
        'left = new_head': '`left`：这一组左边的那个节点',
        'now = head': '`now` 从头开始往后走，`cnt` 记录走到这一组的第几个',
        'while now:': lambda S, B, ret: '`now` 不为空 → 继续' if B.now else '`now` 走到空了：剩下的不足 `k` 个，==保持原顺序==，结束',
        'cnt += 1': '`cnt` = {cnt}：`now`（{now.val}）是这一组的第 {cnt} 个',
        'if cnt == 1': lambda S, B, ret: '`cnt == 1` → 记下这一组的头部 `start`' if S.cnt == 1 else '`cnt` ≠ 1',
        'start = now': '`start` = node_1 = `{start.val}`',
        'now = now.next': lambda S, B, ret: '`now` 往后走一步 → {}'.format(S.now.val if S.now else 'None'),
        'elif cnt == k': lambda S, B, ret: ('`cnt == k`：`now` 停在了 node_k（{}），开始翻转这一组'.format(S.now.val) if S.cnt == S.k
                                            else '`cnt` = {} < `k`：还没凑够一组，继续走'.format(S.cnt)),
        'right = now.next': lambda S, B, ret: '`right` = node_k 的下一个（{}）'.format(S.right.val if S.right else 'None'),
        'left.next = now': '`left.next = now`：old_left 直接指向 node_k（翻转后它就是组头）',
        'left = start': '翻转后 node_1 会成为后面部分的 `left` → `left = start`',
        'last_one = right': lambda S, B, ret: '`last_one`：当前节点在答案中的下一个；node_1 的就是 `right`（{}）'.format(
            S.right.val if S.right else 'None'),
        'while start != now': lambda S, B, ret: ('`start` 还没到 `now` → 把 `start` 插到 `last_one` 前面' if B.start is not B.now
                                                 else '`start` 走到 `now` 了：前 `k-1` 个都插好了'),
        'tmp = start': '取出当前节点 `tmp` = `{tmp.val}`',
        'start = start.next': '`start` 先后移到 `{start.val}`（不然改完 `tmp.next` 就找不到了）',
        'tmp.next = last_one': '把 `{tmp.val}` 插在 `{last_one.val}` 前面：`tmp.next = last_one`',
        'last_one = tmp': '`last_one` 更新为 `{last_one.val}`：下一个节点要插在它前面',
        'now = start.next': lambda S, B, ret: '先把 `now` 移到 `right`（`start.next` = {}），继续后面的操作'.format(
            S.now.val if S.now else 'None'),
        'start.next = last_one': 'node_k（`{start.val}`）接上 `last_one`（`{last_one.val}`）：==这一组翻转完成==',
        8: '`cnt` = 0：这一组还一个没数',
        9: '`start` 是这一组的头部，先置空',
        27: '`cnt` 清零，开始数下一组',
        'return new_head.next': '返回 `new_head.next`',
    },
    cards=dict(
        one_liner='先数够 k 个，再把 node_1…node_k-1 逐个插到 right 前面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每 `k` 个节点一组翻转，返回修改后的链表',
                 '最后剩余不足 `k` 个的节点==保持原有顺序==；只能改指针',
                 '示例：`[1,2,3,4,5], k = 3` → `[3,2,1,4,5]`'],
        quote='我们只需要将(2)中的节点，从start开始到now，一个一个插在right的前方即可。我们定义一个last_one表示当前处理节点在答案中的下一个节点是什么。',
        quote_src='—— yiduobo 题解',
        idea=['数到第 `k` 个（node_k）：先 `left.next = now`，再 `left = start`',
              '`last_one` 从 `right` 开始；`start` 逐个取出、插到 `last_one` 前面',
              '最后 `now = start.next` 移到 `right`，`start.next = last_one` 合并'],
        summary=['时间 `O(n)`，空间 `O(1)`；不足 `k` 个的尾巴 `cnt` 数不满，自然不动',
                 '易错：插入前先 `start = start.next`，否则改完 `tmp.next` 就断了',
                 '注意 `k = 1` 时 `cnt == 1` 分支会先命中，原代码相当于不翻转（结果恰好也对）',
                 '原文为 Python 2 写法：仅删掉了 `"""type"""` 文档字符串，逻辑未改'],
    ),
)
