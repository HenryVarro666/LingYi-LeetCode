import sys as _sys
import tracer as _tr


def _up(name, test, depth=16):
    # 取调用栈上层的局部变量（custom 视图只拿到合并后的 S；这里取完整帧列表与全部关键帧）
    f = _sys._getframe(2)
    for _ in range(depth):
        if f is None:
            return None
        v = f.f_locals.get(name)
        if v is not None and test(v):
            return v
        f = f.f_back
    return None


def _reach(frames, S):
    vals = [v for fr in frames for v in fr['locals'].values()] if frames else list(S.values())
    nodes = {}
    for v in vals:
        while isinstance(v, ListNode) and v._uid not in nodes:
            nodes[v._uid] = v
            v = v.next
    return nodes


def _ll(ptrs, title='链表', place=None, deco=None):
    """自绘链表：相邻节点用直箭头（反向链接走下方车道），远距离链接画在节点下方的弧线；
    指针名写在节点上方；这一步改动过的 next 用黄色；已经没有变量指向的节点画成暗色（ghost）。"""
    cache = {}

    def history():
        vid = _up('self', lambda x: hasattr(x, 'keys') and hasattr(x, 'draw_viz'))
        if vid is None:
            return []
        if id(vid) not in cache:
            order, seen = [], set()
            for stt, _, _ in vid.keys:
                S_ = stt.get('_S')
                if S_ is None or id(S_) in seen:
                    continue
                seen.add(id(S_))
                order.append((id(S_), _reach(stt.get('_frames'), S_)))
            cache[id(vid)] = order
        return cache[id(vid)]

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        st = _up('st', lambda x: isinstance(x, dict) and '_S' in x) or {}
        nodes = _reach(st.get('_frames'), S)
        hist = history()
        idx = next((i for i, (k, _) in enumerate(hist) if k == id(S)), None)
        ghost = {}
        if idx is not None:
            for j in range(idx - 1, -1, -1):
                for u, nd in hist[j][1].items():
                    if u not in nodes and u not in ghost:
                        ghost[u] = nd
        bnodes = _reach(None, B)
        if idx:
            for u, nd in hist[idx - 1][1].items():
                bnodes.setdefault(u, nd)
        alln = dict(ghost)
        alln.update(nodes)
        org = _tr._origin
        base = max([r for r, c in org.values()] + [-1]) + 1
        every = set(alln)
        for _, nd in hist:
            every |= set(nd)
        pos = {u: org[u] for u in every if u in org}
        for k, u in enumerate(sorted(u for u in every if u not in org)):
            pos[u] = place(k, base) if place else (base, k)
        allp = list(org.values()) + list(pos.values())
        R = max(r for r, c in allp) + 1
        C = max(c for r, c in allp) + 1
        gap = min(150, (x1 - x0 - 100) / C)
        nw, nh = min(84, gap * 0.58), 60
        top = y0 + 118
        rowh = min(180, (y1 - top - nh - 50) / max(1, R - 1)) if R > 1 else 0
        top = max(top, (y0 + y1) / 2 + 20 - (nh + rowh * (R - 1)) / 2)
        left = x0 + max(50, (x1 - x0 - C * gap) / 2 + (gap - nw) / 2 - 10)

        def xy(u):
            r, c = pos[u]
            return left + c * gap + nw / 2, top + nh / 2 + r * rowh

        fwd, back = set(), set()
        for u, nd in alln.items():
            r, c = pos[u]
            p2 = pos.get(getattr(nd.next, '_uid', None))
            if nd.next is None or p2 == (r, c + 1):
                fwd.add((r, c))
            elif p2 == (r, c - 1):
                back.add((r, c - 1))
        both = fwd & back
        for u, nd in alln.items():
            X, Y = xy(u)
            r, c = pos[u]
            nx = nd.next
            bn = bnodes.get(u)
            ch = bn is not None and getattr(bn.next, '_uid', None) != getattr(nx, '_uid', None)
            lc, lw = (T['yellow'], 4) if ch else ((T['dim'], 2) if u in ghost else (T['muted'], 3))
            if nx is None:
                cv.text((X + nw / 2 + 8, Y - (11 if (r, c) in both else 0)), '∅', 24,
                        T['yellow'] if ch else T['dim'], anchor='lm')
                continue
            if nx._uid not in pos:
                continue
            X2, Y2 = xy(nx._uid)
            r2, c2 = pos[nx._uid]
            if r2 == r and c2 == c + 1:
                d = -11 if (r, c) in both else 0
                cv.arrow((X + nw / 2, Y + d), (X2 - nw / 2 - 2, Y2 + d), lc, lw, 12)
            elif r2 == r and c2 == c - 1:
                d = 11 if (r, c2) in both else 0
                cv.arrow((X - nw / 2, Y + d), (X2 + nw / 2 + 2, Y2 + d), lc, lw, 12)
            elif r2 == r:
                cv.arc_arrow((X, Y + nh / 2), (X2, Y2 + nh / 2 + 2), -(34 + abs(X2 - X) * 0.1), lc, lw, 12)
            else:
                if abs(X2 - X) < 1:  # 竖直箭头往右偏一点，避开节点上方的指针名
                    X, X2 = X + nw * 0.3, X2 + nw * 0.3
                dx, dy = X2 - X, Y2 - Y
                t0 = min((nw / 2) / abs(dx) if dx else 9e9, (nh / 2) / abs(dy) if dy else 9e9)
                t1 = t0 + 4 / math.hypot(dx, dy)
                cv.arrow((X + dx * t0, Y + dy * t0), (X2 - dx * t1, Y2 - dy * t1), lc, lw, 12)
        hit = {}
        for name, cc in ptrs.items():
            v = S.get(name)
            if isinstance(v, ListNode):
                hit.setdefault(v._uid, []).append((name, T[cc]))
        for u, nd in alln.items():
            X, Y = xy(u)
            hs = hit.get(u, [])
            bn = bnodes.get(u)
            vch = bn is not None and bn.val != nd.val
            gh = u in ghost
            fill = hs[0][1] if hs else ((24, 28, 35) if gh else T['panel2'])
            cv.rect((X - nw / 2, Y - nh / 2, X + nw / 2, Y + nh / 2), fill=fill, r=10,
                    outline=T['yellow'] if vch else T['border'], width=4 if vch else 2)
            cv.text((X, Y), str(nd.val), 30, T['bg'] if hs else (T['dim'] if gh else T['text']), anchor='mm', bold=True)
            for k, (name, cc) in enumerate(hs):
                cv.text((X, Y - nh / 2 - 6 - k * 26), name, 22, cc, anchor='mb', bold=True)
        if deco:
            deco(cv, S, alln, xy, T)
        nones = [n for n in ptrs if n in S and S[n] is None]
        if nones:
            cv.text((x1 - 20, y0 + 6), '  '.join(f'{n}=None' for n in nones), 20, T['muted'], anchor='ra', mono=True)
    return draw


def _v(x):
    return '∅' if x is None else str(x.val)


def _res(S):
    if S.get('now') is None:
        return '（还没有写入）'
    return '[' + ','.join(map(str, list_vals(S['head']))) + ']'


def _deco(cv, S, nodes, xy, T):
    inv = {(r, c): u for u, (r, c) in _tr._origin.items()}
    for (r, c), lab in (((0, 0), 'l1'), ((1, 0), 'l2')):
        u = inv.get((r, c))
        if u in nodes:
            X, Y = xy(u)
            cv.text((X - 52, Y), lab, 24, T['muted'], anchor='rm', bold=True)


CONFIG = dict(
    num=2, title='两数相加', difficulty='Medium', category='链表',
    author='yiduobo', technique='模拟竖式加法 · 进位标记',
    code='''
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        add_flag = 0
        head = ListNode(0)
        now = None

        while l1 != None or l2 != None or add_flag != 0:
            sum = add_flag
            if l1:
                sum += l1.val
                l1 = l1.next
            if l2:
                sum += l2.val
                l2 = l2.next

            add_flag = sum // 10
            sum %= 10

            if not now:
                head.val = sum
                now = head
            else:
                new_node = ListNode(sum)
                now.next = new_node
                now = new_node

        return head
''',
    call='Solution().addTwoNumbers(L([9, 9]), L([1]))',
    expect=[0, 0, 1],
    result_fn=list_vals,
    views=[
        dict(type='text', fn=lambda S: f'`99 + 1 = 100`（逆序存放）　　结果：=={_res(S)}==', size=26),
        dict(type='custom', h=520, draw=_ll({'now': 'yellow', 'l1': 'blue', 'l2': 'pink', 'head': 'purple'},
                                             title='上两行：l1、l2（同一列是同一位）　最下行：结果链表', deco=_deco)),
    ],
    watch=[('add_flag', 'add_flag', 'orange'), ('sum', 'sum', 'green')],
    captions={
        3: '进位标记 `add_flag = 0`：加法每次最多进 1，用一个标记记录即可',
        4: '结果链表的头 `head`：先建好，第一位算出来再把值填进去',
        5: '`now = None`：结果链表还没有写入任何一位',
        7: lambda S, B, r: (('两个链表都走到头了，但==最高位有进位== → 还要再算一位（细节 3）'
                             if S.l1 is None and S.l2 is None else '还有节点没加完 → 继续')
                            if (S.l1 is not None or S.l2 is not None or S.add_flag != 0) else '都走完了，也没有进位 → 结束'),
        8: lambda S, B, r: f'`sum` 先等于进位 `{S.add_flag}`',
        9: lambda S, B, r: f'`l1` 还有节点（{S.l1.val}）' if S.l1 else '`l1` 已经走完 → 跳过',
        10: lambda S, B, r: f'`sum += {B.l1.val}` → `{S.sum}`',
        11: lambda S, B, r: f'`l1` 后移 → `{_v(S.l1)}`',
        12: lambda S, B, r: (f'`l2` 还有节点（{S.l2.val}）' if S.l2 else
                             ('`l2` 已经走完 → 跳过，==只走另一个链表==（细节 2）' if S.sum != S.add_flag
                              else '`l2` 也走完了 → 跳过')),
        13: lambda S, B, r: f'`sum += {B.l2.val}` → `{S.sum}`',
        14: lambda S, B, r: f'`l2` 后移 → `{_v(S.l2)}`',
        16: lambda S, B, r: (f'`add_flag = sum // 10 = {S.add_flag}`' + ('：==进位==（细节 1）' if S.add_flag else '')
                             + ('。原文 `sum / 10` 是 Python 2 整除，这里改为 `//`' if B.now is None else '')),
        17: lambda S, B, r: f'`sum %= 10` → 这一位是 `{S.sum}`',
        19: lambda S, B, r: ('`now` 为空：这是第一位 → 直接写进 `head`' if S.now is None else
                             '已经有结果了 → 新建节点接在后面'),
        20: lambda S, B, r: f'`head.val = {S.sum}`',
        21: '`now = head`：`now` 指向结果链表的末尾',
        23: lambda S, B, r: f'新建节点 `ListNode({S.sum})`',
        24: '`now.next = new_node`：接到结果链表末尾',
        25: '`now` 移到新节点',
        27: lambda S, B, r: f'返回 `head` → ==[{",".join(map(str, list_vals(r)))}]==，即 `100`',
    },
    cards=dict(
        one_liner='逐位相加，管好三个细节：进位、一条先走完、最高位进位',
        complexity='时间 `O(max(m,n))`，空间 `O(1)`（不计结果）',
        problem=['两个==非空==链表表示两个非负整数，数字==逆序==存储，每个节点存一位',
                 '把两数相加，以同样的形式返回和的链表',
                 '示例：`l1 = [9,9]`，`l2 = [1]` → `[0,0,1]`（99 + 1 = 100）'],
        quote='1、进位的处理……每次最多进1，用一个标记记录一下即可。2、指针同时移动时某个链表走完了。此时需要继续走另一个链表。3、两个链表都走到头时==最高位有进位==。',
        quote_src='—— yiduobo 题解',
        idea=['相加之后链表指针同时往后移动；`add_flag` 记录进位',
              '某个链表走完了，就只加另一个链表的节点',
              '循环条件带上 `add_flag != 0`：最高位的进位也会写进结果'],
        summary=['时间 `O(max(m,n))`，空间 `O(1)`（不计结果链表）',
                 '没用哨兵节点：第一位直接写进 `head`，用 `now` 是否为空来区分',
                 '原文为 Python 2 写法：`sum / 10` 改为 `sum // 10`，删掉文档字符串',
                 '变量名 `sum` 会遮住内置函数 `sum()`，自己写时建议换个名字'],
    ),
)
