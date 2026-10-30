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


def _order(S):
    d = S.get('p_head')
    if d is None:
        return ''
    out, x, seen = [], d.next, set()
    while x is not None and id(x) not in seen and len(out) < 12:
        seen.add(id(x)); out.append(str(x.val)); x = x.next
    if x is not None:
        out.append(f'（回到 {x.val}）')  # 归并途中两段没断开，可能暂时成环
    s = '从 `p_head` 往后读：' + ' → '.join(out)
    if 'step' in S:
        s += f'　　`step` = =={S["step"]}=='
    return s


def _pick(S, B, ret):
    if B.cnt1 == B.l1:
        return '第一部分已取完 → 只能取 `part2` 的 `{}`'.format(B.part2.val)
    if B.cnt2 == B.l2:
        return '第二部分已取完 → 取 `part1` 的 `{}`'.format(B.part1.val)
    if B.part1.val > B.part2.val:
        return '`{} > {}` → 取 `part2`'.format(B.part1.val, B.part2.val)
    return '`{} ≤ {}` → 取 `part1`'.format(B.part1.val, B.part2.val)


CONFIG = dict(
    num=148, title='排序链表', difficulty='Medium', category='链表',
    author='yiduobo', technique='倍增步长的自底向上归并',
    code='''
class Solution(object):
    def sortList(self, head):
        if not head:
            return head

        p_head = ListNode(0)
        p_head.next = head

        now = head
        l = 0
        while now:
            l += 1
            now = now.next

        step = 1
        while step < l:
            last_node = p_head
            while last_node.next:
                part1 = last_node.next
                now = last_node
                l1 = 0
                while l1 < step and now.next:
                    l1 += 1
                    now = now.next
                if not now.next:
                    break

                part2 = now.next
                l2 = 0
                while l2 < step and now.next:
                    l2 += 1
                    now = now.next

                next_part = now.next

                cnt1 = cnt2 = 0
                while cnt1 < l1 or cnt2 < l2:
                    choose_one = True
                    if cnt1 == l1 or ((cnt2 != l2) and (part1.val > part2.val)):
                        choose_one = False

                    if choose_one:
                        last_node.next = part1
                        last_node = part1
                        part1 = part1.next
                        cnt1 += 1
                    else:
                        last_node.next = part2
                        last_node = part2
                        part2 = part2.next
                        cnt2 += 1

                last_node.next = next_part

            step += step

        return p_head.next
''',
    # setup 只做布局：把运行中创建的第一个节点（假头 p_head）放在第 0 行最左边，原链表整体右移一格
    setup="""
import tracer, itertools
head = L([4,2,1,3])
for _u in list(tracer._origin): tracer._origin[_u] = (0, tracer._origin[_u][1] + 1)
_n = next(tracer._uid); tracer._uid = itertools.count(_n); tracer._origin[_n] = (0, 0)
""",
    call='Solution().sortList(head)',
    expect=[1, 2, 3, 4],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=_order),
        dict(type='custom', draw=_ll_view({'last_node': 'purple', 'part1': 'blue', 'part2': 'pink', 'now': 'green',
                                           'next_part': 'orange', 'p_head': 'cyan'},
                                          title='链表（最左边是假头 p_head；黄色 = 这一步改的 next）'), h=430),
    ],
    watch=['step', 'l1', 'l2', 'cnt1', 'cnt2'],
    # 走路、计数、选边的碎步不单独成一步（状态变化会体现在下一步里）
    skip=['while now:', 'l += 1', 'now = now.next', 'l1 += 1', 'l2 += 1', 'l1 = 0', 'l2 = 0', 'cnt1 = cnt2 = 0',
          'while l1 < step', 'while l2 < step',
          'choose_one = True', 'choose_one = False', 'if choose_one', 'last_node = part1', 'last_node = part2',
          'part1 = part1.next', 'part2 = part2.next', 'cnt1 += 1', 'cnt2 += 1'],
    captions={
        'if not head': '`head` 非空，不用特判',
        'p_head = ListNode(0)': '先加入一个假头 `p_head` 方便计算',
        'p_head.next = head': '假头接在原链表前面',
        'now = head': '先用 `now` 走一遍，数出链表长度 `l`',
        'l = 0': '计数器 `l` 从 0 开始（数数的循环略过，下一步直接看结果）',
        'step = 1': '链表长度 `l` = {l}；步长 `step` 从 1 开始',
        'while step < l': lambda S, B, ret: ('`step` = {} < `l` → 新一趟：从头开始，每次划出两段长 `step` 的部分归并'.format(B.step)
                                             if B.step < B.l else '`step` = {} ≥ `l`：整条链已经有序，结束'.format(B.step)),
        'last_node = p_head': '`last_node` = 已完成排序部分的最后一个节点，初始为 `p_head`',
        'while last_node.next': lambda S, B, ret: ('`last_node` 后面还有节点 → 继续划分' if B.last_node.next else
                                                   '`last_node` 后面没有了 → 这一趟结束'),
        'part1 = last_node.next': '第一部分的头 `part1` 一定是 `last_node.next`（{part1.val}）',
        'now = last_node': '`now` 从 `last_node` 出发，往后走 `step` 位',
        'if not now.next': lambda S, B, ret: ('走了 {} 位后 `now.next` 为空：没有第二部分 → 不用归并'.format(S.l1) if not B.now.next else
                                              '走了 `l1` = {} 位，`now.next` 就是第二部分的头'.format(S.l1)),
        'break': '`break`：剩下这段原样保留，这一趟结束',
        'part2 = now.next': '`part2` = {part2.val}',
        'next_part = now.next': lambda S, B, ret: '第二部分走了 `l2` = {} 位；先记下后面的 `next_part` = {}'.format(
            S.l2, S.next_part.val if S.next_part else 'None'),
        'while cnt1 < l1 or cnt2 < l2': lambda S, B, ret: ('还没取完：`part1` 段已取 {}/{}，`part2` 段已取 {}/{}'.format(B.cnt1, B.l1, B.cnt2, B.l2)
                                                           if B.cnt1 < B.l1 or B.cnt2 < B.l2 else '两段都取完了'),
        'if cnt1 == l1 or': _pick,
        'last_node.next = part1': '把 `{last_node.next.val}` 接到 `last_node` 后面（随后 `last_node`、`part1` 各前进一位）',
        'last_node.next = part2': '把 `{last_node.next.val}` 接到 `last_node` 后面（随后 `last_node`、`part2` 各前进一位）',
        'last_node.next = next_part': lambda S, B, ret: '这两段归并完毕：末尾接上 `next_part`（{}）'.format(
            S.next_part.val if S.next_part else 'None'),
        'step += step': '倍增：`step` = {step}',
        'return p_head.next': '返回 `p_head.next`',
    },
    cards=dict(
        one_liner='step = 1, 2, 4…：每趟把相邻两段长 step 的有序段归并',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['给链表头 `head`，按==升序==排序后返回',
                 '要求 `O(n log n)` 时间、`O(1)` 空间',
                 '示例：`[4,2,1,3]` → `[1,2,3,4]`'],
        quote='需要递归的，例如快排、归并，或者需要额外空间的，例如堆排都不能达成要求。在这里，可以运用倍增的思想，逐步归并排序。',
        quote_src='—— yiduobo 题解',
        idea=['设置步长 `step`，每次从头划分出两个长度为 `step` 的部分归并',
              '`step` 倍增直到 ≥ 链表长度；`[4,2,1,3]` → `[2,4][1,3]` → `[1,2,3,4]`',
              '每趟 `O(n)`，`log n` 趟 ⇒ `O(n log n)`；只改指针，空间 `O(1)`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`：满足进阶要求',
                 '`last_node`：已排好部分的最后一个节点；第一段的头总是 `last_node.next`',
                 '易错：归并前先记下 `next_part`，归并完 `last_node.next = next_part` 接回去',
                 '两段并没有断开，靠 `l1`/`l2` 计数判断段尾（中途可能暂时成环，不影响）',
                 '原文为 Python 2 写法：仅删掉了 `"""type"""` 文档字符串，逻辑未改'],
    ),
)
